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
    
    with httpx.Client() as client:
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
        print(f"    Name: {test_name}")
        
        signup_data = {
            "email": test_email,
            "password": test_password,
            "name": test_name
        }
        
        try:
            resp = client.post(
                f"{API_BASE}/auth/sign-up",
                json=signup_data,
                headers={"Content-Type": "application/json"}
            )
            signup_response = resp.json()
            
            if resp.status_code == 200:
                print(f"    ✅ Sign Up SUCCESS")
                print(f"       Status: {resp.status_code}")
                
                # Extract token and user
                if "session" in signup_response and "access_token" in signup_response["session"]:
                    token = signup_response["session"]["access_token"]
                    user = signup_response.get("user", {})
                    
                    print(f"       Token: {token[:30]}...")
                    print(f"       User ID: {user.get('id', 'N/A')}")
                    print(f"       User Email: {user.get('email', 'N/A')}")
                else:
                    print(f"       ⚠️  Response missing session/token")
                    print(f"       Response: {json.dumps(signup_response, indent=2)}")
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
        print(f"    Email: {test_email}")
        
        signin_data = {
            "email": test_email,
            "password": test_password
        }
        
        try:
            resp = client.post(
                f"{API_BASE}/auth/sign-in",
                json=signin_data,
                headers={"Content-Type": "application/json"}
            )
            signin_response = resp.json()
            
            if resp.status_code == 200:
                print(f"    ✅ Sign In SUCCESS")
                print(f"       Status: {resp.status_code}")
                
                if "session" in signin_response and "access_token" in signin_response["session"]:
                    token = signin_response["session"]["access_token"]
                    user = signin_response.get("user", {})
                    
                    print(f"       Token: {token[:30]}...")
                    print(f"       User ID: {user.get('id', 'N/A')}")
                    print(f"       User Email: {user.get('email', 'N/A')}")
                else:
                    print(f"       ⚠️  Response missing session/token")
            else:
                print(f"    ❌ Sign In FAILED")
                print(f"       Status: {resp.status_code}")
                print(f"       Response: {json.dumps(signin_response, indent=2)}")
                return
        except Exception as e:
            print(f"    ❌ Sign In ERROR: {e}")
            return
        
        # 3. Test Session Retrieval with Token
        print(f"\n[3] Testing Session endpoint with Bearer token...")
        
        try:
            resp = client.get(
                f"{API_BASE}/auth/session",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
            )
            session_response = resp.json()
            
            if resp.status_code == 200:
                print(f"    ✅ Session Retrieval SUCCESS")
                print(f"       Status: {resp.status_code}")
                
                if "user" in session_response:
                    user = session_response["user"]
                    print(f"       User ID: {user.get('id', 'N/A')}")
                    print(f"       User Email: {user.get('email', 'N/A')}")
                    print(f"       User Name: {user.get('name', 'N/A')}")
            else:
                print(f"    ❌ Session Retrieval FAILED")
                print(f"       Status: {resp.status_code}")
                print(f"       Response: {json.dumps(session_response, indent=2)}")
        except Exception as e:
            print(f"    ❌ Session Retrieval ERROR: {e}")
        
        # 4. Test Sign Out
        print(f"\n[4] Testing Sign Out endpoint...")
        
        try:
            resp = client.post(
                f"{API_BASE}/auth/sign-out",
                headers={"Authorization": f"Bearer {token}"}
            )
            if resp.status_code == 200:
                print(f"    ✅ Sign Out SUCCESS")
                print(f"       Status: {resp.status_code}")
            else:
                print(f"    ❌ Sign Out FAILED")
                print(f"       Status: {resp.status_code}")
        except Exception as e:
            print(f"    ❌ Sign Out ERROR: {e}")
        
        print(f"\n{'='*60}")
        print(f"Authentication Flow Test Completed!")
        print(f"{'='*60}\n")

if __name__ == "__main__":
    test_auth_flow()
