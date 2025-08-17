"""
Models package for Multi-Agent CrewAI Backend
"""

from .base import BaseModel
from .user import User
from .project import Project, ProjectStatus, ProjectType
from .agent import Agent, AgentType, AgentStatus
from .task import Task, TaskStatus, TaskPriority, TaskType
from .workflow import Workflow, WorkflowStatus, WorkflowType, WorkflowTrigger, workflow_agents
from .execution import Execution, ExecutionStatus, ExecutionType

__all__ = [
    # Base model
    "BaseModel",
    
    # User model
    "User",
    
    # Project models
    "Project",
    "ProjectStatus", 
    "ProjectType",
    
    # Agent models
    "Agent",
    "AgentType",
    "AgentStatus",
    
    # Task models
    "Task",
    "TaskStatus",
    "TaskPriority",
    "TaskType",
    
    # Workflow models
    "Workflow",
    "WorkflowStatus",
    "WorkflowType",
    "WorkflowTrigger",
    "workflow_agents",
    
    # Execution models
    "Execution",
    "ExecutionStatus",
    "ExecutionType",
]

