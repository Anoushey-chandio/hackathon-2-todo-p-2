# Testing Guide

This document describes how to test the Todo App authentication and task management features.

## Quick Start Testing

### 1. Start the Backend

Open a terminal in the `backend` directory:

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux

# Start backend
python -m uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
```

You should see output like:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 [press SHIFT+W to quit]
```

### 2. Run Quick Tests (in another terminal)

From the project root directory:

```bash
python run_quick_tests.py
```

This will:
- ✅ Test backend connection
- ✅ Test user sign up
- ✅ Test session retrieval
- ✅ Test error handling
- ✅ Test task creation
- ✅ Test task list retrieval
- ✅ Test task update
- ✅ Test task deletion

## Comprehensive Integration Tests

### Run Full Test Suite

From the project root directory:

```bash
# Install pytest if not already installed
pip install pytest httpx

# Run all tests with verbose output
pytest TEST_INTEGRATION.md -v

# Run specific test class
pytest TEST_INTEGRATION.md::TestAuthenticationFlow -v

# Run specific test
pytest TEST_INTEGRATION.md::TestAuthenticationFlow::test_sign_up_success -v

# Run with coverage
pytest TEST_INTEGRATION.md --cov=backend/src --cov-report=html
```

## Test Coverage

### Authentication Tests (TestAuthenticationFlow)
- ✅ Sign up success
- ✅ Sign up with duplicate email
- ✅ Sign in success
- ✅ Sign in with wrong password
- ✅ Sign in with non-existent user
- ✅ Get session success
- ✅ Get session with invalid token
- ✅ Get session without auth header
- ✅ Sign out success

### Task Management Tests (TestTaskManagement)
- ✅ Create task success
- ✅ Create task without title
- ✅ Create task without authentication
- ✅ Get all tasks success
- ✅ Get all tasks without authentication
- ✅ Get task by ID
- ✅ Get non-existent task
- ✅ Update task success
- ✅ Update task without authentication
- ✅ Delete task success
- ✅ Delete non-existent task

### Error Handling Tests (TestErrorHandling)
- ✅ Malformed JSON
- ✅ Invalid email format
- ✅ Weak password
- ✅ Missing required field
- ✅ Expired/tampered token handling

### Integration Tests (TestIntegration)
- ✅ Complete signup → create task → update → delete workflow
- ✅ Multiple users with isolated tasks

## Manual Testing with curl

### Sign Up
```bash
curl -X POST http://127.0.0.1:8000/api/auth/sign-up \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123!",
    "name": "Test User"
  }'
```

Expected Response (200):
```json
{
  "session": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "Bearer",
    "expires_in": 1800
  },
  "user": {
    "id": "1",
    "email": "test@example.com",
    "name": "Test User",
    "image": null,
    "emailVerified": null,
    "createdAt": "2024-01-15T10:30:00Z",
    "updatedAt": "2024-01-15T10:30:00Z"
  }
}
```

### Sign In
```bash
curl -X POST http://127.0.0.1:8000/api/auth/sign-in \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123!"
  }'
```

### Get Session
```bash
TOKEN="<access_token_from_signup>"

curl -H "Authorization: Bearer $TOKEN" \
  http://127.0.0.1:8000/api/auth/session
```

### Create Task
```bash
TOKEN="<access_token>"

curl -X POST http://127.0.0.1:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Task",
    "description": "Task description"
  }'
```

### Get All Tasks
```bash
TOKEN="<access_token>"

curl -H "Authorization: Bearer $TOKEN" \
  http://127.0.0.1:8000/api/tasks
```

### Update Task
```bash
TOKEN="<access_token>"
TASK_ID="1"

curl -X PUT "http://127.0.0.1:8000/api/tasks/$TASK_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title",
    "done": true
  }'
```

### Delete Task
```bash
TOKEN="<access_token>"
TASK_ID="1"

curl -X DELETE "http://127.0.0.1:8000/api/tasks/$TASK_ID" \
  -H "Authorization: Bearer $TOKEN"
```

## Frontend Testing

### 1. Start Frontend Dev Server

In a new terminal from the `frontend` directory:

```bash
npm run dev
```

