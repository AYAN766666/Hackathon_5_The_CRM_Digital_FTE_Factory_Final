@echo off
REM =====================================================
REM HACKATHON 5 - QUICK START SCRIPT
REM Customer Success FTE - Multi-Channel AI Support
REM =====================================================

echo.
echo =====================================================
echo   HACKATHON 5 - QUICK START
echo   Customer Success FTE System
echo =====================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.9+ and try again
    pause
    exit /b 1
)

echo [1/4] Python found...
python --version
echo.

REM Navigate to backend directory
cd /d "%~dp0backend"

REM Install dependencies
echo [2/4] Installing Python dependencies...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed
echo.

REM Check if .env exists
if not exist ".env" (
    echo [WARNING] .env file not found!
    echo Please create .env file with required configuration:
    echo   - DATABASE_URL
    echo   - GEMINI_API_KEY
    echo   - GMAIL_EMAIL
    echo   - GMAIL_APP_PASSWORD
    echo.
    pause
)

echo [3/4] Starting Backend Server...
echo.
echo =====================================================
echo   Backend will start at: http://localhost:8000
echo   API Docs at: http://localhost:8000/docs
echo   Health Check: http://localhost:8000/health
echo =====================================================
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause
