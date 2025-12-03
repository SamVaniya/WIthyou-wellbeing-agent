"""
config/settings.py
Centralized configuration for the application.
Refactored for Pydantic V2 Compliance.
"""
"""
config/settings.py
Centralized configuration for the application.
Refactored for Pydantic V2 Compliance.
"""
import os
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Infrastructure
    GOOGLE_API_KEY: str = Field(..., alias="GOOGLE_API_KEY")
    ENV: str = Field("development", alias="ENV")
    APP_NAME: str = "withyou_clinical_system"
    
    # Model Configurations
    # [FIX]: Trying 'latest' alias which often resolves v1beta routing issues
    SAFETY_MODEL: str = "gemini-1.5-flash" 
    REASONING_MODEL: str = "gemini-1.5-pro"
    
    # Clinical Thresholds
    MAX_RETRY_ATTEMPTS: int = 3
    CRISIS_TRIGGER_KEYWORDS: list = ["suicide", "kill myself", "end it all"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = 'ignore'

# Singleton instance
settings = Settings()