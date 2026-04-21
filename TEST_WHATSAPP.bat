@echo off
REM Test WhatsApp Setup
echo ========================================
echo   WhatsApp Import Test
echo ========================================
echo.

cd "E:\Hackathon 5\The CRM Digital FTE Factory Final\backend"

echo Current directory: %CD%
echo.

echo Testing Python...
python --version
echo.

echo Testing imports...
python -c "from services.whatsapp_agent import WhatsAppAgent; print('WhatsApp Agent: OK')"
python -c "from routes.whatsapp import router; print('WhatsApp Routes: OK')"

echo.
echo Done!
pause
