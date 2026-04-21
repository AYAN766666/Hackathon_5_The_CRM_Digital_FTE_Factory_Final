"""
Agent Routes - Expose AI Agent capabilities via API
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, Any

router = APIRouter(tags=["AI Agent"])


class AgentProcessRequest(BaseModel):
    """Request to process customer message via agent"""
    customer_message: str = Field(..., description="Customer's message")
    customer_email: EmailStr = Field(..., description="Customer email")
    channel: str = Field(default="webform", description="Communication channel")
    customer_name: Optional[str] = Field(None, description="Customer name")
    customer_phone: Optional[str] = Field(None, description="Customer phone")
    category: str = Field(default="General", description="Support category")


class AgentProcessResponse(BaseModel):
    """Response from agent processing"""
    success: bool
    ticket_id: Optional[str]
    response: str
    response_sent: bool
    escalation_required: bool
    sentiment_score: float
    category: str


@router.get(
    "/info",
    summary="Get agent information",
    description="Get information about the AI agent capabilities"
)
async def get_agent_info():
    """Get agent information"""
    from agents.customer_agent import get_agent
    
    agent = get_agent()
    return agent.get_agent_info()


@router.post(
    "/process",
    response_model=Dict[str, Any],
    summary="Process customer message",
    description="Process a customer message using the AI agent workflow"
)
async def process_customer_message(request: AgentProcessRequest):
    """
    Process customer message using AI agent
    
    The agent will:
    1. Search knowledge base
    2. Get customer history
    3. Create ticket if new customer
    4. Generate AI response
    5. Send response via channel
    6. Handle escalation if needed
    
    - **customer_message**: Customer's message
    - **customer_email**: Customer email address
    - **channel**: Communication channel (email/whatsapp/webform)
    - **customer_name**: Optional customer name
    - **customer_phone**: Optional phone number
    - **category**: Support category
    """
    from agents.customer_agent import get_agent
    
    agent = get_agent()
    
    result = await agent.process_message(
        customer_message=request.customer_message,
        customer_email=request.customer_email,
        channel=request.channel,
        customer_name=request.customer_name,
        customer_phone=request.customer_phone,
        category=request.category
    )
    
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("error", "Unknown error")
        )
    
    return result


@router.get(
    "/tools",
    summary="Get agent tools",
    description="Get list of tools available to the AI agent"
)
async def get_agent_tools():
    """Get agent tools"""
    from mcp_server import mcp_server
    
    return {
        "tools": mcp_server.get_tools_schema()
    }
