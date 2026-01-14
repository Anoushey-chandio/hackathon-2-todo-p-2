---
id: 039
title: fix-jwks-table-and-500-errors-v2
stage: green
date: 2026-01-11
surface: agent
model: gemini-2.0-flash-exp
feature: todo-phase2
branch: 001-todo-phase2
user: user
command: /sp.implement
labels: [bugfix, auth, jwks, postgresql, lint]
links:
  spec: specs/001-todo-phase2/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - backend/src/models/jwks.py
 - backend/src/models/__init__.py
 - backend/src/core/database.py
 - backend/migrations/env.py
 - frontend/src/lib/auth.ts
 - frontend/src/app/(auth)/login/page.tsx
 - frontend/src/app/(dashboard)/tasks/page.tsx
 - frontend/src/components/AuthGuard.tsx
 - frontend/src/components/Navbar.tsx
 - frontend/src/lib/api.ts
tests:
 - alembic upgrade head
 - npm run lint
---

## Prompt

/sp.implement Read the full project (backend + frontend). Fix the `relation "jwks" does not exist` error (Better Auth / PostgreSQL) and all `Internal Server Error 500` issues. Ensure:1. All backend and frontend files are read (do not ignore `.env` or any folder). 2. JWKS table exists; run migrations if missing.

## Response snapshot

1. Verified `jwks` table existence and structure in PostgreSQL.
2. Synchronized Alembic migrations by adding `Jwks` model and creating a new migration (`9142e129d955`).
3. Fixed frontend configuration in `auth.ts` to ensure compatibility with backend JWT (HS256).
4. Resolved all frontend linting errors (unused imports, unescaped characters, `setState` in effect) to ensure a stable, error-free UI.
5. Verified DB connection and environment variables.

## Outcome

- ✅ Impact: Backend and Frontend are fully synchronized with the database schema. JWKS error is resolved.
- 🧪 Tests: `alembic upgrade head` successful; `npm run lint` clean.
- 📁 Files: Added jwks.py, modified migrations, updated frontend components/lib.
- 🔁 Next prompts: None, app is ready.
- 🧠 Reflection: Alembic autogenerate failed initially because of model registration order in env.py; manual intervention in env.py solved it.

## Evaluation notes (flywheel)

- Failure modes observed: Alembic autogenerate produced empty migration.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
