# Better Auth + Neon DB Complete Setup Tasks

## Phases
### PHASE 1: Cleanup & Preparation
- [ ] 1.1 Remove old custom auth backend code
- [ ] 1.2 Remove old auth frontend files (session.ts, auth-client.ts)
- [ ] 1.3 Clean database (keep connection string)
- [ ] 1.4 Create environment variables properly

### PHASE 2: Backend - API Setup with Better Auth  
- [ ] 2.1 Install better-auth package with PostgreSQL adapter
- [ ] 2.2 Initialize Better Auth in backend/src/lib/auth.ts
- [ ] 2.3 Configure Neon PostgreSQL connection properly
- [ ] 2.4 Set up migrations with better-auth
- [ ] 2.5 Test database connection and schema creation

### PHASE 3: Backend - API Endpoints
- [ ] 3.1 Create auth routes using better-auth endpoints
- [ ] 3.2 Setup getSession endpoint with error handling
- [ ] 3.3 Setup signUp/signIn endpoints
- [ ] 3.4 Setup logout endpoint with cleanup
- [ ] 3.5 Add CORS and middleware properly

### PHASE 4: Frontend - Authentication Setup
- [ ] 4.1 Install @better-auth/react client library
- [ ] 4.2 Create auth client configuration
- [ ] 4.3 Setup useAuth hook for React
- [ ] 4.4 Create auth provider/context wrapper
- [ ] 4.5 Add error boundaries for auth failures

### PHASE 5: Frontend - Pages & Guards
- [ ] 5.1 Create/update login page with error handling
- [ ] 5.2 Create/update signup page with validation
- [ ] 5.3 Create AuthGuard component for protected routes
- [ ] 5.4 Update layout with session provider
- [ ] 5.5 Setup redirect logic for unauthenticated users

### PHASE 6: Frontend - Task Integration
- [ ] 6.1 Create tasks API client with auth headers
- [ ] 6.2 Fetch tasks with proper error handling
- [ ] 6.3 Create task with auth verification
- [ ] 6.4 Update task with auth
- [ ] 6.5 Delete task with auth
- [ ] 6.6 Test all operations with auth

### PHASE 7: Error Handling & Edge Cases
- [ ] 7.1 Implement token expiration handling
- [ ] 7.2 Add session refresh logic
- [ ] 7.3 Handle network errors gracefully
- [ ] 7.4 Add rate limiting on auth endpoints
- [ ] 7.5 Implement proper logging for debugging

### PHASE 8: Testing & Verification
- [ ] 8.1 Test signup flow end-to-end
- [ ] 8.2 Test login flow end-to-end
- [ ] 8.3 Test logout flow
- [ ] 8.4 Test task operations while authenticated
- [ ] 8.5 Test unauthorized access (401 handling)
- [ ] 8.6 Test session persistence across page reload

## Status Tracking
- **Current Phase**: PHASE 1
- **Completed**: 0/53 tasks
- **In Progress**: None
- **Last Updated**: 2026-01-15

## Notes
- Database connection string will be reused: `postgresql://neondb_owner:npg_hzlM1ECn7kmu@ep-small-flower-admw54i9-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require`
- Better Auth Secret: `2WypiaRVBrMvEaUAlUYkYc1kaL9b59ct`
- All error handling must be secure and not leak sensitive info
- All endpoints must validate input and handle edge cases
