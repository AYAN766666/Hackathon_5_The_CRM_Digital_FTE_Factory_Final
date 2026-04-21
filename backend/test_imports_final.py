print("=" * 50)
print("  Testing Backend Imports")
print("=" * 50)
print()

try:
    print("1. Testing WhatsApp Agent...")
    from services.whatsapp_agent import WhatsAppAgent
    print("   OK")
except Exception as e:
    print(f"   ERROR: {e}")

try:
    print("2. Testing WhatsApp Routes...")
    from routes.whatsapp import router
    print("   OK")
except Exception as e:
    print(f"   ERROR: {e}")

try:
    print("3. Testing Webform Routes...")
    from routes.webform import router as webform_router
    print("   OK")
except Exception as e:
    print(f"   ERROR: {e}")

try:
    print("4. Testing Main App...")
    from main import app
    print("   OK")
except Exception as e:
    print(f"   ERROR: {e}")

print()
print("=" * 50)
print("  Import Test Complete!")
print("=" * 50)
print()
input("Press Enter to exit...")
