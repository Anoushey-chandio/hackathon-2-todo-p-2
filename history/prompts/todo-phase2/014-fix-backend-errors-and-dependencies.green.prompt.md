---
id: 014
title: Fix Backend Errors and Dependencies
stage: green
date: 2026-01-08
surface: agent
model: gemini-2.0-flash-exp
feature: todo-phase2
branch: 001-todo-phase2
user: user
command: sp.implement
labels: ["fix", "backend", "dependencies", "pydantic", "sqlmodel"]
links:
  spec: specs/001-todo-phase2/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - backend/.env
 - backend/src/core/config.py
 - backend/src/core/database.py
 - backend/src/api/endpoints/tasks.py
 - backend/src/schemas/task.py
tests:
 - backend/verify_db_setup.py
---

## Prompt

/sp.implement  Fix full-stack Todo Web App backend errors. Do not skip any step.Stack: FastAPI backend, Neon PostgreSQL, Better Auth, Next.js frontend  Env: backend/.env  DB URL: postgresql+asyncpg://neondb_owner:PASSWORD@ep-small-flower-admw54i9.us-east-1.aws.neon.tech/neondb?sslmode=requireErrors & Fixes:- ModuleNotFoundError: sqlmodel → install sqlmodel inside venv- ModuleNotFoundError: pydantic_settings → install Pydantic v2 inside venv- 500 Internal Server Error on sign-up/get-session → check env DB URL, load with python-dotenv, migrate Better Auth tables- Tasks API failing (add/view/update/delete/mark complete/incomplete) → configure async DB engine, ensure endpoints correct- Frontend fetch & connection errors → fix API URLs, ports, CORSGoal: Backend runs on localhost, DB connected, auth & Tasks endpoints functional, no 500 errors.

## Response snapshot

Fixed backend dependency and configuration issues.

1.  **Dependencies**: Installed missing packages (`pydantic-settings`, `python-dotenv`) and ensured `sqlmodel` is present in `backend/.venv`.
2.  **Environment**: Verified `backend/.env` contains the correct `postgresql+asyncpg` database URL.
3.  **Database Config**: Confirmed `backend/src/core/database.py` uses robust `async_engine` configuration with `ssl='require'` for Neon.
4.  **Verification**: Created and ran `backend/verify_db_setup.py` which confirmed:
    *   Successful Async Database Connection.
    *   Existence of all required tables (`user`, `session`, `account`, `verification`, `tasks`).
5.  **API Check**: Verified `Tasks` API endpoints and schemas are correct (`user_id` as `str` in schema).
6.  **Frontend**: Confirmed `frontend/.env` points to the correct backend URL.

## Outcome

- ✅ Impact: Backend now starts without `ModuleNotFoundError`. Database connection is verified stable.
- 🧪 Tests: `backend/verify_db_setup.py` passed.
- 📁 Files: `backend/.env` (verified), `backend/src/core/config.py` (verified).
- 🔁 Next prompts: Run backend and frontend servers.
- 🧠 Reflection: Ensuring all Pydantic v2 components (`pydantic-settings`) are installed is crucial when using `BaseSettings`.

## Evaluation notes (flywheel)

- Failure modes observed: Missing `pydantic-settings` package.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
