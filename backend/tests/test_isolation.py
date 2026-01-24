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

    # Client for User A
    async with httpx.AsyncClient(base_url=API_BASE) as client_a:
        # 1. Create User A
        email_a = f"user.a.{int(datetime.now().timestamp())}@example.com"
        resp_a = await client_a.post("/auth/sign-up", json={
            "email": email_a,
            "password": "Password123!",
            "name": "User A"
        })
        if resp_a.status_code != 200:
            print(f"❌ User A Creation Failed: {resp_a.text}")
            return
        
        # Verify cookie is set
        if "access_token" not in client_a.cookies:
            print("❌ User A has no access_token cookie!")
            return

        print(f"✅ User A Created: {email_a}")

        # 3. User A creates a task
        print(f"Testing Task Creation for User A...")
        resp_task_a = await client_a.post(
            "/tasks/",
            json={"title": "Task for User A"}
        )
        
        if resp_task_a.status_code != 201:
            print(f"❌ User A failed to create task! Status: {resp_task_a.status_code}")
            print(f"   Response: {resp_task_a.text}")
            return

        task_a_id = resp_task_a.json()["id"]
        print(f"✅ User A created task: {task_a_id}")

        # Client for User B
        async with httpx.AsyncClient(base_url=API_BASE) as client_b:
            # 2. Create User B
            email_b = f"user.b.{int(datetime.now().timestamp())}@example.com"
            resp_b = await client_b.post("/auth/sign-up", json={
                "email": email_b,
                "password": "Password123!",
                "name": "User B"
            })
            if resp_b.status_code != 200:
                print(f"❌ User B Creation Failed: {resp_b.text}")
                return
            
            print(f"✅ User B Created: {email_b}")

            # 4. User B tries to read User A's task
            resp_read = await client_b.get(f"/tasks/{task_a_id}")
            if resp_read.status_code == 404:
                print(f"✅ Isolation Verified: User B cannot see User A's task (404)")
            else:
                print(f"❌ Isolation Failed: User B saw User A's task! Status: {resp_read.status_code}")
                return

            # 5. User B tries to update User A's task
            resp_update = await client_b.patch(
                f"/tasks/{task_a_id}",
                json={"title": "Hacked by B"}
            )
            if resp_update.status_code == 404:
                print(f"✅ Isolation Verified: User B cannot update User A's task (404)")
            else:
                print(f"❌ Isolation Failed: User B updated User A's task! Status: {resp_update.status_code}")
                return

            # 6. User B tries to delete User A's task
            resp_delete = await client_b.delete(f"/tasks/{task_a_id}")
            if resp_delete.status_code == 404:
                print(f"✅ Isolation Verified: User B cannot delete User A's task (404)")
            else:
                print(f"❌ Isolation Failed: User B deleted User A's task! Status: {resp_delete.status_code}")
                return

if __name__ == "__main__":
    asyncio.run(test_isolation())