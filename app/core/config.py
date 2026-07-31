"""Base Settings."""

import secrets
from os import getenv

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

env = getenv("APP_ENV", "development")

# .env files for local development only
if env != "production":
    env_file = ".env.local"
    load_dotenv(env_file)
else:
    env_file = None  # In production, variables are already provided by the container environment


class Settings(BaseSettings):
    """Base Settings."""

    app_name: str = "Robot Payment Testing Platform"
    app_env: str = "development"
    debug: bool = True

    database_url: str = "postgresql://robot_user:robot_pass@db:5432/robot_payment"

    secret_key: str = "dev-secret-key-change-in-production"
    algorithms: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    aws_region: str = "eu-central-1"
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    s3_bucket_name: str = ""
    max_upload_size_mb: int = 10

    model_config = SettingsConfigDict(env_file=env_file, extra="ignore")


class TestSettings(Settings):
    """Settings for testing environment."""

    app_env: str = "test"
    database_url: str = "postgresql://test_user:test_pass@postgres:5432/test_db"
    secret_key: str = secrets.token_urlsafe(32)
    debug: bool = True


settings = TestSettings() if env == "test" else Settings()
