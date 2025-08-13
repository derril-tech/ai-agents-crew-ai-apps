# backend/agents/flows/email_flow.py
"""
Email Processing Flow
Main orchestrator for the email agent system
"""

import os
import json
import time
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field

from crewai.flow.flow import Flow
from pydantic import BaseModel

from ..crews.email_filter_crew import EmailFilterCrew
from ..tools.gmail_tool import GmailTool


class EmailState(BaseModel):
    """State management for email processing flow"""
    emails: List[Dict[str, Any]] = []
    processed_ids: set = set()
    drafts: List[Dict[str, Any]] = []
    last_check: Optional[datetime] = None
    error_count: int = 0
    status: str = "idle"


class EmailProcessingFlow(Flow[EmailState]):
    """Main flow for email processing"""
    
    initial_state = EmailState
    
    def __init__(self):
        """Initialize the flow"""
        super().__init__()
        self.gmail_tool = GmailTool()
        self.email_crew = EmailFilterCrew()
        self.check_interval = int(os.getenv("AGENT_CHECK_INTERVAL", 180))
        self.batch_size = int(os.getenv("AGENT_BATCH_SIZE", 10))
        self.running = False
    
    async def check_emails(self) -> EmailState:
        """
        Check for new unread emails
        
        Returns:
            Updated state with new emails
        """
        print("📧 Checking for new emails...")
        self.state.status = "checking"
        
        try:
            # Get unread emails
            unread_emails = self.gmail_tool.get_unread_emails(max_results=self.batch_size)
            
            # Filter out already processed emails
            new_emails = [
                email for email in unread_emails 
                if email['id'] not in self.state.processed_ids
            ]
            
            if new_emails:
                print(f"📬 Found {len(new_emails)} new email(s)")
                self.state.emails = new_emails
                self.state.last_check = datetime.now()
            else:
                print("📭 No new emails")
                self.state.emails = []
            
            self.state.status = "idle"
            return self.state
            
        except Exception as e:
            print(f"❌ Error checking emails: {str(e)}")
            self.state.error_count += 1
            self.state.status = "error"
            return self.state
    
    async def process_emails(self) -> EmailState:
        """
        Process emails through the CrewAI agents
        
        Returns:
            Updated state with drafts
        """
        if not self.state.emails:
            print("⏭️ No emails to process")
            return self.state
        
        print(f"🤖 Processing {len(self.state.emails)} email(s)...")
        self.state.status = "processing"
        
        try:
            # Process emails through the crew
            result = self.email_crew.process_emails(
                self.state.emails,
                user_context={
                    "user_name": os.getenv("USER_NAME", "User"),
                    "user_company": os.getenv("USER_COMPANY", "Company"),
                    "user_role": os.getenv("USER_ROLE", "Professional")
                }
            )
            
            # Extract drafts from results
            if result.get("success") and result.get("tasks", {}).get("drafts"):
                drafts_data = result["tasks"]["drafts"]
                
                # Parse drafts if they're in JSON string format
                if isinstance(drafts_data, str):
                    try:
                        drafts_data = json.loads(drafts_data)
                    except json.JSONDecodeError:
                        print("⚠️ Could not parse drafts JSON")
                        drafts_data = []
                
                self.state.drafts = drafts_data if isinstance(drafts_data, list) else []
                
                # Mark emails as processed
                for email in self.state.emails:
                    self.state.processed_ids.add(email['id'])
                
                print(f"✅ Generated {len(self.state.drafts)} draft(s)")
            else:
                print("⚠️ No drafts generated")
            
            self.state.status = "idle"
            return self.state
            
        except Exception as e:
            print(f"❌ Error processing emails: {str(e)}")
            self.state.error_count += 1
            self.state.status = "error"
            return self.state
    
    async def save_drafts(self) -> EmailState:
        """
        Save drafts to Gmail
        
        Returns:
            Updated state
        """
        if not self.state.drafts:
            return self.state
        
        print(f"💾 Saving {len(self.state.drafts)} draft(s) to Gmail...")
        self.state.status = "saving"
        
        from ..tools.draft_tool import DraftTool
        
        saved_count = 0
        for draft in self.state.drafts:
            try:
                # Extract draft details
                email_id = draft.get("id")
                draft_data = draft.get("draft", {})
                
                # Find original email for reply context
                original_email = next(
                    (e for e in self.state.emails if e['id'] == email_id),
                    None
                )
                
                if original_email:
                    # Create Gmail draft
                    result = DraftTool.create_draft(
                        to=original_email['sender'],
                        subject=draft_data.get('subject', f"Re: {original_email['subject']}"),
                        body=draft_data.get('body', ''),
                        thread_id=original_email.get('threadId'),
                        reply_to_id=original_email.get('id')
                    )
                    
                    if result.get('success'):
                        saved_count += 1
                        print(f"✉️ Draft saved for: {original_email['sender']}")
                    else:
                        print(f"⚠️ Failed to save draft: {result.get('error')}")
            
            except Exception as e:
                print(f"⚠️ Error saving draft: {str(e)}")
        
        print(f"✅ Saved {saved_count} draft(s)")
        
        # Clear processed emails and drafts
        self.state.emails = []
        self.state.drafts = []
        self.state.status = "idle"
        
        return self.state
    
    async def run_cycle(self):
        """
        Run a single processing cycle
        """
        print(f"\n{'='*60}")
        print(f"🔄 Email Processing Cycle - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        # Check for new emails
        await self.check_emails()
        
        # Process if we have emails
        if self.state.emails:
            await self.process_emails()
            await self.save_drafts()
        
        # Log statistics
        print(f"\n📊 Statistics:")
        print(f"  • Processed emails: {len(self.state.processed_ids)}")
        print(f"  • Error count: {self.state.error_count}")
        print(f"  • Status: {self.state.status}")
    
    async def start(self):
        """
        Start the continuous email processing flow
        """
        print("🚀 Starting Email Processing Flow")
        print(f"⏰ Check interval: {self.check_interval} seconds")
        print(f"📦 Batch size: {self.batch_size} emails")
        print("Press Ctrl+C to stop\n")
        
        self.running = True
        
        try:
            while self.running:
                await self.run_cycle()
                
                print(f"\n⏳ Waiting {self.check_interval} seconds until next check...")
                await asyncio.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Stopping Email Processing Flow")
            self.running = False
        except Exception as e:
            print(f"\n❌ Fatal error: {str(e)}")
            self.running = False
    
    def stop(self):
        """Stop the flow"""
        self.running = False
        print("🛑 Flow stopped")


def main():
    """Main entry point for the email flow"""
    flow = EmailProcessingFlow()
    asyncio.run(flow.start())


if __name__ == "__main__":
    main()