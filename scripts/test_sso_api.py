#!/usr/bin/env python
"""
Script to test SSO API endpoints
"""

import os
import sys
import django
import requests
import json
from django.conf import settings

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
django.setup()

from sso.models import SSOClient


def test_sso_api():
    """Test SSO API endpoints"""
    
    base_url = "http://127.0.0.1:8000"
    
    # Get client credentials
    try:
        client = SSOClient.objects.get(client_id='app1_client')
        client_id = client.client_id
        client_secret = client.client_secret
        redirect_uri = client.redirect_uri
    except SSOClient.DoesNotExist:
        print("❌ کلاینت app1_client یافت نشد. ابتدا کلاینت‌ها را ایجاد کنید.")
        return
    
    print("🧪 تست API های SSO")
    print("=" * 50)
    print(f"Base URL: {base_url}")
    print(f"Client ID: {client_id}")
    print(f"Redirect URI: {redirect_uri}")
    print()
    
    # Test 1: Register a new user
    print("1️⃣ تست ثبت‌نام کاربر جدید")
    print("-" * 30)
    
    register_data = {
        "username": "testuser",
        "email": "test@example.com",
        "phone_number": "+989123456789",
        "first_name": "تست",
        "last_name": "کاربر",
        "password": "testpassword123",
        "password_confirm": "testpassword123",
        "client_id": client_id,
        "redirect_uri": redirect_uri
    }
    
    try:
        response = requests.post(f"{base_url}/api/register/", json=register_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 201:
            access_token = response.json().get('access_token')
            print("✅ ثبت‌نام موفق")
        else:
            print("❌ ثبت‌نام ناموفق")
            access_token = None
            
    except requests.exceptions.ConnectionError:
        print("❌ خطا در اتصال به سرور. مطمئن شوید سرور در حال اجرا است.")
        return
    except Exception as e:
        print(f"❌ خطا در ثبت‌نام: {str(e)}")
        access_token = None
    
    print()
    
    # Test 2: Login with existing user
    print("2️⃣ تست ورود کاربر")
    print("-" * 30)
    
    login_data = {
        "username": "testuser",
        "password": "testpassword123",
        "client_id": client_id,
        "redirect_uri": redirect_uri
    }
    
    try:
        response = requests.post(f"{base_url}/api/login/", json=login_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            access_token = response.json().get('access_token')
            print("✅ ورود موفق")
        else:
            print("❌ ورود ناموفق")
            access_token = None
            
    except Exception as e:
        print(f"❌ خطا در ورود: {str(e)}")
        access_token = None
    
    print()
    
    # Test 3: Validate token
    if access_token:
        print("3️⃣ تست اعتبارسنجی توکن")
        print("-" * 30)
        
        validate_data = {
            "token": access_token,
            "client_id": client_id
        }
        
        try:
            response = requests.post(f"{base_url}/api/validate-token/", json=validate_data)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
            
            if response.status_code == 200 and response.json().get('valid'):
                print("✅ اعتبارسنجی توکن موفق")
            else:
                print("❌ اعتبارسنجی توکن ناموفق")
                
        except Exception as e:
            print(f"❌ خطا در اعتبارسنجی توکن: {str(e)}")
        
        print()
        
        # Test 4: Get user info
        print("4️⃣ تست دریافت اطلاعات کاربر")
        print("-" * 30)
        
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        try:
            response = requests.get(f"{base_url}/api/user-info/", headers=headers)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
            
            if response.status_code == 200:
                print("✅ دریافت اطلاعات کاربر موفق")
            else:
                print("❌ دریافت اطلاعات کاربر ناموفق")
                
        except Exception as e:
            print(f"❌ خطا در دریافت اطلاعات کاربر: {str(e)}")
        
        print()
        
        # Test 5: Logout
        print("5️⃣ تست خروج از سیستم")
        print("-" * 30)
        
        logout_data = {
            "client_id": client_id,
            "redirect_uri": "http://localhost:3000"
        }
        
        try:
            response = requests.post(f"{base_url}/api/logout/", json=logout_data, headers=headers)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
            
            if response.status_code == 200:
                print("✅ خروج موفق")
            else:
                print("❌ خروج ناموفق")
                
        except Exception as e:
            print(f"❌ خطا در خروج: {str(e)}")
    
    print()
    print("🎯 تست‌های API تکمیل شد!")
    print()
    print("📝 نکات:")
    print("1. برای تست کامل، سرور Django باید در حال اجرا باشد")
    print("2. کلاینت‌های SSO باید از قبل ایجاد شده باشند")
    print("3. برای تست رابط کاربری، فایل‌های HTML را در مرورگر باز کنید")
    print("4. URL های تست:")
    print(f"   - Auth Service: {base_url}")
    print(f"   - App1: {base_url}/client_apps/app1/index.html")
    print(f"   - App2: {base_url}/client_apps/app2/index.html")


if __name__ == '__main__':
    test_sso_api()
