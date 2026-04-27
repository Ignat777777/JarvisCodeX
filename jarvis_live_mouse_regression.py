import os
import sys
import time
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication, QWidget

import main


WINDOW_CLS = getattr(main, "JarvisWindow", None)
if WINDOW_CLS is None:
    raise RuntimeError("JarvisWindow does not exist in main.py")


def _pump(app: QApplication, ms: int = 120) -> None:
    end = time.time() + max(1, int(ms)) / 1000.0
    while time.time() < end:
        app.processEvents()
        QTest.qWait(8)


def _safe_name(value: str) -> str:
    out = []
    for ch in str(value):
        if ch.isalnum() or ch in ("_", "-", "."):
            out.append(ch)
        else:
            out.append("_")
    return "".join(out)[:120]


def _mouse_drag_qtest(app: QApplication, widget: QWidget, delta: QPoint) -> None:
    start = widget.rect().center()
    end = start + QPoint(int(delta.x()), int(delta.y()))
    QTest.mousePress(widget, Qt.LeftButton, Qt.NoModifier, start, delay=10)
    _pump(app, 20)
    steps = 6
    for i in range(1, steps + 1):
        x = int(start.x() + (end.x() - start.x()) * i / steps)
        y = int(start.y() + (end.y() - start.y()) * i / steps)
        QTest.mouseMove(widget, QPoint(x, y), delay=10)
        _pump(app, 16)
    QTest.mouseRelease(widget, Qt.LeftButton, Qt.NoModifier, end, delay=10)
    _pump(app, 80)


def _mouse_drag_manual(app: QApplication, widget: QWidget, delta: QPoint) -> None:
    start_local = widget.rect().center()
    end_local = start_local + QPoint(int(delta.x()), int(delta.y()))
    start_global = widget.mapToGlobal(start_local)
    end_global = widget.mapToGlobal(end_local)
    press = QMouseEvent(
        QMouseEvent.Type.MouseButtonPress,
        start_local,
        start_global,
        Qt.LeftButton,
        Qt.LeftButton,
        Qt.NoModifier,
    )
    QApplication.sendEvent(widget, press)
    _pump(app, 20)
    steps = 6
    for i in range(1, steps + 1):
        x = int(start_local.x() + (end_local.x() - start_local.x()) * i / steps)
        y = int(start_local.y() + (end_local.y() - start_local.y()) * i / steps)
        lp = QPoint(x, y)
        gp = widget.mapToGlobal(lp)
        move = QMouseEvent(
            QMouseEvent.Type.MouseMove,
            lp,
            gp,
            Qt.NoButton,
            Qt.LeftButton,
            Qt.NoModifier,
        )
        QApplication.sendEvent(widget, move)
        _pump(app, 16)
    release = QMouseEvent(
        QMouseEvent.Type.MouseButtonRelease,
        end_local,
        end_global,
        Qt.LeftButton,
        Qt.NoButton,
        Qt.NoModifier,
    )
    QApplication.sendEvent(widget, release)
    _pump(app, 80)


def _override_delta(before: dict[str, float], after: dict[str, float]) -> float:
    keys = ("dx", "dy", "dw", "dh")
    total = 0.0
    for k in keys:
        total += abs(float(after.get(k, 0.0)) - float(before.get(k, 0.0)))
    return total


def _center_global(widget: QWidget) -> QPoint:
    return widget.mapToGlobal(widget.rect().center())


