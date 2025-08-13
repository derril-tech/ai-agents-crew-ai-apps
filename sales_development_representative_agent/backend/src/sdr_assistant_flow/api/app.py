"""
FastAPI Backend for SDR Assistant Flow

This module provides REST API endpoints for the SDR Assistant application,
enabling frontend integration and external system connectivity.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from typing import List, Dict, Any, Optional
import asyncio
from datetime import datetime
import uuid

from src.sdr_assistant_flow.api.routes import leads, emails, analytics
from src.sdr_assistant_flow.api.models.api_models import (
    LeadAnalysisRequest,
    LeadAnalysisResponse,
    EmailGenerationRequest,
    EmailGenerationResponse,
    CampaignStatusResponse,
    BulkProcessRequest
)
from src.sdr_assistant_flow.flows.sdr_flow import SDRAssistantFlow, kickoff_flow
from src.sdr_assistant_flow.lead_types import LeadInput
from src.sdr_assistant_flow.utils.config import get_settings
from src.sdr_assistant_flow.utils.logger import get_logger
from src.sdr_assistant_flow.utils.database import DatabaseManager

logger = get_logger(__name__)
settings = get_settings()

# Global state management for active flows
active_flows: Dict[str, SDRAssistantFlow] = {}
flow_results: Dict[str, Dict[str, Any]] = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    logger.info("Starting SDR Assistant API...")
    
    # Initialize database
    db_manager = DatabaseManager()
    await db_manager.initialize()
    
    yield
    
    logger.info("Shutting down SDR Assistant API...")
    # Cleanup active flows
    active_flows.clear()
    flow_results.clear()

# Create FastAPI app
app = FastAPI(
    title="SDR Assistant API",
    description="AI-powered Sales Development Representative Assistant",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(leads.router, prefix="/api/leads", tags=["leads"])
app.include_router(emails.router, prefix="/api/emails", tags=["emails"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "SDR Assistant API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "operational",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_flows": len(active_flows),
        "cached_results": len(flow_results)
    }

@app.post("/api/analyze-lead", response_model=LeadAnalysisResponse)
async def analyze_single_lead(
    request: LeadAnalysisRequest,
    background_tasks: BackgroundTasks
):
    """
    Analyze a single lead for readiness and qualification
    
    This endpoint processes one lead through the analysis crew to determine
    their outreach readiness and generates insights for email creation.
    """
    try:
        session_id = str(uuid.uuid4())
        logger.info(f"Starting single lead analysis: {session_id}")
        
        # Convert request to LeadInput
        lead_input = LeadInput(**request.lead_data.model_dump())
        
        # Start flow in background
        def run_analysis():
            try:
                flow = kickoff_flow([lead_input])
                active_flows[session_id] = flow
                
                # Store results when complete
                results = flow.get_campaign_results()
                flow_results[session_id] = results
                
                # Clean up active flow
                if session_id in active_flows:
                    del active_flows[session_id]
                    
            except Exception as e:
                logger.error(f"Error in background analysis {session_id}: {str(e)}")
                flow_results[session_id] = {"error": str(e)}
        
        if request.async_processing:
            background_tasks.add_task(run_analysis)
            return LeadAnalysisResponse(
                session_id=session_id,
                status="processing",
                message="Lead analysis started. Check status endpoint for results."
            )
        else:
            # Synchronous processing
            run_analysis()
            results = flow_results.get(session_id, {})
            
            if "error" in results:
                raise HTTPException(status_code=500, detail=results["error"])
            
            return LeadAnalysisResponse(
                session_id=session_id,
                status="completed",
                message="Lead analysis completed successfully",
                results=results
            )
            
    except Exception as e:
        logger.error(f"Error analyzing lead: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-email", response_model=EmailGenerationResponse)
async def generate_email(
    request: EmailGenerationRequest,
    background_tasks: BackgroundTasks
):
    """
    Generate a personalized cold email for a lead
    
    This endpoint takes lead analysis data and generates a personalized
    outreach email using the email generation crew.
    """
    try:
        session_id = str(uuid.uuid4())
        logger.info(f"Starting email generation: {session_id}")
        
        # This would use the DraftColdEmailCrew directly
        # For now, return a mock response
        
        return EmailGenerationResponse(
            session_id=session_id,
            status="completed",
            message="Email generated successfully",
            email={
                "subject": f"AI Strategy Discussion for {request.company_name}",
                "body": "Personalized email content here...",
                "personalization_score": 0.85,
                "call_to_action": "Schedule a 15-minute call",
                "estimated_read_time": 25
            }
        )
        
    except Exception as e:
        logger.error(f"Error generating email: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/bulk-process", response_model=CampaignStatusResponse)
async def bulk_process_leads(
    request: BulkProcessRequest,
    background_tasks: BackgroundTasks
):
    """
    Process multiple leads in bulk
    
    This endpoint handles bulk lead processing, running the complete
    SDR flow for multiple leads simultaneously.
    """
    try:
        session_id = str(uuid.uuid4())
        logger.info(f"Starting bulk processing: {session_id} with {len(request.leads)} leads")
        
        # Convert request leads to LeadInput objects
        lead_inputs = [LeadInput(**lead.model_dump()) for lead in request.leads]
        
        def run_bulk_processing():
            try:
                flow = kickoff_flow(lead_inputs)
                active_flows[session_id] = flow
                
                # Store results when complete
                results = flow.get_campaign_results()
                flow_results[session_id] = results
                
                # Clean up active flow
                if session_id in active_flows:
                    del active_flows[session_id]
                    
            except Exception as e:
                logger.error(f"Error in bulk processing {session_id}: {str(e)}")
                flow_results[session_id] = {"error": str(e)}
        
        # Always process in background for bulk operations
        background_tasks.add_task(run_bulk_processing)
        
        return CampaignStatusResponse(
            session_id=session_id,
            status="processing",
            message=f"Bulk processing started for {len(lead_inputs)} leads",
            total_leads=len(lead_inputs),
            processed_leads=0,
            estimated_completion_time="5-10 minutes"
        )
        
    except Exception as e:
        logger.error(f"Error in bulk processing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/status/{session_id}", response_model=CampaignStatusResponse)
async def get_campaign_status(session_id: str):
    """
    Get the status of a campaign/flow session
    
    This endpoint allows clients to check the progress and results
    of ongoing or completed lead processing sessions.
    """
    try:
        # Check if flow is still active
        if session_id in active_flows:
            flow = active_flows[session_id]
            return CampaignStatusResponse(
                session_id=session_id,
                status="processing",
                message="Campaign is still processing",
                total_leads=len(flow.state.leads),
                processed_leads=len(flow.state.analyzed_leads),
                current_step="analyzing" if flow.state.analyzed_leads else "initializing"
            )
        
        # Check if results are available
        if session_id in flow_results:
            results = flow_results[session_id]
            
            if "error" in results:
                return CampaignStatusResponse(
                    session_id=session_id,
                    status="error",
                    message=f"Campaign failed: {results['error']}",
                    error=results["error"]
                )
            
            return CampaignStatusResponse(
                session_id=session_id,
                status="completed",
                message="Campaign completed successfully",
                total_leads=results.get("metrics", {}).get("total_leads", 0),
                processed_leads=results.get("leads_analyzed", 0),
                results=results
            )
        
        # Session not found
        raise HTTPException(status_code=404, detail="Session not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting campaign status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/results/{session_id}")
async def get_campaign_results(session_id: str):
    """
    Get detailed results for a completed campaign
    
    This endpoint returns comprehensive results including lead analysis,
    generated emails, and campaign metrics.
    """
    try:
        if session_id not in flow_results:
            raise HTTPException(status_code=404, detail="Results not found")
        
        results = flow_results[session_id]
        
        if "error" in results:
            raise HTTPException(status_code=500, detail=results["error"])
        
        return results
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting campaign results: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/session/{session_id}")
async def cleanup_session(session_id: str):
    """Clean up a session and its data"""
    try:
        cleaned_up = False
        
        if session_id in active_flows:
            del active_flows[session_id]
            cleaned_up = True
        
        if session_id in flow_results:
            del flow_results[session_id]
            cleaned_up = True
        
        if not cleaned_up:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return {"message": "Session cleaned up successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error cleaning up session: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sessions")
async def list_active_sessions():
    """List all active sessions"""
    try:
        sessions = []
        
        for session_id, flow in active_flows.items():
            sessions.append({
                "session_id": session_id,
                "status": "processing",
                "total_leads": len(flow.state.leads),
                "processed_leads": len(flow.state.analyzed_leads),
                "start_time": flow.state.start_time.isoformat()
            })
        
        for session_id, results in flow_results.items():
            if "error" not in results:
                sessions.append({
                    "session_id": session_id,
                    "status": "completed",
                    "total_leads": results.get("metrics", {}).get("total_leads", 0),
                    "processed_leads": results.get("leads_analyzed", 0),
                    "completion_time": results.get("processing_time", 0)
                })
        
        return {"sessions": sessions, "total_active": len(active_flows)}
        
    except Exception as e:
        logger.error(f"Error listing sessions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "timestamp": datetime.now().isoformat()}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "timestamp": datetime.now().isoformat()}
    )

# Development helper endpoints
@app.get("/api/sample-leads")
async def get_sample_leads():
    """Get sample lead data for testing"""
    return {
        "leads": [
            {
                "name": "Mark Benioff",
                "job_title": "CEO",
                "company": "Salesforce",
                "email": "mark@salesforce.com",
                "linkedin_url": "https://linkedin.com/in/benioff",
                "company_website": "https://salesforce.com",
                "use_case": "Exploring GenAI strategy for executive-level productivity"
            },
            {
                "name": "Satya Nadella",
                "job_title": "CEO", 
                "company": "Microsoft",
                "email": "satya@microsoft.com",
                "linkedin_url": "https://linkedin.com/in/satyanadella",
                "company_website": "https://microsoft.com",
                "use_case": "AI integration across enterprise products"
            }
        ]
    }

@app.get("/api/config")
async def get_api_config():
    """Get API configuration info"""
    return {
        "environment": settings.environment,
        "cors_origins": settings.cors_origins,
        "features": {
            "bulk_processing": True,
            "async_processing": True,
            "real_time_analytics": True,
            "email_templates": True,
            "lead_enrichment": True
        },
        "limits": {
            "max_leads_per_batch": 100,
            "max_concurrent_flows": 10,
            "session_timeout_hours": 24
        }
    }

def main():
    """Main function to run the API server"""
    import uvicorn
    
    uvicorn.run(
        "src.sdr_assistant_flow.api.app:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_level="info" if not settings.debug else "debug"
    )

if __name__ == "__main__":
    main()