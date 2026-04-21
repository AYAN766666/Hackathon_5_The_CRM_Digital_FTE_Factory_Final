@echo off
REM Quick Test Script
cd /d "%~dp0"
python -c "import uvicorn; print('Uvicorn OK:', uvicorn.__version__)"
pause
