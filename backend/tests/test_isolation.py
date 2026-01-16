import asyncio
import sys
import os
import httpx
from datetime import datetime

# Add backend to sys.path
sys.path.append(os.path.join(os.getcwd(), "backend"))

API_BASE = "http://127.0.0.1:8000/api"

async def test_isolation():
    print(f"\n{'='*60}")
    print(f"Testing Data Isolation")
    print(f"{'='*60}")

    async with httpx.AsyncClient() as client:
        # 1. Create User A
        email_a = f"user.a.{int(datetime.now().timestamp())}@example.com"
        resp_a = await client.post(f"{API_BASE}/auth/sign-up", json={
            "email": email_a,
            "password": "Password123!",
            "name": "User A"
        })
        token_a = resp_a.json()["session"]["access_token"]
        print(f"✅ User A Created: {email_a}")

        # 2. Create User B
        email_b = f"user.b.{int(datetime.now().timestamp())}@example.com"
        resp_b = await client.post(f"{API_BASE}/auth/sign-up", json={
            "email": email_b,
            "password": "Password123!",
            "name": "User B"
        })
        token_b = resp_b.json()["session"]["access_token"]
        print(f"✅ User B Created: {email_b}")

        # 3. User A creates a task
        print(f"Testing Task Creation for User A...")
        resp_task_a = await client.post(
            f"{API_BASE}/tasks/",
            json={"title": "Task for User A"},
            headers={"Authorization": f"Bearer {token_a}"}
        )
        
        if resp_task_a.status_code != 201:
            print(f"❌ User A failed to create task! Status: {resp_task_a.status_code}")
            print(f"   Response: {resp_task_a.text}")
            return

        task_a_id = resp_task_a.json()["id"]
        print(f"✅ User A created task: {task_a_id}")

        # 4. User B tries to read User A's task
        resp_read = await client.get(
            f"{API_BASE}/tasks/{task_a_id}",
            headers={"Authorization": f"Bearer {token_b}"}
        )
        if resp_read.status_code == 404:
            print(f"✅ Isolation Verified: User B cannot see User A's task (404)")
        else:
            print(f"❌ Isolation Failed: User B saw User A's task! Status: {resp_read.status_code}")
            return

        # 5. User B tries to update User A's task
        resp_update = await client.patch(
            f"{API_BASE}/tasks/{task_a_id}",
            json={"title": "Hacked by B"},
            headers={"Authorization": f"Bearer {token_b}"}
        )
        if resp_update.status_code == 404:
            print(f"✅ Isolation Verified: User B cannot update User A's task (404)")
        else:
            print(f"❌ Isolation Failed: User B updated User A's task! Status: {resp_update.status_code}")
            return

        # 6. User B tries to delete User A's task
        resp_delete = await client.delete(
            f"{API_BASE}/tasks/{task_a_id}",
            headers={"Authorization": f"Bearer {token_b}"}
        )
        if resp_delete.status_code == 404:
            print(f"✅ Isolation Verified: User B cannot delete User A's task (404)")
        else:
            print(f"❌ Isolation Failed: User B deleted User A's task! Status: {resp_delete.status_code}")
            return

if __name__ == "__main__":
    asyncio.run(test_isolation())