#!/usr/bin/env python
"""Test all imports and config"""
import sys
import os

print("=" * 50)
print("Testing Backend Configuration")
print("=" * 50)
print()

try:
    print("1. Testing config import...")
    from config import settings, get_cors_origins
    print("   ✓ Config imported successfully")
    print(f"   - Database URL: {settings.database_url[:50]}...")
    print(f"   - Gemini Model: {settings.gemini_model}")
    print(f"   - CORS Origins: {get_cors_origins()}")
    print()
except Exception as e:
    print(f"   ✗ Config Error: {e}")
    print()

try:
    print("2. Testing database import...")
    from database import Base, engine, async_session_maker
    print("   ✓ Database imported successfully")
    print()
except Exception as e:
    print(f"   ✗ Database Error: {e}")
    print()

try:
    print("3. Testing models import...")
    from models import Customer, Conversation, Message, ChannelType
    print("   ✓ Models imported successfully")
    print()
except Exception as e:
    print(f"   ✗ Models Error: {e}")
    print()

try:
    print("4. Testing services import...")
    from services.ai_service import ai_service
    from services.customer_service import customer_service
    from services.conversation_service import conversation_service
    from services.message_service import message_service
    print("   ✓ Services imported successfully")
    print()
except Exception as e:
    print(f"   ✗ Services Error: {e}")
    print()

try:
    print("5. Testing routes import...")
    from routes.webform import router
    print("   ✓ Routes imported successfully")
    print()
except Exception as e:
    print(f"   ✗ Routes Error: {e}")
    print()

try:
    print("6. Testing main app import...")
    from main import app
    print("   ✓ Main app imported successfully")
    print()
except Exception as e:
    print(f"   ✗ Main App Error: {e}")
    print()

print("=" * 50)
print("Testing Complete!")
print("=" * 50)
