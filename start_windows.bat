@echo off
setlocal
cd /d "%~dp0"
title Voice Cloner

echo ========================================
echo          VOICE CLONER
echo ========================================
echo.

where py >nul 2>nul
if errorlevel 1 (
    echo Python was not found.
    echo Install Python 3.11 from python.org, then run this file again.
    echo Make sure "Add Python to PATH" is enabled during installation.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo [1/3] Creating the Python environment...
    py -3.11 -m venv .venv
    if errorlevel 1 (
        echo Could not create the environment.
        echo Make sure Python 3.11 is installed.
        pause
        exit /b 1
    )
)

echo [2/3] Installing/checking dependencies...
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo Dependency installation failed.
    pause
    exit /b 1
)

echo.
echo [3/3] Starting Voice Cloner...
echo.
echo Keep this window open while using the app.
echo Your browser should open automatically.
echo.

".venv\Scripts\python.exe" app.py
pause
