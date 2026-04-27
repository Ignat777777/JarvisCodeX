import json
import os
import tempfile
import threading
import time
import types
from collections import Counter

import main

WINDOW_CLS = getattr(main, "JarvisWindow", None)
if WINDOW_CLS is None:
    raise RuntimeError("JarvisWindow does not exist in main.py")

RU_CLOSE_ALL = "\u0437\u0430\u043a\u0440\u043e\u0439 \u0432\u0441\u0435 \u043e\u043a\u043d\u0430"
RU_CLOSE_ALL_PLEASE = (
    "\u0437\u0430\u043a\u0440\u043e\u0439 \u0432\u0441\u0435 \u043e\u043a\u043d\u0430 "
    "\u043f\u043e\u0436\u0430\u043b\u0443\u0439\u0441\u0442\u0430"
)
RU_PREFIX = "\u0434\u0436\u0430\u0440\u0432\u0438\u0441"
RU_CONFIRM = "\u0434\u0430"
RU_CANCEL = "\u043d\u0435\u0442"


def _make_stub():
    wnd = WINDOW_CLS.__new__(WINDOW_CLS)
    wnd._settings = {
        "interface_language": "\u0420\u0443\u0441\u0441\u043a\u0438\u0439",
        "confirm_phrase": (
            "\u0434\u0430, \u043f\u0440\u0430\u0432\u0438\u043b\u044c\u043d\u043e, "
            "\u043f\u043e\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0430\u044e"
        ),
        "cancel_phrase": "\u043d\u0435\u0442, \u043e\u0442\u043c\u0435\u043d\u0430, \u043e\u0442\u043c\u0435\u043d\u0438\u0442\u044c",
        "cancel_triggers": "\u043e\u0441\u0442\u0430\u043d\u043e\u0432\u0438 \u043a\u043e\u043c\u0430\u043d\u0434\u0443",
        "prefix_word": RU_PREFIX,
        "prefix_sensitivity": 50,
    }
    wnd._prefix_mode_enabled = False
    wnd._command_confirm_lock = threading.Lock()
    wnd._command_confirm_requests = {}
    wnd._command_confirm_seq = 0
    wnd._active_command_confirm_req_id = 0
    wnd._active_command_confirm_dialog = None
    wnd._command_variants_cache = {}
    wnd._variant_token_cache = {}
    wnd._append_runtime_line = lambda *args, **kwargs: None
    wnd._show_foreground_window = lambda *args, **kwargs: True
    wnd._close_all_windows = lambda *args, **kwargs: (3, 4)
    wnd._mouse_left_click = lambda *args, **kwargs: True
    wnd._mouse_right_click = lambda *args, **kwargs: True
    wnd._mouse_double_click = lambda *args, **kwargs: True
    wnd._mouse_move_to = lambda *args, **kwargs: True
    wnd._mouse_move_by = lambda *args, **kwargs: True
    wnd._send_keys = lambda *args, **kwargs: True
    wnd._run_powershell = lambda *args, **kwargs: True
    wnd._run_powershell_capture = lambda *args, **kwargs: "Test Voice"
    wnd._set_system_volume_percent = lambda *args, **kwargs: True
    wnd._change_system_volume_by_steps = lambda *args, **kwargs: True
    wnd._set_system_brightness_percent = lambda *args, **kwargs: True
    wnd._change_system_brightness_by_steps = lambda *args, **kwargs: True
    wnd._resolve_existing_path_by_search_settings = lambda *args, **kwargs: ""
    wnd._play_wave_file = lambda *args, **kwargs: True
    wnd._speak_text = lambda *args, **kwargs: True
    wnd._select_voice_by_gender = lambda *args, **kwargs: True
    wnd._on_setting_changed = lambda key, value, *args, **kwargs: wnd._settings.__setitem__(str(key), value)
    wnd._on_top_mic_toggled = lambda *args, **kwargs: None
    class _MicStub:
        def __init__(self) -> None:
            self._checked = True
        def blockSignals(self, _value: bool) -> bool:
            return False
        def setChecked(self, value: bool) -> None:
            self._checked = bool(value)
    wnd.mic_btn = _MicStub()
    return wnd


def _expect(condition: bool, name: str, failures: list[str]) -> None:
    if not condition:
        failures.append(name)


