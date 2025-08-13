"""
Leads API Routes

This module provides API endpoints for lead management.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/")
async def get_leads():
    """Get all leads"""
    try:
        # Mock data for now
        leads = [
            {
                "id": "1",
                "name": "Mark Benioff",
                "jobTitle": "CEO",
                "company": "Salesforce",
                "email": "mark@salesforce.com",
                "score": 92,
                "status": "analyzed",
                "industry": "Technology",
                "companySize": "Enterprise",
                "lastContact": "2025-08-10",
                "source": "Conference",
                "linkedinUrl": "",
                "companyWebsite": "",
                "useCase": ""
            },
            {
                "id": "2", 
                "name": "Satya Nadella",
                "jobTitle": "CEO",
                "company": "Microsoft", 
                "email": "satya@microsoft.com",
                "score": 88,
                "status": "email_drafted",
                "industry": "Technology",
                "companySize": "Enterprise",
                "lastContact": "2025-08-09",
                "source": "LinkedIn",
                "linkedinUrl": "",
                "companyWebsite": "",
                "useCase": ""
            }
        ]
        return {"leads": leads, "total": len(leads)}
    except Exception as e:
        logger.error(f"Error getting leads: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def create_lead(lead_data: Dict[str, Any]):
    """Create a new lead"""
    try:
        logger.info(f"Creating lead with data: {lead_data}")
        
        # Mock implementation - return the lead data with an ID
        import uuid
        lead_id = str(uuid.uuid4())
        
        created_lead = {
            "id": lead_id,
            "name": lead_data.get("name", ""),
            "jobTitle": lead_data.get("jobTitle", ""),
            "company": lead_data.get("company", ""),
            "email": lead_data.get("email", ""),
            "linkedinUrl": lead_data.get("linkedinUrl", ""),
            "companyWebsite": lead_data.get("companyWebsite", ""),
            "useCase": lead_data.get("useCase", ""),
            "source": lead_data.get("source", "Manual Entry"),
            "score": lead_data.get("score", 0),
            "status": lead_data.get("status", "new"),
            "industry": lead_data.get("industry", "Technology"),
            "companySize": lead_data.get("companySize", "Medium"),
            "lastContact": lead_data.get("lastContact", None)
        }
        
        logger.info(f"Created lead: {created_lead}")
        return created_lead
    except Exception as e:
        logger.error(f"Error creating lead: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/test")
async def test_endpoint():
    """Test endpoint to verify the router is working"""
    return {"message": "Leads router is working", "status": "ok"}

@router.get("/{lead_id}")
async def get_lead(lead_id: str):
    """Get a specific lead"""
    try:
        # Mock implementation
        return {"id": lead_id, "name": "Sample Lead", "status": "new"}
    except Exception as e:
        logger.error(f"Error getting lead {lead_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
