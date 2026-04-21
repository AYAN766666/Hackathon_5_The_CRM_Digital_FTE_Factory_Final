"""
Analytics Routes - Sentiment Analysis Dashboard
"""
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, extract
from typing import Dict, List
from datetime import datetime, timedelta
import sys
import os

# Add parent path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from database import get_db
from schemas import (
    AnalyticsResponse,
    SentimentTrend,
    CategoryBreakdown,
    ChannelBreakdown
)
from models import ChannelType, Conversation, ConversationStatus, Message, SenderType

router = APIRouter()


@router.get(
    "/analytics",
    response_model=AnalyticsResponse,
    summary="Get analytics dashboard data",
    description="Retrieve comprehensive analytics including sentiment trends, category breakdown, and channel metrics"
)
async def get_analytics(db: AsyncSession = Depends(get_db)) -> AnalyticsResponse:
    """
    Get analytics dashboard data
    
    Returns comprehensive metrics:
    - Total tickets by status
    - Sentiment analysis and trends
    - Category breakdown
    - Channel distribution
    - Customer satisfaction score
    """
    try:
        # Get conversation counts by status
        total_result = await db.execute(select(func.count(Conversation.conversation_id)))
        total_tickets = total_result.scalar() or 0
        
        active_result = await db.execute(
            select(func.count(Conversation.conversation_id))
            .where(Conversation.status == ConversationStatus.active)
        )
        active_tickets = active_result.scalar() or 0
        
        escalated_result = await db.execute(
            select(func.count(Conversation.conversation_id))
            .where(Conversation.status == ConversationStatus.escalated)
        )
        escalated_tickets = escalated_result.scalar() or 0
        
        closed_result = await db.execute(
            select(func.count(Conversation.conversation_id))
            .where(Conversation.status == ConversationStatus.closed)
        )
        closed_tickets = closed_result.scalar() or 0
        
        # Get average sentiment from messages
        sentiment_result = await db.execute(
            select(func.avg(Message.sentiment_score))
            .where(Message.sentiment_score.isnot(None))
        )
        average_sentiment = sentiment_result.scalar()
        
        # Get sentiment trend (last 7 days)
        sentiment_trend = await get_sentiment_trend(db)
        
        # Get category breakdown (from conversation channel distribution as proxy)
        category_breakdown = await get_channel_breakdown(db)
        
        # Get channel breakdown
        channel_breakdown = await get_channel_breakdown_detailed(db)
        
        # Calculate satisfaction score (0-100 based on sentiment)
        satisfaction_score = 0.0
        if average_sentiment is not None:
            # Convert sentiment (-1 to 1) to satisfaction (0 to 100)
            satisfaction_score = round((average_sentiment + 1) * 50, 1)
        
        # Get average response time
        response_time_result = await db.execute(
            select(func.avg(Message.processed_latency_ms))
            .where(Message.processed_latency_ms.isnot(None))
        )
        response_time_avg_ms = int(response_time_result.scalar() or 0)
        
        return AnalyticsResponse(
            total_tickets=total_tickets,
            active_tickets=active_tickets,
            escalated_tickets=escalated_tickets,
            closed_tickets=closed_tickets,
            average_sentiment=round(average_sentiment, 3) if average_sentiment else None,
            sentiment_trend=sentiment_trend,
            category_breakdown=category_breakdown,
            channel_breakdown=channel_breakdown,
            satisfaction_score=satisfaction_score,
            response_time_avg_ms=response_time_avg_ms or None
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving analytics: {str(e)}"
        )


async def get_sentiment_trend(db: AsyncSession) -> List[SentimentTrend]:
    """Get sentiment trend for last 7 days"""
    trend = []
    today = datetime.utcnow().date()
    
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        
        # Get messages for this date
        start_date = datetime.combine(date, datetime.min.time())
        end_date = start_date + timedelta(days=1)
        
        result = await db.execute(
            select(
                func.avg(Message.sentiment_score),
                func.count(Message.message_id)
            )
            .where(Message.created_at >= start_date)
            .where(Message.created_at < end_date)
            .where(Message.sentiment_score.isnot(None))
        )
        row = result.first()
        
        avg_sentiment = row[0] or 0.0
        total_messages = row[1] or 0
        
        # Count by sentiment category
        positive_result = await db.execute(
            select(func.count(Message.message_id))
            .where(Message.created_at >= start_date)
            .where(Message.created_at < end_date)
            .where(Message.sentiment_score > 0.2)
        )
        positive_count = positive_result.scalar() or 0
        
        negative_result = await db.execute(
            select(func.count(Message.message_id))
            .where(Message.created_at >= start_date)
            .where(Message.created_at < end_date)
            .where(Message.sentiment_score < -0.2)
        )
        negative_count = negative_result.scalar() or 0
        
        neutral_count = total_messages - positive_count - negative_count
        
        trend.append(SentimentTrend(
            date=date_str,
            average_sentiment=round(avg_sentiment, 3),
            total_messages=total_messages,
            positive_count=positive_count,
            neutral_count=neutral_count,
            negative_count=negative_count
        ))
    
    return trend


async def get_channel_breakdown(db: AsyncSession) -> List[CategoryBreakdown]:
    """Get breakdown by channel (used as category proxy)"""
    result = await db.execute(
        select(
            Conversation.channel,
            func.count(Conversation.conversation_id),
            func.avg(Message.sentiment_score)
        )
        .outerjoin(Message, Message.conversation_id == Conversation.conversation_id)
        .group_by(Conversation.channel)
    )
    
    rows = result.all()
    total = sum(row[1] for row in rows)
    
    breakdown = []
    for row in rows:
        channel = row[0].value if hasattr(row[0], 'value') else str(row[0])
        count = row[1]
        percentage = round((count / total * 100), 1) if total > 0 else 0
        avg_sentiment = round(row[2], 3) if row[2] else None
        
        breakdown.append(CategoryBreakdown(
            category=channel,
            count=count,
            percentage=percentage,
            average_sentiment=avg_sentiment
        ))
    
    return breakdown


async def get_channel_breakdown_detailed(db: AsyncSession) -> List[ChannelBreakdown]:
    """Get detailed breakdown by channel"""
    result = await db.execute(
        select(
            Conversation.channel,
            func.count(Conversation.conversation_id),
            func.avg(Message.sentiment_score)
        )
        .outerjoin(Message, Message.conversation_id == Conversation.conversation_id)
        .group_by(Conversation.channel)
        .order_by(func.count(Conversation.conversation_id).desc())
    )
    
    rows = result.all()
    total = sum(row[1] for row in rows)
    
    breakdown = []
    for row in rows:
        channel = row[0].value if hasattr(row[0], 'value') else str(row[0])
        count = row[1]
        percentage = round((count / total * 100), 1) if total > 0 else 0
        avg_sentiment = round(row[2], 3) if row[2] else None
        
        breakdown.append(ChannelBreakdown(
            channel=channel,
            count=count,
            percentage=percentage,
            average_sentiment=avg_sentiment
        ))
    
    return breakdown
