from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "AI Telegram News Bot"
    debug: bool = True

    database_url: str = "sqlite:///./aibot.db"
    openai_api_key: str = "mock-key"
    redis_url: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()
