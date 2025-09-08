#!/usr/bin/env python
"""
Simple test script for Auth Service API
"""

import requests
import json
import time

# Wait for server to start
print("Waiting for server to start...")
time.sleep(3)

# Test data
test_user = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpassword123",
    "password_confirm": "testpassword123",
    "first_name": "Test",
    "last_name": "User"
}

# Test registration
print("Testing user registration...")
try:
    response = requests.post(
        "http://127.0.0.1:8000/auth/register/",
        json=test_user,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 201:
        print("✅ Registration successful!")
        data = response.json()
        print(f"User ID: {data['user']['id']}")
        print(f"Username: {data['user']['username']}")
        
        # Save tokens for further testing
        access_token = data['tokens']['access']
        refresh_token = data['tokens']['refresh']
        
        # Test login
        print("\nTesting user login...")
        login_data = {
            "username": test_user["username"],
            "password": test_user["password"]
        }
        
        login_response = requests.post(
            "http://127.0.0.1:8000/auth/login/",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if login_response.status_code == 200:
            print("✅ Login successful!")
            login_data = login_response.json()
            print(f"Access token received: {len(login_data['tokens']['access'])} characters")
            
            # Test get user profile
            print("\nTesting get user profile...")
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            profile_response = requests.get(
                "http://127.0.0.1:8000/auth/me/",
                headers=headers
            )
            
            if profile_response.status_code == 200:
                print("✅ Get profile successful!")
                profile_data = profile_response.json()
                print(f"Profile username: {profile_data['user']['username']}")
                print(f"Profile email: {profile_data['user']['email']}")
            else:
                print(f"❌ Get profile failed: {profile_response.status_code}")
                print(profile_response.text)
        else:
            print(f"❌ Login failed: {login_response.status_code}")
            print(login_response.text)
            
    else:
        print(f"❌ Registration failed: {response.status_code}")
        print(response.text)
        
except requests.exceptions.ConnectionError:
    print("❌ Could not connect to server. Make sure the server is running on http://127.0.0.1:8000/")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n🎉 Test completed!")
