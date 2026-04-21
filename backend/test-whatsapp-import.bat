@echo off
REM Test WhatsApp imports
cd /d "%~dp0"

echo Testing WhatsApp imports...
echo.

python test-whatsapp-import.py

echo.
pause
