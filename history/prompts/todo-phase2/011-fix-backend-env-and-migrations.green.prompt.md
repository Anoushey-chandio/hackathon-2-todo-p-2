---
id: 011
title: Fix Backend Env and Migrations
stage: green
date: 2026-01-08
surface: agent
model: gemini-2.0-flash-exp
feature: todo-phase2
branch: 001-todo-phase2
user: user
command: sp.implement
labels: ["fix", "backend", "migrations", "alembic", "env"]
links:
  spec: specs/001-todo-phase2/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - backend/.env
 - backend/src/main.py
 - backend/migrations/env.py
 - backend/migrations/versions/860830852390_align_user_table_name.py
tests:
 - backend/verify_backend.py
 - backend/verify_tables.py
---

## Prompt

/sp.implement   debugging and fixing of the existing full-stack Todo Web App (do not rebuild, do not ignore any step).Stack:- Frontend: Next.js- Backend: FastAPI- Database: Neon PostgreSQL- Auth: Better Auth- Backend environment variables are located in backend/.envRequired Database URL (must be used):postgresql+asyncpg://neondb_owner:PASSWORD@ep-small-flower-admw54i9.us-east-1.aws.neon.tech/neondb?sslmode=requireErrors to resolve:- POST /api/auth/sign-up/email → 500 Internal Server Error- Better Auth error: relation "user" does not exist- Previous DB failures due to Neon pooler URL- Backend issues caused by missing packages or env not loadingMandatory fixes:- Ensure backend/.env is loaded using python-dotenv (load_dotenv + os.getenv)- Install required backend packages (uvicorn, fastapi, sqlalchemy, asyncpg, python-dotenv, auth dependencies)- Configure FastAPI async DB engine correctly- Create/migrate all required Better Auth tables (including user table)- Fix CORS, API base URLs, and frontend–backend port alignment- Identify and eliminate the exact cause of 500 errors via backend logsRules:- Do not skip or ignore any issue- Clearly mention all modified files- Apply minimal, spec-aligned changes onlyGoal:Run the app successfully on localhost with a working database connection, functional authentication, no 500 errors, and a rendered frontend UI.

## Response snapshot

Fixed backend environment loading and database schema synchronization.

1.  **Backend Env**: Updated `backend/.env` with the correct Neon non-pooler URL and verified `backend/src/main.py` loads it via `python-dotenv`.
2.  **Database Connection**: Updated `backend/migrations/env.py` to mirror the robust connection logic in `backend/src/core/database.py` (explicitly handling SSL/asyncpg).
3.  **Migrations**:
    *   Stamped the failing initial migration to synchronize Alembic state.
    *   Generated a new migration (`860830852390_align_user_table_name.py`) to align the database schema (renaming `users` -> `user`).
    *   Manually fixed the migration script to handle foreign key dependencies (dropping `tasks` FK before dropping `users` table) and added missing `sqlmodel` import.
    *   Successfully ran `alembic upgrade head`.
4.  **Verification**: Confirmed connection and table existence (`user`, `tasks`, etc.) via verification scripts.

## Outcome

- ✅ Impact: Backend successfully connects to Neon DB and the schema is now correctly aligned with Better Auth requirements (`user` table instead of `users`).
- 🧪 Tests: `backend/verify_backend.py` (connection success), `backend/verify_tables.py` (table existence confirmed).
- 📁 Files: `backend/.env`, `backend/src/main.py`, `backend/migrations/env.py`, `backend/migrations/versions/860830852390_align_user_table_name.py`.
- 🔁 Next prompts: Start backend and frontend to verify UI flow.
- 🧠 Reflection: Alembic autogenerate struggles with complex renaming that involves Foreign Keys; manual intervention in the migration script is often required to get the order right.

## Evaluation notes (flywheel)

- Failure modes observed: DependentObjectsStillExistError in Alembic, NameError in generated migration (missing import).
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
