import asyncio
import os
from dotenv import load_dotenv
from pathlib import Path

# Load env vars from backend/.env relative to this file
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=BASE_DIR / ".env", override=True)

from src.core.database import init_db, async_engine
from src.models.user import User
from src.models.auth import Session, Account, Verification
from src.models.task import Task
from sqlmodel import text

async def main():
    print(f"Connecting to: {os.getenv('DATABASE_URL')}")
    try:
        await init_db()
        print("Database initialized successfully.")
        
        async with async_engine.connect() as conn:
            result = await conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
            tables = result.scalars().all()
            print(f"Tables in database: {tables}")
            
    except Exception as e:
        print(f"Error initializing database: {e}")

if __name__ == "__main__":
    asyncio.run(main())
