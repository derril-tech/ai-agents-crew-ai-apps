# backend/api/routes/emails.py
"""
Email management routes
"""

import os
from typing import List, Optional, Dict, Any
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks
from pydantic import BaseModel, EmailStr

from .auth import get_current_user
from ...services.email_service import EmailService
from ...services.queue_service import QueueService
from ...services.analytics_service import AnalyticsService
from ...agents.tools.gmail_tool import GmailTool

router = APIRouter()

# Initialize services
email_service = EmailService()
queue_service = QueueService()
analytics_service = AnalyticsService()
gmail_tool = GmailTool()


class EmailResponse(BaseModel):
    id: str
    thread_id: str
    sender: str
    to: str
    subject: str
    snippet: str
    body: Optional[str] = None
    date: str
    labels: List[str]
    is_unread: bool
    is_important: bool
    has_attachments: bool
    category: Optional[str] = None
    priority: Optional[int] = None


class EmailCategorizeRequest(BaseModel):
    email_ids: List[str]
    process_immediately: bool = False


class EmailQueueResponse(BaseModel):
    queue_size: int
    processing: int
    processed: int
    emails: List[EmailResponse]


class EmailSearchRequest(BaseModel):
    query: str
    max_results: int = 10
    include_spam: bool = False


@router.get("/unread", response_model=List[EmailResponse])
async def get_unread_emails(
    max_results: int = Query(10, ge=1, le=100),
    current_user: Dict = Depends(get_current_user)
):
    """
    Fetch unread emails from Gmail
    """
    try:
        emails = gmail_tool.get_unread_emails(max_results=max_results)
        
        # Track analytics
        await analytics_service.track_event(
            "emails_fetched",
            {
                "user": current_user["email"],
                "count": len(emails)
            }
        )
        
        return [EmailResponse(**email) for email in emails]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch emails: {str(e)}")


@router.get("/thread/{thread_id}")
async def get_email_thread(
    thread_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """
    Get all messages in an email thread
    """
    try:
        thread = gmail_tool.get_email_thread(thread_id)
        
        if "error" in thread:
            raise HTTPException(status_code=404, detail=thread["error"])
        
        return thread
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch thread: {str(e)}")


@router.get("/{email_id}")
async def get_email_details(
    email_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """
    Get detailed information about a specific email
    """
    try:
        email = gmail_tool.get_email_details(email_id)
        
        if not email:
            raise HTTPException(status_code=404, detail="Email not found")
        
        # Get from database if we have additional metadata
        db_email = await email_service.get_email_by_gmail_id(email_id)
        if db_email:
            email.update(db_email)
        
        return EmailResponse(**email)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch email: {str(e)}")


@router.post("/categorize")
async def categorize_emails(
    request: EmailCategorizeRequest,
    background_tasks: BackgroundTasks,
    current_user: Dict = Depends(get_current_user)
):
    """
    Trigger categorization for specific emails
    """
    try:
        if request.process_immediately:
            # Process immediately
            results = await email_service.categorize_emails(request.email_ids)
            return {
                "status": "completed",
                "results": results
            }
        else:
            # Add to queue for background processing
            for email_id in request.email_ids:
                await queue_service.add_to_queue("categorize", email_id)
            
            background_tasks.add_task(
                email_service.process_categorization_queue
            )
            
            return {
                "status": "queued",
                "message": f"{len(request.email_ids)} emails queued for categorization"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Categorization failed: {str(e)}")


@router.get("/queue", response_model=EmailQueueResponse)
async def get_email_queue(
    current_user: Dict = Depends(get_current_user)
):
    """
    Get current email processing queue status
    """
    try:
        queue_stats = await queue_service.get_queue_stats()
        queued_emails = await queue_service.get_queued_emails()
        
        return EmailQueueResponse(
            queue_size=queue_stats["total"],
            processing=queue_stats["processing"],
            processed=queue_stats["processed"],
            emails=[EmailResponse(**email) for email in queued_emails]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get queue: {str(e)}")


@router.post("/search")
async def search_emails(
    request: EmailSearchRequest,
    current_user: Dict = Depends(get_current_user)
):
    """
    Search emails using Gmail search syntax
    """
    try:
        # Enhance query if needed
        query = request.query
        if not request.include_spam:
            query += " -in:spam"
        
        emails = gmail_tool.search_emails(query, max_results=request.max_results)
        
        # Track search
        await analytics_service.track_event(
            "email_search",
            {
                "user": current_user["email"],
                "query": request.query,
                "results": len(emails)
            }
        )
        
        return [EmailResponse(**email) for email in emails]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.post("/{email_id}/mark-read")
async def mark_email_as_read(
    email_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """
    Mark an email as read
    """
    try:
        success = gmail_tool.mark_as_read(email_id)
        
        if success:
            # Update in database
            await email_service.update_email_status(email_id, "read")
            
            return {"message": "Email marked as read"}
        else:
            raise HTTPException(status_code=500, detail="Failed to mark as read")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Operation failed: {str(e)}")


@router.get("/stats/summary")
async def get_email_statistics(
    current_user: Dict = Depends(get_current_user)
):
    """
    Get email processing statistics
    """
    try:
        stats = await email_service.get_statistics(current_user["email"])
        
        return {
            "total_processed": stats.get("total_processed", 0),
            "by_category": stats.get("by_category", {}),
            "by_priority": stats.get("by_priority", {}),
            "average_response_time": stats.get("avg_response_time", "N/A"),
            "today_processed": stats.get("today_processed", 0),
            "this_week_processed": stats.get("week_processed", 0)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")


@router.post("/batch-process")
async def batch_process_emails(
    background_tasks: BackgroundTasks,
    current_user: Dict = Depends(get_current_user)
):
    """
    Trigger batch processing of all unread emails
    """
    try:
        # Get unread emails
        emails = gmail_tool.get_unread_emails(max_results=50)
        
        if not emails:
            return {
                "message": "No unread emails to process",
                "count": 0
            }
        
        # Add to processing queue
        for email in emails:
            await queue_service.add_to_queue("process", email["id"])
        
        # Start background processing
        background_tasks.add_task(
            email_service.process_email_batch,
            [e["id"] for e in emails]
        )
        
        return {
            "message": f"Batch processing started for {len(emails)} emails",
            "count": len(emails),
            "email_ids": [e["id"] for e in emails]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch processing failed: {str(e)}")