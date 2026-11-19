@echo off
cd /d "%~dp0"
set "PATH=%~dp0;C:\Users\Yiion-63\AppData\Roaming\Python\Python314\Scripts;%PATH%"

echo ========================================================
echo   Running OpenAI Whisper on sample.wav (model: tiny)
echo ========================================================
python -m whisper sample.wav --model tiny
echo.
echo ========================================================
echo   Transcription Output (sample.txt):
echo ========================================================
type sample.txt
echo.
pause
