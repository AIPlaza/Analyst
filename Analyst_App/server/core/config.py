import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = "postgresql+psycopg2://user:password@localhost:5432/analyst_app"
    COINGECKO_API_BASE_URL: str = "https://api.coingecko.com/api/v3"
    REDIS_URL: str = "redis://localhost:6379/0"


@lru_cache()
def get_settings():
    return Settings()
