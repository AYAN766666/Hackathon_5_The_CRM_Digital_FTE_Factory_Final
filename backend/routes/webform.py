"""
Web Form Routes - Support form submission and ticket status
"""
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict
import time
from datetime import datetime
import sys
import os
import asyncio

# Add parent path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from database import get_db
from config import settings
from schemas import (
    SupportSubmitRequest,
    SupportSubmitResponse,
    TicketStatusResponse,
    MessageResponse,
    ErrorResponse,
    DeleteTicketResponse
)
from models import ChannelType, SenderType
from services.customer_service import customer_service
from services.conversation_service import conversation_service
from services.message_service import message_service
from services.ai_service import ai_service
from services.email_service import email_service
# Import WhatsApp agent only when needed (lazy import to avoid blocking startup)
# from services.whatsapp_agent import get_whatsapp_agent  # Removed - use lazy import
from services.kafka_producer import kafka_producer

router = APIRouter()


@router.post(
    "/submit",
    response_model=SupportSubmitResponse,
    status_code=status.HTTP_200_OK,
    summary="Submit support request",
    description="Submit a support request via web form. Returns a ticket ID for tracking."
)
async def submit_support_request(
    request: SupportSubmitRequest,
    db: AsyncSession = Depends(get_db)
) -> SupportSubmitResponse:
    """
    Submit support request via web form
    
    - **name**: Customer name (2-50 characters)
    - **email**: Valid email address
    - **category**: Support category (General, Technical, Billing, Feedback, Bug Report)
    - **message**: Support message (20-1000 characters)
    """
    start_time = time.time()
    
    try:
        # Step 1: Get or create customer
        customer = await customer_service.get_or_create_customer(
            email=request.email,
            name=request.name
        )
        
        # Step 2: Get or create conversation
        conversation = await conversation_service.get_or_create_conversation(
            customer_id=customer.customer_id,
            channel=ChannelType.webform
        )
        
        # Step 3: Save customer message
        customer_message = await message_service.create_message(
            conversation_id=conversation.conversation_id,
            content=request.message,
            sender_type=SenderType.customer,
            sender_identifier=request.email
        )
        
        # Step 4: Generate AI response
        ai_start = time.time()
        ai_response = await ai_service.generate_response(
            customer_message=request.message,
            category=request.category.value,
            channel=ChannelType.webform.value  # Pass channel for tone adjustment
        )
        ai_latency_ms = int((time.time() - ai_start) * 1000)
        
        # Step 5: Save AI response
        ai_message = await message_service.create_message(
            conversation_id=conversation.conversation_id,
            content=ai_response["response"],
            sender_type=SenderType.agent,
            sender_identifier="AI Agent",
            sentiment_score=ai_response["sentiment_score"],
            escalation_required=ai_response["escalation_required"],
            processed_latency_ms=ai_latency_ms,
            priority=ai_response.get("priority", "normal"),
            urgency_keywords=",".join(ai_response.get("urgency_keywords", [])) if ai_response.get("urgency_keywords") else None
        )
        
        # Step 6: Update conversation sentiment
        if ai_response["sentiment_score"]:
            await conversation_service.update_sentiment(
                conversation_id=conversation.conversation_id,
                sentiment_score=ai_response["sentiment_score"]
            )
        
        # Step 7: Handle escalation if needed
        if ai_response["escalation_required"]:
            await conversation_service.escalate_conversation(
                conversation_id=conversation.conversation_id
            )

        # Step 8: Publish Kafka event (non-blocking)
        ticket_id_short = str(conversation.conversation_id)[:8].upper()
        asyncio.create_task(
            publish_kafka_event(
                ticket_id=ticket_id_short,
                customer_email=request.email,
                channel=ChannelType.webform.value,
                category=request.category.value,
                ai_latency_ms=ai_latency_ms
            )
        )

        # Step 9: Send confirmation email (async, non-blocking)
        # Only send if email credentials are configured
        if settings.gmail_email and settings.gmail_app_password:
            asyncio.create_task(
                send_confirmation_email(
                    customer_email=request.email,
                    ticket_id=ticket_id_short,
                    ai_response=ai_response["response"],
                    customer_name=request.name
                )
            )

        # Step 10: Send WhatsApp message if phone number provided (async, non-blocking)
        # Only send if explicitly requested - don't block the main flow
        if request.phone:
            # Fire and forget - don't wait for WhatsApp to send
            asyncio.create_task(
                send_whatsapp_notification_non_blocking(
                    phone_number=request.phone,
                    ticket_id=ticket_id_short,
                    customer_name=request.name
                )
            )

        # Calculate total latency
        total_latency_ms = int((time.time() - start_time) * 1000)

        # Return success response
        return SupportSubmitResponse(
            ticket_id=str(conversation.conversation_id)[:8].upper(),  # Short ticket ID
            status="created" if not ai_response["escalation_required"] else "escalated",
            message="Your support request has been received and processed"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing request: {str(e)}"
        )


