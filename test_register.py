#!/usr/bin/env python3
"""
تست ثبت نام کاربر
"""

import os
import sys
import django
import json

# تنظیم Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
django.setup()

from apps.users.models import User
from sso.views import SSORegisterView
from django.test import RequestFactory

def test_register():
    """تست ثبت نام"""
    
    print("🧪 تست ثبت نام...")
    print("=" * 50)
    
    # داده‌های تست
    import time
    timestamp = int(time.time())
    test_data = {
        'username': f'testuser{timestamp}',
        'email': f'test{timestamp}@example.com',
        'password': 'testpass123',
        'password_confirm': 'testpass123',
        'first_name': 'تست',
        'last_name': 'کاربر',
        'phone_number': '+989123456789',
        'client_id': 'meet_avinoo',
        'redirect_uri': 'https://meet.avinoo.ir/room',
        'state': 'test_state'
    }
    
    print(f"📋 داده‌های تست:")
    for key, value in test_data.items():
        if key in ['password', 'password_confirm']:
            print(f"   {key}: {'*' * len(value)}")
        else:
            print(f"   {key}: {value}")
    
    # بررسی وجود کاربر
    if User.objects.filter(username=test_data['username']).exists():
        print(f"⚠️  کاربر {test_data['username']} قبلاً موجود است")
        return
    
    if User.objects.filter(email=test_data['email']).exists():
        print(f"⚠️  ایمیل {test_data['email']} قبلاً استفاده شده است")
        return
    
    try:
        # ایجاد کاربر
        user = User.objects.create_user(
            username=test_data['username'],
            email=test_data['email'],
            password=test_data['password'],
            first_name=test_data['first_name'],
            last_name=test_data['last_name'],
            phone_number=test_data['phone_number'],
            is_active=True,
            is_email_verified=False
        )
        
        print(f"✅ کاربر با موفقیت ایجاد شد:")
        print(f"   - ID: {user.id}")
        print(f"   - Username: {user.username}")
        print(f"   - Email: {user.email}")
        print(f"   - GUID: {user.guid}")
        print(f"   - Active: {user.is_active}")
        print(f"   - Email Verified: {user.is_email_verified}")
        
        # حذف کاربر تست
        user.delete()
        print(f"🗑️  کاربر تست حذف شد")
        
    except Exception as e:
        print(f"❌ خطا در ایجاد کاربر: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_register()
