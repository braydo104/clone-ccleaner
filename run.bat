@echo off
REM CCleaner Clone 7 - Launch Script
REM This script starts the CCleaner Clone application

cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.7 or later from https://python.org
    pause
    exit /b 1
)

REM Run the application
python app.py
