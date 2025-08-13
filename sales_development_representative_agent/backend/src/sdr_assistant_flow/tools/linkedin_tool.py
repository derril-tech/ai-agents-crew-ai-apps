"""
LinkedIn Research Tool for SDR Assistant

This tool provides enhanced LinkedIn profile research capabilities
for lead analysis and qualification.
"""

from crewai_tools import BaseTool
from typing import Dict, Any, Optional
import requests
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from src.sdr_assistant_flow.utils.logger import get_logger

logger = get_logger(__name__)

class LinkedInTool(BaseTool):
    name: str = "LinkedIn Profile Analyzer"
    description: str = (
        "Analyzes LinkedIn profiles to extract professional information, "
        "career history, skills, and engagement patterns for lead qualification."
    )

    def _run(self, linkedin_url: str) -> str:
        """
        Analyze a LinkedIn profile URL and extract relevant information
        
        Args:
            linkedin_url: LinkedIn profile URL to analyze
            
        Returns:
            Formatted string with profile insights
        """
        try:
            if not self._is_valid_linkedin_url(linkedin_url):
                return "Invalid LinkedIn URL provided. Please provide a valid LinkedIn profile URL."
            
            # Extract profile information
            profile_data = self._extract_profile_data(linkedin_url)
            
            if not profile_data:
                return "Could not extract profile information. The profile might be private or URL is incorrect."
            
            # Format the results
            return self._format_profile_insights(profile_data)
            
        except Exception as e:
            logger.error(f"Error analyzing LinkedIn profile: {str(e)}")
            return f"Error analyzing LinkedIn profile: {str(e)}"

    def _is_valid_linkedin_url(self, url: str) -> bool:
        """Validate if the URL is a proper LinkedIn profile URL"""
        try:
            parsed = urlparse(url)
            return (
                parsed.netloc in ['linkedin.com', 'www.linkedin.com'] and
                '/in/' in parsed.path
            )
        except:
            return False

    def _extract_profile_data(self, linkedin_url: str) -> Optional[Dict[str, Any]]:
        """
        Extract profile data from LinkedIn URL
        
        Note: This is a simplified implementation. In production, you would:
        - Use LinkedIn API with proper authentication
        - Implement proper rate limiting
        - Handle GDPR/privacy compliance
        """
        try:
            # For this demo, we'll simulate profile analysis
            # In production, integrate with LinkedIn API or approved scraping service
            
            profile_username = self._extract_username_from_url(linkedin_url)
            
            # Simulated profile data based on common patterns
            mock_data = self._generate_mock_profile_data(profile_username, linkedin_url)
            
            return mock_data
            
        except Exception as e:
            logger.error(f"Error extracting profile data: {str(e)}")
            return None

    def _extract_username_from_url(self, url: str) -> str:
        """Extract username from LinkedIn URL"""
        try:
            # Extract username from URL like /in/username/
            match = re.search(r'/in/([^/]+)', url)
            return match.group(1) if match else "unknown"
        except:
            return "unknown"

    def _generate_mock_profile_data(self, username: str, url: str) -> Dict[str, Any]:
        """
        Generate realistic mock profile data for demonstration
        
        In production, replace this with actual LinkedIn API integration
        """
        # This simulates common LinkedIn profile patterns
        return {
            "username": username,
            "url": url,
            "professional_summary": "Experienced executive with strong background in technology and innovation",
            "current_position": {
                "title": "Chief Executive Officer",
                "company": "Technology Company",
                "duration": "3+ years"
            },
            "experience_level": "Senior Executive (15+ years)",
            "industry_expertise": ["Technology", "SaaS", "Enterprise Software"],
            "education": "MBA from top-tier business school",
            "skills": ["Leadership", "Strategy", "AI/ML", "Digital Transformation"],
            "activity_level": "Active - posts regularly about industry trends",
            "connection_count": "500+",
            "influence_indicators": [
                "Thought leader in AI/technology space",
                "Frequently shares insights on innovation",
                "Engages with industry content"
            ],
            "buying_signals": [
                "Recently posted about AI adoption challenges",
                "Company is scaling technology operations",
                "Active in discussing industry transformation"
            ],
            "contact_preference": "Professional outreach welcome",
            "last_activity": "Active within last week"
        }

    def _format_profile_insights(self, profile_data: Dict[str, Any]) -> str:
        """Format profile data into readable insights"""
        insights = []
        
        insights.append(f"🔍 LinkedIn Profile Analysis")
        insights.append(f"Profile: {profile_data.get('url', 'N/A')}")
        insights.append("")
        
        # Professional Summary
        if profile_data.get('professional_summary'):
            insights.append(f"Professional Summary:")
            insights.append(f"  {profile_data['professional_summary']}")
            insights.append("")
        
        # Current Position
        current_pos = profile_data.get('current_position', {})
        if current_pos:
            insights.append(f"Current Role:")
            insights.append(f"  Title: {current_pos.get('title', 'N/A')}")
            insights.append(f"  Company: {current_pos.get('company', 'N/A')}")
            insights.append(f"  Duration: {current_pos.get('duration', 'N/A')}")
            insights.append("")
        
        # Experience and Skills
        if profile_data.get('experience_level'):
            insights.append(f"Experience Level: {profile_data['experience_level']}")
        
        if profile_data.get('industry_expertise'):
            insights.append(f"Industry Expertise: {', '.join(profile_data['industry_expertise'])}")
        
        if profile_data.get('skills'):
            top_skills = profile_data['skills'][:5]  # Top 5 skills
            insights.append(f"Key Skills: {', '.join(top_skills)}")
        
        insights.append("")
        
        # Activity and Influence
        if profile_data.get('activity_level'):
            insights.append(f"Activity Level: {profile_data['activity_level']}")
        
        if profile_data.get('influence_indicators'):
            insights.append(f"Influence Indicators:")
            for indicator in profile_data['influence_indicators']:
                insights.append(f"  • {indicator}")
        
        insights.append("")
        
        # Buying Signals
        if profile_data.get('buying_signals'):
            insights.append(f"🎯 Buying Signals Detected:")
            for signal in profile_data['buying_signals']:
                insights.append(f"  • {signal}")
        
        insights.append("")
        
        # Contact Insights
        if profile_data.get('contact_preference'):
            insights.append(f"Contact Preference: {profile_data['contact_preference']}")
        
        if profile_data.get('last_activity'):
            insights.append(f"Last Activity: {profile_data['last_activity']}")
        
        return "\n".join(insights)

    def _advanced_profile_analysis(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform advanced analysis on profile data
        
        This method adds AI-powered insights and scoring
        """
        analysis = {
            "decision_maker_score": 0,
            "engagement_likelihood": 0,
            "personalization_opportunities": [],
            "outreach_timing": "neutral",
            "risk_factors": []
        }
        
        # Analyze decision-making power
        current_pos = profile_data.get('current_position', {})
        title = current_pos.get('title', '').lower()
        
        if any(keyword in title for keyword in ['ceo', 'founder', 'president', 'owner']):
            analysis["decision_maker_score"] = 9
        elif any(keyword in title for keyword in ['vp', 'director', 'head of', 'chief']):
            analysis["decision_maker_score"] = 7
        elif any(keyword in title for keyword in ['manager', 'lead', 'senior']):
            analysis["decision_maker_score"] = 5
        else:
            analysis["decision_maker_score"] = 3
        
        # Analyze engagement likelihood
        activity = profile_data.get('activity_level', '').lower()
        if 'active' in activity and 'regularly' in activity:
            analysis["engagement_likelihood"] = 8
        elif 'active' in activity:
            analysis["engagement_likelihood"] = 6
        else:
            analysis["engagement_likelihood"] = 4
        
        # Identify personalization opportunities
        buying_signals = profile_data.get('buying_signals', [])
        if buying_signals:
            analysis["personalization_opportunities"].extend(buying_signals)
        
        influence_indicators = profile_data.get('influence_indicators', [])
        if influence_indicators:
            analysis["personalization_opportunities"].extend(influence_indicators)
        
        # Determine outreach timing
        last_activity = profile_data.get('last_activity', '').lower()
        if 'active within' in last_activity and ('day' in last_activity or 'week' in last_activity):
            analysis["outreach_timing"] = "favorable"
        elif 'month' in last_activity:
            analysis["outreach_timing"] = "neutral"
        else:
            analysis["outreach_timing"] = "cautious"
        
        return analysis

# Additional LinkedIn utility functions
def extract_company_from_linkedin(profile_data: Dict[str, Any]) -> Optional[str]:
    """Extract current company from LinkedIn profile data"""
    current_pos = profile_data.get('current_position', {})
    return current_pos.get('company')

def get_seniority_level(job_title: str) -> str:
    """Determine seniority level from job title"""
    title_lower = job_title.lower()
    
    if any(keyword in title_lower for keyword in ['ceo', 'founder', 'president', 'owner', 'chief']):
        return "C-Level"
    elif any(keyword in title_lower for keyword in ['vp', 'vice president', 'svp']):
        return "VP-Level"
    elif any(keyword in title_lower for keyword in ['director', 'head of']):
        return "Director-Level"
    elif any(keyword in title_lower for keyword in ['manager', 'lead']):
        return "Manager-Level"
    elif any(keyword in title_lower for keyword in ['senior', 'sr', 'principal']):
        return "Senior-Level"
    else:
        return "Individual Contributor"

def calculate_linkedin_score(profile_data: Dict[str, Any]) -> int:
    """Calculate overall LinkedIn profile score for lead qualification"""
    score = 0
    
    # Decision-making power (0-30 points)
    current_pos = profile_data.get('current_position', {})
    title = current_pos.get('title', '').lower()
    
    if any(keyword in title for keyword in ['ceo', 'founder', 'president']):
        score += 30
    elif any(keyword in title for keyword in ['vp', 'director', 'chief']):
        score += 25
    elif any(keyword in title for keyword in ['manager', 'head of']):
        score += 20
    else:
        score += 10
    
    # Activity level (0-20 points)
    activity = profile_data.get('activity_level', '').lower()
    if 'active' in activity and 'regularly' in activity:
        score += 20
    elif 'active' in activity:
        score += 15
    else:
        score += 5
    
    # Influence indicators (0-25 points)
    influence_indicators = profile_data.get('influence_indicators', [])
    score += min(len(influence_indicators) * 8, 25)
    
    # Buying signals (0-25 points)
    buying_signals = profile_data.get('buying_signals', [])
    score += min(len(buying_signals) * 8, 25)
    
    return min(score, 100)  # Cap at 100