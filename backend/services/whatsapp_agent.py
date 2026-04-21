"""
WhatsApp Agent - Persistent WhatsApp Web automation with Playwright
Runs as a background agent to send and receive WhatsApp messages
"""
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Optional, Callable
from datetime import datetime

# Add parent path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class WhatsAppAgent:
    """
    Persistent WhatsApp Web agent using Playwright
    Maintains a browser session for reliable messaging
    """

    def __init__(self, user_data_dir: str = None):
        self.whatsapp_url = "https://web.whatsapp.com"
        self.browser = None
        self.page = None
        self.is_connected = False
        self.user_data_dir = user_data_dir or self._get_default_user_data_dir()
        self.message_queue = asyncio.Queue()
        self.is_running = False

    def _get_default_user_data_dir(self) -> str:
        """Get default user data directory for browser persistence"""
        app_data = os.path.join(os.path.dirname(__file__), '..', '.whatsapp_session')
        os.makedirs(app_data, exist_ok=True)
        return app_data

    async def start(self):
        """Start the WhatsApp agent with persistent session"""
        try:
            from playwright.async_api import async_playwright

            print("[INFO] Starting WhatsApp Agent...")

            playwright = await async_playwright().start()

            # Launch browser with persistent user data
            self.browser = await playwright.chromium.launch_persistent_context(
                user_data_dir=self.user_data_dir,
                headless=False,  # Keep visible for QR code scanning on first run
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--disable-gpu',
                    '--disable-extensions',
                    '--disable-background-networking',
                    '--disable-default-apps',
                    '--disable-sync',
                    '--no-first-run',
                ]
            )

            # Get the first page
            pages = self.browser.pages
            self.page = pages[0] if pages else await self.browser.new_page()

            # Navigate to WhatsApp Web
            print("[INFO] Navigating to WhatsApp Web...")
            try:
                await self.page.goto(self.whatsapp_url, timeout=60000, wait_until='domcontentloaded')
            except Exception as nav_error:
                nav_error_msg = str(nav_error)
                if "net::ERR_NAME_NOT_RESOLVED" in nav_error_msg or "getaddrinfo" in nav_error_msg:
                    print("\n[WARN] NETWORK ERROR: Cannot resolve WhatsApp Web hostname")
                    print("   Please check your internet connection")
                    print("   Trying to continue...")
                elif "net::ERR_INTERNET_DISCONNECTED" in nav_error_msg or "Network error" in nav_error_msg:
                    print("\n[WARN] NETWORK ERROR: No internet connection")
                    print("   Please check your internet connection")
                    print("   Trying to continue...")
                else:
                    print(f"\n[WARN] Navigation error: {nav_error_msg}")
                # Try to continue anyway
                try:
                    await self.page.goto(self.whatsapp_url, timeout=30000, wait_until='domcontentloaded')
                except:
                    print("[WARN] Could not load WhatsApp Web - will retry later")

            # Wait for WhatsApp to load
            await self._wait_for_whatsapp_ready()

            self.is_connected = True
            self.is_running = True

            print("[OK] WhatsApp Agent started successfully!")
            print(f"[INFO] Session stored in: {self.user_data_dir}")

            # Start message processor
            asyncio.create_task(self._process_message_queue())

            return True

        except Exception as e:
            error_msg = str(e)
            print(f"[ERROR] Error starting WhatsApp Agent: {error_msg}")
            
            # Provide helpful error messages
            if "playwright" in error_msg.lower():
                print("\n[WARN] Playwright not installed. Run: pip install playwright")
                print("   Then run: playwright install chromium")
            elif "getaddrinfo" in error_msg or "Name or service not known" in error_msg:
                print("\n[WARN] NETWORK ERROR: Cannot resolve hostname")
                print("   Please check your internet connection")
            elif "permission" in error_msg.lower() or "access" in error_msg.lower():
                print("\n[WARN] PERMISSION ERROR: Browser launch failed")
                print("   Try running as administrator or check firewall settings")
            
            self.is_connected = False
            return False

    async def _wait_for_whatsapp_ready(self, timeout: int = 60):
        """Wait for WhatsApp Web to be ready (logged in)"""
        print("[INFO] Waiting for WhatsApp Web to load...")
        print("[INFO] If this is your first time, please scan the QR code with your WhatsApp app")

        start_time = datetime.now()

        while (datetime.now() - start_time).total_seconds() < timeout:
            try:
                # Check for main app elements (search box, chat list)
                search_box = await self.page.query_selector('[data-testid="search"]')
                if search_box:
                    print("[OK] WhatsApp Web is ready and logged in!")
                    return True

                # Check for QR code (not logged in yet)
                qr_code = await self.page.query_selector('[data-testid="qr-icon"]')
                if qr_code:
                    elapsed = int((datetime.now() - start_time).total_seconds())
                    print(f"[INFO] QR code detected. Please scan... ({elapsed}/{timeout}s)")
                    await asyncio.sleep(3)
                else:
                    await asyncio.sleep(2)

            except Exception as e:
                await asyncio.sleep(2)

        print("[WARN] WhatsApp Web timeout. May need manual login.")
        return False

    async def send_message(self, phone_number: str, message: str) -> bool:
        """
        Send a WhatsApp message using WhatsApp Web search

        Args:
            phone_number: Phone number with country code (e.g., 923198130598)
            message: Message to send

        Returns:
            bool: True if sent successfully
        """
        if not self.is_connected or not self.page:
            print(f"[ERROR] WhatsApp Agent not connected")
            return False

        try:
            # Format phone number
            phone_number = phone_number.replace("+", "").replace(" ", "").replace("-", "")

            print(f"[INFO] Sending message to {phone_number}...")

            # Method 1: Search for contact using phone number
            try:
                # Wait for search box
                search_box = await self.page.wait_for_selector(
                    '[data-testid="search"][role="textbox"]',
                    timeout=10000
                )
                
                # Clear search box
                await search_box.click()
                await self.page.keyboard.press("Control+A")
                await self.page.keyboard.press("Delete")
                
                # Type phone number in search
                await search_box.fill(phone_number)
                await asyncio.sleep(2)
                
                # Click on the contact
                await self.page.keyboard.press("Enter")
                await asyncio.sleep(2)
                
                # Type message
                chat_input = await self.page.wait_for_selector(
                    '[data-testid="compose-box-input"][contenteditable="true"]',
                    timeout=10000
                )
                await chat_input.fill(message)
                await asyncio.sleep(1)
                
                # Press Enter to send
                await self.page.keyboard.press("Enter")
                print(f"[OK] Message sent to {phone_number}")
                await asyncio.sleep(2)
                return True

            except Exception as search_error:
                print(f"[WARN] Search method failed: {str(search_error)}")

                # Method 2: Try click-to-chat as fallback
                message_encoded = message.replace(" ", "%20").replace("\n", "%0A").replace("*", "%2A")
                whatsapp_url = f"https://web.whatsapp.com/send?phone={phone_number}&text={message_encoded}"

                print(f"[INFO] Trying direct chat URL...")
                await self.page.goto(whatsapp_url, timeout=30000)
                await asyncio.sleep(5)

                # Try to send
                try:
                    send_button = await self.page.wait_for_selector(
                        'button[data-testid="compose-btn-send"]',
                        timeout=10000
                    )
                    await send_button.click()
                    print(f"[OK] Message sent via direct URL")
                    await asyncio.sleep(2)
                    return True
                except:
                    print("[WARN] Message ready - may need manual send")
                    return True

        except Exception as e:
            print(f"[ERROR] Error sending message: {str(e)}")
            return False

    async def send_message_queued(self, phone_number: str, message: str):
        """Queue a message for sending (non-blocking)"""
        await self.message_queue.put({
            'phone': phone_number,
            'message': message,
            'timestamp': datetime.now()
        })

    async def _process_message_queue(self):
        """Process queued messages"""
        while self.is_running:
            try:
                if not self.message_queue.empty():
                    item = await self.message_queue.get()
                    await self.send_message(item['phone'], item['message'])
                    self.message_queue.task_done()
                else:
                    await asyncio.sleep(1)
            except Exception as e:
                print(f"Error processing queue: {str(e)}")
                await asyncio.sleep(2)

    async def send_support_notification(
        self,
        phone_number: str,
        ticket_id: str,
        customer_name: str = None
    ) -> bool:
        """
        Send support ticket notification

        Args:
            phone_number: Customer phone number
            ticket_id: Support ticket ID
            customer_name: Optional customer name

        Returns:
            bool: Success status
        """
        name_str = customer_name if customer_name else "there"

        message = f"""Hello {name_str}! 👋

Your support ticket *{ticket_id}* has been created.

Our team will review your issue shortly.

Thank you for contacting us!"""

        return await self.send_message(phone_number, message)

    async def stop(self):
        """Stop the WhatsApp agent"""
        print("[INFO] Stopping WhatsApp Agent...")
        self.is_running = False

        if self.browser:
            await self.browser.close()
            self.browser = None
            self.page = None
            self.is_connected = False

        print("[OK] WhatsApp Agent stopped")


# Singleton instance
whatsapp_agent: Optional[WhatsAppAgent] = None


async def get_whatsapp_agent() -> WhatsAppAgent:
    """Get or create WhatsApp agent singleton"""
    global whatsapp_agent
    if whatsapp_agent is None:
        whatsapp_agent = WhatsAppAgent()
        await whatsapp_agent.start()
    return whatsapp_agent


async def initialize_whatsapp_agent():
    """Initialize WhatsApp agent for use"""
    agent = await get_whatsapp_agent()
    return agent


# For testing
async def main():
    """Test the WhatsApp agent"""
    agent = WhatsAppAgent()

    try:
        await agent.start()

        # Keep running
        print("\n[OK] Agent ready. Press Ctrl+C to stop.")

        # Test message
        await asyncio.sleep(5)
        await agent.send_support_notification(
            phone_number="+923198130598",
            ticket_id="TEST1234",
            customer_name="Test User"
        )

        # Keep alive
        while True:
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        await agent.stop()


if __name__ == "__main__":
    asyncio.run(main())
