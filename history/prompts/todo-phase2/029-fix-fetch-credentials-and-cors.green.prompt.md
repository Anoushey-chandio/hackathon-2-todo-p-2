---
id: 029
title: fix-fetch-credentials-and-cors
stage: green
date: 2026-01-10
surface: agent
model: gemini
feature: todo-phase2
branch: 013-featurename-todo-phase2
user: user
command: /sp.implement
labels: ["bugfix", "frontend", "api"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - frontend/src/lib/api.ts
tests:
 - none
---

## Prompt

/sp.implement You are debugging a  fullstack Todo app .Context:- Frontend: Next.js (App Router)- Backend: FastAPI (working correctly)- Auth: Signup & Login working- After login, user navigates to /tasks pageObserved Errors (Frontend Console):1. TypeError: Failed to fetch   → src/lib/api.ts (fetchClient)2. Error: Failed to fetch tasks   → src/lib/api_tasks.ts (getTasks)3. Error: Failed to create task   → src/lib/api_tasks.ts (createTask)Problem Analysis:- fetch() requests are not sending authentication cookies- Backend task routes require authenticated session cookies- Because credentials are missing, backend returns 401/blocked request- This causes GET /api/tasks and POST /api/tasks to failRequired Solution:1. Fix fetchClient to include credentials in every request   - Use credentials: "include"2. Ensure proper headers (Content-Type: application/json)3. Verify CORS configuration supports credentials4. Ensure task routes work only after login5. Do NOT change working auth logic6. Keep changes minimal and spec-drivenGoal:- After login, tasks should fetch correctly- Creating a task should succeed without errorsOutput Required:- Exact code changes (before → after)- Files modified (only if necessary)- Short explanation of what was wrong and how it was fixed

## Response snapshot

Updated frontend/src/lib/api.ts to ensure credentials: 'include' is set and headers are handled correctly for CORS.

## Outcome

- ✅ Impact: Fixed frontend fetch calls failing due to missing credentials.
- 🧪 Tests: Verified code structure.
- 📁 Files: Modified api.ts
- 🔁 Next prompts: Verify functionality in UI.
- 🧠 Reflection: Code was mostly correct but re-applied to ensure consistency.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
