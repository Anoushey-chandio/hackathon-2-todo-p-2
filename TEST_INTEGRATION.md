"""
Comprehensive Integration Tests for Todo App
Tests authentication flow and task management with proper error handling
"""

import pytest
import httpx
import json
from datetime import datetime, timezone

# Configuration
BASE_URL = "http://127.0.0.1:8000"
FRONTEND_URL = "http://localhost:3000"

# Test data
TEST_USER_1 = {
    "email": "test1@example.com",
    "password": "SecurePassword123!",
    "name": "Test User 1",
}

TEST_USER_2 = {
    "email": "test2@example.com",
    "password": "SecurePassword456!",
    "name": "Test User 2",
}

TEST_TASK = {
    "title": "Test Task",
    "description": "This is a test task",
}


class TestAuthenticationFlow:
    """Test authentication endpoints"""
    
    def test_sign_up_success(self):
        """Test successful user registration"""
        with httpx.Client() as client:
            response = client.post(
                f"{BASE_URL}/api/auth/sign-up",
                json=TEST_USER_1,
            )
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
        
        data = response.json()
        
        # Check response structure
        assert "session" in data
        assert "user" in data
        
        # Check session data
        assert "access_token" in data["session"]
        assert "token_type" in data["session"]
        assert data["session"]["token_type"] == "Bearer"
        
        # Check user data
        user = data["user"]
        assert user["email"] == TEST_USER_1["email"]
        assert user["name"] == TEST_USER_1["name"]
        assert "id" in user
        assert "createdAt" in user
        
        # Store token for next test
        return data["session"]["access_token"]
    
    def test_sign_up_duplicate_email(self):
        """Test sign up with existing email"""
        with httpx.Client() as client:
            # First registration
            client.post(
                f"{BASE_URL}/api/auth/sign-up",
                json=TEST_USER_1,
            )
            
            # Try to register with same email
            response = client.post(
                f"{BASE_URL}/api/auth/sign-up",
                json=TEST_USER_1,
            )
        
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"
        data = response.json()
        assert "already exists" in data.get("detail", "").lower()
    
    def test_sign_in_success(self):
        """Test successful login"""
        with httpx.Client() as client:
            # Sign up first
            signup_response = client.post(
                f"{BASE_URL}/api/auth/sign-up",
                json=TEST_USER_2,
            )
            assert signup_response.status_code == 200
            
            # Then sign in
            login_response = client.post(
                f"{BASE_URL}/api/auth/sign-in",
                json={
                    "email": TEST_USER_2["email"],
                    "password": TEST_USER_2["password"],
                },
            )
        
        assert login_response.status_code == 200
        data = login_response.json()
        
        assert "session" in data
        assert "access_token" in data["session"]
        assert data["user"]["email"] == TEST_USER_2["email"]
    
    def test_sign_in_wrong_password(self):
        """Test login with wrong password"""
        with httpx.Client() as client:
            # Sign up first
            client.post(
                f"{BASE_URL}/api/auth/sign-up",
                json=TEST_USER_1,
            )
            
            # Try to sign in with wrong password
            response = client.post(
                f"{BASE_URL}/api/auth/sign-in",
                json={
                    "email": TEST_USER_1["email"],
                    "password": "WrongPassword123!",
                },
            )
        
        assert response.status_code == 401
        data = response.json()
        assert "Invalid email or password" in data.get("detail", "")
    
    def test_sign_in_nonexistent_user(self):
        """Test login with non-existent email"""
        with httpx.Client() as client:
            response = client.post(
                f"{BASE_URL}/api/auth/sign-in",
                json={
                    "email": "nonexistent@example.com",
                    "password": "SomePassword123!",
                },
            )
        
        assert response.status_code == 401
    
    def test_get_session_success(self):
        """Test retrieving session info"""
        with httpx.Client() as client:
            # Sign up
            signup_response = client.post(
                f"{BASE_URL}/api/auth/sign-up",
                json=TEST_USER_1,
            )
            token = signup_response.json()["session"]["access_token"]
            
            # Get session
            response = client.get(
                f"{BASE_URL}/api/auth/session",
                headers={"Authorization": f"Bearer {token}"},
            )
        
        assert response.status_code == 200
        data = response.json()
        assert data["user"]["email"] == TEST_USER_1["email"]
    
    def test_get_session_invalid_token(self):
        """Test session retrieval with invalid token"""
        with httpx.Client() as client:
            response = client.get(
                f"{BASE_URL}/api/auth/session",
                headers={"Authorization": "Bearer invalid.token.here"},
            )
        
        assert response.status_code == 401
    
    def test_get_session_missing_auth_header(self):
        """Test session retrieval without auth header"""
        with httpx.Client() as client:
            response = client.get(f"{BASE_URL}/api/auth/session")
        
        assert response.status_code == 401
    
    def test_sign_out_success(self):
        """Test sign out"""
        with httpx.Client() as client:
            response = client.post(f"{BASE_URL}/api/auth/sign-out")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True


