"""
Workflow model for Multi-Agent CrewAI Backend
"""

import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import Column, String, Text, Boolean, DateTime, Integer, ForeignKey, Enum, Float, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from models.base import BaseModel

# Association table for workflow-agent many-to-many relationship
workflow_agents = Table(
    'workflow_agents',
    BaseModel.metadata,
    Column('workflow_id', UUID(as_uuid=True), ForeignKey('workflow.id'), primary_key=True),
    Column('agent_id', UUID(as_uuid=True), ForeignKey('agent.id'), primary_key=True),
    Column('role', String(100), nullable=True),  # Role of agent in workflow
    Column('order', Integer, default=0, nullable=False),  # Order of agent in workflow
    Column('created_at', DateTime, default=datetime.utcnow, nullable=False)
)


class WorkflowStatus(enum.Enum):
    """Workflow status enumeration"""
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ERROR = "error"


class WorkflowType(enum.Enum):
    """Workflow type enumeration"""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"
    LOOP = "loop"
    HIERARCHICAL = "hierarchical"
    CUSTOM = "custom"


class WorkflowTrigger(enum.Enum):
    """Workflow trigger enumeration"""
    MANUAL = "manual"
    SCHEDULED = "scheduled"
    EVENT_DRIVEN = "event_driven"
    API_CALL = "api_call"
    WEBHOOK = "webhook"
    CONDITION = "condition"