### 2. Test Sign Up Flow
1. Open http://localhost:3000
2. Click "Sign up"
3. Enter email, password, name
4. Click "Sign up"
5. Verify redirected to dashboard

### 3. Test Sign In Flow
1. Open http://localhost:3000
2. Click "Sign in"
3. Enter email and password
4. Click "Sign in"
5. Verify redirected to dashboard with task list

### 4. Test Task Management
1. Sign in to app
2. Add new task
3. Check task appears in list
4. Mark task as done
5. Delete task
6. Verify task is removed

## Debugging

### Backend Issues

**Check logs:**
```bash
# Uvicorn logs show all requests
# Look for error messages and status codes
```

**Test database connection:**
```bash
# From backend directory
python -c "from src.core.database import init_db; import asyncio; asyncio.run(init_db())"
```

**Test a single endpoint:**
```bash
curl -v http://127.0.0.1:8000/
```

### Frontend Issues

**Check console:**
- Open browser DevTools (F12)
- Check Console tab for JavaScript errors
- Check Network tab to see API requests/responses

**Test API rewrite:**
- Open DevTools Network tab
- Try to create a task
- Verify request goes to `http://127.0.0.1:8000/api/tasks`

## Performance Testing

Load test the API:

```bash
# Install locust
pip install locust

# Create locustfile.py
cat > locustfile.py << 'EOF'
from locust import HttpUser, task, between
import json

class TaskUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def get_tasks(self):
        self.client.get("/api/tasks", headers={"Authorization": f"Bearer token"})
EOF

# Run load test
locust -f locustfile.py --headless -u 10 -r 2 -t 60s
```

## Continuous Integration

For CI/CD pipelines:

```bash
#!/bin/bash
# Start backend
cd backend
python -m uvicorn src.main:app --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Run tests
cd ..
pytest TEST_INTEGRATION.md -v --tb=short --junit-xml=test-results.xml

# Kill backend
kill $BACKEND_PID

# Exit with test result code
exit $?
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'jwt'"
```bash
pip install PyJWT
```

### "Connection refused" error
- Ensure backend is running on port 8000
- Check: `uvicorn src.main:app --reload` output
- Try: `curl http://127.0.0.1:8000/`

### "401 Unauthorized" errors
- Verify token is being sent in Authorization header
- Check token hasn't expired (expires after 30 minutes)
- Test with: `curl -H "Authorization: Bearer <token>" http://127.0.0.1:8000/api/tasks`

### Database connection errors
- Check DATABASE_URL in `.env`
- Verify Neon credentials are correct
- Test connection: `psql <DATABASE_URL>`

## Test Results Examples

### Successful test run:
```
🧪 Todo App Integration Test Suite
============================================================

🔌 Testing backend connection...
✅ Backend is running and responding

📝 Testing sign up...
✅ Sign up successful
   User: test@example.com
   Token: eyJhbGciOiJIUzI1NiIsInR5...

👤 Testing get session...
✅ Session retrieved successfully
   User: test@example.com

🛡️  Testing error handling...
✅ Invalid token correctly rejected (401)
✅ Missing auth header correctly rejected (401)

📋 Testing create task...
✅ Task created successfully
   Task ID: 1
   Title: Test Task

📚 Testing get tasks...
✅ Tasks retrieved successfully
   Total tasks: 1
   - Test Task (ID: 1, Done: False)

✏️  Testing update task...
✅ Task updated successfully
   Title: Updated Task
   Done: True

🗑️  Testing delete task...
✅ Task deleted successfully

============================================================
✅ All core tests completed!
============================================================
```

## Next Steps

1. Run quick tests: `python run_quick_tests.py`
2. Run full test suite: `pytest TEST_INTEGRATION.md -v`
3. Test frontend: Start `npm run dev` and test UI manually
4. Deploy to production with confidence!

## Resources

- [FastAPI Testing Documentation](https://fastapi.tiangolo.com/advanced/testing/)
- [pytest Documentation](https://docs.pytest.org/)
- [httpx Documentation](https://www.python-httpx.org/)
- [JWT Testing Best Practices](https://auth0.com/blog/on-the-subject-of-jwt/)
