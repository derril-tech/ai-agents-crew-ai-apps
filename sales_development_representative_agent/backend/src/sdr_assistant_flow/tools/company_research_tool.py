"""
Company Research Tool

This tool provides company research capabilities for the SDR Assistant.
"""

from crewai_tools import BaseTool
from typing import Optional
import requests
import json

class CompanyResearchTool(BaseTool):
    """Tool for researching company information"""
    
    name: str = "Company Research Tool"
    description: str = "Research company information including size, industry, and recent news"
    
    def _run(self, company_name: str) -> str:
        """Research company information"""
        try:
            # Mock implementation for now
            company_info = {
                "name": company_name,
                "industry": "Technology",
                "size": "Enterprise",
                "revenue": "Unknown",
                "headquarters": "Unknown",
                "founded": "Unknown"
            }
            
            return json.dumps(company_info, indent=2)
            
        except Exception as e:
            return f"Error researching company {company_name}: {str(e)}"
    
    async def _arun(self, company_name: str) -> str:
        """Async version of company research"""
        return self._run(company_name)