@router.get(
    "/ticket/{ticket_id}",
    response_model=TicketStatusResponse,
    summary="Get ticket status",
    description="Retrieve ticket status and conversation history using ticket ID"
)
async def get_ticket_status(ticket_id: str) -> TicketStatusResponse:
    """
    Get ticket status and conversation history

    - **ticket_id**: Ticket ID received after submission (e.g., 928054FD)
    """
    try:
        # Get conversation by short ticket ID (first 8 chars of UUID)
        conversation_data = await conversation_service.get_conversation_by_short_id(ticket_id)

        if not conversation_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ticket not found: {ticket_id}. Please check your ticket ID."
            )

        # Get messages
        messages_data = await message_service.get_messages_by_conversation(
            conversation_data.conversation_id
        )

        # Format messages
        formatted_messages = [
            MessageResponse(
                sender=msg.sender_type.value,
                content=msg.content,
                timestamp=msg.created_at,
                sentiment_score=msg.sentiment_score
            )
            for msg in messages_data
        ]

        return TicketStatusResponse(
            ticket_id=str(conversation_data.conversation_id)[:8].upper(),
            status=conversation_data.status.value,
            channel=conversation_data.channel.value,
            created_at=conversation_data.started_at,
            messages=formatted_messages
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving ticket: {str(e)}"
        )


@router.delete(
    "/ticket/{ticket_id}",
    response_model=DeleteTicketResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete ticket",
    description="Delete a ticket and its conversation history"
)
async def delete_ticket(ticket_id: str) -> DeleteTicketResponse:
    """
    Delete ticket and conversation history

    - **ticket_id**: Ticket ID to delete (e.g., 928054FD)
    """
    try:
        # Get conversation by short ticket ID
        conversation_data = await conversation_service.get_conversation_by_short_id(ticket_id)

        if not conversation_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ticket not found: {ticket_id}. Please check your ticket ID."
            )

        # Delete the conversation
        deleted = await conversation_service.delete_conversation(
            conversation_data.conversation_id
        )

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete ticket"
            )

        return DeleteTicketResponse(
            message="Ticket deleted successfully",
            ticket_id=ticket_id
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting ticket: {str(e)}"
        )


async def send_confirmation_email(
    customer_email: str,
    ticket_id: str,
    ai_response: str,
    customer_name: str = None
):
    """Send confirmation email in background"""
    try:
        await email_service.send_support_email(
            customer_email=customer_email,
            ticket_id=ticket_id,
            ai_response=ai_response,
            customer_name=customer_name
        )
    except Exception as e:
        print(f"Email notification failed: {str(e)}")


async def send_whatsapp_notification_non_blocking(
    phone_number: str,
    ticket_id: str,
    customer_name: str = None
):
    """Send WhatsApp notification in background (non-blocking, with timeout)"""
    try:
        print(f"[INFO] [WhatsApp] Starting notification for {phone_number}...")
        
        # Add timeout to prevent blocking
        from services.whatsapp_agent import get_whatsapp_agent
        from asyncio import wait_for
        
        # Try to get agent with timeout
        try:
            agent = await wait_for(get_whatsapp_agent(), timeout=5.0)
        except asyncio.TimeoutError:
            print("[WARN] [WhatsApp] Agent startup timed out - skipping notification")
            return
        
        if not agent or not agent.is_connected:
            print(f"[WARN] [WhatsApp] Agent not connected - skipping notification")
            return

        # Send with timeout
        try:
            result = await wait_for(
                agent.send_support_notification(
                    phone_number=phone_number,
                    ticket_id=ticket_id,
                    customer_name=customer_name
                ),
                timeout=30.0
            )
            if result:
                print(f"[OK] [WhatsApp] Message sent to {phone_number}")
            else:
                print(f"[WARN] [WhatsApp] Failed to send to {phone_number}")
        except asyncio.TimeoutError:
            print(f"[WARN] [WhatsApp] Send timed out - skipping")
        
    except Exception as e:
        print(f"[ERROR] [WhatsApp] Error: {str(e)}")
        # Don't propagate error - this is background task


async def publish_kafka_event(
    ticket_id: str,
    customer_email: str,
    channel: str,
    category: str,
    ai_latency_ms: int
):
    """Publish ticket event to Kafka in background"""
    try:
        await kafka_producer.publish_ticket_created(
            ticket_id=ticket_id,
            customer_email=customer_email,
            channel=channel,
            category=category,
            ai_latency_ms=ai_latency_ms
        )
    except Exception as e:
        print(f"Kafka event publishing failed: {str(e)}")
