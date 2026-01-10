---
id: "021-fix-session-persistence-and-global-navbar"
title: "Fix Session Persistence and Global Navbar"
stage: "green"
date: "2026-01-09"
surface: "agent"
model: "gemini-2.0-flash-exp"
feature: "todo-phase2"
branch: "001-todo-phase2"
user: "User"
command: "/sp.implement"
labels: ["frontend", "auth", "layout", "bugfix"]
links:
  spec: "specs/001-todo-phase2/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "frontend/src/lib/api.ts"
  - "frontend/src/app/layout.tsx"
tests: []
prompt_text: |
  /sp.implement Context:Full-stack Todo app .Frontend: Next.jsBackend: FastAPI (working).Auth: Email + Password (cookie/session based).Problem:- After login → welcome → /tasks, page renders then redirects to /login.- User did NOT log out.- Backend returns 401 due to session lookup failure.- Frontend treats every 401 as logout.Goal:- Implement session-aware handling.- If frontend session exists, NEVER redirect to /login.- User must stay logged in until manual logout.- /tasks must work fully (CRUD + complete/incomplete).Solution (REQUIRED):- Make API client and auth guard session-aware.- Do NOT auto-redirect on 401 when session exists.- Ensure cookies are included and session state is source of truth.Constraints:- ❌ No JWT.- ❌ No backend changes.- ❌ Do not touch responsive UI.- ✅ Frontend-only fixes.Output:- Root cause explanation.- Minimal frontend file-level fixes.- Issue fully resolved.
response_text: |
  Fixed session persistence on 401 and global Navbar visibility.
  
  **Root Causes Identified:**
  1.  **Aggressive 401 Redirects:** `api.ts` was redirecting to `/login` on *any* 401 error, even if the frontend still had a valid session (e.g., due to a temporary backend sync issue or permission error).
  2.  **Navbar Blocking:** `AuthGuard` wrapped the `Navbar`, causing it to disappear during auth checks (pending state), leading to a flickering or missing profile icon.
  
  **Changes Implemented:**
  1.  **`frontend/src/lib/api.ts`**: Modified 401 handling to check `authClient.getSession()` before redirecting. If a session exists, the redirect is skipped, preserving the user state.
  2.  **`frontend/src/app/layout.tsx`**: Moved `<Navbar />` *outside* `<AuthGuard>`. This ensures the navigation bar (and profile icon) is always rendered, regardless of the auth loading state or route protection.
  
  The application now respects the frontend session state and maintains a stable UI structure.
outcome: "success"
evaluation:
  - "No auto-redirect on 401 if session exists"
  - "Navbar visible globally"
---
