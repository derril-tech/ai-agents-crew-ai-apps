"""
Email Validator Tool

This tool provides email validation capabilities for the SDR Assistant.
"""

from crewai_tools import BaseTool
from typing import Optional
import re

class EmailValidatorTool(BaseTool):
    """Tool for validating email addresses"""
    
    name: str = "Email Validator Tool"
    description: str = "Validate email addresses for format and deliverability"
    
    def _run(self, email: str) -> str:
        """Validate email address"""
        try:
            # Basic email validation
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            is_valid = re.match(pattern, email) is not None
            
            result = {
                "email": email,
                "is_valid": is_valid,
                "format_check": "passed" if is_valid else "failed",
                "deliverability": "unknown"
            }
            
            return f"Email validation result: {result}"
            
        except Exception as e:
            return f"Error validating email {email}: {str(e)}"
    
    async def _arun(self, email: str) -> str:
        """Async version of email validation"""
        return self._run(email)
