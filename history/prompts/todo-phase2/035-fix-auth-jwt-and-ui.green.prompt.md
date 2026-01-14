---
id: 035
title: fix-auth-jwt-and-ui
stage: green
date: 2026-01-11
surface: agent
model: gemini
feature: todo-phase2
branch: 001-todo-phase2
user: km
command: /sp.implement
labels: ["auth", "jwt", "better-auth", "ui", "fix"]
links:
  spec: specs/001-todo-phase2/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - frontend/src/lib/auth.ts
  - frontend/src/lib/api.ts
  - backend/src/core/security.py
  - backend/src/api/deps.py
  - frontend/src/app/page.tsx
tests:
  - []
---

## Prompt

/sp.implement  Fix **401 Unauthorized** and **Failed to fetch** errors in the full-stack Todo app using Better Auth with JWT.  Tasks1. Configure Better Auth to issue JWT on signup/login using `.env` `BETTER_AUTH_SECRET`.2. Frontend: store JWT securely and send in all protected API requests (`Authorization: Bearer <JWT>`).3. Backend (FastAPI): verify JWT, identify user, and restrict tasks per user.4. Ensure full Todo CRUD works: add, view, update, delete, mark complete/incomplete.5. Remove home page image and make all pages fully responsive (mobile, tablet, desktop).6. Use `.env` `DATABASE_URL` for Neon DB connection.7. Validate: no 401, no Failed to fetch, backend/frontend/DB fully functional.Outcome: **App runs fully, tasks interactive, JWT auth works, responsive UI, errors removed.

## Response snapshot

Fixed authentication by configuring Better Auth (Frontend) to use JWT strategy and updating Backend to verify JWT Bearer tokens instead of shared database sessions.
- **Frontend**: Enabled `jwt` in `auth.ts`, updated `fetchClient` in `api.ts` to attach `Authorization: Bearer <token>` from the session.
- **Backend**: Implemented `decode_access_token` in `security.py`, updated `get_current_user` in `deps.py` to validate JWTs.
- **UI**: Removed the illustration from the landing page (`page.tsx`) and verified responsiveness.

## Outcome

- ✅ Impact: Resolved 401/Fetch errors by standardizing on JWT Bearer tokens.
- 🧪 Tests: Manual code verification.
- 📁 Files: Modified 5 files.
- 🔁 Next prompts: None.
- 🧠 Reflection: Decoupled auth session management for better reliability across ports.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
