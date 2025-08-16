"""
Database configuration and setup
"""

import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool
from sqlalchemy import MetaData

from config.settings import get_settings

settings = get_settings()

# Database URL for async operations
ASYNC_DATABASE_URL = settings.DATABASE_URL.replace(
    "postgresql://", "postgresql+asyncpg://"
)

# Create async engine
engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=settings.DEBUG,
    poolclass=NullPool if settings.TESTING else None,
    pool_pre_ping=True,
    pool_recycle=300,
    max_overflow=20,
    pool_size=10,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Create declarative base
Base = declarative_base()

# Metadata for migrations
metadata = MetaData()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Initialize database"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """Close database connections"""
    await engine.dispose()


# Database health check
async def check_db_health() -> bool:
    """Check database health"""
    try:
        async with AsyncSessionLocal() as session:
            await session.execute("SELECT 1")
        return True
    except Exception as e:
        print(f"Database health check failed: {e}")
        return False


# Database statistics
async def get_db_stats() -> dict:
    """Get database statistics"""
    try:
        async with AsyncSessionLocal() as session:
            # Get connection pool stats
            pool_stats = {
                "pool_size": engine.pool.size(),
                "checked_in": engine.pool.checkedin(),
                "checked_out": engine.pool.checkedout(),
                "overflow": engine.pool.overflow(),
                "invalid": engine.pool.invalid(),
            }
            
            # Get table counts (example)
            # This would need to be customized based on your models
            table_counts = {}
            
            return {
                "status": "healthy",
                "pool_stats": pool_stats,
                "table_counts": table_counts,
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
        }


# Database migration helpers
async def run_migrations():
    """Run database migrations"""
    try:
        import alembic.config
        import alembic.command
        
        # Create Alembic configuration
        alembic_cfg = alembic.config.Config(settings.ALEMBIC_CONFIG_PATH)
        alembic_cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
        
        # Run upgrade
        alembic.command.upgrade(alembic_cfg, "head")
        return True
    except Exception as e:
        print(f"Migration failed: {e}")
        return False


async def create_migration(message: str):
    """Create a new migration"""
    try:
        import alembic.config
        import alembic.command
        
        # Create Alembic configuration
        alembic_cfg = alembic.config.Config(settings.ALEMBIC_CONFIG_PATH)
        alembic_cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
        
        # Create migration
        alembic.command.revision(alembic_cfg, message=message, autogenerate=True)
        return True
    except Exception as e:
        print(f"Migration creation failed: {e}")
        return False


# Database backup helpers
async def backup_database(backup_path: str = None):
    """Backup database"""
    if not backup_path:
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"backup_{timestamp}.sql"
    
    try:
        import subprocess
        
        # Extract database connection details
        db_url = settings.DATABASE_URL
        if db_url.startswith("postgresql://"):
            db_url = db_url.replace("postgresql://", "")
        
        # Parse connection string
        auth_part, rest = db_url.split("@", 1)
        user, password = auth_part.split(":", 1)
        host_port, database = rest.split("/", 1)
        
        if ":" in host_port:
            host, port = host_port.split(":", 1)
        else:
            host, port = host_port, "5432"
        
        # Run pg_dump
        cmd = [
            "pg_dump",
            f"--host={host}",
            f"--port={port}",
            f"--username={user}",
            f"--dbname={database}",
            "--no-password",
            "--verbose",
            f"--file={backup_path}"
        ]
        
        # Set password environment variable
        env = os.environ.copy()
        env["PGPASSWORD"] = password
        
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        if result.returncode == 0:
            return {"success": True, "backup_path": backup_path}
        else:
            return {"success": False, "error": result.stderr}
            
    except Exception as e:
        return {"success": False, "error": str(e)}


# Database restore helpers
async def restore_database(backup_path: str):
    """Restore database from backup"""
    try:
        import subprocess
        
        # Extract database connection details
        db_url = settings.DATABASE_URL
        if db_url.startswith("postgresql://"):
            db_url = db_url.replace("postgresql://", "")
        
        # Parse connection string
        auth_part, rest = db_url.split("@", 1)
        user, password = auth_part.split(":", 1)
        host_port, database = rest.split("/", 1)
        
        if ":" in host_port:
            host, port = host_port.split(":", 1)
        else:
            host, port = host_port, "5432"
        
        # Run pg_restore
        cmd = [
            "pg_restore",
            f"--host={host}",
            f"--port={port}",
            f"--username={user}",
            f"--dbname={database}",
            "--no-password",
            "--verbose",
            "--clean",
            "--if-exists",
            backup_path
        ]
        
        # Set password environment variable
        env = os.environ.copy()
        env["PGPASSWORD"] = password
        
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        if result.returncode == 0:
            return {"success": True}
        else:
            return {"success": False, "error": result.stderr}
            
    except Exception as e:
        return {"success": False, "error": str(e)}


# Database connection pool monitoring
class DatabaseMonitor:
    """Database connection pool monitor"""
    
    def __init__(self):
        self.engine = engine
    
    async def get_pool_status(self) -> dict:
        """Get connection pool status"""
        return {
            "pool_size": self.engine.pool.size(),
            "checked_in": self.engine.pool.checkedin(),
            "checked_out": self.engine.pool.checkedout(),
            "overflow": self.engine.pool.overflow(),
            "invalid": self.engine.pool.invalid(),
        }
    
    async def get_connection_info(self) -> dict:
        """Get connection information"""
        return {
            "database_url": settings.DATABASE_URL.replace(
                settings.DATABASE_URL.split("@")[0].split(":")[-1], 
                "***"
            ),
            "async_database_url": ASYNC_DATABASE_URL.replace(
                ASYNC_DATABASE_URL.split("@")[0].split(":")[-1], 
                "***"
            ),
            "pool_class": str(self.engine.pool.__class__.__name__),
            "echo": self.engine.echo,
        }


# Database utilities
class DatabaseUtils:
    """Database utility functions"""
    
    @staticmethod
    async def execute_raw_sql(sql: str, params: dict = None) -> list:
        """Execute raw SQL query"""
        async with AsyncSessionLocal() as session:
            result = await session.execute(sql, params or {})
            return result.fetchall()
    
    @staticmethod
    async def execute_raw_sql_scalar(sql: str, params: dict = None):
        """Execute raw SQL query and return scalar result"""
        async with AsyncSessionLocal() as session:
            result = await session.execute(sql, params or {})
            return result.scalar()
    
    @staticmethod
    async def table_exists(table_name: str) -> bool:
        """Check if table exists"""
        sql = """
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = :table_name
        );
        """
        result = await DatabaseUtils.execute_raw_sql_scalar(sql, {"table_name": table_name})
        return result
    
    @staticmethod
    async def get_table_count(table_name: str) -> int:
        """Get row count for table"""
        sql = f"SELECT COUNT(*) FROM {table_name};"
        result = await DatabaseUtils.execute_raw_sql_scalar(sql)
        return result or 0
    
    @staticmethod
    async def get_table_size(table_name: str) -> dict:
        """Get table size information"""
        sql = """
        SELECT 
            pg_size_pretty(pg_total_relation_size(:table_name)) as total_size,
            pg_size_pretty(pg_relation_size(:table_name)) as table_size,
            pg_size_pretty(pg_total_relation_size(:table_name) - pg_relation_size(:table_name)) as index_size
        """
        result = await DatabaseUtils.execute_raw_sql(sql, {"table_name": table_name})
        if result:
            return {
                "total_size": result[0][0],
                "table_size": result[0][1],
                "index_size": result[0][2]
            }
        return {}


# Initialize database monitor
db_monitor = DatabaseMonitor()
db_utils = DatabaseUtils()


# Export for use in other modules
__all__ = [
    "engine",
    "AsyncSessionLocal",
    "Base",
    "metadata",
    "get_db",
    "init_db",
    "close_db",
    "check_db_health",
    "get_db_stats",
    "run_migrations",
    "create_migration",
    "backup_database",
    "restore_database",
    "DatabaseMonitor",
    "DatabaseUtils",
    "db_monitor",
    "db_utils",
]
