"""
Database Management for SDR Assistant

This module provides database connectivity and management for the SDR Assistant application.
"""

import asyncio
from typing import Optional, Dict, Any
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Database manager for SDR Assistant"""
    
    def __init__(self, database_url: Optional[str] = None):
        self.database_url = database_url or "sqlite:///./sdr_assistant.db"
        self.engine = None
        self.async_engine = None
        self.SessionLocal = None
        self.AsyncSessionLocal = None
        self.metadata = MetaData()
        
    async def initialize(self):
        """Initialize database connection"""
        try:
            # For SQLite, use synchronous engine for now
            if self.database_url.startswith("sqlite"):
                self.engine = create_engine(
                    self.database_url,
                    connect_args={"check_same_thread": False},
                    poolclass=StaticPool,
                    echo=False
                )
                self.SessionLocal = sessionmaker(
                    autocommit=False,
                    autoflush=False,
                    bind=self.engine
                )
            else:
                # For other databases, use async engine
                self.async_engine = create_async_engine(
                    self.database_url,
                    echo=False
                )
                self.AsyncSessionLocal = sessionmaker(
                    self.async_engine,
                    class_=AsyncSession,
                    expire_on_commit=False
                )
            
            logger.info(f"Database initialized: {self.database_url}")
            
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            # Continue without database for now
            pass
    
    def get_session(self):
        """Get database session"""
        if self.SessionLocal:
            return self.SessionLocal()
        return None
    
    async def get_async_session(self):
        """Get async database session"""
        if self.AsyncSessionLocal:
            return self.AsyncSessionLocal()
        return None
    
    async def close(self):
        """Close database connections"""
        if self.engine:
            self.engine.dispose()
        if self.async_engine:
            await self.async_engine.dispose()
        logger.info("Database connections closed")
    
    def health_check(self) -> Dict[str, Any]:
        """Check database health"""
        try:
            if self.engine:
                with self.engine.connect() as conn:
                    conn.execute("SELECT 1")
                return {"status": "healthy", "type": "sqlite"}
            elif self.async_engine:
                return {"status": "healthy", "type": "async"}
            else:
                return {"status": "not_initialized", "type": "none"}
        except Exception as e:
            return {"status": "error", "error": str(e), "type": "unknown"}
