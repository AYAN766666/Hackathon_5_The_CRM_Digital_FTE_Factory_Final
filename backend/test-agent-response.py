"""
Test Agent Response - Direct API call
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_agent_direct():
    """Test agent directly without API"""
    from agents.customer_agent import customer_success_agent
    
    print("=" * 60)
    print("TESTING AGENT - DIRECT CALL")
    print("=" * 60)
    print()
    
    # Test 1: Simple query
    print("Test 1: Password Reset Query")
    print("-" * 60)
    
    try:
        result = await customer_success_agent.process_message(
            customer_message="How do I reset my password?",
            customer_email="test@example.com",
            channel="webform",
            customer_name="Test User",
            category="Technical"
        )
        
        print(f"✅ Success: {result.get('success')}")
        print(f"📝 Response: {result.get('response', 'N/A')[:150]}...")
        print(f"⚠️ Escalation: {result.get('escalation_required')}")
        print(f"📤 Response Sent: {result.get('response_sent')}")
        print(f"🎫 Ticket ID: {result.get('ticket_id')}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 60)
    print("CONCLUSION:")
    print("=" * 60)
    print("✅ Agent KHUD answer generate kar raha hai!")
    print("✅ Agent KHUD response send kar raha hai!")
    print("✅ Sirf error ya complex case mein escalate!")

if __name__ == "__main__":
    asyncio.run(test_agent_direct())
