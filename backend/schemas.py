"""
Pydantic Schemas for Request/Response Validation
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum
import uuid


class CategoryType(str, Enum):
    """Support ticket categories"""
    general = "General"
    technical = "Technical"
    billing = "Billing"
    feedback = "Feedback"
    bug_report = "Bug Report"


class ChannelType(str, Enum):
    """Communication channels"""
    email = "email"
    whatsapp = "whatsapp"
    webform = "webform"


class ConversationStatus(str, Enum):
    """Conversation status"""
    active = "active"
    closed = "closed"
    escalated = "escalated"


# Request Schemas
class SupportSubmitRequest(BaseModel):
    """Request schema for support form submission"""
    name: str = Field(..., min_length=2, max_length=50, description="Customer name")
    email: EmailStr = Field(..., description="Customer email address")
    phone: Optional[str] = Field(None, description="Customer phone number with country code")
    category: CategoryType = Field(..., description="Support category")
    message: str = Field(..., min_length=20, max_length=1000, description="Support message")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john@example.com",
                "phone": "+923198130598",
                "category": "Technical",
                "message": "I'm having trouble logging into my account. Can you help?"
            }
        }


class SupportSubmitResponse(BaseModel):
    """Response schema for support form submission"""
    ticket_id: str = Field(..., description="Unique ticket identifier")
    status: str = Field(..., description="Ticket status")
    message: str = Field(..., description="Success message")
    
    class Config:
        json_schema_extra = {
            "example": {
                "ticket_id": "12345",
                "status": "created",
                "message": "Your support request has been received"
            }
        }


class TicketStatusResponse(BaseModel):
    """Response schema for ticket status check"""
    ticket_id: str
    status: str
    channel: str
    created_at: datetime
    messages: List["MessageResponse"]


class MessageResponse(BaseModel):
    """Message in conversation history"""
    sender: str
    content: str
    timestamp: datetime
    sentiment_score: Optional[float] = None
    priority: Optional[str] = None
    urgency_keywords: Optional[List[str]] = None


class DeleteTicketResponse(BaseModel):
    """Response schema for ticket deletion"""
    message: str = Field(..., description="Success message")
    ticket_id: str = Field(..., description="Deleted ticket ID")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Ticket deleted successfully",
                "ticket_id": "12345"
            }
        }


# Error Response
class ErrorResponse(BaseModel):
    """Error response schema"""
    error: str
    detail: str
    ticket_id: Optional[str] = None


# Analytics Schemas
class SentimentTrend(BaseModel):
    """Sentiment trend data point"""
    date: str
    average_sentiment: float
    total_messages: int
    positive_count: int
    neutral_count: int
    negative_count: int


class CategoryBreakdown(BaseModel):
    """Category breakdown data"""
    category: str
    count: int
    percentage: float
    average_sentiment: Optional[float] = None


class ChannelBreakdown(BaseModel):
    """Channel breakdown data"""
    channel: str
    count: int
    percentage: float
    average_sentiment: Optional[float] = None


class AnalyticsResponse(BaseModel):
    """Analytics dashboard response"""
    total_tickets: int
    active_tickets: int
    escalated_tickets: int
    closed_tickets: int
    average_sentiment: Optional[float] = None
    sentiment_trend: List[SentimentTrend]
    category_breakdown: List[CategoryBreakdown]
    channel_breakdown: List[ChannelBreakdown]
    satisfaction_score: float
    response_time_avg_ms: Optional[int] = None
