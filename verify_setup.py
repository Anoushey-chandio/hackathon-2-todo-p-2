#!/usr/bin/env python3
"""
Comprehensive verification script for Todo App setup
Checks all components and provides detailed status report
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Tuple, List

class Verification:
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
        self.root_dir = Path(__file__).parent
        
    def check(self, name: str, condition: bool, details: str = "") -> None:
        """Record a check result"""
        status = "✅ PASS" if condition else "❌ FAIL"
        self.results.append(f"{status} - {name}")
        if details:
            self.results.append(f"    └─ {details}")
        
        if condition:
            self.passed += 1
        else:
            self.failed += 1
    
    def section(self, title: str) -> None:
        """Print a section header"""
        self.results.append("")
        self.results.append(f"{'='*60}")
        self.results.append(f"  {title}")
        self.results.append(f"{'='*60}")
    
    def print_results(self) -> None:
        """Print all results"""
        for result in self.results:
            print(result)
        
        print("")
        print("="*60)
        print(f"SUMMARY: {self.passed} passed, {self.failed} failed")
        print("="*60)
        
        if self.failed == 0:
            print("\n🎉 All checks passed! Todo App is ready to run.")
        else:
            print(f"\n⚠️  {self.failed} check(s) failed. See details above.")
        
        sys.exit(0 if self.failed == 0 else 1)

def main():
    v = Verification()
    
    # System checks
    v.section("SYSTEM REQUIREMENTS")
    
    # Python
    python_version = sys.version_info
    v.check(
        "Python version",
        python_version.major >= 3 and python_version.minor >= 11,
        f"Python {python_version.major}.{python_version.minor}.{python_version.micro}"
    )
    
    # Git
    try:
        subprocess.run(["git", "--version"], capture_output=True, timeout=5)
        v.check("Git installed", True)
    except:
        v.check("Git installed", False, "Optional but recommended")
    
    # Project structure
    v.section("PROJECT STRUCTURE")
    
    backend_dir = v.root_dir / "backend"
    frontend_dir = v.root_dir / "frontend"
    
    v.check("Backend directory exists", backend_dir.exists(), str(backend_dir))
    v.check("Frontend directory exists", frontend_dir.exists(), str(frontend_dir))
    
    # Backend files
    v.section("BACKEND FILES")
    
    backend_files = [
        "src/main.py",
        "src/api/api.py",
        "src/api/endpoints/auth.py",
        "src/core/database.py",
        "src/core/config.py",
        "src/models/user.py",
        "src/lib/auth_better.py",
        "requirements.txt",
    ]
    
    for file in backend_files:
        file_path = backend_dir / file
        v.check(f"Backend {file}", file_path.exists())
    
    # Frontend files
    v.section("FRONTEND FILES")
    
    frontend_files = [
        "src/app/layout.tsx",
        "src/app/page.tsx",
        "src/app/(auth)/signup/page.tsx",
        "src/app/(auth)/login/page.tsx",
        "src/lib/auth-client.ts",
        "package.json",
        "next.config.ts",
    ]
    
    for file in frontend_files:
        file_path = frontend_dir / file
        v.check(f"Frontend {file}", file_path.exists())
    
    # Root documentation
    v.section("DOCUMENTATION")
    
    docs = [
        "README.md",
        "SETUP_GUIDE.md",
        "TESTING_GUIDE.md",
        "GETTING_STARTED.md",
        "TEST_INTEGRATION.md",
        "IMPLEMENTATION_COMPLETE.md",
    ]
    
    for doc in docs:
        doc_path = v.root_dir / doc
        v.check(f"Documentation: {doc}", doc_path.exists())
    
    # Test files
    v.section("TEST FILES")
    
    test_files = [
        "run_quick_tests.py",
        "TEST_INTEGRATION.md",
    ]
    
    for test_file in test_files:
        test_path = v.root_dir / test_file
        v.check(f"Test file: {test_file}", test_path.exists())
    
    # Startup scripts
    v.section("STARTUP SCRIPTS")
    
    startup_files = [
        "START_APP.bat",
        "start_app.sh",
    ]
    
    for startup in startup_files:
        startup_path = v.root_dir / startup
        v.check(f"Startup script: {startup}", startup_path.exists())
    
    # Configuration files
    v.section("CONFIGURATION FILES")
    
    backend_env = backend_dir / ".env"
    v.check(".env file exists", backend_env.exists(), str(backend_env))
    
    if backend_env.exists():
        with open(backend_env) as f:
            env_content = f.read()
            v.check("DATABASE_URL configured", "DATABASE_URL=" in env_content)
            v.check("BETTER_AUTH_SECRET configured", "BETTER_AUTH_SECRET=" in env_content)
    
    # Dependencies
    v.section("PYTHON DEPENDENCIES")
    
    # Check key packages
    key_packages = [
        ("fastapi", "FastAPI"),
        ("sqlalchemy", "SQLAlchemy"),
        ("asyncpg", "asyncpg"),
        ("pydantic", "Pydantic"),
        ("uvicorn", "Uvicorn"),
        ("jwt", "PyJWT"),
        ("passlib", "passlib"),
    ]
    
    for package, name in key_packages:
        try:
            __import__(package)
            v.check(f"Python package: {name}", True)
        except ImportError:
            v.check(f"Python package: {name}", False, "Run: pip install -r backend/requirements.txt")
    
    # Database
    v.section("DATABASE")
    
    # Try to import database module
    try:
        sys.path.insert(0, str(backend_dir))
        from src.core.database import DATABASE_URL
        v.check("Database URL loaded", True)
        v.check("Database URL valid", "postgresql://" in DATABASE_URL)
    except Exception as e:
        v.check("Database configuration", False, str(e))
    
    # Summary
    v.section("FINAL STATUS")
    
    if v.failed == 0:
        v.check("All components", True, "Todo App is fully set up!")
        v.check("Ready to run", True, "Execute: python run_quick_tests.py")
        v.check("Next step", True, "Start servers using START_APP.bat or start_app.sh")
    else:
        v.check("Components status", False, f"{v.failed} issue(s) to resolve")
    
    v.print_results()

if __name__ == "__main__":
    main()
