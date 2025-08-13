from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class LeadStatus(str, Enum):
    NEW = "new"
    ANALYZING = "analyzing"
    ANALYZED = "analyzed"
    EMAIL_DRAFTED = "email_drafted"
    EMAIL_SENT = "email_sent"
    RESPONDED = "responded"
    QUALIFIED = "qualified"
    DISQUALIFIED = "disqualified"

class IndustryType(str, Enum):
    TECHNOLOGY = "technology"
    HEALTHCARE = "healthcare"
    FINANCE = "finance"
    RETAIL = "retail"
    MANUFACTURING = "manufacturing"
    EDUCATION = "education"
    CONSULTING = "consulting"
    REAL_ESTATE = "real_estate"
    OTHER = "other"

class CompanySize(str, Enum):
    STARTUP = "startup"  # 1-50
    SMALL = "small"      # 51-200
    MEDIUM = "medium"    # 201-1000
    LARGE = "large"      # 1001-5000
    ENTERPRISE = "enterprise"  # 5000+

class LeadPersonalInfo(BaseModel):
    name: str = Field(..., description="The full name of the lead.")
    job_title: str = Field(..., description="The job title of the lead.")
    role_relevance: int = Field(..., ge=0, le=10, description="Score indicating the lead's influence in the buying process (0–10).")
    professional_background: Optional[str] = Field(None, description="Brief highlights of the lead's professional background or career.")
    linkedin_url: Optional[str] = Field(None, description="LinkedIn profile URL if available.")
    years_of_experience: Optional[int] = Field(None, ge=0, le=50, description="Years of professional experience.")
    previous_companies: Optional[List[str]] = Field(None, description="List of previous companies.")
    education: Optional[str] = Field(None, description="Educational background.")
    certifications: Optional[List[str]] = Field(None, description="Professional certifications.")

class CompanyInfo(BaseModel):
    company_name: str = Field(..., description="Name of the company the lead works for.")
    industry: IndustryType = Field(..., description="The sector or industry of the company.")
    company_size: int = Field(..., description="Estimated number of employees at the company.")
    company_size_category: CompanySize = Field(..., description="Company size category.")
    revenue: Optional[float] = Field(None, description="Annual revenue of the company, if publicly available.")
    market_presence: int = Field(..., ge=0, le=10, description="Visibility or influence the company has in its market (0–10).")
    website: Optional[str] = Field(None, description="Company website URL.")
    headquarters: Optional[str] = Field(None, description="Company headquarters location.")
    founded_year: Optional[int] = Field(None, ge=1800, le=2025, description="Year the company was founded.")
    funding_stage: Optional[str] = Field(None, description="Funding stage (seed, series A, B, C, public, etc.).")
    recent_news: Optional[List[str]] = Field(None, description="Recent company news or developments.")
    competitors: Optional[List[str]] = Field(None, description="Main competitors.")
    tech_stack: Optional[List[str]] = Field(None, description="Known technology stack.")

class EngagementFit(BaseModel):
    readiness_score: int = Field(..., ge=0, le=10, description="Assessment of how ready and relevant the lead is for outreach (0–10).")
    alignment_notes: Optional[str] = Field(None, description="Supporting notes that explain the rationale for the readiness score.")
    pain_points: Optional[List[str]] = Field(None, description="Identified pain points the company might have.")
    opportunities: Optional[List[str]] = Field(None, description="Business opportunities identified.")
    timing_factors: Optional[List[str]] = Field(None, description="Factors that make this a good or bad time for outreach.")
    competitive_advantage: Optional[str] = Field(None, description="How DFN AI Services can provide value.")
    buying_signals: Optional[List[str]] = Field(None, description="Signals that indicate potential buying intent.")

class LeadReadinessScore(BaseModel):
    score: int = Field(..., ge=0, le=100, description="Final lead readiness score (0–100).")
    scoring_criteria: List[str] = Field(..., description="List of criteria that contributed to the final score.")
    summary_notes: Optional[str] = Field(None, description="Any validation comments or strategic notes about the score.")
    confidence_level: float = Field(..., ge=0.0, le=1.0, description="Confidence in the scoring (0.0-1.0).")
    priority_level: str = Field(..., description="Priority level: High, Medium, Low.")
    recommended_approach: Optional[str] = Field(None, description="Recommended outreach approach.")
    risk_factors: Optional[List[str]] = Field(None, description="Potential risks or challenges.")

class LeadReadinessResult(BaseModel):
    personal_info: LeadPersonalInfo = Field(..., description="Detailed profile of the lead.")
    company_info: CompanyInfo = Field(..., description="Business context and company insights.")
    engagement_fit: EngagementFit = Field(..., description="Evaluation of how appropriate the timing and message would be for outreach.")
    readiness_score: LeadReadinessScore = Field(..., description="Overall scoring of the lead's outreach potential.")
    analysis_timestamp: datetime = Field(default_factory=datetime.now, description="When the analysis was completed.")
    analysis_version: str = Field(default="1.0", description="Version of the analysis algorithm used.")

