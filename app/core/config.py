"""Base Settings."""

import secrets
from os import getenv

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    """Base Settings."""

    app_name: str = "API AI Application"
    app_env: str = (
        "development"  # Дозволені значення: development, staging, production, testing, test
    )
    debug: bool = True

    database_url: str
    secret_key: str
    postgres_password: str = ""
    postgres_db: str = ""
    postgres_user: str = ""

    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    algorithms: str = "HS256"

    AWS_REGION: str = "eu-central-1"
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    S3_BUCKET_NAME: str = ""
    MAX_UPLOAD_SIZE_MB: int = 10

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class TestSettings(Settings):
    """Settings for testing environment."""

    app_env: str = "test"
    database_url: str = "postgresql://test_user:test_pass@postgres:5432/test_db"
    secret_key: str = secrets.token_urlsafe(32)
    postgres_password: str = "test_pass"
    postgres_db: str = "test_db"
    postgres_user: str = "test_user"
    AWS_ACCESS_KEY_ID: str = "test_key"
    AWS_SECRET_ACCESS_KEY: str = "test_secret"
    S3_BUCKET_NAME: str = "test_bucket"
    debug: bool = True


# Вибираємо налаштування залежно від середовища
env = getenv("APP_ENV", "development")
if env == "test":
    settings = TestSettings()
else:
    settings = Settings()
