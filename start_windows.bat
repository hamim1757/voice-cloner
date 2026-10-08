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
    echo Python is not installed.
    echo Install Python 3.12 and then double-click this file again.
    echo.
    pause
    exit /b 1
)

set "PYTHON_CMD="
py -3.12 -V >nul 2>&1 && set "PYTHON_CMD=py -3.12"
if not defined PYTHON_CMD py -3.13 -V >nul 2>&1 && set "PYTHON_CMD=py -3.13"
if not defined PYTHON_CMD py -3.11 -V >nul 2>&1 && set "PYTHON_CMD=py -3.11"
if not defined PYTHON_CMD py -3.10 -V >nul 2>&1 && set "PYTHON_CMD=py -3.10"
if not defined PYTHON_CMD py -3.14 -V >nul 2>&1 && set "PYTHON_CMD=py -3.14"

if not defined PYTHON_CMD (
    echo No supported Python version was found.
    echo Supported versions: 3.10, 3.11, 3.12, 3.13, or 3.14.
    echo.
    echo Install Python 3.12, then run this file again.
    echo.
    pause
    exit /b 1
)

echo Using %PYTHON_CMD%
echo.

if not exist ".venv\Scripts\python.exe" (
    echo [1/3] Creating the Python environment...
    %PYTHON_CMD% -m venv .venv
    if errorlevel 1 (
        echo Could not create the environment.
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
    echo.
    pause
    exit /b 1
)

echo.
echo [3/3] Starting Voice Cloner...
echo.
echo Keep this window open while using the app.
echo.

".venv\Scripts\python.exe" app.py
pause
