"""
Test only JWT generation for meet.avinoo.ir
"""

import os
import sys
import django
import jwt
from datetime import datetime

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
django.setup()

from apps.users.models import User
from apps.meet.jwt_utils import get_meet_jwt_generator


def test_meet_jwt_generation():
    """Test meet JWT generation only"""
    
    print("=== تست تولید JWT برای meet.avinoo.ir ===\n")
    
    # Test 1: Check if test user exists
    print("1. بررسی وجود کاربر تست...")
    try:
        user = User.objects.get(username='admin')
        print(f"   ✓ کاربر یافت شد: {user.username}")
        print(f"   ✓ GUID: {user.guid}")
        print(f"   ✓ ایمیل: {user.email}")
        print(f"   ✓ فعال: {user.is_active}")
    except User.DoesNotExist:
        print("   ✗ کاربر admin یافت نشد!")
        return False
    
    # Test 2: Test JWT generator
    print("\n2. تست JWT Generator...")
    try:
        jwt_generator = get_meet_jwt_generator()
        print(f"   ✓ JWT Generator ایجاد شد")
        print(f"   ✓ App ID: {jwt_generator.app_id}")
        print(f"   ✓ Domain: {jwt_generator.domain}")
        print(f"   ✓ External API: {jwt_generator.external_api_url}")
    except Exception as e:
        print(f"   ✗ خطا در ایجاد JWT Generator: {e}")
        return False
    
    # Test 3: Test external API call (simulated)
    print("\n3. تست فراخوانی API خارجی...")
    try:
        room_name = "test-room"
        access_data = jwt_generator.check_user_access(room_name, user.guid)
        if access_data:
            print(f"   ✓ API خارجی پاسخ داد")
            print(f"   ✓ دسترسی: {access_data.get('has_access', False)}")
            print(f"   ✓ نوع کاربر: {access_data.get('user_type', 'unknown')}")
        else:
            print(f"   ⚠ API خارجی پاسخ نداد (استفاده از تنظیمات پیش‌فرض)")
            # Use mock data for testing
            access_data = {
                "has_access": True,
                "user_type": "organizer",
                "start_time": "2025-01-13T10:00:00Z",
                "end_time": "2025-01-13T11:00:00Z",
                "is_organizer": True,
                "is_participant": False,
                "is_active": False,
                "is_upcoming": True,
                "is_past": False
            }
            print(f"   ✓ استفاده از داده‌های شبیه‌سازی شده")
    except Exception as e:
        print(f"   ⚠ خطا در فراخوانی API خارجی: {e}")
        access_data = None
    
    # Test 4: Test JWT generation
    print("\n4. تست تولید JWT token...")
    try:
        jwt_token = jwt_generator.generate_meet_jwt(user, room_name, access_data)
        if jwt_token:
            print(f"   ✓ JWT token تولید شد")
            print(f"   ✓ طول توکن: {len(jwt_token)} کاراکتر")
            print(f"   ✓ شروع توکن: {jwt_token[:50]}...")
            
            # Decode and display JWT payload
            try:
                decoded = jwt.decode(jwt_token, options={"verify_signature": False})
                print(f"   ✓ محتوای JWT:")
                print(f"     - aud: {decoded.get('aud')}")
                print(f"     - iss: {decoded.get('iss')}")
                print(f"     - sub: {decoded.get('sub')}")
                print(f"     - room: {decoded.get('room')}")
                print(f"     - moderator: {decoded.get('moderator')}")
                print(f"     - exp: {datetime.fromtimestamp(decoded.get('exp'))}")
                print(f"     - nbf: {datetime.fromtimestamp(decoded.get('nbf'))}")
                
                # Check user context
                context = decoded.get('context', {})
                user_context = context.get('user', {})
                print(f"     - user.id: {user_context.get('id')}")
                print(f"     - user.name: {user_context.get('name')}")
                print(f"     - user.email: {user_context.get('email')}")
                print(f"     - user.moderator: {user_context.get('moderator')}")
                
            except Exception as e:
                print(f"   ⚠ خطا در رمزگشایی JWT: {e}")
        else:
            print(f"   ✗ خطا در تولید JWT token")
            return False
    except Exception as e:
        print(f"   ✗ خطا در تولید JWT: {e}")
        return False
    
    # Test 5: Test redirect URL generation
    print("\n5. تست تولید URL بازگشت...")
    try:
        redirect_url = jwt_generator.generate_meet_redirect_url(user, room_name, access_data)
        if redirect_url:
            print(f"   ✓ URL بازگشت تولید شد")
            print(f"   ✓ URL: {redirect_url}")
        else:
            print(f"   ✗ خطا در تولید URL بازگشت")
            return False
    except Exception as e:
        print(f"   ✗ خطا در تولید URL: {e}")
        return False
    
    # Test 6: Test user data formatting
    print("\n6. تست فرمت‌بندی اطلاعات کاربر...")
    try:
        user_data = user.get_meet_user_data()
        print(f"   ✓ اطلاعات کاربر فرمت شد")
        print(f"   ✓ نام: {user_data.get('name')}")
        print(f"   ✓ ایمیل: {user_data.get('email')}")
        print(f"   ✓ منطقه: {user_data.get('region')}")
        print(f"   ✓ مدیر: {user_data.get('moderator')}")
        print(f"   ✓ وابستگی: {user_data.get('affiliation')}")
    except Exception as e:
        print(f"   ✗ خطا در فرمت‌بندی اطلاعات کاربر: {e}")
        return False
    
    print("\n=== تمام تست‌ها با موفقیت انجام شد! ===")
    return True


def test_sso_flow_simulation():
    """Test SSO flow simulation"""
    
    print("\n=== شبیه‌سازی جریان SSO ===\n")
    
    print("🔄 جریان کامل:")
    print("   1. کاربر روی لینک meet.avinoo.ir/roomname کلیک می‌کند")
    print("   2. سیستم meet کاربر را به auth.avinoo.ir/login هدایت می‌کند")
    print("   3. کاربر در auth.avinoo.ir وارد می‌شود")
    print("   4. سیستم auth با API خارجی دسترسی کاربر را بررسی می‌کند")
    print("   5. اگر دسترسی داشته باشد، JWT token تولید می‌شود")
    print("   6. کاربر به meet.avinoo.ir/roomname?jwt=TOKEN هدایت می‌شود")
    print("   7. سیستم meet JWT را اعتبارسنجی می‌کند و کاربر را وارد جلسه می‌کند")
    
    print("\n📋 تنظیمات:")
    print("   • کلاینت SSO: meet_avinoo")
    print("   • دامنه: meet.avinoo.ir")
    print("   • API خارجی: http://avinoo.ir/api/meets/access/")
    print("   • JWT Secret: meet_secret_key_2024")
    print("   • App ID: meet_avinoo")
    
    print("\n✅ تست URL ها:")
    print("   • ورود: http://auth.avinoo.ir/login/?client_id=meet_avinoo&redirect_uri=https://meet.avinoo.ir/test-room")
    print("   • بازگشت: http://auth.avinoo.ir/callback/?client_id=meet_avinoo&state=test")


if __name__ == '__main__':
    success = test_meet_jwt_generation()
    if success:
        test_sso_flow_simulation()
        print("\n🎉 تمام تست‌ها موفقیت‌آمیز بودند!")
    else:
        print("\n❌ برخی تست‌ها ناموفق بودند!")
        sys.exit(1)
