from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from .config import settings
from sqlalchemy.engine.url import make_url
# Import models to register them with SQLModel.metadata
from src.models import User, Task, Session, Account, Verification, Jwks

database_url = settings.DATABASE_URL
# Ensure async driver
if "postgresql://" in database_url or "postgresql+asyncpg://" in database_url:
    url = make_url(database_url)
    query = dict(url.query)
    query.pop("sslmode", None)
    query.pop("channel_binding", None)
    
    url = url.set(drivername="postgresql+asyncpg", query=query)
else:
    url = make_url(database_url)

connect_args = {}
# Check original string or url.host for neon
if "neon.tech" in str(url):
    connect_args["ssl"] = "require"

# Use create_async_engine from sqlalchemy.ext.asyncio directly
async_engine = create_async_engine(
    url, 
    echo=True,
    connect_args=connect_args
)

# Async session factory
async def get_db() -> AsyncSession:
    async with AsyncSession(async_engine) as session:
        yield session

async def init_db():
    async with async_engine.begin() as conn:
        # SQLModel.metadata.create_all is not async, so run in a sync context
        # This will create tables if they don't exist
        await conn.run_sync(SQLModel.metadata.create_all)