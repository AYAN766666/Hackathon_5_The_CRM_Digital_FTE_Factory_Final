"""
Test Delete Ticket API
"""
import asyncio
import aiohttp

async def test_delete():
    base_url = "http://localhost:8000"
    
    print("=" * 50)
    print("Testing Delete Ticket API")
    print("=" * 50)
    
    # First, check if we can get ticket status
    ticket_id = input("\nEnter a ticket ID to test delete (e.g., ABC12345): ").strip()
    
    if not ticket_id:
        print("❌ No ticket ID provided")
        return
    
    async with aiohttp.ClientSession() as session:
        # Step 1: Check if ticket exists
        print(f"\n📋 Step 1: Checking if ticket {ticket_id} exists...")
        try:
            async with session.get(f"{base_url}/support/ticket/{ticket_id}") as resp:
                if resp.status == 404:
                    print(f"❌ Ticket {ticket_id} not found. Please create a ticket first.")
                    return
                ticket_data = await resp.json()
                print(f"✅ Ticket found!")
                print(f"   Status: {ticket_data.get('status')}")
                print(f"   Messages: {len(ticket_data.get('messages', []))}")
        except Exception as e:
            print(f"❌ Error checking ticket: {e}")
            return
        
        # Step 2: Ask for confirmation
        confirm = input(f"\n⚠️  Are you sure you want to DELETE ticket {ticket_id}? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("❌ Delete cancelled")
            return
        
        # Step 3: Delete ticket
        print(f"\n🗑️  Step 2: Deleting ticket {ticket_id}...")
        try:
            async with session.delete(f"{base_url}/support/ticket/{ticket_id}") as resp:
                result = await resp.json()
                if resp.status == 200:
                    print(f"✅ Delete successful!")
                    print(f"   Message: {result.get('message')}")
                else:
                    print(f"❌ Delete failed: {result}")
                    return
        except Exception as e:
            print(f"❌ Error deleting ticket: {e}")
            return
        
        # Step 4: Verify deletion
        print(f"\n🔍 Step 3: Verifying deletion...")
        try:
            async with session.get(f"{base_url}/support/ticket/{ticket_id}") as resp:
                if resp.status == 404:
                    print(f"✅ VERIFIED: Ticket {ticket_id} has been deleted from database!")
                else:
                    print(f"❌ WARNING: Ticket still exists! Deletion may not have worked.")
        except Exception as e:
            print(f"Error verifying: {e}")
    
    print("\n" + "=" * 50)
    print("Test Complete!")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(test_delete())
