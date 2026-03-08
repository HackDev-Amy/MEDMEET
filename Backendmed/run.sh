#!/bin/bash

# MedMeet Run Script for macOS/Linux

echo ""
echo "===== MedMeet Development Server ====="
echo ""

# Check if virtual environment exists
if [ ! -f ".venv/bin/activate" ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please run setup.sh first"
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

echo "Starting development server..."
echo ""
echo "Access the application at: http://127.0.0.1:8000/"
echo "Press CTRL+C to stop the server"
echo ""

python manage.py runserver
