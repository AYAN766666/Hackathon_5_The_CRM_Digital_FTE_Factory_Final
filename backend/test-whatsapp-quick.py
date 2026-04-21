"""
Quick WhatsApp Test - Check if automation works
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_whatsapp_simple():
    """Test WhatsApp with simple approach"""
    print("="*60)
    print("WHATSAPP AUTOMATION TEST")
    print("="*60)
    print()
    
    try:
        from playwright.async_api import async_playwright
        
        phone = "923198130598"
        ticket_id = "TEST1234"
        message = f"Hello! Your support ticket {ticket_id} has been created. Test message from hackathon."
        
        print(f"📱 Sending to: {phone}")
        print(f"📝 Message: {message}")
        print()
        
        async with async_playwright() as p:
            print("🌐 Launching browser...")
            browser = await p.chromium.launch(
                headless=False,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            
            page = await browser.new_page()
            
            # Encode message
            message_encoded = message.replace(" ", "%20").replace("\n", "%0A")
            whatsapp_url = f"https://wa.me/{phone}?text={message_encoded}"
            
            print(f"🔗 Opening: {whatsapp_url}")
            await page.goto(whatsapp_url, timeout=30000)
            
            print("⏳ Waiting for chat to load (10 seconds)...")
            await asyncio.sleep(10)
            
            # Try to find send button
            try:
                send_button = await page.query_selector('button[data-testid="compose-btn-send"]')
                if send_button:
                    print("✅ Send button found!")
                    await send_button.click()
                    print("✅ CLICKED SEND!")
                    await asyncio.sleep(3)
                else:
                    print("⚠️ Send button not found - may need manual click")
            except Exception as e:
                print(f"⚠️ Error: {e}")
            
            print()
            print("="*60)
            print("TEST COMPLETE - Check your WhatsApp!")
            print("="*60)
            
            await asyncio.sleep(5)
            await browser.close()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_whatsapp_simple())