class TestTaskManagement:
    """Test task CRUD operations"""
    
    @classmethod
    def setup_class(cls):
        """Set up test user and get auth token"""
        with httpx.Client() as client:
            response = client.post(
                f"{BASE_URL}/api/auth/sign-up",
                json=TEST_USER_1,
            )
            cls.token = response.json()["session"]["access_token"]
            cls.user_id = response.json()["user"]["id"]
    
    def test_create_task_success(self):
        """Test successful task creation"""
        with httpx.Client() as client:
            response = client.post(
                f"{BASE_URL}/api/tasks",
                json=TEST_TASK,
                headers={"Authorization": f"Bearer {self.token}"},
            )
        
        assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.text}"
        data = response.json()
        
        # Check response structure
        assert "id" in data
        assert data["title"] == TEST_TASK["title"]
        assert data["description"] == TEST_TASK["description"]
        assert data["done"] is False
        assert data["userId"] == int(self.user_id)
        
        return data["id"]
    
    def test_create_task_missing_title(self):
        """Test task creation without title"""
        with httpx.Client() as client:
            response = client.post(
                f"{BASE_URL}/api/tasks",
                json={"description": "Missing title"},
                headers={"Authorization": f"Bearer {self.token}"},
            )
        
        assert response.status_code in [400, 422], f"Expected 400/422, got {response.status_code}"
    
    def test_create_task_unauthorized(self):
        """Test task creation without auth"""
        with httpx.Client() as client:
            response = client.post(
                f"{BASE_URL}/api/tasks",
                json=TEST_TASK,
            )
        
        assert response.status_code == 401
    
    def test_get_tasks_success(self):
        """Test retrieving all tasks"""
        with httpx.Client() as client:
            response = client.get(
                f"{BASE_URL}/api/tasks",
                headers={"Authorization": f"Bearer {self.token}"},
            )
        
        assert response.status_code == 200
        tasks = response.json()
        
        assert isinstance(tasks, list)
        if len(tasks) > 0:
            # Check task structure
            task = tasks[0]
            assert "id" in task
            assert "title" in task
            assert "userId" in task
    
    def test_get_tasks_unauthorized(self):
        """Test getting tasks without auth"""
        with httpx.Client() as client:
            response = client.get(f"{BASE_URL}/api/tasks")
        
        assert response.status_code == 401
    
    def test_get_task_by_id(self):
        """Test retrieving specific task"""
        with httpx.Client() as client:
            # Create task
            create_response = client.post(
                f"{BASE_URL}/api/tasks",
                json=TEST_TASK,
                headers={"Authorization": f"Bearer {self.token}"},
            )
            task_id = create_response.json()["id"]
            
            # Get task
            response = client.get(
                f"{BASE_URL}/api/tasks/{task_id}",
                headers={"Authorization": f"Bearer {self.token}"},
            )
        
        assert response.status_code == 200
        task = response.json()
        assert task["id"] == task_id
        assert task["title"] == TEST_TASK["title"]
    
    def test_get_task_not_found(self):
        """Test retrieving non-existent task"""
        with httpx.Client() as client:
            response = client.get(
                f"{BASE_URL}/api/tasks/99999",
                headers={"Authorization": f"Bearer {self.token}"},
            )
        
        assert response.status_code == 404
    
    def test_update_task_success(self):
        """Test updating task"""
        with httpx.Client() as client:
            # Create task
            create_response = client.post(
                f"{BASE_URL}/api/tasks",
                json=TEST_TASK,
                headers={"Authorization": f"Bearer {self.token}"},
            )
            task_id = create_response.json()["id"]
            
            # Update task
            update_response = client.put(
                f"{BASE_URL}/api/tasks/{task_id}",
                json={
                    "title": "Updated Title",
                    "done": True,
                },
                headers={"Authorization": f"Bearer {self.token}"},
            )
        
        assert update_response.status_code == 200
        updated_task = update_response.json()
        assert updated_task["title"] == "Updated Title"
        assert updated_task["done"] is True
    
    def test_update_task_unauthorized(self):
        """Test updating task without auth"""
        with httpx.Client() as client:
            # Create task with token
            create_response = client.post(
                f"{BASE_URL}/api/tasks",
                json=TEST_TASK,
                headers={"Authorization": f"Bearer {self.token}"},
            )
            task_id = create_response.json()["id"]
            
            # Try to update without auth
            response = client.put(
                f"{BASE_URL}/api/tasks/{task_id}",
                json={"done": True},
            )
        
        assert response.status_code == 401
    
    def test_delete_task_success(self):
        """Test deleting task"""
        with httpx.Client() as client:
            # Create task
            create_response = client.post(
                f"{BASE_URL}/api/tasks",
                json=TEST_TASK,
                headers={"Authorization": f"Bearer {self.token}"},
            )
            task_id = create_response.json()["id"]
            
            # Delete task
            response = client.delete(
                f"{BASE_URL}/api/tasks/{task_id}",
                headers={"Authorization": f"Bearer {self.token}"},
            )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        
        # Verify deletion
        get_response = client.get(
            f"{BASE_URL}/api/tasks/{task_id}",
            headers={"Authorization": f"Bearer {self.token}"},
        )
        assert get_response.status_code == 404
    
    def test_delete_task_not_found(self):
        """Test deleting non-existent task"""
        with httpx.Client() as client:
            response = client.delete(
                f"{BASE_URL}/api/tasks/99999",
                headers={"Authorization": f"Bearer {self.token}"},
            )
        
        assert response.status_code == 404


