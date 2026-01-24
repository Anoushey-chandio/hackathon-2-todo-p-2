"""
Quick integration test runner - verifies core functionality
Run after starting backend: uvicorn src.main:app --reload
"""

import httpx
import sys
import time

BASE_URL = "http://127.0.0.1:8000"

def test_backend_connection():
    """Test if backend is running"""
    print("🔌 Testing backend connection...")
    try:
        response = httpx.get(f"{BASE_URL}/", timeout=2)
        assert response.status_code == 200
        print("✅ Backend is running and responding")
        return True
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print(f"   Make sure backend is running: uvicorn src.main:app --reload")
        return False

def test_sign_up():
    """Test user registration"""
    print("\n📝 Testing sign up...")
    timestamp = int(time.time())
    email = f"test_{timestamp}@example.com"
    try:
        with httpx.Client() as client:
            response = client.post(
                f"{BASE_URL}/api/auth/sign-up",
                json={
                    "email": email,
                    "password": "TestPassword123!",
                    "name": "Test User",
                },
                timeout=15,
            )
        
        if response.status_code != 200:
            print(f"❌ Sign up failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
        
        cookies = response.cookies
        token = cookies.get("access_token")
        
        if not token:
            print("❌ No access_token cookie in response")
            return None
        
        data = response.json()
        print(f"✅ Sign up successful")
        print(f"   User: {data['user']['email']}")
        print(f"   Token (Cookie): {token[:50]}...")
        return cookies
    except Exception as e:
        print(f"❌ Sign up error: {e}")
        return None

def test_get_session(cookies):
    """Test session retrieval"""
    print("\n👤 Testing get session...")
    try:
        with httpx.Client(cookies=cookies) as client:
            response = client.get(
                f"{BASE_URL}/api/auth/session",
                timeout=15,
            )
        
        if response.status_code != 200:
            print(f"❌ Get session failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        data = response.json()
        print(f"✅ Session retrieved successfully")
        print(f"   User: {data['user']['email']}")
        return True
    except Exception as e:
        print(f"❌ Get session error: {e}")
        return False

def test_create_task(cookies):
    """Test task creation"""
    print("\n📋 Testing create task...")
    try:
        with httpx.Client(cookies=cookies) as client:
            response = client.post(
                f"{BASE_URL}/api/tasks/",
                json={
                    "title": "Test Task",
                    "description": "This is a test task",
                },
                timeout=15,
            )
        
        if response.status_code != 201:
            print(f"❌ Create task failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
        
        data = response.json()
        task_id = data.get("id")
        print(f"✅ Task created successfully")
        print(f"   Task ID: {task_id}")
        print(f"   Title: {data['title']}")
        return task_id
    except Exception as e:
        print(f"❌ Create task error: {e}")
        return None

def test_get_tasks(cookies):
    """Test retrieving tasks"""
    print("\n📚 Testing get tasks...")
    try:
        with httpx.Client(cookies=cookies) as client:
            response = client.get(
                f"{BASE_URL}/api/tasks/",
                timeout=15,
            )
        
        if response.status_code != 200:
            print(f"❌ Get tasks failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        tasks = response.json()
        print(f"✅ Tasks retrieved successfully")
        print(f"   Total tasks: {len(tasks)}")
        for task in tasks[:3]:  # Show first 3
            print(f"   - {task['title']} (ID: {task['id']}, Done: {task['is_completed']})")
        return True
    except Exception as e:
        print(f"❌ Get tasks error: {e}")
        return False

def test_update_task(cookies, task_id):
    """Test task update"""
    print("\n✏️  Testing update task...")
    try:
        with httpx.Client(cookies=cookies) as client:
            response = client.patch(
                f"{BASE_URL}/api/tasks/{task_id}",
                json={"is_completed": True, "title": "Updated Task"},
                timeout=15,
            )
        
        if response.status_code != 200:
            print(f"❌ Update task failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        data = response.json()
        print(f"✅ Task updated successfully")
        print(f"   Title: {data['title']}")
        print(f"   Done: {data['is_completed']}")
        return True
    except Exception as e:
        print(f"❌ Update task error: {e}")
        return False

def test_delete_task(cookies, task_id):
    """Test task deletion"""
    print("\n🗑️  Testing delete task...")
    try:
        with httpx.Client(cookies=cookies) as client:
            response = client.delete(
                f"{BASE_URL}/api/tasks/{task_id}",
                timeout=15,
            )
        
        if response.status_code not in [200, 204]:
            print(f"❌ Delete task failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        print(f"✅ Task deleted successfully")
        return True
    except Exception as e:
        print(f"❌ Delete task error: {e}")
        return None

def test_auth_error_handling(cookies):
    """Test authentication error handling"""
    print("\n🛡️  Testing error handling...")
    
    # Test with invalid token (modify cookie)
    invalid_cookies = httpx.Cookies()
    invalid_cookies.set("access_token", "invalid_token")
    
    try:
        with httpx.Client(cookies=invalid_cookies) as client:
            response = client.get(
                f"{BASE_URL}/api/tasks/",
                timeout=15,
            )
        
        if response.status_code == 401:
            print(f"✅ Invalid token correctly rejected (401)")
        else:
            print(f"⚠️  Unexpected status code for invalid token: {response.status_code}")
    except Exception as e:
        print(f"❌ Error test failed: {e}")
        return False
    
    # Test without auth cookie
    try:
        with httpx.Client() as client:
            response = client.get(
                f"{BASE_URL}/api/tasks/",
                timeout=15,
            )
        
        if response.status_code == 401:
            print(f"✅ Missing auth cookie correctly rejected (401)")
        else:
            print(f"⚠️  Unexpected status code for missing auth: {response.status_code}")
    except Exception as e:
        print(f"❌ Error test failed: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 Todo App Integration Test Suite")
    print("=" * 60)
    
    # Test 1: Backend connection
    if not test_backend_connection():
        sys.exit(1)
    
    # Test 2: Sign up
    cookies = test_sign_up()
    if not cookies:
        print("\n❌ Cannot continue without cookies")
        sys.exit(1)
    
    # Test 3: Get session
    if not test_get_session(cookies):
        print("\n⚠️  Session test failed, continuing...")
    
    # Test 4: Error handling
    if not test_auth_error_handling(cookies):
        print("\n⚠️  Error handling test failed")
    
    # Test 5: Create task
    task_id = test_create_task(cookies)
    if not task_id:
        print("\n⚠️  Cannot test other task operations")
    else:
        # Test 6: Get tasks
        test_get_tasks(cookies)
        
        # Test 7: Update task
        test_update_task(cookies, task_id)
        
        # Test 8: Delete task
        test_delete_task(cookies, task_id)
    
    print("\n" + "=" * 60)
    print("✅ All core tests completed!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Start backend: uvicorn src.main:app --reload")
    print("2. Start frontend: npm run dev")
    print("3. Open http://localhost:3000 in browser")
    print("4. Test signup/login flows in the UI")
    print("\nFor detailed tests, run:")
    print("pip install pytest httpx")
    print("pytest TEST_INTEGRATION.md -v")

if __name__ == "__main__":
    main()
