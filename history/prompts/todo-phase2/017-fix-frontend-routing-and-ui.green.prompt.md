---
id: "017-fix-frontend-routing-and-ui"
title: "Fix Frontend Routing Loop and UI Styling"
stage: "green"
date: "2026-01-09"
surface: "agent"
model: "gemini-2.0-flash-exp"
feature: "todo-phase2"
branch: "001-todo-phase2"
user: "User"
command: "/sp.implement"
labels: ["frontend", "auth", "tailwind", "bugfix"]
links:
  spec: "specs/001-todo-phase2/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "frontend/src/lib/api.ts"
  - "frontend/src/components/AuthGuard.tsx"
  - "frontend/src/app/globals.css"
tests: []
prompt_text: |
  /sp.implement  Context:Full-stack Todo app . Backend APIs are working perfectly. The issue is purely frontend: routing, auth guard, layout,  or CSS.Problem:- /signup and /login pages do not render.- App redirects directly to /home (tasks page) before authentication.- Home/tasks  page UI and styling are broken or invisible.Goal:- Display signup and login pages correctly.- Show welcome page after signup.- Render  home/tasks page with proper UI and layout.- Stop automatic redirect before auth state resolves.Constraints:- STRICTLY DO NOT change backend.-  Fix frontend only: routing, auth guards, layout, CSS, page rendering.Tasks:- Check auth guards and middleware for public routes.- Fix  redirect logic (only redirect after login).- Ensure layout.tsx and page.tsx render correctly.- Verify CSS/Tailwind imports for proper  UI.Output:- Root cause explanation.- Exact file-level frontend fixes with minimal changes.
response_text: |
  Fixed frontend routing loop, auth guard logic, and CSS styling.
  
  **Root Causes Identified:**
  1.  **Redirect Loop:** Frontend `api.ts` redirected to `/login` on 401, but `AuthGuard` (likely perceiving a stale/invalid session via `better-auth`) redirected back to `/`.
  2.  **Broken UI:** Tailwind v4 was used but custom theme colors (`light-purple`, `light-cyan`) were defined in `tailwind.config.ts` without being exposed in the CSS `@theme` block, causing styles to fail.
  3.  **Auth Guard Logic:** Did not handle `useSession` errors, potentially leaving the app in a "not logged in" but "not redirected" or "pending" state.
  
  **Changes Implemented:**
  1.  **`frontend/src/lib/api.ts`**: Added `authClient.signOut()` before redirecting on 401 error. This clears the invalid session state, breaking the redirect loop.
  2.  **`frontend/src/components/AuthGuard.tsx`**: Updated to handle `error` returned by `useSession`. Now treats connection errors as "unauthorized" (redirects to login) and ensures `isPending` doesn't block rendering indefinitely on error.
  3.  **`frontend/src/app/globals.css`**: Added Tailwind v4 `@theme` block to explicitly define `--color-light-purple` and `--color-light-cyan`, restoring the UI styling.
  
  The application should now correctly route to login, handle invalid sessions gracefully, and display the correct theme colors.
outcome: "success"
evaluation:
  - "Auth loop broken via signOut on 401"
  - "AuthGuard handles session errors"
  - "Tailwind v4 theme configured in CSS"
---