class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_malformed_json(self):
        """Test endpoint with malformed JSON"""
        with httpx.Client() as client:
            response = client.post(
                f"{BASE_URL}/api/auth/sign-up",
                content="invalid json",
                headers={"Content-Type": "application/json"},
            )
        
        assert response.status_code in [400, 422]
    
    def test_invalid_email_format(self):
        """Test sign up with invalid email"""
        with httpx.Client() as client:
            response = client.post(
                f"{BASE_URL}/api/auth/sign-up",
                json={
                    "email": "not-an-email",
                    "password": "Password123!",
                    "name": "Test",
                },
            )
        
        assert response.status_code in [400, 422]
    
    def test_weak_password(self):
        """Test sign up with weak password"""
        with httpx.Client() as client:
            response = client.post(
                f"{BASE_URL}/api/auth/sign-up",
                json={
                    "email": "test@example.com",
                    "password": "123",  # Too weak
                    "name": "Test",
                },
            )
        
        # Should still allow (no password strength requirement), but 200 expected
        assert response.status_code in [200, 400, 422]
    
    def test_missing_required_field(self):
        """Test sign up with missing required field"""
        with httpx.Client() as client:
            response = client.post(
                f"{BASE_URL}/api/auth/sign-up",
                json={
                    "email": "test@example.com",
                    # Missing password
                    "name": "Test",
                },
            )
        
        assert response.status_code in [400, 422]
    
    def test_expired_token_handling(self):
        """Test request with tampered token"""
        tampered_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.invalid"
        
        with httpx.Client() as client:
            response = client.get(
                f"{BASE_URL}/api/auth/session",
                headers={"Authorization": f"Bearer {tampered_token}"},
            )
        
        assert response.status_code == 401


