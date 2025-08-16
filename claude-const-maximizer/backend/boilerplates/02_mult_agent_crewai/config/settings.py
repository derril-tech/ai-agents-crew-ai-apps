"""
Application settings and configuration
"""

import os
from typing import List, Optional
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Multi-Agent CrewAI Backend"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost/crewai_db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # AI APIs
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    CREWAI_API_KEY: Optional[str] = None
    
    # Vector Database
    PINECONE_API_KEY: Optional[str] = None
    PINECONE_ENVIRONMENT: Optional[str] = None
    CHROMA_DB_PATH: str = "./chroma_db"
    
    # External APIs
    GOOGLE_API_KEY: Optional[str] = None
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    SENDGRID_API_KEY: Optional[str] = None
    
    # Social Media APIs
    TWITTER_API_KEY: Optional[str] = None
    TWITTER_API_SECRET: Optional[str] = None
    LINKEDIN_CLIENT_ID: Optional[str] = None
    LINKEDIN_CLIENT_SECRET: Optional[str] = None
    
    # Business APIs
    STRIPE_SECRET_KEY: Optional[str] = None
    SHOPIFY_API_KEY: Optional[str] = None
    SHOPIFY_API_SECRET: Optional[str] = None
    
    # Health APIs
    FHIR_BASE_URL: Optional[str] = None
    HL7_ENDPOINT: Optional[str] = None
    
    # Real Estate APIs
    ZILLOW_API_KEY: Optional[str] = None
    
    # SEO APIs
    AHREFS_API_KEY: Optional[str] = None
    GOOGLE_ANALYTICS_ID: Optional[str] = None
    
    # Calendar APIs
    GOOGLE_CALENDAR_CREDENTIALS: Optional[str] = None
    
    # Communication APIs
    SLACK_BOT_TOKEN: Optional[str] = None
    DISCORD_BOT_TOKEN: Optional[str] = None
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    
    # Payment APIs
    PAYPAL_CLIENT_ID: Optional[str] = None
    PAYPAL_CLIENT_SECRET: Optional[str] = None
    
    # CRM APIs
    SALESFORCE_CLIENT_ID: Optional[str] = None
    SALESFORCE_CLIENT_SECRET: Optional[str] = None
    PIPEDRIVE_API_KEY: Optional[str] = None
    
    # Project Management APIs
    ASANA_ACCESS_TOKEN: Optional[str] = None
    TRELLO_API_KEY: Optional[str] = None
    MONDAY_API_TOKEN: Optional[str] = None
    
    # File Storage
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_S3_BUCKET: Optional[str] = None
    GOOGLE_CLOUD_STORAGE_BUCKET: Optional[str] = None
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    DATADOG_API_KEY: Optional[str] = None
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 100
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # Agent Configuration
    MAX_AGENTS_PER_WORKFLOW: int = 10
    MAX_TASKS_PER_AGENT: int = 50
    AGENT_TIMEOUT_SECONDS: int = 300
    WORKFLOW_TIMEOUT_SECONDS: int = 3600
    
    # File Upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: List[str] = [
        "txt", "pdf", "doc", "docx", "xls", "xlsx", 
        "csv", "json", "xml", "html", "md"
    ]
    
    # Email
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_USE_TLS: bool = True
    
    # Webhooks
    WEBHOOK_SECRET: Optional[str] = None
    
    # Cache
    CACHE_TTL: int = 3600  # 1 hour
    CACHE_MAX_SIZE: int = 1000
    
    # Background Jobs
    MAX_CONCURRENT_JOBS: int = 10
    JOB_TIMEOUT_SECONDS: int = 1800  # 30 minutes
    
    # API Versioning
    API_V1_STR: str = "/api/v1"
    
    # Documentation
    DOCS_URL: Optional[str] = "/docs"
    REDOC_URL: Optional[str] = "/redoc"
    
    # Health Check
    HEALTH_CHECK_INTERVAL: int = 30  # seconds
    
    # Metrics
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090
    
    # Development
    AUTO_RELOAD: bool = True
    ENABLE_DEBUG_TOOLBAR: bool = False
    
    # Testing
    TESTING: bool = False
    TEST_DATABASE_URL: Optional[str] = None
    
    # Migration
    ALEMBIC_CONFIG_PATH: str = "alembic.ini"
    
    # Docker
    DOCKER_IMAGE: str = "crewai-backend"
    DOCKER_TAG: str = "latest"
    
    # Kubernetes
    K8S_NAMESPACE: str = "default"
    K8S_REPLICAS: int = 3
    
    # Load Balancer
    LB_HEALTH_CHECK_PATH: str = "/health"
    LB_HEALTH_CHECK_INTERVAL: int = 30
    
    # SSL/TLS
    SSL_CERT_PATH: Optional[str] = None
    SSL_KEY_PATH: Optional[str] = None
    
    # Backup
    BACKUP_ENABLED: bool = False
    BACKUP_SCHEDULE: str = "0 2 * * *"  # Daily at 2 AM
    BACKUP_RETENTION_DAYS: int = 30
    
    # Security Headers
    ENABLE_SECURITY_HEADERS: bool = True
    CONTENT_SECURITY_POLICY: str = "default-src 'self'"
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    
    # Trusted Hosts
    TRUSTED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    
    # Session
    SESSION_SECRET: str = "session-secret-change-in-production"
    SESSION_COOKIE_NAME: str = "crewai_session"
    SESSION_COOKIE_SECURE: bool = False
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SAMESITE: str = "lax"
    
    # Password Policy
    MIN_PASSWORD_LENGTH: int = 8
    REQUIRE_UPPERCASE: bool = True
    REQUIRE_LOWERCASE: bool = True
    REQUIRE_DIGITS: bool = True
    REQUIRE_SPECIAL_CHARS: bool = True
    
    # Account Lockout
    MAX_LOGIN_ATTEMPTS: int = 5
    LOCKOUT_DURATION_MINUTES: int = 15
    
    # Email Verification
    REQUIRE_EMAIL_VERIFICATION: bool = True
    EMAIL_VERIFICATION_EXPIRE_HOURS: int = 24
    
    # Password Reset
    PASSWORD_RESET_EXPIRE_HOURS: int = 1
    
    # Two-Factor Authentication
    ENABLE_2FA: bool = False
    TOTP_ISSUER: str = "CrewAI Backend"
    
    # API Keys
    ENABLE_API_KEYS: bool = True
    API_KEY_PREFIX: str = "crewai_"
    
    # WebSocket
    ENABLE_WEBSOCKET: bool = True
    WEBSOCKET_PING_INTERVAL: int = 20
    WEBSOCKET_PING_TIMEOUT: int = 20
    
    # Real-time Updates
    ENABLE_REALTIME_UPDATES: bool = True
    REALTIME_UPDATE_INTERVAL: int = 5  # seconds
    
    # Agent Communication
    AGENT_COMMUNICATION_TIMEOUT: int = 60  # seconds
    AGENT_RETRY_ATTEMPTS: int = 3
    AGENT_RETRY_DELAY: int = 5  # seconds
    
    # Workflow Persistence
    ENABLE_WORKFLOW_PERSISTENCE: bool = True
    WORKFLOW_SNAPSHOT_INTERVAL: int = 60  # seconds
    
    # Task Queue
    TASK_QUEUE_NAME: str = "crewai_tasks"
    TASK_PRIORITY_LEVELS: int = 5
    TASK_RETRY_POLICY: str = "exponential_backoff"
    
    # Performance
    ENABLE_CACHING: bool = True
    CACHE_BACKEND: str = "redis"
    ENABLE_COMPRESSION: bool = True
    COMPRESSION_LEVEL: int = 6
    
    # Monitoring
    ENABLE_APM: bool = False
    APM_SERVICE_NAME: str = "crewai-backend"
    APM_SERVER_URL: Optional[str] = None
    
    # Alerting
    ENABLE_ALERTS: bool = False
    ALERT_WEBHOOK_URL: Optional[str] = None
    ALERT_EMAIL_RECIPIENTS: List[str] = []
    
    # Audit Logging
    ENABLE_AUDIT_LOG: bool = True
    AUDIT_LOG_LEVEL: str = "INFO"
    AUDIT_LOG_RETENTION_DAYS: int = 90
    
    # Data Retention
    DATA_RETENTION_DAYS: int = 365
    AUTO_CLEANUP_ENABLED: bool = True
    CLEANUP_SCHEDULE: str = "0 3 * * *"  # Daily at 3 AM
    
    # Feature Flags
    ENABLE_EXPERIMENTAL_FEATURES: bool = False
    ENABLE_BETA_FEATURES: bool = False
    
    # Integration Limits
    MAX_API_CALLS_PER_MINUTE: int = 1000
    MAX_CONCURRENT_INTEGRATIONS: int = 50
    
    # Agent Limits
    MAX_AGENTS_PER_USER: int = 100
    MAX_WORKFLOWS_PER_USER: int = 50
    MAX_TASKS_PER_WORKFLOW: int = 100
    
    # Resource Limits
    MAX_MEMORY_USAGE_MB: int = 1024
    MAX_CPU_USAGE_PERCENT: int = 80
    MAX_DISK_USAGE_PERCENT: int = 90
    
    # Backup and Recovery
    BACKUP_FREQUENCY: str = "daily"
    BACKUP_COMPRESSION: bool = True
    BACKUP_ENCRYPTION: bool = True
    
    # Disaster Recovery
    ENABLE_DISASTER_RECOVERY: bool = False
    DR_REPLICATION_INTERVAL: int = 300  # 5 minutes
    
    # Compliance
    GDPR_COMPLIANCE: bool = True
    HIPAA_COMPLIANCE: bool = False
    SOC2_COMPLIANCE: bool = False
    
    # Privacy
    DATA_ENCRYPTION_AT_REST: bool = True
    DATA_ENCRYPTION_IN_TRANSIT: bool = True
    PII_MASKING: bool = True
    
    # Performance Optimization
    ENABLE_QUERY_OPTIMIZATION: bool = True
    ENABLE_CONNECTION_POOLING: bool = True
    ENABLE_QUERY_CACHING: bool = True
    
    # Development Tools
    ENABLE_DEBUG_MODE: bool = False
    ENABLE_PROFILING: bool = False
    ENABLE_METRICS_COLLECTION: bool = True
    
    # API Documentation
    ENABLE_SWAGGER: bool = True
    ENABLE_REDOC: bool = True
    API_DOCS_TITLE: str = "CrewAI Backend API"
    API_DOCS_DESCRIPTION: str = "Backend API for multi-agent AI systems"
    
    # Version Control
    GIT_COMMIT_HASH: Optional[str] = None
    GIT_BRANCH: Optional[str] = None
    BUILD_DATE: Optional[str] = None
    
    # Deployment
    DEPLOYMENT_ENVIRONMENT: str = "development"
    DEPLOYMENT_REGION: Optional[str] = None
    DEPLOYMENT_VERSION: Optional[str] = None
    
    # Health Checks
    HEALTH_CHECK_ENDPOINTS: List[str] = ["/health", "/api/v1/health"]
    HEALTH_CHECK_TIMEOUT: int = 30
    HEALTH_CHECK_RETRIES: int = 3
    
    # Circuit Breaker
    ENABLE_CIRCUIT_BREAKER: bool = True
    CIRCUIT_BREAKER_THRESHOLD: int = 5
    CIRCUIT_BREAKER_TIMEOUT: int = 60
    
    # Load Balancing
    ENABLE_LOAD_BALANCING: bool = False
    LOAD_BALANCER_ALGORITHM: str = "round_robin"
    
    # Auto Scaling
    ENABLE_AUTO_SCALING: bool = False
    MIN_INSTANCES: int = 1
    MAX_INSTANCES: int = 10
    SCALE_UP_THRESHOLD: int = 80
    SCALE_DOWN_THRESHOLD: int = 20
    
    # Maintenance Mode
    MAINTENANCE_MODE: bool = False
    MAINTENANCE_MESSAGE: str = "System is under maintenance"
    
    # Feature Toggles
    FEATURE_TOGGLES: dict = {
        "advanced_agents": True,
        "workflow_templates": True,
        "real_time_monitoring": True,
        "api_integrations": True,
        "advanced_analytics": False,
        "machine_learning": True,
        "natural_language_processing": True,
        "computer_vision": False,
        "blockchain_integration": False,
        "iot_support": False
    }
    
    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict) -> str:
        """Assemble database connection string"""
        if isinstance(v, str):
            return v
        
        # Build from components if not provided
        user = values.get("DB_USER", "user")
        password = values.get("DB_PASSWORD", "password")
        host = values.get("DB_HOST", "localhost")
        port = values.get("DB_PORT", "5432")
        name = values.get("DB_NAME", "crewai_db")
        
        return f"postgresql://{user}:{password}@{host}:{port}/{name}"
    
    @validator("ALLOWED_HOSTS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str]:
        """Assemble CORS origins"""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
_settings = None


def get_settings() -> Settings:
    """Get settings instance"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


# Export settings for use in other modules
settings = get_settings()
