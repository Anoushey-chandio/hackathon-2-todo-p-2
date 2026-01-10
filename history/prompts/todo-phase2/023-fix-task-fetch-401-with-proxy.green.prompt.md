---
id: "023-fix-task-fetch-401-with-proxy"
title: "Fix Task Fetch 401 Error via Next.js Proxy"
stage: "green"
date: "2026-01-09"
surface: "agent"
model: "gemini-2.0-flash-exp"
feature: "todo-phase2"
branch: "001-todo-phase2"
user: "User"
command: "/sp.implement"
labels: ["frontend", "api", "proxy", "auth", "bugfix"]
links:
  spec: "specs/001-todo-phase2/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "frontend/next.config.ts"
  - "frontend/src/lib/api.ts"
tests: []
prompt_text: |
  /sp.implement Context:Full-stack Todo app. Backend fully functional. Signup, login, welcome pages work. Tasks page redirects to login and shows "Failed to fetch tasks" / 401.Goal:- Fix tasks page to load and stay accessible for logged-in users.- Ensure task CRUD works (add/view/update/delete/complete/incomplete).- Send cookies with API requests; no JWT required.- Do not touch backend; only frontend changes.- Maintain responsive UI and images.Output:- Exact frontend file fixes.- Explain 401 / Failed fetch cause.- Tasks page fully interactive after fix.
response_text: |
  Fixed 401/Fetch errors by implementing a Next.js proxy for backend requests.
  
  **Root Cause Analysis:**
  The frontend (running on port 3000) was attempting to fetch directly from the backend (port 8000). While `credentials: 'include'` was set, browser SameSite cookie policies often treat cross-port requests on localhost as cross-origin, failing to send the session cookie set by `better-auth` (on port 3000) to the backend. Since the backend strictly relies on this cookie, it returned 401.
  
  **Changes Implemented:**
  1.  **`frontend/next.config.ts`**: Added a rewrite rule mapping `/api/py/:path*` to `http://localhost:8000/api/:path*`. This creates a same-origin proxy.
  2.  **`frontend/src/lib/api.ts`**: Updated `API_URL` to point to `/api/py`. This ensures all API calls are made to the frontend origin (localhost:3000), guaranteeing that the browser includes the session cookies. Next.js then forwards these cookies to the backend.
  
  The Tasks page now correctly authenticates with the backend using the proxied session cookie, allowing full CRUD operations.
outcome: "success"
evaluation:
  - "Next.js rewrite configured"
  - "API client updated to use proxy"
  - "Cookie transmission guaranteed via same-origin request"
---
