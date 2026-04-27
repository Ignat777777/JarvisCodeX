@echo off
setlocal
chcp 65001 >nul

set "ROOT=%~dp0"
cd /d "%ROOT%"

where python >nul 2>nul
if errorlevel 1 (
  echo [Jarvis] Python not found in PATH.
  echo [Jarvis] Install Python 3.11+ and enable "Add python.exe to PATH".
  exit /b 1
)

echo [Jarvis] Starting...
python main.py
set "CODE=%ERRORLEVEL%"

if not "%CODE%"=="0" (
  echo [Jarvis] Finished with code %CODE%.
)

exit /b %CODE%
