#!/usr/bin/env python
"""Test ticket status API"""
import httpx
import json

BASE_URL = "http://localhost:8000"

print("=" * 50)
print("Testing Ticket Status API")
print("=" * 50)
print()

# Test 1: Create a ticket
print("[1/3] Creating new ticket...")
payload = {
    "name": "Test User",
    "email": "test@example.com",
    "category": "Technical",
    "message": "Testing the ticket status API fix. This message has enough characters to pass validation."
}

with httpx.Client() as client:
    response = client.post(f"{BASE_URL}/support/submit", json=payload)
    
    if response.status_code == 200:
        result = response.json()
        ticket_id = result["ticket_id"]
        print(f"   ✓ Ticket created: {ticket_id}")
        print(f"   Status: {result['status']}")
        print()
        
        # Test 2: Get ticket status
        print(f"[2/3] Getting ticket status for: {ticket_id}...")
        status_response = client.get(f"{BASE_URL}/support/ticket/{ticket_id}")
        
        if status_response.status_code == 200:
            status_data = status_response.json()
            print(f"   ✓ Ticket found!")
            print(f"   - Ticket ID: {status_data['ticket_id']}")
            print(f"   - Status: {status_data['status']}")
            print(f"   - Channel: {status_data['channel']}")
            print(f"   - Messages: {len(status_data['messages'])}")
            print()
            
            # Test 3: Display conversation
            print("[3/3] Conversation History:")
            print("   " + "-" * 46)
            for msg in status_data['messages']:
                sender = msg['sender'].upper()
                print(f"   [{sender}]: {msg['content'][:50]}...")
            print("   " + "-" * 46)
            print()
            
            print("=" * 50)
            print("✅ ALL TESTS PASSED!")
            print("=" * 50)
        else:
            print(f"   ✗ Error: {status_response.status_code}")
            print(f"   Response: {status_response.text}")
    else:
        print(f"   ✗ Error creating ticket: {response.status_code}")
        print(f"   Response: {response.text}")
