import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
from sqlmodel import SQLModel
from src.models.user import User 
from src.models.task import Task
from src.models.auth import Session, Account, Verification
from src.models.jwks import Jwks

target_metadata = SQLModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

from src.core.config import settings

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    from sqlalchemy.engine.url import make_url
    from sqlalchemy.ext.asyncio import create_async_engine
    
    # 1. Get URL from settings
    database_url = settings.DATABASE_URL
    
    # 2. Process URL exactly like database.py
    if "postgresql://" in database_url or "postgresql+asyncpg://" in database_url:
        url = make_url(database_url)
        query = dict(url.query)
        query.pop("sslmode", None)
        query.pop("channel_binding", None)
        
        url = url.set(drivername="postgresql+asyncpg", query=query)
    else:
        url = make_url(database_url)

    connect_args = {}
    if "neon.tech" in str(url):
        connect_args["ssl"] = "require"

    # 3. Create engine directly (skipping async_engine_from_config for direct control)
    connectable = create_async_engine(
        url,
        poolclass=pool.NullPool,
        connect_args=connect_args,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
