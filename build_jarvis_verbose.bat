@echo off
setlocal
cd /d "%~dp0"
title Jarvis Build (Verbose, Onefile)
echo.
echo [Jarvis] Starting verbose onefile build...
echo [Jarvis] Full PyInstaller command and full live log will be shown below.
echo.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0build_jarvis_verbose.ps1" -BuildMode onefile
set "EC=%ERRORLEVEL%"
echo.
if "%EC%"=="0" (
  echo [Jarvis] Build completed successfully.
) else (
  echo [Jarvis] Build failed with code %EC%.
)
echo.
pause
exit /b %EC%
