from httpx import AsyncClient, ASGITransport
from src.main import app
from src.core.database import get_db, async_engine
from src.models import User, Session
from sqlmodel import select
import pytest

@pytest.mark.asyncio
async def test_auth_flow_full():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        import time
        email = f"test_auth_fix_{int(time.time())}@example.com"
        password = "password123"
        name = "Test User"

        # 1. Sign Up
        response = await ac.post("/api/auth/sign-up/email", json={
            "email": email,
            "password": password,
            "name": name
        })
        assert response.status_code == 200
        data = response.json()
        assert "user" in data
        assert "session" in data
        token = data["session"]["token"]
        # Cookie should be set
        assert "better-auth.session_token" in response.cookies

        # 2. Access Tasks (Protected) with Token in Header
        headers = {"Authorization": f"Bearer {token}"}
        response = await ac.get("/api/tasks/", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

        # 3. Access Tasks with Cookie
        ac.cookies.set("better-auth.session_token", token)
        response = await ac.get("/api/tasks/")
        assert response.status_code == 200

        # 4. Get Session
        response = await ac.get("/api/auth/get-session", headers=headers)
        assert response.status_code == 200
        assert response.json()["session"]["token"] == token

        # 6. Task CRUD Operations
        # Create Task
        task_data = {"title": "Test Task", "description": "This is a test task"}
        response = await ac.post("/api/tasks/", json=task_data, headers=headers)
        assert response.status_code == 201
        created_task = response.json()
        assert created_task["title"] == task_data["title"]
        task_id = created_task["id"]

        # Read Tasks
        response = await ac.get("/api/tasks/", headers=headers)
        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) > 0
        assert any(t["id"] == task_id for t in tasks)

        # Update Task
        update_data = {"title": "Updated Task", "is_completed": True}
        response = await ac.put(f"/api/tasks/{task_id}", json=update_data, headers=headers)
        assert response.status_code == 200
        updated_task = response.json()
        assert updated_task["title"] == "Updated Task"
        assert updated_task["is_completed"] is True

        # Delete Task
        response = await ac.delete(f"/api/tasks/{task_id}", headers=headers)
        assert response.status_code == 204

        # Verify Deletion
        response = await ac.get(f"/api/tasks/{task_id}", headers=headers)
        assert response.status_code == 404

        # 7. Sign Out
        response = await ac.post("/api/auth/sign-out", headers=headers)
        assert response.status_code == 200
        
        # 8. Access Tasks after Logout (should fail)
        response = await ac.get("/api/tasks/", headers=headers)
        assert response.status_code == 401

        # 9. Get Session after Logout (should fail)
        response = await ac.get("/api/auth/get-session", headers=headers)
        assert response.status_code == 401