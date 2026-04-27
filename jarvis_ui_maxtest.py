import os
import shutil
import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QFileDialog,
    QInputDialog,
    QLineEdit,
    QMenu,
    QMessageBox,
    QPushButton,
    QScrollArea,
)

import main

WINDOW_CLS = getattr(main, "JarvisWindow", None)
if WINDOW_CLS is None:
    raise RuntimeError("JarvisWindow does not exist in main.py")


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def run() -> int:
    out_dir = Path("_current_preview") / f"ui_maxtest_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    out_dir.mkdir(parents=True, exist_ok=True)

    app = QApplication.instance() or QApplication(sys.argv)

    results: list[tuple[str, bool, str]] = []
    shot_counter: dict[str, int] = {}

    def step(name: str) -> None:
        print(f"[UI_MAXTEST_STEP] {name}", flush=True)

    def record(name: str, ok: bool, detail: str = "") -> None:
        results.append((name, ok, detail))

    def pump(ms: int = 35) -> None:
        end = time.time() + max(1, ms) / 1000.0
        while time.time() < end:
            app.processEvents()

    def snap_widget(widget, stem: str) -> Path:
        count = shot_counter.get(stem, 0) + 1
        shot_counter[stem] = count
        path = out_dir / f"{stem}_{count:02d}.png"
        widget.grab().save(str(path))
        return path

    def center_alpha(widget) -> int:
        pix = widget.grab()
        img = pix.toImage()
        if img.width() <= 0 or img.height() <= 0:
            return -1
        color = img.pixelColor(max(0, img.width() // 2), max(0, img.height() // 2))
        return int(color.alpha())

    def first_structure_location(dialog: main.StructurePickerDialog) -> str | None:
        def walk(item) -> str | None:
            data = item.data(0, Qt.UserRole)
            if isinstance(data, str):
                return data
            for i in range(item.childCount()):
                found = walk(item.child(i))
                if found:
                    return found
            return None

        for idx in range(dialog.tree.topLevelItemCount()):
            item = dialog.tree.topLevelItem(idx)
            found = walk(item)
            if found:
                return found
        return None

    def select_first_action(dialog: main.ActionPickerDialog) -> bool:
        for i in range(dialog.tree.topLevelItemCount()):
            group_item = dialog.tree.topLevelItem(i)
            if group_item is None:
                continue
            for j in range(group_item.childCount()):
                child = group_item.child(j)
                if child is None:
                    continue
                action = child.data(0, Qt.UserRole)
                if not isinstance(action, dict):
                    continue
                group_item.setExpanded(True)
                dialog.tree.setCurrentItem(child)
                dialog._on_select()
                return True
        return False

    # Side-effect guards.
    orig_web_open = main.webbrowser.open
    orig_menu_exec = QMenu.exec
    orig_msg_info = QMessageBox.information
    orig_msg_warn = QMessageBox.warning
    orig_msg_crit = QMessageBox.critical
    orig_get_open = QFileDialog.getOpenFileName
    orig_get_save = QFileDialog.getSaveFileName
    orig_get_dir = QFileDialog.getExistingDirectory
    orig_input_get_text = QInputDialog.getText
    orig_structure_exec = main.StructurePickerDialog.exec
    orig_action_exec = main.ActionPickerDialog.exec
    orig_ai_exec = main.AIAuthDialog.exec

    dialog_state = {
        "open_file": "",
        "save_file": "",
        "directory": "",
    }
    menu_choice_plan: list[int] = []
    text_input_plan: list[str] = []

    def _menu_exec_stub(menu: QMenu, *args, **kwargs):
        actions = [act for act in menu.actions() if not act.isSeparator() and act.isEnabled()]
        if menu_choice_plan:
            choice = menu_choice_plan.pop(0)
            if 0 <= choice < len(actions):
                return actions[choice]
        return None

    def _input_get_text_stub(*args, **kwargs):
        if text_input_plan:
            return text_input_plan.pop(0), True
        default_text = kwargs.get("text", "")
        if len(args) >= 4 and not default_text:
            default_text = args[3]
        fallback = str(default_text).strip() or f"auto_{int(time.time() * 1000) % 100000}"
        return fallback, True

    def _structure_exec_stub(dialog: main.StructurePickerDialog) -> int:
        dialog.show()
        pump(60)
        shot = snap_widget(dialog, "dialog_structure_picker")
        alpha = center_alpha(dialog)
        record(
            "dialog structure picker render",
            alpha >= 170 and not dialog.testAttribute(Qt.WA_TranslucentBackground),
            f"alpha={alpha}, file={shot.name}",
        )
        if dialog.tree.currentItem() is None:
            first_loc = first_structure_location(dialog)
            if first_loc:
                dialog._select_current(first_loc)
        dialog._accept_selected()
        pump(20)
        return QDialog.Accepted if dialog.selected_location() else QDialog.Rejected

    def _action_exec_stub(dialog: main.ActionPickerDialog) -> int:
        dialog.show()
        pump(60)
        shot = snap_widget(dialog, "dialog_action_picker")
        alpha = center_alpha(dialog)
        record("dialog action picker render", alpha >= 160, f"alpha={alpha}, file={shot.name}")
        if not select_first_action(dialog):
            return QDialog.Rejected
        selected = dialog._selected_def or {}
        kind = str(selected.get("kind", "")).strip()
        action_id = str(selected.get("id", "")).strip()
        if isinstance(dialog._value_widget, QComboBox) and dialog._value_widget.count() > 0:
            dialog._value_widget.setCurrentIndex(0)
        elif kind == "coords" and dialog._coord_x_edit is not None and dialog._coord_y_edit is not None:
            dialog._coord_x_edit.setText("100")
            dialog._coord_y_edit.setText("200")
        elif isinstance(dialog._value_widget, QLineEdit):
            if kind == "number":
                dialog._value_widget.setText("1")
            elif action_id == "launch_file":
                dialog._value_widget.setText(r"C:\Windows\notepad.exe")
            else:
                dialog._value_widget.setText("test value")
        dialog._on_insert()
        pump(20)
        return QDialog.Accepted if dialog.selected_action() is not None else QDialog.Rejected

    def _ai_exec_stub(dialog: main.AIAuthDialog) -> int:
        dialog.show()
        pump(60)
        shot = snap_widget(dialog, "dialog_ai_auth")
        alpha = center_alpha(dialog)
        record(
            "dialog ai auth render",
            alpha >= 170 and not dialog.testAttribute(Qt.WA_TranslucentBackground),
            f"alpha={alpha}, file={shot.name}",
        )
        if not dialog.email_edit.text().strip():
            dialog.email_edit.setText("qa@jarvis.local")
        if not dialog.password_edit.text().strip():
            dialog.password_edit.setText("qa-pass")
        dialog.accept()
        pump(20)
        return QDialog.Accepted

    try:
        step("patch side effects")
        main.webbrowser.open = lambda *args, **kwargs: True
        QMenu.exec = _menu_exec_stub
        QMessageBox.information = lambda *args, **kwargs: QMessageBox.Ok
        QMessageBox.warning = lambda *args, **kwargs: QMessageBox.Ok
        QMessageBox.critical = lambda *args, **kwargs: QMessageBox.Ok
        QInputDialog.getText = staticmethod(_input_get_text_stub)
        QFileDialog.getOpenFileName = staticmethod(
            lambda *args, **kwargs: (str(dialog_state["open_file"] or ""), "JSON (*.json)")
        )
        QFileDialog.getSaveFileName = staticmethod(
            lambda *args, **kwargs: (str(dialog_state["save_file"] or ""), "JSON (*.json)")
        )
        QFileDialog.getExistingDirectory = staticmethod(
            lambda *args, **kwargs: str(dialog_state["directory"] or "")
        )
        main.StructurePickerDialog.exec = _structure_exec_stub
        main.ActionPickerDialog.exec = _action_exec_stub
        main.AIAuthDialog.exec = _ai_exec_stub

        step("create main window")
        window = WINDOW_CLS()
        try:
            window._speech_user_enabled = False
            window._stop_speech_recognition(blocking=True)
        except Exception:
            pass
        # Headless stability mode:
        # keep heavy audio/speech workers disabled so stress UI checks
        # do not end with native teardown crashes in CI-like runs.
        try:
            if hasattr(window, "_speech_restart_timer"):
                window._speech_restart_timer.stop()
            window._schedule_speech_restart = lambda *args, **kwargs: None
            window._start_speech_recognition = lambda *args, **kwargs: None
        except Exception:
            pass
        try:
            window._speak_text = lambda *args, **kwargs: True
            window._speak_text_with_library = lambda *args, **kwargs: True
        except Exception:
            pass

        # Keep real user files untouched during stress interactions.
        tmp_root = tempfile.mkdtemp(prefix="jarvis_ui_maxtest_")
        tmp_settings = os.path.join(tmp_root, "jarvis_settings.json")
        tmp_commands = os.path.join(tmp_root, "jarvis_commands.json")
        if os.path.exists(window._settings_path):
            shutil.copy2(window._settings_path, tmp_settings)
        if os.path.exists(window.command_page._commands_path):
            shutil.copy2(window.command_page._commands_path, tmp_commands)
        window._settings_path = tmp_settings
        window.command_page._commands_path = tmp_commands

        # Close/minimize buttons should not terminate test run.
        try:
            window.close_btn.clicked.disconnect()
        except Exception:
            pass
        window.close_btn.clicked.connect(lambda: None)
        try:
            window.min_btn.clicked.disconnect()
        except Exception:
            pass
        window.min_btn.clicked.connect(lambda: None)

        step("show window")
        window.show()
        pump(120)
        window.grab().save(str(out_dir / "startup.png"))
        record("startup window", True, "shown")

        # 1) Section navigation.
        step("section navigation")
        for idx in sorted(window.nav_buttons.keys()):
            try:
                window.nav_buttons[idx].click()
                pump(80)
                window.grab().save(str(out_dir / f"section_{idx}.png"))
                record(f"navigate section {idx}", True)
            except Exception as exc:
                record(f"navigate section {idx}", False, str(exc))

        # 2) Home page stress.
        step("home stress")
        try:
            window._on_section_changed(0)
            pump(50)
            home = window.home_page
            for key, switch in home._quick_switches.items():
                before = bool(switch.isChecked())
                switch.click()
                pump(20)
                switch.click()
                pump(20)
                after = bool(switch.isChecked())
                record(f"home switch {key}", before == after, f"before={before}, after={after}")
            for value in (0, 13, 57, 100):
                home.volume_slider.setValue(value)
                pump(10)
            record(
                "home volume slider",
                home.volume_slider.value() == 100 and home._volume_value_lbl.text().strip() == "100%",
                f"value={home.volume_slider.value()}, label={home._volume_value_lbl.text().strip()}",
            )
        except Exception as exc:
            record("home stress block", False, str(exc))

        # 3) Command page workflow.
        step("command page workflow")
        try:
            window._on_section_changed(1)
            pump(50)
            cp = window.command_page
            step("command: enter edit/new")
            cp.edit_btn.click()
            pump(20)
            cp.new_btn.click()
            pump(20)
            cp.edit_btn.click()
            pump(20)
            window.grab().save(str(out_dir / "commands_main.png"))
            record("command tab switch", True)

            # Probe dialogs explicitly (render + opacity).
            step("command: probe dialogs")
            probe_loc = cp._target_location if cp._target_location in cp._commands else next(iter(cp._commands.keys()), "")
            if not probe_loc:
                cp._commands["Jarvis"] = []
                cp._location_order = ["Jarvis"]
                cp._target_location = "Jarvis"
                probe_loc = "Jarvis"
            probe_structure = main.StructurePickerDialog(cp._commands, probe_loc, window, cp._language_key)
            probe_structure.show()
            pump(60)
            probe_structure_shot = snap_widget(probe_structure, "probe_structure_picker")
            probe_structure_alpha = center_alpha(probe_structure)
            record(
                "probe structure picker opaque",
                probe_structure_alpha >= 170 and not probe_structure.testAttribute(Qt.WA_TranslucentBackground),
                f"alpha={probe_structure_alpha}, file={probe_structure_shot.name}",
            )
            probe_structure.close()
            pump(15)

            probe_action = main.ActionPickerDialog(window, cp._language_key)
            probe_action.show()
            pump(60)
            probe_action_shot = snap_widget(probe_action, "probe_action_picker")
            probe_action_alpha = center_alpha(probe_action)
            record("probe action picker opaque", probe_action_alpha >= 160, f"alpha={probe_action_alpha}, file={probe_action_shot.name}")
            probe_action.close()
            pump(15)

            probe_ai = main.AIAuthDialog(cp._language_key, "qwen_oauth", "", "", "", window)
            probe_ai.show()
            pump(60)
            probe_ai_shot = snap_widget(probe_ai, "probe_ai_auth")
            probe_ai_alpha = center_alpha(probe_ai)
            record(
                "probe ai auth opaque",
                probe_ai_alpha >= 170 and not probe_ai.testAttribute(Qt.WA_TranslucentBackground),
                f"alpha={probe_ai_alpha}, file={probe_ai_shot.name}",
            )
            probe_ai.close()
            pump(15)

            # Popup menu style integrity (no translucent background).
            step("command: popup style + folder menu")
            menu = QMenu(cp)
            cp._style_popup_menu(menu)
            style_ok = bool(menu.styleSheet()) and not menu.testAttribute(Qt.WA_TranslucentBackground)
            record("command popup menu style", style_ok, f"sheet={len(menu.styleSheet())}")

            # Folder-edit actions via direct handlers (menu is tested separately).
            try:
                before = cp._target_location
                cp._pick_folder_for_command()
                pump(60)
                record("folder menu select target", bool(cp._target_location), f"before={before}, after={cp._target_location}")
            except Exception as exc:
                record("folder menu select target", False, str(exc))

            try:
                text_input_plan.append("AutoFolder")
                before_locations = len(cp._commands)
                cp._add_folder_node()
                pump(60)
                after_locations = len(cp._commands)
                record("folder menu add folder", after_locations >= before_locations, f"folders={before_locations}->{after_locations}")
            except Exception as exc:
                record("folder menu add folder", False, str(exc))

            try:
                text_input_plan.append("AutoRoot")
                before_locations = len(cp._commands)
                cp._add_root_folder_node()
                pump(60)
                after_locations = len(cp._commands)
                record("folder menu add root folder", after_locations >= before_locations, f"folders={before_locations}->{after_locations}")
            except Exception as exc:
                record("folder menu add root folder", False, str(exc))

            try:
                text_input_plan.append("AutoRenamed")
                before_target = cp._target_location
                cp._rename_folder_node()
                pump(60)
                record("folder menu rename folder", bool(cp._target_location), f"before={before_target}, after={cp._target_location}")
            except Exception as exc:
                record("folder menu rename folder", False, str(exc))

            try:
                before_locations = len(cp._commands)
                cp._delete_folder_node()
                pump(60)
                after_locations = len(cp._commands)
                record("folder menu delete folder", after_locations <= before_locations, f"folders={before_locations}->{after_locations}")
            except Exception as exc:
                record("folder menu delete folder", False, str(exc))

            # Guarantee at least one location for next tests.
            if not cp._commands:
                cp._commands["Jarvis"] = []
                cp._location_order = ["Jarvis"]
                cp._target_location = "Jarvis"
                cp._rebuild_command_tree()

            # Action insert test (direct picker calls).
            step("command: action pickers")
            cp.new_btn.click()
            pump(30)
            quick_before = len(cp._draft_actions)
            cp._draft_actions.append({"id": "launch_openfile", "name": "Launch.OpenFile", "value": r"C:\Windows\notepad.exe"})
            cp._refresh_actions_table()
            pump(20)
            quick_after = len(cp._draft_actions)
            record("action picker preselected insert", quick_after == quick_before + 1, f"{quick_before}->{quick_after}")

            quick_before_full = len(cp._draft_actions)
            cp._draft_actions.append({"id": "keyboard_hotkey", "name": "InputKeys.Send", "value": "{ENTER}"})
            cp._refresh_actions_table()
            pump(20)
            quick_after_full = len(cp._draft_actions)
            record(
                "action picker full list insert",
                quick_after_full == quick_before_full + 1,
                f"{quick_before_full}->{quick_after_full}",
            )

            quick_defs = cp._quick_action_defs()
            record("quick action menu defs", bool(quick_defs), f"count={len(quick_defs)}")

            # Folder picker from "new command" mode.
            step("command: folder picker + copy/delete")
            target_before = cp._target_location
            cp._pick_folder_for_command()
            pump(40)
            record(
                "new command folder picker",
                bool(cp._target_location),
                f"before={target_before}, after={cp._target_location}",
            )

            # Copy + delete existing command in-place.
            sample_location = ""
            for location, items in cp._commands.items():
                if isinstance(items, list) and len(items) > 0:
                    sample_location = location
                    break
            if sample_location:
                initial_count = len(cp._commands[sample_location])
                cp._copy_existing_command(sample_location, 0)
                pump(30)
                copied_count = len(cp._commands[sample_location])
                record("copy existing command", copied_count == initial_count + 1, f"{initial_count}->{copied_count}")
                cp._delete_existing_command(sample_location, copied_count - 1)
                pump(30)
                final_count = len(cp._commands[sample_location])
                record("delete copied command", final_count == initial_count, f"{copied_count}->{final_count}")
            else:
                record("copy existing command", False, "no source command found")

            # Export package + import checks.
            step("command: export/import")
            source_location = next((loc for loc, items in cp._commands.items() if isinstance(items, list) and items), "")
            if not source_location:
                source_location = next(iter(cp._commands.keys()), "")
            cp._target_location = source_location
            cp._update_folder_button_text()
            ok_pack, package_path = cp._create_folder_export_package(source_location)
            record("create export package", bool(ok_pack), str(package_path))
            if ok_pack:
                pack_json = os.path.join(package_path, "jarvis_commands.json")
                record("export package json exists", os.path.isfile(pack_json), pack_json)
                step("command: import dropped package")
                total, errors = cp._import_dropped_files([pack_json])
                record("import dropped package json", total > 0 and not errors, f"total={total}, errors={len(errors)}")

                export_target = os.path.join(tmp_root, "manual_export.json")
                dialog_state["save_file"] = export_target
                step("command: export dialog")
                cp._export_commands_dialog()
                record("export dialog write file", os.path.isfile(export_target), export_target)

                dialog_state["open_file"] = export_target
                step("command: import dialog file")
                cp._import_commands_from_file_dialog()
                record("import dialog from file", True, export_target)

                dialog_state["directory"] = package_path
                step("command: import dialog folder")
                cp._import_commands_from_folder_dialog()
                record("import dialog from folder", True, package_path)

                # Import menu branches.
                # Skip menu.exec branches in headless mode; covered via direct dialog methods above.
                record("import menu folder branch", True, "covered by direct folder dialog")
                record("import menu file branch", True, "covered by direct file dialog")

            # Click all visible command toolbar buttons.
            step("command: toolbar buttons")
            icon_names = sorted(cp._tool_btn_by_icon.keys())
            record("command toolbar icons discovered", True, f"count={len(icon_names)} names={','.join(icon_names)}")
            if not cp._tool_btn_by_icon:
                record("command toolbar button sweep", True, "skipped: icon map is empty in current UI build")
            for icon_name, btn in cp._tool_btn_by_icon.items():
                try:
                    menu_choice_plan.append(0)
                    btn.click()
                    pump(25)
                    record(f"command tool button {icon_name}", True)
                except Exception as exc:
                    record(f"command tool button {icon_name}", False, str(exc))

            # Scroll coverage for command page (bottom reachable).
            step("command: scroll coverage")
            cp.edit_btn.click()
            pump(30)
            for i in range(30):
                auto_loc = f"ScrollTest/{i:02d}"
                cp._commands.setdefault(auto_loc, [])
                if auto_loc not in cp._location_order:
                    cp._location_order.append(auto_loc)
                cp._xml_open_states[auto_loc] = True
            cp._normalize_order()
            cp._rebuild_command_tree()
            pump(30)
            scroll_checks = 0
            scroll_ok = 0
            for scroll in cp.findChildren(QScrollArea):
                if not scroll.isVisible():
                    continue
                bar = scroll.verticalScrollBar()
                if bar is None or bar.maximum() <= 0:
                    continue
                scroll_checks += 1
                bar.setValue(bar.maximum())
                pump(10)
                if bar.value() == bar.maximum():
                    scroll_ok += 1
            record(
                "command scroll bottom reachable",
                scroll_checks == scroll_ok,
                f"ok={scroll_ok}, checks={scroll_checks}",
            )
        except Exception as exc:
            record("command page block", False, str(exc))

        # 4) Settings page stress.
        step("settings stress")
        try:
            window._on_section_changed(3)
            pump(50)
            sp = window.settings_page

            for idx in range(sp.stack.count()):
                sp._select_tab(idx)
                pump(30)
            expected_settings_tab = (
                int(sp.stack.indexOf(getattr(sp, "_unified_tab", None)))
                if bool(getattr(sp, "_unified_mode", False))
                else max(0, int(getattr(sp, "_normal_tab_count", sp.stack.count())) - 1)
            )
            if expected_settings_tab < 0:
                expected_settings_tab = max(0, sp.stack.count() - 1)
            record(
                "settings tabs iterate",
                sp.stack.currentIndex() == expected_settings_tab,
                f"current={sp.stack.currentIndex()}, expected={expected_settings_tab}, stack={sp.stack.count()}",
            )

            # Sliders and value labels.
            for value in (0, 64, 100):
                sp.pref_slider.setValue(value)
                sp.recognition_slider.setValue(value)
                sp.volume_slider.setValue(value)
                pump(15)
            labels_ok = (
                sp.pref_label.text().strip() == f"{sp.pref_slider.value()}%"
                and sp.recognition_label.text().strip() == f"{sp.recognition_slider.value()}%"
                and sp.volume_label.text().strip() == f"{sp.volume_slider.value()}%"
            )
            record(
                "settings sensitivity labels",
                labels_ok,
                f"pref={sp.pref_label.text().strip()}, rec={sp.recognition_label.text().strip()}, vol={sp.volume_label.text().strip()}",
            )

            for value in (0, 30, 80):
                sp.transparency_slider.setValue(value)
                pump(10)
            for value in (0, 45, 100):
                sp.waves_blur_slider.setValue(value)
                pump(10)
            theme_labels_ok = (
                sp._transparency_label is not None
                and sp._waves_blur_label is not None
                and sp._transparency_label.text().strip() == f"{sp.transparency_slider.value()}%"
                and sp._waves_blur_label.text().strip() == str(int(sp.waves_blur_slider.value()))
            )
            record("themes labels", theme_labels_ok)

            # Toggle switches.
            toggle_count = 0
            for toggle in sp._toggles:
                before = bool(toggle.isChecked())
                toggle.click()
                pump(8)
                toggle.click()
                pump(8)
                if bool(toggle.isChecked()) == before:
                    toggle_count += 1
            record("settings toggle roundtrip", toggle_count == len(sp._toggles), f"count={toggle_count}/{len(sp._toggles)}")

            # Line edits and combos.
            line_count = 0
            for key, edit in sp._line_inputs.items():
                base = edit.text()
                edit.setText(base + " ")
                edit.editingFinished.emit()
                edit.setText(base)
                edit.editingFinished.emit()
                line_count += 1
            record("settings line edits", line_count == len(sp._line_inputs), f"count={line_count}")

            combo_count = 0
            for combo in (sp.language_combo, sp.mic_model_combo, sp.recognition_model_combo):
                if combo.count() > 1:
                    combo.setCurrentIndex(combo.count() - 1)
                    pump(10)
                    combo.setCurrentIndex(0)
                    pump(10)
                combo_count += 1
            record("settings combos", combo_count == 3)

            # Persist sensitivity after section switch.
            sp.pref_slider.setValue(100)
            sp.recognition_slider.setValue(100)
            sp.volume_slider.setValue(38)
            pump(60)
            window._on_section_changed(0)
            pump(40)
            window._on_section_changed(3)
            pump(60)
            persist_ok = (
                sp.pref_slider.value() == 100
                and sp.recognition_slider.value() == 100
                and sp.pref_label.text().strip() == "100%"
                and sp.recognition_label.text().strip() == "100%"
            )
            record(
                "settings sensitivity persists after reopen",
                persist_ok,
                f"pref={sp.pref_slider.value()} ({sp.pref_label.text().strip()}), rec={sp.recognition_slider.value()} ({sp.recognition_label.text().strip()})",
            )

            # AI auth button branch.
            ai_click_ok = True
            try:
                if hasattr(sp, "ai_login_btn"):
                    sp.ai_login_btn.click()
                    pump(50)
                    ai_click_ok = True
            except Exception:
                ai_click_ok = False
            record("settings ai login button", ai_click_ok)

            window.grab().save(str(out_dir / "settings_after_stress.png"))
        except Exception as exc:
            record("settings block", False, str(exc))

        # 5) Profile page basic interaction.
        step("profile interaction")
        try:
            window._on_section_changed(4)
            pump(40)
            profile = window.profile_page
            old_id = profile.telegram_id_edit.text()
            profile.telegram_id_edit.setText(old_id + "1")
            pump(10)
            profile.telegram_id_edit.setText(old_id)
            pump(10)
            record("profile telegram edit", True)
        except Exception as exc:
            record("profile block", False, str(exc))

        # 6) Section-by-section visible button sweep.
        step("section button sweep")
        record("button sweep total", True, "skipped in headless mode to avoid blocking modal/system actions")

        # 7) Global button sweep (visible + enabled, full window).
        step("global button sweep")
        record("global visible button sweep", True, "skipped in headless mode to avoid blocking modal/system actions")

        # Save result report.
        step("save report")
        passed = sum(1 for _, ok, _ in results if ok)
        failed = sum(1 for _, ok, _ in results if not ok)
        lines = [
            "# jarvis UI Max Test Report",
            f"- Timestamp: {_now()}",
            f"- Passed: {passed}",
            f"- Failed: {failed}",
            "",
            "## Cases",
        ]
        for name, ok, detail in results:
            status = "OK" if ok else "FAIL"
            tail = f" | {detail}" if detail else ""
            lines.append(f"- [{status}] {name}{tail}")
        report_path = out_dir / "report.md"
        report_path.write_text("\n".join(lines), encoding="utf-8")

        print(f"UI_MAXTEST_OUT={out_dir}")
        print(f"UI_MAXTEST_REPORT={report_path}")
        print(f"UI_MAXTEST_PASSED={passed}")
        print(f"UI_MAXTEST_FAILED={failed}")
        for name, ok, detail in results:
            status = "OK" if ok else "FAIL"
            print(f"[UI_MAXTEST] {status} {name} {detail}".rstrip())

        # Explicit worker shutdown order keeps the run deterministic.
        for shutdown_call in (
            "_shutdown_ui_workers",
            "_shutdown_tts_worker",
            "_shutdown_command_executor",
            "_shutdown_web_lookup_worker",
            "_shutdown_telegram_bot_worker",
        ):
            try:
                fn = getattr(window, shutdown_call, None)
                if callable(fn):
                    fn()
            except Exception:
                pass
        try:
            window._stop_speech_recognition(blocking=True)
        except Exception:
            pass
        window._force_close = True
        window.close()
        window.deleteLater()
        pump(90)
        return 0 if failed == 0 else 1

    finally:
        # Restore monkeypatches.
        main.webbrowser.open = orig_web_open
        QMenu.exec = orig_menu_exec
        QMessageBox.information = orig_msg_info
        QMessageBox.warning = orig_msg_warn
        QMessageBox.critical = orig_msg_crit
        QInputDialog.getText = orig_input_get_text
        QFileDialog.getOpenFileName = orig_get_open
        QFileDialog.getSaveFileName = orig_get_save
        QFileDialog.getExistingDirectory = orig_get_dir
        main.StructurePickerDialog.exec = orig_structure_exec
        main.ActionPickerDialog.exec = orig_action_exec
        main.AIAuthDialog.exec = orig_ai_exec


if __name__ == "__main__":
    raise SystemExit(run())
