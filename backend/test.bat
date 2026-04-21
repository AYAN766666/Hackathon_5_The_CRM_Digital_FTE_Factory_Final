@echo off
REM Test Backend Config
cd /d "%~dp0"
echo Testing backend configuration...
python test_config.py
pause
