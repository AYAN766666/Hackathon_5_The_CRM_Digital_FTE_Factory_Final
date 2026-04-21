@echo off
REM Test Backend API
cd /d "%~dp0"

echo ================================================
echo Testing Backend API
echo ================================================
echo.

echo 1. Testing Health Endpoint...
curl http://localhost:8000/health
echo.
echo.

echo 2. Testing Root Endpoint...
curl http://localhost:8000/
echo.
echo.

echo 3. Testing API Docs...
curl http://localhost:8000/docs ^| findstr /C:"title"
echo.

echo ================================================
echo Tests Complete!
echo ================================================
pause
