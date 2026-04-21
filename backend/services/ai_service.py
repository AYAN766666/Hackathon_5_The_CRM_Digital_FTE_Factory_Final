"""
AI Service - Groq Integration (100% FREE CLOUD)
Uses Groq Cloud API with Llama 3 models - FAST & FREE!
"""
import os
import asyncio
from typing import Optional, Dict, Any, List
from datetime import datetime
import json
import sys

# Add parent path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    print("[WARN] Groq not installed. Run: pip install groq")

from config import settings
from services.knowledge_base_service import knowledge_base


class AIService:
    """AI Service for customer support automation using Groq (100% FREE CLOUD)"""

    def __init__(self):
        """Initialize AI client with Groq configuration - FREE API KEY!"""
        if not GROQ_AVAILABLE:
            print("[WARN] Groq library not available. Install: pip install groq")

        # Get API key from environment
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            api_key = settings.groq_api_key

        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment or .env file")

        # Initialize Groq client with timeout configuration
        self.client = Groq(
            api_key=api_key,
            timeout=15.0  # 15 second timeout for API calls
        )
        self.model = settings.groq_model if hasattr(settings, 'groq_model') else 'llama-3.1-8b-instant'

        # System prompt for AI agent - simplified for better focus
        self.system_prompt = """You are a helpful customer support assistant.

Your job:
1. Understand the customer's question
2. Provide a direct, helpful answer
3. Detect if escalation is needed (angry customer, legal threats, complex issues)
4. Identify sentiment (positive, neutral, negative)

Always respond in JSON format with:
{
    "response": "your helpful response",
    "escalation_required": false,
    "sentiment_score": 0.5,
    "category": "Technical|Billing|General|Feedback|Bug Report",
    "confidence": 0.9
}

Be friendly, professional, and concise."""

    def search_knowledge_base(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Search knowledge base for relevant articles
        
        Args:
            query: Search query
            top_k: Number of results
            
        Returns:
            List of relevant articles with scores
        """
        return knowledge_base.search(query, top_k)

    def _build_kb_context(self, kb_results: List[Dict[str, Any]]) -> str:
        """Build context string from knowledge base results
        
        Args:
            kb_results: List of knowledge base search results
            
        Returns:
            Formatted context string
        """
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
        Generate AI response using Groq (100% FREE CLOUD)

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

            # Build a clear, focused prompt that directly addresses the customer's message
            user_prompt = f"""You are helping a customer with their question.

CUSTOMER'S MESSAGE:
{customer_message}

{context_text}

RELEVANT DOCUMENTATION:
{kb_context if kb_context else "No specific documentation found. Use your general knowledge to help the customer."}

SUPPORT CATEGORY: {category or 'Unknown'}
CHANNEL: {channel}

{channel_instruction}

IMPORTANT: 
- Directly answer the customer's question
- Be helpful, friendly, and professional
- Use the documentation above to provide accurate information
- If you don't have specific information, provide a general helpful response

Respond in JSON format with this exact structure:
{{
    "response": "Your direct answer to the customer's question",
    "escalation_required": false,
    "sentiment_score": 0.5,
    "category": "Technical or Billing or General or Feedback or Bug Report",
    "confidence": 0.9,
    "kb_articles_used": ["article1", "article2"]
}}"""

            # Step 3: Call Groq API (FREE & FAST)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful customer support assistant. Always respond in valid JSON format."},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=600,
                response_format={"type": "json_object"}
            )

            # Step 4: Parse response
            ai_response_text = response.choices[0].message.content

            # Extract JSON from response
            try:
                # Find JSON in response
                start_idx = ai_response_text.find('{')
                end_idx = ai_response_text.rfind('}') + 1
                if start_idx >= 0 and end_idx > start_idx:
                    json_str = ai_response_text[start_idx:end_idx]
                    result = json.loads(json_str)
                else:
                    result = json.loads(ai_response_text)

                # Add priority detection (NEW HACKATHON FEATURE)
                result['priority'] = self._detect_priority(customer_message, result)
                result['urgency_keywords'] = self._extract_urgency_keywords(customer_message)
            except:
                # Fallback parsing
                result = {
                    "response": ai_response_text,
                    "escalation_required": False,
                    "sentiment_score": 0.5,
                    "category": category or "General",
                    "confidence": 0.8
                }

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

    async def classify_message(self, message: str) -> Dict[str, Any]:
        """
        Classify support message to determine category and priority

        Args:
            message: Customer message

        Returns:
            Classification results
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Classify support messages. Return JSON: {category, priority, keywords}"},
                    {"role": "user", "content": f"Classify this message: {message}"}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )

            result = json.loads(response.choices[0].message.content)
            return result

        except Exception as e:
            print(f"Classification Error: {str(e)}")
            return {
                "category": "General",
                "priority": "normal",
                "keywords": []
            }

    def _detect_priority(self, message: str, ai_response: dict) -> str:
        """
        Detect ticket priority based on message content and AI response
        
        Args:
            message: Customer message
            ai_response: Parsed AI response
            
        Returns:
            Priority level: 'critical', 'high', 'normal', or 'low'
        """
        message_lower = message.lower()
        
        # Critical keywords - immediate attention needed
        critical_keywords = [
            'urgent', 'emergency', 'critical', 'down', 'outage', 'broken',
            'lost money', 'data lost', 'security breach', 'hack', 'fraud',
            'lawsuit', 'legal', 'sue', 'court', 'lawyer', 'attorney'
        ]
        
        # High priority keywords
        high_keywords = [
            'asap', 'immediately', 'right now', 'today', 'important',
            'complaint', 'angry', 'frustrated', 'unacceptable', 'terrible',
            'worst', 'cancel', 'refund', 'chargeback'
        ]
        
        # Check for critical indicators
        if any(word in message_lower for word in critical_keywords):
            return 'critical'
        
        # Check for high priority indicators
        if any(word in message_lower for word in high_keywords):
            return 'high'
        
        # Check if AI detected escalation
        if ai_response.get('escalation_required', False):
            return 'high'
        
        # Check sentiment
        sentiment = ai_response.get('sentiment_score', 0.5)
        if sentiment < -0.5:  # Very negative sentiment
            return 'high'
        
        # Default to normal
        return 'normal'

    def _extract_urgency_keywords(self, message: str) -> list:
        """
        Extract keywords that indicate urgency from the message
        
        Args:
            message: Customer message
            
        Returns:
            List of urgency keywords found
        """
        message_lower = message.lower()
        urgency_words = [
            'urgent', 'emergency', 'critical', 'asap', 'immediately',
            'right now', 'today', 'important', 'down', 'outage', 'broken',
            'not working', 'error', 'failed', 'crash', 'freeze', 'stuck'
        ]
        
        found = [word for word in urgency_words if word in message_lower]
        return found

    async def detect_sentiment(self, message: str) -> float:
        """
        Detect sentiment score from message (-1.0 to 1.0)

        Args:
            message: Customer message

        Returns:
            Sentiment score
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Analyze sentiment. Return JSON: {score: float between -1.0 and 1.0}"},
                    {"role": "user", "content": f"Analyze sentiment: {message}"}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )

            result = json.loads(response.choices[0].message.content)
            return float(result.get("score", 0.0))

        except Exception as e:
            print(f"Sentiment Analysis Error: {str(e)}")
            return 0.0


# Global AI service instance
ai_service = AIService()
