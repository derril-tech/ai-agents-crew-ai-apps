"""
Agent model for Multi-Agent CrewAI Backend
"""

import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import Column, String, Text, Boolean, DateTime, Integer, ForeignKey, Enum, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from models.base import BaseModel


class AgentType(enum.Enum):
    """Agent type enumeration"""
    RESEARCHER = "researcher"
    ANALYST = "analyst"
    WRITER = "writer"
    MARKETING = "marketing"
    DEVELOPER = "developer"
    HEALTHCARE = "healthcare"
    LEGAL = "legal"
    ECOMMERCE = "ecommerce"
    CYBERSECURITY = "cybersecurity"
    CUSTOM = "custom"


class AgentStatus(enum.Enum):
    """Agent status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    BUSY = "busy"
    ERROR = "error"
    MAINTENANCE = "maintenance"


class Agent(BaseModel):
    """Agent model for AI agent definitions"""
    
    # Basic information
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    agent_type = Column(Enum(AgentType), default=AgentType.CUSTOM, nullable=False)
    status = Column(Enum(AgentStatus), default=AgentStatus.ACTIVE, nullable=False)
    
    # Agent configuration
    role = Column(String(500), nullable=False)
    goals = Column(Text, nullable=True)  # JSON array of goals
    constraints = Column(Text, nullable=True)  # JSON array of constraints
    tools = Column(Text, nullable=True)  # JSON array of available tools
    
    # AI model configuration
    model_name = Column(String(100), default="gpt-4", nullable=False)
    model_provider = Column(String(50), default="openai", nullable=False)
    temperature = Column(Float, default=0.7, nullable=False)
    max_tokens = Column(Integer, default=4000, nullable=False)
    
    # Agent behavior
    personality = Column(Text, nullable=True)  # JSON object for personality traits
    communication_style = Column(String(100), default="professional", nullable=False)
    decision_making_style = Column(String(100), default="analytical", nullable=False)
    
    # Performance tracking
    total_tasks_completed = Column(Integer, default=0, nullable=False)
    total_tasks_failed = Column(Integer, default=0, nullable=False)
    average_task_duration = Column(Float, nullable=True)  # In seconds
    success_rate = Column(Float, default=0.0, nullable=False)  # Percentage
    
    # Resource usage
    total_tokens_used = Column(Integer, default=0, nullable=False)
    total_cost = Column(Float, default=0.0, nullable=False)  # In USD
    last_used_at = Column(DateTime, nullable=True)
    
    # Agent capabilities
    capabilities = Column(Text, nullable=True)  # JSON array of capabilities
    specializations = Column(Text, nullable=True)  # JSON array of specializations
    limitations = Column(Text, nullable=True)  # JSON array of limitations
    
    # Integration settings
    api_endpoints = Column(Text, nullable=True)  # JSON object for API endpoints
    webhook_urls = Column(Text, nullable=True)  # JSON array of webhook URLs
    external_apis = Column(Text, nullable=True)  # JSON object for external API configs
    
    # Security and permissions
    access_level = Column(String(50), default="standard", nullable=False)
    allowed_actions = Column(Text, nullable=True)  # JSON array of allowed actions
    restricted_actions = Column(Text, nullable=True)  # JSON array of restricted actions
    
    # Monitoring and logging
    log_level = Column(String(20), default="info", nullable=False)
    enable_monitoring = Column(Boolean, default=True, nullable=False)
    alert_thresholds = Column(Text, nullable=True)  # JSON object for alert thresholds
    
    # Relationships
    creator_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey("project.id"), nullable=True)
    
    creator = relationship("User", back_populates="agents")
    project = relationship("Project", back_populates="agents")
    tasks = relationship("Task", back_populates="agent", cascade="all, delete-orphan")
    workflows = relationship("Workflow", secondary="workflow_agents", back_populates="agents")
    
    def __repr__(self) -> str:
        return f"<Agent(id={self.id}, name={self.name}, type={self.agent_type.value})>"
    
    @property
    def is_available(self) -> bool:
        """Check if agent is available for tasks"""
        return self.status == AgentStatus.ACTIVE
    
    @property
    def is_busy(self) -> bool:
        """Check if agent is currently busy"""
        return self.status == AgentStatus.BUSY
    
    @property
    def total_tasks(self) -> int:
        """Get total number of tasks"""
        return self.total_tasks_completed + self.total_tasks_failed
    
    @property
    def failure_rate(self) -> float:
        """Get task failure rate"""
        if self.total_tasks == 0:
            return 0.0
        return (self.total_tasks_failed / self.total_tasks) * 100
    
    @property
    def cost_per_task(self) -> float:
        """Get average cost per task"""
        if self.total_tasks_completed == 0:
            return 0.0
        return self.total_cost / self.total_tasks_completed
    
    @property
    def tokens_per_task(self) -> float:
        """Get average tokens per task"""
        if self.total_tasks_completed == 0:
            return 0.0
        return self.total_tokens_used / self.total_tasks_completed
    
    def get_goals(self) -> List[str]:
        """Get agent goals as list"""
        if self.goals:
            import json
            try:
                return json.loads(self.goals)
            except (json.JSONDecodeError, TypeError):
                return []
        return []
    
    def set_goals(self, goals: List[str]) -> None:
        """Set agent goals from list"""
        import json
        self.goals = json.dumps(goals)
    
    def add_goal(self, goal: str) -> None:
        """Add a goal to the agent"""
        goals = self.get_goals()
        if goal not in goals:
            goals.append(goal)
            self.set_goals(goals)
    
    def remove_goal(self, goal: str) -> None:
        """Remove a goal from the agent"""
        goals = self.get_goals()
        if goal in goals:
            goals.remove(goal)
            self.set_goals(goals)
    
    def get_constraints(self) -> List[str]:
        """Get agent constraints as list"""
        if self.constraints:
            import json
            try:
                return json.loads(self.constraints)
            except (json.JSONDecodeError, TypeError):
                return []
        return []
    
    def set_constraints(self, constraints: List[str]) -> None:
        """Set agent constraints from list"""
        import json
        self.constraints = json.dumps(constraints)
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Get agent tools as list"""
        if self.tools:
            import json
            try:
                return json.loads(self.tools)
            except (json.JSONDecodeError, TypeError):
                return []
        return []
    
    def set_tools(self, tools: List[Dict[str, Any]]) -> None:
        """Set agent tools from list"""
        import json
        self.tools = json.dumps(tools)
    
    def add_tool(self, tool: Dict[str, Any]) -> None:
        """Add a tool to the agent"""
        tools = self.get_tools()
        tool_id = tool.get("id")
        if tool_id:
            # Update existing tool or add new one
            existing_tool = next((t for t in tools if t.get("id") == tool_id), None)
            if existing_tool:
                tools.remove(existing_tool)
            tools.append(tool)
            self.set_tools(tools)
    
    def remove_tool(self, tool_id: str) -> None:
        """Remove a tool from the agent"""
        tools = self.get_tools()
        tools = [t for t in tools if t.get("id") != tool_id]
        self.set_tools(tools)
    
    def get_personality(self) -> Dict[str, Any]:
        """Get agent personality as dictionary"""
        if self.personality:
            import json
            try:
                return json.loads(self.personality)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}
    
    def set_personality(self, personality: Dict[str, Any]) -> None:
        """Set agent personality from dictionary"""
        import json
        self.personality = json.dumps(personality)
    
    def get_capabilities(self) -> List[str]:
        """Get agent capabilities as list"""
        if self.capabilities:
            import json
            try:
                return json.loads(self.capabilities)
            except (json.JSONDecodeError, TypeError):
                return []
        return []
    
    def set_capabilities(self, capabilities: List[str]) -> None:
        """Set agent capabilities from list"""
        import json
        self.capabilities = json.dumps(capabilities)
    
    def has_capability(self, capability: str) -> bool:
        """Check if agent has specific capability"""
        return capability in self.get_capabilities()
    
    def get_specializations(self) -> List[str]:
        """Get agent specializations as list"""
        if self.specializations:
            import json
            try:
                return json.loads(self.specializations)
            except (json.JSONDecodeError, TypeError):
                return []
        return []
    
    def set_specializations(self, specializations: List[str]) -> None:
        """Set agent specializations from list"""
        import json
        self.specializations = json.dumps(specializations)
    
    def get_limitations(self) -> List[str]:
        """Get agent limitations as list"""
        if self.limitations:
            import json
            try:
                return json.loads(self.limitations)
            except (json.JSONDecodeError, TypeError):
                return []
        return []
    
    def set_limitations(self, limitations: List[str]) -> None:
        """Set agent limitations from list"""
        import json
        self.limitations = json.dumps(limitations)
    
    def get_api_endpoints(self) -> Dict[str, Any]:
        """Get API endpoints as dictionary"""
        if self.api_endpoints:
            import json
            try:
                return json.loads(self.api_endpoints)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}
    
    def set_api_endpoints(self, endpoints: Dict[str, Any]) -> None:
        """Set API endpoints from dictionary"""
        import json
        self.api_endpoints = json.dumps(endpoints)
    
    def get_webhook_urls(self) -> List[str]:
        """Get webhook URLs as list"""
        if self.webhook_urls:
            import json
            try:
                return json.loads(self.webhook_urls)
            except (json.JSONDecodeError, TypeError):
                return []
        return []
    
    def set_webhook_urls(self, urls: List[str]) -> None:
        """Set webhook URLs from list"""
        import json
        self.webhook_urls = json.dumps(urls)
    
    def get_external_apis(self) -> Dict[str, Any]:
        """Get external API configurations as dictionary"""
        if self.external_apis:
            import json
            try:
                return json.loads(self.external_apis)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}
    
    def set_external_apis(self, apis: Dict[str, Any]) -> None:
        """Set external API configurations from dictionary"""
        import json
        self.external_apis = json.dumps(apis)
    
    def get_allowed_actions(self) -> List[str]:
        """Get allowed actions as list"""
        if self.allowed_actions:
            import json
            try:
                return json.loads(self.allowed_actions)
            except (json.JSONDecodeError, TypeError):
                return []
        return []
    
    def set_allowed_actions(self, actions: List[str]) -> None:
        """Set allowed actions from list"""
        import json
        self.allowed_actions = json.dumps(actions)
    
    def can_perform_action(self, action: str) -> bool:
        """Check if agent can perform specific action"""
        allowed = self.get_allowed_actions()
        restricted = self.get_restricted_actions()
        
        # If no allowed actions specified, agent can perform any action
        if not allowed:
            return action not in restricted
        
        return action in allowed and action not in restricted
    
    def get_restricted_actions(self) -> List[str]:
        """Get restricted actions as list"""
        if self.restricted_actions:
            import json
            try:
                return json.loads(self.restricted_actions)
            except (json.JSONDecodeError, TypeError):
                return []
        return []
    
    def set_restricted_actions(self, actions: List[str]) -> None:
        """Set restricted actions from list"""
        import json
        self.restricted_actions = json.dumps(actions)
    
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
    
    def increment_task_completion(self, success: bool, duration: float = None, tokens: int = 0, cost: float = 0.0) -> None:
        """Increment task completion counters"""
        if success:
            self.total_tasks_completed += 1
        else:
            self.total_tasks_failed += 1
        
        # Update success rate
        if self.total_tasks > 0:
            self.success_rate = (self.total_tasks_completed / self.total_tasks) * 100
        
        # Update average task duration
        if duration is not None:
            if self.average_task_duration is None:
                self.average_task_duration = duration
            else:
                total_duration = self.average_task_duration * (self.total_tasks - 1) + duration
                self.average_task_duration = total_duration / self.total_tasks
        
        # Update resource usage
        self.total_tokens_used += tokens
        self.total_cost += cost
        self.last_used_at = datetime.utcnow()
    
    def set_busy(self) -> None:
        """Set agent as busy"""
        self.status = AgentStatus.BUSY
    
    def set_available(self) -> None:
        """Set agent as available"""
        self.status = AgentStatus.ACTIVE
    
    def set_error(self) -> None:
        """Set agent as error state"""
        self.status = AgentStatus.ERROR
    
    def set_maintenance(self) -> None:
        """Set agent as maintenance mode"""
        self.status = AgentStatus.MAINTENANCE
    
    def reset_stats(self) -> None:
        """Reset agent statistics"""
        self.total_tasks_completed = 0
        self.total_tasks_failed = 0
        self.average_task_duration = None
        self.success_rate = 0.0
        self.total_tokens_used = 0
        self.total_cost = 0.0
        self.last_used_at = None
    
    def get_stats(self) -> Dict[str, Any]:
        """Get agent statistics"""
        return {
            "total_tasks": self.total_tasks,
            "total_tasks_completed": self.total_tasks_completed,
            "total_tasks_failed": self.total_tasks_failed,
            "success_rate": self.success_rate,
            "failure_rate": self.failure_rate,
            "average_task_duration": self.average_task_duration,
            "total_tokens_used": self.total_tokens_used,
            "total_cost": self.total_cost,
            "cost_per_task": self.cost_per_task,
            "tokens_per_task": self.tokens_per_task,
            "last_used_at": self.last_used_at.isoformat() if self.last_used_at else None,
            "status": self.status.value,
            "is_available": self.is_available,
            "is_busy": self.is_busy
        }
    
    def duplicate(self, new_name: str, new_creator_id: uuid.UUID) -> "Agent":
        """Create a duplicate of this agent"""
        duplicate = Agent(
            name=new_name,
            description=self.description,
            agent_type=self.agent_type,
            status=AgentStatus.INACTIVE,  # Start as inactive
            role=self.role,
            goals=self.goals,
            constraints=self.constraints,
            tools=self.tools,
            model_name=self.model_name,
            model_provider=self.model_provider,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            personality=self.personality,
            communication_style=self.communication_style,
            decision_making_style=self.decision_making_style,
            capabilities=self.capabilities,
            specializations=self.specializations,
            limitations=self.limitations,
            api_endpoints=self.api_endpoints,
            webhook_urls=self.webhook_urls,
            external_apis=self.external_apis,
            access_level=self.access_level,
            allowed_actions=self.allowed_actions,
            restricted_actions=self.restricted_actions,
            log_level=self.log_level,
            enable_monitoring=self.enable_monitoring,
            alert_thresholds=self.alert_thresholds,
            creator_id=new_creator_id,
            project_id=self.project_id
        )
        return duplicate
    
    def validate(self) -> bool:
        """Validate agent data"""
        errors = self.get_validation_errors()
        return len(errors) == 0
    
    def get_validation_errors(self) -> List[str]:
        """Get validation errors"""
        errors = []
        
        if not self.name:
            errors.append("Agent name is required")
        elif len(self.name) < 1:
            errors.append("Agent name must be at least 1 character")
        elif len(self.name) > 200:
            errors.append("Agent name must be less than 200 characters")
        
        if not self.role:
            errors.append("Agent role is required")
        elif len(self.role) < 1:
            errors.append("Agent role must be at least 1 character")
        elif len(self.role) > 500:
            errors.append("Agent role must be less than 500 characters")
        
        if self.temperature < 0.0 or self.temperature > 2.0:
            errors.append("Temperature must be between 0.0 and 2.0")
        
        if self.max_tokens < 1:
            errors.append("Max tokens must be at least 1")
        
        if self.success_rate < 0.0 or self.success_rate > 100.0:
            errors.append("Success rate must be between 0.0 and 100.0")
        
        if self.total_cost < 0.0:
            errors.append("Total cost cannot be negative")
        
        if self.total_tokens_used < 0:
            errors.append("Total tokens used cannot be negative")
        
        return errors
    
    @classmethod
    def get_by_type(cls, session, agent_type: AgentType) -> List["Agent"]:
        """Get agents by type"""
        return session.query(cls).filter(
            cls.agent_type == agent_type,
            cls.is_deleted == False
        ).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_available_agents(cls, session) -> List["Agent"]:
        """Get available agents"""
        return session.query(cls).filter(
            cls.status == AgentStatus.ACTIVE,
            cls.is_deleted == False
        ).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_by_creator(cls, session, creator_id: uuid.UUID) -> List["Agent"]:
        """Get agents by creator"""
        return session.query(cls).filter(
            cls.creator_id == creator_id,
            cls.is_deleted == False
        ).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_by_project(cls, session, project_id: uuid.UUID) -> List["Agent"]:
        """Get agents by project"""
        return session.query(cls).filter(
            cls.project_id == project_id,
            cls.is_deleted == False
        ).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def search(cls, session, query: str, agent_type: AgentType = None) -> List["Agent"]:
        """Search agents"""
        search_query = session.query(cls).filter(cls.is_deleted == False)
        
        # Add search conditions
        search_query = search_query.filter(
            (cls.name.ilike(f"%{query}%")) |
            (cls.description.ilike(f"%{query}%")) |
            (cls.role.ilike(f"%{query}%"))
        )
        
        # Filter by type if specified
        if agent_type:
            search_query = search_query.filter(cls.agent_type == agent_type)
        
        return search_query.order_by(cls.created_at.desc()).all()

