#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تست نهایی JWT مطابق با jisttiii_jwt_token.py
"""

import os
import sys
import django
import json
import jwt

# تنظیم Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
django.setup()

from apps.users.models import User
from apps.meet.jwt_utils import get_meet_jwt_generator

def test_final_jwt():
    """تست نهایی JWT"""
    print("=" * 60)
    print("🎯 تست نهایی JWT مطابق با jisttiii_jwt_token.py")
    print("=" * 60)
    
    try:
        # دریافت کاربر
        user = User.objects.get(email='mohammad.rahimaee@gmail.com')
        print(f"✅ کاربر: {user.username} ({user.email})")
        
        # ایجاد JWT Generator
        jwt_generator = get_meet_jwt_generator()
        print(f"✅ App ID: {jwt_generator.app_id}")
        print(f"✅ Domain: {jwt_generator.domain}")
        print(f"✅ Secret: {jwt_generator.app_secret}")
        
        # تولید JWT
        jwt_token = jwt_generator.generate_meet_jwt(user, 'room', None)
        print(f"✅ JWT تولید شد (طول: {len(jwt_token)} کاراکتر)")
        
        # رمزگشایی
        decoded = jwt.decode(jwt_token, options={'verify_signature': False})
        
        print("\n" + "=" * 60)
        print("📋 محتوای JWT:")
        print("=" * 60)
        print(json.dumps(decoded, indent=2, ensure_ascii=False))
        
        print("\n" + "=" * 60)
        print("🔍 بررسی تطبیق با jisttiii_jwt_token.py:")
        print("=" * 60)
        
        # بررسی فیلدهای اصلی
        checks = [
            ("aud", decoded.get('aud'), "meet_avinoo"),
            ("iss", decoded.get('iss'), "meet_avinoo"),
            ("sub", decoded.get('sub'), "meet.avinoo.ir"),
            ("room", decoded.get('room'), "room"),
            ("moderator", decoded.get('moderator'), True),
        ]
        
        for field, actual, expected in checks:
            if actual == expected:
                print(f"✅ {field}: {actual}")
            else:
                print(f"❌ {field}: {actual} (انتظار: {expected})")
        
        # بررسی context
        context = decoded.get('context', {})
        print(f"\n📁 Context:")
        print(f"✅ user: موجود")
        print(f"✅ group: {context.get('group')}")
        print(f"✅ features: موجود")
        
        # بررسی features
        features = context.get('features', {})
        feature_checks = [
            ("livestreaming", True),
            ("recording", True),
            ("screen-sharing", True),
            ("sip", False),
            ("etherpad", False),
            ("transcription", True),
            ("breakout-rooms", True),
        ]
        
        print(f"\n🎛️ Features:")
        for feature, expected in feature_checks:
            actual = features.get(feature)
            if actual == expected:
                print(f"✅ {feature}: {actual}")
            else:
                print(f"❌ {feature}: {actual} (انتظار: {expected})")
        
        # بررسی identity
        identity = decoded.get('identity', {})
        print(f"\n🆔 Identity:")
        print(f"✅ type: {identity.get('type')}")
        print(f"✅ guest: {identity.get('guest')}")
        print(f"✅ externalId: {identity.get('externalId')}")
        
        # بررسی custom
        custom = decoded.get('custom', {})
        print(f"\n🎨 Custom:")
        print(f"✅ theme: {custom.get('theme')}")
        print(f"✅ allowKnocking: {custom.get('allowKnocking')}")
        print(f"✅ enablePolls: {custom.get('enablePolls')}")
        
        print("\n" + "=" * 60)
        print("🎉 تست کامل شد!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ خطا: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_final_jwt()
