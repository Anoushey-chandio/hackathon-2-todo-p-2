from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

class Settings(BaseSettings):
    DATABASE_URL: str
    BETTER_AUTH_SECRET: str
    SECRET_KEY: str = Field(alias="BETTER_AUTH_SECRET")
    
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding='utf-8',
        extra='ignore'
    )

settings = Settings()
