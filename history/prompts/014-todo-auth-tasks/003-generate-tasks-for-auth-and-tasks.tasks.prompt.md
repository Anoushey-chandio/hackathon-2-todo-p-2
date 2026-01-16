---
id: "003"
title: "Generate Tasks for Auth and Tasks"
stage: "tasks"
date: "2026-01-15"
surface: "agent"
model: "gemini-2.0-flash-exp"
feature: "014-todo-auth-tasks"
branch: "014-todo-auth-tasks"
user: "user"
command: "/sp.tasks"
labels: ["tasks", "full-stack", "auth", "crud"]
links:
  spec: "specs/014-todo-auth-tasks/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/014-todo-auth-tasks/tasks.md"
tests: []
---

## Prompt

Generate an actionable, dependency-ordered tasks.md for the feature based on available design artifacts.
Context: Backend: protect /tasks endpoints with auth, implement tasks CRUD. Frontend: call API correctly, show tasks list, allow mark complete/incomplete. Ensure no unauthorized access, no redirect loops. Test signup, login, tasks operations end-to-end.

## Response snapshot

Generated `specs/014-todo-auth-tasks/tasks.md` with 33 tasks organized into 6 phases:
1.  **Setup**: Project init (Backend/Frontend).
2.  **Foundational**: Database (SQLModel/Alembic) & Security (JWT) setup.
3.  **US1 (Auth)**: User model, Auth API, Frontend Auth Pages & Middleware.
4.  **US2 (Tasks)**: Task model, CRUD API, Frontend Dashboard & Task Components.
5.  **US3 (Privacy)**: Permission checks & error handling.
6.  **Polish**: Final security checks & docs.

## Outcome

- ✅ Impact: Clear roadmap for implementation.
- 🧪 Tests: Included integration tasks for Auth and Isolation.
- 📁 Files: `specs/014-todo-auth-tasks/tasks.md`
- 🔁 Next prompts: `/sp.implement` to begin Phase 1.
- 🧠 Reflection: The task breakdown separates Auth and Data (Tasks) cleanly, allowing for incremental testing (login first, then data access).

## Evaluation notes (flywheel)

- Failure modes observed: None.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
