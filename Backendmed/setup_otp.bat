@echo off
REM Setup script for OTP System
echo ===============================================================================
echo MEDMEET OTP SYSTEM - SETUP SCRIPT
echo ===============================================================================

cd /d "C:\Users\amiam\Downloads\Books\Books\Projects Zipped\Final Project\FINAL PRO\Backendmed"

echo.
echo [1/5] Installing Django and core dependencies...
python -m pip install --no-cache-dir Django==6.0.2 asgiref sqlparse tzdata
if %ERRORLEVEL% NEQ 0 goto error

echo.
echo [2/5] Installing python-decouple for configuration...
python -m pip install --no-cache-dir python-decouple
if %ERRORLEVEL% NEQ 0 goto error

echo.
echo [3/5] Installing boto3 for AWS SNS (optional)...
python -m pip install --no-cache-dir boto3
if %ERRORLEVEL% NEQ 0 goto error

echo.
echo [4/5] Running Django checks...
python manage.py check
if %ERRORLEVEL% NEQ 0 goto error

echo.
echo [5/5] Setting up database...
REM Database should already be set up from previous migration
if NOT exist db.sqlite3 (
    python manage.py makemigrations
    python manage.py migrate
)

echo.
echo ===============================================================================
echo.
echo ✓ SETUP COMPLETE!
echo.
echo Next Steps:
echo   1. Create a .env file (if not exists) with:
echo      SMS_PROVIDER=MOCK
echo      OTP_VALIDITY_MINUTES=10
echo      OTP_LENGTH=6
echo .
echo   2. Start Django server:
echo      python manage.py runserver
echo .
echo   3. Visit OTP login page:
echo      http://localhost:8000/frontendmed/otp_login/
echo .
echo ===============================================================================
goto end

:error
echo.
echo ✗ ERROR during setup! Please check the output above.
echo.
exit /b 1

:end
