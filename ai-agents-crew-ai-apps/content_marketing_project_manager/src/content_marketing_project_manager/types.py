from typing import List, Optional
from pydantic import BaseModel, Field

class TaskEstimate(BaseModel):
    task_name: str = Field(..., description="Name of the content task")
    format: str = Field(..., description="e.g., blog, video, email")
    estimated_time_hours: float = Field(..., description="Hours to complete")
    required_resources: List[str] = Field(..., description="Roles/tools required")
    target_publish_date: Optional[str] = Field(None, description="YYYY-MM-DD")
    dependencies: List[str] = Field(default_factory=list, description="Dependent tasks")

class TaskAssignment(BaseModel):
    task_name: str = Field(..., description="Name of the content task")
    assigned_to: str = Field(..., description="Team member")
    role: str = Field(..., description="e.g., writer, editor")
    start_date: Optional[str] = Field(None, description="YYYY-MM-DD")
    end_date: Optional[str] = Field(None, description="YYYY-MM-DD")
    justification: Optional[str] = Field(None, description="Why this match")

class Milestone(BaseModel):
    milestone_name: str = Field(..., description="Milestone label")
    tasks: List[str] = Field(..., description="Task names under this milestone")

class ProjectPlan(BaseModel):
    tasks: List[TaskEstimate] = Field(..., description="Detailed tasks")
    assignments: List[TaskAssignment] = Field(..., description="Task-to-person mapping")
    milestones: List[Milestone] = Field(default_factory=list, description="High-level milestones")
    content_calendar: Optional[str] = Field(None, description="Calendar summary or link")
