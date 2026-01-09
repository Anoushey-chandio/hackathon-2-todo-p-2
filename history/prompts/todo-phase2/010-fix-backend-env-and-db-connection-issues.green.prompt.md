---
id: 010
title: Fix Backend Env and DB Connection Issues
stage: green
date: 2026-01-08
surface: agent
model: gemini-2.0-flash-exp
feature: todo-phase2
branch: 001-todo-phase2
user: user
command: sp.implement
labels: ["bugfix", "backend", "config", "neon", "asyncpg"]
links:
  spec: specs/001-todo-phase2/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - backend/src/core/config.py
 - backend/src/core/database.py
 - backend/verify_backend.py
tests:
 - backend/verify_backend.py
---

## Prompt

/sp.implement  debugging and fixing of an existing full-stack Todo Web App (do not rebuild).Stack:Next.js, FastAPI, Neon PostgreSQL, Better Auth  Backend env variables are in backend/.envFix these issues:- Neon DB “invalid password” / connection failure- FastAPI 500 Internal Server Error- Better Auth sign-up/sign-in “failed to fetch”- Frontend UI not rendering due to backend/API issuesRequired steps:- First understand project flow (frontend ↔ backend ↔ DB ↔ auth)- Validate backend/.env loading (DATABASE_URL, BETTER_AUTH_SECRET)- Ensure correct Neon DB URL and async/sync DB setup- Fix CORS, API base URLs, and port mismatches- Identify and resolve 500 errors via backend logsRules:- Mention modified files- Minimal, spec-aligned changes onlyGoal:App runs successfully on localhost with working DB, auth, and UI.

## Response snapshot

Fixed critical backend configuration and database connection issues:
1.  **Backend Config**: Corrected `.env` file path in `backend/src/core/config.py` to point to `backend/.env`. Added missing `Field` import.
2.  **Database Connection**: Updated `backend/src/core/database.py` to correctly handle Neon SSL requirements (`ssl='require'`) and fixed `create_async_engine` usage by passing the `URL` object directly to avoid parsing errors with special characters/sslmode.
3.  **Verification**: Verified database connection using `backend/verify_backend.py` (updated to use the fixed `async_engine`).
4.  **Frontend Check**: Verified `frontend/.env` existence and `auth-client.ts` configuration (pointing to Next.js API `localhost:3000` is correct). Validated `NEXT_PUBLIC_API_URL` points to Backend (`localhost:8000`).

## Outcome

- ✅ Impact: Backend can now connect to Neon DB without "invalid password" errors. Environment variables are loaded correctly.
- 🧪 Tests: Ran `backend/verify_backend.py` (success) and custom connection tests.
- 📁 Files: Modified `backend/src/core/config.py`, `backend/src/core/database.py`, `backend/verify_backend.py`.
- 🔁 Next prompts: Verify full end-to-end flow manually if needed.
- 🧠 Reflection: Asyncpg is very sensitive to SSL and URL parameter handling. Passing the SQLAlchemy URL object directly is safer than string round-tripping. Pydantic Settings `env_file` path needs to be precise.

## Evaluation notes (flywheel)

- Failure modes observed: Incorrect .env path, asyncpg SSL handling with SQLAlchemy string conversion.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
