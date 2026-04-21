"""
Test Groq AI Service - FREE Alternative
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_groq_ai():
    """Test Groq AI service"""
    print("="*60)
    print("TESTING GROQ AI SERVICE (FREE)")
    print("="*60)
    print()
    
    try:
        from services.groq_ai_service import groq_ai_service
        
        if not groq_ai_service:
            print("❌ Groq not available. Install: pip install groq")
            return
        
        print("Testing: 'How do I reset my password?'")
        print("-"*60)
        
        response = await groq_ai_service.generate_response(
            customer_message="How do I reset my password?",
            category="Technical",
            channel="webform"
        )
        
        print(f"✅ Response: {response['response'][:150]}...")
        print(f"✅ Escalation: {response['escalation_required']}")
        print(f"✅ Sentiment: {response['sentiment_score']}")
        print(f"✅ Confidence: {response['confidence']}")
        print(f"✅ KB Articles: {response['kb_articles_used']}")
        print()
        print("="*60)
        print("✅ GROQ AI SERVICE WORKING!")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print()
        print("Setup Instructions:")
        print("1. pip install groq")
        print("2. Get API key: https://console.groq.com/keys")
        print("3. Add to .env: GROQ_API_KEY=gsk_xxxxx")
        print("4. Add to .env: GROQ_MODEL=llama-3.1-70b-versatile")

if __name__ == "__main__":
    asyncio.run(test_groq_ai())
