@echo off
REM MedMeet Run Script for Windows

echo.
echo ===== MedMeet Development Server =====
echo.

REM Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

echo Starting development server...
echo.
echo Access the application at: http://127.0.0.1:8000/
echo Press CTRL+C to stop the server
echo.

python manage.py runserver

pause
