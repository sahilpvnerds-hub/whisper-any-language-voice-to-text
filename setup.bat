@echo off
chcp 65001 >nul
echo ======================================================================
echo    Whisper AI - Auto Detect Voice to Text - Setup Installer
echo ======================================================================
echo.

:: 1. Check Python
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)
echo [OK] Python detected.

:: 2. Check FFmpeg
ffmpeg -version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [INFO] FFmpeg not found in PATH. Attempting automatic install via winget...
    winget install Gyan.FFmpeg --accept-source-agreements --accept-package-agreements
    echo.
    echo If winget completed, please restart your terminal after setup!
) else (
    echo [OK] FFmpeg detected.
)

:: 3. Install Python Dependencies
echo.
echo Installing Python dependencies from requirements.txt...
python -m pip install -r requirements.txt

echo.
echo ======================================================================
echo    Setup completed successfully!
echo    To launch the ChatGPT-style Voice Web UI, run: run_web_ui.bat
echo ======================================================================
pause
