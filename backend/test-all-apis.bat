@echo off
REM ================================================
REM Complete API Test Suite
REM ================================================

cd /d "%~dp0"

echo.
echo ================================================
echo   Customer Success FTE - API Test Suite
echo ================================================
echo.

echo [1/4] Testing Root Endpoint...
echo ----------------------------------------
curl -s http://localhost:8000/
echo.
echo.

echo [2/4] Testing Health Endpoint...
echo ----------------------------------------
curl -s http://localhost:8000/health
echo.
echo.

echo [3/4] Testing API Docs...
echo ----------------------------------------
curl -s http://localhost:8000/docs | findstr /C:"<title>"
echo.

echo [4/4] Testing Submit Support Request...
echo ----------------------------------------
curl -X POST http://localhost:8000/support/submit ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"Test User\",\"email\":\"test@example.com\",\"category\":\"Technical\",\"message\":\"This is a test message to verify the API is working correctly. This message has enough characters.\"}"
echo.
echo.

echo ================================================
echo   API Test Suite Complete!
echo ================================================
echo.

pause
