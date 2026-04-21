@echo off
REM Customer Success FTE - Setup and Run Script for Windows
REM This script sets up and runs both backend and frontend

echo ========================================
echo Customer Success FTE - Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python 3.9+ is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js 18+ is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)

echo [1/5] Setting up Backend...
cd backend

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo Creating Python virtual environment...
    uv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate

REM Install dependencies
echo Installing Python dependencies...
uv sync

echo.
echo [2/5] Configuring Backend Environment...
if not exist ".env" (
    echo Creating .env from .env.example...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please update backend\.env with your Gemini API key
    echo Get your API key from: https://makersuite.google.com/app/apikey
    echo.
    notepad .env
)

cd ..

echo.
echo [3/5] Setting up Frontend...
cd forened

REM Install Node dependencies
echo Installing Node.js dependencies...
call npm install

cd ..

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To run the application:
echo.
echo 1. Backend (Terminal 1):
echo    cd backend
echo    .venv\Scripts\activate
echo    uvicorn main:app --reload --host 0.0.0.0 --port 8000
echo.
echo 2. Frontend (Terminal 2):
echo    cd forened
echo    npm run dev
echo.
echo Then open: http://localhost:3000
echo.
echo API Docs: http://localhost:8000/docs
echo ========================================
echo.
pause
