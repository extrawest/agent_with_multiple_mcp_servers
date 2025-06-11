from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    news_api_key: Optional[str] = Field(default=None, description="News API key")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"

settings = Settings()