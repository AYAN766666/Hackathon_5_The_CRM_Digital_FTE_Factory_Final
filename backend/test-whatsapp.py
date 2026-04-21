"""
Test WhatsApp Agent
Quick test script to verify WhatsApp integration
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from services.whatsapp_agent import WhatsAppAgent


async def test_whatsapp():
    """Test WhatsApp agent"""
    print("=" * 50)
    print("  WhatsApp Agent Test")
    print("=" * 50)
    print()

    agent = WhatsAppAgent()

    try:
        # Start agent
        print("🚀 Starting WhatsApp Agent...")
        success = await agent.start()

        if not success:
            print("❌ Failed to start agent")
            return

        print("\n✅ Agent started successfully!")
        print("\n📱 Sending test message...")

        # Send test message
        await agent.send_support_notification(
            phone_number="+923198130598",
            ticket_id="TEST1234",
            customer_name="Test User"
        )

        print("\n✅ Test message sent!")
        print("\n💡 Keep this running to maintain session")
        print("   Press Ctrl+C to stop\n")

        # Keep alive
        while True:
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        print("\n\n🛑 Stopping agent...")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
    finally:
        await agent.stop()


if __name__ == "__main__":
    asyncio.run(test_whatsapp())
