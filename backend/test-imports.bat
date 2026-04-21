@echo off
REM Test All Imports
cd /d "%~dp0"

echo ========================================
echo   Testing Backend Imports
echo ========================================
echo.

echo 1. Testing WhatsApp Agent...
python -c "from services.whatsapp_agent import WhatsAppAgent; print('   OK')"
if errorlevel 1 goto error

echo 2. Testing WhatsApp Routes...
python -c "from routes.whatsapp import router; print('   OK')"
if errorlevel 1 goto error

echo 3. Testing Webform Routes...
python -c "from routes.webform import router; print('   OK')"
if errorlevel 1 goto error

echo 4. Testing Main App...
python -c "from main import app; print('   OK')"
if errorlevel 1 goto error

echo.
echo ========================================
echo   ALL IMPORTS SUCCESSFUL!
echo ========================================
echo.
echo Backend is ready!
echo Run: uvicorn main:app --reload
echo.
pause
exit /b 0

:error
echo.
echo ========================================
echo   IMPORT ERROR!
echo ========================================
echo.
pause
exit /b 1