def _check_phrases_and_confirmations(failures: list[str]) -> None:
    wnd = _make_stub()

    _expect(wnd._is_close_all_windows_phrase(RU_CLOSE_ALL), "phrase: exact ru", failures)
    _expect(
        wnd._is_close_all_windows_phrase(RU_CLOSE_ALL_PLEASE),
        "phrase: ru with extra token",
        failures,
    )
    _expect(
        wnd._is_close_all_windows_phrase(f"{RU_PREFIX} {RU_CLOSE_ALL}"),
        "phrase: with prefix",
        failures,
    )
    _expect(
        wnd._is_close_all_windows_phrase("close all windows now"),
        "phrase: en with extra token",
        failures,
    )

    wnd._prefix_mode_enabled = True
    _expect(
        not wnd._is_close_all_windows_phrase(RU_CLOSE_ALL),
        "prefix mode requires prefix",
        failures,
    )
    _expect(
        wnd._is_close_all_windows_phrase(f"{RU_PREFIX} {RU_CLOSE_ALL}"),
        "prefix mode with prefix",
        failures,
    )
    wnd._prefix_mode_enabled = False

    wnd._find_best_command_for_phrase = (
        lambda phrase: (
            {"name": "close one", "actions": [{"id": "window_close", "value": ""}]},
            1.0,
        )
    )
    result = wnd._try_execute_registered_command(RU_CLOSE_ALL)
    _expect(
        isinstance(result, dict) and result.get("kind") == "confirm_request",
        "builtin priority over registered",
        failures,
    )

    req_id = int(result.get("id", 0)) if isinstance(result, dict) else 0
    _expect(req_id > 0, "confirm request id", failures)
    _expect(wnd._handle_voice_command_confirmation(RU_CONFIRM), "voice confirm handled", failures)
    approved, cmd, _ = wnd._await_command_confirm_result(req_id, 0.1)
    _expect(approved and isinstance(cmd, dict), "voice confirm result approved", failures)

    result2 = wnd._try_execute_builtin_command(RU_CLOSE_ALL)
    req_id2 = int(result2.get("id", 0)) if isinstance(result2, dict) else 0
    _expect(req_id2 > 0, "confirm request id 2", failures)
    _expect(wnd._handle_voice_command_confirmation(RU_CANCEL), "voice cancel handled", failures)
    approved2, _, _ = wnd._await_command_confirm_result(req_id2, 0.1)
    _expect(not approved2, "voice cancel result", failures)


def _check_brightness_phrases(failures: list[str]) -> int:
    cases = [
        ("\u0443\u0432\u0435\u043b\u0438\u0447\u044c \u044f\u0440\u043a\u043e\u0441\u0442\u044c", "change", 10),
        (
            "\u0443\u0432\u0435\u043b\u0438\u0447\u044c \u043f\u043e\u0436\u0430\u043b\u0443\u0439\u0441\u0442\u0430 \u044f\u0440\u043a\u043e\u0441\u0442\u044c \u044d\u043a\u0440\u0430\u043d\u0430",
            "change",
            10,
        ),
        (
            "\u0434\u0436\u0430\u0440\u0432\u0438\u0441 \u0443\u0432\u0435\u043b\u0438\u0447\u044c \u043c\u043d\u0435 \u044f\u0440\u043a\u043e\u0441\u0442\u044c \u043d\u0430 15",
            "change",
            15,
        ),
        (
            "\u0441\u0434\u0435\u043b\u0430\u0439 \u044d\u043a\u0440\u0430\u043d \u044f\u0440\u0447\u0435",
            "change",
            10,
        ),
        ("\u0434\u043e\u0431\u0430\u0432\u044c \u0441\u0432\u0435\u0442\u0430", "change", 10),
        ("\u044f\u0440\u043a\u043e\u0441\u0442\u044c \u0432\u044b\u0448\u0435", "change", 10),
        (
            "\u0443\u043c\u0435\u043d\u044c\u0448\u0438 \u044f\u0440\u043a\u043e\u0441\u0442\u044c",
            "change",
            -10,
        ),
        (
            "\u0441\u0434\u0435\u043b\u0430\u0439 \u0442\u0435\u043c\u043d\u0435\u0435",
            "change",
            -10,
        ),
        ("\u044f\u0440\u043a\u043e\u0441\u0442\u044c 70", "set", 70),
        (
            "\u044f\u0440\u043a\u043e\u0441\u0442\u044c \u043c\u0430\u043a\u0441\u0438\u043c\u0443\u043c",
            "set",
            100,
        ),
    ]

    for phrase, expected_kind, expected_value in cases:
        wnd = _make_stub()
        calls: list[tuple[str, int, bool]] = []

        def _change(delta, *args, **kwargs):
            calls.append(("change", int(delta), bool(kwargs.get("verify", False))))
            return True

        def _set_percent(target, *args, **kwargs):
            calls.append(("set", int(target), bool(kwargs.get("verify", False))))
            return True

        wnd._change_system_brightness_by_steps = _change
        wnd._set_system_brightness_percent = _set_percent
        wnd._known_system_brightness_percent = lambda *args, **kwargs: None
        wnd._get_system_brightness_percent = lambda *args, **kwargs: 50

        reply = wnd._try_execute_builtin_brightness_command(phrase)
        _expect(bool(reply), f"brightness phrase reply: {phrase!r}", failures)
        _expect(bool(calls), f"brightness phrase calls action: {phrase!r}", failures)
        if calls:
            kind, value, verify = calls[0]
            _expect(
                kind == expected_kind and value == expected_value,
                f"brightness phrase action: {phrase!r}",
                failures,
            )
            _expect(verify, f"brightness phrase verifies: {phrase!r}", failures)

    return len(cases)


