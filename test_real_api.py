#!/usr/bin/env python3
"""
تست API واقعی با GUID کاربر محمد
"""

import os
import sys
import django
import requests
import json

# تنظیم Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
django.setup()

from apps.users.models import User

def test_real_api():
    """تست API واقعی"""
    
    print("🌐 تست API واقعی...")
    print("=" * 60)
    
    # دریافت کاربر محمد
    try:
        user = User.objects.get(username='mohammad')
        print(f"✅ کاربر: {user.username}")
        print(f"📋 GUID: {user.guid}")
    except User.DoesNotExist:
        print("❌ کاربر محمد یافت نشد!")
        return
    
    # تست API
    api_url = "http://avinoo.ir/api/meets/access/"
    params = {
        'room_name': 'room',
        'user_guid': str(user.guid)
    }
    
    print(f"\n📡 درخواست API:")
    print(f"   URL: {api_url}")
    print(f"   Room: {params['room_name']}")
    print(f"   GUID: {params['user_guid']}")
    
    try:
        response = requests.get(api_url, params=params, timeout=10)
        print(f"\n📊 پاسخ API:")
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Success: {data.get('success', False)}")
            
            if data.get('success'):
                access_data = data['data']
                print(f"\n✅ اطلاعات جلسه:")
                print(f"   - عنوان: {access_data.get('meet_title', 'نامشخص')}")
                print(f"   - وضعیت: {access_data.get('status', 'نامشخص')}")
                print(f"   - نوع کاربر: {access_data.get('user_type', 'نامشخص')}")
                print(f"   - مدیر جلسه: {access_data.get('is_organizer', False)}")
                print(f"   - شرکت‌کننده: {access_data.get('is_participant', False)}")
                print(f"   - زمان شروع: {access_data.get('start_time', 'نامشخص')}")
                print(f"   - زمان پایان: {access_data.get('end_time', 'نامشخص')}")
                print(f"   - دسترسی: {access_data.get('has_access', False)}")
            else:
                print(f"   ❌ خطا: {data.get('error', 'نامشخص')}")
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")

if __name__ == "__main__":
    test_real_api()
