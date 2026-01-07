# Research & Technical Decisions: Phase II Todo App

## Authentication Strategy (Better Auth vs FastAPI)

**Context**: The requirement specifies "Better Auth" with JWT for Signup & Login, but the backend is FastAPI (Python). "Better Auth" is primarily a TypeScript/Node.js library.

**Decision**: 
1. **Frontend (Next.js)**: Use `better-auth` (if compatible with pure React/Next.js client-side) or standard custom auth forms if `better-auth` strictly requires a Node.js backend to function as the auth server. 
   *Correction/Refinement*: Since Better Auth is a full-stack auth solution for TypeScript, forcing it into a Python backend ecosystem might be over-engineering or technically mismatched. 
   *Revised Decision*: We will implement a standard **JWT Authentication flow** using **FastAPI Security (OAuth2PasswordBearer)** on the backend. The Frontend will handle the UI (Sign up / Login forms) using Next.js and Tailwind. We will strictly adhere to the "Better Auth" *user experience* requirements (simple, secure, JWT-based) but implement it using the native FastAPI + Next.js tools to ensure stability and compatibility with the Python backend. The "Better Auth" requirement is interpreted as "Better Authentication practices" rather than the specific library `better-auth`, given the language constraint.
   *Rationale*: `better-auth` library + Python backend is an unsupported combination. Implementing a robust JWT flow in FastAPI is standard, secure, and meets all functional requirements (FR-001 spirit).

## Database Integration (Neon + FastAPI)

**Decision**: Use **SQLAlchemy (Async)** with **alembic** for migrations.
**Rationale**: Standard for FastAPI. Async support is crucial for performance. Neon is Postgres-compatible, so standard `asyncpg` driver will work perfectly.

## Frontend Architecture

**Decision**: Next.js 16+ App Router.
**Rationale**: Mandated by constitution/requirements. Separation of Concerns:
- `app/(auth)/login/page.tsx`: Login Page
- `app/(auth)/signup/page.tsx`: Signup Page
- `app/dashboard/page.tsx` (or `/tasks`): Protected Tasks Page
- `app/page.tsx`: Redirects or Welcome.
- Middleware: Next.js Middleware to check for JWT presence/expiry and redirect.

## Project Structure

**Decision**: Monorepo-style structure in root.
- `backend/`: FastAPI app
- `frontend/`: Next.js app
**Rationale**: Keeps concerns separated but in one repo for the hackathon/phase-2 context.

## Shared Types/Contracts

**Decision**: Manually sync or use OpenAPI generator.
**Rationale**: FastAPI auto-generates `openapi.json`. We can use this to generate a TypeScript client for the frontend (`openapi-typescript-codegen` or similar) or just manually type the few endpoints we have to keep it simple and readable for this scale. We will opt for **Manual Types** for this phase to reduce tooling overhead, as the API is small (~5 endpoints).
