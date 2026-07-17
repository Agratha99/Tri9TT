from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central application configuration.

    Values are loaded from environment variables or a local .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = Field(
        default="Tri9T CT-200 Backend",
        description="Application display name.",
    )

    database_url: str = Field(
        default="sqlite:///./tri9t.db",
        description="Primary SQLAlchemy database URL.",
        alias="DATABASE_URL",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Return a cached application settings instance.
    """
    return Settings()