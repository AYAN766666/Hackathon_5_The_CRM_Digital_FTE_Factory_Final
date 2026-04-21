@echo off
REM Run Backend Server
echo Starting Customer Success FTE Backend...
echo.

cd /d "%~dp0"

echo Current directory: %CD%
echo.
echo Starting uvicorn server...
echo Backend will be available at: http://localhost:8000
echo API docs at: http://localhost:8000/docs
echo.

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause
