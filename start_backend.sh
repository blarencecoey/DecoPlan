#!/bin/bash

# Start script for DecoPlan Flask Backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found!"
    echo "Please run setup_backend.sh first:"
    echo "  chmod +x setup_backend.sh"
    echo "  ./setup_backend.sh"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if furniture_db exists
if [ ! -d "furniture_db" ]; then
    echo "Warning: furniture_db directory not found!"
    echo "The API will start but won't be fully functional."
    echo "Please run rag/build_furniture_db.py to create the database."
    echo ""
fi

# Start Flask app
echo "Starting Flask backend..."
echo "Server will be available at: http://localhost:5000"
echo "Press Ctrl+C to stop"
echo ""

python app.py
