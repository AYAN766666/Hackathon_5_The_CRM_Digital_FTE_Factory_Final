@echo off
REM Start Backend Server - Simple Version
cd /d "%~dp0"

echo ===============================================
echo Customer Success FTE - Backend Server
echo ===============================================
echo.
echo Starting FastAPI server...
echo Backend: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo ===============================================
echo.

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Server failed to start!
    echo Check the error message above.
    echo.
    pause
)
