@echo off
echo ========================================
echo   AI Object Detection Studio v6.1
echo   Automatic Installation Script
echo ========================================
echo.

echo [1/3] Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found! Please install Python first.
    pause
    exit /b 1
)

echo [2/3] Installing dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo [3/3] Setting up directories...
if not exist "models" mkdir models

echo.
echo ========================================
echo   Installation Complete!
echo ========================================
echo.
echo To run the application: python main_app.py
echo To add custom model: Place 'best.pt' in 'models' folder
echo.
pause
