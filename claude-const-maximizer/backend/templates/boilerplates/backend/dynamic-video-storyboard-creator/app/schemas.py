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


class StoryboardBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    data: Optional[Dict[str, Any]] = None

class StoryboardCreate(StoryboardBase):
    pass

class StoryboardResponse(StoryboardBase):
    id: int
    created_by_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class SceneBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    data: Optional[Dict[str, Any]] = None

class SceneCreate(SceneBase):
    pass

class SceneResponse(SceneBase):
    id: int
    created_by_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class VisualBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    data: Optional[Dict[str, Any]] = None

class VisualCreate(VisualBase):
    pass

class VisualResponse(VisualBase):
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