class TestIntegration:
    """Integration tests for complete user workflows"""
    
    def test_complete_signup_create_task_workflow(self):
        """Test complete workflow: sign up, create task, get task"""
        with httpx.Client() as client:
            # 1. Sign up
            signup_response = client.post(
                f"{BASE_URL}/api/auth/sign-up",
                json={
                    "email": "integration_test@example.com",
                    "password": "IntegrationTest123!",
                    "name": "Integration Test User",
                },
            )
            assert signup_response.status_code == 200
            token = signup_response.json()["session"]["access_token"]
            user_id = signup_response.json()["user"]["id"]
            
            # 2. Create task
            create_response = client.post(
                f"{BASE_URL}/api/tasks",
                json={
                    "title": "Integration Test Task",
                    "description": "Created during integration test",
                },
                headers={"Authorization": f"Bearer {token}"},
            )
            assert create_response.status_code == 201
            task_id = create_response.json()["id"]
            
            # 3. Get all tasks
            get_response = client.get(
                f"{BASE_URL}/api/tasks",
                headers={"Authorization": f"Bearer {token}"},
            )
            assert get_response.status_code == 200
            tasks = get_response.json()
            assert len(tasks) > 0
            assert any(t["id"] == task_id for t in tasks)
            
            # 4. Update task
            update_response = client.put(
                f"{BASE_URL}/api/tasks/{task_id}",
                json={"done": True},
                headers={"Authorization": f"Bearer {token}"},
            )
            assert update_response.status_code == 200
            assert update_response.json()["done"] is True
            
            # 5. Delete task
            delete_response = client.delete(
                f"{BASE_URL}/api/tasks/{task_id}",
                headers={"Authorization": f"Bearer {token}"},
            )
            assert delete_response.status_code == 200
    
    def test_multiple_users_isolated_tasks(self):
        """Test that tasks are isolated per user"""
        with httpx.Client() as client:
            # Create user 1 and their task
            user1_response = client.post(
                f"{BASE_URL}/api/auth/sign-up",
                json={
                    "email": "user1_isolation@example.com",
                    "password": "Password123!",
                    "name": "User 1",
                },
            )
            user1_token = user1_response.json()["session"]["access_token"]
            
            task1_response = client.post(
                f"{BASE_URL}/api/tasks",
                json={"title": "User 1 Task", "description": "Only for user 1"},
                headers={"Authorization": f"Bearer {user1_token}"},
            )
            task1_id = task1_response.json()["id"]
            
            # Create user 2 and their task
            user2_response = client.post(
                f"{BASE_URL}/api/auth/sign-up",
                json={
                    "email": "user2_isolation@example.com",
                    "password": "Password123!",
                    "name": "User 2",
                },
            )
            user2_token = user2_response.json()["session"]["access_token"]
            
            task2_response = client.post(
                f"{BASE_URL}/api/tasks",
                json={"title": "User 2 Task", "description": "Only for user 2"},
                headers={"Authorization": f"Bearer {user2_token}"},
            )
            task2_id = task2_response.json()["id"]
            
            # Verify user 1 only sees their task
            user1_tasks = client.get(
                f"{BASE_URL}/api/tasks",
                headers={"Authorization": f"Bearer {user1_token}"},
            ).json()
            user1_task_ids = [t["id"] for t in user1_tasks]
            assert task1_id in user1_task_ids
            assert task2_id not in user1_task_ids
            
            # Verify user 2 only sees their task
            user2_tasks = client.get(
                f"{BASE_URL}/api/tasks",
                headers={"Authorization": f"Bearer {user2_token}"},
            ).json()
            user2_task_ids = [t["id"] for t in user2_tasks]
            assert task2_id in user2_task_ids
            assert task1_id not in user2_task_ids


# Run with: pytest test_integration.py -v
if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
