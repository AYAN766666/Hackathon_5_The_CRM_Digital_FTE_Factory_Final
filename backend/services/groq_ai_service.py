"""
Groq AI Service - FREE Alternative to Gemini
Uses Groq Cloud API with Llama 3 models
"""
import os
import sys
import json
from typing import Optional, Dict, Any, List
from datetime import datetime

# Add parent path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    print("⚠️ Groq not installed. Run: pip install groq")

from config import settings


class GroqAIService:
    """AI Service using Groq Cloud API (FREE)"""

    def __init__(self):
        """Initialize Groq client"""
        if not GROQ_AVAILABLE:
            raise ImportError("Groq library not installed. Run: pip install groq")
        
        # Get API key from environment or settings
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            from config import settings
            api_key = settings.groq_api_key
        
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment or .env file")
        
        self.client = Groq(api_key=api_key)

        # Get model from environment or use default (llama-3.1-70b-versatile is decommissioned)
        self.model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
        
        # System prompt for AI agent
        self.system_prompt = """You are a helpful customer support assistant for a multi-channel support system.

Your responsibilities:
1. Understand customer messages and identify their intent
2. Search the knowledge base for relevant information
3. Generate helpful, accurate responses based on knowledge base
4. Detect when escalation to human support is needed
5. Determine sentiment (positive, neutral, negative)

Escalation criteria (mark escalation_required = true):
- Customer expresses anger or frustration
- Legal threats or complaints
- Refund requests that require manual approval
- Complex technical issues beyond basic troubleshooting
- Requests for human agent explicitly

Response format:
Always respond in JSON format with these fields:
{
    "response": "your helpful response to the customer",
    "escalation_required": false,
    "sentiment_score": 0.5,
    "category": "Technical|Billing|General|Feedback|Bug Report",
    "confidence": 0.9,
    "kb_articles_used": ["article1", "article2"]
}

Be friendly, professional, and concise. Aim to resolve issues on first contact.

Channel-specific tone:
- Email: Formal and detailed
- WhatsApp: Short friendly reply with emojis
- Webform: Professional but conversational"""

    def search_knowledge_base(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Search knowledge base for relevant articles"""
        from services.knowledge_base_service import knowledge_base
        return knowledge_base.search(query, top_k)

    def _build_kb_context(self, kb_results: List[Dict[str, Any]]) -> str:
        """Build context string from knowledge base results"""
        if not kb_results:
            return ""
        
        context_parts = []
        for result in kb_results:
            doc_name = result.get('document', 'Unknown')
            excerpt = result.get('excerpt', '')
            score = result.get('score', 0)
            
            if score > 5:  # Only include high-relevance results
                context_parts.append(f"""
From {doc_name}:
{excerpt}
""")
        
        if context_parts:
            return "\n--- RELEVANT DOCUMENTATION ---\n" + "\n".join(context_parts) + "\n--- END DOCUMENTATION ---\n"
        
        return ""

    async def generate_response(
        self,
        customer_message: str,
        conversation_context: Optional[str] = None,
        category: Optional[str] = None,
        channel: str = "webform"
    ) -> Dict[str, Any]:
        """
        Generate AI response using Groq (FREE)

        Args:
            customer_message: The customer's message
            conversation_context: Previous messages in conversation (optional)
            category: Support category if known
            channel: Communication channel (email/whatsapp/webform)

        Returns:
            Dictionary with response, escalation flag, sentiment, etc.
        """
        try:
            # Step 1: Search knowledge base
            kb_results = self.search_knowledge_base(customer_message, top_k=3)
            kb_context = self._build_kb_context(kb_results)
            
            # Step 2: Build context-aware prompt
            context_text = ""
            if conversation_context:
                context_text = f"\n\nPrevious conversation:\n{conversation_context}"
            
            # Add channel-specific instructions
            channel_instruction = ""
            if channel == "email":
                channel_instruction = "Use formal, detailed language appropriate for email."
            elif channel == "whatsapp":
                channel_instruction = "Use short, friendly language with emojis. Keep it conversational."
            else:
                channel_instruction = "Use professional but conversational language."

            user_prompt = f"""Customer message: {customer_message}{context_text}
{kb_context}
Category: {category or 'Unknown'}
Channel: {channel}

{channel_instruction}

Generate a helpful response based on the documentation provided above. If the documentation doesn't contain relevant information, use your general knowledge but note this in the response.

Respond in JSON format only."""

            # Step 3: Call Groq API (FREE & FAST)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=600,
                response_format={"type": "json_object"}
            )

            # Step 4: Parse response
            ai_response = response.choices[0].message.content
            result = json.loads(ai_response)

            # Get KB article names used
            kb_articles = result.get("kb_articles_used", [])
            if not kb_articles and kb_results:
                kb_articles = [r.get('document', '') for r in kb_results if r.get('score', 0) > 5]

            # Ensure all required fields exist
            return {
                "response": result.get("response", "Thank you for contacting us. We're looking into your request."),
                "escalation_required": result.get("escalation_required", False),
                "sentiment_score": result.get("sentiment_score", 0.5),
                "category": result.get("category", category or "General"),
                "confidence": result.get("confidence", 0.8),
                "kb_articles_used": kb_articles
            }

        except Exception as e:
            # Fallback response on error
            print(f"Groq AI Service Error: {str(e)}")
            return {
                "response": "Thank you for contacting us. Your request has been received and will be reviewed by our team.",
                "escalation_required": True,
                "sentiment_score": 0.5,
                "category": category or "General",
                "confidence": 0.0,
                "error": str(e)
            }


# Global Groq AI service instance
groq_ai_service = GroqAIService() if GROQ_AVAILABLE else None
