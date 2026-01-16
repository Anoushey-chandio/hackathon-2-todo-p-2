"""
Comprehensive integration test for the Todo App backend.
Tests auth flow, task creation, and full end-to-end workflow.
"""

import pytest
import httpx
import uuid
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

def wait_for_server(max_retries: int = 30, retry_delay: float = 1):
    """Wait for the server to be available."""
    for i in range(max_retries):
        try:
            httpx.get(f"{BASE_URL}/", timeout=2.0)
            print(f"✓ Server is ready (attempt {i+1})")
            return True
        except Exception as e:
            if i < max_retries - 1:
                time.sleep(retry_delay)
            else:
                print(f"✗ Server not reachable after {max_retries} attempts: {e}")
    return False


class TestAuthFlow:
    """Test user authentication flows."""

    @pytest.fixture
    def client(self):
        """Create an HTTP client that persists cookies."""
        return httpx.Client(base_url=BASE_URL)

    @pytest.fixture
    def unique_email(self):
        """Generate a unique email for testing."""
        return f"test_{uuid.uuid4().hex[:8]}@example.com"

    def test_server_health(self, client):
        """Test that the server is running."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data

    def test_signup_success(self, client, unique_email):
        """Test successful user signup."""
        password = "SecurePassword123!"
        name = "Test User"

        response = client.post(
            "/api/auth/sign-up/email",
            json={"email": unique_email, "password": password, "name": name}
        )

        assert response.status_code == 200, f"Signup failed: {response.text}"
        data = response.json()

        # Verify response structure
        assert "user" in data
        assert "session" in data
        assert data["user"]["email"] == unique_email
        assert data["user"]["name"] == name
        assert data["user"]["emailVerified"] is False
        assert "token" in data["session"]
        assert "expiresAt" in data["session"]

        # Verify session cookie is set
        cookies = {c.name: c.value for c in response.cookies.jar}
        assert "better-auth.session_token" in cookies, "Session cookie not set"

    def test_signup_duplicate_email(self, client, unique_email):
        """Test that duplicate email signup fails."""
        password = "SecurePassword123!"

        # First signup
        response1 = client.post(
            "/api/auth/sign-up/email",
            json={"email": unique_email, "password": password, "name": "User 1"}
        )
        assert response1.status_code == 200

        # Duplicate signup
        response2 = client.post(
            "/api/auth/sign-up/email",
            json={"email": unique_email, "password": password, "name": "User 2"}
        )
        assert response2.status_code == 400
        data = response2.json()
        assert "Email already registered" in data["detail"]

    def test_login_success(self, client, unique_email):
        """Test successful user login."""
        password = "SecurePassword123!"
        name = "Login Test User"

        # Signup first
        client.post(
            "/api/auth/sign-up/email",
            json={"email": unique_email, "password": password, "name": name}
        )

        # Clear cookies by creating a new client
        login_client = httpx.Client(base_url=BASE_URL)

        # Login
        response = login_client.post(
            "/api/auth/sign-in/email",
            json={"email": unique_email, "password": password}
        )

        assert response.status_code == 200, f"Login failed: {response.text}"
        data = response.json()
        assert "user" in data
        assert "session" in data
        assert data["user"]["email"] == unique_email

        # Verify session cookie
        cookies = {c.name: c.value for c in response.cookies.jar}
        assert "better-auth.session_token" in cookies

    def test_login_wrong_password(self, client, unique_email):
        """Test login with wrong password fails."""
        password = "SecurePassword123!"

        # Signup
        client.post(
            "/api/auth/sign-up/email",
            json={"email": unique_email, "password": password, "name": "User"}
        )

        # Try to login with wrong password
        login_client = httpx.Client(base_url=BASE_URL)
        response = login_client.post(
            "/api/auth/sign-in/email",
            json={"email": unique_email, "password": "WrongPassword123!"}
        )

        assert response.status_code == 401
        data = response.json()
        assert "detail" in data

    def test_login_nonexistent_email(self, client):
        """Test login with non-existent email fails."""
        response = client.post(
            "/api/auth/sign-in/email",
            json={"email": "nonexistent@example.com", "password": "password"}
        )

        assert response.status_code == 401

    def test_get_session_authenticated(self, client, unique_email):
        """Test getting session for authenticated user."""
        password = "SecurePassword123!"

        # Signup
        signup_response = client.post(
            "/api/auth/sign-up/email",
            json={"email": unique_email, "password": password, "name": "Session Test"}
        )
        assert signup_response.status_code == 200

        # Get session (cookies are persisted by client)
        response = client.get("/api/auth/get-session")
        assert response.status_code == 200
        data = response.json()
        assert data["user"]["email"] == unique_email
        assert "token" in data["session"]

    def test_get_session_unauthenticated(self):
        """Test getting session without authentication fails."""
        client = httpx.Client(base_url=BASE_URL)
        response = client.get("/api/auth/get-session")
        assert response.status_code == 401


class TestTaskOperations:
    """Test task CRUD operations."""

    @pytest.fixture
    def authenticated_client(self):
        """Create an authenticated client."""
        client = httpx.Client(base_url=BASE_URL)
        email = f"task_user_{uuid.uuid4().hex[:8]}@example.com"
        password = "TaskPassword123!"

        client.post(
            "/api/auth/sign-up/email",
            json={"email": email, "password": password, "name": "Task User"}
        )
        return client

    def test_create_task(self, authenticated_client):
        """Test creating a task."""
        response = authenticated_client.post(
            "/api/tasks/",
            json={"title": "Test Task", "description": "A test task", "isCompleted": False}
        )

        assert response.status_code == 201, f"Create failed: {response.text}"
        data = response.json()
        assert data["title"] == "Test Task"
        assert data["description"] == "A test task"
        assert data["isCompleted"] is False
        assert "id" in data
        assert "createdAt" in data
        assert "updatedAt" in data
        assert "userId" in data

    def test_create_task_minimal(self, authenticated_client):
        """Test creating a task with minimal fields."""
        response = authenticated_client.post(
            "/api/tasks/",
            json={"title": "Minimal Task"}
        )

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Minimal Task"
        assert data["isCompleted"] is False
        assert data["description"] is None

    def test_get_tasks_empty(self, authenticated_client):
        """Test getting tasks when none exist."""
        response = authenticated_client.get("/api/tasks/")
        assert response.status_code == 200
        data = response.json()
        assert data == []

    def test_get_tasks_multiple(self, authenticated_client):
        """Test getting multiple tasks."""
        # Create tasks
        titles = ["Task 1", "Task 2", "Task 3"]
        for title in titles:
            authenticated_client.post(
                "/api/tasks/",
                json={"title": title}
            )

        # Get tasks
        response = authenticated_client.get("/api/tasks/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        retrieved_titles = [t["title"] for t in data]
        for title in titles:
            assert title in retrieved_titles

    def test_get_task_by_id(self, authenticated_client):
        """Test getting a specific task by ID."""
        # Create task
        create_response = authenticated_client.post(
            "/api/tasks/",
            json={"title": "Get Me"}
        )
        task_id = create_response.json()["id"]

        # Get task
        response = authenticated_client.get(f"/api/tasks/{task_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == "Get Me"

    def test_get_task_not_found(self, authenticated_client):
        """Test getting a non-existent task."""
        response = authenticated_client.get("/api/tasks/99999")
        assert response.status_code == 404

    def test_update_task(self, authenticated_client):
        """Test updating a task."""
        # Create task
        create_response = authenticated_client.post(
            "/api/tasks/",
            json={"title": "Original Title", "description": "Original"}
        )
        task_id = create_response.json()["id"]

        # Update task
        response = authenticated_client.put(
            f"/api/tasks/{task_id}",
            json={"title": "Updated Title", "description": "Updated"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["description"] == "Updated"
        assert data["id"] == task_id

    def test_update_task_partial(self, authenticated_client):
        """Test partial task update."""
        # Create task
        create_response = authenticated_client.post(
            "/api/tasks/",
            json={"title": "Original", "description": "Desc"}
        )
        task_id = create_response.json()["id"]

        # Partial update
        response = authenticated_client.put(
            f"/api/tasks/{task_id}",
            json={"title": "New Title"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "New Title"
        # Description should remain unchanged if not in update

    def test_toggle_task_completion(self, authenticated_client):
        """Test toggling task completion status."""
        # Create task
        create_response = authenticated_client.post(
            "/api/tasks/",
            json={"title": "Complete Me", "isCompleted": False}
        )
        task_id = create_response.json()["id"]

        # Toggle completion (should become True)
        response = authenticated_client.patch(f"/api/tasks/{task_id}/complete")
        assert response.status_code == 200
        data = response.json()
        assert data["isCompleted"] is True

        # Toggle again (should become False)
        response = authenticated_client.patch(f"/api/tasks/{task_id}/complete")
        assert response.status_code == 200
        data = response.json()
        assert data["isCompleted"] is False

    def test_delete_task(self, authenticated_client):
        """Test deleting a task."""
        # Create task
        create_response = authenticated_client.post(
            "/api/tasks/",
            json={"title": "Delete Me"}
        )
        task_id = create_response.json()["id"]

        # Delete task
        response = authenticated_client.delete(f"/api/tasks/{task_id}")
        assert response.status_code == 204

        # Verify task is deleted
        response = authenticated_client.get(f"/api/tasks/{task_id}")
        assert response.status_code == 404

    def test_task_isolation(self):
        """Test that users can only see their own tasks."""
        # Create two users
        user1_client = httpx.Client(base_url=BASE_URL)
        user2_client = httpx.Client(base_url=BASE_URL)

        user1_email = f"user1_{uuid.uuid4().hex[:8]}@example.com"
        user2_email = f"user2_{uuid.uuid4().hex[:8]}@example.com"
        password = "Password123!"

        # Signup users
        user1_client.post(
            "/api/auth/sign-up/email",
            json={"email": user1_email, "password": password, "name": "User 1"}
        )
        user2_client.post(
            "/api/auth/sign-up/email",
            json={"email": user2_email, "password": password, "name": "User 2"}
        )

        # User 1 creates tasks
        user1_client.post("/api/tasks/", json={"title": "User 1 Task 1"})
        user1_client.post("/api/tasks/", json={"title": "User 1 Task 2"})

        # User 2 creates tasks
        user2_client.post("/api/tasks/", json={"title": "User 2 Task 1"})

        # User 1 should see only their tasks
        response = user1_client.get("/api/tasks/")
        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 2
        assert all(t["title"].startswith("User 1") for t in tasks)

        # User 2 should see only their tasks
        response = user2_client.get("/api/tasks/")
        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 1
        assert tasks[0]["title"] == "User 2 Task 1"

    def test_tasks_require_authentication(self):
        """Test that task endpoints require authentication."""
        client = httpx.Client(base_url=BASE_URL)

        # Try to create task without auth
        response = client.post("/api/tasks/", json={"title": "Test"})
        assert response.status_code == 401

        # Try to get tasks without auth
        response = client.get("/api/tasks/")
        assert response.status_code == 401


class TestEndToEndWorkflow:
    """Test complete user workflows."""

    def test_signup_create_tasks_login(self):
        """Test complete workflow: signup, create tasks, logout, login, view tasks."""
        client = httpx.Client(base_url=BASE_URL)
        email = f"workflow_{uuid.uuid4().hex[:8]}@example.com"
        password = "WorkflowPass123!"
        name = "Workflow User"

        # Signup
        signup_response = client.post(
            "/api/auth/sign-up/email",
            json={"email": email, "password": password, "name": name}
        )
        assert signup_response.status_code == 200

        # Create tasks
        task_ids = []
        for i in range(3):
            response = client.post(
                "/api/tasks/",
                json={"title": f"Task {i+1}", "description": f"Description {i+1}"}
            )
            assert response.status_code == 201
            task_ids.append(response.json()["id"])

        # Complete first task
        response = client.patch(f"/api/tasks/{task_ids[0]}/complete")
        assert response.status_code == 200
        assert response.json()["isCompleted"] is True

        # Create new client (simulates browser session loss)
        new_client = httpx.Client(base_url=BASE_URL)

        # Login
        login_response = new_client.post(
            "/api/auth/sign-in/email",
            json={"email": email, "password": password}
        )
        assert login_response.status_code == 200

        # Verify tasks are still there
        response = new_client.get("/api/tasks/")
        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 3

        # Verify first task is completed
        completed_tasks = [t for t in tasks if t["isCompleted"]]
        assert len(completed_tasks) == 1


# Run with: pytest backend/tests/test_full_integration.py -v
