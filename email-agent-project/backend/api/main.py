# FastAPI app entry
# backend/api/main.py
"""
FastAPI Main Application
Email Agent Backend Server
"""

import os
import logging
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from dotenv import load_dotenv

# Import routers
from .routes import auth, emails, agents, drafts
from .middleware.logging import LoggingMiddleware
from .middleware.auth import AuthMiddleware
from .websockets.email_stream import websocket_endpoint

# Import services
from ..services.email_service import EmailService
from ..services.queue_service import QueueService
from ..services.analytics_service import AnalyticsService
from ..database.connection import engine, Base

# Import background tasks
from ..services.background_tasks import start_background_tasks

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize services
email_service = EmailService()
queue_service = QueueService()
analytics_service = AnalyticsService()

# Sentry initialization (Phase 2)
if os.getenv("SENTRY_DSN"):
    import sentry_sdk
    from sentry_sdk.integrations.fastapi import FastApiIntegration
    
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        integrations=[FastApiIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=True,
        environment=os.getenv("APP_ENV", "development")
    )
    logger.info("Sentry initialized")

# PostHog initialization (Phase 2)
if os.getenv("POSTHOG_API_KEY"):
    from posthog import Posthog
    
    posthog = Posthog(
        project_api_key=os.getenv("POSTHOG_API_KEY"),
        host=os.getenv("POSTHOG_HOST", "https://eu.i.posthog.com")
    )
    logger.info("PostHog analytics initialized")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle
    """
    # Startup
    logger.info("🚀 Starting Email Agent Backend...")
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created/verified")
    
    # Initialize Redis connection
    await queue_service.initialize()
    logger.info("Redis connection established")
    
    # Start background tasks
    await start_background_tasks()
    logger.info("Background tasks started")
    
    # Track startup event
    if 'posthog' in globals():
        posthog.capture("server_started", properties={
            "environment": os.getenv("APP_ENV", "development"),
            "version": "0.1.0"
        })
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Email Agent Backend...")
    
    # Cleanup
    await queue_service.cleanup()
    await email_service.cleanup()
    
    # Track shutdown event
    if 'posthog' in globals():
        posthog.capture("server_stopped")
    
    logger.info("Cleanup completed")


# Create FastAPI app
app = FastAPI(
    title="Email Agent API",
    description="AI-powered email management system",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(AuthMiddleware)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(emails.router, prefix="/api/emails", tags=["Emails"])
app.include_router(agents.router, prefix="/api/agents", tags=["Agents"])
app.include_router(drafts.router, prefix="/api/drafts", tags=["Drafts"])

# WebSocket endpoint
app.add_api_websocket_route("/ws/emails", websocket_endpoint)

# Static files (for later when we have frontend build)
if os.path.exists("../frontend/out"):
    app.mount("/", StaticFiles(directory="../frontend/out", html=True), name="static")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Email Agent API",
        "version": "0.1.0",
        "status": "operational",
        "docs": "/api/docs"
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check database
        db_status = await email_service.check_health()
        
        # Check Redis
        redis_status = await queue_service.check_health()
        
        # Check agent status
        agent_status = "operational"  # TODO: Implement actual check
        
        return {
            "status": "healthy",
            "services": {
                "database": db_status,
                "redis": redis_status,
                "agents": agent_status
            },
            "timestamp": os.popen('date').read().strip()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e)
            }
        )


@app.get("/api/metrics")
async def metrics():
    """Get system metrics"""
    metrics_data = await analytics_service.get_metrics()
    return metrics_data


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Handle 404 errors"""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not found",
            "path": str(request.url)
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """Handle 500 errors"""
    logger.error(f"Internal error: {exc}")
    
    # Report to Sentry if configured
    if 'sentry_sdk' in globals():
        sentry_sdk.capture_exception(exc)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred"
        }
    )


# Development/Debug endpoints
if os.getenv("APP_ENV") == "development":
    @app.get("/api/debug/config")
    async def debug_config():
        """Show current configuration (development only)"""
        return {
            "environment": os.getenv("APP_ENV"),
            "email": os.getenv("MY_EMAIL"),
            "check_interval": os.getenv("AGENT_CHECK_INTERVAL"),
            "batch_size": os.getenv("AGENT_BATCH_SIZE"),
            "cors_origins": os.getenv("CORS_ORIGINS"),
            "services": {
                "openai": bool(os.getenv("OPENAI_API_KEY")),
                "google": bool(os.getenv("GOOGLE_API_KEY")),
                "serper": bool(os.getenv("SERPER_API_KEY")),
                "tavily": bool(os.getenv("TAVILY_API_KEY")),
                "sentry": bool(os.getenv("SENTRY_DSN")),
                "posthog": bool(os.getenv("POSTHOG_API_KEY"))
            }
        }
    
    @app.get("/api/debug/sentry")
    async def trigger_sentry_error():
        """Trigger a test error for Sentry (development only)"""
        division_by_zero = 1 / 0


def start_server():
    """Start the FastAPI server"""
    uvicorn.run(
        "backend.api.main:app",
        host="0.0.0.0",
        port=int(os.getenv("API_PORT", 8000)),
        reload=os.getenv("APP_ENV") == "development",
        log_level=os.getenv("LOG_LEVEL", "info").lower()
    )


if __name__ == "__main__":
    start_server()