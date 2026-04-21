#!/usr/bin/env python
"""Test backend configuration"""
from config import settings

print("Database URL:", settings.database_url[:50] + "...")
print("Gemini Model:", settings.gemini_model)
print("Debug Mode:", settings.debug)
print("\nConfiguration loaded successfully!")
