#!/usr/bin/env python
"""
Start Backend Server
Direct Python script to start uvicorn server
"""
import uvicorn
import os

# Get current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

print("=" * 50)
print("Customer Success FTE - Backend Server")
print("=" * 50)
print()
print(f"Starting server from: {current_dir}")
print()
print("Backend will be available at: http://localhost:8000")
print("API Docs at: http://localhost:8000/docs")
print()
print("Press Ctrl+C to stop the server")
print("=" * 50)
print()

# Start server
uvicorn.run(
    "main:app",
    host="0.0.0.0",
    port=8000,
    reload=True
)
