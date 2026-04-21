"""
Complete Flow Test - Check AI + Email + WhatsApp
"""
import asyncio
import sys
import os
import httpx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_complete_flow():
    """Test complete support flow"""
    print("="*70)
    print("COMPLETE FLOW TEST - AI + EMAIL + WHATSAPP")
    print("="*70)
    print()
    
    # Test data
    test_data = {
        "name": "Hackathon Test",
        "email": "aayanu52@gmail.com",
        "phone": "+923198130598",
        "category": "Technical",
        "message": "I cannot login to my account. Please help me reset my password."
    }
    
    print("📝 Test Data:")
    print(f"   Name: {test_data['name']}")
    print(f"   Email: {test_data['email']}")
    print(f"   Phone: {test_data['phone']}")
    print(f"   Message: {test_data['message'][:50]}...")
    print()
    
    try:
        # Step 1: Submit support request
        print("Step 1: Submitting support request...")
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "http://localhost:8000/support/submit",
                json=test_data
            )
            
            if response.status_code == 200:
                result = response.json()
                ticket_id = result.get('ticket_id')
                print(f"✅ Ticket Created: {ticket_id}")
                print(f"   Status: {result.get('status')}")
                print()
                
                # Step 2: Get ticket status (check AI response)
                print("Step 2: Checking AI response...")
                ticket_response = await client.get(f"http://localhost:8000/support/ticket/{ticket_id}")
                
                if ticket_response.status_code == 200:
                    ticket_data = ticket_response.json()
                    messages = ticket_data.get('messages', [])
                    
                    print(f"   Total Messages: {len(messages)}")
                    print()
                    
                    for msg in messages:
                        sender = msg['sender']
                        content = msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content']
                        
                        if sender == 'customer':
                            print(f"👤 Customer: {content}")
                        elif sender == 'agent':
                            print(f"🤖 AI Agent: {content}")
                            print(f"   Sentiment: {msg.get('sentiment_score', 'N/A')}")
                        print()
                    
                    # Step 3: Check email
                    print("Step 3: Email Status")
                    print(f"   📧 Email should be sent to: {test_data['email']}")
                    print(f"   📱 WhatsApp should be sent to: {test_data['phone']}")
                    print()
                    
                    print("="*70)
                    print("✅ TEST COMPLETE!")
                    print("="*70)
                    print()
                    print("CHECK YOUR:")
                    print(f"   1. Gmail Inbox: {test_data['email']}")
                    print(f"   2. WhatsApp: {test_data['phone']}")
                    print()
                    
                    return True
                else:
                    print(f"❌ Failed to get ticket: {ticket_response.status_code}")
                    return False
            else:
                print(f"❌ Failed to submit: {response.status_code}")
                print(f"   Error: {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Starting Complete Flow Test...\n")
    success = asyncio.run(test_complete_flow())
    sys.exit(0 if success else 1)
