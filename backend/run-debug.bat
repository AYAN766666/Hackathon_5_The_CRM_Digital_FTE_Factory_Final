@echo off
REM Run backend and show errors
cd /d "%~dp0"

echo ================================================
echo Starting Backend Server...
echo ================================================
echo.

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

echo.
echo Server stopped.
pause
