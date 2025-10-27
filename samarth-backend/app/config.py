from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    # api config
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True
    ENVIRONMENT: str = "development" 
    
    # gemini api key
    GEMINI_API_KEY: str = Field(..., description="The required API Key for Google Gemini.")
    AI_MODEL: str = "gemini-2.5-flash"
    
    # data src
    # DATA_GOV_API_KEY: str = Field(default="", description="The API Key for the external data service (data.gov.in).")
    # DATA_GOV_BASE_URL: str = "https://api.data.gov.in/resource"
    
    # Security (Placeholder for POC)
    SECRET_KEY: str = Field(..., description="A strong secret key for security tokens.")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # ALLOW_ORIGINS=""
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    model_config = SettingsConfigDict(
        env_file = ".env",
        case_sensitive = True,
        env_parse_lists = True 
    )

settings = Settings()