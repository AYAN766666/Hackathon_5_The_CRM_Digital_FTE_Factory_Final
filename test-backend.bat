@echo off
REM Test Backend Imports
cd /d "%~dp0"

echo Testing Backend Imports...
echo.

cd backend
python -c "from services.whatsapp_agent import WhatsAppAgent; print('WhatsApp Agent: OK')"
python -c "from routes.whatsapp import router; print('WhatsApp Routes: OK')"
python -c "from routes.webform import router; print('Webform Routes: OK')"
python -c "from main import app; print('Main App: OK')"

echo.
echo All imports tested!
pause
