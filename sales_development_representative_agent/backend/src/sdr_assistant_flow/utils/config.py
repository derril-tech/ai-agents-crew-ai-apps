"""
Configuration Management for SDR Assistant

This module handles all configuration settings for the application,
including environment variables, API keys, and application settings.
"""

import os
import sys
from typing import List, Optional, Dict, Any
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = False
    environment: str = "development"
    
    # CORS Configuration
    cors_origins: str = "http://localhost:3000,http://localhost:3001,https://your-vercel-app.vercel.app"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convert comma-separated CORS origins string to list"""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]
    
    # AI Model Configuration
    model: str = "gpt-4o-mini"
    openai_api_key: str
    serper_api_key: str
    
    # Database Configuration
    database_url: Optional[str] = "sqlite:///./sdr_assistant.db"
    redis_url: Optional[str] = "redis://localhost:6379"
    
    # CrewAI Configuration
    pythonpath: str = "src"
    crew_verbose: bool = True
    max_iterations: int = 3
    
    # Email Configuration
    smtp_host: Optional[str] = None
    smtp_port: Optional[int] = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    smtp_use_tls: bool = True
    
    # Application Limits
    max_leads_per_batch: int = 100
    max_concurrent_flows: int = 10
    session_timeout_hours: int = 24
    
    # File Storage
    upload_directory: str = "./uploads"
    results_directory: str = "./results"
    
    # Security
    secret_key: str = "your-secret-key-change-this-in-production"
    access_token_expire_minutes: int = 30
    
    # Feature Flags
    enable_lead_enrichment: bool = True
    enable_email_tracking: bool = True
    enable_analytics: bool = True
    enable_webhooks: bool = True
    enable_ab_testing: bool = True
    
    # External Services
    linkedin_api_key: Optional[str] = None
    clearbit_api_key: Optional[str] = None
    hunter_api_key: Optional[str] = None
    
    # Logging
    log_level: str = "INFO"
    log_file: Optional[str] = None
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        
        # Environment variable prefixes
        env_prefix = ""
        
        # Allow extra fields for future extensibility
        extra = "allow"

class CrewAIConfig(BaseSettings):
    """Specific configuration for CrewAI components"""
    
    # LLM Configuration
    llm_provider: str = "openai"
    llm_model: str = "gpt-4o-mini"
    llm_temperature: float = 0.1
    llm_max_tokens: Optional[int] = None
    
    # Embeddings Configuration
    embedder_provider: str = "openai"
    embedder_model: str = "text-embedding-3-small"
    
    # Agent Configuration
    agent_max_iter: int = 3
    agent_memory: bool = True
    agent_verbose: bool = True
    
    # Task Configuration
    task_timeout: int = 300  # 5 minutes
    
    # Tools Configuration
    tools_timeout: int = 30
    serper_num_results: int = 10
    
    class Config:
        env_file = ".env"
        env_prefix = "CREWAI_"

class DatabaseConfig(BaseSettings):
    """Database configuration settings"""
    
    database_url: str = "sqlite:///./sdr_assistant.db"
    pool_size: int = 5
    max_overflow: int = 10
    pool_timeout: int = 30
    pool_recycle: int = 3600
    echo: bool = False
    
    class Config:
        env_file = ".env"
        env_prefix = "DB_"

@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings"""
    return Settings()

@lru_cache()
def get_crewai_config() -> CrewAIConfig:
    """Get cached CrewAI configuration"""
    return CrewAIConfig()

@lru_cache()
def get_database_config() -> DatabaseConfig:
    """Get cached database configuration"""
    return DatabaseConfig()

def load_config() -> Settings:
    """Load and validate configuration"""
    settings = get_settings()
    
    # Validate required settings
    required_keys = ["openai_api_key", "serper_api_key"]
    missing_keys = [key for key in required_keys if not getattr(settings, key)]
    
    if missing_keys:
        raise ValueError(f"Missing required configuration: {', '.join(missing_keys)}")
    
    # Create directories if they don't exist
    os.makedirs(settings.upload_directory, exist_ok=True)
    os.makedirs(settings.results_directory, exist_ok=True)
    
    return settings

def get_llm_config() -> Dict[str, Any]:
    """Get LLM configuration for CrewAI"""
    settings = get_settings()
    crewai_config = get_crewai_config()
    
    return {
        "provider": crewai_config.llm_provider,
        "config": {
            "model": crewai_config.llm_model,
            "temperature": crewai_config.llm_temperature,
            "api_key": settings.openai_api_key,
            "max_tokens": crewai_config.llm_max_tokens,
        }
    }

def get_embedder_config() -> Dict[str, Any]:
    """Get embedder configuration for CrewAI"""
    settings = get_settings()
    crewai_config = get_crewai_config()
    
    return {
        "provider": crewai_config.embedder_provider,
        "config": {
            "model": crewai_config.embedder_model,
            "api_key": settings.openai_api_key,
        }
    }

def get_tool_configs() -> Dict[str, Dict[str, Any]]:
    """Get configuration for various tools"""
    settings = get_settings()
    
    return {
        "serper": {
            "api_key": settings.serper_api_key,
            "num_results": get_crewai_config().serper_num_results
        },
        "linkedin": {
            "api_key": settings.linkedin_api_key,
            "enabled": bool(settings.linkedin_api_key)
        },
        "clearbit": {
            "api_key": settings.clearbit_api_key,
            "enabled": bool(settings.clearbit_api_key)
        },
        "hunter": {
            "api_key": settings.hunter_api_key,
            "enabled": bool(settings.hunter_api_key)
        }
    }

# Development helpers
def print_config_summary():
    """Print a summary of current configuration (for debugging)"""
    settings = get_settings()
    
    print("🔧 SDR Assistant Configuration Summary")
    print("=" * 50)
    print(f"Environment: {settings.environment}")
    print(f"Debug Mode: {settings.debug}")
    print(f"API Host: {settings.api_host}:{settings.api_port}")
    print(f"Model: {settings.model}")
    print(f"Database: {settings.database_url}")
    print(f"CORS Origins: {len(settings.cors_origins)} configured")
    print(f"Feature Flags:")
    print(f"  - Lead Enrichment: {settings.enable_lead_enrichment}")
    print(f"  - Email Tracking: {settings.enable_email_tracking}")
    print(f"  - Analytics: {settings.enable_analytics}")
    print(f"  - A/B Testing: {settings.enable_ab_testing}")
    print("=" * 50)

if __name__ == "__main__":
    # For testing configuration
    try:
        config = load_config()
        print_config_summary()
        print("✅ Configuration loaded successfully!")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        sys.exit(1)