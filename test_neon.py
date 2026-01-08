import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine

async def run():
    url = "postgresql+asyncpg://neondb_owner:npg_hzlM1ECn7kmu@ep-small-flower-admw54i9-pooler.c-2.us-east-1.aws.neon.tech/neondb"
    print(f"Testing URL with SQLAlchemy: {url}")
    try:
        engine = create_async_engine(url, connect_args={"ssl": True})
        async with engine.connect() as conn:
            print("Connected successfully with SQLAlchemy!")
        await engine.dispose()
    except Exception as e:
        print(f"Connection failed with SQLAlchemy: {e}")

if __name__ == "__main__":
    asyncio.run(run())
