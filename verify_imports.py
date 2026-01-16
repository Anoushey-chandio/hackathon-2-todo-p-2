#!/usr/bin/env python3
"""Quick verification that all imports work correctly."""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

print("=" * 60)
print("BACKEND VERIFICATION TEST")
print("=" * 60)

# Test imports
tests = [
    ("FastAPI App", lambda: __import__("src.main").main.app),
    ("User Model", lambda: __import__("src.models.user").models.user.User),
    ("Task Model", lambda: __import__("src.models.task").models.task.Task),
    ("User Schemas", lambda: __import__("src.schemas.user").schemas.user.UserCreate),
    ("Task Schemas", lambda: __import__("src.schemas.task").schemas.task.TaskCreate),
    ("API Router", lambda: __import__("src.api.api").api.api.api_router),
    ("Security Utils", lambda: __import__("src.core.security").core.security.verify_password),
    ("Database Config", lambda: __import__("src.core.database").core.database.init_db),
]

passed = 0
failed = 0

for test_name, test_func in tests:
    try:
        test_func()
        print(f"✓ {test_name}")
        passed += 1
    except Exception as e:
        print(f"✗ {test_name}: {e}")
        failed += 1

print("=" * 60)
print(f"Results: {passed} passed, {failed} failed")
print("=" * 60)

if failed == 0:
    print("\n✓ All backend components verified successfully!")
    sys.exit(0)
else:
    print(f"\n✗ {failed} component(s) failed verification")
    sys.exit(1)
