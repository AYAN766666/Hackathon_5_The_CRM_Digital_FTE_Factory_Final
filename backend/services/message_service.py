"""
Message Service - Handle message operations
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from datetime import datetime
import uuid
import sys
import os

# Add parent path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models import Message, SenderType
from database import async_session_maker


class MessageService:
    """Service for message management"""
    
    async def create_message(
        self,
        conversation_id: uuid.UUID,
        content: str,
        sender_type: SenderType,
        sender_identifier: Optional[str] = None,
        sentiment_score: Optional[float] = None,
        escalation_required: bool = False,
        processed_latency_ms: Optional[int] = None,
        priority: Optional[str] = None,
        urgency_keywords: Optional[str] = None
    ) -> Message:
        """
        Create a new message

        Args:
            conversation_id: Parent conversation ID
            content: Message content
            sender_type: Who sent the message
            sender_identifier: Identifier for the sender
            sentiment_score: Message sentiment (-1.0 to 1.0)
            escalation_required: Whether escalation is needed
            processed_latency_ms: Processing latency in milliseconds
            priority: Message priority (critical, high, normal, low)
            urgency_keywords: Comma-separated urgency keywords

        Returns:
            Created Message
        """
        async with async_session_maker() as session:
            message = Message(
                conversation_id=conversation_id,
                content=content,
                sender_type=sender_type,
                sender_identifier=sender_identifier,
                sentiment_score=sentiment_score,
                escalation_required=escalation_required,
                processed_latency_ms=processed_latency_ms,
                priority=priority,
                urgency_keywords=urgency_keywords
            )
            session.add(message)
            await session.commit()
            await session.refresh(message)

            return message
    
    async def get_messages_by_conversation(
        self,
        conversation_id: uuid.UUID
    ) -> List[Message]:
        """Get all messages for a conversation"""
        async with async_session_maker() as session:
            result = await session.execute(
                select(Message)
                .where(Message.conversation_id == conversation_id)
                .order_by(Message.created_at.asc())
            )
            messages = result.scalars().all()
            print(f"📦 Found {len(messages)} messages for conversation {conversation_id}")
            for i, msg in enumerate(messages):
                print(f"   Message {i+1}: sender={msg.sender_type.value}, content={msg.content[:50]}...")
            return messages
    
    async def get_message_by_id(
        self,
        message_id: uuid.UUID
    ) -> Optional[Message]:
        """Get message by ID"""
        async with async_session_maker() as session:
            result = await session.execute(
                select(Message)
                .where(Message.message_id == message_id)
            )
            return result.scalar_one_or_none()
    
    async def mark_escalation(
        self,
        message_id: uuid.UUID
    ) -> Optional[Message]:
        """Mark message as requiring escalation"""
        async with async_session_maker() as session:
            result = await session.execute(
                select(Message)
                .where(Message.message_id == message_id)
            )
            message = result.scalar_one_or_none()
            
            if message:
                message.escalation_required = True
                await session.commit()
                await session.refresh(message)
            
            return message


# Global message service instance
message_service = MessageService()
