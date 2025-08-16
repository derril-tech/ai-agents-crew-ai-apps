"""
Project model for Multi-Agent CrewAI Backend
"""

import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import Column, String, Text, Boolean, DateTime, Integer, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from models.base import BaseModel


class ProjectStatus(enum.Enum):
    """Project status enumeration"""
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"
    CANCELLED = "cancelled"


class ProjectType(enum.Enum):
    """Project type enumeration"""
    RESEARCH = "research"
    MARKETING = "marketing"
    DEVELOPMENT = "development"
    BUSINESS = "business"
    HEALTHCARE = "healthcare"
    LEGAL = "legal"
    ECOMMERCE = "ecommerce"
    CYBERSECURITY = "cybersecurity"
    EDUCATION = "education"
    CUSTOM = "custom"


class Project(BaseModel):
    """Project model for organizing agents and workflows"""
    
    # Basic information
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    slug = Column(String(200), unique=True, nullable=False, index=True)
    
    # Project details
    status = Column(Enum(ProjectStatus), default=ProjectStatus.DRAFT, nullable=False)
    project_type = Column(Enum(ProjectType), default=ProjectType.CUSTOM, nullable=False)
    priority = Column(Integer, default=1, nullable=False)  # 1-5, 5 being highest
    
    # Ownership and access
    owner_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    is_public = Column(Boolean, default=False, nullable=False)
    is_template = Column(Boolean, default=False, nullable=False)
    
    # Project configuration
    settings_json = Column(Text, nullable=True)  # JSON string for project settings
    tags = Column(Text, nullable=True)  # JSON array of tags
    
    # Progress tracking
    progress_percentage = Column(Integer, default=0, nullable=False)
    estimated_completion = Column(DateTime, nullable=True)
    actual_completion = Column(DateTime, nullable=True)
    
    # Budget and resources
    budget_limit = Column(Integer, nullable=True)  # In cents
    budget_used = Column(Integer, default=0, nullable=False)  # In cents
    resource_limits = Column(Text, nullable=True)  # JSON object for resource limits
    
    # Performance metrics
    total_executions = Column(Integer, default=0, nullable=False)
    successful_executions = Column(Integer, default=0, nullable=False)
    failed_executions = Column(Integer, default=0, nullable=False)
    average_execution_time = Column(Integer, nullable=True)  # In seconds
    
    # Collaboration
    collaborators = Column(Text, nullable=True)  # JSON array of user IDs
    shared_with = Column(Text, nullable=True)  # JSON array of user IDs with read access
    
    # Notifications
    notification_settings = Column(Text, nullable=True)  # JSON object for notification preferences
    
    # Relationships
    owner = relationship("User", back_populates="projects")
    agents = relationship("Agent", back_populates="project", cascade="all, delete-orphan")
    workflows = relationship("Workflow", back_populates="project", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    executions = relationship("Execution", back_populates="project", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Project(id={self.id}, name={self.name}, status={self.status.value})>"
    
    @property
    def is_active(self) -> bool:
        """Check if project is active"""
        return self.status in [ProjectStatus.ACTIVE, ProjectStatus.DRAFT]
    
    @property
    def is_completed(self) -> bool:
        """Check if project is completed"""
        return self.status == ProjectStatus.COMPLETED
    
    @property
    def budget_remaining(self) -> Optional[int]:
        """Get remaining budget"""
        if self.budget_limit is None:
            return None
        return max(0, self.budget_limit - self.budget_used)
    
    @property
    def budget_usage_percentage(self) -> float:
        """Get budget usage percentage"""
        if self.budget_limit is None or self.budget_limit == 0:
            return 0.0
        return min(100.0, (self.budget_used / self.budget_limit) * 100)
    
    @property
    def success_rate(self) -> float:
        """Get execution success rate"""
        if self.total_executions == 0:
            return 0.0
        return (self.successful_executions / self.total_executions) * 100
    
    @property
    def failure_rate(self) -> float:
        """Get execution failure rate"""
        if self.total_executions == 0:
            return 0.0
        return (self.failed_executions / self.total_executions) * 100
    
    def get_settings(self) -> Dict[str, Any]:
        """Get project settings as dictionary"""
        if self.settings_json:
            import json
            try:
                return json.loads(self.settings_json)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}
    
    def set_settings(self, settings: Dict[str, Any]) -> None:
        """Set project settings from dictionary"""
        import json
        self.settings_json = json.dumps(settings)
    
    def update_settings(self, settings: Dict[str, Any]) -> None:
        """Update project settings by merging with existing"""
        current = self.get_settings()
        current.update(settings)
        self.set_settings(current)
    
    def get_tags(self) -> List[str]:
        """Get project tags as list"""
        if self.tags:
            import json
            try:
                return json.loads(self.tags)
            except (json.JSONDecodeError, TypeError):
                return []
        return []
    
    def set_tags(self, tags: List[str]) -> None:
        """Set project tags from list"""
        import json
        self.tags = json.dumps(tags)
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to the project"""
        tags = self.get_tags()
        if tag not in tags:
            tags.append(tag)
            self.set_tags(tags)
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the project"""
        tags = self.get_tags()
        if tag in tags:
            tags.remove(tag)
            self.set_tags(tags)
    
    def get_resource_limits(self) -> Dict[str, Any]:
        """Get resource limits as dictionary"""
        if self.resource_limits:
            import json
            try:
                return json.loads(self.resource_limits)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}
    
    def set_resource_limits(self, limits: Dict[str, Any]) -> None:
        """Set resource limits from dictionary"""
        import json
        self.resource_limits = json.dumps(limits)
    
    def get_collaborators(self) -> List[uuid.UUID]:
        """Get collaborator user IDs as list"""
        if self.collaborators:
            import json
            try:
                return [uuid.UUID(uid) for uid in json.loads(self.collaborators)]
            except (json.JSONDecodeError, TypeError, ValueError):
                return []
        return []
    
    def set_collaborators(self, collaborator_ids: List[uuid.UUID]) -> None:
        """Set collaborators from list of user IDs"""
        import json
        self.collaborators = json.dumps([str(uid) for uid in collaborator_ids])
    
    def add_collaborator(self, user_id: uuid.UUID) -> None:
        """Add a collaborator to the project"""
        collaborators = self.get_collaborators()
        if user_id not in collaborators:
            collaborators.append(user_id)
            self.set_collaborators(collaborators)
    
    def remove_collaborator(self, user_id: uuid.UUID) -> None:
        """Remove a collaborator from the project"""
        collaborators = self.get_collaborators()
        if user_id in collaborators:
            collaborators.remove(user_id)
            self.set_collaborators(collaborators)
    
    def get_shared_with(self) -> List[uuid.UUID]:
        """Get users with read access as list"""
        if self.shared_with:
            import json
            try:
                return [uuid.UUID(uid) for uid in json.loads(self.shared_with)]
            except (json.JSONDecodeError, TypeError, ValueError):
                return []
        return []
    
    def set_shared_with(self, user_ids: List[uuid.UUID]) -> None:
        """Set users with read access from list of user IDs"""
        import json
        self.shared_with = json.dumps([str(uid) for uid in user_ids])
    
    def share_with(self, user_id: uuid.UUID) -> None:
        """Share project with a user (read access)"""
        shared_with = self.get_shared_with()
        if user_id not in shared_with:
            shared_with.append(user_id)
            self.set_shared_with(shared_with)
    
    def unshare_with(self, user_id: uuid.UUID) -> None:
        """Remove read access for a user"""
        shared_with = self.get_shared_with()
        if user_id in shared_with:
            shared_with.remove(user_id)
            self.set_shared_with(shared_with)
    
    def get_notification_settings(self) -> Dict[str, Any]:
        """Get notification settings as dictionary"""
        if self.notification_settings:
            import json
            try:
                return json.loads(self.notification_settings)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}
    
    def set_notification_settings(self, settings: Dict[str, Any]) -> None:
        """Set notification settings from dictionary"""
        import json
        self.notification_settings = json.dumps(settings)
    
    def update_progress(self, percentage: int) -> None:
        """Update project progress"""
        self.progress_percentage = max(0, min(100, percentage))
        if self.progress_percentage == 100 and not self.actual_completion:
            self.actual_completion = datetime.utcnow()
            self.status = ProjectStatus.COMPLETED
    
    def increment_execution(self, success: bool, execution_time: int = None) -> None:
        """Increment execution counters"""
        self.total_executions += 1
        if success:
            self.successful_executions += 1
        else:
            self.failed_executions += 1
        
        # Update average execution time
        if execution_time is not None:
            if self.average_execution_time is None:
                self.average_execution_time = execution_time
            else:
                total_time = self.average_execution_time * (self.total_executions - 1) + execution_time
                self.average_execution_time = total_time // self.total_executions
    
    def add_budget_usage(self, amount: int) -> None:
        """Add budget usage"""
        self.budget_used += amount
    
    def can_user_access(self, user_id: uuid.UUID) -> bool:
        """Check if user can access this project"""
        # Owner always has access
        if self.owner_id == user_id:
            return True
        
        # Public projects can be accessed by anyone
        if self.is_public:
            return True
        
        # Check collaborators
        if user_id in self.get_collaborators():
            return True
        
        # Check shared users
        if user_id in self.get_shared_with():
            return True
        
        return False
    
    def can_user_edit(self, user_id: uuid.UUID) -> bool:
        """Check if user can edit this project"""
        # Owner can always edit
        if self.owner_id == user_id:
            return True
        
        # Collaborators can edit
        if user_id in self.get_collaborators():
            return True
        
        return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get project statistics"""
        return {
            "total_agents": len(self.agents),
            "total_workflows": len(self.workflows),
            "total_tasks": len(self.tasks),
            "total_executions": self.total_executions,
            "successful_executions": self.successful_executions,
            "failed_executions": self.failed_executions,
            "success_rate": self.success_rate,
            "failure_rate": self.failure_rate,
            "average_execution_time": self.average_execution_time,
            "progress_percentage": self.progress_percentage,
            "budget_used": self.budget_used,
            "budget_limit": self.budget_limit,
            "budget_remaining": self.budget_remaining,
            "budget_usage_percentage": self.budget_usage_percentage,
            "estimated_completion": self.estimated_completion.isoformat() if self.estimated_completion else None,
            "actual_completion": self.actual_completion.isoformat() if self.actual_completion else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    def duplicate(self, new_name: str, new_owner_id: uuid.UUID) -> "Project":
        """Create a duplicate of this project"""
        duplicate = Project(
            name=new_name,
            description=self.description,
            slug=f"{new_name.lower().replace(' ', '-')}-{uuid.uuid4().hex[:8]}",
            status=ProjectStatus.DRAFT,
            project_type=self.project_type,
            priority=self.priority,
            owner_id=new_owner_id,
            is_public=False,
            is_template=False,
            settings_json=self.settings_json,
            tags=self.tags,
            resource_limits=self.resource_limits,
            notification_settings=self.notification_settings
        )
        return duplicate
    
    def archive(self) -> None:
        """Archive the project"""
        self.status = ProjectStatus.ARCHIVED
    
    def unarchive(self) -> None:
        """Unarchive the project"""
        if self.status == ProjectStatus.ARCHIVED:
            self.status = ProjectStatus.DRAFT
    
    def cancel(self) -> None:
        """Cancel the project"""
        self.status = ProjectStatus.CANCELLED
    
    def pause(self) -> None:
        """Pause the project"""
        if self.status == ProjectStatus.ACTIVE:
            self.status = ProjectStatus.PAUSED
    
    def resume(self) -> None:
        """Resume the project"""
        if self.status == ProjectStatus.PAUSED:
            self.status = ProjectStatus.ACTIVE
    
    def activate(self) -> None:
        """Activate the project"""
        if self.status == ProjectStatus.DRAFT:
            self.status = ProjectStatus.ACTIVE
    
    def validate(self) -> bool:
        """Validate project data"""
        errors = self.get_validation_errors()
        return len(errors) == 0
    
    def get_validation_errors(self) -> List[str]:
        """Get validation errors"""
        errors = []
        
        if not self.name:
            errors.append("Project name is required")
        elif len(self.name) < 1:
            errors.append("Project name must be at least 1 character")
        elif len(self.name) > 200:
            errors.append("Project name must be less than 200 characters")
        
        if not self.slug:
            errors.append("Project slug is required")
        elif len(self.slug) < 1:
            errors.append("Project slug must be at least 1 character")
        elif len(self.slug) > 200:
            errors.append("Project slug must be less than 200 characters")
        
        if self.priority < 1 or self.priority > 5:
            errors.append("Priority must be between 1 and 5")
        
        if self.progress_percentage < 0 or self.progress_percentage > 100:
            errors.append("Progress percentage must be between 0 and 100")
        
        if self.budget_used < 0:
            errors.append("Budget used cannot be negative")
        
        if self.budget_limit is not None and self.budget_limit < 0:
            errors.append("Budget limit cannot be negative")
        
        return errors
    
    @classmethod
    def get_by_slug(cls, session, slug: str) -> Optional["Project"]:
        """Get project by slug"""
        return session.query(cls).filter(cls.slug == slug, cls.is_deleted == False).first()
    
    @classmethod
    def get_by_owner(cls, session, owner_id: uuid.UUID) -> List["Project"]:
        """Get projects by owner"""
        return session.query(cls).filter(
            cls.owner_id == owner_id,
            cls.is_deleted == False
        ).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_public_projects(cls, session) -> List["Project"]:
        """Get public projects"""
        return session.query(cls).filter(
            cls.is_public == True,
            cls.is_deleted == False
        ).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_templates(cls, session) -> List["Project"]:
        """Get project templates"""
        return session.query(cls).filter(
            cls.is_template == True,
            cls.is_deleted == False
        ).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def search(cls, session, query: str, user_id: uuid.UUID = None) -> List["Project"]:
        """Search projects"""
        search_query = session.query(cls).filter(cls.is_deleted == False)
        
        # Add search conditions
        search_query = search_query.filter(
            (cls.name.ilike(f"%{query}%")) |
            (cls.description.ilike(f"%{query}%"))
        )
        
        # Filter by access if user_id provided
        if user_id:
            search_query = search_query.filter(
                (cls.owner_id == user_id) |
                (cls.is_public == True) |
                (cls.collaborators.contains(str(user_id))) |
                (cls.shared_with.contains(str(user_id)))
            )
        
        return search_query.order_by(cls.created_at.desc()).all()
