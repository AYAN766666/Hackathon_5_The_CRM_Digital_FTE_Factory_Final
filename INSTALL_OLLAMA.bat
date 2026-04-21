@echo off
REM =====================================================
REM OLLAMA AUTO-INSTALL SCRIPT
REM =====================================================

echo.
echo =====================================================
echo   OLLAMA INSTALLATION SCRIPT
echo =====================================================
echo.

REM Check if Ollama is installed
where ollama >nul 2>&1
if %errorlevel% == 0 (
    echo [OK] Ollama already installed!
    goto :INSTALL_MODEL
) else (
    echo [INFO] Ollama not found. Installing...
)

echo.
echo Step 1: Downloading Ollama...
echo.

REM Download Ollama installer
curl -L https://ollama.com/download/OllamaSetup.exe -O "%TEMP%\OllamaSetup.exe"

if exist "%TEMP%\OllamaSetup.exe" (
    echo [OK] Download complete!
    echo.
    echo Step 2: Installing Ollama...
    echo.
    echo [ACTION] Please run the installer manually:
    echo         %TEMP%\OllamaSetup.exe
    echo.
    echo After installation, close this window and run:
    echo         INSTALL_MODEL.bat
    pause
) else (
    echo [ERROR] Download failed!
    echo.
    echo Please download manually from:
    echo https://ollama.com/download
    pause
    exit /b 1
)

goto :EOF

:INSTALL_MODEL
echo.
echo =====================================================
echo   INSTALLING LLAMA 3.2 MODEL
echo =====================================================
echo.
echo This will download ~4GB. Please wait...
echo.

REM Start Ollama and download model
start "Installing Llama 3.2..." /MIN cmd /c "ollama run llama3.2"

echo.
echo [OK] Model download started in new window!
echo.
echo Please wait for the download to complete.
echo After completion, close all windows and run:
echo         START_QUICK.bat
echo.
pause
