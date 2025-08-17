"""
Resume models and schemas for AI-Powered Resume Parser & Job Matcher
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class ResumeStatus(str, Enum):
    """Resume processing status"""
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class SkillLevel(str, Enum):
    """Skill proficiency levels"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class Experience(BaseModel):
    """Work experience model"""
    company: str = Field(..., description="Company name")
    position: str = Field(..., description="Job title")
    start_date: datetime = Field(..., description="Start date")
    end_date: Optional[datetime] = Field(None, description="End date (None if current)")
    description: str = Field(..., description="Job description")
    skills_used: List[str] = Field(default_factory=list, description="Skills used in this role")
    achievements: List[str] = Field(default_factory=list, description="Key achievements")

class Education(BaseModel):
    """Education model"""
    institution: str = Field(..., description="Educational institution")
    degree: str = Field(..., description="Degree obtained")
    field_of_study: str = Field(..., description="Field of study")
    start_date: datetime = Field(..., description="Start date")
    end_date: Optional[datetime] = Field(None, description="End date")
    gpa: Optional[float] = Field(None, description="GPA if available")
    honors: List[str] = Field(default_factory=list, description="Honors and awards")

class Skill(BaseModel):
    """Skill model"""
    name: str = Field(..., description="Skill name")
    level: SkillLevel = Field(..., description="Skill proficiency level")
    years_experience: Optional[int] = Field(None, description="Years of experience")
    category: str = Field(..., description="Skill category (e.g., programming, soft skills)")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="AI confidence in skill extraction")

class Project(BaseModel):
    """Project model"""
    name: str = Field(..., description="Project name")
    description: str = Field(..., description="Project description")
    technologies: List[str] = Field(default_factory=list, description="Technologies used")
    url: Optional[str] = Field(None, description="Project URL")
    start_date: Optional[datetime] = Field(None, description="Start date")
    end_date: Optional[datetime] = Field(None, description="End date")

class Certification(BaseModel):
    """Certification model"""
    name: str = Field(..., description="Certification name")
    issuer: str = Field(..., description="Certifying organization")
    issue_date: datetime = Field(..., description="Issue date")
    expiry_date: Optional[datetime] = Field(None, description="Expiry date")
    credential_id: Optional[str] = Field(None, description="Credential ID")

class Resume(BaseModel):
    """Resume model"""
    id: Optional[int] = Field(None, description="Resume ID")
    user_id: int = Field(..., description="User ID")
    filename: str = Field(..., description="Original filename")
    file_path: str = Field(..., description="File storage path")
    file_size: int = Field(..., description="File size in bytes")
    file_type: str = Field(..., description="File type (pdf, docx, doc)")
    
    # Parsed content
    raw_text: str = Field(..., description="Extracted raw text")
    name: str = Field(..., description="Candidate name")
    email: str = Field(..., description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    location: Optional[str] = Field(None, description="Location")
    linkedin: Optional[str] = Field(None, description="LinkedIn URL")
    github: Optional[str] = Field(None, description="GitHub URL")
    portfolio: Optional[str] = Field(None, description="Portfolio URL")
    
    # Structured data
    summary: str = Field(..., description="Professional summary")
    experience: List[Experience] = Field(default_factory=list, description="Work experience")
    education: List[Education] = Field(default_factory=list, description="Education")
    skills: List[Skill] = Field(default_factory=list, description="Skills")
    projects: List[Project] = Field(default_factory=list, description="Projects")
    certifications: List[Certification] = Field(default_factory=list, description="Certifications")
    
    # AI analysis
    ai_score: Optional[float] = Field(None, ge=0.0, le=100.0, description="AI-generated resume score")
    ai_feedback: List[str] = Field(default_factory=list, description="AI feedback and suggestions")
    keywords: List[str] = Field(default_factory=list, description="Extracted keywords")
    industry: Optional[str] = Field(None, description="Detected industry")
    seniority_level: Optional[str] = Field(None, description="Detected seniority level")
    
    # Processing metadata
    status: ResumeStatus = Field(ResumeStatus.UPLOADED, description="Processing status")
    processing_time: Optional[float] = Field(None, description="Processing time in seconds")
    error_message: Optional[str] = Field(None, description="Error message if processing failed")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    
    class Config:
        """Pydantic configuration"""
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ResumeCreate(BaseModel):
    """Resume creation model"""
    filename: str = Field(..., description="Original filename")
    file_path: str = Field(..., description="File storage path")
    file_size: int = Field(..., description="File size in bytes")
    file_type: str = Field(..., description="File type")
    
    @validator('file_type')
    def validate_file_type(cls, v):
        """Validate file type"""
        allowed_types = ['pdf', 'docx', 'doc']
        if v.lower() not in allowed_types:
            raise ValueError(f"File type must be one of: {allowed_types}")
        return v.lower()

class ResumeUpdate(BaseModel):
    """Resume update model"""
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None
    summary: Optional[str] = None
    experience: Optional[List[Experience]] = None
    education: Optional[List[Education]] = None
    skills: Optional[List[Skill]] = None
    projects: Optional[List[Project]] = None
    certifications: Optional[List[Certification]] = None

class ResumeResponse(BaseModel):
    """Resume response model"""
    id: int
    user_id: int
    filename: str
    name: str
    email: str
    phone: Optional[str]
    location: Optional[str]
    summary: str
    experience: List[Experience]
    education: List[Education]
    skills: List[Skill]
    projects: List[Project]
    certifications: List[Certification]
    ai_score: Optional[float]
    ai_feedback: List[str]
    keywords: List[str]
    industry: Optional[str]
    seniority_level: Optional[str]
    status: ResumeStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        """Pydantic configuration"""
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ResumeAnalysis(BaseModel):
    """Resume analysis model"""
    resume_id: int
    overall_score: float = Field(..., ge=0.0, le=100.0, description="Overall resume score")
    strengths: List[str] = Field(default_factory=list, description="Resume strengths")
    weaknesses: List[str] = Field(default_factory=list, description="Areas for improvement")
    suggestions: List[str] = Field(default_factory=list, description="Specific suggestions")
    keyword_match_score: float = Field(..., ge=0.0, le=1.0, description="Keyword matching score")
    formatting_score: float = Field(..., ge=0.0, le=1.0, description="Formatting and presentation score")
    content_score: float = Field(..., ge=0.0, le=1.0, description="Content quality score")
    industry_relevance: float = Field(..., ge=0.0, le=1.0, description="Industry relevance score")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ResumeSearchFilters(BaseModel):
    """Resume search filters"""
    skills: Optional[List[str]] = None
    experience_years: Optional[int] = None
    education_level: Optional[str] = None
    location: Optional[str] = None
    industry: Optional[str] = None
    seniority_level: Optional[str] = None
    has_certifications: Optional[bool] = None
    has_projects: Optional[bool] = None
