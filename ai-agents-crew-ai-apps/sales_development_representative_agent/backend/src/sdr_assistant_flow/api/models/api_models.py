"""
API Models for SDR Assistant

This module defines Pydantic models for API requests and responses,
ensuring type safety and validation for all API endpoints.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from enum import Enum

from src.sdr_assistant_flow.lead_types import (
    LeadInput,
    LeadReadinessResult,
    GeneratedEmail,
    CampaignMetrics,
    LeadStatus
)

class ProcessingStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"
    CANCELLED = "cancelled"

class PriorityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

# Request Models
class LeadDataRequest(BaseModel):
    """Lead data for analysis requests"""
    name: str = Field(..., min_length=2, max_length=100)
    job_title: str = Field(..., min_length=2, max_length=150)
    company: str = Field(..., min_length=2, max_length=150)
    email: str = Field(..., description="Email address")
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    company_website: Optional[str] = None
    use_case: Optional[str] = None
    source: Optional[str] = None
    notes: Optional[str] = None

class LeadAnalysisRequest(BaseModel):
    """Request model for single lead analysis"""
    lead_data: LeadDataRequest
    async_processing: bool = Field(default=False, description="Whether to process asynchronously")
    include_enrichment: bool = Field(default=True, description="Whether to include data enrichment")
    priority: PriorityLevel = Field(default=PriorityLevel.MEDIUM)

class EmailGenerationRequest(BaseModel):
    """Request model for email generation"""
    lead_name: str
    company_name: str
    personal_info: Dict[str, Any]
    company_info: Dict[str, Any]
    engagement_fit: Dict[str, Any]
    template_id: Optional[str] = None
    custom_talking_points: Optional[List[str]] = None
    tone: Optional[str] = Field(default="professional", description="Email tone: professional, casual, urgent")

class BulkProcessRequest(BaseModel):
    """Request model for bulk lead processing"""
    leads: List[LeadDataRequest] = Field(..., min_items=1, max_items=100)
    campaign_name: Optional[str] = None
    priority: PriorityLevel = Field(default=PriorityLevel.MEDIUM)
    include_enrichment: bool = Field(default=True)
    email_template_id: Optional[str] = None
    custom_instructions: Optional[str] = None

class TemplateRequest(BaseModel):
    """Request model for email template operations"""
    name: str
    subject_line: str
    body: str
    industry_focus: Optional[List[str]] = None
    role_focus: Optional[List[str]] = None
    use_case: Optional[str] = None

# Response Models
class LeadAnalysisResponse(BaseModel):
    """Response model for lead analysis"""
    session_id: str
    status: ProcessingStatus
    message: str
    results: Optional[Dict[str, Any]] = None
    processing_time: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.now)

class EmailGenerationResponse(BaseModel):
    """Response model for email generation"""
    session_id: str
    status: ProcessingStatus
    message: str
    email: Optional[Dict[str, Any]] = None
    alternatives: Optional[List[Dict[str, Any]]] = None
    timestamp: datetime = Field(default_factory=datetime.now)

class CampaignStatusResponse(BaseModel):
    """Response model for campaign status"""
    session_id: str
    status: ProcessingStatus
    message: str
    total_leads: int = 0
    processed_leads: int = 0
    current_step: Optional[str] = None
    estimated_completion_time: Optional[str] = None
    results: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)

class AnalyticsResponse(BaseModel):
    """Response model for analytics data"""
    campaign_metrics: CampaignMetrics
    performance_data: Dict[str, Any]
    trends: Dict[str, List[float]]
    insights: List[str]
    timestamp: datetime = Field(default_factory=datetime.now)

class TemplateResponse(BaseModel):
    """Response model for template operations"""
    template_id: str
    name: str
    status: str
    performance_metrics: Optional[Dict[str, float]] = None
    usage_count: int = 0
    created_at: datetime = Field(default_factory=datetime.now)

class ErrorResponse(BaseModel):
    """Standard error response model"""
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    session_id: Optional[str] = None

class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    timestamp: datetime
    active_flows: int
    cached_results: int
    system_info: Optional[Dict[str, Any]] = None

class LeadEnrichmentRequest(BaseModel):
    """Request model for lead enrichment"""
    lead_data: LeadDataRequest
    enrichment_sources: List[str] = Field(default=["linkedin", "company_website", "social_media"])
    include_competitors: bool = Field(default=True)
    include_funding_info: bool = Field(default=True)
    include_tech_stack: bool = Field(default=True)

class LeadEnrichmentResponse(BaseModel):
    """Response model for lead enrichment"""
    session_id: str
    status: ProcessingStatus
    enriched_data: Optional[Dict[str, Any]] = None
    confidence_score: float = Field(default=0.0, ge=0.0, le=1.0)
    sources_used: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.now)

class ABTestRequest(BaseModel):
    """Request model for A/B testing email templates"""
    test_name: str
    template_a_id: str
    template_b_id: str
    leads: List[LeadDataRequest]
    split_percentage: float = Field(default=0.5, ge=0.0, le=1.0)
    target_metric: str = Field(default="reply_rate")
    duration_days: int = Field(default=7, ge=1, le=30)

class ABTestResponse(BaseModel):
    """Response model for A/B test results"""
    test_id: str
    test_name: str
    status: str
    template_a_performance: Dict[str, float]
    template_b_performance: Dict[str, float]
    winner: Optional[str] = None
    confidence_level: float = Field(default=0.0, ge=0.0, le=1.0)
    insights: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.now)

class WebhookRequest(BaseModel):
    """Request model for webhook configuration"""
    url: str = Field(..., description="Webhook URL")
    events: List[str] = Field(..., description="Events to subscribe to")
    secret: Optional[str] = None
    active: bool = Field(default=True)