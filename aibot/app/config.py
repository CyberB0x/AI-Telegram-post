from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional


class Settings(BaseSettings):
    app_name: str = "AI Telegram News Bot"
    debug: bool = True

    database_url: str = "sqlite:///./aibot.db"
    openai_api_key: str = "mock-key"

    telegram_bot_token: str
    telegram_chat_id: str

    redis_url: Optional[str] = None

    model_config = ConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()
