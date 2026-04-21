"""
MCP Routes - Expose MCP server tools via API
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import sys
import os

# Add parent path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from mcp_server import mcp_server, get_mcp_server

router = APIRouter(tags=["MCP"])


class ToolRequest(BaseModel):
    """Request to invoke an MCP tool"""
    tool_name: str = Field(..., description="Name of the tool to invoke")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Tool parameters")


class ToolResponse(BaseModel):
    """Response from MCP tool invocation"""
    tool_name: str
    success: bool
    result: Dict[str, Any]
    error: Optional[str] = None


@router.get(
    "/tools",
    summary="List available MCP tools",
    description="Get list of all available MCP tools"
)
async def list_tools():
    """List all available MCP tools"""
    return {
        "tools": mcp_server.list_tools(),
        "count": len(mcp_server.list_tools())
    }


@router.get(
    "/tools/schema",
    summary="Get MCP tools schema",
    description="Get OpenAI function calling schema for all MCP tools"
)
async def get_tools_schema():
    """Get tools schema for OpenAI function calling"""
    return {
        "tools": mcp_server.get_tools_schema()
    }


@router.get(
    "/tools/{tool_name}",
    summary="Get tool information",
    description="Get detailed information about a specific tool"
)
async def get_tool_info(tool_name: str):
    """Get information about a specific tool"""
    info = mcp_server.get_tool_info(tool_name)
    
    if not info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tool not found: {tool_name}"
        )
    
    return info


@router.post(
    "/invoke",
    response_model=ToolResponse,
    summary="Invoke MCP tool",
    description="Invoke an MCP tool with parameters"
)
async def invoke_tool(request: ToolRequest):
    """
    Invoke an MCP tool
    
    - **tool_name**: Name of the tool (search_knowledge_base, create_ticket, get_customer_history, send_response)
    - **parameters**: Tool parameters as key-value pairs
    """
    tool_name = request.tool_name
    
    if tool_name not in mcp_server.list_tools():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tool not found: {tool_name}. Available tools: {mcp_server.list_tools()}"
        )
    
    try:
        # Get tool function
        tool_func = mcp_server.tools[tool_name]
        
        # Check if function is async
        import inspect
        if inspect.iscoroutinefunction(tool_func):
            # Invoke async tool
            result = await tool_func(**request.parameters)
        else:
            # Invoke sync tool
            result = tool_func(**request.parameters)

        return ToolResponse(
            tool_name=tool_name,
            success=result.get("success", False),
            result=result,
            error=result.get("error")
        )
        
    except Exception as e:
        return ToolResponse(
            tool_name=tool_name,
            success=False,
            result={},
            error=str(e)
        )


# Specific tool endpoints for easier testing

@router.post(
    "/search",
    summary="Search knowledge base",
    description="Search the knowledge base for relevant articles"
)
async def search_kb(query: str, top_k: int = 3):
    """Search knowledge base"""
    result = mcp_server.search_knowledge_base(query, top_k)
    return result


@router.get(
    "/knowledge-base/articles",
    summary="List knowledge base articles",
    description="Get list of all knowledge base articles"
)
async def list_kb_articles():
    """List all KB articles"""
    from services.knowledge_base_service import get_all_articles
    articles = get_all_articles()
    return {
        "articles": articles,
        "count": len(articles)
    }


@router.get(
    "/knowledge-base/articles/{article_name}",
    summary="Get knowledge base article",
    description="Get full content of a specific article"
)
async def get_kb_article(article_name: str):
    """Get KB article"""
    from services.knowledge_base_service import get_article
    content = get_article(article_name)
    
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article not found: {article_name}"
        )
    
    return {
        "article": article_name,
        "content": content
    }