def _check_control_fragment_merge(failures: list[str]) -> int:
    class _TimerStub:
        def __init__(self) -> None:
            self.started: list[int] = []
            self.stopped = False

        def start(self, value: int | None = None) -> None:
            self.started.append(int(value or 0))

        def stop(self) -> None:
            self.stopped = True

        def isActive(self) -> bool:
            return bool(self.started)

    wnd = _make_stub()
    wnd._speech_phrase_timer = _TimerStub()
    wnd._speech_phrase_buffer = ""
    wnd._speech_pending_prefix_stub = ""
    wnd._speech_pending_prefix_ts = 0.0
    wnd._speech_stub_hold_count = 0
    wnd._speech_stub_hold_phrase = ""
    wnd._voice_followup_until = time.monotonic() + 4.0
    wnd._voice_followup_prefix = RU_PREFIX
    wnd._is_current_speech_sender = lambda *args, **kwargs: True
    wnd._is_speech_capture_blocked = lambda *args, **kwargs: False
    wnd._play_wake_ack_clip = lambda *args, **kwargs: True
    wnd._handle_plugin_script_test_phrase = lambda *args, **kwargs: False
    wnd._allow_freeform_arduino_mode_upload_voice = lambda *args, **kwargs: False
    wnd._find_best_command_for_phrase = lambda *args, **kwargs: (None, 0.0)

    _expect(
        wnd._is_likely_control_prefix_stub("\u0443\u0432\u0435\u043b\u0438\u0447\u044c"),
        "control prefix: increase",
        failures,
    )
    _expect(
        wnd._is_likely_control_prefix_stub(
            "\u0443\u0432\u0435\u043b\u0438\u0447\u044c \u043f\u043e\u0436\u0430\u043b\u0443\u0439\u0441\u0442\u0430"
        ),
        "control prefix: increase please",
        failures,
    )
    _expect(
        wnd._is_likely_control_prefix_stub(
            "\u0441\u0434\u0435\u043b\u0430\u0439 \u043f\u043e\u0436\u0430\u043b\u0443\u0439\u0441\u0442\u0430"
        ),
        "control prefix: make please",
        failures,
    )

    wnd._speech_pending_prefix_stub = "\u0443\u0432\u0435\u043b\u0438\u0447\u044c"
    wnd._speech_pending_prefix_ts = time.monotonic()
    merged = wnd._merge_with_pending_control_stub("\u044f\u0440\u043a\u043e\u0441\u0442\u044c")
    _expect(
        merged == "\u0443\u0432\u0435\u043b\u0438\u0447\u044c \u044f\u0440\u043a\u043e\u0441\u0442\u044c",
        "merge pending control stub",
        failures,
    )

    wnd._speech_phrase_buffer = (
        "\u0443\u0432\u0435\u043b\u0438\u0447\u044c \u043f\u043e\u0436\u0430\u043b\u0443\u0439\u0441\u0442\u0430"
    )
    merged2 = wnd._merge_with_active_control_buffer(
        "\u044f\u0440\u043a\u043e\u0441\u0442\u044c \u044d\u043a\u0440\u0430\u043d\u0430"
    )
    _expect(
        merged2
        == "\u0443\u0432\u0435\u043b\u0438\u0447\u044c \u043f\u043e\u0436\u0430\u043b\u0443\u0439\u0441\u0442\u0430 \u044f\u0440\u043a\u043e\u0441\u0442\u044c \u044d\u043a\u0440\u0430\u043d\u0430",
        "merge active control buffer",
        failures,
    )
    _expect(wnd._speech_phrase_buffer == "", "active control buffer cleared", failures)

    calls: list[str] = []
    wnd._enqueue_command_execution = lambda phrase, *args, **kwargs: calls.append(str(phrase))
    wnd._on_speech_text_recognized("\u0443\u0432\u0435\u043b\u0438\u0447\u044c")
    _expect(not calls, "split control first chunk waits", failures)
    wnd._on_speech_text_recognized("\u044f\u0440\u043a\u043e\u0441\u0442\u044c")
    _expect(
        calls[-1:] == ["\u0443\u0432\u0435\u043b\u0438\u0447\u044c \u044f\u0440\u043a\u043e\u0441\u0442\u044c"],
        "split control chunks enqueue merged phrase",
        failures,
    )

    calls.clear()
    wnd._speech_phrase_buffer = ""
    wnd._speech_pending_prefix_stub = ""
    wnd._speech_pending_prefix_ts = 0.0
    wnd._on_speech_text_recognized(
        "\u0434\u0436\u0430\u0440\u0432\u0438\u0441 \u0443\u0432\u0435\u043b\u0438\u0447\u044c \u044f\u0440\u043a\u043e\u0441\u0442\u044c"
    )
    _expect(
        calls[-1:] == ["\u0443\u0432\u0435\u043b\u0438\u0447\u044c \u044f\u0440\u043a\u043e\u0441\u0442\u044c"],
        "wake complete control tail executes",
        failures,
    )

    calls.clear()
    wnd._speech_phrase_buffer = ""
    wnd._speech_pending_prefix_stub = ""
    wnd._speech_pending_prefix_ts = 0.0
    wnd._on_speech_text_recognized("\u0434\u0436\u0430\u0440\u0432\u0438\u0441 \u0443\u0432\u0435\u043b\u0438\u0447\u044c")
    _expect(not calls, "wake control tail waits", failures)
    wnd._on_speech_text_recognized("\u044f\u0440\u043a\u043e\u0441\u0442\u044c")
    _expect(
        calls[-1:] == ["\u0443\u0432\u0435\u043b\u0438\u0447\u044c \u044f\u0440\u043a\u043e\u0441\u0442\u044c"],
        "wake control tail merges next chunk",
        failures,
    )

    return 9


