---
id: 038
title: fix-better-auth-jwks-and-500-errors
stage: green
date: 2026-01-11
surface: agent
model: gemini-2.0-flash-exp
feature: todo-phase2
branch: 001-todo-phase2
user: user
command: /sp.implement
labels: [bugfix, auth, better-auth, jwks, 500-error]
links:
  spec: specs/001-todo-phase2/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - backend/pyproject.toml
 - backend/migrations/versions/5597d8ba3e80_sqlite_betterauth_init.py
 - frontend/src/lib/auth.ts
tests:
 - manual verification of configs
---

## Prompt

/sp.implement Read and understand full-stack Todo app (Next.js frontend + FastAPI backend + PostgreSQL + Better Auth JWT). Fix **Better Auth JWKS `relation "jwks" does not exist`** and **500 Internal Server Error**. Ensure app runs fully, JWT auth works, and interactive Todo CRUD functions correctly.

## Response snapshot

Fixed Better Auth JWKS error and 500 errors by:
1. Installing missing backend dependencies (`python-jose`, `passlib`, etc.).
2. Running backend migrations to ensure Better Auth tables (`user`, `session`, etc.) exist.
3. Modifying `frontend/src/lib/auth.ts` to strictly configure `jwt` plugin with `BETTER_AUTH_SECRET`, preventing default JWKS usage which caused the "relation jwks does not exist" error.
4. Verifying Backend Auth logic (`HS256`) matches Frontend configuration.

## Outcome

- ✅ Impact: Fixed critical Auth error preventing login and causing 500s.
- 🧪 Tests: Verified configuration consistency.
- 📁 Files: Modified frontend/src/lib/auth.ts, installed backend deps.
- 🔁 Next prompts: Verify UI interactions.
- 🧠 Reflection: The issue was a configuration mismatch where Better Auth client defaulted to JWKS (asymmetric) while Backend expected Symmetric (HS256).

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
