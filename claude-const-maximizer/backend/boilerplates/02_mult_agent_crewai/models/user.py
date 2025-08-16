"""
User model for Multi-Agent CrewAI Backend
"""

import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from passlib.context import CryptContext

from models.base import BaseModel

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    """User model for authentication and authorization"""
    
    # User identification
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    
    # Authentication
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    
    # Profile information
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    full_name = Column(String(200), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    
    # Contact information
    phone = Column(String(20), nullable=True)
    company = Column(String(200), nullable=True)
    job_title = Column(String(200), nullable=True)
    website = Column(String(500), nullable=True)
    
    # Preferences
    timezone = Column(String(50), default="UTC", nullable=False)
    language = Column(String(10), default="en", nullable=False)
    theme = Column(String(20), default="light", nullable=False)
    
    # Security
    last_login = Column(DateTime, nullable=True)
    login_attempts = Column(Integer, default=0, nullable=False)
    locked_until = Column(DateTime, nullable=True)
    password_changed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Two-factor authentication
    two_factor_enabled = Column(Boolean, default=False, nullable=False)
    two_factor_secret = Column(String(32), nullable=True)
    backup_codes = Column(Text, nullable=True)  # JSON array of backup codes
    
    # API access
    api_key = Column(String(64), unique=True, nullable=True, index=True)
    api_key_created_at = Column(DateTime, nullable=True)
    api_key_last_used = Column(DateTime, nullable=True)
    
    # Subscription and billing
    subscription_plan = Column(String(50), default="free", nullable=False)
    subscription_status = Column(String(20), default="active", nullable=False)
    subscription_expires_at = Column(DateTime, nullable=True)
    
    # Usage tracking
    total_api_calls = Column(Integer, default=0, nullable=False)
    monthly_api_calls = Column(Integer, default=0, nullable=False)
    last_api_call_at = Column(DateTime, nullable=True)
    
    # Relationships
    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")
    agents = relationship("Agent", back_populates="creator", cascade="all, delete-orphan")
    workflows = relationship("Workflow", back_populates="creator", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="assignee", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, username={self.username})>"
    
    @property
    def is_locked(self) -> bool:
        """Check if user account is locked"""
        if self.locked_until and self.locked_until > datetime.utcnow():
            return True
        return False
    
    @property
    def display_name(self) -> str:
        """Get display name (full name or username)"""
        if self.full_name:
            return self.full_name
        elif self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.username
    
    @property
    def initials(self) -> str:
        """Get user initials"""
        if self.first_name and self.last_name:
            return f"{self.first_name[0]}{self.last_name[0]}".upper()
        elif self.first_name:
            return self.first_name[0].upper()
        elif self.username:
            return self.username[0].upper()
        else:
            return "U"
    
    def set_password(self, password: str) -> None:
        """Hash and set password"""
        self.hashed_password = pwd_context.hash(password)
        self.password_changed_at = datetime.utcnow()
    
    def verify_password(self, password: str) -> bool:
        """Verify password"""
        return pwd_context.verify(password, self.hashed_password)
    
    def generate_api_key(self) -> str:
        """Generate new API key"""
        import secrets
        self.api_key = f"crewai_{secrets.token_urlsafe(32)}"
        self.api_key_created_at = datetime.utcnow()
        return self.api_key
    
    def revoke_api_key(self) -> None:
        """Revoke API key"""
        self.api_key = None
        self.api_key_created_at = None
        self.api_key_last_used = None
    
    def update_last_login(self) -> None:
        """Update last login timestamp"""
        self.last_login = datetime.utcnow()
        self.login_attempts = 0
        self.locked_until = None
    
    def increment_login_attempts(self) -> None:
        """Increment failed login attempts"""
        self.login_attempts += 1
        if self.login_attempts >= 5:  # Lock after 5 failed attempts
            from datetime import timedelta
            self.locked_until = datetime.utcnow() + timedelta(minutes=15)
    
    def reset_login_attempts(self) -> None:
        """Reset login attempts"""
        self.login_attempts = 0
        self.locked_until = None
    
    def enable_two_factor(self) -> str:
        """Enable two-factor authentication"""
        import pyotp
        self.two_factor_secret = pyotp.random_base32()
        self.two_factor_enabled = True
        return self.two_factor_secret
    
    def disable_two_factor(self) -> None:
        """Disable two-factor authentication"""
        self.two_factor_enabled = False
        self.two_factor_secret = None
        self.backup_codes = None
    
    def generate_backup_codes(self) -> List[str]:
        """Generate backup codes for 2FA"""
        import secrets
        codes = [secrets.token_hex(4).upper() for _ in range(10)]
        import json
        self.backup_codes = json.dumps(codes)
        return codes
    
    def verify_two_factor(self, token: str) -> bool:
        """Verify two-factor authentication token"""
        if not self.two_factor_enabled or not self.two_factor_secret:
            return False
        
        import pyotp
        totp = pyotp.TOTP(self.two_factor_secret)
        return totp.verify(token)
    
    def verify_backup_code(self, code: str) -> bool:
        """Verify backup code"""
        if not self.backup_codes:
            return False
        
        import json
        codes = json.loads(self.backup_codes)
        if code in codes:
            codes.remove(code)
            self.backup_codes = json.dumps(codes)
            return True
        return False
    
    def increment_api_calls(self) -> None:
        """Increment API call counters"""
        self.total_api_calls += 1
        self.monthly_api_calls += 1
        self.last_api_call_at = datetime.utcnow()
    
    def reset_monthly_usage(self) -> None:
        """Reset monthly usage counters"""
        self.monthly_api_calls = 0
    
    def has_subscription_access(self) -> bool:
        """Check if user has active subscription"""
        if self.subscription_status != "active":
            return False
        if self.subscription_expires_at and self.subscription_expires_at < datetime.utcnow():
            return False
        return True
    
    def get_subscription_limits(self) -> dict:
        """Get subscription limits"""
        limits = {
            "free": {
                "max_projects": 3,
                "max_agents": 10,
                "max_workflows": 5,
                "max_api_calls_per_month": 1000,
                "max_file_size_mb": 10
            },
            "pro": {
                "max_projects": 20,
                "max_agents": 50,
                "max_workflows": 25,
                "max_api_calls_per_month": 10000,
                "max_file_size_mb": 100
            },
            "enterprise": {
                "max_projects": -1,  # Unlimited
                "max_agents": -1,    # Unlimited
                "max_workflows": -1,  # Unlimited
                "max_api_calls_per_month": -1,  # Unlimited
                "max_file_size_mb": 1000
            }
        }
        return limits.get(self.subscription_plan, limits["free"])
    
    def can_create_project(self) -> bool:
        """Check if user can create new project"""
        if not self.has_subscription_access():
            return False
        
        limits = self.get_subscription_limits()
        if limits["max_projects"] == -1:
            return True
        
        return len(self.projects) < limits["max_projects"]
    
    def can_create_agent(self) -> bool:
        """Check if user can create new agent"""
        if not self.has_subscription_access():
            return False
        
        limits = self.get_subscription_limits()
        if limits["max_agents"] == -1:
            return True
        
        return len(self.agents) < limits["max_agents"]
    
    def can_create_workflow(self) -> bool:
        """Check if user can create new workflow"""
        if not self.has_subscription_access():
            return False
        
        limits = self.get_subscription_limits()
        if limits["max_workflows"] == -1:
            return True
        
        return len(self.workflows) < limits["max_workflows"]
    
    def can_make_api_call(self) -> bool:
        """Check if user can make API call"""
        if not self.has_subscription_access():
            return False
        
        limits = self.get_subscription_limits()
        if limits["max_api_calls_per_month"] == -1:
            return True
        
        return self.monthly_api_calls < limits["max_api_calls_per_month"]
    
    def get_usage_stats(self) -> dict:
        """Get user usage statistics"""
        return {
            "total_projects": len(self.projects),
            "total_agents": len(self.agents),
            "total_workflows": len(self.workflows),
            "total_tasks": len(self.tasks),
            "total_api_calls": self.total_api_calls,
            "monthly_api_calls": self.monthly_api_calls,
            "subscription_plan": self.subscription_plan,
            "subscription_status": self.subscription_status,
            "subscription_expires_at": self.subscription_expires_at.isoformat() if self.subscription_expires_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "last_api_call": self.last_api_call_at.isoformat() if self.last_api_call_at else None
        }
    
    def to_dict(self) -> dict:
        """Convert user to dictionary (excluding sensitive data)"""
        data = super().to_dict()
        # Remove sensitive fields
        sensitive_fields = [
            "hashed_password", "two_factor_secret", "backup_codes",
            "api_key", "login_attempts", "locked_until"
        ]
        for field in sensitive_fields:
            data.pop(field, None)
        return data
    
    def validate(self) -> bool:
        """Validate user data"""
        errors = self.get_validation_errors()
        return len(errors) == 0
    
    def get_validation_errors(self) -> List[str]:
        """Get validation errors"""
        errors = []
        
        if not self.email:
            errors.append("Email is required")
        elif "@" not in self.email:
            errors.append("Invalid email format")
        
        if not self.username:
            errors.append("Username is required")
        elif len(self.username) < 3:
            errors.append("Username must be at least 3 characters")
        elif len(self.username) > 100:
            errors.append("Username must be less than 100 characters")
        
        if not self.hashed_password:
            errors.append("Password is required")
        
        return errors
    
    @classmethod
    def get_by_email(cls, session, email: str) -> Optional["User"]:
        """Get user by email"""
        return session.query(cls).filter(cls.email == email, cls.is_deleted == False).first()
    
    @classmethod
    def get_by_username(cls, session, username: str) -> Optional["User"]:
        """Get user by username"""
        return session.query(cls).filter(cls.username == username, cls.is_deleted == False).first()
    
    @classmethod
    def get_by_api_key(cls, session, api_key: str) -> Optional["User"]:
        """Get user by API key"""
        return session.query(cls).filter(cls.api_key == api_key, cls.is_deleted == False).first()
    
    @classmethod
    def create_user(cls, session, email: str, username: str, password: str, **kwargs) -> "User":
        """Create new user"""
        user = cls(
            email=email,
            username=username,
            **kwargs
        )
        user.set_password(password)
        session.add(user)
        session.commit()
        return user
