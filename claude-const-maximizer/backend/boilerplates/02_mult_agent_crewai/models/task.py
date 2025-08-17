"""
Task model for Multi-Agent CrewAI Backend
"""

import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import Column, String, Text, Boolean, DateTime, Integer, ForeignKey, Enum, Float, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from models.base import BaseModel


class TaskStatus(enum.Enum):
    """Task status enumeration"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"
    BLOCKED = "blocked"


class TaskPriority(enum.Enum):
    """Task priority enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"
    CRITICAL = "critical"


class TaskType(enum.Enum):
    """Task type enumeration"""
    RESEARCH = "research"
    ANALYSIS = "analysis"
    WRITING = "writing"
    CODING = "coding"
    TESTING = "testing"
    REVIEW = "review"
    APPROVAL = "approval"
    NOTIFICATION = "notification"
    INTEGRATION = "integration"
    CUSTOM = "custom"


class Task(BaseModel):
    """Task model for agent task management"""
    
    # Basic information
    title = Column(String(500), nullable=False, index=True)
    description = Column(Text, nullable=True)
    task_type = Column(Enum(TaskType), default=TaskType.CUSTOM, nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False)
    
    # Task details
    instructions = Column(Text, nullable=True)  # Detailed task instructions
    expected_output = Column(Text, nullable=True)  # Expected output format
    requirements = Column(Text, nullable=True)  # JSON array of requirements
    constraints = Column(Text, nullable=True)  # JSON array of constraints
    
    # Assignment and ownership
    assignee_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=True)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agent.id"), nullable=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey("project.id"), nullable=True)
    workflow_id = Column(UUID(as_uuid=True), ForeignKey("workflow.id"), nullable=True)
    
    # Task dependencies
    dependencies = Column(Text, nullable=True)  # JSON array of task IDs
    dependent_tasks = Column(Text, nullable=True)  # JSON array of dependent task IDs
    
    # Timing and scheduling
    estimated_duration = Column(Integer, nullable=True)  # In minutes
    actual_duration = Column(Integer, nullable=True)  # In minutes
    due_date = Column(DateTime, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Progress tracking
    progress_percentage = Column(Integer, default=0, nullable=False)
    current_step = Column(String(200), nullable=True)
    total_steps = Column(Integer, default=1, nullable=False)
    
    # Results and output
    result_data = Column(Text, nullable=True)  # JSON object for task results
    output_files = Column(Text, nullable=True)  # JSON array of output file paths
    error_message = Column(Text, nullable=True)
    error_details = Column(Text, nullable=True)  # JSON object for error details
    
    # Performance metrics
    tokens_used = Column(Integer, default=0, nullable=False)
    cost = Column(Float, default=0.0, nullable=False)  # In USD
    retry_count = Column(Integer, default=0, nullable=False)
    max_retries = Column(Integer, default=3, nullable=False)
    
    # Task configuration
    timeout_minutes = Column(Integer, default=60, nullable=False)
    allow_parallel = Column(Boolean, default=False, nullable=False)
    auto_retry = Column(Boolean, default=True, nullable=False)
    notify_on_completion = Column(Boolean, default=True, nullable=False)
    
    # Metadata and tags
    tags = Column(Text, nullable=True)  # JSON array of tags
    category = Column(String(100), nullable=True)
    complexity_score = Column(Float, default=1.0, nullable=False)  # 1-10 scale
    
    # Relationships
    assignee = relationship("User", back_populates="tasks")
    agent = relationship("Agent", back_populates="tasks")
    project = relationship("Project", back_populates="tasks")
    workflow = relationship("Workflow", back_populates="tasks")
    
    def __repr__(self) -> str:
        return f"<Task(id={self.id}, title={self.title}, status={self.status.value})>"
    
    @property
    def is_completed(self) -> bool:
        """Check if task is completed"""
        return self.status == TaskStatus.COMPLETED
    
    @property
    def is_failed(self) -> bool:
        """Check if task has failed"""
        return self.status == TaskStatus.FAILED
    
    @property
    def is_in_progress(self) -> bool:
        """Check if task is in progress"""
        return self.status == TaskStatus.IN_PROGRESS
    
    @property
    def is_pending(self) -> bool:
        """Check if task is pending"""
        return self.status == TaskStatus.PENDING
    
    @property
    def is_overdue(self) -> bool:
        """Check if task is overdue"""
        if not self.due_date:
            return False
        return datetime.utcnow() > self.due_date and not self.is_completed
    
    @property
    def time_remaining(self) -> Optional[int]:
        """Get time remaining in minutes"""
        if not self.due_date:
            return None
        remaining = (self.due_date - datetime.utcnow()).total_seconds() / 60
        return max(0, int(remaining))
    
    @property
    def duration_minutes(self) -> Optional[int]:
        """Get actual duration in minutes"""
        if not self.started_at or not self.completed_at:
            return None
        return int((self.completed_at - self.started_at).total_seconds() / 60)
    
    @property
    def efficiency_score(self) -> float:
        """Calculate efficiency score"""
        if not self.estimated_duration or not self.actual_duration:
            return 0.0
        return min(2.0, self.estimated_duration / self.actual_duration)
    
    def get_requirements(self) -> List[str]:
        """Get task requirements as list"""
        if self.requirements:
            import json
            try:
                return json.loads(self.requirements)
            except (json.JSONDecodeError, TypeError):
                return []
        return []
    
    def set_requirements(self, requirements: List[str]) -> None:
        """Set task requirements from list"""
        import json
        self.requirements = json.dumps(requirements)
    
    def get_constraints(self) -> List[str]:
        """Get task constraints as list"""
        if self.constraints:
            import json
            try:
                return json.loads(self.constraints)
            except (json.JSONDecodeError, TypeError):
                return []
        return []
    
    def set_constraints(self, constraints: List[str]) -> None:
        """Set task constraints from list"""
        import json
        self.constraints = json.dumps(constraints)
    
    def get_dependencies(self) -> List[uuid.UUID]:
        """Get task dependencies as list"""
        if self.dependencies:
            import json
            try:
                return [uuid.UUID(task_id) for task_id in json.loads(self.dependencies)]
            except (json.JSONDecodeError, TypeError, ValueError):
                return []
        return []
    
    def set_dependencies(self, task_ids: List[uuid.UUID]) -> None:
        """Set task dependencies from list"""
        import json
        self.dependencies = json.dumps([str(task_id) for task_id in task_ids])
    
    def add_dependency(self, task_id: uuid.UUID) -> None:
        """Add a dependency to the task"""
        dependencies = self.get_dependencies()
        if task_id not in dependencies:
            dependencies.append(task_id)
            self.set_dependencies(dependencies)
    
    def remove_dependency(self, task_id: uuid.UUID) -> None:
        """Remove a dependency from the task"""
        dependencies = self.get_dependencies()
        if task_id in dependencies:
            dependencies.remove(task_id)
            self.set_dependencies(dependencies)
    
    def get_dependent_tasks(self) -> List[uuid.UUID]:
        """Get dependent tasks as list"""
        if self.dependent_tasks:
            import json
            try:
                return [uuid.UUID(task_id) for task_id in json.loads(self.dependent_tasks)]
            except (json.JSONDecodeError, TypeError, ValueError):
                return []
        return []
    
    def set_dependent_tasks(self, task_ids: List[uuid.UUID]) -> None:
        """Set dependent tasks from list"""
        import json
        self.dependent_tasks = json.dumps([str(task_id) for task_id in task_ids])
    
    def get_result_data(self) -> Dict[str, Any]:
        """Get task result data as dictionary"""
        if self.result_data:
            import json
            try:
                return json.loads(self.result_data)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}
    
    def set_result_data(self, data: Dict[str, Any]) -> None:
        """Set task result data from dictionary"""
        import json
        self.result_data = json.dumps(data)
    
    def update_result_data(self, data: Dict[str, Any]) -> None:
        """Update task result data by merging with existing"""
        current = self.get_result_data()
        current.update(data)
        self.set_result_data(current)
    
    def get_output_files(self) -> List[str]:
        """Get output files as list"""
        if self.output_files:
            import json
            try:
                return json.loads(self.output_files)
            except (json.JSONDecodeError, TypeError):
                return []
        return []
    
    def set_output_files(self, files: List[str]) -> None:
        """Set output files from list"""
        import json
        self.output_files = json.dumps(files)
    
    def add_output_file(self, file_path: str) -> None:
        """Add an output file to the task"""
        files = self.get_output_files()
        if file_path not in files:
            files.append(file_path)
            self.set_output_files(files)
    
    def get_error_details(self) -> Dict[str, Any]:
        """Get error details as dictionary"""
        if self.error_details:
            import json
            try:
                return json.loads(self.error_details)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}
    
    def set_error_details(self, details: Dict[str, Any]) -> None:
        """Set error details from dictionary"""
        import json
        self.error_details = json.dumps(details)
    
    def get_tags(self) -> List[str]:
        """Get task tags as list"""
        if self.tags:
            import json
            try:
                return json.loads(self.tags)
            except (json.JSONDecodeError, TypeError):
                return []
        return []
    
    def set_tags(self, tags: List[str]) -> None:
        """Set task tags from list"""
        import json
        self.tags = json.dumps(tags)
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to the task"""
        tags = self.get_tags()
        if tag not in tags:
            tags.append(tag)
            self.set_tags(tags)
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the task"""
        tags = self.get_tags()
        if tag in tags:
            tags.remove(tag)
            self.set_tags(tags)
    
    def start_task(self) -> None:
        """Start the task"""
        if self.status == TaskStatus.PENDING:
            self.status = TaskStatus.IN_PROGRESS
            self.started_at = datetime.utcnow()
            self.progress_percentage = 0
    
    def complete_task(self, result_data: Dict[str, Any] = None) -> None:
        """Complete the task"""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.utcnow()
        self.progress_percentage = 100
        
        if result_data:
            self.set_result_data(result_data)
    
    def fail_task(self, error_message: str, error_details: Dict[str, Any] = None) -> None:
        """Mark task as failed"""
        self.status = TaskStatus.FAILED
        self.error_message = error_message
        
        if error_details:
            self.set_error_details(error_details)
    
    def pause_task(self) -> None:
        """Pause the task"""
        if self.status == TaskStatus.IN_PROGRESS:
            self.status = TaskStatus.PAUSED
    
    def resume_task(self) -> None:
        """Resume the task"""
        if self.status == TaskStatus.PAUSED:
            self.status = TaskStatus.IN_PROGRESS
    
    def cancel_task(self) -> None:
        """Cancel the task"""
        if self.status in [TaskStatus.PENDING, TaskStatus.IN_PROGRESS, TaskStatus.PAUSED]:
            self.status = TaskStatus.CANCELLED
    
    def retry_task(self) -> None:
        """Retry the task"""
        if self.status == TaskStatus.FAILED and self.retry_count < self.max_retries:
            self.status = TaskStatus.PENDING
            self.retry_count += 1
            self.error_message = None
            self.error_details = None
            self.started_at = None
            self.completed_at = None
            self.progress_percentage = 0
    
    def update_progress(self, percentage: int, current_step: str = None) -> None:
        """Update task progress"""
        self.progress_percentage = max(0, min(100, percentage))
        if current_step:
            self.current_step = current_step
        
        # Auto-complete if progress reaches 100%
        if self.progress_percentage == 100 and not self.completed_at:
            self.complete_task()
    
    def increment_step(self) -> None:
        """Increment task step"""
        if self.current_step_number < self.total_steps:
            self.current_step_number += 1
            progress = (self.current_step_number / self.total_steps) * 100
            self.update_progress(int(progress))
    
    def add_cost(self, amount: float) -> None:
        """Add cost to the task"""
        self.cost += amount
    
    def add_tokens(self, count: int) -> None:
        """Add tokens to the task"""
        self.tokens_used += count
    
    def can_start(self) -> bool:
        """Check if task can be started"""
        if self.status != TaskStatus.PENDING:
            return False
        
        # Check if dependencies are completed
        dependencies = self.get_dependencies()
        if dependencies:
            # This would need to be checked against the database
            # For now, we'll assume dependencies are met
            pass
        
        return True
    
    def is_blocked(self) -> bool:
        """Check if task is blocked by dependencies"""
        dependencies = self.get_dependencies()
        if not dependencies:
            return False
        
        # This would need to be checked against the database
        # For now, we'll assume it's not blocked
        return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get task statistics"""
        return {
            "duration_minutes": self.duration_minutes,
            "efficiency_score": self.efficiency_score,
            "time_remaining": self.time_remaining,
            "is_overdue": self.is_overdue,
            "retry_count": self.retry_count,
            "tokens_used": self.tokens_used,
            "cost": self.cost,
            "progress_percentage": self.progress_percentage,
            "complexity_score": self.complexity_score,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "due_date": self.due_date.isoformat() if self.due_date else None
        }
    
    def duplicate(self, new_title: str) -> "Task":
        """Create a duplicate of this task"""
        duplicate = Task(
            title=new_title,
            description=self.description,
            task_type=self.task_type,
            status=TaskStatus.PENDING,  # Start as pending
            priority=self.priority,
            instructions=self.instructions,
            expected_output=self.expected_output,
            requirements=self.requirements,
            constraints=self.constraints,
            assignee_id=self.assignee_id,
            agent_id=self.agent_id,
            project_id=self.project_id,
            workflow_id=self.workflow_id,
            estimated_duration=self.estimated_duration,
            due_date=self.due_date,
            timeout_minutes=self.timeout_minutes,
            allow_parallel=self.allow_parallel,
            auto_retry=self.auto_retry,
            notify_on_completion=self.notify_on_completion,
            tags=self.tags,
            category=self.category,
            complexity_score=self.complexity_score
        )
        return duplicate
    
    def validate(self) -> bool:
        """Validate task data"""
        errors = self.get_validation_errors()
        return len(errors) == 0
    
    def get_validation_errors(self) -> List[str]:
        """Get validation errors"""
        errors = []
        
        if not self.title:
            errors.append("Task title is required")
        elif len(self.title) < 1:
            errors.append("Task title must be at least 1 character")
        elif len(self.title) > 500:
            errors.append("Task title must be less than 500 characters")
        
        if self.progress_percentage < 0 or self.progress_percentage > 100:
            errors.append("Progress percentage must be between 0 and 100")
        
        if self.total_steps < 1:
            errors.append("Total steps must be at least 1")
        
        if self.estimated_duration is not None and self.estimated_duration < 0:
            errors.append("Estimated duration cannot be negative")
        
        if self.actual_duration is not None and self.actual_duration < 0:
            errors.append("Actual duration cannot be negative")
        
        if self.timeout_minutes < 1:
            errors.append("Timeout must be at least 1 minute")
        
        if self.max_retries < 0:
            errors.append("Max retries cannot be negative")
        
        if self.retry_count < 0:
            errors.append("Retry count cannot be negative")
        
        if self.tokens_used < 0:
            errors.append("Tokens used cannot be negative")
        
        if self.cost < 0.0:
            errors.append("Cost cannot be negative")
        
        if self.complexity_score < 1.0 or self.complexity_score > 10.0:
            errors.append("Complexity score must be between 1.0 and 10.0")
        
        return errors
    
    @classmethod
    def get_by_status(cls, session, status: TaskStatus) -> List["Task"]:
        """Get tasks by status"""
        return session.query(cls).filter(
            cls.status == status,
            cls.is_deleted == False
        ).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_by_priority(cls, session, priority: TaskPriority) -> List["Task"]:
        """Get tasks by priority"""
        return session.query(cls).filter(
            cls.priority == priority,
            cls.is_deleted == False
        ).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_by_type(cls, session, task_type: TaskType) -> List["Task"]:
        """Get tasks by type"""
        return session.query(cls).filter(
            cls.task_type == task_type,
            cls.is_deleted == False
        ).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_by_assignee(cls, session, assignee_id: uuid.UUID) -> List["Task"]:
        """Get tasks by assignee"""
        return session.query(cls).filter(
            cls.assignee_id == assignee_id,
            cls.is_deleted == False
        ).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_by_agent(cls, session, agent_id: uuid.UUID) -> List["Task"]:
        """Get tasks by agent"""
        return session.query(cls).filter(
            cls.agent_id == agent_id,
            cls.is_deleted == False
        ).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_by_project(cls, session, project_id: uuid.UUID) -> List["Task"]:
        """Get tasks by project"""
        return session.query(cls).filter(
            cls.project_id == project_id,
            cls.is_deleted == False
        ).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_overdue_tasks(cls, session) -> List["Task"]:
        """Get overdue tasks"""
        return session.query(cls).filter(
            cls.due_date < datetime.utcnow(),
            cls.status.in_([TaskStatus.PENDING, TaskStatus.IN_PROGRESS]),
            cls.is_deleted == False
        ).order_by(cls.due_date.asc()).all()
    
    @classmethod
    def get_ready_tasks(cls, session) -> List["Task"]:
        """Get tasks ready to start"""
        return session.query(cls).filter(
            cls.status == TaskStatus.PENDING,
            cls.is_deleted == False
        ).order_by(cls.priority.desc(), cls.created_at.asc()).all()
    
    @classmethod
    def search(cls, session, query: str, status: TaskStatus = None) -> List["Task"]:
        """Search tasks"""
        search_query = session.query(cls).filter(cls.is_deleted == False)
        
        # Add search conditions
        search_query = search_query.filter(
            (cls.title.ilike(f"%{query}%")) |
            (cls.description.ilike(f"%{query}%")) |
            (cls.instructions.ilike(f"%{query}%"))
        )
        
        # Filter by status if specified
        if status:
            search_query = search_query.filter(cls.status == status)
        
        return search_query.order_by(cls.created_at.desc()).all()

