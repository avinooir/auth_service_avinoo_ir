#!/usr/bin/env python3
"""
مثال ساده برای تست API های SSO
"""

import requests
import json

# تنظیمات
BASE_URL = "http://127.0.0.1:8000"
CLIENT_ID = "test_page_client"
REDIRECT_URI = "http://127.0.0.1:8000/test/callback/"

def test_login():
    """تست ورود"""
    print("🔐 تست ورود...")
    
    url = f"{BASE_URL}/api/login/"
    data = {
        "username": "mohammad",
        "password": "1",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "state": "test_state"
    }
    
    response = requests.post(url, json=data)
    result = response.json()
    
    if result.get("success"):
        print("✅ ورود موفق!")
        print(f"Token: {result['access_token'][:50]}...")
        print(f"User: {result['user']['username']}")
        return result['access_token']
    else:
        print("❌ ورود ناموفق!")
        print(f"Error: {result.get('error')}")
        return None

def test_validate_token(token):
    """تست اعتبارسنجی token"""
    print("\n🔍 تست اعتبارسنجی token...")
    
    url = f"{BASE_URL}/api/validate-token/"
    data = {
        "token": token,
        "client_id": CLIENT_ID
    }
    
    response = requests.post(url, json=data)
    result = response.json()
    
    if result.get("valid"):
        print("✅ Token معتبر!")
        print(f"User: {result['user']['username']}")
    else:
        print("❌ Token نامعتبر!")
        print(f"Error: {result.get('error')}")

def test_user_info(token):
    """تست دریافت اطلاعات کاربر"""
    print("\n👤 تست اطلاعات کاربر...")
    
    url = f"{BASE_URL}/api/user-info/"
    params = {"token": token}
    
    response = requests.get(url, params=params)
    result = response.json()
    
    if result.get("success"):
        print("✅ اطلاعات کاربر دریافت شد!")
        print(f"Username: {result['user']['username']}")
        print(f"Email: {result['user']['email']}")
    else:
        print("❌ خطا در دریافت اطلاعات!")
        print(f"Error: {result.get('error')}")

def test_logout(token):
    """تست خروج"""
    print("\n🚪 تست خروج...")
    
    url = f"{BASE_URL}/api/logout/"
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": "http://127.0.0.1:8000/test/",
        "token": token
    }
    
    response = requests.get(url, params=params)
    result = response.json()
    
    if result.get("success"):
        print("✅ خروج موفق!")
        print(f"Message: {result['message']}")
    else:
        print("❌ خروج ناموفق!")
        print(f"Error: {result.get('error')}")

def test_register():
    """تست ثبت‌نام"""
    print("\n📝 تست ثبت‌نام...")
    
    url = f"{BASE_URL}/api/register/"
    data = {
        "username": "testuser123",
        "email": "testuser123@example.com",
        "password": "password123",
        "password_confirm": "password123",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI
    }
    
    response = requests.post(url, json=data)
    result = response.json()
    
    if result.get("success"):
        print("✅ ثبت‌نام موفق!")
        print(f"User: {result['user']['username']}")
    else:
        print("❌ ثبت‌نام ناموفق!")
        print(f"Error: {result.get('error')}")

def main():
    """تابع اصلی"""
    print("🚀 شروع تست API های SSO")
    print("=" * 50)
    
    # تست ورود
    token = test_login()
    
    if token:
        # تست اعتبارسنجی token
        test_validate_token(token)
        
        # تست اطلاعات کاربر
        test_user_info(token)
        
        # تست خروج
        test_logout(token)
    
    # تست ثبت‌نام
    test_register()
    
    print("\n" + "=" * 50)
    print("✅ تست‌ها تمام شد!")

if __name__ == "__main__":
    main()
