@echo off
setlocal
cd /d "%~dp0"
title MailSense AI - Setup and Launch

echo.
echo ==========================================
echo          MailSense AI - Launcher
echo ==========================================
echo.

where py >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python launcher was not found.
    echo Install Python 3.10 or newer from https://www.python.org/downloads/
    echo During installation, enable the option to add Python to PATH.
    goto :failed
)

if not exist ".venv\Scripts\python.exe" (
    echo [1/3] Creating the project environment...
    py -3 -m venv .venv
    if errorlevel 1 goto :failed
) else (
    echo [1/3] Existing project environment found.
)

echo.
echo [2/3] Installing required packages...
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto :failed
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto :failed

echo.
echo [3/3] Starting MailSense AI...
echo The browser should open automatically. Keep this window open.
echo Press Ctrl+C in this window to stop the app.
echo.
".venv\Scripts\python.exe" -m streamlit run app.py
goto :done

:failed
echo.
echo Setup could not finish. Read the error above.
echo If Python is missing, install Python 3.10+ and run this file again.
pause
exit /b 1

:done
endlocal
