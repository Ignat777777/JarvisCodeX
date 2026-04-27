@echo off
setlocal
cd /d "%~dp0"
title Jarvis Onefile Launch
echo.
echo [Jarvis] Onefile launch mode.
echo [Jarvis] Startup can take 30-90+ seconds on first/cold run.
echo [Jarvis] Showing startup progress...
echo.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0run_jarvis_with_progress.ps1" -Mode onefile -TimeoutSec 180
set "EC=%ERRORLEVEL%"
echo.
if not "%EC%"=="0" (
  echo [Jarvis] Launch script returned error code %EC%.
)
pause
exit /b %EC%
