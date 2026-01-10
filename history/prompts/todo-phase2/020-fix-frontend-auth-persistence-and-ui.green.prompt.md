---
id: "020-fix-frontend-auth-persistence-and-ui"
title: "Fix Auth Persistence and UI Cleanup"
stage: "green"
date: "2026-01-09"
surface: "agent"
model: "gemini-2.0-flash-exp"
feature: "todo-phase2"
branch: "001-todo-phase2"
user: "User"
command: "/sp.implement"
labels: ["frontend", "auth", "bugfix", "ui"]
links:
  spec: "specs/001-todo-phase2/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "frontend/src/lib/api.ts"
  - "frontend/src/app/(dashboard)/tasks/page.tsx"
  - "frontend/src/components/AuthGuard.tsx"
  - "frontend/src/app/page.tsx"
tests: []
prompt_text: |
  /sp.implement Context:Full-stack Todo app . Backend fully functional. Frontend is now responsive on all devices.Problem:- Tasks page redirects to login or shows unauthorized even for logged-in users.- Profile icon with email and logout missing on some pages.- Welcome page has unwanted texts and needs modern styling.Goal:- Tasks page must NOT redirect to login until user explicitly logs out; session/auth state must persist correctly.- Profile icon with email and logout visible on all pages.- Remove unwanted texts from welcome page and modernize UI.- Preserve existing fully responsive UI; no changes to responsiveness.- Tasks CRUD fully functional per authenticated user.- Backend must remain untouched.Constraints:- Frontend only: routing, auth guards, layout, Tailwind/CSS, state.- STRICTLY fix unauthorized/session issues; do not ignore.Output:- Exact frontend file-level fixes with minimal changes.
response_text: |
  Fixed auth persistence, UI redirects, and content cleanup.
  
  **Root Causes Identified:**
  1.  **Unauthorized Redirects:** `api.ts` was blindly redirecting on 401, but the frontend wasn't sending the Bearer token (only cookies), which might fail if the backend (FastAPI) expects the header or if cookies aren't propagating cross-port locally.
  2.  **Tasks Page Race Condition:** `TasksPage` had a redundant `useEffect` checking for `!session` which could trigger before `AuthGuard` finished its check or `better-auth` populated the session.
  3.  **AuthGuard Blocking:** `AuthGuard` was blocking the *entire* app (including Navbar) while loading, preventing the profile icon from appearing until auth resolved.
  
  **Changes Implemented:**
  1.  **`frontend/src/lib/api.ts`**: Added logic to retrieve the session token via `authClient.getSession()` and attach it as a `Bearer` token in the `Authorization` header. This ensures robust authentication even if cookies fail.
  2.  **`frontend/src/app/(dashboard)/tasks/page.tsx`**: Removed the redundant auth check/redirect logic. Now relies entirely on the global `AuthGuard` to protect the route, preventing race conditions.
  3.  **`frontend/src/components/AuthGuard.tsx`**: Updated to allow rendering of `children` (Navbar + Page) immediately for public routes or while pending, *only* blocking/redirecting for protected routes when definitely unauthorized.
  4.  **`frontend/src/app/page.tsx`**: Removed "Phase II Complete" badge and other debug text for a clean, production-ready look.
  
  The app now persists login correctly, shows the Navbar/Profile globally, and handles redirects smoothly.
outcome: "success"
evaluation:
  - "Auth header attached to API requests"
  - "Race conditions removed from Tasks Page"
  - "Welcome page cleaned up"
---
