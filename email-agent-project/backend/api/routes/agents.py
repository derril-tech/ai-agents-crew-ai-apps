# backend/api/routes/agents.py
"""
Agent management routes
"""

import os
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel

from .auth import get_current_user
from ...services.agent_service import AgentService
from ...services.analytics_service import AnalyticsService

router = APIRouter()

# Initialize services
agent_service = AgentService()
analytics_service = AnalyticsService()


class AgentStartRequest(BaseModel):
    interval_seconds: Optional[int] = None
    batch_size: Optional[int] = None
    auto_send_drafts: bool = False


class AgentConfigRequest(BaseModel):
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    model_preferences: Optional[Dict[str, str]] = None


class AgentTrainRequest(BaseModel):
    training_data: Optional[List[Dict]] = None
    use_historical: bool = True
    training_type: str = "fine_tune"  # or "few_shot"


@router.post("/start")
async def start_agent_processing(
    request: AgentStartRequest,
    background_tasks: BackgroundTasks,
    current_user: Dict = Depends(get_current_user)
):
    """
    Start the email processing agent
    """
    try:
        # Check if agent is already running
        if agent_service.is_running():
            return {
                "status": "already_running",
                "message": "Agent is already processing emails"
            }
        
        # Configure agent parameters
        config = {
            "interval": request.interval_seconds or int(os.getenv("AGENT_CHECK_INTERVAL", 180)),
            "batch_size": request.batch_size or int(os.getenv("AGENT_BATCH_SIZE", 10)),
            "auto_send": request.auto_send_drafts,
            "user": current_user["email"]
        }
        
        # Start agent in background
        background_tasks.add_task(agent_service.start_processing, config)
        
        # Track event
        await analytics_service.track_event(
            "agent_started",
            {
                "user": current_user["email"],
                "config": config
            }
        )
        
        return {
            "status": "started",
            "message": "Email processing agent started",
            "config": config
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start agent: {str(e)}")


@router.post("/stop")
async def stop_agent_processing(
    current_user: Dict = Depends(get_current_user)
):
    """
    Stop the email processing agent
    """
    try:
        if not agent_service.is_running():
            return {
                "status": "not_running",
                "message": "Agent is not currently running"
            }
        
        # Stop agent
        await agent_service.stop_processing()
        
        # Track event
        await analytics_service.track_event(
            "agent_stopped",
            {"user": current_user["email"]}
        )
        
        return {
            "status": "stopped",
            "message": "Email processing agent stopped"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to stop agent: {str(e)}")


@router.get("/status")
async def get_agent_status(
    current_user: Dict = Depends(get_current_user)
):
    """
    Get current agent status and statistics
    """
    try:
        status = await agent_service.get_status()
        
        return {
            "running": status["is_running"],
            "status": status["status"],
            "current_task": status.get("current_task"),
            "started_at": status.get("started_at"),
            "last_check": status.get("last_check"),
            "statistics": {
                "emails_processed": status.get("emails_processed", 0),
                "drafts_created": status.get("drafts_created", 0),
                "errors": status.get("error_count", 0),
                "uptime_seconds": status.get("uptime", 0)
            },
            "configuration": status.get("config", {}),
            "agents": {
                "triage": status.get("triage_status", "idle"),
                "context": status.get("context_status", "idle"),
                "strategist": status.get("strategist_status", "idle"),
                "composer": status.get("composer_status", "idle")
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get status: {str(e)}")


@router.post("/train")
async def train_agents(
    request: AgentTrainRequest,
    background_tasks: BackgroundTasks,
    current_user: Dict = Depends(get_current_user)
):
    """
    Train agents with custom data or historical patterns
    """
    try:
        # Prepare training configuration
        training_config = {
            "user": current_user["email"],
            "type": request.training_type,
            "use_historical": request.use_historical
        }
        
        if request.training_data:
            training_config["custom_data"] = request.training_data
        
        # Start training in background
        background_tasks.add_task(
            agent_service.train_agents,
            training_config
        )
        
        return {
            "status": "training_started",
            "message": "Agent training initiated",
            "config": training_config
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")


@router.post("/config")
async def update_agent_configuration(
    request: AgentConfigRequest,
    current_user: Dict = Depends(get_current_user)
):
    """
    Update agent configuration parameters
    """
    try:
        updated_config = {}
        
        if request.temperature is not None:
            updated_config["temperature"] = request.temperature
            os.environ["AGENT_TEMPERATURE"] = str(request.temperature)
        
        if request.max_tokens is not None:
            updated_config["max_tokens"] = request.max_tokens
            os.environ["AGENT_MAX_TOKENS"] = str(request.max_tokens)
        
        if request.model_preferences:
            updated_config["models"] = request.model_preferences
            # Update model preferences in agent service
            await agent_service.update_model_preferences(request.model_preferences)
        
        return {
            "message": "Agent configuration updated",
            "updated": updated_config
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Configuration update failed: {str(e)}")


@router.get("/performance")
async def get_agent_performance_metrics(
    current_user: Dict = Depends(get_current_user)
):
    """
    Get detailed agent performance metrics
    """
    try:
        metrics = await agent_service.get_performance_metrics()
        
        return {
            "response_times": {
                "average_ms": metrics.get("avg_response_time", 0),
                "p95_ms": metrics.get("p95_response_time", 0),
                "p99_ms": metrics.get("p99_response_time", 0)
            },
            "accuracy": {
                "categorization": metrics.get("categorization_accuracy", 0),
                "draft_approval_rate": metrics.get("draft_approval_rate", 0),
                "false_positive_rate": metrics.get("false_positive_rate", 0)
            },
            "throughput": {
                "emails_per_hour": metrics.get("emails_per_hour", 0),
                "drafts_per_hour": metrics.get("drafts_per_hour", 0)
            },
            "costs": {
                "total_tokens": metrics.get("total_tokens", 0),
                "estimated_cost_usd": metrics.get("estimated_cost", 0),
                "cost_per_email": metrics.get("cost_per_email", 0)
            },
            "model_usage": metrics.get("model_usage", {}),
            "error_rate": metrics.get("error_rate", 0)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get metrics: {str(e)}")


@router.post("/test")
async def test_agent_pipeline(
    current_user: Dict = Depends(get_current_user)
):
    """
    Test agent pipeline with a sample email
    """
    try:
        # Create test email
        test_email = {
            "id": "test_" + datetime.now().strftime("%Y%m%d_%H%M%S"),
            "threadId": "test_thread",
            "sender": "test@example.com",
            "subject": "Test Email for Agent Pipeline",
            "body": "This is a test email to verify the agent pipeline is working correctly. Please respond with confirmation.",
            "snippet": "This is a test email...",
            "labels": ["UNREAD"],
            "is_unread": True,
            "is_important": False,
            "has_attachments": False
        }
        
        # Process through pipeline
        result = await agent_service.process_single_email(test_email)
        
        return {
            "status": "success",
            "message": "Test completed successfully",
            "results": {
                "categorization": result.get("category"),
                "priority": result.get("priority"),
                "context": result.get("context"),
                "strategy": result.get("strategy"),
                "draft": result.get("draft")
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test failed: {str(e)}")


@router.get("/logs")
async def get_agent_logs(
    limit: int = 100,
    current_user: Dict = Depends(get_current_user)
):
    """
    Get recent agent processing logs
    """
    try:
        logs = await agent_service.get_recent_logs(limit)
        
        return {
            "count": len(logs),
            "logs": logs
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get logs: {str(e)}")