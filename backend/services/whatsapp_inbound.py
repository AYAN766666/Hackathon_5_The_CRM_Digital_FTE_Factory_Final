"""
WhatsApp Inbound Service - Receive and process incoming WhatsApp messages
"""
import os
import sys
import asyncio
from typing import Optional, Dict, Any, List
from datetime import datetime
import json
import re

# Add parent path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.whatsapp_agent import WhatsAppAgent, get_whatsapp_agent
from services.ai_service import ai_service
from services.customer_service import customer_service
from services.conversation_service import conversation_service
from services.message_service import message_service
from services.kafka_producer import kafka_producer
from models import ChannelType, SenderType


class WhatsAppInboundService:
    """
    WhatsApp Inbound Service - Process incoming WhatsApp messages
    
    Features:
    - Monitor WhatsApp Web for new messages
    - Parse incoming messages
    - Generate AI responses
    - Send replies via WhatsApp
    - Create/update tickets
    """

    def __init__(self):
        self.agent: Optional[WhatsAppAgent] = None
        self.is_monitoring = False
        self.message_handlers = []

    async def start_monitoring(self, check_interval: int = 5):
        """
        Start monitoring WhatsApp for new messages
        
        Args:
            check_interval: Seconds between checks
        """
        try:
            self.agent = await get_whatsapp_agent()
            self.is_monitoring = True
            
            print("📱 WhatsApp inbound monitoring started")
            
            while self.is_monitoring:
                try:
                    # Check for new messages
                    messages = await self._fetch_new_messages()
                    
                    for message in messages:
                        await self.process_message(message)
                    
                    await asyncio.sleep(check_interval)
                    
                except Exception as e:
                    print(f"Error in monitoring loop: {str(e)}")
                    await asyncio.sleep(check_interval * 2)
                    
        except Exception as e:
            print(f"❌ WhatsApp monitoring error: {str(e)}")
            self.is_monitoring = False

    async def stop_monitoring(self):
        """Stop monitoring WhatsApp"""
        self.is_monitoring = False
        print("🛑 WhatsApp inbound monitoring stopped")

    async def _fetch_new_messages(self) -> List[Dict[str, Any]]:
        """
        Fetch new messages from WhatsApp
        Note: This is a placeholder - actual implementation depends on WhatsApp Web scraping
        
        For now, we'll use a simplified approach with message queue
        """
        # This would need actual WhatsApp Web scraping
        # For demo purposes, we'll return empty list
        # Real implementation would use Playwright to scrape WhatsApp Web
        
        return []

    async def process_message(
        self,
        message_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process incoming WhatsApp message
        
        Args:
            message_data: Message data with phone, content, etc.
            
        Returns:
            Processing result
        """
        try:
            phone_number = message_data.get("phone_number")
            content = message_data.get("content")
            sender_name = message_data.get("sender_name", "Unknown")
            
            if not phone_number or not content:
                return {"success": False, "error": "Missing phone or content"}
            
            # Format phone number
            phone_formatted = phone_number.replace("+", "").replace(" ", "").replace("-", "")
            
            # Get or create customer (using phone as identifier)
            customer = await customer_service.get_or_create_customer(
                email=None,
                phone=phone_formatted,
                name=sender_name if sender_name != "Unknown" else None
            )
            
            # Get or create conversation
            conversation = await conversation_service.get_or_create_conversation(
                customer_id=customer.customer_id,
                channel=ChannelType.whatsapp
            )
            
            # Save customer message
            await message_service.create_message(
                conversation_id=conversation.conversation_id,
                content=content,
                sender_type=SenderType.customer,
                sender_identifier=phone_formatted
            )
            
            # Generate AI response (WhatsApp style - short and friendly)
            ai_response = await ai_service.generate_response(
                customer_message=content,
                category="General",
                channel="whatsapp"
            )
            
            # Save AI response
            await message_service.create_message(
                conversation_id=conversation.conversation_id,
                content=ai_response["response"],
                sender_type=SenderType.agent,
                sender_identifier="AI Agent",
                sentiment_score=ai_response.get("sentiment_score"),
                escalation_required=ai_response.get("escalation_required", False)
            )
            
            # Send WhatsApp response
            ticket_id = str(conversation.conversation_id)[:8].upper()
            
            # Format response for WhatsApp (short with emojis)
            whatsapp_message = f"""Hi {sender_name}! 👋

{ai_response["response"]}

Ticket: {ticket_id}"""

            response_sent = await self.agent.send_message(
                phone_number=phone_formatted,
                message=whatsapp_message
            )
            
            # Publish Kafka event
            await kafka_producer.publish_ticket_created(
                ticket_id=ticket_id,
                customer_email=customer.email or "",
                channel="whatsapp",
                category="General"
            )
            
            # Handle escalation
            if ai_response.get("escalation_required"):
                await conversation_service.escalate_conversation(
                    conversation_id=conversation.conversation_id
                )
                
                await kafka_producer.publish_ticket_escalated(
                    ticket_id=ticket_id,
                    reason="AI detected complex issue"
                )
            
            return {
                "success": True,
                "ticket_id": ticket_id,
                "response_sent": response_sent,
                "escalation_required": ai_response.get("escalation_required", False)
            }
            
        except Exception as e:
            print(f"Error processing WhatsApp message: {str(e)}")
            return {"success": False, "error": str(e)}

    async def send_support_notification(
        self,
        phone_number: str,
        ticket_id: str,
        customer_name: str = None
    ) -> bool:
        """
        Send support ticket notification via WhatsApp
        
        Args:
            phone_number: Customer phone number
            ticket_id: Support ticket ID
            customer_name: Optional customer name
            
        Returns:
            bool: Success status
        """
        if not self.agent:
            self.agent = await get_whatsapp_agent()
        
        name_str = customer_name if customer_name else "there"
        
        message = f"""Hello {name_str}! 👋

Your support ticket *{ticket_id}* has been created.

Our team will review your issue shortly.

Thank you for contacting us!"""
        
        return await self.agent.send_message(phone_number, message)


# Singleton instance
whatsapp_inbound = WhatsAppInboundService()


async def start_whatsapp_monitoring():
    """Start WhatsApp message monitoring"""
    await whatsapp_inbound.start_monitoring()


async def stop_whatsapp_monitoring():
    """Stop WhatsApp message monitoring"""
    await whatsapp_inbound.stop_monitoring()


async def process_whatsapp_message(message_data: Dict[str, Any]):
    """Process a single WhatsApp message"""
    return await whatsapp_inbound.process_message(message_data)
