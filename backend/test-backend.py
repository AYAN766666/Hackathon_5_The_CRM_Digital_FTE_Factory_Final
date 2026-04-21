"""
Test Backend API Endpoints
"""
import asyncio
import httpx

async def test_api():
    base_url = "http://localhost:8000"
    
    print("=" * 60)
    print("Testing Backend API Endpoints")
    print("=" * 60)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Test 1: Root endpoint
        print("\n1. Testing GET /")
        try:
            response = await client.get(f"{base_url}/")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
        except Exception as e:
            print(f"   ERROR: {str(e)}")
        
        # Test 2: Health endpoint
        print("\n2. Testing GET /health")
        try:
            response = await client.get(f"{base_url}/health")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}")
        except Exception as e:
            print(f"   ERROR: {str(e)}")
        
        # Test 3: Submit support request
        print("\n3. Testing POST /support/submit")
        try:
            payload = {
                "name": "Test User",
                "email": "test@example.com",
                "category": "General",
                "message": "This is a test message to verify the backend API works correctly"
            }
            response = await client.post(
                f"{base_url}/support/submit",
                json=payload
            )
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   Ticket ID: {data.get('ticket_id')}")
                print(f"   Status: {data.get('status')}")
                print(f"   Message: {data.get('message')}")
            else:
                print(f"   Response: {response.text}")
        except Exception as e:
            print(f"   ERROR: {str(e)}")
        
        # Test 4: Get ticket status (will use a dummy ID)
        print("\n4. Testing GET /support/ticket/TEST123")
        try:
            response = await client.get(f"{base_url}/support/ticket/TEST123")
            print(f"   Status: {response.status_code}")
            if response.status_code == 404:
                print(f"   Expected 404 - Ticket not found (this is OK)")
            else:
                print(f"   Response: {response.json()}")
        except Exception as e:
            print(f"   ERROR: {str(e)}")
        
        # Test 5: WhatsApp endpoints
        print("\n5. Testing GET /whatsapp/qr")
        try:
            response = await client.get(f"{base_url}/whatsapp/qr")
            print(f"   Status: {response.status_code}")
            print(f"   Response available: {len(response.content) > 0}")
        except Exception as e:
            print(f"   ERROR: {str(e)}")
        
        print("\n" + "=" * 60)
        print("Test Complete!")
        print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_api())
