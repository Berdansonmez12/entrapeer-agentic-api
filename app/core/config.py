from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    google_api_key: str
    tavily_api_key: str | None = None

    mongodb_uri: str = "mongodb://mongodb:27017"
    mongodb_db_name: str = "entrapeer"

    redis_url: str = "redis://redis:6379/0"

    app_env: str = "development"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()