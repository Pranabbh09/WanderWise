#!/bin/bash

echo "🌍 Smart Place Recommender"
echo "================================"
echo ""
echo "🚀 Starting the application..."
echo ""
echo "📍 The website will open automatically in your browser"
echo "🔗 Or visit: http://localhost:5000"
echo ""
echo "⏹️  Press Ctrl+C to stop the application"
echo "================================="
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "✅ Virtual environment found, activating..."
    source venv/bin/activate
else
    echo "⚠️  Virtual environment not found, using system Python..."
fi

# Check if requirements are installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "❌ Flask not found. Installing requirements..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install requirements. Please check your Python installation."
        exit 1
    fi
fi

# Make the script executable
chmod +x run.py

# Start the application
echo "🚀 Launching Smart Place Recommender..."
python3 run.py

