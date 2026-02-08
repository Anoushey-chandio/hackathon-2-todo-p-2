from dotenv import load_dotenv
from pathlib import Path
import os

# Explicitly load local .env and override system env
env_path = Path(__file__).resolve().parent.parent / ".env"

# Debug prints only in development
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

if DEBUG:
    print(f"🔍 Loading .env from: {env_path}")
    print(f"📁 File exists: {env_path.exists()}")

load_dotenv(dotenv_path=env_path, override=True)

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    DATABASE_URL: str
    BETTER_AUTH_SECRET: str
    SECRET_KEY: str = Field(alias="BETTER_AUTH_SECRET")
    
    # Optional settings
    DEBUG: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

# Debug prints only in development
if settings.DEBUG:
    print(f"✅ DATABASE_URL loaded: {settings.DATABASE_URL[:80]}...")
    print(f"🔑 Has password in URL: {'npg_' in settings.DATABASE_URL}")
    print(f"🔒 Has sslmode: {'sslmode' in settings.DATABASE_URL}")