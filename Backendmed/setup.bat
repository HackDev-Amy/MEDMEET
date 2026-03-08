@echo off
REM MedMeet Setup Script for Windows
echo.
echo ===== MedMeet Setup =====
echo.

REM Check if Python is installed
py -3 --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python 3 is not installed or not in PATH
    echo Please install Python 3.11+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/5] Creating virtual environment...
py -3 -m venv .venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/5] Activating virtual environment...
call .venv\Scripts\activate.bat

echo [3/5] Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [4/5] Running database migrations...
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Failed to run migrations
    pause
    exit /b 1
)

echo [5/5] Setup complete!
echo.
echo ===== Next Steps =====
echo 1. Create an admin account:
echo    python manage.py createsuperuser
echo.
echo 2. Start the development server:
echo    python manage.py runserver
echo.
echo 3. Open your browser and visit:
echo    http://127.0.0.1:8000/
echo.
echo ===== Access Points =====
echo Admin Dashboard: http://127.0.0.1:8000/Backendmed/back_main/
echo Patient Portal: http://127.0.0.1:8000/frontendmed/Med_Meet/
echo Django Admin: http://127.0.0.1:8000/admin/
echo.
pause
