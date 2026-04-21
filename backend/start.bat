@echo off
REM ================================================
REM Customer Success FTE - Quick Start
REM ================================================

cd /d "%~dp0"

cls
echo.
echo ================================================
echo   Customer Success FTE - Backend Server
echo ================================================
echo.
echo   Starting server...
echo.
echo   Backend: http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo.
echo   Press Ctrl+C to stop
echo ================================================
echo.

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

if %errorlevel% neq 0 (
    echo.
    echo ================================================
    echo   ERROR: Server failed to start!
    echo ================================================
    echo.
    echo   Common fixes:
    echo   1. Check if Python is installed: python --version
    echo   2. Install dependencies: pip install -r requirements.txt
    echo   3. Check .env file exists
    echo   4. Check if port 8000 is free
    echo.
    pause
)
