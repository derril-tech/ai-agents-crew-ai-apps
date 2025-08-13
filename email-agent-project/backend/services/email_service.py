# backend/services/email_service.py
"""
Email Service for managing email operations
"""

import json
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func

from ..database.connection import SessionLocal
from ..models.email import Email, EmailCategory
from ..agents.crews.email_filter_crew import EmailFilterCrew
from ..agents.tools.gmail_tool import GmailTool
from .queue_service import QueueService
from ..api.websockets.email_stream import broadcast_email_event

class EmailService:
    """Service for email-related operations"""
    
    def __init__(self):
        self.gmail_tool = GmailTool()
        self.email_crew = EmailFilterCrew()
        self.queue_service = QueueService()
    
    async def check_health(self) -> str:
        """Check database health"""
        try:
            db = SessionLocal()
            db.execute("SELECT 1")
            db.close()
            return "healthy"
        except Exception as e:
            return f"unhealthy: {str(e)}"
    
    async def get_email_by_gmail_id(self, gmail_id: str) -> Optional[Dict]:
        """Get email from database by Gmail ID"""
        db = SessionLocal()
        try:
            email = db.query(Email).filter(Email.gmail_id == gmail_id).first()
            if email:
                return email.to_dict()
            return None
        finally:
            db.close()
    
    async def categorize_emails(self, email_ids: List[str]) -> List[Dict]:
        """Categorize a batch of emails"""
        results = []
        
        # Fetch emails from Gmail
        emails = []
        for email_id in email_ids:
            email_data = self.gmail_tool.get_email_details(email_id)
            if email_data:
                emails.append(email_data)
        
        if not emails:
            return results
        
        # Process through CrewAI
        crew_result = self.email_crew.process_emails(emails)
        
        # Parse results and save to database
        if crew_result.get("success"):
            categorized = crew_result.get("tasks", {}).get("triage")
            
            if categorized:
                db = SessionLocal()
                try:
                    for email_data in json.loads(categorized) if isinstance(categorized, str) else categorized:
                        # Save to database
                        email = Email(
                            gmail_id=email_data["id"],
                            thread_id=email_data["threadId"],
                            sender_email=email_data["sender"],
                            subject=email_data["subject"],
                            category=email_data["category"],
                            priority=email_data["priority"],
                            sentiment=email_data.get("sentiment"),
                            confidence_score=email_data.get("confidence"),
                            processed_at=datetime.now()
                        )
                        db.merge(email)
                        results.append(email_data)
                    
                    db.commit()
                    
                    # Broadcast categorization complete
                    await broadcast_email_event("categorization_complete", {
                        "count": len(results),
                        "email_ids": email_ids
                    })
                    
                finally:
                    db.close()
        
        return results
    
    async def process_categorization_queue(self):
        """Process emails in categorization queue"""
        while True:
            email_id = await self.queue_service.get_from_queue("categorize")
            if not email_id:
                break
            
            try:
                await self.categorize_emails([email_id])
            except Exception as e:
                print(f"Error categorizing {email_id}: {e}")
                await self.queue_service.add_to_error_queue("categorize", email_id, str(e))
    
    async def process_email_batch(self, email_ids: List[str]):
        """Process a batch of emails through the full pipeline"""
        # Fetch email details
        emails = []
        for email_id in email_ids:
            email_data = self.gmail_tool.get_email_details(email_id)
            if email_data:
                emails.append(email_data)
        
        if not emails:
            return
        
        # Process through CrewAI
        result = self.email_crew.process_emails(emails)
        
        # Save results
        if result.get("success"):
            db = SessionLocal()
            try:
                # Save categorization, context, and drafts
                for task_name, task_data in result.get("tasks", {}).items():
                    if task_data:
                        # Process based on task type
                        if task_name == "drafts" and task_data:
                            await self._save_drafts(task_data, db)
                
                db.commit()
                
                # Broadcast completion
                await broadcast_email_event("batch_processing_complete", {
                    "count": len(email_ids),
                    "email_ids": email_ids
                })
                
            finally:
                db.close()
    
    async def _save_drafts(self, drafts_data: Any, db: Session):
        """Save generated drafts"""
        from ..models.draft import Draft
        
        drafts = json.loads(drafts_data) if isinstance(drafts_data, str) else drafts_data
        
        for draft_data in drafts:
            draft = Draft(
                email_id=draft_data["id"],
                draft_content=draft_data["draft"]["body"],
                subject=draft_data["draft"]["subject"],
                confidence_score=draft_data["draft"].get("confidence_score"),
                created_at=datetime.now()
            )
            db.add(draft)
    
    async def update_email_status(self, email_id: str, status: str):
        """Update email status in database"""
        db = SessionLocal()
        try:
            email = db.query(Email).filter(Email.gmail_id == email_id).first()
            if email:
                email.status = status
                email.updated_at = datetime.now()
                db.commit()
        finally:
            db.close()
    
    async def get_statistics(self, user_email: str) -> Dict:
        """Get email processing statistics"""
        db = SessionLocal()
        try:
            # Get counts by category
            category_counts = db.query(
                Email.category,
                func.count(Email.id)
            ).group_by(Email.category).all()
            
            # Get counts by priority
            priority_counts = db.query(
                Email.priority,
                func.count(Email.id)
            ).group_by(Email.priority).all()
            
            # Get today's processed count
            today = datetime.now().date()
            today_count = db.query(func.count(Email.id)).filter(
                func.date(Email.processed_at) == today
            ).scalar()
            
            # Get this week's count
            week_ago = datetime.now() - timedelta(days=7)
            week_count = db.query(func.count(Email.id)).filter(
                Email.processed_at >= week_ago
            ).scalar()
            
            return {
                "total_processed": db.query(func.count(Email.id)).scalar(),
                "by_category": dict(category_counts),
                "by_priority": dict(priority_counts),
                "today_processed": today_count or 0,
                "week_processed": week_count or 0
            }
            
        finally:
            db.close()
    
    async def cleanup(self):
        """Cleanup service resources"""
        # Close any open connections
        pass