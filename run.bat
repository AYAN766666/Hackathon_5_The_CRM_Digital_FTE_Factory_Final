@echo off
REM Customer Success FTE - Run Script for Windows
REM Runs both backend and frontend simultaneously

echo ========================================
echo Customer Success FTE - Running...
echo ========================================
echo.
echo Starting Backend on http://localhost:8000
echo Starting Frontend on http://localhost:3000
echo.
echo Press Ctrl+C in each window to stop
echo ========================================
echo.

REM Start Backend in new window
start "Backend - Customer Success FTE" cmd /k "cd backend && .venv\Scripts\activate && uvicorn main:app --reload --host 0.0.0.0 --port 8000"

REM Wait a bit for backend to start
timeout /t 3 /nobreak >nul

REM Start Frontend in new window
start "Frontend - Customer Success FTE" cmd /k "cd forened && npm run dev"

echo.
echo Both servers are starting...
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Close the terminal windows to stop the servers
echo.
pause
