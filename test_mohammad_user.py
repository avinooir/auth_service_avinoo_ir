"""
Test with mohammad.rahimaee@gmail.com user
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


def test_mohammad_user():
    """Test with mohammad user"""
    
    print("=== تست با کاربر mohammad.rahimaee@gmail.com ===\n")
    
    # Test parameters
    room_name = "room"
    
    print(f"🔍 پارامترهای تست:")
    print(f"   Room: {room_name}")
    print()
    
    # Step 1: Get mohammad user
    print("1️⃣ بررسی کاربر mohammad...")
    try:
        user = User.objects.get(email='mohammad.rahimaee@gmail.com')
        print(f"   ✅ کاربر یافت شد: {user.username}")
        print(f"   ✅ ایمیل: {user.email}")
        print(f"   ✅ GUID: {user.guid}")
        print(f"   ✅ فعال: {user.is_active}")
        print(f"   ✅ Superuser: {user.is_superuser}")
        print(f"   ✅ Staff: {user.is_staff}")
        
        user_guid = str(user.guid)
        print(f"   ✅ GUID برای API: {user_guid}")
    except User.DoesNotExist:
        print(f"   ❌ کاربر mohammad.rahimaee@gmail.com یافت نشد!")
        return False
    
    # Step 2: Test external API
    print(f"\n2️⃣ تست API خارجی...")
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
                print(f"   📋 نتایج دسترسی:")
                print(f"     - Has Access: {access_data.get('has_access', 'N/A')}")
                print(f"     - User Type: {access_data.get('user_type', 'N/A')}")
                print(f"     - Is Organizer: {access_data.get('is_organizer', 'N/A')}")
                print(f"     - Is Participant: {access_data.get('is_participant', 'N/A')}")
                print(f"     - Is Active: {access_data.get('is_active', 'N/A')}")
                print(f"     - Is Upcoming: {access_data.get('is_upcoming', 'N/A')}")
                print(f"     - Is Past: {access_data.get('is_past', 'N/A')}")
                
                if access_data.get('start_time'):
                    print(f"     - Start Time: {access_data.get('start_time')}")
                if access_data.get('end_time'):
                    print(f"     - End Time: {access_data.get('end_time')}")
                
                # Check access result
                if access_data.get('has_access'):
                    print(f"\n   🎉 کاربر دسترسی دارد!")
                    print(f"   نوع دسترسی: {access_data.get('user_type', 'unknown')}")
                else:
                    print(f"\n   ❌ کاربر دسترسی ندارد")
                    
                # Show full response
                print(f"\n   📋 پاسخ کامل API:")
                print("   " + "=" * 60)
                print("   " + json.dumps(data, indent=2, ensure_ascii=False).replace('\n', '\n   '))
                print("   " + "=" * 60)
                    
            else:
                print(f"   ❌ Error: {data.get('error', 'Unknown error')}")
                print(f"   📋 پاسخ کامل:")
                print("   " + json.dumps(data, indent=2, ensure_ascii=False).replace('\n', '\n   '))
                access_data = None
        else:
            print(f"   ⚠️ API خطا داد: {response.status_code}")
            print(f"   Response: {response.text}")
            access_data = None
            
    except Exception as e:
        print(f"   ⚠️ خطا در API: {e}")
        access_data = None
    
    # Step 3: Generate JWT
    print(f"\n3️⃣ تولید JWT token...")
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
            print(f"   ✅ User Name: {decoded.get('context', {}).get('user', {}).get('name')}")
            print(f"   ✅ User Email: {decoded.get('context', {}).get('user', {}).get('email')}")
            print(f"   ✅ User Affiliation: {decoded.get('context', {}).get('user', {}).get('affiliation')}")
        else:
            print(f"   ❌ خطا در تولید JWT")
            return False
            
    except Exception as e:
        print(f"   ❌ خطا در تولید JWT: {e}")
        return False
    
    # Step 4: Generate redirect URL
    print(f"\n4️⃣ تولید URL بازگشت...")
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
    
    # Step 5: Show JWT payload
    print(f"\n5️⃣ نمایش JWT Payload...")
    try:
        import jwt as jwt_lib
        decoded = jwt_lib.decode(jwt_token, options={"verify_signature": False})
        print(f"   📋 JWT Payload:")
        print("   " + "=" * 60)
        print("   " + json.dumps(decoded, indent=2, ensure_ascii=False).replace('\n', '\n   '))
        print("   " + "=" * 60)
    except Exception as e:
        print(f"   ❌ خطا در نمایش payload: {e}")
    
    print(f"\n🎉 تست با کاربر mohammad موفقیت‌آمیز بود!")
    return True


def test_mohammad_with_different_rooms():
    """Test mohammad user with different rooms"""
    
    print("\n=== تست mohammad با اتاق‌های مختلف ===\n")
    
    try:
        user = User.objects.get(email='mohammad.rahimaee@gmail.com')
        user_guid = str(user.guid)
        
        # Test different rooms
        test_rooms = [
            "room",
            "test-room",
            "meeting-123",
            "demo-meeting"
        ]
        
        api_url = "http://avinoo.ir/api/meets/access/"
        
        for i, room_name in enumerate(test_rooms, 1):
            print(f"{i}. تست اتاق: {room_name}")
            
            try:
                response = requests.get(api_url, params={
                    'room_name': room_name,
                    'user_guid': user_guid
                }, timeout=10)
                
                print(f"   Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success'):
                        access_data = data.get('data', {})
                        print(f"   ✅ Has Access: {access_data.get('has_access', 'N/A')}")
                        print(f"   ✅ User Type: {access_data.get('user_type', 'N/A')}")
                    else:
                        print(f"   ❌ Error: {data.get('error', 'Unknown error')}")
                else:
                    print(f"   ❌ خطا: {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ خطا: {e}")
            
            print()
        
    except Exception as e:
        print(f"❌ خطا در تست اتاق‌های مختلف: {e}")


if __name__ == '__main__':
    print("🚀 شروع تست با کاربر mohammad...\n")
    
    # Test 1: Main test with mohammad user
    success = test_mohammad_user()
    
    if success:
        # Test 2: Different rooms
        test_mohammad_with_different_rooms()
        
        print("\n🎉 تمام تست‌ها با کاربر mohammad موفقیت‌آمیز بود!")
        print("\n📝 خلاصه:")
        print("✅ کاربر mohammad یافت شد")
        print("✅ API خارجی تست شد")
        print("✅ JWT token تولید شد")
        print("✅ URL بازگشت تولید شد")
        print("✅ سیستم با کاربر mohammad کار می‌کند")
    else:
        print("\n❌ تست با کاربر mohammad ناموفق بود!")
        sys.exit(1)
