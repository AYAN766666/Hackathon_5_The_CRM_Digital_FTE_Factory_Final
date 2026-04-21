import ast
import sys

print("Checking Python syntax...")
print()

files_to_check = [
    'main.py',
    'services/whatsapp_agent.py',
    'routes/whatsapp.py',
    'routes/webform.py'
]

all_ok = True

for filepath in files_to_check:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        ast.parse(code)
        print(f"  {filepath}: OK")
    except SyntaxError as e:
        print(f"  {filepath}: SYNTAX ERROR - {e}")
        all_ok = False
    except Exception as e:
        print(f"  {filepath}: ERROR - {e}")
        all_ok = False

print()
if all_ok:
    print("All files have valid Python syntax!")
else:
    print("Some files have errors!")

input("\nPress Enter to exit...")
