# backend/api/routes/drafts.py
"""
Draft management routes
"""

from typing import List, Optional, Dict, Any
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel

from .auth import get_current_user
from ...services.draft_service import DraftService
from ...services.analytics_service import AnalyticsService
from ...agents.tools.draft_tool import DraftTool

router = APIRouter()

# Initialize services
draft_service = DraftService()
analytics_service = AnalyticsService()


class DraftCreateRequest(BaseModel):
    email_id: str
    to: str
    subject: str
    body: str
    cc: Optional[str] = None
    bcc: Optional[str] = None
    thread_id: Optional[str] = None
    is_reply: bool = False


class DraftUpdateRequest(BaseModel):
    to: Optional[str] = None
    subject: Optional[str] = None
    body: Optional[str] = None
    cc: Optional[str] = None
    bcc: Optional[str] = None


class DraftResponse(BaseModel):
    id: str
    email_id: Optional[str]
    to: str
    subject: str
    body: str
    cc: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    status: str
    confidence_score: Optional[float]


@router.get("/", response_model=List[DraftResponse])
async def list_drafts(
    limit: int = 10,
    current_user: Dict = Depends(get_current_user)
):
    """
    List all email drafts
    """
    try:
        # Get drafts from Gmail
        gmail_drafts = DraftTool().list_drafts(max_results=limit)
        
        # Get additional metadata from database
        db_drafts = await draft_service.get_user_drafts(current_user["email"], limit)
        
        # Merge information
        drafts = []
        for gmail_draft in gmail_drafts.get("drafts", []):
            draft_data = {
                "id": gmail_draft["id"],
                "to": gmail_draft.get("to", ""),
                "subject": gmail_draft.get("subject", ""),
                "body": gmail_draft.get("snippet", ""),
                "status": "draft",
                "created_at": datetime.now()
            }
            
            # Add database metadata if available
            db_draft = next((d for d in db_drafts if d["gmail_id"] == gmail_draft["id"]), None)
            if db_draft:
                draft_data.update(db_draft)
            
            drafts.append(DraftResponse(**draft_data))
        
        return drafts
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list drafts: {str(e)}")


@router.post("/", response_model=DraftResponse)
async def create_draft(
    request: DraftCreateRequest,
    current_user: Dict = Depends(get_current_user)
):
    """
    Create a new email draft
    """
    try:
        # Create draft in Gmail
        result = DraftTool.create_draft(
            to=request.to,
            subject=request.subject,
            body=request.body,
            cc=request.cc,
            bcc=request.bcc,
            thread_id=request.thread_id,
            reply_to_id=request.email_id if request.is_reply else None
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("error"))
        
        # Save to database
        db_draft = await draft_service.save_draft({
            "gmail_id": result["draft_id"],
            "email_id": request.email_id,
            "to": request.to,
            "subject": request.subject,
            "body": request.body,
            "user_email": current_user["email"],
            "status": "draft"
        })
        
        # Track event
        await analytics_service.track_event(
            "draft_created",
            {
                "user": current_user["email"],
                "draft_id": result["draft_id"]
            }
        )
        
        return DraftResponse(
            id=result["draft_id"],
            email_id=request.email_id,
            to=request.to,
            subject=request.subject,
            body=request.body,
            cc=request.cc,
            created_at=datetime.now(),
            status="draft",
            confidence_score=None
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create draft: {str(e)}")


@router.put("/{draft_id}", response_model=DraftResponse)
async def update_draft(
    draft_id: str,
    request: DraftUpdateRequest,
    current_user: Dict = Depends(get_current_user)
):
    """
    Update an existing draft
    """
    try:
        # Update in Gmail
        tool = DraftTool()
        result = tool.update_draft(
            draft_id=draft_id,
            to=request.to,
            subject=request.subject,
            body=request.body,
            cc=request.cc
        )
        
        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("error"))
        
        # Update in database
        await draft_service.update_draft(draft_id, request.dict(exclude_unset=True))
        
        # Get updated draft
        updated_draft = await draft_service.get_draft(draft_id)
        
        return DraftResponse(**updated_draft)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update draft: {str(e)}")


@router.delete("/{draft_id}")
async def delete_draft(
    draft_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """
    Delete a draft
    """
    try:
        # Delete from Gmail
        tool = DraftTool()
        result = tool.delete_draft(draft_id)
        
        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("error"))
        
        # Delete from database
        await draft_service.delete_draft(draft_id)
        
        # Track event
        await analytics_service.track_event(
            "draft_deleted",
            {
                "user": current_user["email"],
                "draft_id": draft_id
            }
        )
        
        return {"message": "Draft deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete draft: {str(e)}")


@router.post("/{draft_id}/send")
async def send_draft(
    draft_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """
    Send a draft email
    """
    try:
        # Send via Gmail
        tool = DraftTool()
        result = tool.send_draft(draft_id)
        
        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("error"))
        
        # Update database status
        await draft_service.update_draft(draft_id, {"status": "sent", "sent_at": datetime.now()})
        
        # Track event
        await analytics_service.track_event(
            "draft_sent",
            {
                "user": current_user["email"],
                "draft_id": draft_id,
                "message_id": result.get("message_id")
            }
        )
        
        return {
            "message": "Draft sent successfully",
            "message_id": result.get("message_id")
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send draft: {str(e)}")


@router.get("/{draft_id}")
async def get_draft_details(
    draft_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """
    Get detailed information about a draft
    """
    try:
        # Get from database
        draft = await draft_service.get_draft(draft_id)
        
        if not draft:
            raise HTTPException(status_code=404, detail="Draft not found")
        
        # Verify ownership
        if draft.get("user_email") != current_user["email"]:
            raise HTTPException(status_code=403, detail="Access denied")
        
        return DraftResponse(**draft)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get draft: {str(e)}")


@router.post("/generate")
async def generate_draft_for_email(
    email_id: str,
    background_tasks: BackgroundTasks,
    current_user: Dict = Depends(get_current_user)
):
    """
    Generate a draft response for a specific email using AI
    """
    try:
        # Add to processing queue
        background_tasks.add_task(
            draft_service.generate_draft_for_email,
            email_id,
            current_user["email"]
        )
        
        return {
            "message": "Draft generation initiated",
            "email_id": email_id,
            "status": "processing"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate draft: {str(e)}")


@router.get("/stats/summary")
async def get_draft_statistics(
    current_user: Dict = Depends(get_current_user)
):
    """
    Get draft statistics for the user
    """
    try:
        stats = await draft_service.get_user_statistics(current_user["email"])
        
        return {
            "total_drafts": stats.get("total_drafts", 0),
            "sent_drafts": stats.get("sent_drafts", 0),
            "pending_drafts": stats.get("pending_drafts", 0),
            "average_confidence": stats.get("avg_confidence", 0),
            "approval_rate": stats.get("approval_rate", 0),
            "drafts_by_day": stats.get("by_day", {}),
            "average_edit_count": stats.get("avg_edits", 0)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get statistics: {str(e)}")