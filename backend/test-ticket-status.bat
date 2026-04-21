@echo off
REM Quick Ticket Status Test
cd /d "%~dp0"

echo.
echo ================================================
echo   Quick Ticket Status Test
echo ================================================
echo.
echo Opening Swagger UI in your browser...
echo.
echo 1. Go to: http://localhost:8000/docs
echo 2. Create a ticket using POST /support/submit
echo 3. Copy the ticket_id (e.g., 928054FD)
echo 4. Test GET /support/ticket/{ticket_id}
echo.
echo Launching browser...
start http://localhost:8000/docs
echo.
echo Done! Test the APIs in Swagger UI.
echo ================================================
echo.
pause