def _mojibake_cp1251(text: str) -> str:
    return text.encode("utf-8").decode("cp1251")


def _mojibake_latin1(text: str) -> str:
    return text.encode("utf-8").decode("latin1")


def _check_settings_mojibake_repair(failures: list[str]) -> int:
    wnd = _make_stub()
    bad_prefix = _mojibake_cp1251(RU_PREFIX)
    bad_title = _mojibake_latin1("\u041d\u0410\u0421\u0422\u0420\u041e\u0419\u041a\u0418")

    _expect(
        wnd._normalize_loaded_value(bad_prefix, "") == RU_PREFIX,
        "settings mojibake: prefix",
        failures,
    )

    normalized = wnd._normalize_loaded_value(
        {"settings.title": bad_title, "broken": "????"},
        {},
    )
    _expect(
        isinstance(normalized, dict)
        and normalized.get("settings.title") == "\u041d\u0410\u0421\u0422\u0420\u041e\u0419\u041a\u0418",
        "settings mojibake: nested dict",
        failures,
    )
    _expect(
        isinstance(normalized, dict) and "broken" not in normalized,
        "settings mojibake: drops corrupt override",
        failures,
    )
    return 3


def _check_wake_phrase_fast_path(failures: list[str]) -> int:
    class _TimerStub:
        def stop(self) -> None:
            pass

        def start(self, _value: int | None = None) -> None:
            pass

    wnd = _make_stub()
    wnd._speech_phrase_timer = _TimerStub()
    wnd._speech_phrase_buffer = ""
    wnd._speech_pending_prefix_stub = ""
    wnd._speech_pending_prefix_ts = 0.0
    wnd._speech_stub_hold_count = 0
    wnd._speech_stub_hold_phrase = ""
    wnd._voice_followup_until = 0.0
    wnd._voice_followup_prefix = ""
    wnd._is_current_speech_sender = lambda *args, **kwargs: True
    wnd._is_speech_capture_blocked = lambda *args, **kwargs: False

    ack_calls: list[bool] = []
    enqueued: list[str] = []
    wnd._play_wake_ack_clip = lambda *args, **kwargs: ack_calls.append(True) or True
    wnd._enqueue_command_execution = lambda phrase, *args, **kwargs: enqueued.append(str(phrase))

    wnd._on_speech_text_recognized(RU_PREFIX)
    _expect(bool(ack_calls), "wake phrase ack is played", failures)
    _expect(not enqueued, "wake phrase does not enqueue pure wake command", failures)
    _expect(wnd._is_voice_followup_active(), "wake phrase arms followup", failures)

    wnd._on_speech_text_recognized(f"{RU_PREFIX} \u044d\u043d\u0442\u0435\u0440")
    _expect(enqueued[-1:] == ["\u044d\u043d\u0442\u0435\u0440"], "wake phrase tail enqueues command", failures)
    return 4


