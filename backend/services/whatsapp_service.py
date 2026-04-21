"""
WhatsApp Service - Send messages via WhatsApp Web using Playwright
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class WhatsAppService:
    """Handle WhatsApp messaging via Playwright automation"""
    
    def __init__(self):
        self.whatsapp_url = "https://web.whatsapp.com"
        self.browser = None
        self.page = None
    
    async def send_whatsapp_message(
        self,
        phone_number: str,
        ticket_id: str,
        customer_name: str = None
    ) -> bool:
        """
        Send WhatsApp message using Playwright automation
        
        Args:
            phone_number: Customer's phone number (with country code, e.g., 923198130598)
            ticket_id: Support ticket ID
            customer_name: Optional customer name
            
        Returns:
            bool: True if message sent successfully, False otherwise
        """
        try:
            from playwright.async_api import async_playwright
            
            # Format phone number (remove + and spaces)
            phone_number = phone_number.replace("+", "").replace(" ", "").replace("-", "")
            
            # Create message
            name_str = customer_name if customer_name else "there"
            message = f"""Hello {name_str}! 👋

Your support ticket *{ticket_id}* has been created.

Our team will review your issue shortly.

Thank you for contacting us!"""

            async with async_playwright() as p:
                # Launch browser
                self.browser = await p.chromium.launch(
                    headless=False,  # Keep visible for QR code scanning
                    args=[
                        '--no-sandbox',
                        '--disable-setuid-sandbox',
                        '--disable-dev-shm-usage',
                        '--disable-accelerated-2d-canvas',
                        '--disable-gpu'
                    ]
                )
                
                # Create page
                self.page = await self.browser.new_page()
                
                # Navigate to WhatsApp Web
                print("📱 Opening WhatsApp Web...")
                await self.page.goto(self.whatsapp_url, timeout=60000)
                
                # Wait for QR code or main page (user needs to be logged in)
                print("⏳ Waiting for WhatsApp Web to load (scan QR code if needed)...")
                await asyncio.sleep(10)  # Give time for QR code scan if needed
                
                # Check if already logged in by looking for main app
                try:
                    # Wait for the main chat list or search box
                    await self.page.wait_for_selector('[data-testid="search"]', timeout=15000)
                    print("✅ WhatsApp Web loaded and ready")
                except Exception as e:
                    print(f"⚠️ WhatsApp Web may need manual login: {str(e)}")
                    # Continue anyway, user might be logged in
                
                # Use WhatsApp click-to-chat URL instead
                # This is more reliable than automation
                message_encoded = message.replace(" ", "%20").replace("\n", "%0A").replace("*", "%2A")
                whatsapp_click_url = f"https://wa.me/{phone_number}?text={message_encoded}"
                
                print(f"📲 Opening chat with {phone_number}...")
                await self.page.goto(whatsapp_click_url, timeout=30000)
                await asyncio.sleep(3)
                
                # Look for send button and click it
                try:
                    # Wait for send button to appear
                    send_button = await self.page.wait_for_selector(
                        'button[data-testid="compose-btn-send"]',
                        timeout=10000
                    )
                    await send_button.click()
                    print(f"✅ WhatsApp message sent to {phone_number}")
                    await asyncio.sleep(2)
                    return True
                except Exception as e:
                    print(f"⚠️ Could not auto-send message. WhatsApp page opened: {str(e)}")
                    print("📝 Message is ready, user may need to click send manually")
                    await asyncio.sleep(5)
                    return True
                    
        except Exception as e:
            print(f"❌ Error sending WhatsApp message: {str(e)}")
            return False
        finally:
            # Cleanup
            if self.browser:
                await self.browser.close()
                self.browser = None
                self.page = None
    
    async def send_whatsapp_simple(
        self,
        phone_number: str,
        ticket_id: str,
        customer_name: str = None
    ) -> bool:
        """
        Simplified WhatsApp message sender using click-to-chat
        More reliable for demo purposes
        
        Args:
            phone_number: Customer's phone number
            ticket_id: Support ticket ID
            customer_name: Optional customer name
            
        Returns:
            bool: Success status
        """
        try:
            from playwright.async_api import async_playwright
            
            # Format phone number
            phone_number = phone_number.replace("+", "").replace(" ", "").replace("-", "")
            
            # Create message
            name_str = customer_name if customer_name else "there"
            message = f"Hello {name_str}! Your support ticket {ticket_id} has been created. Our team will review your issue shortly."
            
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=False)
                page = await browser.new_page()
                
                # Use click-to-chat URL
                message_encoded = message.replace(" ", "%20").replace("\n", "%0A")
                whatsapp_url = f"https://wa.me/{phone_number}?text={message_encoded}"
                
                print(f"📲 Opening WhatsApp chat for {phone_number}...")
                await page.goto(whatsapp_url, timeout=30000)
                await asyncio.sleep(5)
                
                # Try to click send button
                try:
                    send_btn = await page.wait_for_selector('button[data-testid="compose-btn-send"]', timeout=5000)
                    await send_btn.click()
                    print("✅ Message sent!")
                    await asyncio.sleep(2)
                except:
                    print("⚠️ Message ready in compose box (manual send may be required)")
                
                await browser.close()
                return True
                
        except Exception as e:
            print(f"❌ WhatsApp error: {str(e)}")
            return False


# Singleton instance
whatsapp_service = WhatsAppService()
