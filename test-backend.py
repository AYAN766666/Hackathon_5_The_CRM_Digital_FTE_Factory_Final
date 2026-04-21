import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("Testing imports...")
print()

try:
    print("1. Testing main app import...")
    from main import app
    print("   ✅ Main app imported successfully!")
    print()
    
    print("2. Testing WhatsApp agent import...")
    from services.whatsapp_agent import WhatsAppAgent, get_whatsapp_agent
    print("   ✅ WhatsApp agent imported successfully!")
    print()
    
    print("3. Testing WhatsApp routes import...")
    from routes.whatsapp import router as whatsapp_router
    print("   ✅ WhatsApp routes imported successfully!")
    print()
    
    print("4. Testing webform routes import...")
    from routes.webform import router as webform_router
    print("   ✅ Webform routes imported successfully!")
    print()
    
    print("=" * 50)
    print("✅ ALL IMPORTS SUCCESSFUL!")
    print("=" * 50)
    print()
    print("Backend is ready to start!")
    print("Run: uvicorn main:app --reload")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
    input("\nPress Enter to exit...")