def _check_keyboard_phrases(failures: list[str]) -> int:
    commands: dict[str, object] = {}
    if os.path.exists("jarvis_commands.json"):
        with open("jarvis_commands.json", "r", encoding="utf-8") as fh:
            payload = json.load(fh)
        raw_commands = payload.get("commands", {}) if isinstance(payload, dict) else {}
        if isinstance(raw_commands, dict):
            commands = raw_commands

    cases = [
        "\u044d\u043d\u0442\u0435\u0440",
        "\u044d\u043d\u0442\u044d\u0440",
        "enter",
        "\u043d\u0430\u0436\u043c\u0438 \u044d\u043d\u0442\u0435\u0440",
        "\u0434\u0436\u0430\u0440\u0432\u0438\u0441 \u044d\u043d\u0442\u0435\u0440",
    ]

    checked = 0
    for phrase in cases:
        wnd = _make_stub()
        if commands:
            wnd.command_page = types.SimpleNamespace(_commands=commands)
        sent: list[str] = []
        wnd._send_keys = lambda pattern, *args, **kwargs: sent.append(str(pattern)) or True
        reply = wnd._try_execute_registered_command(phrase)
        _expect(bool(reply), f"keyboard enter reply: {phrase!r}", failures)
        _expect(sent == ["{ENTER}"], f"keyboard enter sends key: {phrase!r}", failures)
        checked += 1

    return checked


def _check_command_match_latency(failures: list[str]) -> int:
    if not os.path.exists("jarvis_commands.json"):
        return 0

    with open("jarvis_commands.json", "r", encoding="utf-8") as fh:
        payload = json.load(fh)
    commands = payload.get("commands", {}) if isinstance(payload, dict) else {}
    if not isinstance(commands, dict):
        return 0

    wnd = _make_stub()
    wnd.command_page = types.SimpleNamespace(_commands=commands)
    wnd._voice_followup_until = 0.0
    wnd._voice_followup_prefix = ""

    cases = [
        ("\u043e\u0442\u043a\u0440\u043e\u0439 \u044e\u0442\u0443\u0431", True),
        ("\u043e\u0442\u043a\u0440\u043e\u0439 \u0431\u0440\u0430\u0443\u0437\u0435\u0440", True),
        ("\u043e\u0442\u043a\u0440\u043e\u0439", False),
    ]

    checked = 0
    for phrase, expected_found in cases:
        durations: list[float] = []
        found = False
        for _ in range(12):
            started = time.perf_counter()
            command, _score = wnd._find_best_command_for_phrase(phrase)
            durations.append((time.perf_counter() - started) * 1000.0)
            found = command is not None
        avg_ms = sum(durations) / max(1, len(durations))
        _expect(found is expected_found, f"command match found: {phrase!r}", failures)
        _expect(avg_ms < 80.0, f"command match latency: {phrase!r} avg={avg_ms:.1f}ms", failures)
        checked += 1
    return checked


