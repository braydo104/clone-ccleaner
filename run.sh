#!/bin/bash
# CCleaner Clone 7 - Launch Script (Linux/macOS)

cd "$(dirname "$0")"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed."
    echo "Please install Python 3.7 or later"
    exit 1
fi

# Run the application
python3 app.py
