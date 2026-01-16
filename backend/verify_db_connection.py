import asyncio
import sys
import os

# Add backend to sys.path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from src.core.database import async_engine
from sqlalchemy import text

async def verify():
    print("Verifying database connection...")
    try:
        async with async_engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            print(f"Connection successful! Result: {result.scalar()}")
    except Exception as e:
        print(f"Connection failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(verify())