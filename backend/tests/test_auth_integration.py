import pytest
import httpx
import uuid
import time

BASE_URL = "http://localhost:8000"

def wait_for_server():
    max_retries = 10
    for i in range(max_retries):
        try:
            httpx.get(f"{BASE_URL}/")
            return True
        except:
            time.sleep(1)
    return False

def test_signup_and_session_flow():
    if not wait_for_server():
        pytest.fail("Server not reachable")
        
    client = httpx.Client(base_url=BASE_URL)
    email = f"test_{uuid.uuid4()}@example.com"
    password = "SecurePassword123!"
    name = "Test User"
    
    # 1. Sign Up
    response = client.post(
        "/api/auth/sign-up/email",
        json={"email": email, "password": password, "name": name}
    )
    if response.status_code != 200:
        print(response.text)
        
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["email"] == email
    assert data["user"]["name"] == name
    
    # Verify Cookie
    cookies = {c.name: c.value for c in response.cookies.jar}
    assert "better-auth.session_token" in cookies, "Session cookie not set"
    token = cookies["better-auth.session_token"]
    assert token is not None
    
    # 2. Get Session (Client automatically sends cookies if using same client instance?)
    # httpx.Client persists cookies by default.
    response_session = client.get("/api/auth/get-session")
    assert response_session.status_code == 200
    session_data = response_session.json()
    assert session_data["user"]["email"] == email
    # Check token from session object matches cookie
    assert session_data["session"]["token"] == token

def test_login_flow():
    if not wait_for_server():
        pytest.fail("Server not reachable")

    # Setup: Create user first
    setup_client = httpx.Client(base_url=BASE_URL)
    email = f"login_{uuid.uuid4()}@example.com"
    password = "SecurePassword123!"
    setup_client.post(
        "/api/auth/sign-up/email",
        json={"email": email, "password": password, "name": "Login User"}
    )
    
    # Test Login
    client = httpx.Client(base_url=BASE_URL)
    response = client.post(
        "/api/auth/sign-in/email",
        json={"email": email, "password": password}
    )
    assert response.status_code == 200
    
    cookies = {c.name: c.value for c in response.cookies.jar}
    assert "better-auth.session_token" in cookies
    
    # Verify session
    response_session = client.get("/api/auth/get-session")
    assert response_session.status_code == 200
    assert response_session.json()["user"]["email"] == email

def test_unauthorized():
    if not wait_for_server():
        pytest.fail("Server not reachable")
        
    client = httpx.Client(base_url=BASE_URL)
    response = client.get("/api/auth/get-session")
    assert response.status_code == 401
