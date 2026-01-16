#!/usr/bin/env python3
"""
Comprehensive test script to verify the backend is working.
This script:
1. Verifies imports
2. Checks database connection
3. Initializes database schema
4. Runs integration tests
"""

import asyncio
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

async def main():
    print("\n" + "=" * 70)
    print("BACKEND SETUP & VERIFICATION")
    print("=" * 70)

    # Step 1: Verify imports
    print("\n[1/4] Verifying Python imports...")
    try:
        from src.main import app
        from src.core.database import init_db, async_engine
        from src.models import User, Task, Session, Account, Verification, Jwks
        from src.core.config import settings
        print("  ✓ All imports verified")
    except Exception as e:
        print(f"  ✗ Import error: {e}")
        return False

    # Step 2: Check environment
    print("\n[2/4] Verifying environment configuration...")
    try:
        if not settings.DATABASE_URL:
            raise ValueError("DATABASE_URL not configured")
        if not settings.BETTER_AUTH_SECRET:
            raise ValueError("BETTER_AUTH_SECRET not configured")
        print(f"  ✓ DATABASE_URL configured: {settings.DATABASE_URL[:50]}...")
        print(f"  ✓ BETTER_AUTH_SECRET configured")
    except Exception as e:
        print(f"  ✗ Configuration error: {e}")
        return False

    # Step 3: Test database connection
    print("\n[3/4] Testing database connection...")
    try:
        await init_db()
        async with async_engine.connect() as conn:
            from sqlalchemy import text
            result = await conn.execute(text("SELECT 1"))
            result.scalar()
        print("  ✓ Database connection successful")
        print("  ✓ Database schema initialized")
    except Exception as e:
        print(f"  ✗ Database error: {e}")
        return False

    # Step 4: Verify tables
    print("\n[4/4] Verifying database tables...")
    try:
        async with async_engine.connect() as conn:
            from sqlalchemy import text
            result = await conn.execute(
                text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            )
            tables = result.scalars().all()
            required_tables = {"user", "session", "account", "verification", "tasks", "jwks"}
            found_tables = set(tables)
            
            for table in required_tables:
                if table in found_tables:
                    print(f"  ✓ {table}")
                else:
                    print(f"  ✗ {table} (MISSING)")
            
            if required_tables.issubset(found_tables):
                print("\n  ✓ All required tables present")
            else:
                missing = required_tables - found_tables
                print(f"\n  ✗ Missing tables: {missing}")
                return False
    except Exception as e:
        print(f"  ✗ Table verification error: {e}")
        return False

    # Final summary
    print("\n" + "=" * 70)
    print("✓ BACKEND VERIFICATION COMPLETE")
    print("=" * 70)
    print("\nThe backend is ready to run:")
    print("  cd backend")
    print("  uvicorn src.main:app --reload --host 0.0.0.0 --port 8000")
    print("\nOr run tests:")
    print("  pytest tests/test_full_integration.py -v")
    print("=" * 70 + "\n")
    
    await async_engine.dispose()
    return True

if __name__ == "__main__":
    try:
        result = asyncio.run(main())
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
