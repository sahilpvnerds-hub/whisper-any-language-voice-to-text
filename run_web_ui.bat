@echo off
chcp 65001 >nul
cd /d "%~dp0"
set "PATH=%~dp0;%APPDATA%\Python\Python314\Scripts;%APPDATA%\Python\Scripts;%PATH%"

echo ==========================================================
echo   Starting Whisper ChatGPT-Style Voice Web UI
echo   URL: http://127.0.0.1:5000
echo ==========================================================
echo.

start "" "http://127.0.0.1:5000"
python app.py
pause
