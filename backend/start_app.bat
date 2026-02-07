@echo off
title Smart Grocery Recipe Planner
echo ========================================
echo   Smart Grocery + Recipe Planner
echo ========================================
echo.

echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)
echo ✅ Python is available

echo.
echo [2/4] Changing to project directory...
cd /d "F:\Chatbot\smart-grocery-recipe-planner\backend"
if errorlevel 1 (
    echo ERROR: Cannot access project directory
    pause
    exit /b 1
)
echo ✅ Project directory: %cd%

echo.
echo [3/4] Installing/checking dependencies...
pip install flask flask-cors python-dotenv --quiet
if errorlevel 1 (
    echo WARNING: Some packages may not have installed correctly
)
echo ✅ Dependencies checked

echo.
echo [4/4] Starting Flask application...
echo.
echo ==========================================
echo 🚀 Starting Smart Grocery Recipe Planner
echo 📱 Access your app at: http://localhost:5000
echo 🔥 Press Ctrl+C to stop the server
echo ==========================================
echo.

python flask_app.py

echo.
echo Server stopped. Press any key to exit...
pause >nul
