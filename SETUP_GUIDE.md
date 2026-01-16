# Todo App - Complete Setup Guide

## Overview

This is a full-stack Todo application with:
- **Frontend**: Next.js 16.1.1 with TypeScript, Tailwind CSS, and better-auth client
- **Backend**: FastAPI with async SQLAlchemy, PostgreSQL (Neon), and JWT authentication
- **Database**: Neon PostgreSQL (cloud-hosted)
- **Authentication**: Email/password with JWT tokens

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     BROWSER                                  │
│  (Stores JWT token in localStorage)                          │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/REST
                       ↓
┌─────────────────────────────────────────────────────────────┐
│               FRONTEND (Next.js 16.1.1)                      │
│  - better-auth client for sign-up/sign-in/sign-out         │
│  - Protected pages with AuthGuard component                 │
│  - Task management UI                                        │
│  - Port: 3000                                                │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/REST
                       │ (API rewrites /api/* to backend)
                       ↓
┌─────────────────────────────────────────────────────────────┐
│               BACKEND (FastAPI)                              │
│  - Auth endpoints: /api/auth/sign-up, /sign-in, /session    │
│  - Task endpoints: /api/tasks                                │
│  - JWT validation on protected routes                        │
│  - Port: 8000                                                │
└──────────────────────┬──────────────────────────────────────┘
                       │ SQL/Async
                       ↓
┌─────────────────────────────────────────────────────────────┐
│         DATABASE (Neon PostgreSQL)                           │
│  - Users table (id, email, password, name, createdAt)       │
│  - Tasks table (id, userId, title, description, done, ...)  │
│  - Automatic SSL connection (sslmode=require)               │
└─────────────────────────────────────────────────────────────┘
```

## Prerequisites

- **Python 3.11+** (Backend)
- **Node.js 18+** (Frontend)
- **PostgreSQL 13+** or Neon account (Database)
- **Git** (for version control)

## Quick Start

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment (if not already done)
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Install additional auth packages
pip install PyJWT cryptography passlib

# Create .env file with database and secrets
cat > .env << EOF
DATABASE_URL=postgresql://neondb_owner:npg_hzlM1ECn7kmu@ep-small-flower-admw54i9-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require
BETTER_AUTH_SECRET=2WypiaRVBrMvEaUAlUYkYc1kaL9b59ct
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
EOF

# Start backend server (from backend directory)
uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
```

Backend will be available at: **http://127.0.0.1:8000**

### 2. Frontend Setup

```bash
# In a NEW terminal, navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at: **http://localhost:3000**

## API Endpoints

### Authentication

#### Sign Up
```http
POST /api/auth/sign-up
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "John Doe"
}

Response (200):
{
  "session": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "Bearer",
    "expires_in": 1800
  },
  "user": {
    "id": "1",
    "email": "user@example.com",
    "name": "John Doe",
    "image": null,
    "emailVerified": null,
    "createdAt": "2024-01-15T10:30:00Z",
    "updatedAt": "2024-01-15T10:30:00Z"
  }
}
```

#### Sign In
```http
POST /api/auth/sign-in
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securePassword123"
}

Response (200): Same as Sign Up
```

#### Get Session
```http
GET /api/auth/session
Authorization: Bearer <token>

Response (200):
{
  "session": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "Bearer"
  },
  "user": { ... }
}
```

#### Sign Out
```http
POST /api/auth/sign-out

Response (200):
{
  "success": true
}
```

### Tasks

#### Get All Tasks
```http
GET /api/tasks
Authorization: Bearer <token>

Response (200):
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "done": false,
    "userId": 1,
    "createdAt": "2024-01-15T10:30:00Z",
    "updatedAt": "2024-01-15T10:30:00Z"
  }
]
```

#### Create Task
```http
POST /api/tasks
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}

Response (201):
{
  "id": 1,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "done": false,
  "userId": 1,
  "createdAt": "2024-01-15T10:30:00Z",
  "updatedAt": "2024-01-15T10:30:00Z"
}
```

#### Update Task
```http
PUT /api/tasks/1
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Updated title",
  "done": true
}

Response (200):
{ ... updated task ... }
```

#### Delete Task
```http
DELETE /api/tasks/1
Authorization: Bearer <token>

Response (200):
{
  "success": true
}
```

## Database Schema

### Users Table
```sql
CREATE TABLE "user" (
  id SERIAL PRIMARY KEY,
  email VARCHAR UNIQUE NOT NULL,
  password VARCHAR,
  name VARCHAR,
  emailVerified TIMESTAMP,
  image VARCHAR,
  createdAt TIMESTAMP DEFAULT NOW(),
  updatedAt TIMESTAMP DEFAULT NOW()
);
```

### Tasks Table
```sql
CREATE TABLE task (
  id SERIAL PRIMARY KEY,
  userId INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
  title VARCHAR NOT NULL,
  description TEXT,
  done BOOLEAN DEFAULT FALSE,
  createdAt TIMESTAMP DEFAULT NOW(),
  updatedAt TIMESTAMP DEFAULT NOW()
);
```

## Authentication Flow

### Sign Up Flow
1. User enters email, password, and name on signup page
2. Frontend sends POST to `/api/auth/sign-up`
3. Backend creates user with hashed password
4. Backend returns JWT access token
5. Frontend stores token in localStorage
6. Frontend redirects to dashboard

### Sign In Flow
1. User enters email and password on login page
2. Frontend sends POST to `/api/auth/sign-in`
3. Backend verifies password, creates session
4. Backend returns JWT access token
5. Frontend stores token in localStorage
6. Frontend redirects to dashboard

### Protected Routes
1. Frontend reads token from localStorage
2. On each API call, token sent in Authorization header: `Bearer <token>`
3. Backend validates JWT signature and expiry
4. If valid, request processed; if invalid, returns 401 Unauthorized
5. Frontend catches 401 and redirects to login

## Token Management

### JWT Token Structure
```
Header: {
  "alg": "HS256",
  "typ": "JWT"
}

Payload: {
  "sub": "1",              // user ID
  "email": "user@example.com",
  "type": "access",
  "iat": 1705325400,       // issued at
  "exp": 1705327200        // expires in 30 minutes
}

Signature: HMACSHA256(header + payload, secret)
```

### Token Expiry Handling
- **Access Token**: 30 minutes
- **Refresh Token**: 7 days (optional future feature)
- When token expires, frontend redirects to login
- User must sign in again to get new token

## Configuration Files

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
BETTER_AUTH_SECRET=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### Frontend (next.config.ts)
```typescript
rewrites: async () => [
  // Authentication rewrites
  {
    source: '/api/auth/:path*',
    destination: 'http://127.0.0.1:8000/api/auth/:path*',
  },
  // Task API rewrites
  {
    source: '/api/py/:path*',
    destination: 'http://127.0.0.1:8000/api/:path*',
  },
]
```

## Troubleshooting

### Backend Issues

#### Database Connection Failed
- **Symptom**: `Error connecting to database`
- **Solution**: 
  1. Check DATABASE_URL in `.env`
  2. Verify Neon account credentials
  3. Ensure sslmode=require is in URL
  4. Test with: `psql <DATABASE_URL>`

#### Port 8000 Already in Use
- **Symptom**: `Address already in use`
- **Solution**: `lsof -i :8000` (macOS/Linux) or `netstat -ano | findstr :8000` (Windows), then kill the process

#### ModuleNotFoundError: No module named 'jwt'
- **Solution**: `pip install PyJWT`

#### 401 Unauthorized on Protected Routes
- **Symptom**: Can sign up/in but task endpoints return 401
- **Solution**:
  1. Check token is in Authorization header
  2. Verify token hasn't expired
  3. Check BETTER_AUTH_SECRET matches frontend

### Frontend Issues

#### API calls return 404
- **Symptom**: Requests to `/api/auth/*` return 404
- **Solution**:
  1. Ensure backend is running on port 8000
  2. Check next.config.ts rewrites are correct
  3. Restart frontend dev server: `npm run dev`

#### Token not persisting across page reloads
- **Symptom**: User logged out after F5 refresh
- **Solution**: 
  1. Check localStorage is being used (DevTools → Application → Local Storage)
  2. Verify AuthGuard component is reading token
  3. Call `/api/auth/session` on page load to re-validate

#### CORS errors
- **Symptom**: `Access to XMLHttpRequest at 'http://127.0.0.1:8000' from origin 'http://localhost:3000' has been blocked by CORS`
- **Solution**:
  1. Backend has CORS configured for `http://localhost:3000`
  2. Verify next.config.ts rewrites are working (should proxy through /api/*)
  3. Check backend isn't returning CORS errors in logs

## Development Workflow

### Running Both Servers
```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn src.main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev
```

### Making Changes

**Backend**:
1. Edit files in `backend/src/`
2. Uvicorn auto-reloads on save
3. Test with: `curl -H "Authorization: Bearer <token>" http://127.0.0.1:8000/api/tasks`

**Frontend**:
1. Edit files in `frontend/src/`
2. Next.js hot-reloads on save
3. Check DevTools → Network tab for API responses

### Debugging

**Backend Logs**:
```bash
# Uvicorn logs show all requests/responses
# Look for status codes: 200 (OK), 400 (Bad Request), 401 (Unauthorized)
```

**Frontend Logs**:
```bash
# Browser DevTools Console for JavaScript errors
# Network tab to inspect API requests/responses
# Local Storage to check token persistence
```

## Security Best Practices

### Production Checklist
- [ ] Change `BETTER_AUTH_SECRET` to a strong random string
- [ ] Set `secure=True` in FastAPI CORS settings
- [ ] Use HTTPS in production (set `base_url` to https)
- [ ] Hash passwords with bcrypt (already implemented)
- [ ] Implement rate limiting on auth endpoints
- [ ] Add CSRF protection for state-changing operations
- [ ] Implement refresh token rotation
- [ ] Add email verification flow
- [ ] Monitor failed login attempts
- [ ] Keep dependencies updated

### Current Security Measures
- ✅ Passwords hashed with bcrypt
- ✅ JWT signatures validated with secret
- ✅ CORS restricted to localhost
- ✅ HTTPOnly flag on session cookies (not used currently)
- ✅ Token expiry enforced
- ✅ SQL injection prevented with parameterized queries

## Performance Optimization

### Backend
- Async database operations (asyncio + asyncpg)
- Connection pooling with asyncpg
- Lazy-loading relationships
- Database indexing on frequently queried columns

### Frontend
- Code splitting with Next.js
- Image optimization with next/image
- Tailwind CSS tree-shaking
- Client-side caching of task lists

## Testing

See `TEST_INTEGRATION.md` for comprehensive integration tests.

### Quick Manual Test
```bash
# 1. Sign up
curl -X POST http://127.0.0.1:8000/api/auth/sign-up \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "name": "Test User"
  }'

# 2. Save the access_token from response
TOKEN="eyJhbGciOiJIUzI1NiIs..."

# 3. Get session
curl -H "Authorization: Bearer $TOKEN" \
  http://127.0.0.1:8000/api/auth/session

# 4. Create task
curl -X POST http://127.0.0.1:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test task",
    "description": "Testing the API"
  }'

# 5. Get tasks
curl -H "Authorization: Bearer $TOKEN" \
  http://127.0.0.1:8000/api/tasks
```

## Further Reading

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Neon Documentation](https://neon.tech/docs)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)

## Support

For issues or questions:
1. Check logs in both backend and frontend
2. Verify database connection
3. Test API endpoints with curl
4. Check browser DevTools (Network, Console, Application tabs)
5. Review this guide's Troubleshooting section
