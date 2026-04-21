@echo off
REM Start WhatsApp Agent
REM This script starts the WhatsApp agent with persistent session

echo ========================================
echo   WhatsApp Agent Starter
echo ========================================
echo.

cd /d "%~dp0"

echo Starting WhatsApp Agent...
echo.
echo IMPORTANT: 
echo - A browser window will open
echo - If you see a QR code, scan it with your WhatsApp app
echo - Once logged in, the session will be saved
echo - Keep this window open while using the application
echo.
echo Press Ctrl+C to stop the agent
echo.

python services\whatsapp_agent.py

pause
