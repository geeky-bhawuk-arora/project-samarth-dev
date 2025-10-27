from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True
    
    # AI Service
    GEMINI_API_KEY: str
    AI_MODEL: str = "gemini-pro"
    
    # Data Sources
    DATA_GOV_API_KEY: str = ""
    DATA_GOV_BASE_URL: str = "https://api.data.gov.in/resource"
    
    # Security (Placeholder for POC)
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()