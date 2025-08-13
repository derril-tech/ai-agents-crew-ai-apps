# backend/agents/tools/gmail_tool.py
"""
Gmail Integration Tool for CrewAI
Handles Gmail API interactions for reading and managing emails
"""

import os
import base64
import json
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import pickle

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from crewai_tools import BaseTool


class GmailTool(BaseTool):
    """Tool for Gmail operations"""
    
    name: str = "gmail_tool"
    description: str = "Interact with Gmail to read emails, get thread history, and manage messages"
    
    def __init__(self):
        """Initialize Gmail service"""
        super().__init__()
        self.service = self._get_gmail_service()
        self.user_email = os.getenv("MY_EMAIL", "me")
    
    def _get_gmail_service(self):
        """Authenticate and return Gmail service instance"""
        creds = None
        token_file = "token.json"
        
        # Token file stores the user's access and refresh tokens
        if os.path.exists(token_file):
            creds = Credentials.from_authorized_user_file(token_file)
        
        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    os.getenv("GMAIL_CREDENTIALS_PATH", "credentials.json"),
                    scopes=os.getenv("GMAIL_SCOPES", "").split(",")
                )
                creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            with open(token_file, 'w') as token:
                token.write(creds.to_json())
        
        return build('gmail', 'v1', credentials=creds)
    
    def _run(self, action: str, **kwargs) -> str:
        """
        Execute Gmail operations
        
        Args:
            action: The action to perform (get_unread, get_thread, search, etc.)
            **kwargs: Additional parameters for the action
        """
        try:
            if action == "get_unread":
                return json.dumps(self.get_unread_emails(**kwargs))
            elif action == "get_thread":
                return json.dumps(self.get_email_thread(kwargs.get("thread_id")))
            elif action == "search":
                return json.dumps(self.search_emails(kwargs.get("query", "")))
            elif action == "get_email":
                return json.dumps(self.get_email_details(kwargs.get("email_id")))
            else:
                return json.dumps({"error": f"Unknown action: {action}"})
        except Exception as e:
            return json.dumps({"error": str(e)})
    
    def get_unread_emails(self, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Fetch unread emails from Gmail
        
        Args:
            max_results: Maximum number of emails to fetch
            
        Returns:
            List of email dictionaries
        """
        try:
            # Query for unread emails
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread',
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            emails = []
            
            for message in messages:
                email_data = self.get_email_details(message['id'])
                if email_data:
                    emails.append(email_data)
            
            print(f"📧 Fetched {len(emails)} unread emails")
            return emails
            
        except HttpError as error:
            print(f'❌ An error occurred: {error}')
            return []
    
    def get_email_details(self, email_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific email
        
        Args:
            email_id: Gmail message ID
            
        Returns:
            Email details dictionary
        """
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=email_id,
                format='full'
            ).execute()
            
            # Parse email headers
            headers = message['payload'].get('headers', [])
            header_dict = {h['name']: h['value'] for h in headers}
            
            # Extract email body
            body = self._extract_body(message['payload'])
            
            # Get labels and metadata
            labels = message.get('labelIds', [])
            
            return {
                'id': message['id'],
                'threadId': message['threadId'],
                'sender': header_dict.get('From', ''),
                'to': header_dict.get('To', ''),
                'cc': header_dict.get('Cc', ''),
                'subject': header_dict.get('Subject', ''),
                'date': header_dict.get('Date', ''),
                'body': body,
                'snippet': message.get('snippet', ''),
                'labels': labels,
                'is_unread': 'UNREAD' in labels,
                'is_important': 'IMPORTANT' in labels,
                'has_attachments': self._has_attachments(message['payload'])
            }
            
        except HttpError as error:
            print(f'❌ Error fetching email {email_id}: {error}')
            return None
    
    def get_email_thread(self, thread_id: str) -> Dict[str, Any]:
        """
        Get all messages in an email thread
        
        Args:
            thread_id: Gmail thread ID
            
        Returns:
            Thread details with all messages
        """
        try:
            thread = self.service.users().threads().get(
                userId='me',
                id=thread_id,
                format='full'
            ).execute()
            
            messages = []
            for message in thread.get('messages', []):
                # Parse each message in the thread
                headers = message['payload'].get('headers', [])
                header_dict = {h['name']: h['value'] for h in headers}
                
                messages.append({
                    'id': message['id'],
                    'sender': header_dict.get('From', ''),
                    'date': header_dict.get('Date', ''),
                    'subject': header_dict.get('Subject', ''),
                    'snippet': message.get('snippet', ''),
                    'body': self._extract_body(message['payload'])
                })
            
            return {
                'threadId': thread_id,
                'message_count': len(messages),
                'messages': messages
            }
            
        except HttpError as error:
            print(f'❌ Error fetching thread {thread_id}: {error}')
            return {'error': str(error)}
    
    def search_emails(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search emails using Gmail query syntax
        
        Args:
            query: Gmail search query
            max_results: Maximum number of results
            
        Returns:
            List of matching emails
        """
        try:
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            emails = []
            
            for message in messages:
                email_data = self.get_email_details(message['id'])
                if email_data:
                    emails.append(email_data)
            
            return emails
            
        except HttpError as error:
            print(f'❌ Search error: {error}')
            return []
    
    def _extract_body(self, payload: Dict) -> str:
        """
        Extract email body from payload
        
        Args:
            payload: Gmail message payload
            
        Returns:
            Email body text
        """
        body = ""
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body']['data']
                    body += base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                elif part['mimeType'] == 'text/html' and not body:
                    # Use HTML if plain text not available
                    data = part['body']['data']
                    body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                elif 'parts' in part:
                    # Recursive for nested parts
                    body += self._extract_body(part)
        elif payload.get('body', {}).get('data'):
            body = base64.urlsafe_b64decode(
                payload['body']['data']
            ).decode('utf-8', errors='ignore')
        
        return body.strip()
    
    def _has_attachments(self, payload: Dict) -> bool:
        """
        Check if email has attachments
        
        Args:
            payload: Gmail message payload
            
        Returns:
            True if has attachments
        """
        if 'parts' in payload:
            for part in payload['parts']:
                if part.get('filename'):
                    return True
                if 'parts' in part and self._has_attachments(part):
                    return True
        return False
    
    def mark_as_read(self, email_id: str) -> bool:
        """
        Mark an email as read
        
        Args:
            email_id: Gmail message ID
            
        Returns:
            Success status
        """
        try:
            self.service.users().messages().modify(
                userId='me',
                id=email_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            return True
        except HttpError as error:
            print(f'❌ Error marking as read: {error}')
            return False