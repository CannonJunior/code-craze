"""
Application configuration settings.

Reads configuration from environment variables using pydantic-settings.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    All settings can be overridden by creating a .env file.
    """

    # Application
    app_name: str = Field(default="Code Craze Academy", alias="APP_NAME")
    app_version: str = Field(default="0.1.0", alias="APP_VERSION")
    debug: bool = Field(default=False, alias="DEBUG")
    port: int = Field(default=8989, alias="PORT")

    # Database
    database_url: str = Field(default="sqlite:///data/code_craze.db", alias="DATABASE_URL")

    # Security
    secret_key: str = Field(default="dev-secret-key-change-in-production", alias="SECRET_KEY")
    algorithm: str = Field(default="HS256", alias="ALGORITHM")
    access_token_expire_minutes: int = Field(default=10080, alias="ACCESS_TOKEN_EXPIRE_MINUTES")  # 1 week

    # CORS - Include localhost for development and render.com for production
    allowed_origins: str = Field(
        default="http://localhost:8989,http://127.0.0.1:8989,https://code-craze-academy.onrender.com",
        alias="ALLOWED_ORIGINS"
    )

    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        case_sensitive = False
        extra = "allow"

    @property
    def cors_origins(self) -> List[str]:
        """Get CORS origins as a list."""
        return [origin.strip() for origin in self.allowed_origins.split(",")]


# Global settings instance
settings = Settings()
