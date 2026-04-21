"""
Email Routes - Email sending endpoints
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Optional

router = APIRouter()


class EmailTestRequest(BaseModel):
    """Request model for test email"""
    email: EmailStr
    name: Optional[str] = None


class EmailTestResponse(BaseModel):
    """Response model for test email"""
    status: str
    message: str


@router.post(
    "/test",
    response_model=EmailTestResponse,
    summary="Test email sending",
    description="Send a test email to verify email configuration"
)
async def test_email(request: EmailTestRequest):
    """
    Send a test email to verify email configuration works
    """
    try:
        from services.email_service import email_service
        
        success = await email_service.send_support_email(
            customer_email=request.email,
            ticket_id="TEST-12345",
            ai_response="This is a test email to verify your email configuration is working correctly.",
            customer_name=request.name
        )
        
        if success:
            return EmailTestResponse(
                status="success",
                message=f"Test email sent to {request.email}"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send email. Check server logs for details."
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error sending email: {str(e)}"
        )
