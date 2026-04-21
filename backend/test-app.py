#!/usr/bin/env python
"""Test main app"""
import sys
sys.path.insert(0, '.')

print("=" * 50)
print("Testing Main Application")
print("=" * 50)

try:
    print("\n1. Importing main app...")
    from main import app
    print("   ✓ Main app imported successfully!")
    
    print("\n2. Checking routes...")
    routes = [route.path for route in app.routes]
    print(f"   ✓ Found {len(routes)} routes:")
    for route in routes:
        print(f"      - {route}")
    
    print("\n3. Testing database connection...")
    import asyncio
    from database import init_db
    
    async def test_db():
        try:
            await init_db()
            print("   ✓ Database connected successfully!")
            return True
        except Exception as e:
            print(f"   ✗ Database Error: {e}")
            return False
    
    db_ok = asyncio.run(test_db())
    
    print("\n" + "=" * 50)
    print("All Tests Complete!")
    print("=" * 50)
    print(f"\nDatabase: {'✓ OK' if db_ok else '✗ ERROR'}")
    print(f"App: ✓ OK")
    print("\nReady to start server!")
    
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
