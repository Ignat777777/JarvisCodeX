@echo off
setlocal
chcp 65001 >nul

set "ROOT=%~dp0"
cd /d "%ROOT%"

where python >nul 2>nul
if errorlevel 1 (
  echo [Jarvis Verify] Python not found in PATH.
  exit /b 1
)

echo [Jarvis Verify] 1/6 compile...
python -m py_compile main.py jarvis_telegram.py jarvis_selftest.py jarvis_live_mouse_regression.py jarvis_ui_maxtest.py jarvis_tg_smoke.py jarvis_tray_close_smoke.py
if errorlevel 1 exit /b 1

echo [Jarvis Verify] 2/6 selftest...
set "QT_QPA_PLATFORM=offscreen"
python jarvis_selftest.py
if errorlevel 1 exit /b 1

echo [Jarvis Verify] 3/6 live mouse regression...
python jarvis_live_mouse_regression.py
if errorlevel 1 exit /b 1

echo [Jarvis Verify] 4/6 ui max test...
python jarvis_ui_maxtest.py
if errorlevel 1 exit /b 1

echo [Jarvis Verify] 5/6 telegram smoke...
python jarvis_tg_smoke.py
if errorlevel 1 exit /b 1

echo [Jarvis Verify] 6/6 tray close smoke...
python jarvis_tray_close_smoke.py
if errorlevel 1 exit /b 1

echo [Jarvis Verify] OK
exit /b 0
