import asyncio
import sys
import os
from pathlib import Path

# Add backend to sys.path
sys.path.append(str(Path(__file__).parent))

from src.core.database import async_engine
from src.models.base import SQLModel as BaseSQLModel
from src.models.user import User
from src.models.auth import Account, Session
from sqlalchemy import text

async def reset_users():
    async with async_engine.begin() as conn:
        print("Resetting User, Account, Session tables...")
        # Use DELETE instead of TRUNCATE for safety/compatibility or CASCADE
        # user is a reserved keyword in Postgres, must be quoted
        try:
             await conn.execute(text('TRUNCATE TABLE "session" CASCADE'))
             await conn.execute(text('TRUNCATE TABLE "account" CASCADE'))
             await conn.execute(text('TRUNCATE TABLE "user" CASCADE'))
        except Exception as e:
            print(f"Truncate failed, trying DELETE: {e}")
            await conn.execute(text('DELETE FROM "session"'))
            await conn.execute(text('DELETE FROM "account"'))
            await conn.execute(text('DELETE FROM "user"'))
            
        print("Tables reset.")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(reset_users())
