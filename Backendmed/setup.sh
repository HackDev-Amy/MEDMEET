#!/bin/bash

# MedMeet Setup Script for macOS/Linux

echo ""
echo "===== MedMeet Setup ====="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.11+ from https://www.python.org/"
    exit 1
fi

echo "[1/5] Creating virtual environment..."
python3 -m venv .venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

echo "[2/5] Activating virtual environment..."
source .venv/bin/activate

echo "[3/5] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo "[4/5] Running database migrations..."
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to run migrations"
    exit 1
fi

echo "[5/5] Setup complete!"
echo ""
echo "===== Next Steps ====="
echo "1. Create an admin account:"
echo "   python manage.py createsuperuser"
echo ""
echo "2. Start the development server:"
echo "   python manage.py runserver"
echo ""
echo "3. Open your browser and visit:"
echo "   http://127.0.0.1:8000/"
echo ""
echo "===== Access Points ====="
echo "Admin Dashboard: http://127.0.0.1:8000/Backendmed/back_main/"
echo "Patient Portal: http://127.0.0.1:8000/frontendmed/Med_Meet/"
echo "Django Admin: http://127.0.0.1:8000/admin/"
echo ""
