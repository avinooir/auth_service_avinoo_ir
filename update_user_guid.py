#!/usr/bin/env python3
"""
به‌روزرسانی GUID کاربر محمد
"""

import os
import sys
import django

# تنظیم Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
django.setup()

from apps.users.models import User

def update_user_guid():
    """به‌روزرسانی GUID کاربر محمد"""
    
    print("🔧 به‌روزرسانی GUID کاربر محمد...")
    print("=" * 50)
    
    try:
        # دریافت کاربر محمد
        user = User.objects.get(username='mohammad')
        print(f"✅ کاربر یافت شد: {user.username}")
        print(f"📋 GUID فعلی: {user.guid}")
        
        # GUID جدید (مطابق با API)
        new_guid = "13bf04c5-6b5d-4325-88ce-b43ca98d14db"
        print(f"🔄 GUID جدید: {new_guid}")
        
        # به‌روزرسانی GUID
        user.guid = new_guid
        user.save()
        
        print("✅ GUID به‌روزرسانی شد!")
        
        # تایید تغییر
        user.refresh_from_db()
        print(f"✅ GUID تایید شد: {user.guid}")
        
    except User.DoesNotExist:
        print("❌ کاربر محمد یافت نشد!")
    except Exception as e:
        print(f"❌ خطا: {str(e)}")

if __name__ == "__main__":
    update_user_guid()
