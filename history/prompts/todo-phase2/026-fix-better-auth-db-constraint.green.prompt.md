---
id: 026
title: fix-better-auth-db-constraint
stage: green
date: 2026-01-13
surface: agent
model: gemini-2.0-flash-exp
feature: todo-phase2
branch: 001-todo-phase2
user: local-user
command: /sp.implement
labels: ["bugfix", "db", "auth", "migration"]
links:
  spec: specs/001-todo-phase2/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - backend/migrations/versions/9142e129d955_add_jwks_table.py
tests:
 - curl http://localhost:3000/api/auth/get-session (Pass)
---

## Prompt

/sp.implement reslove these error No assumptions. No hallucination. Do not declare success without localhost proof

## Response snapshot

Resolved `500 Internal Server Error` on `/api/auth/get-session`. The root cause was `Better Auth` (running in Next.js) trying to insert into the `jwks` table without an `updatedAt` value, violating a Not-Null constraint. Fixed by modifying the Alembic migration to add `server_default=sa.text('now()')` to `createdAt` and `updatedAt` columns and recreating the table. Verified `get-session` returns `200 OK`.

## Outcome

- ✅ Impact: Authentication system is now functional. Better Auth can initialize and manage keys.
- 🧪 Tests: `curl -v http://localhost:3000/api/auth/get-session` -> 200 OK.
- 📁 Files: Modified `backend/migrations/versions/9142e129d955_add_jwks_table.py`.
- 🔁 Next prompts: Continue frontend integration or polish UI.
- 🧠 Reflection: The error log explicitly pointed to the DB constraint. Fixing the schema to support the library's behavior (which expects DB defaults) was the correct solution.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): default
- Next experiment (smallest change to try): none
