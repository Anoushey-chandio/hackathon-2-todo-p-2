from sqlmodel import create_engine, Session, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession, AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine
from .config import settings

# Neon requires sslmode=require usually, which is in the URL.
# Asyncpg needs postgresql+asyncpg:// scheme.
database_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# Use create_async_engine from sqlalchemy.ext.asyncio directly
async_engine = create_async_engine(database_url, echo=True)

# Async session factory
async def get_db() -> AsyncSession:
    async with AsyncSession(async_engine) as session:
        yield session

async def init_db():
    async with async_engine.begin() as conn:
        # SQLModel.metadata.create_all is not async, so run in a sync context
        # This will create tables if they don't exist
        await conn.run_sync(SQLModel.metadata.create_all)