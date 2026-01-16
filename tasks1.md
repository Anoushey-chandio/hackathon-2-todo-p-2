# Full-Stack Todo App - Bug Fix & Verification Tasks

**Status**: In Progress  
**Date**: 2026-01-15  
**Goal**: Resolve all API errors and verify full end-to-end functionality

---

## Environment Status
- [x] Python: 3.13.9
- [x] Virtual Environment: Active
- [x] Backend: Running on http://127.0.0.1:8000
- [x] Frontend: Running on http://localhost:3000
- [x] Database: Neon PostgreSQL configured

---

## Installed Dependencies (Verified ✅)
- [x] fastapi 0.124.4
- [x] httpx 0.28.1
- [x] pydantic 2.10.3
- [x] sqlalchemy 2.0.36
- [x] PyJWT 2.10.1
- [x] requests 2.32.5

---

## Issues to Fix

### Issue #1: API Routing Problems
**Status**: Testing  
**Symptoms**: 400/500 errors on auth endpoints  
**Root Cause**: API prefix routing issues  
**Fix**: Verify correct API paths in frontend  

**Endpoints to Test**:
- POST `/api/auth/sign-up` - Create account
- POST `/api/auth/sign-in` - Login with email/password
- GET `/api/auth/session` - Get session with Bearer token
- POST `/api/auth/sign-out` - Logout

---

### Issue #2: Frontend API Base URL
**Status**: Testing  
**Symptoms**: Frontend can't reach backend endpoints  
**Root Cause**: API base URL not correctly configured  
**Fix**: Verify Next.js rewrites and API client configuration  

**Config Files**:
- [ ] frontend/next.config.ts - Check rewrites
- [ ] frontend/src/lib/api.ts - Check base URL
- [ ] frontend/src/lib/auth-client.ts - Check endpoint paths

---

### Issue #3: Database Connection
**Status**: Verifying  
**Symptoms**: Database operations might fail  
**Root Cause**: Neon connection or schema issues  
**Fix**: Verify tables exist and connection works  

**Check**:
- [ ] Neon PostgreSQL connection active
- [ ] All 6 tables created (user, tasks, session, account, verification, jwks)
- [ ] Can read/write to user table

---

### Issue #4: Auth Flow Integration
**Status**: Testing  
**Symptoms**: Signup/Login doesn't work end-to-end  
**Root Cause**: Frontend-backend communication issue  
**Fix**: Test each step of auth flow  

**Steps**:
1. [ ] Test signup form submission
2. [ ] Verify JWT token returned
3. [ ] Store token in localStorage
4. [ ] Use token in subsequent requests
5. [ ] Verify session endpoint
6. [ ] Test logout flow

---

## Test Plan

### Step 1: API Health Check
- [ ] Backend responds to GET http://127.0.0.1:8000/
- [ ] Frontend dev server is ready
- [ ] CORS headers allow localhost:3000

### Step 2: Sign-Up Endpoint Test
```
POST http://127.0.0.1:8000/api/auth/sign-up
Body: {
  "email": "test@example.com",
  "password": "TestPassword123!",
  "name": "Test User"
}
Expected: 200 OK with JWT token
```

### Step 3: Sign-In Endpoint Test
```
POST http://127.0.0.1:8000/api/auth/sign-in
Body: {
  "email": "test@example.com",
  "password": "TestPassword123!"
}
Expected: 200 OK with JWT token
```

### Step 4: Session Endpoint Test
```
GET http://127.0.0.1:8000/api/auth/session
Headers: Authorization: Bearer <token>
Expected: 200 OK with user data
```

### Step 5: Frontend Sign-Up Flow
- [ ] Navigate to http://localhost:3000/signup
- [ ] Fill form with email, password, name
- [ ] Submit form
- [ ] Check network tab for /api/auth/sign-up request
- [ ] Verify response has token
- [ ] Check localStorage for token
- [ ] Should redirect to dashboard

### Step 6: Frontend Sign-In Flow
- [ ] Navigate to http://localhost:3000/login
- [ ] Enter credentials
- [ ] Submit form
- [ ] Verify API call succeeds
- [ ] Check token stored
- [ ] Should redirect to dashboard

### Step 7: Protected Routes
- [ ] Verify /dashboard redirects to /login if not authenticated
- [ ] Dashboard shows user info after login
- [ ] Tasks page loads

---

## Bug Resolution Log

| # | Issue | Root Cause | Fix Applied | Status |
|---|-------|-----------|-------------|--------|
| 1 | 400/500 on sign-up | TBD | Pending | 🟡 |
| 2 | 400/500 on login | TBD | Pending | 🟡 |
| 3 | API base URL mismatch | TBD | Pending | 🟡 |
| 4 | CORS issues | TBD | Pending | 🟡 |
| 5 | Session not persisting | TBD | Pending | 🟡 |

---

## Verification Checklist

**System Components**:
- [ ] Backend starts without errors
- [ ] Database initializes successfully
- [ ] Frontend builds successfully
- [ ] All 6 database tables exist

**API Endpoints**:
- [ ] POST /api/auth/sign-up works
- [ ] POST /api/auth/sign-in works
- [ ] GET /api/auth/session works
- [ ] POST /api/auth/sign-out works

**Frontend Features**:
- [ ] Signup page functional
- [ ] Login page functional
- [ ] Dashboard protected and working
- [ ] Task management works
- [ ] Logout works

**End-to-End Flow**:
- [ ] Can create new account via signup
- [ ] Can login with credentials
- [ ] Can create tasks
- [ ] Can view/edit/delete tasks
- [ ] Can logout
- [ ] Can login again
- [ ] Session persists correctly

---

## Success Criteria
✅ All API endpoints return 200/201 OK  
✅ Frontend can communicate with backend  
✅ Auth flow works end-to-end  
✅ Data persists in Neon PostgreSQL  
✅ No console errors or warnings  
✅ User can complete full signup→login→tasks→logout flow  

---

## Next Actions
1. Test API endpoints with curl/httpx
2. Check browser DevTools network tab for errors
3. Review backend logs for any exceptions
4. Verify frontend API client configuration
5. Fix issues one by one
6. Re-test after each fix