def _check_action_handlers(failures: list[str]) -> int:
    wnd = _make_stub()

    web_calls: list[str] = []
    start_calls: list[str] = []
    popen_calls: list[object] = []

    old_web_open = main.webbrowser.open
    old_startfile = getattr(main.os, "startfile", None)
    old_popen = main.subprocess.Popen

    try:
        main.webbrowser.open = lambda url: web_calls.append(str(url)) or True
        if old_startfile is not None:
            main.os.startfile = lambda path: start_calls.append(str(path)) or True  # type: ignore[attr-defined]
        main.subprocess.Popen = (
            lambda args, *a, **kw: popen_calls.append(args) or types.SimpleNamespace(pid=1234)
        )

        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
            tmp_path = tmp.name

        cases = [
            ({"id": "voice_say", "value": "test"}, "voice_say"),
            ({"id": "window_close", "value": ""}, "window_close"),
            ({"id": "window_close_all", "value": ""}, "window_close_all"),
            ({"id": "window_minimize", "value": ""}, "window_minimize"),
            ({"id": "window_maximize", "value": ""}, "window_maximize"),
            ({"id": "window_normalize", "value": ""}, "window_normalize"),
            ({"id": "mouse_click", "value": "\u041b\u0435\u0432\u044b\u0439 \u043a\u043b\u0438\u043a"}, "mouse_click"),
            ({"id": "mouse_right_click", "value": ""}, "mouse_right_click"),
            ({"id": "mouse_to_coords", "value": "100 200"}, "mouse_to_coords"),
            ({"id": "move_mouse_left", "value": ""}, "move_mouse_left"),
            ({"id": "move_mouse_right", "value": ""}, "move_mouse_right"),
            ({"id": "move_mouse_up", "value": ""}, "move_mouse_up"),
            ({"id": "move_mouse_down", "value": ""}, "move_mouse_down"),
            ({"id": "move_mouse_to_coordinates", "value": "100 200"}, "move_mouse_to_coordinates"),
            ({"id": "keyboard_hotkey", "value": "^a"}, "keyboard_hotkey"),
            ({"id": "keyboard_text", "value": "test"}, "keyboard_text"),
            ({"id": "sound_play_wav", "value": tmp_path}, "sound_play_wav"),
            ({"id": "sound_play_mp3", "value": tmp_path}, "sound_play_mp3"),
            ({"id": "sound_increase_volume_by", "value": "3"}, "sound_increase_volume_by"),
            ({"id": "sound_decrease_volume_by", "value": "3"}, "sound_decrease_volume_by"),
            ({"id": "system_set_brightness", "value": "55"}, "system_set_brightness"),
            ({"id": "system_increase_brightness_by", "value": "3"}, "system_increase_brightness_by"),
            ({"id": "system_decrease_brightness_by", "value": "3"}, "system_decrease_brightness_by"),
            ({"id": "launch_openurl", "value": "https://example.com"}, "launch_openurl"),
            ({"id": "launch_url", "value": "https://example.com"}, "launch_url"),
            ({"id": "launch_openfile", "value": tmp_path}, "launch_openfile"),
            ({"id": "launch_command_line", "value": "echo 1"}, "launch_command_line"),
            ({"id": "system_monitor_off", "value": ""}, "system_monitor_off"),
            ({"id": "system_monitor_on", "value": ""}, "system_monitor_on"),
            ({"id": "system_monitor_standby", "value": ""}, "system_monitor_standby"),
            ({"id": "system_sleep", "value": ""}, "system_sleep"),
            ({"id": "system_shutdown", "value": ""}, "system_shutdown"),
            ({"id": "system_restart", "value": ""}, "system_restart"),
            ({"id": "system_lock_screen", "value": ""}, "system_lock_screen"),
            ({"id": "sound_setvol", "value": "55"}, "sound_setvol"),
            ({"id": "voice_set_male", "value": ""}, "voice_set_male"),
            ({"id": "voice_set_female", "value": ""}, "voice_set_female"),
            ({"id": "jarvis_prefix_mode", "value": "on"}, "jarvis_prefix_mode"),
            ({"id": "jarvis_silent_mode", "value": "on"}, "jarvis_silent_mode"),
            ({"id": "jarvis_enable_microphone", "value": ""}, "jarvis_enable_microphone"),
            ({"id": "jarvis_disable_microphone", "value": ""}, "jarvis_disable_microphone"),
            ({"id": "system_wait", "value": "0"}, "system_wait"),
            ({"id": "jarvis_pause", "value": "0"}, "jarvis_pause"),
            ({"id": "vc_pause", "value": "0"}, "vc_pause"),
        ]

        for action, label in cases:
            ok, _err = wnd._execute_single_action(action, "\u0433\u0440\u043e\u043c\u043a\u043e\u0441\u0442\u044c 55")
            _expect(ok, f"action: {label}", failures)

        ok_stop, err_stop = wnd._execute_single_action({"id": "jarvis_disable_command", "value": ""}, "")
        _expect((not ok_stop) and err_stop == "__STOP_COMMAND__", "action: jarvis_disable_command", failures)

        ok_unknown, err_unknown = wnd._execute_single_action({"id": "unknown_action", "value": ""}, "")
        _expect((not ok_unknown) and bool(err_unknown), "unknown action returns error", failures)

        url_handled = any("https://example.com" in item for item in web_calls) or any(
            "https://example.com" in item for item in start_calls
        )
        _expect(url_handled, "url launch call", failures)
        if old_startfile is not None:
            _expect(len(start_calls) >= 1, "startfile call", failures)
        _expect(len(popen_calls) >= 1, "popen call", failures)

        try:
            os.remove(tmp_path)
        except Exception:
            pass
    finally:
        main.webbrowser.open = old_web_open
        if old_startfile is not None:
            main.os.startfile = old_startfile  # type: ignore[attr-defined]
        main.subprocess.Popen = old_popen
    return len(cases) + 1


