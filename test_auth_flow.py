#!/usr/bin/env python3
"""
Test end-to-end authentication flow
"""
import httpx
import json
from datetime import datetime

API_BASE = "http://127.0.0.1:8000/api"

def test_auth_flow():
    """Test signup and login flow"""
    
    with httpx.Client(base_url=API_BASE) as client:
        # Test data
        test_email = f"test.user.{int(datetime.now().timestamp())}@example.com"
        test_password = "Test123!"  # Shorter password (< 72 bytes)
        test_name = "Test User"
        
        print(f"\n{'='*60}")
        print(f"Testing Authentication Flow")
        print(f"{'='*60}")
        
        # 1. Test Sign Up
        print(f"\n[1] Testing Sign Up endpoint...")
        print(f"    Email: {test_email}")
        
        signup_data = {
            "email": test_email,
            "password": test_password,
            "name": test_name
        }
        
        try:
            resp = client.post(
                "/auth/sign-up",
                json=signup_data
            )
            signup_response = resp.json()
            
            if resp.status_code == 200:
                print(f"    ✅ Sign Up SUCCESS")
                
                # Check cookie
                if "access_token" in client.cookies:
                    print(f"       ✅ Cookie set: access_token found")
                    user = signup_response.get("user", {})
                    print(f"       User Email: {user.get('email', 'N/A')}")
                else:
                    print(f"       ❌ Cookie NOT set!")
                    return
            else:
                print(f"    ❌ Sign Up FAILED")
                print(f"       Status: {resp.status_code}")
                print(f"       Response: {json.dumps(signup_response, indent=2)}")
                return
        except Exception as e:
            print(f"    ❌ Sign Up ERROR: {e}")
            return
        
        # 2. Test Sign In
        print(f"\n[2] Testing Sign In endpoint...")
        # Clear cookies to test sign in properly
        client.cookies.clear()
        
        signin_data = {
            "email": test_email,
            "password": test_password
        }
        
        try:
            resp = client.post(
                "/auth/sign-in",
                json=signin_data
            )
            signin_response = resp.json()
            
            if resp.status_code == 200:
                print(f"    ✅ Sign In SUCCESS")
                
                if "access_token" in client.cookies:
                    print(f"       ✅ Cookie set: access_token found")
                    user = signin_response.get("user", {})
                    print(f"       User Email: {user.get('email', 'N/A')}")
                else:
                    print(f"       ❌ Cookie NOT set!")
                    return
            else:
                print(f"    ❌ Sign In FAILED")
                print(f"       Status: {resp.status_code}")
                print(f"       Response: {json.dumps(signin_response, indent=2)}")
                return
        except Exception as e:
            print(f"    ❌ Sign In ERROR: {e}")
            return
        
        # 3. Test Session Retrieval
        print(f"\n[3] Testing Session endpoint (Cookie Auth)...")
        
        try:
            resp = client.get("/auth/session")
            session_response = resp.json()
            
            if resp.status_code == 200:
                print(f"    ✅ Session Retrieval SUCCESS")
                
                if "user" in session_response:
                    user = session_response["user"]
                    print(f"       User Email: {user.get('email', 'N/A')}")
            else:
                print(f"    ❌ Session Retrieval FAILED")
                print(f"       Status: {resp.status_code}")
                print(f"       Response: {json.dumps(session_response, indent=2)}")
        except Exception as e:
            print(f"    ❌ Session Retrieval ERROR: {e}")
        
        # 4. Test Sign Out
        print(f"\n[4] Testing Sign Out endpoint...")
        
        try:
            resp = client.post("/auth/sign-out")
            if resp.status_code == 200:
                print(f"    ✅ Sign Out SUCCESS")
                
                # Check cookie is cleared (or expired)
                # Note: httpx doesn't always automatically expire cookies in the jar immediately upon receipt of set-cookie with expiry
                # But we can check if subsequent requests fail
            else:
                print(f"    ❌ Sign Out FAILED")
                print(f"       Status: {resp.status_code}")
        except Exception as e:
            print(f"    ❌ Sign Out ERROR: {e}")
        
        # 5. Verify Session Gone
        print(f"\n[5] Verifying Session Gone...")
        resp = client.get("/auth/session")
        if resp.status_code == 401:
             print(f"    ✅ Session correctly invalid (401)")
        else:
             print(f"    ❌ Session still valid! Status: {resp.status_code}")

        print(f"\n{'='*60}")
        print(f"Authentication Flow Test Completed!")
        print(f"{'='*60}\n")

if __name__ == "__main__":
    test_auth_flow()
