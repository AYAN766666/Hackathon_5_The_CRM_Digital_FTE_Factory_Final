"""
Database Models
"""
from sqlalchemy import Column, String, Text, DateTime, Boolean, Float, Enum as SQLEnum, ForeignKey, Index, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from enum import Enum
import uuid
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import Base


class ChannelType(str, Enum):
    """Supported communication channels"""
    email = "email"
    whatsapp = "whatsapp"
    webform = "webform"


class ConversationStatus(str, Enum):
    """Conversation status options"""
    active = "active"
    closed = "closed"
    escalated = "escalated"


class SenderType(str, Enum):
    """Message sender types"""
    customer = "customer"
    agent = "agent"
    system = "system"


class Customer(Base):
    """Customer model - represents a unique individual seeking support"""
    __tablename__ = "customers"
    
    customer_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=True)
    phone = Column(String, nullable=True, index=True)
    name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_customer_email', 'email'),
        Index('idx_customer_phone', 'phone'),
    )
    
    def __repr__(self):
        return f"<Customer(id={self.customer_id}, email={self.email})>"


class Conversation(Base):
    """Conversation model - represents a support conversation within 24-hour window"""
    __tablename__ = "conversations"

    conversation_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.customer_id"), nullable=False)
    channel = Column(SQLEnum(ChannelType), nullable=False)
    status = Column(SQLEnum(ConversationStatus), default=ConversationStatus.active)
    sentiment_score = Column(Float, nullable=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    last_message_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)

    # Relationship with cascade delete
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Conversation(id={self.conversation_id}, customer_id={self.customer_id}, status={self.status})>"


class Message(Base):
    """Message model - represents individual messages in a conversation"""
    __tablename__ = "messages"

    message_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.conversation_id"), nullable=False)
    sender_type = Column(SQLEnum(SenderType), nullable=False)
    sender_identifier = Column(String, nullable=True)
    content = Column(Text, nullable=False)
    sentiment_score = Column(Float, nullable=True)
    priority = Column(String, nullable=True)  # NEW: critical, high, normal, low
    urgency_keywords = Column(String, nullable=True)  # NEW: comma-separated keywords
    escalation_required = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_latency_ms = Column(Integer, nullable=True)

    # Relationship with conversation
    conversation = relationship("Conversation", back_populates="messages")

    def __repr__(self):
        return f"<Message(id={self.message_id}, conversation_id={self.conversation_id})>"
