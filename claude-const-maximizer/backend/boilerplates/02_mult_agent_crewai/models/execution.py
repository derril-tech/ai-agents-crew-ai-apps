"""
Execution model for Multi-Agent CrewAI Backend
"""

import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import Column, String, Text, Boolean, DateTime, Integer, ForeignKey, Enum, Float, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from models.base import BaseModel


class ExecutionStatus(enum.Enum):
    """Execution status enumeration"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"
    PAUSED = "paused"


class ExecutionType(enum.Enum):
    """Execution type enumeration"""
    WORKFLOW = "workflow"
    TASK = "task"
    AGENT = "agent"
    BATCH = "batch"
    SCHEDULED = "scheduled"
    MANUAL = "manual"


class Execution(BaseModel):
    """Execution model for tracking workflow and task executions"""
    
    # Basic information
    execution_type = Column(Enum(ExecutionType), default=ExecutionType.MANUAL, nullable=False)
    status = Column(Enum(ExecutionStatus), default=ExecutionStatus.PENDING, nullable=False)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Execution details
    input_data = Column(Text, nullable=True)  # JSON object for input data
    output_data = Column(Text, nullable=True)  # JSON object for output data
    parameters = Column(Text, nullable=True)  # JSON object for execution parameters
    context = Column(Text, nullable=True)  # JSON object for execution context
    
    # Timing and scheduling
    scheduled_at = Column(DateTime, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    estimated_duration = Column(Integer, nullable=True)  # In minutes
    actual_duration = Column(Integer, nullable=True)  # In minutes
    
    # Progress tracking
    progress_percentage = Column(Integer, default=0, nullable=False)
    current_step = Column(String(200), nullable=True)
    total_steps = Column(Integer, default=1, nullable=False)
    completed_steps = Column(Integer, default=0, nullable=False)
    
    # Performance metrics
    tokens_used = Column(Integer, default=0, nullable=False)
    cost = Column(Float, default=0.0, nullable=False)  # In USD
    memory_usage = Column(Float, nullable=True)  # In MB
    cpu_usage = Column(Float, nullable=True)  # In percentage
    
    # Error handling
    error_message = Column(Text, nullable=True)
    error_details = Column(Text, nullable=True)  # JSON object for error details
    retry_count = Column(Integer, default=0, nullable=False)
    max_retries = Column(Integer, default=3, nullable=False)
    
    # Resource management
    resource_limits = Column(Text, nullable=True)  # JSON object for resource limits
    resource_usage = Column(Text, nullable=True)  # JSON object for resource usage
    timeout_minutes = Column(Integer, default=60, nullable=False)
    
    # Logging and monitoring
    logs = Column(Text, nullable=True)  # JSON array of log entries
    metrics = Column(Text, nullable=True)  # JSON object for execution metrics
    checkpoints = Column(Text, nullable=True)  # JSON array of execution checkpoints
    
    # Relationships
    executor_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey("project.id"), nullable=True)
    workflow_id = Column(UUID(as_uuid=True), ForeignKey("workflow.id"), nullable=True)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agent.id"), nullable=True)
    task_id = Column(UUID(as_uuid=True), ForeignKey("task.id"), nullable=True)
    
    executor = relationship("User", back_populates="executions")
    project = relationship("Project", back_populates="executions")
    workflow = relationship("Workflow", back_populates="executions")
    agent = relationship("Agent", back_populates="executions")
    task = relationship("Task", back_populates="executions")
    
    def __repr__(self) -> str:
        return f"<Execution(id={self.id}, name={self.name}, status={self.status.value})>"
    
    @property
    def is_completed(self) -> bool:
        """Check if execution is completed"""
        return self.status == ExecutionStatus.COMPLETED
    
    @property
    def is_failed(self) -> bool:
        """Check if execution has failed"""
        return self.status in [ExecutionStatus.FAILED, ExecutionStatus.TIMEOUT]
    
    @property
    def is_running(self) -> bool:
        """Check if execution is running"""
        return self.status == ExecutionStatus.RUNNING
    
    @property
    def is_pending(self) -> bool:
        """Check if execution is pending"""
        return self.status == ExecutionStatus.PENDING
    
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
    
    @property
    def is_overdue(self) -> bool:
        """Check if execution is overdue"""
        if not self.scheduled_at:
            return False
        return datetime.utcnow() > self.scheduled_at and not self.is_completed
    
    @property
    def time_remaining(self) -> Optional[int]:
        """Get time remaining in minutes"""
        if not self.timeout_minutes or not self.started_at:
            return None
        elapsed = (datetime.utcnow() - self.started_at).total_seconds() / 60
        remaining = self.timeout_minutes - elapsed
        return max(0, int(remaining))
    
    def get_input_data(self) -> Dict[str, Any]:
        """Get input data as dictionary"""
        if self.input_data:
            import json
            try:
                return json.loads(self.input_data)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}
    
    def set_input_data(self, data: Dict[str, Any]) -> None:
        """Set input data from dictionary"""
        import json
        self.input_data = json.dumps(data)
    
    def get_output_data(self) -> Dict[str, Any]:
        """Get output data as dictionary"""
        if self.output_data:
            import json
            try:
                return json.loads(self.output_data)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}
    
    def set_output_data(self, data: Dict[str, Any]) -> None:
        """Set output data from dictionary"""
        import json
        self.output_data = json.dumps(data)
    
    def update_output_data(self, data: Dict[str, Any]) -> None:
        """Update output data by merging with existing"""
        current = self.get_output_data()
        current.update(data)
        self.set_output_data(current)
    
    def get_parameters(self) -> Dict[str, Any]:
        """Get execution parameters as dictionary"""
        if self.parameters:
            import json
            try:
                return json.loads(self.parameters)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}
    
    def set_parameters(self, params: Dict[str, Any]) -> None:
        """Set execution parameters from dictionary"""
        import json
        self.parameters = json.dumps(params)
    
    def get_context(self) -> Dict[str, Any]:
        """Get execution context as dictionary"""
        if self.context:
            import json
            try:
                return json.loads(self.context)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}
    
    def set_context(self, context: Dict[str, Any]) -> None:
        """Set execution context from dictionary"""
        import json
        self.context = json.dumps(context)
    
    def update_context(self, context: Dict[str, Any]) -> None:
        """Update execution context by merging with existing"""
        current = self.get_context()
        current.update(context)
        self.set_context(current)
    
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
    
    def get_resource_usage(self) -> Dict[str, Any]:
        """Get resource usage as dictionary"""
        if self.resource_usage:
            import json
            try:
                return json.loads(self.resource_usage)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}
    
    def set_resource_usage(self, usage: Dict[str, Any]) -> None:
        """Set resource usage from dictionary"""
        import json
        self.resource_usage = json.dumps(usage)
    
    def get_logs(self) -> List[Dict[str, Any]]:
        """Get execution logs as list"""
        if self.logs:
            import json
            try:
                return json.loads(self.logs)
            except (json.JSONDecodeError, TypeError):
                return []
        return []
    
    def set_logs(self, logs: List[Dict[str, Any]]) -> None:
        """Set execution logs from list"""
        import json
        self.logs = json.dumps(logs)
    
    def add_log(self, level: str, message: str, details: Dict[str, Any] = None) -> None:
        """Add a log entry"""
        logs = self.get_logs()
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "message": message,
            "details": details or {}
        }
        logs.append(log_entry)
        self.set_logs(logs)
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get execution metrics as dictionary"""
        if self.metrics:
            import json
            try:
                return json.loads(self.metrics)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}
    
    def set_metrics(self, metrics: Dict[str, Any]) -> None:
        """Set execution metrics from dictionary"""
        import json
        self.metrics = json.dumps(metrics)
    
    def update_metrics(self, metrics: Dict[str, Any]) -> None:
        """Update execution metrics by merging with existing"""
        current = self.get_metrics()
        current.update(metrics)
        self.set_metrics(current)
    
    def get_checkpoints(self) -> List[Dict[str, Any]]:
        """Get execution checkpoints as list"""
        if self.checkpoints:
            import json
            try:
                return json.loads(self.checkpoints)
            except (json.JSONDecodeError, TypeError):
                return []
        return []
    
    def set_checkpoints(self, checkpoints: List[Dict[str, Any]]) -> None:
        """Set execution checkpoints from list"""
        import json
        self.checkpoints = json.dumps(checkpoints)
    
    def add_checkpoint(self, name: str, data: Dict[str, Any] = None) -> None:
        """Add a checkpoint"""
        checkpoints = self.get_checkpoints()
        checkpoint = {
            "timestamp": datetime.utcnow().isoformat(),
            "name": name,
            "data": data or {}
        }
        checkpoints.append(checkpoint)
        self.set_checkpoints(checkpoints)
    
    def start_execution(self) -> None:
        """Start the execution"""
        if self.status == ExecutionStatus.PENDING:
            self.status = ExecutionStatus.RUNNING
            self.started_at = datetime.utcnow()
            self.progress_percentage = 0
            self.add_log("info", "Execution started")
    
    def complete_execution(self, output_data: Dict[str, Any] = None) -> None:
        """Complete the execution"""
        self.status = ExecutionStatus.COMPLETED
        self.completed_at = datetime.utcnow()
        self.progress_percentage = 100
        self.completed_steps = self.total_steps
        
        if output_data:
            self.set_output_data(output_data)
        
        self.add_log("info", "Execution completed successfully")
    
    def fail_execution(self, error_message: str, error_details: Dict[str, Any] = None) -> None:
        """Mark execution as failed"""
        self.status = ExecutionStatus.FAILED
        self.completed_at = datetime.utcnow()
        self.error_message = error_message
        
        if error_details:
            self.set_error_details(error_details)
        
        self.add_log("error", f"Execution failed: {error_message}")
    
    def timeout_execution(self) -> None:
        """Mark execution as timed out"""
        self.status = ExecutionStatus.TIMEOUT
        self.completed_at = datetime.utcnow()
        self.error_message = "Execution timed out"
        
        self.add_log("error", "Execution timed out")
    
    def cancel_execution(self) -> None:
        """Cancel the execution"""
        if self.status in [ExecutionStatus.PENDING, ExecutionStatus.RUNNING]:
            self.status = ExecutionStatus.CANCELLED
            self.completed_at = datetime.utcnow()
            
            self.add_log("info", "Execution cancelled")
    
    def pause_execution(self) -> None:
        """Pause the execution"""
        if self.status == ExecutionStatus.RUNNING:
            self.status = ExecutionStatus.PAUSED
            
            self.add_log("info", "Execution paused")
    
    def resume_execution(self) -> None:
        """Resume the execution"""
        if self.status == ExecutionStatus.PAUSED:
            self.status = ExecutionStatus.RUNNING
            
            self.add_log("info", "Execution resumed")
    
    def retry_execution(self) -> None:
        """Retry the execution"""
        if self.status in [ExecutionStatus.FAILED, ExecutionStatus.TIMEOUT] and self.retry_count < self.max_retries:
            self.status = ExecutionStatus.PENDING
            self.retry_count += 1
            self.error_message = None
            self.error_details = None
            self.started_at = None
            self.completed_at = None
            self.progress_percentage = 0
            self.completed_steps = 0
            
            self.add_log("info", f"Execution retry {self.retry_count}/{self.max_retries}")
    
    def update_progress(self, percentage: int, current_step: str = None) -> None:
        """Update execution progress"""
        self.progress_percentage = max(0, min(100, percentage))
        if current_step:
            self.current_step = current_step
        
        # Update completed steps based on progress
        if self.total_steps > 0:
            self.completed_steps = int((self.progress_percentage / 100) * self.total_steps)
        
        # Auto-complete if progress reaches 100%
        if self.progress_percentage == 100 and not self.completed_at:
            self.complete_execution()
    
    def increment_step(self) -> None:
        """Increment execution step"""
        if self.completed_steps < self.total_steps:
            self.completed_steps += 1
            progress = (self.completed_steps / self.total_steps) * 100
            self.update_progress(int(progress))
    
    def add_cost(self, amount: float) -> None:
        """Add cost to the execution"""
        self.cost += amount
    
    def add_tokens(self, count: int) -> None:
        """Add tokens to the execution"""
        self.tokens_used += count
    
    def update_resource_usage(self, memory: float = None, cpu: float = None) -> None:
        """Update resource usage"""
        if memory is not None:
            self.memory_usage = memory
        if cpu is not None:
            self.cpu_usage = cpu
        
        # Update resource usage JSON
        usage = self.get_resource_usage()
        if memory is not None:
            usage["memory_mb"] = memory
        if cpu is not None:
            usage["cpu_percent"] = cpu
        usage["timestamp"] = datetime.utcnow().isoformat()
        self.set_resource_usage(usage)
    
    def check_timeout(self) -> bool:
        """Check if execution has timed out"""
        if not self.started_at or not self.timeout_minutes:
            return False
        
        elapsed = (datetime.utcnow() - self.started_at).total_seconds() / 60
        return elapsed > self.timeout_minutes
    
    def get_stats(self) -> Dict[str, Any]:
        """Get execution statistics"""
        return {
            "duration_minutes": self.duration_minutes,
            "efficiency_score": self.efficiency_score,
            "time_remaining": self.time_remaining,
            "is_overdue": self.is_overdue,
            "retry_count": self.retry_count,
            "tokens_used": self.tokens_used,
            "cost": self.cost,
            "memory_usage": self.memory_usage,
            "cpu_usage": self.cpu_usage,
            "progress_percentage": self.progress_percentage,
            "completed_steps": self.completed_steps,
            "total_steps": self.total_steps,
            "scheduled_at": self.scheduled_at.isoformat() if self.scheduled_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }
    
    def duplicate(self, new_name: str) -> "Execution":
        """Create a duplicate of this execution"""
        duplicate = Execution(
            execution_type=self.execution_type,
            status=ExecutionStatus.PENDING,  # Start as pending
            name=new_name,
            description=self.description,
            input_data=self.input_data,
            parameters=self.parameters,
            context=self.context,
            scheduled_at=self.scheduled_at,
            estimated_duration=self.estimated_duration,
            timeout_minutes=self.timeout_minutes,
            max_retries=self.max_retries,
            resource_limits=self.resource_limits,
            executor_id=self.executor_id,
            project_id=self.project_id,
            workflow_id=self.workflow_id,
            agent_id=self.agent_id,
            task_id=self.task_id
        )
        return duplicate
    
    def validate(self) -> bool:
        """Validate execution data"""
        errors = self.get_validation_errors()
        return len(errors) == 0
    
    def get_validation_errors(self) -> List[str]:
        """Get validation errors"""
        errors = []
        
        if not self.name:
            errors.append("Execution name is required")
        elif len(self.name) < 1:
            errors.append("Execution name must be at least 1 character")
        elif len(self.name) > 200:
            errors.append("Execution name must be less than 200 characters")
        
        if self.progress_percentage < 0 or self.progress_percentage > 100:
            errors.append("Progress percentage must be between 0 and 100")
        
        if self.total_steps < 1:
            errors.append("Total steps must be at least 1")
        
        if self.completed_steps < 0:
            errors.append("Completed steps cannot be negative")
        
        if self.completed_steps > self.total_steps:
            errors.append("Completed steps cannot exceed total steps")
        
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
        
        if self.memory_usage is not None and self.memory_usage < 0:
            errors.append("Memory usage cannot be negative")
        
        if self.cpu_usage is not None and (self.cpu_usage < 0 or self.cpu_usage > 100):
            errors.append("CPU usage must be between 0 and 100")
        
        return errors
    
    @classmethod
    def get_by_status(cls, session, status: ExecutionStatus) -> List["Execution"]:
        """Get executions by status"""
        return session.query(cls).filter(
            cls.status == status,
            cls.is_deleted == False
        ).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_by_type(cls, session, execution_type: ExecutionType) -> List["Execution"]:
        """Get executions by type"""
        return session.query(cls).filter(
            cls.execution_type == execution_type,
            cls.is_deleted == False
        ).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_by_executor(cls, session, executor_id: uuid.UUID) -> List["Execution"]:
        """Get executions by executor"""
        return session.query(cls).filter(
            cls.executor_id == executor_id,
            cls.is_deleted == False
        ).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_by_project(cls, session, project_id: uuid.UUID) -> List["Execution"]:
        """Get executions by project"""
        return session.query(cls).filter(
            cls.project_id == project_id,
            cls.is_deleted == False
        ).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_by_workflow(cls, session, workflow_id: uuid.UUID) -> List["Execution"]:
        """Get executions by workflow"""
        return session.query(cls).filter(
            cls.workflow_id == workflow_id,
            cls.is_deleted == False
        ).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_by_agent(cls, session, agent_id: uuid.UUID) -> List["Execution"]:
        """Get executions by agent"""
        return session.query(cls).filter(
            cls.agent_id == agent_id,
            cls.is_deleted == False
        ).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_by_task(cls, session, task_id: uuid.UUID) -> List["Execution"]:
        """Get executions by task"""
        return session.query(cls).filter(
            cls.task_id == task_id,
            cls.is_deleted == False
        ).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_running_executions(cls, session) -> List["Execution"]:
        """Get running executions"""
        return session.query(cls).filter(
            cls.status == ExecutionStatus.RUNNING,
            cls.is_deleted == False
        ).order_by(cls.started_at.asc()).all()
    
    @classmethod
    def get_failed_executions(cls, session) -> List["Execution"]:
        """Get failed executions"""
        return session.query(cls).filter(
            cls.status.in_([ExecutionStatus.FAILED, ExecutionStatus.TIMEOUT]),
            cls.is_deleted == False
        ).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_overdue_executions(cls, session) -> List["Execution"]:
        """Get overdue executions"""
        return session.query(cls).filter(
            cls.scheduled_at < datetime.utcnow(),
            cls.status.in_([ExecutionStatus.PENDING, ExecutionStatus.RUNNING]),
            cls.is_deleted == False
        ).order_by(cls.scheduled_at.asc()).all()
    
    @classmethod
    def search(cls, session, query: str, status: ExecutionStatus = None) -> List["Execution"]:
        """Search executions"""
        search_query = session.query(cls).filter(cls.is_deleted == False)
        
        # Add search conditions
        search_query = search_query.filter(
            (cls.name.ilike(f"%{query}%")) |
            (cls.description.ilike(f"%{query}%"))
        )
        
        # Filter by status if specified
        if status:
            search_query = search_query.filter(cls.status == status)
        
        return search_query.order_by(cls.created_at.desc()).all()



