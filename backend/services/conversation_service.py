"""
Conversation Service - Handle conversation lifecycle
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional, List
from datetime import datetime, timedelta
import uuid
import sys
import os

# Add parent path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models import Conversation, ConversationStatus, ChannelType, Message, SenderType
from database import async_session_maker


class ConversationService:
    """Service for conversation management"""
    
    CONVERSATION_WINDOW_HOURS = 24
    
    async def get_or_create_conversation(
        self,
        customer_id: uuid.UUID,
        channel: ChannelType
    ) -> Conversation:
        """
        Get active conversation or create new one
        
        Args:
            customer_id: Customer UUID
            channel: Communication channel
            
        Returns:
            Active or new Conversation
        """
        async with async_session_maker() as session:
            # Find active conversation for this customer and channel
            result = await session.execute(
                select(Conversation)
                .where(Conversation.customer_id == customer_id)
                .where(Conversation.channel == channel)
                .where(Conversation.status == ConversationStatus.active)
                .where(Conversation.expires_at > func.now())
                .order_by(Conversation.last_message_at.desc())
            )
            conversation = result.scalar_one_or_none()
            
            if conversation:
                return conversation
            
            # Create new conversation
            now = datetime.utcnow()
            expires_at = now + timedelta(hours=self.CONVERSATION_WINDOW_HOURS)
            
            conversation = Conversation(
                customer_id=customer_id,
                channel=channel,
                status=ConversationStatus.active,
                started_at=now,
                last_message_at=now,
                expires_at=expires_at
            )
            session.add(conversation)
            await session.commit()
            await session.refresh(conversation)
            
            return conversation
    
    async def get_conversation_by_id(
        self,
        conversation_id: uuid.UUID
    ) -> Optional[Conversation]:
        """Get conversation by full UUID"""
        async with async_session_maker() as session:
            result = await session.execute(
                select(Conversation)
                .where(Conversation.conversation_id == conversation_id)
            )
            return result.scalar_one_or_none()
    
    async def get_conversation_by_short_id(
        self,
        short_id: str
    ) -> Optional[Conversation]:
        """
        Get conversation by short ticket ID (first 8 chars of UUID)

        Args:
            short_id: Short ticket ID (e.g., "928054FD")

        Returns:
            Conversation or None
        """
        async with async_session_maker() as session:
            # Convert to uppercase for case-insensitive matching
            short_id_upper = short_id.upper()

            # Get all conversations ordered by most recent first
            result = await session.execute(
                select(Conversation)
                .order_by(Conversation.started_at.desc())
            )
            all_conversations = result.scalars().all()

            # Find matching conversation
            for conv in all_conversations:
                conv_short_id = str(conv.conversation_id)[:8].upper()
                print(f"Checking {conv_short_id} against {short_id_upper}")
                if conv_short_id == short_id_upper:
                    print(f"✅ Found conversation: {conv.conversation_id}")
                    print(f"   Customer ID: {conv.customer_id}")
                    print(f"   Channel: {conv.channel}")
                    print(f"   Status: {conv.status}")
                    return conv

            print(f"❌ No conversation found for {short_id_upper}")
            return None
    
    async def get_conversation_with_messages(
        self,
        conversation_id: uuid.UUID
    ) -> Optional[dict]:
        """Get conversation with all messages"""
        async with async_session_maker() as session:
            # Get conversation
            result = await session.execute(
                select(Conversation)
                .where(Conversation.conversation_id == conversation_id)
            )
            conversation = result.scalar_one_or_none()
            
            if not conversation:
                return None
            
            # Get messages
            result = await session.execute(
                select(Message)
                .where(Message.conversation_id == conversation_id)
                .order_by(Message.created_at.asc())
            )
            messages = result.scalars().all()
            
            return {
                "conversation": conversation,
                "messages": messages
            }
    
    async def close_conversation(
        self,
        conversation_id: uuid.UUID
    ) -> Optional[Conversation]:
        """Mark conversation as closed"""
        async with async_session_maker() as session:
            result = await session.execute(
                select(Conversation)
                .where(Conversation.conversation_id == conversation_id)
            )
            conversation = result.scalar_one_or_none()
            
            if conversation:
                conversation.status = ConversationStatus.closed
                await session.commit()
                await session.refresh(conversation)
            
            return conversation
    
    async def escalate_conversation(
        self,
        conversation_id: uuid.UUID
    ) -> Optional[Conversation]:
        """Mark conversation as escalated"""
        async with async_session_maker() as session:
            result = await session.execute(
                select(Conversation)
                .where(Conversation.conversation_id == conversation_id)
            )
            conversation = result.scalar_one_or_none()
            
            if conversation:
                conversation.status = ConversationStatus.escalated
                await session.commit()
                await session.refresh(conversation)
            
            return conversation
    
    async def update_sentiment(
        self,
        conversation_id: uuid.UUID,
        sentiment_score: float
    ) -> Optional[Conversation]:
        """Update conversation sentiment score"""
        async with async_session_maker() as session:
            result = await session.execute(
                select(Conversation)
                .where(Conversation.conversation_id == conversation_id)
            )
            conversation = result.scalar_one_or_none()

            if conversation:
                conversation.sentiment_score = sentiment_score
                conversation.last_message_at = datetime.utcnow()
                conversation.expires_at = datetime.utcnow() + timedelta(hours=self.CONVERSATION_WINDOW_HOURS)
                await session.commit()
                await session.refresh(conversation)

            return conversation

    async def delete_conversation(
        self,
        conversation_id: uuid.UUID
    ) -> bool:
        """
        Delete conversation and all associated messages (cascade delete)

        Args:
            conversation_id: UUID of conversation to delete

        Returns:
            True if deleted, False if not found
        """
        async with async_session_maker() as session:
            # Get conversation
            result = await session.execute(
                select(Conversation)
                .where(Conversation.conversation_id == conversation_id)
            )
            conversation = result.scalar_one_or_none()

            if not conversation:
                return False

            # Delete the conversation (messages will be deleted via cascade)
            await session.delete(conversation)
            await session.commit()

            print(f"✅ Deleted conversation: {conversation_id} with all messages")
            return True


# Global conversation service instance
conversation_service = ConversationService()
