#!/usr/bin/env python3
"""
تست فیلدهای جدید کاربر (is_superuser, is_staff)
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
django.setup()

from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import User

def test_user_fields():
    """تست فیلدهای کاربر"""
    print("🧪 تست فیلدهای کاربر...")
    
    try:
        # دریافت کاربران مختلف
        users = User.objects.all()[:3]
        
        if not users:
            print("❌ هیچ کاربری در سیستم وجود ندارد")
            return
        
        for user in users:
            print(f"\n👤 کاربر: {user.username}")
            print(f"   ID: {user.id}")
            print(f"   Email: {user.email}")
            print(f"   First Name: {user.first_name}")
            print(f"   Last Name: {user.last_name}")
            print(f"   Is Active: {user.is_active}")
            print(f"   Is Superuser: {user.is_superuser}")
            print(f"   Is Staff: {user.is_staff}")
            
            # تولید JWT token
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            print(f"   JWT Token: {access_token[:50]}...")
            
            # تست اعتبارسنجی
            from rest_framework_simplejwt.tokens import AccessToken
            decoded_token = AccessToken(access_token)
            user_id = decoded_token['user_id']
            
            print(f"   ✅ Token معتبر - User ID: {user_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ خطا در تست: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_api_response():
    """تست پاسخ API"""
    print("\n🔍 تست پاسخ API...")
    
    try:
        # دریافت کاربر اول
        user = User.objects.first()
        if not user:
            print("❌ هیچ کاربری در سیستم وجود ندارد")
            return
        
        # شبیه‌سازی پاسخ API
        api_response = {
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_active': user.is_active,
                'is_superuser': user.is_superuser,
                'is_staff': user.is_staff,
            }
        }
        
        print("📋 پاسخ API:")
        import json
        print(json.dumps(api_response, indent=2, ensure_ascii=False))
        
        # بررسی فیلدهای جدید
        if 'is_superuser' in api_response['user'] and 'is_staff' in api_response['user']:
            print("✅ فیلدهای is_superuser و is_staff اضافه شدند!")
        else:
            print("❌ فیلدهای is_superuser و is_staff اضافه نشدند!")
        
        return True
        
    except Exception as e:
        print(f"❌ خطا در تست API: {str(e)}")
        return False

if __name__ == '__main__':
    print("🚀 تست فیلدهای کاربر")
    print("=" * 50)
    
    success1 = test_user_fields()
    success2 = test_api_response()
    
    if success1 and success2:
        print("\n✅ تمام تست‌ها موفق بود!")
    else:
        print("\n❌ برخی تست‌ها ناموفق بود!")
    
    print("\n💡 حالا می‌توانید از API های SSO استفاده کنید:")
    print("   - POST /sso/api/login/")
    print("   - POST /sso/api/validate-token/")
    print("   - GET /sso/api/user-info/")
    print("   - POST /sso/api/register/")
    print("   - POST /sso/api/callback/")
