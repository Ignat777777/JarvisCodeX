import os
import time

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QSystemTrayIcon

import main


def _pump(app: QApplication, ms: int = 120) -> None:
    end = time.time() + max(1, int(ms)) / 1000.0
    while time.time() < end:
        app.processEvents()
        time.sleep(0.008)


def run() -> int:
    app = QApplication.instance() or QApplication([])
    orig_is_tray_available = QSystemTrayIcon.isSystemTrayAvailable
    QSystemTrayIcon.isSystemTrayAvailable = staticmethod(lambda: True)
    win = main.JarvisWindow()
    try:
        # Stabilize headless run: disable async speech restart side effects.
        try:
            win._speech_user_enabled = False
            win._stop_speech_recognition(blocking=True)
        except Exception:
            pass
        try:
            if hasattr(win, "_speech_restart_timer"):
                win._speech_restart_timer.stop()
            win._schedule_speech_restart = lambda *args, **kwargs: None
            win._start_speech_recognition = lambda *args, **kwargs: None
        except Exception:
            pass

        win.show()
        _pump(app, 220)

        # Case 1: close_to_tray ON + click X => app hides to tray.
        win._on_setting_changed("close_to_tray", True)
        _pump(app, 120)
        assert bool(win._settings.get("close_to_tray", False)), "close_to_tray setting was not applied"
        assert win.isVisible(), "window must be visible before close"
        win._on_close_clicked()
        _pump(app, 220)
        assert not win.isVisible(), "window must be hidden to tray when close_to_tray is enabled"
        tray = getattr(win, "_tray_icon", None)
        assert tray is not None, "tray icon object must exist"
        if bool(QSystemTrayIcon.isSystemTrayAvailable()):
            assert bool(tray.isVisible()), "tray icon must remain visible when system tray is available"

        # Case 2: restore from tray.
        win._restore_from_tray()
        _pump(app, 220)
        assert win.isVisible(), "window must restore from tray"

        # Case 3: explicit quit from tray still fully exits.
        win._quit_from_tray()
        _pump(app, 280)
        assert not win.isVisible(), "window must close on tray quit"

        print("TRAY_CLOSE_SMOKE_OK")
        return 0
    finally:
        try:
            QSystemTrayIcon.isSystemTrayAvailable = orig_is_tray_available
        except Exception:
            pass
        try:
            win._force_close = True
            win.close()
            _pump(app, 120)
        except Exception:
            pass


if __name__ == "__main__":
    raise SystemExit(run())
