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
    
    # NEW: PostgreSQL Database Configuration
    POSTGRES_USER: str = Field("samarth_user", description="PostgreSQL database user.")
    POSTGRES_PASSWORD: str = Field("samarth_password", description="PostgreSQL database password.")
    POSTGRES_SERVER: str = Field("localhost", description="PostgreSQL server hostname.")
    POSTGRES_PORT: str = Field("5432", description="PostgreSQL server port.")
    POSTGRES_DB: str = Field("samarth_db", description="PostgreSQL database name.")

    # Computed Database URL (Used by SQLAlchemy and pandas)
    @property
    def DATABASE_URL(self) -> str:
        # Using psycopg2 driver
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # Security (Placeholder for POC)
    SECRET_KEY: str = Field("a-very-secure-secret-key-for-poc-only", description="A strong secret key for security tokens.")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    model_config = SettingsConfigDict(
        env_file = ".env",
        case_sensitive = True,
        env_parse_lists = True 
    )

settings = Settings()
