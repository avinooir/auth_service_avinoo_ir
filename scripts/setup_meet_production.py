"""
Setup script for meet.avinoo.ir production environment
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
django.setup()

from sso.models import SSOClient
from django.utils.crypto import get_random_string


def setup_meet_production():
    """Setup meet.avinoo.ir for production"""
    
    print("=== راه‌اندازی meet.avinoo.ir برای production ===\n")
    
    # Production client configuration
    client_id = 'meet_avinoo'
    client_secret = get_random_string(32)
    
    # Check if client already exists
    try:
        client = SSOClient.objects.get(client_id=client_id)
        print(f"کلاینت {client_id} قبلاً وجود دارد")
        print(f"نام: {client.name}")
        print(f"دامنه: {client.domain}")
        print(f"آدرس بازگشت: {client.redirect_uri}")
        print(f"فعال: {client.is_active}")
        
        # Update if needed
        update_needed = False
        if client.domain != 'meet.avinoo.ir':
            client.domain = 'meet.avinoo.ir'
            update_needed = True
            print("✓ دامنه به‌روزرسانی شد")
        
        if not client.allow_any_path:
            client.allow_any_path = True
            update_needed = True
            print("✓ اجازه هر مسیر فعال شد")
        
        if update_needed:
            client.save()
            print("✓ کلاینت به‌روزرسانی شد")
        
        return client
        
    except SSOClient.DoesNotExist:
        pass
    
    # Create new production client
    client = SSOClient.objects.create(
        name='Meet Avinoo Production',
        domain='meet.avinoo.ir',
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri='https://meet.avinoo.ir/roomname',  # Placeholder
        allowed_redirect_uris=[
            'https://meet.avinoo.ir/',
            'https://meet.avinoo.ir/roomname',
            'https://meet.avinoo.ir/*'
        ],
        allow_any_path=True,  # Allow any path on meet.avinoo.ir
        is_active=True
    )
    
    print(f"کلاینت meet.avinoo.ir برای production ایجاد شد:")
    print(f"شناسه کلاینت: {client.client_id}")
    print(f"رمز کلاینت: {client.client_secret}")
    print(f"نام: {client.name}")
    print(f"دامنه: {client.domain}")
    print(f"آدرس بازگشت: {client.redirect_uri}")
    print(f"اجازه هر مسیر: {client.allow_any_path}")
    print(f"فعال: {client.is_active}")
    
    return client


def print_production_config():
    """Print production configuration"""
    
    print("\n=== پیکربندی Production ===\n")
    
    print("📋 تنظیمات کلاینت SSO:")
    print("   • شناسه کلاینت: meet_avinoo")
    print("   • دامنه: meet.avinoo.ir")
    print("   • اجازه هر مسیر: True")
    print("   • فعال: True")
    
    print("\n🔧 تنظیمات JWT:")
    print("   • App ID: meet_avinoo")
    print("   • Domain: meet.avinoo.ir")
    print("   • Secret: meet_secret_key_2024")
    print("   • Algorithm: HS256")
    
    print("\n🌐 API خارجی:")
    print("   • URL: http://avinoo.ir/api/meets/access/")
    print("   • Parameters: room_name, user_guid")
    print("   • Response: JSON with access information")
    
    print("\n🔄 جریان SSO:")
    print("   1. کاربر روی meet.avinoo.ir/roomname کلیک می‌کند")
    print("   2. هدایت به: http://auth.avinoo.ir/login/?client_id=meet_avinoo&redirect_uri=https://meet.avinoo.ir/roomname")
    print("   3. کاربر وارد می‌شود")
    print("   4. بررسی دسترسی از طریق API خارجی")
    print("   5. تولید JWT token")
    print("   6. هدایت به: https://meet.avinoo.ir/roomname?jwt=TOKEN")
    
    print("\n✅ تست URL ها:")
    print("   • ورود: http://auth.avinoo.ir/login/?client_id=meet_avinoo&redirect_uri=https://meet.avinoo.ir/test-room")
    print("   • بازگشت: http://auth.avinoo.ir/callback/?client_id=meet_avinoo&state=test")
    
    print("\n🔒 امنیت:")
    print("   • JWT tokens با secret key امضا می‌شوند")
    print("   • اعتبار توکن بر اساس زمان جلسه محاسبه می‌شود")
    print("   • دسترسی کاربر از طریق API خارجی بررسی می‌شود")
    print("   • تمام فعالیت‌ها در لاگ ثبت می‌شوند")


if __name__ == '__main__':
    client = setup_meet_production()
    print_production_config()
    
    print("\n🎉 راه‌اندازی production تکمیل شد!")
    print("\n📝 نکات مهم:")
    print("   • مطمئن شوید که API خارجی در دسترس است")
    print("   • JWT secret را در production تغییر دهید")
    print("   • لاگ‌ها را برای نظارت بر فعالیت‌ها بررسی کنید")
    print("   • تست‌های کامل را قبل از deployment انجام دهید")
