"""
Auto Test Delete - Creates a ticket then deletes it
"""
import asyncio
import aiohttp

async def test_full_flow():
    base_url = "http://localhost:8000"
    
    print("=" * 60)
    print("Testing Full Delete Flow: Create → Verify → Delete → Confirm")
    print("=" * 60)
    
    async with aiohttp.ClientSession() as session:
        # Step 1: Create a ticket
        print("\n📝 Step 1: Creating a test ticket...")
        create_data = {
            "name": "Test User",
            "email": "test_delete@example.com",
            "category": "General",
            "message": "This is a test ticket to verify delete functionality works properly."
        }
        
        try:
            async with session.post(f"{base_url}/support/submit", json=create_data) as resp:
                result = await resp.json()
                if resp.status == 200:
                    ticket_id = result.get('ticket_id')
                    print(f"✅ Ticket created: {ticket_id}")
                else:
                    print(f"❌ Failed to create ticket: {result}")
                    return
        except Exception as e:
            print(f"❌ Error creating ticket: {e}")
            return
        
        # Step 2: Verify ticket exists
        print(f"\n🔍 Step 2: Verifying ticket {ticket_id} exists...")
        try:
            async with session.get(f"{base_url}/support/ticket/{ticket_id}") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    msg_count = len(data.get('messages', []))
                    print(f"✅ Ticket verified! Messages: {msg_count}")
                else:
                    print(f"❌ Ticket not found!")
                    return
        except Exception as e:
            print(f"❌ Error: {e}")
            return
        
        # Step 3: Delete the ticket
        print(f"\n🗑️  Step 3: Deleting ticket {ticket_id}...")
        try:
            async with session.delete(f"{base_url}/support/ticket/{ticket_id}") as resp:
                result = await resp.json()
                if resp.status == 200:
                    print(f"✅ Delete API returned: {result.get('message')}")
                else:
                    print(f"❌ Delete failed: {result}")
                    return
        except Exception as e:
            print(f"❌ Error deleting: {e}")
            return
        
        # Step 4: Verify deletion
        print(f"\n✅ Step 4: Verifying ticket is deleted from database...")
        try:
            async with session.get(f"{base_url}/support/ticket/{ticket_id}") as resp:
                if resp.status == 404:
                    print(f"✅ SUCCESS! Ticket {ticket_id} is completely deleted from database!")
                    print("\n" + "=" * 60)
                    print("🎉 DELETE FUNCTIONALITY IS WORKING PERFECTLY!")
                    print("=" * 60)
                else:
                    print(f"⚠️  WARNING: Ticket still exists! Status: {resp.status}")
                    print("\nThere might be an issue with the delete operation.")
        except Exception as e:
            print(f"❌ Error verifying: {e}")
    
    print("\nTest complete!")

if __name__ == "__main__":
    asyncio.run(test_full_flow())
