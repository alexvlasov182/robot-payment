"""Base Settings"""

from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    app_name: str = "Robot Payment Testing"
    app_env: Literal["development", "staging", "production"] = "development"
    debug: bool = True
    secret_key: str
    algorithms: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    database_url: str

    @property
    def sync_database_url(self) -> str:
        """Convert async URL to sync for SQLAlchemy"""
        return self.database_url.replace("+asyncpg", "")

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )


settings = Settings()  # type: ignore
