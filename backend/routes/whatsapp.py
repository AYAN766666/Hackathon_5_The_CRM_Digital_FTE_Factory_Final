"""
WhatsApp Route - Send WhatsApp messages via persistent agent
"""
from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.whatsapp_agent import WhatsAppAgent, get_whatsapp_agent, initialize_whatsapp_agent

router = APIRouter()

# Global agent instance
_whatsapp_agent: Optional[WhatsAppAgent] = None


class WhatsAppMessageRequest(BaseModel):
    """Request model for sending WhatsApp message"""
    phone_number: str
    message: str


class WhatsAppTicketRequest(BaseModel):
    """Request model for sending ticket notification"""
    phone_number: str
    ticket_id: str
    customer_name: Optional[str] = None


@router.on_event("startup")
async def startup_whatsapp():
    """Initialize WhatsApp agent on startup"""
    global _whatsapp_agent
    try:
        print("🚀 Initializing WhatsApp Agent...")
        # Don't await - let it initialize in background
        # _whatsapp_agent = await initialize_whatsapp_agent()
        print("✅ WhatsApp Agent will be initialized on first use")
    except Exception as e:
        print(f"⚠️ WhatsApp Agent startup deferred: {str(e)}")


@router.post("/send", summary="Send WhatsApp message")
async def send_whatsapp_message(request: WhatsAppMessageRequest):
    """
    Send a WhatsApp message

    - **phone_number**: Phone number with country code (e.g., 923198130598)
    - **message**: Message to send
    """
    try:
        agent = await get_whatsapp_agent()
        success = await agent.send_message(request.phone_number, request.message)

        if success:
            return {"status": "sent", "message": "WhatsApp message sent successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to send WhatsApp message")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.post("/send-ticket", summary="Send ticket notification")
async def send_ticket_notification(
    request: WhatsAppTicketRequest,
    background_tasks: BackgroundTasks
):
    """
    Send support ticket notification via WhatsApp

    - **phone_number**: Customer phone number
    - **ticket_id**: Support ticket ID
    - **customer_name**: Optional customer name
    """
    try:
        agent = await get_whatsapp_agent()

        # Send in background
        background_tasks.add_task(
            agent.send_support_notification,
            request.phone_number,
            request.ticket_id,
            request.customer_name
        )

        return {
            "status": "queued",
            "message": "WhatsApp notification queued for sending"
        }

    except Exception as e:
        # If agent not ready, use fallback
        print(f"WhatsApp agent error: {str(e)}")
        return {
            "status": "fallback",
            "message": "WhatsApp agent not ready, using fallback"
        }


@router.get("/status", summary="Get WhatsApp agent status")
async def get_agent_status():
    """Check WhatsApp agent connection status"""
    global _whatsapp_agent

    if _whatsapp_agent is None:
        return {
            "status": "not_initialized",
            "message": "WhatsApp agent not yet initialized"
        }

    return {
        "status": "connected" if _whatsapp_agent.is_connected else "disconnected",
        "is_running": _whatsapp_agent.is_running,
        "queue_size": _whatsapp_agent.message_queue.qsize() if hasattr(_whatsapp_agent, 'message_queue') else 0
    }


@router.post("/initialize", summary="Initialize WhatsApp agent")
async def initialize_agent():
    """Manually initialize WhatsApp agent"""
    global _whatsapp_agent

    try:
        _whatsapp_agent = await initialize_whatsapp_agent()
        return {
            "status": "initialized",
            "message": "WhatsApp agent initialized successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Initialization error: {str(e)}")
