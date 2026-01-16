import asyncio
import sys
import os
from sqlalchemy import text

# Add backend to sys.path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from src.core.database import async_engine

async def reset_tasks_table():
    async with async_engine.begin() as conn:
        print("Dropping tasks table...")
        await conn.execute(text("DROP TABLE IF EXISTS tasks CASCADE"))
        print("Tasks table dropped.")
        # Re-init will happen on app startup, or I can trigger it here?
        # App startup calls init_db.
        # But let's just let the app handle creation or do it manually if needed.
        # actually init_db is called in lifespan.

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(reset_tasks_table())
