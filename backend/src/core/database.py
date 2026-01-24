from typing import AsyncGenerator
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.engine.url import make_url
from .config import settings

# Import models to register with metadata
from src.models import User, Task, Session, Account, Verification  # removed Jwks

DATABASE_URL = settings.DATABASE_URL

# Parse URL to ensure async driver
url = make_url(DATABASE_URL)

# Ensure asyncpg driver for PostgreSQL
if url.drivername in ("postgresql", "postgresql+asyncpg"):
    query = dict(url.query)
    query.pop("sslmode", None)
    query.pop("channel_binding", None)
    url = url.set(drivername="postgresql+asyncpg", query=query)

connect_args = {}
# If using Neon, require SSL
if "neon.tech" in str(url):
    connect_args["ssl"] = "require"

# Create async engine
async_engine = create_async_engine(
    url,
    echo=True,
    connect_args=connect_args,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    pool_recycle=300
)

# Async session factory
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(async_engine, expire_on_commit=False) as session:
        yield session

# Initialize database (create tables)
async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
