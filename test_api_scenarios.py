#!/usr/bin/env python3
"""
تست سناریوهای مختلف API برای بررسی دسترسی کاربران
"""

import os
import sys
import django
import requests
from datetime import datetime

# تنظیم Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
django.setup()

from apps.users.models import User
from apps.meet.jwt_utils import get_meet_jwt_generator

def test_api_scenarios():
    """تست سناریوهای مختلف API"""
    
    print("🔍 تست سناریوهای مختلف API...")
    print("=" * 60)
    
    # دریافت کاربر محمد
    try:
        user = User.objects.get(username='mohammad')
        print(f"✅ کاربر یافت شد: {user.username} (GUID: {user.guid})")
    except User.DoesNotExist:
        print("❌ کاربر محمد یافت نشد!")
        return
    
    # دریافت JWT generator
    jwt_generator = get_meet_jwt_generator()
    
    # سناریوهای مختلف
    test_cases = [
        {
            'name': 'جلسه موجود با دسترسی',
            'room_name': 'room',
            'expected': 'success'
        },
        {
            'name': 'جلسه ناموجود',
            'room_name': 'nonexistent_room',
            'expected': 'no_access'
        },
        {
            'name': 'جلسه با نام خالی',
            'room_name': '',
            'expected': 'error'
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 تست {i}: {test_case['name']}")
        print("-" * 40)
        
        room_name = test_case['room_name']
        print(f"🏠 نام جلسه: '{room_name}'")
        
        # تست API
        access_data, error_message = jwt_generator.check_user_access(room_name, user.guid)
        
        if error_message:
            print(f"❌ خطا: {error_message}")
        else:
            print("✅ دسترسی تایید شد")
            if access_data:
                print(f"📊 اطلاعات جلسه:")
                print(f"   - عنوان: {access_data.get('meet_title', 'نامشخص')}")
                print(f"   - وضعیت: {access_data.get('status', 'نامشخص')}")
                print(f"   - نوع کاربر: {access_data.get('user_type', 'نامشخص')}")
                print(f"   - مدیر جلسه: {access_data.get('is_organizer', False)}")
                print(f"   - شرکت‌کننده: {access_data.get('is_participant', False)}")
                print(f"   - زمان شروع: {access_data.get('start_time', 'نامشخص')}")
                print(f"   - زمان پایان: {access_data.get('end_time', 'نامشخص')}")
                
                # تولید JWT
                jwt_token = jwt_generator.generate_meet_jwt(user, room_name, access_data)
                if jwt_token:
                    print(f"🎫 JWT تولید شد: {jwt_token[:50]}...")
                else:
                    print("❌ خطا در تولید JWT")
    
    print("\n" + "=" * 60)
    print("✅ تست سناریوها تکمیل شد")

def test_direct_api_call():
    """تست مستقیم API"""
    
    print("\n🌐 تست مستقیم API...")
    print("=" * 60)
    
    # تست API مستقیماً
    api_url = "http://avinoo.ir/api/meets/access/"
    
    test_params = [
        {
            'room_name': 'room',
            'user_guid': '13bf04c5-6b5d-4325-88ce-b43ca98d14db'
        },
        {
            'room_name': 'test_room',
            'user_guid': '13bf04c5-6b5d-4325-88ce-b43ca98d14db'
        }
    ]
    
    for i, params in enumerate(test_params, 1):
        print(f"\n📡 تست API {i}:")
        print(f"   - Room: {params['room_name']}")
        print(f"   - User GUID: {params['user_guid']}")
        
        try:
            response = requests.get(api_url, params=params, timeout=10)
            print(f"   - Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   - Success: {data.get('success', False)}")
                
                if data.get('success'):
                    access_data = data['data']
                    print(f"   - Has Access: {access_data.get('has_access', False)}")
                    print(f"   - Status: {access_data.get('status', 'نامشخص')}")
                    print(f"   - User Type: {access_data.get('user_type', 'نامشخص')}")
                else:
                    print(f"   - Error: {data.get('message', 'نامشخص')}")
            else:
                print(f"   - Error: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   - Exception: {str(e)}")

if __name__ == "__main__":
    test_api_scenarios()
    test_direct_api_call()
