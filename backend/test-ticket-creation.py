"""
Quick Test Script - Test ticket creation without WhatsApp blocking
"""
import asyncio
import sys
import os
import time

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.ext.asyncio import AsyncSession
from database import async_session_maker
from models import Customer, Conversation, Message, ChannelType, SenderType
from services.customer_service import customer_service
from services.conversation_service import conversation_service
from services.message_service import message_service
from services.ai_service import ai_service


async def test_ticket_creation():
    """Test complete ticket creation flow"""
    
    print("=" * 60)
    print("Testing Ticket Creation Flow")
    print("=" * 60)
    
    start_time = time.time()
    
    try:
        # Test 1: Create/Get Customer
        print("\n[1/5] Creating customer...")
        customer = await customer_service.get_or_create_customer(
            email="test@example.com",
            name="Test User"
        )
        print(f"✅ Customer: {customer.customer_id}")
        
        # Test 2: Create/Get Conversation
        print("\n[2/5] Creating conversation...")
        conversation = await conversation_service.get_or_create_conversation(
            customer_id=customer.customer_id,
            channel=ChannelType.webform
        )
        print(f"✅ Conversation: {conversation.conversation_id}")
        
        # Test 3: Save customer message
        print("\n[3/5] Saving customer message...")
        customer_message = await message_service.create_message(
            conversation_id=conversation.conversation_id,
            content="How does the agent handle multi-channel queries?",
            sender_type=SenderType.customer,
            sender_identifier="test@example.com"
        )
        print(f"✅ Message saved: {customer_message.message_id}")
        
        # Test 4: Generate AI response (this is the slow part)
        print("\n[4/5] Generating AI response...")
        ai_start = time.time()
        ai_response = await ai_service.generate_response(
            customer_message="How does the agent handle multi-channel queries?",
            category="General",
            channel="webform"
        )
        ai_latency = time.time() - ai_start
        print(f"✅ AI Response generated in {ai_latency:.2f}s")
        print(f"   Response preview: {ai_response['response'][:100]}...")
        print(f"   Priority: {ai_response.get('priority', 'normal')}")
        print(f"   Escalation: {ai_response.get('escalation_required', False)}")
        
        # Test 5: Save AI response
        print("\n[5/5] Saving AI response...")
        ai_message = await message_service.create_message(
            conversation_id=conversation.conversation_id,
            content=ai_response["response"],
            sender_type=SenderType.agent,
            sender_identifier="AI Agent",
            sentiment_score=ai_response["sentiment_score"],
            escalation_required=ai_response["escalation_required"],
            processed_latency_ms=int(ai_latency * 1000),
            priority=ai_response.get("priority", "normal"),
            urgency_keywords=",".join(ai_response.get("urgency_keywords", [])) if ai_response.get("urgency_keywords") else None
        )
        print(f"✅ AI Response saved: {ai_message.message_id}")
        
        total_time = time.time() - start_time
        
        print("\n" + "=" * 60)
        print(f"✅ TEST PASSED!")
        print(f"   Total time: {total_time:.2f}s")
        print(f"   Ticket ID: {str(conversation.conversation_id)[:8].upper()}")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"❌ TEST FAILED!")
        print(f"   Error: {str(e)}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_ticket_creation())
    sys.exit(0 if success else 1)
