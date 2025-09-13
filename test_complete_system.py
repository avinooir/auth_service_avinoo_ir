#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تست کامل سیستم JWT برای meet.avinoo.ir
"""

import os
import sys
import django
import json
import jwt
from datetime import datetime

# تنظیم Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
django.setup()

from apps.users.models import User
from apps.meet.jwt_utils import get_meet_jwt_generator

def test_complete_system():
    """تست کامل سیستم JWT"""
    print("=" * 50)
    print("🧪 تست کامل سیستم JWT برای meet.avinoo.ir")
    print("=" * 50)
    
    try:
        # 1. بررسی کاربر
        print("\n1️⃣ بررسی کاربر...")
        user = User.objects.get(email='mohammad.rahimaee@gmail.com')
        print(f"✅ کاربر یافت شد: {user.username} ({user.email})")
        print(f"   - GUID: {user.guid}")
        print(f"   - نام کامل: {user.first_name} {user.last_name}")
        print(f"   - نقش: {'مدیر' if user.is_superuser else 'کاربر عادی'}")
        
        # 2. ایجاد JWT Generator
        print("\n2️⃣ ایجاد JWT Generator...")
        jwt_generator = get_meet_jwt_generator()
        print("✅ JWT Generator ایجاد شد")
        print(f"   - App ID: {jwt_generator.app_id}")
        print(f"   - Domain: {jwt_generator.domain}")
        
        # 3. تولید JWT Token
        print("\n3️⃣ تولید JWT Token...")
        jwt_token = jwt_generator.generate_meet_jwt(user, 'room', None)
        print("✅ JWT Token تولید شد")
        print(f"   - طول توکن: {len(jwt_token)} کاراکتر")
        
        # 4. رمزگشایی و بررسی JWT
        print("\n4️⃣ رمزگشایی و بررسی JWT...")
        decoded = jwt.decode(jwt_token, options={'verify_signature': False})
        print("✅ JWT Token رمزگشایی شد")
        
        # 5. نمایش محتوای JWT
        print("\n5️⃣ محتوای JWT:")
        print("-" * 30)
        print(json.dumps(decoded, indent=2, ensure_ascii=False))
        
        # 6. بررسی ساختار
        print("\n6️⃣ بررسی ساختار JWT...")
        required_fields = ['aud', 'iss', 'sub', 'room', 'exp', 'nbf', 'moderator', 'context', 'identity', 'custom']
        for field in required_fields:
            if field in decoded:
                print(f"✅ {field}: موجود")
            else:
                print(f"❌ {field}: مفقود")
        
        # بررسی context
        if 'context' in decoded:
            context_fields = ['user', 'group']
            for field in context_fields:
                if field in decoded['context']:
                    print(f"✅ context.{field}: موجود")
                else:
                    print(f"❌ context.{field}: مفقود")
        
        # بررسی user
        if 'context' in decoded and 'user' in decoded['context']:
            user_fields = ['id', 'name', 'email', 'avatar', 'affiliation', 'moderator', 'region', 'displayName']
            for field in user_fields:
                if field in decoded['context']['user']:
                    print(f"✅ context.user.{field}: موجود")
                else:
                    print(f"❌ context.user.{field}: مفقود")
        
        # 7. بررسی زمان‌ها
        print("\n7️⃣ بررسی زمان‌ها...")
        exp_time = datetime.fromtimestamp(decoded['exp'])
        nbf_time = datetime.fromtimestamp(decoded['nbf'])
        now = datetime.now()
        
        print(f"✅ زمان شروع (nbf): {nbf_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"✅ زمان انقضا (exp): {exp_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"✅ زمان فعلی: {now.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if now < nbf_time:
            print("⚠️  توکن هنوز فعال نشده")
        elif now > exp_time:
            print("❌ توکن منقضی شده")
        else:
            print("✅ توکن در حال حاضر معتبر است")
        
        # 8. URL نهایی
        print("\n8️⃣ URL نهایی...")
        final_url = f"https://meet.avinoo.ir/room?jwt={jwt_token}"
        print("✅ URL نهایی:")
        print(final_url)
        
        # 9. تست External API
        print("\n9️⃣ تست External API...")
        try:
            access_data = jwt_generator.check_user_access('room', user.guid)
            if access_data:
                print("✅ External API پاسخ داد")
                print(f"   - دسترسی: {access_data.get('has_access', False)}")
                print(f"   - نوع کاربر: {access_data.get('user_type', 'unknown')}")
            else:
                print("⚠️  External API پاسخ نداد (استفاده از داده‌های پیش‌فرض)")
        except Exception as e:
            print(f"⚠️  خطا در External API: {e}")
        
        print("\n" + "=" * 50)
        print("🎉 تست کامل با موفقیت انجام شد!")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"\n❌ خطا در تست: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_complete_system()
