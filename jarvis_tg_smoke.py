import os
import time

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication

import main


def run() -> int:
    app = QApplication.instance() or QApplication([])
    win = main.JarvisWindow()
    try:
        win._apply_runtime_setting("tg_bot_enabled", False)
        win._on_telegram_phrase_received("test telegram command", "777", 1)
        for _ in range(40):
            app.processEvents()
            win._drain_command_execution_results()
            time.sleep(0.02)
        item = win._telegram_outgoing_queue.get_nowait()
        assert item[0] == "777" and bool(item[1]), "telegram smoke failed"
        print("TG_SMOKE_OK")
        return 0
    finally:
        try:
            win._force_close = True
            win.close()
            app.processEvents()
        except Exception:
            pass


if __name__ == "__main__":
    raise SystemExit(run())
