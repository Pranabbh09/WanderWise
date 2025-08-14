@echo off
echo 🌍 Smart Place Recommender
echo ================================
echo.
echo 🚀 Starting the application...
echo.
echo 📍 The website will open automatically in your browser
echo 🔗 Or visit: http://localhost:5000
echo.
echo ⏹️  Press Ctrl+C to stop the application
echo ================================
echo.

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo ✅ Virtual environment found, activating...
    call venv\Scripts\activate.bat
) else (
    echo ⚠️  Virtual environment not found, using system Python...
)

REM Check if requirements are installed
python -c "import flask" 2>nul
if errorlevel 1 (
    echo ❌ Flask not found. Installing requirements...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install requirements. Please check your Python installation.
        pause
        exit /b 1
    )
)

REM Start the application
echo 🚀 Launching Smart Place Recommender...
python run.py

pause

