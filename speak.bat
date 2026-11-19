@echo off
chcp 65001 >nul
cd /d "%~dp0"
set "PATH=%~dp0;%APPDATA%\Python\Python314\Scripts;%APPDATA%\Python\Scripts;%PATH%"

echo Starting Whisper Live Terminal Voice-to-Text...
python live_speak.py
pause
