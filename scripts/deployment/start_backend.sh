#!/bin/bash

# Start script for DecoPlan Flask Backend

# Get the script directory and project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/../.." && pwd )"

cd "$PROJECT_ROOT"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found!"
    echo "Please run scripts/setup/setup_backend.sh first:"
    echo "  bash scripts/setup/setup_backend.sh"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if furniture_db exists
if [ ! -d "data/furniture_db" ]; then
    echo "Warning: data/furniture_db directory not found!"
    echo "The API will start but won't be fully functional."
    echo "Please run: python -m backend.rag.build_furniture_db"
    echo ""
fi

# Start Flask app
echo "Starting Flask backend..."
echo "Server will be available at: http://localhost:5000"
echo "Press Ctrl+C to stop"
echo ""

# Run from project root using the convenience script
python run_backend.py