def _check_catalog_coverage(failures: list[str]) -> int:
    catalog_ids = {
        item.get("id", "")
        for group in main.ACTION_CATALOG.values()
        for item in group
        if isinstance(item, dict)
    }
    supported_ids = {
        "launch_file",
        "launch_url",
        "launch_command_line",
        "keyboard_hotkey",
        "keyboard_text",
        "mouse_left_click",
        "mouse_right_click",
        "mouse_left_click_no_move",
        "mouse_right_click_no_move",
        "move_mouse_left",
        "move_mouse_right",
        "move_mouse_up",
        "move_mouse_down",
        "move_mouse_to_coordinates",
        "move_mouse_to_coordinates_no_move",
        "mouse_click",
        "mouse_to_coords",
        "system_shutdown",
        "system_restart",
        "system_sleep",
        "system_lock_screen",
        "monitor_off",
        "monitor_on",
        "monitor_standby",
        "system_wait",
        "sound_play_wav",
        "sound_play_mp3",
        "sound_increase_volume_by",
        "sound_decrease_volume_by",
        "sound_setvol",
        "voice_set_male",
        "voice_set_female",
        "voice_say",
        "jarvis_pause",
        "jarvis_prefix_mode",
        "jarvis_silent_mode",
        "jarvis_enable_microphone",
        "jarvis_disable_microphone",
        "jarvis_disable_command",
        "jarvis_run_command",
        "arduino_mode_upload_v2",
        "launch_app",
        "launch_openfilex",
        "vc_pause",
        "launch_openurl",
        "launch_open_url",
        "launch_openfile",
        "launch_open_file",
        "sound_playstream",
        "tts_speak",
        "window_close",
        "window_close_all",
        "system_close_all_windows",
        "window_minimize",
        "window_maximize",
        "window_normalize",
        "mouse_leftclick",
        "inputkeys_send",
        "system_monitor_off",
        "system_monitor_on",
        "system_monitor_standby",
        "system_set_brightness",
        "system_increase_brightness_by",
        "system_decrease_brightness_by",
        "sound_set_volume_to",
        "none",
        "action_none",
        "empty",
        "",
    }
    for action_id in sorted(catalog_ids):
        _expect(action_id in supported_ids, f"catalog support: {action_id}", failures)
    return len(catalog_ids)


