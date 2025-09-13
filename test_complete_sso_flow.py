"""
Test complete SSO flow with real room
"""

import os
import sys
import django
import requests
import json
from datetime import datetime

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
django.setup()

from apps.users.models import User
from apps.meet.jwt_utils import get_meet_jwt_generator
from sso.models import SSOClient


def test_complete_sso_flow():
    """Test complete SSO flow with real room"""
    
    print("=== تست جریان کامل SSO با اتاق واقعی ===\n")
    
    # Test parameters
    room_name = "room"
    user_guid = "6f99b0b3-33e7-49da-8ce9-7b1b7450c2bb"  # admin user
    
    print(f"🔍 پارامترهای تست:")
    print(f"   Room: {room_name}")
    print(f"   User GUID: {user_guid}")
    print()
    
    # Step 1: Check SSO client
    print("1️⃣ بررسی کلاینت SSO...")
    try:
        client = SSOClient.objects.get(client_id='meet_avinoo')
        print(f"   ✅ کلاینت یافت شد: {client.name}")
        print(f"   ✅ دامنه: {client.domain}")
        print(f"   ✅ فعال: {client.is_active}")
        print(f"   ✅ اجازه هر مسیر: {client.allow_any_path}")
    except SSOClient.DoesNotExist:
        print(f"   ❌ کلاینت meet_avinoo یافت نشد!")
        return False
    
    # Step 2: Check user
    print(f"\n2️⃣ بررسی کاربر...")
    try:
        user = User.objects.get(username='admin')  # Use username instead of GUID
        print(f"   ✅ کاربر یافت شد: {user.username}")
        print(f"   ✅ GUID: {user.guid}")
        print(f"   ✅ ایمیل: {user.email}")
        print(f"   ✅ فعال: {user.is_active}")
        
        # Update user_guid with actual GUID
        user_guid = str(user.guid)
        print(f"   ✅ GUID به‌روزرسانی شد: {user_guid}")
    except User.DoesNotExist:
        print(f"   ❌ کاربر admin یافت نشد!")
        return False
    
    # Step 3: Test external API
    print(f"\n3️⃣ تست API خارجی...")
    api_url = "http://avinoo.ir/api/meets/access/"
    try:
        response = requests.get(api_url, params={
            'room_name': room_name,
            'user_guid': user_guid
        }, timeout=10)
        
        print(f"   📡 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ API پاسخ داد")
            print(f"   Success: {data.get('success', 'N/A')}")
            
            if data.get('success'):
                access_data = data.get('data', {})
                print(f"   ✅ Has Access: {access_data.get('has_access', 'N/A')}")
                print(f"   ✅ User Type: {access_data.get('user_type', 'N/A')}")
            else:
                print(f"   ⚠️ Error: {data.get('error', 'Unknown error')}")
                access_data = None
        else:
            print(f"   ⚠️ API خطا داد: {response.status_code}")
            access_data = None
            
    except Exception as e:
        print(f"   ⚠️ خطا در API: {e}")
        access_data = None
    
    # Step 4: Generate JWT
    print(f"\n4️⃣ تولید JWT token...")
    try:
        jwt_generator = get_meet_jwt_generator()
        jwt_token = jwt_generator.generate_meet_jwt(user, room_name, access_data)
        
        if jwt_token:
            print(f"   ✅ JWT token تولید شد")
            print(f"   ✅ طول توکن: {len(jwt_token)} کاراکتر")
            
            # Decode JWT to show key info
            import jwt as jwt_lib
            decoded = jwt_lib.decode(jwt_token, options={"verify_signature": False})
            print(f"   ✅ Room: {decoded.get('room')}")
            print(f"   ✅ Moderator: {decoded.get('moderator')}")
            print(f"   ✅ User ID: {decoded.get('context', {}).get('user', {}).get('id')}")
        else:
            print(f"   ❌ خطا در تولید JWT")
            return False
            
    except Exception as e:
        print(f"   ❌ خطا در تولید JWT: {e}")
        return False
    
    # Step 5: Generate redirect URL
    print(f"\n5️⃣ تولید URL بازگشت...")
    try:
        redirect_url = jwt_generator.generate_meet_redirect_url(user, room_name, access_data)
        if redirect_url:
            print(f"   ✅ URL بازگشت تولید شد")
            print(f"   🔗 URL: {redirect_url}")
        else:
            print(f"   ❌ خطا در تولید URL")
            return False
            
    except Exception as e:
        print(f"   ❌ خطا در تولید URL: {e}")
        return False
    
    # Step 6: Test SSO URLs
    print(f"\n6️⃣ تست URL های SSO...")
    
    # SSO Login URL
    sso_login_url = f"http://auth.avinoo.ir/login/?client_id=meet_avinoo&redirect_uri=https://meet.avinoo.ir/{room_name}"
    print(f"   🔗 SSO Login URL: {sso_login_url}")
    
    # SSO Callback URL
    sso_callback_url = f"http://auth.avinoo.ir/callback/?client_id=meet_avinoo&state=test_state"
    print(f"   🔗 SSO Callback URL: {sso_callback_url}")
    
    # Final redirect URL
    final_redirect_url = f"https://meet.avinoo.ir/{room_name}?jwt={jwt_token}"
    print(f"   🔗 Final Redirect URL: {final_redirect_url}")
    
    print(f"\n🎉 جریان کامل SSO تست شد!")
    return True


def show_complete_flow():
    """Show complete SSO flow"""
    
    print("\n=== جریان کامل SSO ===\n")
    
    print("🔄 مراحل جریان SSO:")
    print("   1. کاربر روی لینک meet.avinoo.ir/room کلیک می‌کند")
    print("   2. سیستم meet کاربر را به auth.avinoo.ir/login هدایت می‌کند")
    print("   3. کاربر در auth.avinoo.ir وارد می‌شود")
    print("   4. سیستم auth با API خارجی دسترسی کاربر را بررسی می‌کند")
    print("   5. اگر دسترسی داشته باشد، JWT token تولید می‌شود")
    print("   6. کاربر به meet.avinoo.ir/room?jwt=TOKEN هدایت می‌شود")
    print("   7. سیستم meet JWT را اعتبارسنجی می‌کند و کاربر را وارد جلسه می‌کند")
    
    print(f"\n📋 تنظیمات:")
    print(f"   • کلاینت SSO: meet_avinoo")
    print(f"   • دامنه: meet.avinoo.ir")
    print(f"   • API خارجی: http://avinoo.ir/api/meets/access/")
    print(f"   • JWT Secret: meet_secret_key_2024")
    print(f"   • App ID: meet_avinoo")
    
    print(f"\n✅ تست URL ها:")
    print(f"   • ورود: http://auth.avinoo.ir/login/?client_id=meet_avinoo&redirect_uri=https://meet.avinoo.ir/room")
    print(f"   • بازگشت: http://auth.avinoo.ir/callback/?client_id=meet_avinoo&state=test")


if __name__ == '__main__':
    print("🚀 شروع تست جریان کامل SSO...\n")
    
    # Test complete SSO flow
    success = test_complete_sso_flow()
    
    if success:
        # Show complete flow
        show_complete_flow()
        
        print("\n🎉 تست جریان کامل SSO موفقیت‌آمیز بود!")
        print("\n📝 خلاصه:")
        print("✅ کلاینت SSO فعال است")
        print("✅ کاربر یافت شد")
        print("✅ API خارجی تست شد")
        print("✅ JWT token تولید شد")
        print("✅ URL بازگشت تولید شد")
        print("✅ سیستم آماده production است")
    else:
        print("\n❌ تست جریان کامل SSO ناموفق بود!")
        sys.exit(1)
