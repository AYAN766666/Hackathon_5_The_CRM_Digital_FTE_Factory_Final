"""
Test Ollama AI - Complete Integration Test
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_ollama():
    """Test Ollama AI integration"""
    print("="*60)
    print("🚀 OLLAMA AI - INTEGRATION TEST")
    print("="*60)
    print()
    
    # Step 1: Check if Ollama is installed
    print("Step 1: Checking Ollama installation...")
    print("-"*60)
    
    try:
        import ollama
        print("✅ Ollama Python library installed")
    except ImportError:
        print("❌ Ollama not installed. Run: pip install ollama")
        return
    
    # Check if Ollama server is running
    print("-"*60)
    print("Step 2: Checking Ollama server...")
    print("-"*60)
    
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama server running on http://localhost:11434")
            models = response.json().get('models', [])
            print(f"✅ Available models: {len(models)}")
            for model in models:
                print(f"   - {model.get('name', 'unknown')}")
        else:
            print("❌ Ollama server not responding")
            print()
            print("INSTALL OLLAMA:")
            print("1. Download: https://ollama.com/download")
            print("2. Install karo")
            print("3. Run: ollama run llama3.2")
            return
    except Exception as e:
        print("❌ Ollama server not running")
        print()
        print("INSTALL OLLAMA:")
        print("1. Download: https://ollama.com/download")
        print("2. Install karo")
        print("3. Run: ollama run llama3.2")
        return
    
    # Step 3: Test Ollama AI Service
    print()
    print("-"*60)
    print("Step 3: Testing Ollama AI Service...")
    print("-"*60)
    
    try:
        from services.ollama_ai_service import ollama_ai_service
        
        if not ollama_ai_service:
            print("❌ Ollama AI service not initialized")
            return
        
        print("✅ Ollama AI service initialized")
        
        # Test response generation
        print()
        print("Testing: 'How do I reset my password?'")
        print("-"*60)
        
        response = await ollama_ai_service.generate_response(
            customer_message="How do I reset my password?",
            category="Technical",
            channel="webform"
        )
        
        print(f"✅ Response: {response['response'][:200]}...")
        print(f"✅ Confidence: {response['confidence']}")
        print(f"✅ Escalation: {response['escalation_required']}")
        print(f"✅ Sentiment: {response['sentiment_score']}")
        print(f"✅ KB Articles: {response['kb_articles_used']}")
        
        print()
        print("="*60)
        print("🎉 OLLAMA AI - WORKING PERFECTLY!")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_ollama())
