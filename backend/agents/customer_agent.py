"""
Customer Success Agent using OpenAI Agents SDK
Note: This is a wrapper that uses our existing AI service with MCP tools
OpenAI Agents SDK is still in beta, so we're using the function calling approach
"""
import os
import sys
import json
from typing import Optional, Dict, Any, List
from datetime import datetime

# Add parent path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.ai_service import ai_service
from mcp_server import mcp_server
from services.kafka_producer import kafka_producer


class CustomerSuccessAgent:
    """
    Customer Success AI Agent
    
    Uses OpenAI function calling with MCP tools to:
    1. Understand customer messages
    2. Search knowledge base
    3. Create/update tickets
    4. Send responses
    5. Escalate when needed
    """

    def __init__(self):
        self.name = "customer-success-agent"
        self.version = "1.0.0"
        self.tools = mcp_server.get_tools_schema()
        
        # Agent system prompt
        self.system_prompt = """You are a Customer Success AI Agent for a multi-channel support system.

Your capabilities:
1. search_knowledge_base - Search product documentation and FAQs
2. create_ticket - Create support tickets for customers
3. get_customer_history - Retrieve customer's past conversations
4. send_response - Send responses via email or WhatsApp

Your workflow:
1. When a customer message arrives, first search the knowledge base
2. If the customer is new, create a ticket
3. If the customer exists, get their history for context
4. Generate a helpful response based on knowledge base
5. Send the response via the appropriate channel
6. If the issue is complex or customer is angry, mark for escalation

Response format:
Always think step-by-step and use tools in this order:
1. search_knowledge_base(query)
2. get_customer_history(email) - if customer exists
3. create_ticket(...) - if new customer
4. send_response(channel, recipient, message)

Escalation criteria:
- Customer expresses anger or frustration
- Legal threats or complaints
- Refund requests requiring manual approval
- Complex technical issues
- Explicit request for human agent

Be friendly, professional, and concise. Adapt your tone to the channel:
- Email: Formal and detailed
- WhatsApp: Short, friendly with emojis
- Web: Professional but conversational"""

    async def process_message(
        self,
        customer_message: str,
        customer_email: str,
        channel: str = "webform",
        customer_name: Optional[str] = None,
        customer_phone: Optional[str] = None,
        category: str = "General"
    ) -> Dict[str, Any]:
        """
        Process customer message using agent workflow
        
        Args:
            customer_message: Customer's message
            customer_email: Customer email
            channel: Communication channel
            customer_name: Optional customer name
            customer_phone: Optional phone number
            category: Support category
            
        Returns:
            Processing result with response and ticket info
        """
        try:
            # Step 1: Search knowledge base
            kb_results = mcp_server.search_knowledge_base(customer_message, top_k=3)
            
            # Step 2: Get customer history (if exists)
            customer_history = await mcp_server.get_customer_history(
                email=customer_email,
                phone=customer_phone,
                limit=5
            )
            
            # Step 3: Create ticket if new customer
            ticket_info = None
            if customer_history.get("success") and customer_history.get("conversations_count", 0) == 0:
                # New customer, create ticket
                ticket_info = await mcp_server.create_ticket(
                    customer_email=customer_email,
                    channel=channel,
                    message=customer_message,
                    customer_name=customer_name,
                    customer_phone=customer_phone,
                    category=category
                )
            elif customer_history.get("success"):
                # Existing customer, extract ticket ID from recent conversation
                history = customer_history.get("history", [])
                if history:
                    ticket_info = {
                        "ticket_id": history[0].get("conversation_id"),
                        "existing_customer": True
                    }
            
            # Step 4: Generate AI response using knowledge base
            ai_response = await ai_service.generate_response(
                customer_message=customer_message,
                category=category,
                channel=channel
            )
            
            # Step 5: Send response
            response_sent = False
            if channel == "email" and customer_email:
                send_result = await mcp_server.send_response(
                    channel="email",
                    recipient=customer_email,
                    message=ai_response["response"],
                    ticket_id=ticket_info.get("ticket_id") if ticket_info else None
                )
                response_sent = send_result.get("success", False)
                
            elif channel == "whatsapp" and customer_phone:
                send_result = await mcp_server.send_response(
                    channel="whatsapp",
                    recipient=customer_phone,
                    message=ai_response["response"],
                    ticket_id=ticket_info.get("ticket_id") if ticket_info else None
                )
                response_sent = send_result.get("success", False)
            
            # Step 6: Handle escalation
            if ai_response.get("escalation_required"):
                # Publish escalation event
                await kafka_producer.publish_ticket_escalated(
                    ticket_id=ticket_info.get("ticket_id", "UNKNOWN"),
                    reason="AI detected complex issue requiring human agent"
                )
            
            # Compile result
            return {
                "success": True,
                "ticket_id": ticket_info.get("ticket_id") if ticket_info else None,
                "response": ai_response["response"],
                "response_sent": response_sent,
                "escalation_required": ai_response.get("escalation_required", False),
                "sentiment_score": ai_response.get("sentiment_score", 0.5),
                "category": ai_response.get("category", category),
                "kb_articles_used": ai_response.get("kb_articles_used", []),
                "customer_history": customer_history.get("conversations_count", 0) if customer_history.get("success") else 0
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "fallback_response": "Thank you for contacting us. Your request has been received and will be reviewed by our team."
            }

    def get_agent_info(self) -> Dict[str, Any]:
        """Get agent information"""
        return {
            "name": self.name,
            "version": self.version,
            "tools": [tool["function"]["name"] for tool in self.tools],
            "capabilities": [
                "Knowledge base search",
                "Ticket creation",
                "Customer history lookup",
                "Multi-channel response",
                "Escalation detection"
            ]
        }


# Global agent instance
customer_success_agent = CustomerSuccessAgent()


def get_agent() -> CustomerSuccessAgent:
    """Get customer success agent instance"""
    return customer_success_agent
