import sys
sys.path.insert(0, '.')
from main import app
print("Backend imports OK!")
print(f"App title: {app.title}")
