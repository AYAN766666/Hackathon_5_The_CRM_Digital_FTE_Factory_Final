#!/usr/bin/env python
"""Test ticket lookup only"""
import asyncio
import sys
sys.path.insert(0, '.')

print("=" * 50)
print("Testing Ticket Lookup")
print("=" * 50)
print()

async def test():
    from services.conversation_service import conversation_service
    
    # Test 1: Get all conversations
    print("[1/2] Getting all conversations from database...")
    from sqlalchemy.ext.asyncio import async_sessionmaker
    from sqlalchemy import select
    from models import Conversation
    
    from database import async_session_maker
    
    async with async_session_maker() as session:
        result = await session.execute(
            select(Conversation).order_by(Conversation.started_at.desc())
        )
        conversations = result.scalars().all()
        
        if conversations:
            print(f"   ✓ Found {len(conversations)} conversations")
            print()
            
            # Show first conversation
            conv = conversations[0]
            ticket_id = str(conv.conversation_id)[:8].upper()
            print(f"   Latest Ticket ID: {ticket_id}")
            print(f"   - Full UUID: {conv.conversation_id}")
            print(f"   - Status: {conv.status.value}")
            print(f"   - Channel: {conv.channel.value}")
            print()
            
            # Test 2: Lookup by short ID
            print(f"[2/2] Looking up ticket by short ID: {ticket_id}...")
            found_conv = await conversation_service.get_conversation_by_short_id(ticket_id)
            
            if found_conv:
                print(f"   ✓ Ticket FOUND!")
                print(f"   - Ticket ID: {str(found_conv.conversation_id)[:8].upper()}")
                print(f"   - Status: {found_conv.status.value}")
                print()
                print("=" * 50)
                print("✅ TICKET LOOKUP WORKING!")
                print("=" * 50)
            else:
                print(f"   ✗ Ticket NOT FOUND!")
        else:
            print("   No conversations in database yet.")
            print("   Create a ticket first using POST /support/submit")

asyncio.run(test())
