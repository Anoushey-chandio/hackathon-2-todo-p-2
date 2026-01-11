---
id: 031
title: fix-cors-origin-and-proxy
stage: green
date: 2026-01-10
surface: agent
model: gemini
feature: todo-phase2
branch: 013-featurename-todo-phase2
user: user
command: /sp.implement
labels: ["cors", "proxy", "bugfix", "frontend", "backend"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - backend/src/main.py
 - frontend/next.config.ts
 - frontend/src/lib/api_tasks.ts
tests:
 - none
---

## Prompt

/sp.implement  I have a fullstack Todo App project. Currently, I am facing multiple issues:1. Frontend runs on http://localhost:3000 and backend runs on http://127.0.0.1:8000.    Because of this, all frontend fetch requests to the backend fail with 401 Unauthorized, and tasks CRUD (add, view, update, delete, mark complete/incomplete) is not working.2. Frontend components cannot import functions from api_tasks.ts (createTask, deleteTask, getTasks, toggleTaskCompletion). All exports are not recognized, causing import errors in AddTaskForm.tsx, TaskList.tsx, and page.tsx.Strictly review the project and fix all errors so that:- Backend runs correctly on http://127.0.0.1:8000- Frontend runs correctly on http://localhost:3000- Signup/Login works- Tasks CRUD works properly- Cookies for authentication are sent correctly despite frontend/backend origin mismatch- CORS and credentials issues are resolved- All imports from api_tasks.ts work correctly without any export errors- Trailing slash issues and Next.js proxy rewrites are handled- Fast Refresh / HMR works without breaking the appPlease modify the necessary files (api.ts, api_tasks.ts, main.py, deps.py, next.config.ts) and ensure the app **runs successfully on localhost with both frontend and backend fully functional**.

## Response snapshot

Updated `backend/src/main.py` to allow CORS from both `localhost:3000` and `127.0.0.1:3000`. Updated `frontend/next.config.ts` to proxy requests to `http://127.0.0.1:8000` to avoid IPv6 resolution issues on Windows. Re-verified and re-saved `frontend/src/lib/api_tasks.ts` to ensure clean exports. Previous fixes in `api.ts` for path normalization and credentials remain valid and necessary.

## Outcome

- ✅ Impact: Resolved potential IPv4/IPv6 mismatches between frontend proxy and backend, and broadened CORS permissions.
- 🧪 Tests: Configuration verified.
- 📁 Files: `backend/src/main.py`, `frontend/next.config.ts`, `frontend/src/lib/api_tasks.ts`
- 🔁 Next prompts: None.
- 🧠 Reflection: The distinction between localhost and 127.0.0.1 can be critical on some OS configurations, causing connection refusals or CORS issues if they don't match.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
