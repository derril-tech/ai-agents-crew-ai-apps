"""
Base model with common fields and methods
"""

import uuid
from datetime import datetime
from typing import Any, Dict, Optional
from sqlalchemy import Column, DateTime, String, Text, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Session

from config.database import Base


class BaseModel(Base):
    """Base model with common fields and methods"""
    
    __abstract__ = True
    
    # Common fields
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_by = Column(UUID(as_uuid=True), nullable=True)
    updated_by = Column(UUID(as_uuid=True), nullable=True)
    
    # Soft delete
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    deleted_by = Column(UUID(as_uuid=True), nullable=True)
    
    # Metadata
    metadata_json = Column(Text, nullable=True)  # JSON string for flexible metadata
    
    # Versioning
    version = Column(Integer, default=1, nullable=False)
    
    # Audit fields
    audit_trail = Column(Text, nullable=True)  # JSON string for audit trail
    
    @declared_attr
    def __tablename__(cls) -> str:
        """Generate table name from class name"""
        return cls.__name__.lower()
    
    def __repr__(self) -> str:
        """String representation"""
        return f"<{self.__class__.__name__}(id={self.id})>"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                value = value.isoformat()
            elif isinstance(value, uuid.UUID):
                value = str(value)
            result[column.name] = value
        return result
    
    def to_json(self) -> Dict[str, Any]:
        """Convert model to JSON-serializable dictionary"""
        return self.to_dict()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseModel":
        """Create model instance from dictionary"""
        # Filter out non-column attributes
        column_names = {column.name for column in cls.__table__.columns}
        filtered_data = {k: v for k, v in data.items() if k in column_names}
        
        return cls(**filtered_data)
    
    def update_from_dict(self, data: Dict[str, Any]) -> None:
        """Update model instance from dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def soft_delete(self, deleted_by: Optional[uuid.UUID] = None) -> None:
        """Soft delete the record"""
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()
        self.deleted_by = deleted_by
    
    def restore(self) -> None:
        """Restore a soft-deleted record"""
        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by = None
    
    def is_active(self) -> bool:
        """Check if record is active (not soft deleted)"""
        return not self.is_deleted
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get metadata as dictionary"""
        if self.metadata_json:
            import json
            try:
                return json.loads(self.metadata_json)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}
    
    def set_metadata(self, metadata: Dict[str, Any]) -> None:
        """Set metadata from dictionary"""
        import json
        self.metadata_json = json.dumps(metadata)
    
    def update_metadata(self, metadata: Dict[str, Any]) -> None:
        """Update metadata by merging with existing"""
        current = self.get_metadata()
        current.update(metadata)
        self.set_metadata(current)
    
    def get_audit_trail(self) -> Dict[str, Any]:
        """Get audit trail as dictionary"""
        if self.audit_trail:
            import json
            try:
                return json.loads(self.audit_trail)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}
    
    def add_audit_entry(self, action: str, user_id: Optional[uuid.UUID] = None, details: Dict[str, Any] = None) -> None:
        """Add audit trail entry"""
        import json
        from datetime import datetime
        
        audit_trail = self.get_audit_trail()
        if "entries" not in audit_trail:
            audit_trail["entries"] = []
        
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "user_id": str(user_id) if user_id else None,
            "details": details or {}
        }
        
        audit_trail["entries"].append(entry)
        self.audit_trail = json.dumps(audit_trail)
    
    def increment_version(self) -> None:
        """Increment version number"""
        self.version += 1
    
    @classmethod
    def get_by_id(cls, session: Session, id: uuid.UUID, include_deleted: bool = False) -> Optional["BaseModel"]:
        """Get record by ID"""
        query = session.query(cls).filter(cls.id == id)
        if not include_deleted:
            query = query.filter(cls.is_deleted == False)
        return query.first()
    
    @classmethod
    def get_all(cls, session: Session, include_deleted: bool = False, limit: Optional[int] = None, offset: Optional[int] = None) -> list["BaseModel"]:
        """Get all records"""
        query = session.query(cls)
        if not include_deleted:
            query = query.filter(cls.is_deleted == False)
        
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    @classmethod
    def count(cls, session: Session, include_deleted: bool = False) -> int:
        """Count records"""
        query = session.query(cls)
        if not include_deleted:
            query = query.filter(cls.is_deleted == False)
        return query.count()
    
    @classmethod
    def exists(cls, session: Session, id: uuid.UUID, include_deleted: bool = False) -> bool:
        """Check if record exists"""
        return cls.get_by_id(session, id, include_deleted) is not None
    
    def save(self, session: Session) -> None:
        """Save the record"""
        session.add(self)
        session.commit()
    
    def delete(self, session: Session, hard_delete: bool = False) -> None:
        """Delete the record"""
        if hard_delete:
            session.delete(self)
        else:
            self.soft_delete()
        session.commit()
    
    def refresh(self, session: Session) -> None:
        """Refresh the record from database"""
        session.refresh(self)
    
    def copy(self) -> "BaseModel":
        """Create a copy of the record (without ID)"""
        data = self.to_dict()
        data.pop('id', None)
        data.pop('created_at', None)
        data.pop('updated_at', None)
        data.pop('created_by', None)
        data.pop('updated_by', None)
        data.pop('is_deleted', None)
        data.pop('deleted_at', None)
        data.pop('deleted_by', None)
        data.pop('version', None)
        
        return self.__class__.from_dict(data)
    
    def get_changes(self, session: Session) -> Dict[str, Any]:
        """Get changes made to the record"""
        if not session.is_modified(self):
            return {}
        
        changes = {}
        for attr in session.dirty:
            if attr.key in self.__table__.columns:
                changes[attr.key] = {
                    'old': attr.history.deleted[0] if attr.history.deleted else None,
                    'new': attr.value
                }
        
        return changes
    
    def has_changes(self, session: Session) -> bool:
        """Check if record has unsaved changes"""
        return session.is_modified(self)
    
    def validate(self) -> bool:
        """Validate the record"""
        # Override in subclasses for specific validation
        return True
    
    def get_validation_errors(self) -> list[str]:
        """Get validation errors"""
        # Override in subclasses for specific validation
        return []
    
    def is_valid(self) -> bool:
        """Check if record is valid"""
        return len(self.get_validation_errors()) == 0
    
    @classmethod
    def get_table_name(cls) -> str:
        """Get table name"""
        return cls.__tablename__
    
    @classmethod
    def get_column_names(cls) -> list[str]:
        """Get column names"""
        return [column.name for column in cls.__table__.columns]
    
    @classmethod
    def get_primary_key_name(cls) -> str:
        """Get primary key column name"""
        return cls.__table__.primary_key.columns[0].name
    
    def get_primary_key_value(self) -> Any:
        """Get primary key value"""
        return getattr(self, self.get_primary_key_name())
    
    def __eq__(self, other: Any) -> bool:
        """Equality comparison"""
        if not isinstance(other, self.__class__):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        """Hash function"""
        return hash(self.id)
    
    def __str__(self) -> str:
        """String representation"""
        return f"{self.__class__.__name__}(id={self.id})"
    
    def __lt__(self, other: "BaseModel") -> bool:
        """Less than comparison (by created_at)"""
        if not isinstance(other, BaseModel):
            return NotImplemented
        return self.created_at < other.created_at
    
    def __le__(self, other: "BaseModel") -> bool:
        """Less than or equal comparison (by created_at)"""
        if not isinstance(other, BaseModel):
            return NotImplemented
        return self.created_at <= other.created_at
    
    def __gt__(self, other: "BaseModel") -> bool:
        """Greater than comparison (by created_at)"""
        if not isinstance(other, BaseModel):
            return NotImplemented
        return self.created_at > other.created_at
    
    def __ge__(self, other: "BaseModel") -> bool:
        """Greater than or equal comparison (by created_at)"""
        if not isinstance(other, BaseModel):
            return NotImplemented
        return self.created_at >= other.created_at
