"""Base Settings."""

import secrets
from os import getenv

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

env = getenv("APP_ENV", "development")

# .env файли для локальної розробки тільки
if env != "production":
    env_file = ".env.local"
    load_dotenv(env_file)
else:
    env_file = None  # на проді змінні вже в оточенні контейнера


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

    AWS_REGION: str = "eu-central-1"
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    S3_BUCKET_NAME: str = ""
    MAX_UPLOAD_SIZE_MB: int = 10

    model_config = SettingsConfigDict(env_file=env_file, extra="ignore")


class TestSettings(Settings):
    """Settings for testing environment."""

    app_env: str = "test"
    database_url: str = "postgresql://test_user:test_pass@postgres:5432/test_db"
    secret_key: str = secrets.token_urlsafe(32)
    debug: bool = True


settings = TestSettings() if env == "test" else Settings()
