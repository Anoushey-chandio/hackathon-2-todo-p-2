import asyncio
from sqlalchemy import text
from src.core.database import async_engine
from dotenv import load_dotenv
import os

# Load env for verification script just in case
load_dotenv(dotenv_path="backend/.env")

async def verify_db():
    print("--- Verifying Database Connection ---")
    try:
        async with async_engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            print(f"DB Connection: SUCCESS (Result: {result.scalar()})")
            
            # Check Tables
            result = await conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
            tables = result.scalars().all()
            print(f"Tables found: {tables}")
            
            required_tables = ["user", "session", "account", "verification", "tasks"]
            missing = [t for t in required_tables if t not in tables]
            
            if missing:
                print(f"MISSING TABLES: {missing}")
            else:
                print("All required tables present.")
                
    except Exception as e:
        print(f"DB Connection FAILED: {e}")

if __name__ == "__main__":
    asyncio.run(verify_db())
