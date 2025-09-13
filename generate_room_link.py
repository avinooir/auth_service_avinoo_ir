#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تولید لینک ورود به اتاق برای کاربر محمد
"""

import os
import sys
import django

# تنظیم Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
django.setup()

from apps.users.models import User
from apps.meet.jwt_utils import get_meet_jwt_generator

def generate_room_link():
    """تولید لینک ورود به اتاق"""
    try:
        # دریافت کاربر محمد
        user = User.objects.get(email='mohammad.rahimaee@gmail.com')
        print(f"👤 کاربر: {user.username} ({user.email})")
        
        # ایجاد JWT Generator
        jwt_generator = get_meet_jwt_generator()
        
        # تولید JWT برای اتاق room
        jwt_token = jwt_generator.generate_meet_jwt(user, 'room', None)
        
        # تولید لینک نهایی
        final_url = f"https://meet.avinoo.ir/room?jwt={jwt_token}"
        
        print("\n" + "="*80)
        print("🔗 لینک ورود به اتاق room برای کاربر محمد:")
        print("="*80)
        print()
        print(final_url)
        print()
        print("="*80)
        print("📋 اطلاعات:")
        print("="*80)
        print(f"👤 کاربر: {user.username} ({user.email})")
        print(f"🏠 اتاق: room")
        print(f"🔑 طول توکن: {len(jwt_token)} کاراکتر")
        print(f"🆔 User ID: {user.id}")
        print(f"🔐 GUID: {user.guid}")
        print("="*80)
        
        return final_url
        
    except Exception as e:
        print(f"❌ خطا: {e}")
        return None

if __name__ == "__main__":
    generate_room_link()
