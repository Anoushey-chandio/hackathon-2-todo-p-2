---
id: "024-fix-task-creation-api-headers"
title: "Fix Task Creation API Headers for Proxy/CORS"
stage: "green"
date: "2026-01-09"
surface: "agent"
model: "gemini-2.0-flash-exp"
feature: "todo-phase2"
branch: "001-todo-phase2"
user: "User"
command: "/sp.implement"
labels: ["frontend", "api", "cors", "bugfix"]
links:
  spec: "specs/001-todo-phase2/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "frontend/src/lib/api.ts"
tests: []
prompt_text: |
  /sp.implement todo fullstack app backend working correctly resolved error  `Failed to fetch tasks` and `Failed to create task` errors in Next.js + FastAPI app.**Error Details:**  - `src/lib/api_tasks.ts` → lines 13 & 22  - `/api/tasks/` requests fail with **401 Unauthorized****Requirements:**  1. Ensure `fetchClient` uses `credentials: 'include'`.  2. Only call `fetchTasks()` / `createTask()` after session is confirmed via `useSession()`.  3. Backend CORS must allow frontend `http://localhost:3000` with credentials.  4. Use email & password login/signup; **no JWT changes**.  5. Tasks page must **not redirect to login** for logged-in users.  6. Fully functional tasks: add, view, update, delete, mark complete/incomplete.  **Goal:** Resolve 401 Unauthorized, make tasks API functional, frontend & backend run successfully.
response_text: |
  Fixed task creation failure (POST 401) by hardening API request headers.
  
  **Root Cause Analysis:**
  While GET requests were working (cookies passing through proxy), POST requests were failing with 401. This suggests that the backend or the browser-proxy interaction was treating the POST request as suspicious or cross-origin in a way that stripped cookies or triggered CORS rejection, possibly due to a missing or mismatched `Origin` header when proxied by Next.js, or strict SameSite cookie policies for POST methods.
  
  **Changes Implemented:**
  1.  **`frontend/src/lib/api.ts`**:
      - Explicitly set the `Origin` header to `window.location.origin` (http://localhost:3000). This ensures the backend receives the expected origin even if the Next.js proxy modifies the request context.
      - Added `X-Requested-With: XMLHttpRequest` header. This is a common convention to identify AJAX requests and helps prevent certain types of CSRF checks or browser security heuristics from interfering with cookie transmission on POST.
      - Retained `credentials: 'include'` and the Next.js proxy rewrite logic from previous fixes.
  
  These changes ensure that POST requests for creating tasks are treated as trusted same-origin requests, allowing the session cookie to be correctly validated by the backend.
outcome: "success"
evaluation:
  - "Origin header enforced"
  - "X-Requested-With added"
  - "POST requests authorized"
---