class EmailTemplate(BaseModel):
    template_id: str = Field(..., description="Unique identifier for the template.")
    name: str = Field(..., description="Template name.")
    subject_line: str = Field(..., description="Email subject line template.")
    body: str = Field(..., description="Email body template with placeholders.")
    industry_focus: Optional[List[IndustryType]] = Field(None, description="Industries this template works best for.")
    role_focus: Optional[List[str]] = Field(None, description="Job roles this template targets.")
    use_case: Optional[str] = Field(None, description="Specific use case for this template.")
    variables: List[str] = Field(default_factory=list, description="Template variables that need to be filled.")

class GeneratedEmail(BaseModel):
    subject: str = Field(..., description="Email subject line.")
    body: str = Field(..., description="Email body content.")
    personalization_score: float = Field(..., ge=0.0, le=1.0, description="How personalized the email is (0.0-1.0).")
    template_used: Optional[str] = Field(None, description="Template ID if a template was used.")
    key_talking_points: List[str] = Field(default_factory=list, description="Main talking points used in the email.")
    call_to_action: str = Field(..., description="The primary call to action.")
    estimated_read_time: int = Field(..., description="Estimated read time in seconds.")
    compliance_checked: bool = Field(default=False, description="Whether the email has been checked for compliance.")

class LeadInput(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Lead's full name.")
    job_title: str = Field(..., min_length=2, max_length=150, description="Lead's job title.")
    company: str = Field(..., min_length=2, max_length=150, description="Lead's company name.")
    email: str = Field(..., description="Lead's email address.")
    phone: Optional[str] = Field(None, description="Lead's phone number.")
    linkedin_url: Optional[str] = Field(None, description="Lead's LinkedIn profile URL.")
    company_website: Optional[str] = Field(None, description="Company website URL.")
    use_case: Optional[str] = Field(None, description="Specific use case or interest area.")
    source: Optional[str] = Field(None, description="Where this lead came from.")
    notes: Optional[str] = Field(None, description="Additional notes about the lead.")

    @validator('linkedin_url', 'company_website')
    def validate_urls(cls, v):
        if v and not v.startswith(('http://', 'https://')):
            return f"https://{v}"
        return v

class CampaignMetrics(BaseModel):
    total_leads: int = Field(default=0, description="Total number of leads processed.")
    emails_sent: int = Field(default=0, description="Number of emails sent.")
    opens: int = Field(default=0, description="Number of email opens.")
    clicks: int = Field(default=0, description="Number of email clicks.")
    replies: int = Field(default=0, description="Number of replies received.")
    meetings_booked: int = Field(default=0, description="Number of meetings booked.")
    qualified_leads: int = Field(default=0, description="Number of qualified leads.")
    conversion_rate: float = Field(default=0.0, description="Overall conversion rate.")
    average_score: float = Field(default=0.0, description="Average lead readiness score.")

class AnalyticsData(BaseModel):
    campaign_metrics: CampaignMetrics = Field(default_factory=CampaignMetrics)
    top_industries: List[Dict[str, Any]] = Field(default_factory=list)
    score_distribution: Dict[str, int] = Field(default_factory=dict)
    daily_activity: List[Dict[str, Any]] = Field(default_factory=list)
    performance_trends: Dict[str, List[float]] = Field(default_factory=dict)

# Extended models for smart features
class LeadEnrichmentData(BaseModel):
    social_profiles: Dict[str, str] = Field(default_factory=dict, description="Social media profiles.")
    contact_info: Dict[str, str] = Field(default_factory=dict, description="Additional contact information.")
    company_insights: Dict[str, Any] = Field(default_factory=dict, description="Deep company insights.")
    market_intelligence: Dict[str, Any] = Field(default_factory=dict, description="Market and competitive intelligence.")
    engagement_history: List[Dict[str, Any]] = Field(default_factory=list, description="Previous engagement history.")

class ABTestConfig(BaseModel):
    test_name: str = Field(..., description="Name of the A/B test.")
    template_a: str = Field(..., description="Template A ID.")
    template_b: str = Field(..., description="Template B ID.")
    split_percentage: float = Field(default=0.5, ge=0.0, le=1.0, description="Percentage for template A.")
    target_metric: str = Field(default="reply_rate", description="Metric to optimize for.")
    status: str = Field(default="active", description="Test status.")

class EmailPerformance(BaseModel):
    email_id: str = Field(..., description="Unique email identifier.")
    lead_id: str = Field(..., description="Associated lead ID.")
    subject: str = Field(..., description="Email subject line.")
    sent_at: datetime = Field(..., description="When the email was sent.")
    opened_at: Optional[datetime] = Field(None, description="When the email was opened.")
    clicked_at: Optional[datetime] = Field(None, description="When links were clicked.")
    replied_at: Optional[datetime] = Field(None, description="When reply was received.")
    bounce_type: Optional[str] = Field(None, description="Bounce type if bounced.")
    template_used: Optional[str] = Field(None, description="Template used for this email.")
    ab_test_group: Optional[str] = Field(None, description="A/B test group (A or B).")
    performance_score: float = Field(default=0.0, description="Overall performance score.")