import os
from typing import Optional

class Settings:
    """Simple settings class using environment variables"""
    
    def __init__(self):
        # OpenAI Configuration
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.model_name = os.getenv("MODEL_NAME", "gpt-4o-mini")
        
        # Application Configuration
        self.app_name = "Py-Agentic AI"
        self.app_version = "1.0.0"
        self.root_path = "/agenticai"
        
        # CORS Configuration
        self.cors_origins = ["http://localhost:3000"]
        
        # Logging Configuration
        self.log_level = os.getenv("LOG_LEVEL", "INFO")

# Global settings instance
settings = Settings()
