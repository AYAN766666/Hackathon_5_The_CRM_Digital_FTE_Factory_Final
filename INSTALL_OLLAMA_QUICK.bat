@echo off
REM =====================================================
REM QUICK OLLAMA INSTALL
REM =====================================================

echo.
echo =====================================================
echo   INSTALLING OLLAMA
echo =====================================================
echo.

echo Step 1: Downloading Ollama Installer...
echo.

REM Download installer
curl -L https://ollama.com/download/OllamaSetup.exe -o "%TEMP%\OllamaSetup.exe"

if exist "%TEMP%\OllamaSetup.exe" (
    echo [OK] Download complete!
    echo.
    echo Step 2: Starting Installer...
    echo.
    echo [ACTION] Installer window open ho raha hai.
    echo         Please install Ollama.
    echo.
    
    REM Start installer
    start "" "%TEMP%\OllamaSetup.exe"
    
    echo.
    echo =====================================================
    echo   AFTER INSTALLATION:
    echo =====================================================
    echo.
    echo 1. Close this window
    echo 2. Open NEW Command Prompt
    echo 3. Run: ollama run llama3.2
    echo 4. Wait for model download
    echo 5. Run: START_QUICK.bat
    echo.
    pause
) else (
    echo [ERROR] Download failed!
    echo.
    echo Please download manually from:
    echo https://ollama.com/download
    echo.
    pause
    exit /b 1
)
