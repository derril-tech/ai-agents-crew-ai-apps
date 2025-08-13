# backend/services/draft_service.py
"""
Draft Service for managing email drafts
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy import func

from ..database.connection import SessionLocal
from ..models.draft import Draft
from ..models.email import Email
from ..agents.crews.email_filter_crew import EmailFilterCrew
from ..agents.tools.gmail_tool import GmailTool
from ..api.websockets.email_stream import broadcast_draft_event

class DraftService:
    """Service for draft management"""
    
    def __init__(self):
        self.gmail_tool = GmailTool()
        self.email_crew = EmailFilterCrew()
    
    async def get_user_drafts(self, user_email: str, limit: int = 10) -> List[Dict]:
        """Get drafts for a user"""
        db = SessionLocal()
        try:
            drafts = db.query(Draft).filter(
                Draft.user_email == user_email,
                Draft.status == "draft"
            ).order_by(
                Draft.created_at.desc()
            ).limit(limit).all()
            
            return [draft.to_dict() for draft in drafts]
            
        finally:
            db.close()
    
    async def save_draft(self, draft_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save draft to database"""
        db = SessionLocal()
        try:
            draft = Draft(
                gmail_draft_id=draft_data.get("gmail_id"),
                email_id=draft_data.get("email_id"),
                to_email=draft_data.get("to"),
                subject=draft_data.get("subject"),
                body=draft_data.get("body"),
                user_email=draft_data.get("user_email"),
                status="draft",
                created_at=datetime.now()
            )
            
            db.add(draft)
            db.commit()
            db.refresh(draft)
            
            # Broadcast event
            await broadcast_draft_event("draft_created", {
                "draft_id": str(draft.id),
                "email_id": draft.email_id
            })
            
            return draft.to_dict()
            
        finally:
            db.close()
    
    async def update_draft(self, draft_id: str, updates: Dict[str, Any]):
        """Update draft in database"""
        db = SessionLocal()
        try:
            draft = db.query(Draft).filter(Draft.gmail_draft_id == draft_id).first()
            
            if draft:
                for key, value in updates.items():
                    if hasattr(draft, key):
                        setattr(draft, key, value)
                
                draft.updated_at = datetime.now()
                db.commit()
                
                # Broadcast event
                await broadcast_draft_event("draft_updated", {
                    "draft_id": draft_id,
                    "updates": list(updates.keys())
                })
            
        finally:
            db.close()
    
    async def delete_draft(self, draft_id: str):
        """Delete draft from database"""
        db = SessionLocal()
        try:
            draft = db.query(Draft).filter(Draft.gmail_draft_id == draft_id).first()
            
            if draft:
                draft.status = "discarded"
                draft.updated_at = datetime.now()
                db.commit()
                
                # Broadcast event
                await broadcast_draft_event("draft_deleted", {
                    "draft_id": draft_id
                })
            
        finally:
            db.close()
    
    async def get_draft(self, draft_id: str) -> Optional[Dict]:
        """Get single draft"""
        db = SessionLocal()
        try:
            draft = db.query(Draft).filter(
                Draft.gmail_draft_id == draft_id
            ).first()
            
            if draft:
                return draft.to_dict()
            return None
            
        finally:
            db.close()
    
    async def generate_draft_for_email(self, email_id: str, user_email: str):
        """Generate draft for specific email using AI"""
        try:
            # Get email details
            email_data = self.gmail_tool.get_email_details(email_id)
            
            if not email_data:
                return
            
            # Process through CrewAI
            result = self.email_crew.process_emails([email_data])
            
            if result.get("success"):
                drafts_data = result.get("tasks", {}).get("drafts")
                
                if drafts_data:
                    # Parse and save draft
                    drafts = json.loads(drafts_data) if isinstance(drafts_data, str) else drafts_data
                    
                    for draft_info in drafts:
                        if draft_info.get("id") == email_id:
                            # Create Gmail draft
                            from ..agents.tools.draft_tool import DraftTool
                            
                            gmail_result = DraftTool.create_draft(
                                to=email_data["sender"],
                                subject=draft_info["draft"]["subject"],
                                body=draft_info["draft"]["body"],
                                thread_id=email_data.get("threadId")
                            )
                            
                            if gmail_result.get("success"):
                                # Save to database
                                await self.save_draft({
                                    "gmail_id": gmail_result["draft_id"],
                                    "email_id": email_id,
                                    "to": email_data["sender"],
                                    "subject": draft_info["draft"]["subject"],
                                    "body": draft_info["draft"]["body"],
                                    "user_email": user_email,
                                    "confidence_score": draft_info["draft"].get("confidence_score")
                                })
                            
                            # Broadcast completion
                            await broadcast_draft_event("draft_generated", {
                                "email_id": email_id,
                                "draft_id": gmail_result.get("draft_id")
                            })
            
        except Exception as e:
            print(f"Error generating draft: {e}")
            await broadcast_draft_event("draft_generation_failed", {
                "email_id": email_id,
                "error": str(e)
            })
    
    async def get_user_statistics(self, user_email: str) -> Dict[str, Any]:
        """Get draft statistics for user"""
        db = SessionLocal()
        try:
            # Total drafts
            total = db.query(func.count(Draft.id)).filter(
                Draft.user_email == user_email
            ).scalar()
            
            # Sent drafts
            sent = db.query(func.count(Draft.id)).filter(
                Draft.user_email == user_email,
                Draft.status == "sent"
            ).scalar()
            
            # Pending drafts
            pending = db.query(func.count(Draft.id)).filter(
                Draft.user_email == user_email,
                Draft.status == "draft"
            ).scalar()
            
            # Average confidence
            avg_confidence = db.query(func.avg(Draft.confidence_score)).filter(
                Draft.user_email == user_email,
                Draft.confidence_score.isnot(None)
            ).scalar()
            
            # Drafts by day (last 7 days)
            by_day = {}
            for i in range(7):
                day = (datetime.now() - timedelta(days=i)).date()
                count = db.query(func.count(Draft.id)).filter(
                    Draft.user_email == user_email,
                    func.date(Draft.created_at) == day
                ).scalar()
                by_day[day.isoformat()] = count
            
            return {
                "total_drafts": total or 0,
                "sent_drafts": sent or 0,
                "pending_drafts": pending or 0,
                "avg_confidence": float(avg_confidence) if avg_confidence else 0,
                "approval_rate": (sent / total * 100) if total > 0 else 0,
                "by_day": by_day
            }
            
        finally:
            db.close()