class Workflow(BaseModel):
    """Workflow model for orchestrating agent tasks"""
    
    # Basic information
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    workflow_type = Column(Enum(WorkflowType), default=WorkflowType.SEQUENTIAL, nullable=False)
    status = Column(Enum(WorkflowStatus), default=WorkflowStatus.DRAFT, nullable=False)
    trigger_type = Column(Enum(WorkflowTrigger), default=WorkflowTrigger.MANUAL, nullable=False)
    
    # Workflow configuration
    steps = Column(Text, nullable=True)  # JSON array of workflow steps
    conditions = Column(Text, nullable=True)  # JSON object for conditional logic
    variables = Column(Text, nullable=True)  # JSON object for workflow variables
    settings = Column(Text, nullable=True)  # JSON object for workflow settings
    
    # Execution control
    max_concurrent_executions = Column(Integer, default=1, nullable=False)
    timeout_minutes = Column(Integer, default=1440, nullable=False)  # 24 hours default
    retry_policy = Column(Text, nullable=True)  # JSON object for retry configuration
    error_handling = Column(Text, nullable=True)  # JSON object for error handling
    
    # Scheduling and triggers
    schedule_cron = Column(String(100), nullable=True)  # Cron expression for scheduling
    trigger_conditions = Column(Text, nullable=True)  # JSON object for trigger conditions
    webhook_url = Column(String(500), nullable=True)
    api_endpoint = Column(String(200), nullable=True)
    
    # Performance tracking
    total_executions = Column(Integer, default=0, nullable=False)
    successful_executions = Column(Integer, default=0, nullable=False)
    failed_executions = Column(Integer, default=0, nullable=False)
    average_execution_time = Column(Float, nullable=True)  # In minutes
    last_execution_at = Column(DateTime, nullable=True)
    
    # Resource usage
    total_tokens_used = Column(Integer, default=0, nullable=False)
    total_cost = Column(Float, default=0.0, nullable=False)  # In USD
    resource_limits = Column(Text, nullable=True)  # JSON object for resource limits
    
    # Monitoring and alerts
    enable_monitoring = Column(Boolean, default=True, nullable=False)
    alert_thresholds = Column(Text, nullable=True)  # JSON object for alert thresholds
    notification_settings = Column(Text, nullable=True)  # JSON object for notifications
    
    # Versioning and templates
    version = Column(String(20), default="1.0.0", nullable=False)
    is_template = Column(Boolean, default=False, nullable=False)
    template_category = Column(String(100), nullable=True)
    template_tags = Column(Text, nullable=True)  # JSON array of template tags
    
    # Access control
    is_public = Column(Boolean, default=False, nullable=False)
    allowed_users = Column(Text, nullable=True)  # JSON array of user IDs
    required_permissions = Column(Text, nullable=True)  # JSON array of required permissions
    
    # Relationships
    creator_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey("project.id"), nullable=True)
    
    creator = relationship("User", back_populates="workflows")
    project = relationship("Project", back_populates="workflows")
    agents = relationship("Agent", secondary=workflow_agents, back_populates="workflows")
    tasks = relationship("Task", back_populates="workflow", cascade="all, delete-orphan")
    executions = relationship("Execution", back_populates="workflow", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Workflow(id={self.id}, name={self.name}, type={self.workflow_type.value})>"
    
    @property
    def is_active(self) -> bool:
        """Check if workflow is active"""
        return self.status == WorkflowStatus.ACTIVE
    
    @property
    def is_completed(self) -> bool:
        """Check if workflow is completed"""
        return self.status == WorkflowStatus.COMPLETED
    
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
    
    @property
    def cost_per_execution(self) -> float:
        """Get average cost per execution"""
        if self.total_executions == 0:
            return 0.0
        return self.total_cost / self.total_executions
    
    @property
    def tokens_per_execution(self) -> float:
        """Get average tokens per execution"""
        if self.total_executions == 0:
            return 0.0
        return self.total_tokens_used / self.total_executions
    
    def get_steps(self) -> List[Dict[str, Any]]:
        """Get workflow steps as list"""
        if self.steps:
            import json
            try:
                return json.loads(self.steps)
            except (json.JSONDecodeError, TypeError):
                return []
        return []
    
    def set_steps(self, steps: List[Dict[str, Any]]) -> None:
        """Set workflow steps from list"""
        import json
        self.steps = json.dumps(steps)
    
    def add_step(self, step: Dict[str, Any]) -> None:
        """Add a step to the workflow"""
        steps = self.get_steps()
        step_id = step.get("id")
        if step_id:
            # Update existing step or add new one
            existing_step = next((s for s in steps if s.get("id") == step_id), None)
            if existing_step:
                steps.remove(existing_step)
            steps.append(step)
            self.set_steps(steps)
    
    def remove_step(self, step_id: str) -> None:
        """Remove a step from the workflow"""
        steps = self.get_steps()
        steps = [s for s in steps if s.get("id") != step_id]
        self.set_steps(steps)
    
    def get_conditions(self) -> Dict[str, Any]:
        """Get workflow conditions as dictionary"""
        if self.conditions:
            import json
            try:
                return json.loads(self.conditions)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}
    
    def set_conditions(self, conditions: Dict[str, Any]) -> None:
        """Set workflow conditions from dictionary"""
        import json
        self.conditions = json.dumps(conditions)
    
    def get_variables(self) -> Dict[str, Any]:
        """Get workflow variables as dictionary"""
        if self.variables:
            import json
            try:
                return json.loads(self.variables)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}
    
    def set_variables(self, variables: Dict[str, Any]) -> None:
        """Set workflow variables from dictionary"""
        import json
        self.variables = json.dumps(variables)
    
    def update_variables(self, variables: Dict[str, Any]) -> None:
        """Update workflow variables by merging with existing"""
        current = self.get_variables()
        current.update(variables)
        self.set_variables(current)
    
    def get_settings(self) -> Dict[str, Any]:
        """Get workflow settings as dictionary"""
        if self.settings:
            import json
            try:
                return json.loads(self.settings)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}
    
    def set_settings(self, settings: Dict[str, Any]) -> None:
        """Set workflow settings from dictionary"""
        import json
        self.settings = json.dumps(settings)
    
    def get_retry_policy(self) -> Dict[str, Any]:
        """Get retry policy as dictionary"""
        if self.retry_policy:
            import json
            try:
                return json.loads(self.retry_policy)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}
    
    def set_retry_policy(self, policy: Dict[str, Any]) -> None:
        """Set retry policy from dictionary"""
        import json
        self.retry_policy = json.dumps(policy)
    
    def get_error_handling(self) -> Dict[str, Any]:
        """Get error handling configuration as dictionary"""
        if self.error_handling:
            import json
            try:
                return json.loads(self.error_handling)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}
    
    def set_error_handling(self, handling: Dict[str, Any]) -> None:
        """Set error handling configuration from dictionary"""
        import json
        self.error_handling = json.dumps(handling)
    
    def get_trigger_conditions(self) -> Dict[str, Any]:
        """Get trigger conditions as dictionary"""
        if self.trigger_conditions:
            import json
            try:
                return json.loads(self.trigger_conditions)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}
    
    def set_trigger_conditions(self, conditions: Dict[str, Any]) -> None:
        """Set trigger conditions from dictionary"""
        import json
        self.trigger_conditions = json.dumps(conditions)
    
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
    
    def get_alert_thresholds(self) -> Dict[str, Any]:
        """Get alert thresholds as dictionary"""
        if self.alert_thresholds:
            import json
            try:
                return json.loads(self.alert_thresholds)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}
    
    def set_alert_thresholds(self, thresholds: Dict[str, Any]) -> None:
        """Set alert thresholds from dictionary"""
        import json
        self.alert_thresholds = json.dumps(thresholds)
    
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
    
    def get_template_tags(self) -> List[str]:
        """Get template tags as list"""
        if self.template_tags:
            import json
            try:
                return json.loads(self.template_tags)
            except (json.JSONDecodeError, TypeError):
                return []
        return []
    
    def set_template_tags(self, tags: List[str]) -> None:
        """Set template tags from list"""
        import json
        self.template_tags = json.dumps(tags)
    
    def get_allowed_users(self) -> List[uuid.UUID]:
        """Get allowed users as list"""
        if self.allowed_users:
            import json
            try:
                return [uuid.UUID(uid) for uid in json.loads(self.allowed_users)]
            except (json.JSONDecodeError, TypeError, ValueError):
                return []
        return []
    
    def set_allowed_users(self, user_ids: List[uuid.UUID]) -> None:
        """Set allowed users from list"""
        import json
        self.allowed_users = json.dumps([str(uid) for uid in user_ids])
    
    def get_required_permissions(self) -> List[str]:
        """Get required permissions as list"""
        if self.required_permissions:
            import json
            try:
                return json.loads(self.required_permissions)
            except (json.JSONDecodeError, TypeError):
                return []
        return []
    
    def set_required_permissions(self, permissions: List[str]) -> None:
        """Set required permissions from list"""
        import json
        self.required_permissions = json.dumps(permissions)
    
    def increment_execution(self, success: bool, execution_time: float = None, tokens: int = 0, cost: float = 0.0) -> None:
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
                self.average_execution_time = total_time / self.total_executions
        
        # Update resource usage
        self.total_tokens_used += tokens
        self.total_cost += cost
        self.last_execution_at = datetime.utcnow()
    
    def activate(self) -> None:
        """Activate the workflow"""
        if self.status == WorkflowStatus.DRAFT:
            self.status = WorkflowStatus.ACTIVE
    
    def pause(self) -> None:
        """Pause the workflow"""
        if self.status == WorkflowStatus.ACTIVE:
            self.status = WorkflowStatus.PAUSED
    
    def resume(self) -> None:
        """Resume the workflow"""
        if self.status == WorkflowStatus.PAUSED:
            self.status = WorkflowStatus.ACTIVE
    
    def complete(self) -> None:
        """Mark workflow as completed"""
        self.status = WorkflowStatus.COMPLETED
    
    def cancel(self) -> None:
        """Cancel the workflow"""
        if self.status in [WorkflowStatus.ACTIVE, WorkflowStatus.PAUSED]:
            self.status = WorkflowStatus.CANCELLED
    
    def set_error(self) -> None:
        """Set workflow as error state"""
        self.status = WorkflowStatus.ERROR
    
    def reset_stats(self) -> None:
        """Reset workflow statistics"""
        self.total_executions = 0
        self.successful_executions = 0
        self.failed_executions = 0
        self.average_execution_time = None
        self.total_tokens_used = 0
        self.total_cost = 0.0
        self.last_execution_at = None
    
    def can_user_access(self, user_id: uuid.UUID) -> bool:
        """Check if user can access this workflow"""
        # Creator always has access
        if self.creator_id == user_id:
            return True
        
        # Public workflows can be accessed by anyone
        if self.is_public:
            return True
        
        # Check allowed users
        if user_id in self.get_allowed_users():
            return True
        
        return False
    
    def can_user_execute(self, user_id: uuid.UUID) -> bool:
        """Check if user can execute this workflow"""
        if not self.can_user_access(user_id):
            return False
        
        # Check if workflow is active
        if not self.is_active:
            return False
        
        return True
    
    def get_stats(self) -> Dict[str, Any]:
        """Get workflow statistics"""
        return {
            "total_executions": self.total_executions,
            "successful_executions": self.successful_executions,
            "failed_executions": self.failed_executions,
            "success_rate": self.success_rate,
            "failure_rate": self.failure_rate,
            "average_execution_time": self.average_execution_time,
            "total_tokens_used": self.total_tokens_used,
            "total_cost": self.total_cost,
            "cost_per_execution": self.cost_per_execution,
            "tokens_per_execution": self.tokens_per_execution,
            "last_execution_at": self.last_execution_at.isoformat() if self.last_execution_at else None,
            "status": self.status.value,
            "is_active": self.is_active,
            "is_completed": self.is_completed
        }
    
    def duplicate(self, new_name: str, new_creator_id: uuid.UUID) -> "Workflow":
        """Create a duplicate of this workflow"""
        duplicate = Workflow(
            name=new_name,
            description=self.description,
            workflow_type=self.workflow_type,
            status=WorkflowStatus.DRAFT,  # Start as draft
            trigger_type=self.trigger_type,
            steps=self.steps,
            conditions=self.conditions,
            variables=self.variables,
            settings=self.settings,
            max_concurrent_executions=self.max_concurrent_executions,
            timeout_minutes=self.timeout_minutes,
            retry_policy=self.retry_policy,
            error_handling=self.error_handling,
            schedule_cron=self.schedule_cron,
            trigger_conditions=self.trigger_conditions,
            webhook_url=self.webhook_url,
            api_endpoint=self.api_endpoint,
            enable_monitoring=self.enable_monitoring,
            alert_thresholds=self.alert_thresholds,
            notification_settings=self.notification_settings,
            version=self.version,
            is_template=False,  # Duplicate is not a template
            template_category=self.template_category,
            template_tags=self.template_tags,
            is_public=False,  # Duplicate is private
            allowed_users=self.allowed_users,
            required_permissions=self.required_permissions,
            creator_id=new_creator_id,
            project_id=self.project_id
        )
        return duplicate
    
    def validate(self) -> bool:
        """Validate workflow data"""
        errors = self.get_validation_errors()
        return len(errors) == 0
    
    def get_validation_errors(self) -> List[str]:
        """Get validation errors"""
        errors = []
        
        if not self.name:
            errors.append("Workflow name is required")
        elif len(self.name) < 1:
            errors.append("Workflow name must be at least 1 character")
        elif len(self.name) > 200:
            errors.append("Workflow name must be less than 200 characters")
        
        if self.max_concurrent_executions < 1:
            errors.append("Max concurrent executions must be at least 1")
        
        if self.timeout_minutes < 1:
            errors.append("Timeout must be at least 1 minute")
        
        if self.total_executions < 0:
            errors.append("Total executions cannot be negative")
        
        if self.successful_executions < 0:
            errors.append("Successful executions cannot be negative")
        
        if self.failed_executions < 0:
            errors.append("Failed executions cannot be negative")
        
        if self.total_tokens_used < 0:
            errors.append("Total tokens used cannot be negative")
        
        if self.total_cost < 0.0:
            errors.append("Total cost cannot be negative")
        
        return errors
    
    @classmethod
    def get_by_type(cls, session, workflow_type: WorkflowType) -> List["Workflow"]:
        """Get workflows by type"""
        return session.query(cls).filter(
            cls.workflow_type == workflow_type,
            cls.is_deleted == False
        ).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_by_status(cls, session, status: WorkflowStatus) -> List["Workflow"]:
        """Get workflows by status"""
        return session.query(cls).filter(
            cls.status == status,
            cls.is_deleted == False
        ).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_by_trigger(cls, session, trigger_type: WorkflowTrigger) -> List["Workflow"]:
        """Get workflows by trigger type"""
        return session.query(cls).filter(
            cls.trigger_type == trigger_type,
            cls.is_deleted == False
        ).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_by_creator(cls, session, creator_id: uuid.UUID) -> List["Workflow"]:
        """Get workflows by creator"""
        return session.query(cls).filter(
            cls.creator_id == creator_id,
            cls.is_deleted == False
        ).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_by_project(cls, session, project_id: uuid.UUID) -> List["Workflow"]:
        """Get workflows by project"""
        return session.query(cls).filter(
            cls.project_id == project_id,
            cls.is_deleted == False
        ).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_templates(cls, session) -> List["Workflow"]:
        """Get workflow templates"""
        return session.query(cls).filter(
            cls.is_template == True,
            cls.is_deleted == False
        ).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_public_workflows(cls, session) -> List["Workflow"]:
        """Get public workflows"""
        return session.query(cls).filter(
            cls.is_public == True,
            cls.is_deleted == False
        ).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_active_workflows(cls, session) -> List["Workflow"]:
        """Get active workflows"""
        return session.query(cls).filter(
            cls.status == WorkflowStatus.ACTIVE,
            cls.is_deleted == False
        ).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def search(cls, session, query: str, workflow_type: WorkflowType = None) -> List["Workflow"]:
        """Search workflows"""
        search_query = session.query(cls).filter(cls.is_deleted == False)
        
        # Add search conditions
        search_query = search_query.filter(
            (cls.name.ilike(f"%{query}%")) |
            (cls.description.ilike(f"%{query}%"))
        )
        
        # Filter by type if specified
        if workflow_type:
            search_query = search_query.filter(cls.workflow_type == workflow_type)
        
        return search_query.order_by(cls.created_at.desc()).all()



