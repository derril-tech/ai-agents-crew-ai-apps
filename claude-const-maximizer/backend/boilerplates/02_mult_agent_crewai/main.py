"""
Multi-Agent CrewAI Backend Boilerplate
Main FastAPI application entry point
"""

import os
import logging
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from config.settings import get_settings
from config.database import engine, Base
from api.v1 import auth, users, projects, agents, tasks, workflows
from core.security import get_current_user
from utils.logger import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Global settings
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting Multi-Agent CrewAI Backend...")
    
    # Create database tables
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise
    
    # Initialize services
    try:
        # Initialize agent registry
        from services.agent_service import AgentService
        agent_service = AgentService()
        await agent_service.initialize_agents()
        logger.info("Agent service initialized successfully")
        
        # Initialize workflow templates
        from services.workflow_service import WorkflowService
        workflow_service = WorkflowService()
        await workflow_service.initialize_templates()
        logger.info("Workflow service initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        raise
    
    logger.info("Multi-Agent CrewAI Backend started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Multi-Agent CrewAI Backend...")
    
    # Cleanup resources
    try:
        await engine.dispose()
        logger.info("Database connections closed")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")


# Create FastAPI application
app = FastAPI(
    title="Multi-Agent CrewAI Backend",
    description="Backend API for multi-agent AI systems using CrewAI",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)


# Exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """Handle validation exceptions"""
    logger.error(f"Validation Error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"error": "Validation error", "details": exc.errors()}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"General Exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )


# Health check endpoint
@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Multi-Agent CrewAI Backend",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT
    }


# Include API routers
app.include_router(
    auth.router,
    prefix="/api/v1/auth",
    tags=["Authentication"]
)

app.include_router(
    users.router,
    prefix="/api/v1/users",
    tags=["Users"],
    dependencies=[Depends(get_current_user)]
)

app.include_router(
    projects.router,
    prefix="/api/v1/projects",
    tags=["Projects"],
    dependencies=[Depends(get_current_user)]
)

app.include_router(
    agents.router,
    prefix="/api/v1/agents",
    tags=["Agents"],
    dependencies=[Depends(get_current_user)]
)

app.include_router(
    tasks.router,
    prefix="/api/v1/tasks",
    tags=["Tasks"],
    dependencies=[Depends(get_current_user)]
)

app.include_router(
    workflows.router,
    prefix="/api/v1/workflows",
    tags=["Workflows"],
    dependencies=[Depends(get_current_user)]
)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Multi-Agent CrewAI Backend API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


# API info endpoint
@app.get("/api/info")
async def api_info():
    """API information endpoint"""
    return {
        "name": "Multi-Agent CrewAI Backend",
        "version": "1.0.0",
        "description": "Backend API for multi-agent AI systems using CrewAI",
        "features": [
            "Multi-agent orchestration",
            "Task management",
            "Workflow automation",
            "Real-time monitoring",
            "API integrations",
            "Security and authentication"
        ],
        "endpoints": {
            "authentication": "/api/v1/auth",
            "users": "/api/v1/users",
            "projects": "/api/v1/projects",
            "agents": "/api/v1/agents",
            "tasks": "/api/v1/tasks",
            "workflows": "/api/v1/workflows"
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
