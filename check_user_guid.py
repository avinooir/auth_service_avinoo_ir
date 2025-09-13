#!/usr/bin/env python3
"""
بررسی GUID کاربر محمد
"""

import os
import sys
import django

# تنظیم Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
django.setup()

from apps.users.models import User

def check_user_guid():
    """بررسی GUID کاربر محمد"""
    
    print("🔍 بررسی GUID کاربر محمد...")
    print("=" * 50)
    
    try:
        # دریافت کاربر محمد
        user = User.objects.get(username='mohammad')
        print(f"✅ کاربر یافت شد: {user.username}")
        print(f"📋 GUID: {user.guid}")
        print(f"📧 ایمیل: {user.email}")
        print(f"👤 نام کامل: {user.first_name} {user.last_name}")
        
        # تست API با GUID واقعی
        print(f"\n🌐 تست API با GUID واقعی:")
        print(f"   URL: http://avinoo.ir/api/meets/access/")
        print(f"   Room: room")
        print(f"   GUID: {user.guid}")
        
    except User.DoesNotExist:
        print("❌ کاربر محمد یافت نشد!")
    except Exception as e:
        print(f"❌ خطا: {str(e)}")

if __name__ == "__main__":
    check_user_guid()
