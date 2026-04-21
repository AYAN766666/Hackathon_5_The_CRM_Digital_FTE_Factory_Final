"""
MCP Server - Customer Success FTE Agent Tools
Exposes tools for AI agent to interact with the support system
"""
import os
import sys
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

# Add parent path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.knowledge_base_service import knowledge_base, search_knowledge_base, get_article, get_all_articles
from services.ai_service import ai_service
from services.customer_service import customer_service
from services.conversation_service import conversation_service
from services.message_service import message_service
from services.email_service import email_service
from services.whatsapp_agent import get_whatsapp_agent
from models import ChannelType, SenderType, ConversationStatus
from database import async_session_maker


class MCPServer:
    """
    MCP (Model Context Protocol) Server for Customer Success FTE
    
    Exposes tools for AI agent:
    1. search_knowledge_base - Search product documentation
    2. create_ticket - Create support ticket
    3. get_customer_history - Get customer conversation history
    4. send_response - Send response via appropriate channel
    """

    def __init__(self):
        self.name = "customer-success-fte-mcp"
        self.version = "1.0.0"
        self.tools = self._register_tools()

    def _register_tools(self) -> Dict[str, callable]:
        """Register all MCP tools"""
        return {
            "search_knowledge_base": self.search_knowledge_base,
            "create_ticket": self.create_ticket,
            "get_customer_history": self.get_customer_history,
            "send_response": self.send_response,
        }

    def get_tools_schema(self) -> List[Dict[str, Any]]:
        """Get OpenAI function calling schema for all tools"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "search_knowledge_base",
                    "description": "Search the knowledge base for product documentation and FAQs",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query string"
                            },
                            "top_k": {
                                "type": "integer",
                                "description": "Number of results to return (default: 3)",
                                "default": 3
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_ticket",
                    "description": "Create a new support ticket for a customer",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "customer_email": {
                                "type": "string",
                                "description": "Customer email address"
                            },
                            "customer_name": {
                                "type": "string",
                                "description": "Customer name"
                            },
                            "customer_phone": {
                                "type": "string",
                                "description": "Customer phone number (optional)"
                            },
                            "channel": {
                                "type": "string",
                                "enum": ["email", "whatsapp", "webform"],
                                "description": "Communication channel"
                            },
                            "message": {
                                "type": "string",
                                "description": "Customer message content"
                            },
                            "category": {
                                "type": "string",
                                "enum": ["General", "Technical", "Billing", "Feedback", "Bug Report"],
                                "description": "Support category"
                            }
                        },
                        "required": ["customer_email", "channel", "message"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_customer_history",
                    "description": "Get customer's past conversations and tickets",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "email": {
                                "type": "string",
                                "description": "Customer email address"
                            },
                            "phone": {
                                "type": "string",
                                "description": "Customer phone number (optional)"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of conversations to return (default: 10)",
                                "default": 10
                            }
                        },
                        "required": ["email"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "send_response",
                    "description": "Send response to customer via specified channel",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "channel": {
                                "type": "string",
                                "enum": ["email", "whatsapp"],
                                "description": "Communication channel"
                            },
                            "recipient": {
                                "type": "string",
                                "description": "Email address or phone number"
                            },
                            "message": {
                                "type": "string",
                                "description": "Message content to send"
                            },
                            "ticket_id": {
                                "type": "string",
                                "description": "Associated ticket ID (optional)"
                            }
                        },
                        "required": ["channel", "recipient", "message"]
                    }
                }
            }
        ]

    # Tool 1: Search Knowledge Base
    def search_knowledge_base(self, query: str, top_k: int = 3) -> Dict[str, Any]:
        """
        Search knowledge base for relevant articles
        
        Args:
            query: Search query
            top_k: Number of results
            
        Returns:
            Search results with articles and excerpts
        """
        try:
            results = knowledge_base.search(query, top_k)
            
            # Format for MCP response
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "document": result.get("document"),
                    "score": result.get("score"),
                    "excerpt": result.get("excerpt"),
                    "url": f"kb://{result.get('document')}"
                })
            
            return {
                "success": True,
                "query": query,
                "results_count": len(formatted_results),
                "results": formatted_results
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    # Tool 2: Create Ticket
    async def create_ticket(
        self,
        customer_email: str,
        channel: str,
        message: str,
        customer_name: Optional[str] = None,
        customer_phone: Optional[str] = None,
        category: str = "General"
    ) -> Dict[str, Any]:
        """
        Create a new support ticket
        
        Args:
            customer_email: Customer email
            channel: Communication channel
            message: Customer message
            customer_name: Optional customer name
            customer_phone: Optional phone number
            category: Support category
            
        Returns:
            Ticket creation result with ticket ID
        """
        try:
            async with async_session_maker() as db:
                # Get or create customer
                customer = await customer_service.get_or_create_customer(
                    email=customer_email,
                    name=customer_name
                )
                
                # Get or create conversation
                conversation = await conversation_service.get_or_create_conversation(
                    customer_id=customer.customer_id,
                    channel=ChannelType(channel)
                )
                
                # Save customer message
                await message_service.create_message(
                    conversation_id=conversation.conversation_id,
                    content=message,
                    sender_type=SenderType.customer,
                    sender_identifier=customer_email
                )
                
                return {
                    "success": True,
                    "ticket_id": str(conversation.conversation_id)[:8].upper(),
                    "conversation_id": str(conversation.conversation_id),
                    "customer_id": str(customer.customer_id),
                    "status": conversation.status.value,
                    "channel": channel
                }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    # Tool 3: Get Customer History
    async def get_customer_history(
        self,
        email: str,
        phone: Optional[str] = None,
        limit: int = 10
    ) -> Dict[str, Any]:
        """
        Get customer's conversation history
        
        Args:
            email: Customer email
            phone: Optional phone number
            limit: Maximum conversations to return
            
        Returns:
            Customer history with past conversations
        """
        try:
            async with async_session_maker() as db:
                # Find customer by email or phone
                customer = None
                if email:
                    customer = await customer_service.get_customer_by_email(email)
                elif phone:
                    customer = await customer_service.get_customer_by_phone(phone)
                
                if not customer:
                    return {
                        "success": False,
                        "error": "Customer not found"
                    }
                
                # Get conversations
                conversations = await conversation_service.get_customer_conversations(
                    customer_id=customer.customer_id,
                    limit=limit
                )
                
                # Format response
                history = []
                for conv in conversations:
                    messages = await message_service.get_messages_by_conversation(
                        conv.conversation_id
                    )
                    
                    history.append({
                        "conversation_id": str(conv.conversation_id)[:8].upper(),
                        "channel": conv.channel.value,
                        "status": conv.status.value,
                        "started_at": conv.started_at.isoformat() if conv.started_at else None,
                        "message_count": len(messages),
                        "recent_messages": [
                            {
                                "sender": msg.sender_type.value,
                                "content": msg.content[:100],
                                "timestamp": msg.created_at.isoformat() if msg.created_at else None
                            }
                            for msg in messages[-3:]  # Last 3 messages
                        ]
                    })
                
                return {
                    "success": True,
                    "customer": {
                        "id": str(customer.customer_id),
                        "email": customer.email,
                        "name": customer.name
                    },
                    "conversations_count": len(history),
                    "history": history
                }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    # Tool 4: Send Response
    async def send_response(
        self,
        channel: str,
        recipient: str,
        message: str,
        ticket_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send response to customer
        
        Args:
            channel: Communication channel (email/whatsapp)
            recipient: Email or phone number
            message: Message content
            ticket_id: Optional ticket ID
            
        Returns:
            Send status
        """
        try:
            if channel == "email":
                # Send email
                success = await email_service.send_support_email(
                    customer_email=recipient,
                    ticket_id=ticket_id or "SUPPORT",
                    ai_response=message
                )
                
                return {
                    "success": success,
                    "channel": "email",
                    "recipient": recipient,
                    "message_id": ticket_id
                }
                
            elif channel == "whatsapp":
                # Send WhatsApp
                agent = await get_whatsapp_agent()
                success = await agent.send_message(recipient, message)
                
                return {
                    "success": success,
                    "channel": "whatsapp",
                    "recipient": recipient,
                    "message_id": ticket_id
                }
                
            else:
                return {
                    "success": False,
                    "error": f"Unsupported channel: {channel}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def list_tools(self) -> List[str]:
        """List all available tools"""
        return list(self.tools.keys())

    def get_tool_info(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific tool"""
        schemas = self.get_tools_schema()
        for schema in schemas:
            if schema["function"]["name"] == tool_name:
                return schema["function"]
        return None


# Global MCP server instance
mcp_server = MCPServer()


# Standalone functions for direct import
def get_mcp_server() -> MCPServer:
    """Get MCP server instance"""
    return mcp_server


def get_available_tools() -> List[str]:
    """Get list of available tools"""
    return mcp_server.list_tools()
