@echo off
REM Test all backend imports
cd /d "%~dp0"
echo Running import tests...
python test_imports.py
pause
