# backend/agents/tools/draft_tool.py
"""
Draft Creation Tool for CrewAI
Handles creating and managing email drafts
"""

import os
import json
import base64
from typing import Dict, Any, Optional, List
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from crewai_tools import BaseTool


class DraftTool(BaseTool):
    """Tool for creating and managing email drafts"""
    
    name: str = "draft_creator"
    description: str = "Create, update, and manage Gmail draft emails"
    
    def __init__(self):
        """Initialize draft tool with Gmail service"""
        super().__init__()
        self.service = self._get_gmail_service()
        self.user_email = os.getenv("MY_EMAIL", "me")
    
    def _get_gmail_service(self):
        """Get authenticated Gmail service"""
        token_file = "token.json"
        
        if os.path.exists(token_file):
            creds = Credentials.from_authorized_user_file(token_file)
            return build('gmail', 'v1', credentials=creds)
        else:
            raise Exception("Gmail not authenticated. Please run Gmail setup first.")
    
    def _run(self, action: str, **kwargs) -> str:
        """
        Execute draft operations
        
        Args:
            action: Action to perform (create, update, list, delete)
            **kwargs: Additional parameters
            
        Returns:
            JSON string of result
        """
        try:
            if action == "create":
                return json.dumps(self.create_draft(**kwargs))
            elif action == "update":
                return json.dumps(self.update_draft(**kwargs))
            elif action == "list":
                return json.dumps(self.list_drafts())
            elif action == "delete":
                return json.dumps(self.delete_draft(kwargs.get("draft_id")))
            else:
                return json.dumps({"error": f"Unknown action: {action}"})
        except Exception as e:
            return json.dumps({"error": str(e)})
    
    @staticmethod
    def create_draft(
        to: str,
        subject: str,
        body: str,
        cc: str = "",
        bcc: str = "",
        reply_to_id: str = None,
        thread_id: str = None,
        is_html: bool = False
    ) -> Dict[str, Any]:
        """
        Create a Gmail draft
        
        Args:
            to: Recipient email
            subject: Email subject
            body: Email body
            cc: CC recipients
            bcc: BCC recipients
            reply_to_id: Message ID if replying
            thread_id: Thread ID if part of thread
            is_html: Whether body is HTML
            
        Returns:
            Draft creation result
        """
        tool = DraftTool()
        
        try:
            # Create message
            if is_html:
                message = MIMEMultipart('alternative')
                message.attach(MIMEText(body, 'html'))
            else:
                message = MIMEText(body)
            
            message['to'] = to
            message['subject'] = subject
            
            if cc:
                message['cc'] = cc
            if bcc:
                message['bcc'] = bcc
            
            # Add reply headers if replying
            if reply_to_id:
                message['In-Reply-To'] = reply_to_id
                message['References'] = reply_to_id
            
            # Encode message
            raw_message = base64.urlsafe_b64encode(
                message.as_bytes()
            ).decode('utf-8')
            
            # Create draft body
            draft_body = {
                'message': {
                    'raw': raw_message
                }
            }
            
            if thread_id:
                draft_body['message']['threadId'] = thread_id
            
            # Create draft
            draft = tool.service.users().drafts().create(
                userId='me',
                body=draft_body
            ).execute()
            
            print(f"✉️ Draft created: {draft['id']}")
            
            return {
                'success': True,
                'draft_id': draft['id'],
                'message': f"Draft created for {to}",
                'details': {
                    'to': to,
                    'subject': subject,
                    'thread_id': thread_id
                }
            }
            
        except HttpError as error:
            print(f'❌ Error creating draft: {error}')
            return {
                'success': False,
                'error': str(error)
            }
    
    def update_draft(
        self,
        draft_id: str,
        to: str = None,
        subject: str = None,
        body: str = None,
        cc: str = None
    ) -> Dict[str, Any]:
        """
        Update an existing draft
        
        Args:
            draft_id: Draft ID to update
            to: New recipient (optional)
            subject: New subject (optional)
            body: New body (optional)
            cc: New CC (optional)
            
        Returns:
            Update result
        """
        try:
            # Get existing draft
            draft = self.service.users().drafts().get(
                userId='me',
                id=draft_id
            ).execute()
            
            # Decode existing message
            raw = draft['message']['raw']
            # Here you would decode and modify the message
            # For simplicity, we'll create a new message
            
            if body:
                message = MIMEText(body)
                if to:
                    message['to'] = to
                if subject:
                    message['subject'] = subject
                if cc:
                    message['cc'] = cc
                
                raw_message = base64.urlsafe_b64encode(
                    message.as_bytes()
                ).decode('utf-8')
                
                # Update draft
                updated_draft = self.service.users().drafts().update(
                    userId='me',
                    id=draft_id,
                    body={
                        'message': {
                            'raw': raw_message
                        }
                    }
                ).execute()
                
                return {
                    'success': True,
                    'draft_id': updated_draft['id'],
                    'message': 'Draft updated successfully'
                }
            
            return {
                'success': False,
                'error': 'No updates provided'
            }
            
        except HttpError as error:
            return {
                'success': False,
                'error': str(error)
            }
    
    def list_drafts(self, max_results: int = 10) -> Dict[str, Any]:
        """
        List all drafts
        
        Args:
            max_results: Maximum number of drafts to return
            
        Returns:
            List of drafts
        """
        try:
            results = self.service.users().drafts().list(
                userId='me',
                maxResults=max_results
            ).execute()
            
            drafts = results.get('drafts', [])
            
            draft_list = []
            for draft in drafts:
                # Get draft details
                draft_detail = self.service.users().drafts().get(
                    userId='me',
                    id=draft['id']
                ).execute()
                
                # Extract key information
                message = draft_detail['message']
                headers = message['payload'].get('headers', [])
                header_dict = {h['name']: h['value'] for h in headers}
                
                draft_list.append({
                    'id': draft['id'],
                    'to': header_dict.get('To', ''),
                    'subject': header_dict.get('Subject', ''),
                    'snippet': message.get('snippet', '')
                })
            
            return {
                'success': True,
                'count': len(draft_list),
                'drafts': draft_list
            }
            
        except HttpError as error:
            return {
                'success': False,
                'error': str(error)
            }
    
    def delete_draft(self, draft_id: str) -> Dict[str, Any]:
        """
        Delete a draft
        
        Args:
            draft_id: Draft ID to delete
            
        Returns:
            Deletion result
        """
        try:
            self.service.users().drafts().delete(
                userId='me',
                id=draft_id
            ).execute()
            
            return {
                'success': True,
                'message': f'Draft {draft_id} deleted'
            }
            
        except HttpError as error:
            return {
                'success': False,
                'error': str(error)
            }
    
    def send_draft(self, draft_id: str) -> Dict[str, Any]:
        """
        Send a draft
        
        Args:
            draft_id: Draft ID to send
            
        Returns:
            Send result
        """
        try:
            # Get the draft
            draft = self.service.users().drafts().get(
                userId='me',
                id=draft_id
            ).execute()
            
            # Send the message
            sent_message = self.service.users().messages().send(
                userId='me',
                body={'raw': draft['message']['raw']}
            ).execute()
            
            # Delete the draft
            self.delete_draft(draft_id)
            
            return {
                'success': True,
                'message_id': sent_message['id'],
                'message': 'Draft sent successfully'
            }
            
        except HttpError as error:
            return {
                'success': False,
                'error': str(error)
            }