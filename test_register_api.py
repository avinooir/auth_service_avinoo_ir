#!/usr/bin/env python3
"""
تست مستقیم API ثبت نام
"""

import os
import sys
import django
import requests
import json
import time

# تنظیم Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
django.setup()

def test_register_api():
    """تست مستقیم API ثبت نام"""
    
    print("🌐 تست مستقیم API ثبت نام...")
    print("=" * 60)
    
    # داده‌های تست
    timestamp = int(time.time())
    test_data = {
        'username': f'apiuser{timestamp}',
        'email': f'api{timestamp}@example.com',
        'password': 'testpass123',
        'password_confirm': 'testpass123',
        'first_name': 'API',
        'last_name': 'Test',
        'phone_number': '+989123456789',
        'client_id': 'meet_avinoo',
        'redirect_uri': 'https://meet.avinoo.ir/room',
        'state': 'test_state'
    }
    
    print(f"📋 داده‌های ارسالی:")
    for key, value in test_data.items():
        if key in ['password', 'password_confirm']:
            print(f"   {key}: {'*' * len(value)}")
        else:
            print(f"   {key}: {value}")
    
    # ارسال درخواست
    url = "http://127.0.0.1:8000/api/register/"
    
    try:
        response = requests.post(url, json=test_data, timeout=10)
        
        print(f"\n📊 پاسخ API:")
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ ثبت نام موفق!")
                print(f"   Message: {data.get('message')}")
                print(f"   Redirect URI: {data.get('redirect_uri')}")
            else:
                print(f"❌ خطا: {data.get('error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

if __name__ == "__main__":
    test_register_api()
