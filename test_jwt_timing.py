#!/usr/bin/env python3
"""
تست زمان‌بندی JWT
"""

import os
import sys
import django
import jwt
from datetime import datetime, timedelta

# تنظیم Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
django.setup()

from apps.users.models import User
from apps.meet.jwt_utils import get_meet_jwt_generator

def test_jwt_timing():
    """تست زمان‌بندی JWT"""
    
    print("🕐 تست زمان‌بندی JWT...")
    print("=" * 50)
    
    # دریافت کاربر محمد
    try:
        user = User.objects.get(username='mohammad')
        print(f"✅ کاربر: {user.username}")
    except User.DoesNotExist:
        print("❌ کاربر محمد یافت نشد!")
        return
    
    # دریافت JWT generator
    jwt_generator = get_meet_jwt_generator()
    
    # تولید JWT
    jwt_token = jwt_generator.generate_meet_jwt(user, 'room')
    
    if jwt_token:
        print(f"✅ JWT تولید شد")
        
        # دیکد کردن JWT (بدون بررسی audience)
        try:
            decoded = jwt.decode(jwt_token, jwt_generator.app_secret, algorithms=["HS256"], options={"verify_aud": False})
            
            # زمان‌ها
            now = datetime.now()
            nbf_time = datetime.fromtimestamp(decoded['nbf'])
            exp_time = datetime.fromtimestamp(decoded['exp'])
            
            print(f"\n📅 زمان‌بندی:")
            print(f"   - زمان فعلی: {now.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   - nbf (Not Before): {nbf_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   - exp (Expiration): {exp_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # بررسی اعتبار
            if nbf_time <= now <= exp_time:
                print("✅ JWT معتبر است!")
            else:
                if nbf_time > now:
                    print("❌ JWT هنوز معتبر نیست (nbf در آینده)")
                if now > exp_time:
                    print("❌ JWT منقضی شده است")
                    
        except Exception as e:
            print(f"❌ خطا در دیکد JWT: {str(e)}")
    else:
        print("❌ خطا در تولید JWT")

if __name__ == "__main__":
    test_jwt_timing()