def _check_json_command_ids(failures: list[str]) -> tuple[int, int, int]:
    supported = {
        "launch_file",
        "launch_url",
        "launch_command_line",
        "keyboard_hotkey",
        "keyboard_text",
        "mouse_left_click",
        "mouse_right_click",
        "mouse_left_click_no_move",
        "mouse_right_click_no_move",
        "move_mouse_left",
        "move_mouse_right",
        "move_mouse_up",
        "move_mouse_down",
        "move_mouse_to_coordinates",
        "move_mouse_to_coordinates_no_move",
        "mouse_click",
        "mouse_to_coords",
        "system_shutdown",
        "system_restart",
        "system_sleep",
        "system_lock_screen",
        "monitor_off",
        "monitor_on",
        "monitor_standby",
        "system_wait",
        "sound_play_wav",
        "sound_play_mp3",
        "sound_increase_volume_by",
        "sound_decrease_volume_by",
        "sound_setvol",
        "voice_set_male",
        "voice_set_female",
        "voice_say",
        "jarvis_pause",
        "jarvis_prefix_mode",
        "jarvis_silent_mode",
        "jarvis_enable_microphone",
        "jarvis_disable_microphone",
        "jarvis_disable_command",
        "jarvis_run_command",
        "arduino_mode_upload_v2",
        "launch_app",
        "launch_openfilex",
        "vc_pause",
        "launch_openurl",
        "launch_open_url",
        "launch_openfile",
        "launch_open_file",
        "sound_playstream",
        "tts_speak",
        "window_close",
        "window_close_all",
        "system_close_all_windows",
        "window_minimize",
        "window_maximize",
        "window_normalize",
        "mouse_leftclick",
        "mouse_rightclick",
        "inputkeys_send",
        "system_monitor_off",
        "system_monitor_on",
        "system_monitor_standby",
        "system_set_brightness",
        "system_increase_brightness_by",
        "system_decrease_brightness_by",
        "sound_set_volume_to",
        "disable_command",
        "none",
        "action_none",
        "empty",
        "",
    }

    total_commands = 0
    total_actions = 0
    ids = Counter()
    unknown = Counter()
    for path in ("jarvis_commands.json", "jarvis_commands_full.json"):
        if not os.path.exists(path):
            continue
        with open(path, "r", encoding="utf-8") as fh:
            payload = json.load(fh)
        commands = payload.get("commands", {}) if isinstance(payload, dict) else {}
        for items in commands.values():
            if not isinstance(items, list):
                continue
            for cmd in items:
                if not isinstance(cmd, dict):
                    continue
                total_commands += 1
                actions = cmd.get("actions", [])
                if not isinstance(actions, list):
                    continue
                for action in actions:
                    if not isinstance(action, dict):
                        continue
                    action_id = str(action.get("id", "")).strip().lower()
                    ids[action_id] += 1
                    total_actions += 1
                    if action_id not in supported:
                        unknown[action_id] += 1

    _expect(len(unknown) == 0, "json command ids are supported", failures)
    return total_commands, total_actions, len(ids)


def run() -> int:
    failures: list[str] = []
    _check_phrases_and_confirmations(failures)
    checked_brightness_cases = _check_brightness_phrases(failures)
    checked_control_merge_cases = _check_control_fragment_merge(failures)
    checked_mojibake_cases = _check_settings_mojibake_repair(failures)
    checked_wake_fast_path_cases = _check_wake_phrase_fast_path(failures)
    checked_keyboard_cases = _check_keyboard_phrases(failures)
    checked_match_latency_cases = _check_command_match_latency(failures)
    checked_action_cases = _check_action_handlers(failures)
    catalog_count = _check_catalog_coverage(failures)
    total_commands, total_actions, unique_ids = _check_json_command_ids(failures)

    if failures:
        print("SELFTEST_FAIL")
        for item in failures:
            print(f" - {item}")
        return 1

    print("SELFTEST_OK")
    print("checked_builtin_phrase_cases=6")
    print(f"checked_brightness_phrase_cases={checked_brightness_cases}")
    print(f"checked_control_fragment_merge_cases={checked_control_merge_cases}")
    print(f"checked_settings_mojibake_cases={checked_mojibake_cases}")
    print(f"checked_wake_fast_path_cases={checked_wake_fast_path_cases}")
    print(f"checked_keyboard_phrase_cases={checked_keyboard_cases}")
    print(f"checked_command_match_latency_cases={checked_match_latency_cases}")
    print("checked_voice_confirmation_cases=2")
    print(f"checked_action_handler_cases={checked_action_cases}")
    print(f"checked_action_catalog_ids={catalog_count}")
    print(f"checked_json_commands={total_commands}")
    print(f"checked_json_actions={total_actions}")
    print(f"checked_json_unique_action_ids={unique_ids}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
