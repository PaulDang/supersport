@echo off
REM This script is used to start a new Django app using the manage.py script.

REM Check if Python is installed and accessible in the system path
python --version >nul 2>&1
if errorlevel 1 (
    echo "Python is not installed or not accessible in the system path."
    exit /b
)

REM Check if manage.py exists in the current directory
if not exist manage.py (
    echo "manage.py not found in the current directory."
    exit /b
)

REM Check if an argument is provided
if "%~1"=="" (
    echo "Usage: startapp.bat <app_name>"
    exit /b
)

REM Run the startapp command
python manage.py startapp %1
