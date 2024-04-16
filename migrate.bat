@echo off
if "%~1" == "-M" (
    python manage.py makemigrations
    exit /b
)
if "%~1" == "-m" (
    python manage.py makemigrations
    exit /b
)

python manage.py migrate
