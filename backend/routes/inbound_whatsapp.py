"""
WhatsApp Inbound Routes - Process incoming WhatsApp messages
"""
from fastapi import APIRouter, HTTPException, status, BackgroundTasks, Request
from pydantic import BaseModel
from typing import Dict, Any, Optional

router = APIRouter(tags=["Inbound WhatsApp"])


class WhatsAppMessageRequest(BaseModel):
    """Incoming WhatsApp message webhook"""
    phone_number: str
    content: str
    sender_name: Optional[str] = None
    timestamp: Optional[str] = None


class ProcessMessageRequest(BaseModel):
    """Request to process WhatsApp messages"""
    limit: int = 10


@router.post(
    "/message",
    summary="Receive WhatsApp message webhook",
    description="Receive incoming WhatsApp message via webhook"
)
async def receive_whatsapp_message(
    request: WhatsAppMessageRequest,
    background_tasks: BackgroundTasks
):
    """
    Receive incoming WhatsApp message via webhook
    
    This endpoint can be used as a webhook target for WhatsApp Business API
    or other WhatsApp gateway services.
    
    - **phone_number**: Sender's phone number
    - **content**: Message content
    - **sender_name**: Optional sender name
    - **timestamp**: Optional timestamp
    """
    from services.whatsapp_inbound import process_whatsapp_message
    
    message_data = {
        "phone_number": request.phone_number,
        "content": request.content,
        "sender_name": request.sender_name,
        "timestamp": request.timestamp
    }
    
    # Process in background
    background_tasks.add_task(process_whatsapp_message, message_data)
    
    return {
        "status": "received",
        "message": "WhatsApp message queued for processing"
    }


@router.post(
    "/process",
    summary="Process WhatsApp messages",
    description="Fetch and process pending WhatsApp messages"
)
async def process_whatsapp_messages(request: ProcessMessageRequest = None):
    """
    Process pending WhatsApp messages
    
    Note: This is a placeholder for actual WhatsApp Web scraping
    """
    # For now, return status
    return {
        "status": "monitoring",
        "message": "WhatsApp inbound processing is active",
        "note": "Messages are processed in real-time via WhatsApp agent"
    }


@router.get(
    "/status",
    summary="Check WhatsApp inbound status",
    description="Check if WhatsApp inbound processing is active"
)
async def get_whatsapp_inbound_status() -> Dict[str, Any]:
    """Check WhatsApp inbound status"""
    from services.whatsapp_inbound import whatsapp_inbound
    
    return {
        "is_monitoring": whatsapp_inbound.is_monitoring,
        "agent_connected": whatsapp_inbound.agent is not None and whatsapp_inbound.agent.is_connected
    }


@router.post(
    "/start-monitoring",
    summary="Start WhatsApp monitoring",
    description="Start background WhatsApp message monitoring"
)
async def start_monitoring(background_tasks: BackgroundTasks):
    """Start WhatsApp message monitoring in background"""
    from services.whatsapp_inbound import start_whatsapp_monitoring
    
    background_tasks.add_task(start_whatsapp_monitoring)
    
    return {
        "status": "started",
        "message": "WhatsApp monitoring started in background"
    }


@router.post(
    "/stop-monitoring",
    summary="Stop WhatsApp monitoring",
    description="Stop WhatsApp message monitoring"
)
async def stop_monitoring():
    """Stop WhatsApp message monitoring"""
    from services.whatsapp_inbound import stop_whatsapp_monitoring
    
    await stop_whatsapp_monitoring()
    
    return {
        "status": "stopped",
        "message": "WhatsApp monitoring stopped"
    }


# Webhook endpoint for external WhatsApp services
@router.post(
    "/webhook",
    summary="WhatsApp webhook endpoint",
    description="Generic webhook endpoint for WhatsApp Business API or gateways"
)
async def whatsapp_webhook(request: Request):
    """
    Generic webhook endpoint for WhatsApp messages
    
    Accepts various webhook formats from:
    - WhatsApp Business API
    - Twilio WhatsApp API
    - Other WhatsApp gateway services
    """
    try:
        body = await request.json()
        
        # Extract message data based on webhook format
        # This is a generic handler - customize based on your provider
        
        phone_number = None
        content = None
        sender_name = None
        
        # Twilio format
        if "From" in body:
            phone_number = body.get("From", "").replace("whatsapp:", "")
            content = body.get("Body", "")
        
        # WhatsApp Business API format
        elif "messages" in body:
            messages = body.get("messages", [])
            if messages:
                phone_number = body.get("contacts", [{}])[0].get("wa_id", "")
                content = messages[0].get("text", {}).get("body", "")
                sender_name = body.get("contacts", [{}])[0].get("profile", {}).get("name", "")
        
        # Generic format
        else:
            phone_number = body.get("phone_number") or body.get("phoneNumber")
            content = body.get("content") or body.get("message") or body.get("text")
            sender_name = body.get("sender_name") or body.get("senderName")
        
        if not phone_number or not content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing phone_number or content in webhook"
            )
        
        # Process message
        from services.whatsapp_inbound import process_whatsapp_message
        
        message_data = {
            "phone_number": phone_number,
            "content": content,
            "sender_name": sender_name
        }
        
        result = await process_whatsapp_message(message_data)
        
        return {
            "status": "processed",
            "result": result
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Webhook processing error: {str(e)}"
        )
