# backend/models/email.py
"""
Email database models
"""

from sqlalchemy import Column, String, Integer, Text, DateTime, Float, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
import enum

from ..database.connection import Base

class EmailCategory(enum.Enum):
    URGENT = "urgent"
    ACTION_REQUIRED = "action_required"
    INFORMATIONAL = "informational"
    SPAM = "spam"
    UNCATEGORIZED = "uncategorized"

class Email(Base):
    __tablename__ = "emails"
    __table_args__ = {"schema": "emails"}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    gmail_id = Column(String(255), unique=True, nullable=False, index=True)
    thread_id = Column(String(255), nullable=False, index=True)
    sender_email = Column(String(255), nullable=False, index=True)
    recipient_email = Column(String(255))
    subject = Column(Text)
    body = Column(Text)
    html_body = Column(Text)
    snippet = Column(Text)
    
    # Classification
    category = Column(Enum(EmailCategory), default=EmailCategory.UNCATEGORIZED)
    priority = Column(Integer, default=3)  # 1-5 scale
    sentiment = Column(String(50))  # positive, negative, neutral, mixed
    confidence_score = Column(Float)
    
    # Metadata
    has_attachments = Column(Boolean, default=False)
    is_unread = Column(Boolean, default=True)
    is_important = Column(Boolean, default=False)
    labels = Column(Text)  # JSON string of labels
    
    # Timestamps
    received_at = Column(DateTime)
    processed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Status
    status = Column(String(50), default="unprocessed")
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "gmail_id": self.gmail_id,
            "thread_id": self.thread_id,
            "sender": self.sender_email,
            "subject": self.subject,
            "body": self.body,
            "category": self.category.value if self.category else None,
            "priority": self.priority,
            "sentiment": self.sentiment,
            "confidence": self.confidence_score,
            "status": self.status,
            "processed_at": self.processed_at.isoformat() if self.processed_at else None,
            "created_at": self.created_at.isoformat()
        }


# backend/models/draft.py
"""
Draft database models
"""

from sqlalchemy import Column, String, Integer, Text, DateTime, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from ..database.connection import Base

class Draft(Base):
    __tablename__ = "drafts"
    __table_args__ = {"schema": "emails"}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    gmail_draft_id = Column(String(255), unique=True)
    email_id = Column(String(255), index=True)  # Reference to original email
    thread_id = Column(String(255))
    
    # Draft content
    to_email = Column(String(255))
    cc_email = Column(Text)
    bcc_email = Column(Text)
    subject = Column(Text)
    body = Column(Text)
    
    # Metadata
    version = Column(Integer, default=1)
    confidence_score = Column(Float)
    placeholders = Column(JSONB)  # List of placeholders in draft
    user_edits = Column(JSONB)  # Track user modifications
    
    # Agent info
    agent_name = Column(String(100))
    model_used = Column(String(50))
    
    # Status
    status = Column(String(50), default="draft")  # draft, sent, discarded
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    sent_at = Column(DateTime)
    
    # User
    user_email = Column(String(255), index=True)
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "gmail_draft_id": self.gmail_draft_id,
            "email_id": self.email_id,
            "to": self.to_email,
            "subject": self.subject,
            "body": self.body,
            "confidence_score": self.confidence_score,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "sent_at": self.sent_at.isoformat() if self.sent_at else None
        }


# backend/models/agent.py
"""
Agent processing log models
"""

from sqlalchemy import Column, String, Integer, Text, DateTime, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
import uuid

from ..database.connection import Base

class AgentLog(Base):
    __tablename__ = "processing_logs"
    __table_args__ = {"schema": "agents"}
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email_id = Column(String(255), index=True)
    
    # Agent info
    agent_name = Column(String(100), index=True)
    action = Column(String(100))
    
    # LLM usage
    model_used = Column(String(50))
    input_tokens = Column(Integer)
    output_tokens = Column(Integer)
    total_tokens = Column(Integer)
    latency_ms = Column(Integer)
    cost_usd = Column(Float)
    
    # Results
    success = Column(Boolean)
    error_message = Column(Text)
    result = Column(JSONB)
    metadata = Column(JSONB)
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "email_id": self.email_id,
            "agent": self.agent_name,
            "action": self.action,
            "model": self.model_used,
            "tokens": self.total_tokens,
            "latency_ms": self.latency_ms,
            "cost": self.cost_usd,
            "success": self.success,
            "error": self.error_message,
            "timestamp": self.created_at.isoformat()
        }


# backend/database/connection.py
"""
Database connection and configuration
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://emailagent:emailagent123@localhost:5432/emailagent_db")

# Create engine
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    echo=os.getenv("APP_ENV") == "development"
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()