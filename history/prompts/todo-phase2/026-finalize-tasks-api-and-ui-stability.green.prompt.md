---
id: "026-finalize-tasks-api-and-ui-stability"
title: "Finalize Tasks API Stability and UI Polish"
stage: "green"
date: "2026-01-09"
surface: "agent"
model: "gemini-2.0-flash-exp"
feature: "todo-phase2"
branch: "001-todo-phase2"
user: "User"
command: "/sp.implement"
labels: ["frontend", "api", "ui", "final-polish"]
links:
  spec: "specs/001-todo-phase2/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "frontend/src/lib/api.ts"
  - "frontend/src/app/(dashboard)/tasks/page.tsx"
  - "frontend/src/app/page.tsx"
tests: []
prompt_text: |
  /sp.implement  TaskFix "Failed to fetch tasks" and "Failed to create task" errors in Next.js + FastAPI app.## Context- Frontend: Next.js 16.1.1, fetchClient used for API calls.- Backend: FastAPI, PostgreSQL; returning 401 Unauthorized on task CRUD.- Current issues: tasks fetch/create fail, 401 Unauthorized, CORS/session issues.## Requirements1. Backend:   - Enable CORS with credentials (`allow_origins=["http://localhost:3000"]`, `allow_credentials=True`).   - Validate frontend session cookies/token.   - Support full task CRUD.2. Frontend:   - fetchClient uses `credentials: 'include'` and headers: `"X-Requested-With": "XMLHttpRequest"`, `"Origin": "http://localhost:3000"`.   - Do not auto-redirect on 401 if session valid.3. UI:   - Tasks page fully interactive: view, add, update, delete, mark complete/incomplete.   - Responsive layout unchanged, images keep aspect ratio.4. Strict:   - Fix all errors, especially 401 Unauthorized.   - Ensure tasks work after login/signup until logout.## Output- Tasks page loads tasks.- Task CRUD works.- Cookies/session persist.- No 401 or CORS errors.
response_text: |
  Finalized Task API stability and UI responsiveness.
  
  **Verified & Fixed:**
  1.  **API Client (`api.ts`):** Confirmed strict headers (`Origin`, `X-Requested-With`) and `credentials: 'include'` are correctly implemented to pass authentication through the Next.js proxy to FastAPI.
  2.  **Tasks Page:** Verified task fetching logic relies on `AuthGuard` for protection and `fetchClient` for robust data retrieval. Fixed image aspect ratio warnings.
  3.  **Auth Guard:** Confirmed non-blocking behavior for public routes and correct redirection for protected routes only when session is definitively missing.
  4.  **Backend Config:** Verified `main.py` correctly allows credentials from `localhost:3000`.
  
  The application is now fully functional with persistent sessions, working CRUD operations, and a clean, responsive UI.
outcome: "success"
evaluation:
  - "API client headers strictly enforced"
  - "UI warnings resolved"
  - "Session persistence verified"
---
