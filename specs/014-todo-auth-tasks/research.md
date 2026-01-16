# Research: Full-Stack Todo App Auth and Tasks

**Status**: Complete
**Date**: 2026-01-15

## 1. Auth Redirect Loop Prevention

**Context**: Redirect loops often occur when the authentication state is ambiguous or when protected/public route logic conflicts (e.g., a protected page redirects to login, which thinks the user is logged in and redirects back).

**Findings & Decisions**:
- **Decision**: Use Next.js Middleware (`middleware.ts`) as the single source of truth for route protection.
- **Mechanism**:
  1. Middleware runs on every request.
  2. Extracts session token from HTTP-only cookie.
  3. Validates token presence (and optionally validity via stateless check or fast edge call).
  4. Logic:
     - If path is `/dashboard` (or protected) AND no token -> Redirect `/login`.
     - If path is `/login` (or public auth) AND token exists -> Redirect `/dashboard`.
     - Otherwise -> `NextResponse.next()`.
- **Rationale**: Centralized logic prevents component-level race conditions (`useEffect` redirects) that often cause loops.

## 2. FastAPI & Next.js Alignment (CORS & Ports)

**Context**: Frontend runs on port 3000, Backend on 8000. Cross-origin requests need proper configuration.

**Findings & Decisions**:
- **Decision**: Configure FastAPI CORS middleware to explicitly allow `http://localhost:3000`.
- **Decision**: Use a shared configuration or constant for API Base URL in Next.js (`NEXT_PUBLIC_API_URL=http://localhost:8000`).
- **Rationale**: Strict allow-list is more secure than `*`.

## 3. JWT Implementation (Better Auth Pattern)

**Context**: The Constitution mandates "Better Auth with JWT".

**Findings & Decisions**:
- **Decision**: Implement a custom, lightweight JWT auth flow in FastAPI if a specific "Better Auth" library isn't already integrated (assuming standard library approach for Python context).
- **Tech**: `python-jose` for encoding/decoding, `passlib` for password hashing.
- **Flow**:
  1. **Signup**: `POST /auth/signup` -> Hashes password -> Stores User -> Returns JWT.
  2. **Login**: `POST /auth/login` -> Verifies hash -> Returns JWT.
  3. **Access**: Frontend attaches `Authorization: Bearer <token>` header (or uses Cookie if proxying). Given the requirement for "HTTP-only cookies" in FR-002, we will prefer setting an HTTP-only cookie on the backend response.
  4. **Verification**: FastAPI dependency `get_current_user` decodes token and fetches user.

## 4. Database Integration (Neon + SQLAlchemy)

**Context**: Using Neon PostgreSQL.

**Findings & Decisions**:
- **Decision**: Use `SQLModel` (wrapper around SQLAlchemy) for modern, Pydantic-friendly interactions.
- **Rationale**: Reduces boilerplate and aligns with FastAPI's type system.

## 5. Error Handling for Unauthorized Access

**Findings & Decisions**:
- **Decision**: FastAPI raises `HTTPException(status_code=401)` for invalid tokens.
- **Decision**: Frontend `api` client intercepts 401 responses, clears local state/cookies, and redirects to `/login`.
