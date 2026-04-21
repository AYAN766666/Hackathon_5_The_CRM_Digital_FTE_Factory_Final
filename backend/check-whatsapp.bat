@echo off
cd /d "%~dp0"
python -c "import ast; ast.parse(open('services/whatsapp_agent.py').read()); print('whatsapp_agent.py: Syntax OK')"
pause
