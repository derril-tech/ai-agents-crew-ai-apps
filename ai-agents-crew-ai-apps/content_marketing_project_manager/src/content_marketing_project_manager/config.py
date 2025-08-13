import os
from pathlib import Path
from typing import Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Config:
    """Configuration management for the Content Marketing Project Manager."""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self._load_env_vars()
    
    def _load_env_vars(self):
        """Load environment variables with defaults."""
        # Try to load from .env file if it exists
        env_file = self.base_path / ".env"
        if env_file.exists():
            try:
                from dotenv import load_dotenv
                load_dotenv(env_file)
                logger.info(f"Loaded environment variables from {env_file}")
            except ImportError:
                logger.warning("python-dotenv not available, skipping .env file loading")
    
    @property
    def openai_api_key(self) -> Optional[str]:
        """Get OpenAI API key from environment."""
        return os.getenv("OPENAI_API_KEY")
    
    @property
    def verbose_logging(self) -> bool:
        """Get verbose logging setting from environment."""
        return os.getenv("VERBOSE_LOGGING", "false").lower() == "true"
    
    @property
    def max_iterations(self) -> int:
        """Get max iterations for crew execution."""
        return int(os.getenv("MAX_ITERATIONS", "5"))
    
    def validate_config(self) -> bool:
        """Validate that required configuration is present."""
        required_vars = ["OPENAI_API_KEY"]
        missing_vars = []
        
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
            return False
        
        return True
    
    def _get_timestamp(self) -> str:
        """Generate a timestamp string for file naming."""
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def _get_timestamp(self) -> str:
        """Get current timestamp for file naming."""
        return datetime.now().strftime("%Y%m%d_%H%M%S")

# Global config instance
config = Config()
