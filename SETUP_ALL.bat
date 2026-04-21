@echo off
REM ========================================
REM   Hackathon 5 - Complete Setup
REM ========================================

echo ========================================
echo   Hackathon 5 - Setup Script
echo ========================================
echo.

cd /d "%~dp0backend"

echo Step 1: Installing Python dependencies...
echo.
uv sync
echo.

echo Step 2: Installing Playwright browser...
echo.
python -m playwright install chromium
echo.

echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next Steps:
echo.
echo 1. Start Backend:
echo    cd backend
echo    uvicorn main:app --reload
echo.
echo 2. First-time WhatsApp Login:
echo    python test-whatsapp.py
echo    (Scan QR code when browser opens)
echo.
echo 3. Start Frontend (in another terminal):
echo    cd forened
echo    npm run dev
echo.
echo 4. Open Browser:
echo    http://localhost:3000
echo.
echo ========================================
echo.
pause
