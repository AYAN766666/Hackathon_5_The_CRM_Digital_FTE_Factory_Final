#!/usr/bin/env python
"""Quick test"""
import sys
sys.path.insert(0, '.')

print("Testing config...")
try:
    from config import settings
    print("✓ Config loaded!")
    print(f"Database: {settings.database_url[:30]}...")
except Exception as e:
    print(f"✗ Config Error: {e}")
    import traceback
    traceback.print_exc()
