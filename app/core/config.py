"""Base Settings"""

from pydantic_settings import BaseSettings, SettingsConfigDict  # type: ignore[reportMissingImports]  # pylint: disable=import-error


class Settings(BaseSettings):
    """Main Settings for the application"""

    app_name: str = "Robot Payment Testing"
    app_env: str = "development"
    debug: bool = True
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    database_url: str

    @property
    def sync_database_url(self) -> str:
        """Url to the database from the .env file"""
        return self.database_url.replace("+asyncpg", "")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()  # type: ignore
