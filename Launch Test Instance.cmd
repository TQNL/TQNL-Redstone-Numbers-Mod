@echo off
setlocal
cd /d "%~dp0"
where pythonw.exe >nul 2>&1
if not errorlevel 1 (
    start "" pythonw.exe "%~dp0tools\test_launcher.py"
    exit /b
)
python tools\test_launcher.py
if errorlevel 1 pause
