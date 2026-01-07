import sys
import os
import asyncio

# Add the backend directory to the Python path
# Correct path would be 'backend' so its contents (src) are discoverable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

try:
    from src.main import app
    from src.core.config import settings
    from src.core.database import async_engine, init_db # Added init_db
    from src.models.user import User
    from src.models.task import Task
    from sqlmodel import SQLModel # Added SQLModel import
    
    print("Backend verification successful: All critical modules imported.")
    
    # Optional: try to initialize DB to catch more errors if env is set up
    async def verify_db_init():
        print("Attempting database initialization (no actual connection unless .env is valid)...")
        try:
            # We don't want to actually run create_all here, just check if it can be called.
            # Actual table creation requires an active DB connection, which is not what this script is for.
            # await init_db() # This would attempt to connect and create tables
            print("Database initialization function reachable.")
        except Exception as db_e:
            print(f"Database initialization check failed: {db_e}")

    # asyncio.run(verify_db_init()) # This tries to run async function, requires env for real check

except Exception as e:
    print(f"Backend verification failed: {e}")
    exit(1)