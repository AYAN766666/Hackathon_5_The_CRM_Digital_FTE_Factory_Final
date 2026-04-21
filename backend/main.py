"""
Customer Success FTE - Multi-Channel AI Support System
Main FastAPI Application
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import sys
import traceback

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import init_db
from routes import webform, email, whatsapp, mcp, agent, inbound_email, inbound_whatsapp, analytics
from config import get_cors_origins, settings
from services.kafka_producer import initialize_kafka, shutdown_kafka


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler with proper error handling"""
    # Startup: Initialize database and Kafka with error handling
    try:
        await init_db()
        print("[OK] Database initialized successfully")
    except Exception as e:
        error_msg = str(e)
        print(f"[ERROR] Database initialization failed: {error_msg}")
        
        # Handle DNS/connection errors
        if "getaddrinfo" in error_msg or "Name or service not known" in error_msg:
            print("\n[ERROR] CONNECTION ERROR: Cannot resolve database hostname")
            print("   Please check:")
            print("   1. Your DATABASE_URL in .env file is correct")
            print("   2. You have an active internet connection")
            print("   3. The database server is accessible")
            print(f"   Current DATABASE_URL: {settings.database_url[:50]}...")
        elif "connection refused" in error_msg.lower():
            print("\n[ERROR] CONNECTION ERROR: Database refused connection")
            print("   Please check:")
            print("   1. Database server is running")
            print("   2. Database port is accessible")
            print("   3. Firewall settings allow connections")
        elif "authentication" in error_msg.lower() or "password" in error_msg.lower():
            print("\n[ERROR] AUTHENTICATION ERROR: Database login failed")
            print("   Please check:")
            print("   1. DATABASE_URL username and password are correct")
            print("   2. Database user has proper permissions")
        else:
            print(f"\n[ERROR] Database error details: {error_msg}")
        
        # Store error for health check
        app.state.db_error = error_msg
    
    try:
        await initialize_kafka()
        print("[OK] Kafka initialized successfully")
    except Exception as e:
        error_msg = str(e)
        print(f"[WARN] Kafka initialization failed: {error_msg}")
        print("   Kafka is optional - continuing without it")
        app.state.kafka_error = error_msg

    # Initialize WhatsApp agent in background (deferred - don't block startup)
    print("[INFO] WhatsApp Agent will be initialized on first use (non-blocking)")
    # Don't start WhatsApp agent during app startup - defer to first request

    yield
    # Shutdown: cleanup
    await shutdown_kafka()

    # Stop WhatsApp agent
    try:
        from services.whatsapp_agent import whatsapp_agent
        if whatsapp_agent:
            await whatsapp_agent.stop()
    except:
        pass


async def init_whatsapp_background():
    """Initialize WhatsApp agent in background"""
    try:
        # Add delay to let server start first
        import asyncio
        await asyncio.sleep(2)
        
        from services.whatsapp_agent import get_whatsapp_agent
        agent = await get_whatsapp_agent()
        if agent.is_connected:
            print("✅ WhatsApp Agent ready!")
        else:
            print("⏳ WhatsApp Agent starting... (scan QR code when browser opens)")
    except Exception as e:
        print(f"⚠️ WhatsApp Agent will start on first use: {e}")
        print("   This is normal - WhatsApp will initialize when needed")


app = FastAPI(
    title="Customer Success FTE API",
    description="Multi-Channel AI Support System - Email, WhatsApp, Web Form with MCP Server",
    version="2.0.0",
    lifespan=lifespan
)

# CORS Configuration - Allow ALL origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=False,  # Must be False when allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routes
app.include_router(webform.router, prefix="/support", tags=["Support"])
app.include_router(email.router, prefix="/email", tags=["Email"])
app.include_router(whatsapp.router, prefix="/whatsapp", tags=["WhatsApp"])
app.include_router(mcp.router, prefix="/mcp", tags=["MCP Server"])
app.include_router(agent.router, prefix="/agent", tags=["AI Agent"])
app.include_router(inbound_email.router, prefix="/email/inbound", tags=["Inbound Email"])
app.include_router(inbound_whatsapp.router, prefix="/whatsapp/inbound", tags=["Inbound WhatsApp"])
app.include_router(analytics.router, tags=["Analytics"])


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Customer Success FTE API",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check with error details"""
    from services.kafka_producer import kafka_producer
    from fastapi import FastAPI
    
    # Get app instance to check for errors
    app = FastAPI()
    
    db_status = "connected"
    db_error = None
    kafka_status = kafka_producer.is_connected
    kafka_error = None
    
    # Check for stored errors from lifespan
    try:
        # Access global app state for errors
        from main import app as main_app
        if hasattr(main_app.state, 'db_error') and main_app.state.db_error:
            db_status = "disconnected"
            db_error = str(main_app.state.db_error)
        if hasattr(main_app.state, 'kafka_error') and main_app.state.kafka_error:
            kafka_status = False
            kafka_error = str(main_app.state.kafka_error)
    except:
        pass

    return {
        "status": "healthy" if db_status == "connected" else "degraded",
        "database": {
            "status": db_status,
            "error": db_error
        } if db_error else db_status,
        "ai_service": "ready",
        "kafka": {
            "status": "connected" if kafka_status else "disconnected",
            "error": kafka_error,
            "note": "Kafka is optional - system works without it"
        } if kafka_error else ("connected" if kafka_status else "disconnected"),
        "mcp_server": "ready",
        "help": {
            "database_error": "Check your DATABASE_URL in .env file if database is disconnected"
        } if db_error else None
    }


# Global Exception Handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Handle 404 errors"""
    return JSONResponse(
        status_code=404,
        content={
            "status": "error",
            "error": {
                "code": "NOT_FOUND",
                "message": "The requested resource was not found",
                "path": str(request.url.path),
                "hint": "Please check the URL and try again"
            }
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    error_messages = {
        400: "Bad request - please check your input",
        401: "Unauthorized - please log in",
        403: "Forbidden - you don't have permission",
        404: "Resource not found",
        405: "Method not allowed",
        408: "Request timeout",
        422: "Invalid input - please check the data format",
        429: "Too many requests - please slow down",
        500: "Internal server error",
        502: "Bad gateway",
        503: "Service temporarily unavailable",
    }
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "error": {
                "code": f"HTTP_{exc.status_code}",
                "message": exc.detail or error_messages.get(exc.status_code, "An error occurred"),
                "path": str(request.url.path),
            }
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions"""
    # Log the error for debugging
    print(f"❌ Error: {str(exc)}")
    print(traceback.format_exc())
    
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "Something went wrong on our end. We're working on it!",
                "path": str(request.url.path),
                "hint": "Please try again later or contact support if the issue persists"
            }
        }
    )
