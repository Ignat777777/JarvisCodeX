# How to Run Jarvis

## One-click start
1. Open the project folder.
2. Run `start_jarvis.bat`.

## Start from terminal
```powershell
python main.py
```

## Full verification before use
Run:
```powershell
verify_jarvis.bat
```

This script runs:
1. `py_compile`
2. `jarvis_selftest.py`
3. `jarvis_live_mouse_regression.py`
4. `jarvis_ui_maxtest.py`
5. `jarvis_tg_smoke.py`
6. `jarvis_tray_close_smoke.py`

## If it does not start
1. Check Python:
```powershell
python --version
```
Required: Python 3.11+.

2. If `python` is not found, install Python and enable:
`Add python.exe to PATH`.

3. If PySide6 is missing:
```powershell
pip install PySide6
```

## Test artifacts
Screenshots and reports are saved to `_current_preview`.
