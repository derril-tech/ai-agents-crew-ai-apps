from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# Base schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., regex=r"^[^@]+@[^@]+\.[^@]+$")
    full_name: str = Field(..., min_length=2, max_length=100)
    role: str = Field(default="user")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class KnowledgeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    data: Optional[Dict[str, Any]] = None

class KnowledgeCreate(KnowledgeBase):
    pass

class KnowledgeResponse(KnowledgeBase):
    id: int
    created_by_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class MemoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    data: Optional[Dict[str, Any]] = None

class MemoryCreate(MemoryBase):
    pass

class MemoryResponse(MemoryBase):
    id: int
    created_by_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class AgentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    data: Optional[Dict[str, Any]] = None

class AgentCreate(AgentBase):
    pass

class AgentResponse(AgentBase):
    id: int
    created_by_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# AI-specific schemas
class AnalysisResult(BaseModel):
    analysis_id: int = Field(..., description="ID of the analysis")
    results: List[Dict[str, Any]] = Field(..., description="Analysis results")
    recommendations: List[str] = Field(..., description="AI recommendations")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="AI confidence score")
