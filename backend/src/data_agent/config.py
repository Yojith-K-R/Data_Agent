from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Data Agent API"
    app_version: str = "0.1.0"

    openai_api_key: str | None = None
    groq_api_key: str | None = None
    database_url: str | None = None
    host : str | None= None
    port : str | None= None
    user : str | None= None
    password : str | None= None
    database : str | None= None
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()