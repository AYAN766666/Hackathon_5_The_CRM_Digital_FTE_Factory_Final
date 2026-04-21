import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from services.whatsapp_agent import WhatsAppAgent
    print("✅ WhatsApp Agent import OK")
    
    from routes.whatsapp import router
    print("✅ WhatsApp routes import OK")
    
    print("\n✅ All WhatsApp imports successful!")
    
except Exception as e:
    print(f"❌ Import error: {str(e)}")
    import traceback
    traceback.print_exc()
