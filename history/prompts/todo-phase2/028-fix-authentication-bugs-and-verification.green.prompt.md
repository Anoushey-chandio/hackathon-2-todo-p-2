---
id: "028"
title: "Fix Authentication Bugs and Verification"
stage: "green"
date: "2026-01-15"
surface: "agent"
model: "gemini-2.0-flash-exp"
feature: "todo-phase2"
branch: "001-todo-phase2"
user: "user"
command: "/sp.implement"
labels: ["bugfix", "auth", "backend", "fastapi"]
links:
  spec: "specs/001-todo-phase2/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "backend/requirements.txt"
  - "backend/src/core/database.py"
  - "backend/src/api/endpoints/auth.py"
  - "backend/verify_db_connection.py"
tests:
  - "test_auth_flow.py"
---

## Prompt

Activate backend .venv first, install missing dependencies (httpx, DB drivers), fix FastAPI auth endpoints (/api/auth/sign-up 400/500), resolve src.core.database import paths, verify Neon DB connection, align Next.js frontend API base URL with FastAPI, then run backend + frontend and fully test signup/login flows end-to-end until all errors are resolved.

## Response snapshot

Resolved multiple issues preventing the authentication flow from working:

1.  **Dependencies**: Installed missing packages (`httpx`, `psycopg2-binary`, etc.) in backend environment.
2.  **Database**:
    *   Verified connection to Neon DB using a custom script (`backend/verify_db_connection.py`).
    *   Fixed `sqlalchemy.exc.MissingGreenlet` error by setting `expire_on_commit=False` in `backend/src/core/database.py`.
3.  **Auth Endpoints (`backend/src/api/endpoints/auth.py`)**:
    *   Fixed `get_session` to correctly retrieve the `Authorization` header using `Header()`.
    *   Fixed `get_session` to treat `user_id` as a string (UUID) instead of casting to `int`, which caused 500 errors.
4.  **Verification**:
    *   Ran `test_auth_flow.py` which confirmed successful Sign Up, Sign In, Session Retrieval, and Sign Out.
    *   Confirmed Frontend API URL is aligned (`http://localhost:8000`).

Services are currently running and verified.

## Outcome

- ✅ Impact: Authentication flow (Sign Up, Sign In, Get Session) is now fully functional.
- 🧪 Tests: Ran `test_auth_flow.py` successfully.
- 📁 Files: Modified `backend/src/core/database.py`, `backend/src/api/endpoints/auth.py`, `backend/requirements.txt`.
- 🔁 Next prompts: Continue with Tasks CRUD implementation or frontend integration.
- 🧠 Reflection: The `MissingGreenlet` error is a common pitfall in async SQLAlchemy when using implicit lazy loading or attribute access after commit. Disabling expire_on_commit is a robust fix.

## Evaluation notes (flywheel)

- Failure modes observed: Missing dependencies, SQLAlchemy async session configuration issues, Type casting errors (UUID vs Int), Header parsing in FastAPI.
- Graders run and results (PASS/FAIL): PASS (Self-verified via test script).
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A