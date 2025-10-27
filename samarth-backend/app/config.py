from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True
    # FIX #1: Add the ENVIRONMENT field, as it's in your .env
    ENVIRONMENT: str = "development" 
    
    # AI Service
    GEMINI_API_KEY: str # Must be filled in .env
    AI_MODEL: str = "gemini-pro"
    
    # Data Sources
    DATA_GOV_API_KEY: str = ""
    DATA_GOV_BASE_URL: str = "https://api.data.gov.in/resource"
    
    # Security (Placeholder for POC)
    SECRET_KEY: str # Must be filled in .env
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # FIX #2: Use the modern config and include list parsing flags
    model_config = SettingsConfigDict(
        env_file = ".env",
        case_sensitive = True,
        # This tells Pydantic to split strings by comma for list/set types
        env_parse_lists = True 
    )

settings = Settings()