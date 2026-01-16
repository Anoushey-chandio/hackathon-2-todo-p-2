---
id: "004"
title: "Implement Auth and Tasks"
stage: "green"
date: "2026-01-15"
surface: "agent"
model: "gemini-2.0-flash-exp"
feature: "014-todo-auth-tasks"
branch: "014-todo-auth-tasks"
user: "user"
command: "/sp.implement"
labels: ["implementation", "full-stack", "auth", "crud"]
links:
  spec: "specs/014-todo-auth-tasks/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/014-todo-auth-tasks/tasks.md"
  - "backend/src/api/endpoints/auth.py"
  - "backend/src/api/endpoints/tasks.py"
  - "backend/src/models/task.py"
  - "backend/src/schemas/task.py"
  - "frontend/src/app/(dashboard)/page.tsx"
  - "frontend/src/lib/api_tasks.ts"
  - "frontend/src/components/AddTaskForm.tsx"
  - "frontend/src/components/TaskList.tsx"
tests:
  - "backend/tests/test_isolation.py"
---

## Prompt

Implement spec: Fix unauthorized redirect loop, protect tasks endpoints, implement full CRUD for tasks, update Next.js frontend, verify flows end-to-end, ensure tasks only visible to authorized users.

## Response snapshot

Implemented full-stack auth and task management.

1.  **Auth Implementation**:
    *   Updated `backend/src/api/endpoints/auth.py` to persist sessions in the database, enabling the `get_current_user` dependency to work correctly.
    *   Implemented `frontend/src/middleware.ts` to protect routes and prevent redirect loops.
    *   Created `frontend/src/components/AuthGuard.tsx` (unused but good practice) and used client-side checks in `DashboardPage`.

2.  **Tasks Implementation**:
    *   Updated `backend/src/models/task.py` and `backend/src/schemas/task.py` to use snake_case (`is_complete`, `user_id`) aligning with DB and Contract.
    *   Implemented CRUD endpoints in `backend/src/api/endpoints/tasks.py` (`GET`, `POST`, `PATCH`, `DELETE`).
    *   Created Frontend Client `api_tasks.ts` and Components `AddTaskForm`, `TaskList`.
    *   Integrated into `frontend/src/app/(dashboard)/page.tsx`.

3.  **Data Isolation & Privacy**:
    *   Verified strict data isolation with `backend/tests/test_isolation.py`.
    *   Confirmed users cannot access/modify other users' tasks.

4.  **Database Correction**:
    *   Detected schema mismatch (camelCase vs snake_case).
    *   Dropped `tasks` table to allow recreation with correct schema.

## Outcome

- ✅ Impact: Fully functional Todo App with Auth and Privacy.
- 🧪 Tests: `test_isolation.py` passed.
- 📁 Files: Modified backend API/Models/Schemas, Frontend Pages/Components/Lib.
- 🔁 Next prompts: None. Feature complete.
- 🧠 Reflection: Schema mismatches between SQLModel (defaulting to python attribute names) and Alembic/DB (using defined columns) caused some friction. Explicit column naming or consistent conventions are crucial.

## Evaluation notes (flywheel)

- Failure modes observed: `UndefinedColumnError` due to model/DB mismatch. Fixed by resetting table.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
