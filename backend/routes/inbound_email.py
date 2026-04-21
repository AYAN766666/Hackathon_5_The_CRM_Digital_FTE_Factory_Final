"""
Inbound Email Routes - Process incoming Gmail emails
"""
from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter(tags=["Inbound Email"])


class ProcessEmailsRequest(BaseModel):
    """Request to process incoming emails"""
    limit: int = 10


@router.post(
    "/process",
    summary="Process incoming emails",
    description="Fetch and process unread emails from Gmail inbox"
)
async def process_incoming_emails(request: ProcessEmailsRequest = None):
    """
    Process incoming support emails from Gmail
    
    - Fetches unread emails from support inbox
    - Parses email content
    - Generates AI responses
    - Sends replies
    - Creates/updates tickets
    
    - **limit**: Maximum number of emails to process (default: 10)
    """
    from services.gmail_inbound import gmail_inbound
    
    limit = request.limit if request else 10
    
    try:
        results = await gmail_inbound.process_inbox(limit)
        
        return {
            "success": True,
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing emails: {str(e)}"
        )


@router.get(
    "/status",
    summary="Check Gmail connection status",
    description="Test connection to Gmail IMAP server"
)
async def check_gmail_status() -> Dict[str, Any]:
    """Check Gmail connection status"""
    from config import settings
    
    try:
        import imaplib
        
        mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
        mail.login(settings.gmail_email, settings.gmail_app_password)
        mail.select("INBOX")
        
        # Count unread emails
        status, messages = mail.search(None, "UNSEEN")
        unread_count = len(messages[0].split()) if messages[0] else 0
        
        mail.close()
        mail.logout()
        
        return {
            "status": "connected",
            "email": settings.gmail_email,
            "unread_count": unread_count
        }
        
    except Exception as e:
        return {
            "status": "disconnected",
            "error": str(e)
        }


@router.post(
    "/process/background",
    summary="Process emails in background",
    description="Start background email processing (non-blocking)"
)
async def process_emails_background(
    background_tasks: BackgroundTasks,
    request: ProcessEmailsRequest = None
):
    """Process emails in background (non-blocking)"""
    from services.gmail_inbound import gmail_inbound
    
    limit = request.limit if request else 10
    
    background_tasks.add_task(gmail_inbound.process_inbox, limit)
    
    return {
        "status": "queued",
        "message": f"Email processing started for up to {limit} emails"
    }
