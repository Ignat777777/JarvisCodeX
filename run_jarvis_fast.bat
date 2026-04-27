@echo off
setlocal
cd /d "%~dp0"
title Jarvis Fast Launch (Onedir)
echo.
echo [Jarvis] Fast launch mode (recommended).
echo [Jarvis] Showing startup progress...
echo.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0run_jarvis_with_progress.ps1" -Mode onedir -TimeoutSec 60
set "EC=%ERRORLEVEL%"
echo.
if not "%EC%"=="0" (
  echo [Jarvis] Launch script returned error code %EC%.
)
pause
exit /b %EC%
