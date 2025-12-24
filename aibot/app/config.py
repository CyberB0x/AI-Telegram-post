from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "AI Telegram News Bot"
    debug: bool = True

    database_url: str
    openai_api_key: str
    redis_url: str

    class Config:
        env_file = ".env"


settings = Settings()
