#!/usr/bin/env python3
"""
تست JWT token generation
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

def test_jwt_generation():
    """تست تولید JWT token"""
    print("🧪 تست تولید JWT token...")
    
    try:
        # دریافت کاربر اول
        user = User.objects.first()
        if not user:
            print("❌ هیچ کاربری در سیستم وجود ندارد")
            return
        
        print(f"👤 کاربر: {user.username} (ID: {user.id})")
        
        # تولید JWT token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        print("✅ JWT token تولید شد!")
        print(f"🔑 Access Token: {access_token[:50]}...")
        print(f"🔄 Refresh Token: {refresh_token[:50]}...")
        
        # تست اعتبارسنجی
        from rest_framework_simplejwt.tokens import AccessToken
        decoded_token = AccessToken(access_token)
        user_id = decoded_token['user_id']
        
        print(f"✅ Token اعتبارسنجی شد - User ID: {user_id}")
        
        return access_token
        
    except Exception as e:
        print(f"❌ خطا در تولید JWT: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def test_token_validation(token):
    """تست اعتبارسنجی token"""
    if not token:
        return
    
    print("\n🔍 تست اعتبارسنجی token...")
    
    try:
        from rest_framework_simplejwt.tokens import AccessToken
        decoded_token = AccessToken(token)
        
        print("✅ Token معتبر است!")
        print(f"   User ID: {decoded_token['user_id']}")
        print(f"   Expires: {decoded_token['exp']}")
        print(f"   Issued: {decoded_token['iat']}")
        
    except Exception as e:
        print(f"❌ خطا در اعتبارسنجی: {str(e)}")

if __name__ == '__main__':
    print("🚀 تست JWT Token Generation")
    print("=" * 50)
    
    token = test_jwt_generation()
    test_token_validation(token)
    
    print("\n✨ تست کامل شد!")
