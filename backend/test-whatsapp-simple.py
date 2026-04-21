"""
Simple WhatsApp Test - Manual approach for Pakistan
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_whatsapp_manual():
    """Test WhatsApp manually - user needs to be logged in"""
    print("="*60)
    print("SIMPLE WHATSAPP TEST (Pakistan Friendly)")
    print("="*60)
    print()
    
    phone = "923198130598"
    ticket_id = "HACK5TEST"
    name = "Hackathon User"
    
    message = f"""Hello {name}! 👋

Your support ticket *{ticket_id}* has been created.

Our team will review your issue shortly.

Thank you for contacting us!"""

    print(f"📱 Phone: {phone}")
    print(f"📝 Message: {message[:100]}...")
    print()
    print("INSTRUCTIONS:")
    print("1. Browser will open WhatsApp Web")
    print("2. If QR code shows, scan with your phone")
    print("3. After login, message will be sent automatically")
    print()
    print("Press Enter to start...")
    input()
    
    try:
        from playwright.async_api import async_playwright
        
        async with async_playwright() as p:
            print("🚀 Launching browser...")
            browser = await p.chromium.launch(
                headless=False,
                args=['--no-sandbox']
            )
            
            page = await browser.new_page()
            
            # Go to WhatsApp Web
            print("📱 Opening WhatsApp Web...")
            await page.goto("https://web.whatsapp.com", timeout=60000)
            
            print("⏳ Waiting for login (60 seconds)...")
            print("📱 SCAN QR CODE IF SHOWN!")
            
            # Wait for search box (indicates logged in)
            try:
                await page.wait_for_selector('[data-testid="search"][role="textbox"]', timeout=60000)
                print("✅ Logged in!")
            except:
                print("⚠️ Not logged in yet. Please scan QR code manually.")
                await asyncio.sleep(10)
            
            # Search for phone number
            print(f"🔍 Searching for {phone}...")
            search_box = await page.query_selector('[data-testid="search"][role="textbox"]')
            if search_box:
                await search_box.click()
                await page.keyboard.type(phone)
                await asyncio.sleep(2)
                
                # Press Enter to open chat
                print("📩 Opening chat...")
                await page.keyboard.press("Enter")
                await asyncio.sleep(2)
                
                # Type message
                print("✏️ Typing message...")
                chat_input = await page.query_selector('[data-testid="compose-box-input"]')
                if chat_input:
                    await chat_input.fill(message)
                    await asyncio.sleep(1)
                    
                    # Send
                    print("📤 Sending...")
                    await page.keyboard.press("Enter")
                    await asyncio.sleep(2)
                    
                    print("✅ MESSAGE SENT!")
                else:
                    print("❌ Chat input not found")
            else:
                print("❌ Search box not found - may not be logged in")
            
            print()
            print("="*60)
            print("TEST COMPLETE")
            print("="*60)
            
            await asyncio.sleep(5)
            await browser.close()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Starting WhatsApp Manual Test...")
    asyncio.run(test_whatsapp_manual())