def run() -> int:
    out_dir = Path("_current_preview") / f"live_mouse_regression_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    out_dir.mkdir(parents=True, exist_ok=True)
    app = QApplication.instance() or QApplication(sys.argv)
    results: list[tuple[str, bool, str]] = []
    shots: list[str] = []

    def record(name: str, ok: bool, detail: str = "") -> None:
        results.append((name, ok, detail))
        print(f"[LIVE-MOUSE] {name}: {'OK' if ok else 'FAIL'} {detail}".strip(), flush=True)

    def snap(widget: QWidget, stem: str) -> None:
        file_name = f"{len(shots) + 1:02d}_{_safe_name(stem)}.png"
        path = out_dir / file_name
        widget.grab().save(str(path))
        shots.append(file_name)

    win = WINDOW_CLS()
    try:
        win.show()
        _pump(app, 280)
        snap(win, "main_open")

        try:
            win._speech_user_enabled = False
            win._stop_speech_recognition(blocking=True)
        except Exception:
            pass

        # 1) Switch sections by mouse clicks.
        nav_ok = True
        for idx in (0, 1, 2, 3):
            btn = win.nav_buttons.get(idx)
            if not isinstance(btn, QWidget):
                nav_ok = False
                record(f"nav click section {idx}", False, "button missing")
                continue
            QTest.mouseClick(btn, Qt.LeftButton, Qt.NoModifier, btn.rect().center(), delay=10)
            _pump(app, 180)
            actual = int(win.stack.currentIndex())
            ok = actual == idx
            nav_ok = nav_ok and ok
            record(f"nav click section {idx}", ok, f"stack_index={actual}")
        snap(win, "after_nav_clicks")
        if not nav_ok:
            record("mouse nav scenario", False, "not all sections switched by click")

        # 2) In settings, toggle "output text window" by mouse (window mode).
        settings_page = win.settings_page
        tab_buttons = list(getattr(settings_page, "_tab_buttons", []) or [])
        if len(tab_buttons) > 0 and isinstance(tab_buttons[0], QWidget):
            QTest.mouseClick(tab_buttons[0], Qt.LeftButton, Qt.NoModifier, tab_buttons[0].rect().center(), delay=10)
            _pump(app, 140)
        output_switch = getattr(settings_page, "output_text_switch", None)
        if not isinstance(output_switch, QWidget):
            record("window mode switch exists", False, "output_text_switch missing")
            return 1

        # Force a deterministic user path: click off then on.
        if bool(getattr(output_switch, "isChecked", lambda: False)()):
            QTest.mouseClick(output_switch, Qt.LeftButton, Qt.NoModifier, output_switch.rect().center(), delay=10)
            _pump(app, 200)
        QTest.mouseClick(output_switch, Qt.LeftButton, Qt.NoModifier, output_switch.rect().center(), delay=10)
        _pump(app, 300)
        wnd = getattr(win, "_output_window", None)
        output_visible = bool(isinstance(wnd, QWidget) and wnd.isVisible())
        record("window mode enabled by mouse", output_visible, f"main_visible={win.isVisible()}")
        if not output_visible:
            return 1
        snap(wnd, "output_window_open")

        # 3) Type /редактировать настройки in output window and submit with Enter.
        console = getattr(wnd, "_console", None)
        if not isinstance(console, QWidget):
            record("output console exists", False, "console missing")
            return 1
        try:
            wnd.raise_()
            wnd.activateWindow()
        except Exception:
            pass
        _pump(app, 80)
        console.setFocus()
        _pump(app, 80)
        cmd = "/\u0440\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u043d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438"
        try:
            if hasattr(console, "_move_cursor_to_end"):
                console._move_cursor_to_end()
            console.insertPlainText(cmd)
        except Exception:
            QApplication.clipboard().setText(cmd)
            QTest.keyClick(console, Qt.Key_V, Qt.ControlModifier)
        QTest.keyClick(console, Qt.Key_Return)
        _pump(app, 520)
        if not bool(win.isVisible()):
            try:
                if hasattr(console, "command_submitted"):
                    console.command_submitted.emit(cmd)
            except Exception:
                pass
            _pump(app, 420)
        section_key = win._section_key_from_index(int(win.stack.currentIndex()))
        edit_enabled = bool(win._settings_drag_enabled())
        restored = bool(win.isVisible()) and section_key == "settings" and (not edit_enabled)
        record(
            "command /редактировать from output window",
            restored,
            f"main_visible={win.isVisible()} section={section_key} settings_drag_enabled={edit_enabled}",
        )
        snap(win, "after_edit_command")
        if not restored:
            return 1

        # 4) In Settings section drag must be locked: no geometry edits.
        _pump(app, 220)
        mapping = win._settings_draggable_widgets()
        visible_items = {
            str(key): widget
            for key, widget in mapping.items()
            if isinstance(widget, QWidget) and widget.isVisible()
        }
        preferred_keys = [
            "prefix_edit",
            "language_combo",
            "mic_model_combo",
            "bind_edit",
            "ai_model_edit",
            "recognition_model_combo",
        ]
        human_key1 = ""
        widget1: QWidget | None = None
        for key in preferred_keys:
            candidate = visible_items.get(key)
            if isinstance(candidate, QWidget):
                human_key1 = key
                widget1 = candidate
                break
        if widget1 is None:
            for key, widget in visible_items.items():
                if key.startswith("settings."):
                    human_key1 = key
                    widget1 = widget
                    break
        if widget1 is None:
            record("settings drag targets", False, "no visible draggable settings widget found")
            return 1

        human_key2 = ""
        widget2: QWidget | None = None
        for key in preferred_keys:
            candidate = visible_items.get(key)
            if isinstance(candidate, QWidget) and id(candidate) != id(widget1):
                human_key2 = key
                widget2 = candidate
                break
        if widget2 is None:
            candidate = visible_items.get("title")
            if isinstance(candidate, QWidget) and id(candidate) != id(widget1):
                human_key2 = "title"
                widget2 = candidate
        if widget2 is None:
            for key, widget in visible_items.items():
                if id(widget) != id(widget1):
                    human_key2 = key
                    widget2 = widget
                    break
        if widget2 is None:
            record("settings drag targets", False, "could not pick witness widget")
            return 1

        key1, _ = win._settings_drag_target_by_widget(widget1)
        key2, _ = win._settings_drag_target_by_widget(widget2)
        if not key1 or not key2:
            record("settings drag targets", False, "could not resolve active drag keys")
            return 1
        before1 = dict(win._widget_override_values("settings", key1))
        before2 = dict(win._widget_override_values("settings", key2))
        center1_before = _center_global(widget1)
        center2_before = _center_global(widget2)

        _mouse_drag_qtest(app, widget1, QPoint(220, 48))
        after1 = dict(win._widget_override_values("settings", key1))
        qtest_delta_1 = _override_delta(before1, after1)
        if qtest_delta_1 <= 0.0:
            _mouse_drag_manual(app, widget1, QPoint(220, 48))
            after1 = dict(win._widget_override_values("settings", key1))
        after2 = dict(win._widget_override_values("settings", key2))
        center1_after = _center_global(widget1)
        center2_after = _center_global(widget2)
        delta1 = _override_delta(before1, after1)
        delta2 = _override_delta(before2, after2)
        center_delta1 = int((center1_after - center1_before).manhattanLength())
        center_delta2 = int((center2_after - center2_before).manhattanLength())
        locked = (delta1 == 0.0) and (delta2 == 0.0)
        record(
            "mouse drag is blocked in settings",
            locked,
            (
                f"key1={key1}({human_key1}) delta1={delta1:.2f} center1={center_delta1} "
                f"key2={key2}({human_key2}) delta2={delta2:.2f} center2={center_delta2}"
            ),
        )
        record("settings object remains visible", bool(widget1.isVisible()), f"key1={key1}")
        snap(win, "after_settings_drag")

    finally:
        report_lines = [
            "# live mouse regression",
            f"- timestamp: {datetime.now().isoformat(timespec='seconds')}",
            f"- out_dir: {out_dir}",
            "",
        ]
        for name, ok, detail in results:
            marker = "OK" if ok else "FAIL"
            report_lines.append(f"- [{marker}] {name} {detail}".rstrip())
        if shots:
            report_lines.append("")
            report_lines.append("## screenshots")
            for file_name in shots:
                report_lines.append(f"- {file_name}")
        (out_dir / "report.md").write_text("\n".join(report_lines), encoding="utf-8")

        try:
            win._set_ui_editor_mode(False)
        except Exception:
            pass
        try:
            if hasattr(win, "_output_window") and win._output_window is not None:
                win._output_window.hide()
        except Exception:
            pass
        try:
            win._shutdown_command_executor()
        except Exception:
            pass
        try:
            win._stop_speech_recognition(blocking=True)
        except Exception:
            pass
        win.close()
        _pump(app, 120)

    failed = [r for r in results if not r[1]]
    print(f"LIVE_MOUSE_REPORT={out_dir}", flush=True)
    if failed:
        print(f"LIVE_MOUSE_REGRESSION_FAILED={len(failed)}", flush=True)
        return 1
    print("LIVE_MOUSE_REGRESSION_OK", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(run())
