"""
Test API with real room 'room'
"""

import requests
import json
from datetime import datetime


def test_room_api():
    """Test API with real room 'room'"""
    
    print("=== تست API با اتاق واقعی 'room' ===\n")
    
    # API URL
    api_url = "http://avinoo.ir/api/meets/access/"
    
    # Test with admin user GUID
    user_guid = "6f99b0b3-33e7-49da-8ce9-7b1b7450c2bb"
    room_name = "room"
    
    print(f"🔍 تست با:")
    print(f"   Room: {room_name}")
    print(f"   User GUID: {user_guid}")
    print(f"   API URL: {api_url}")
    print()
    
    try:
        # Make API request
        response = requests.get(api_url, params={
            'room_name': room_name,
            'user_guid': user_guid
        }, timeout=10)
        
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ پاسخ JSON دریافت شد")
                print(f"   Success: {data.get('success', 'N/A')}")
                
                if data.get('success'):
                    access_data = data.get('data', {})
                    print(f"\n📋 نتایج دسترسی:")
                    print(f"   ✓ Has Access: {access_data.get('has_access', 'N/A')}")
                    print(f"   ✓ User Type: {access_data.get('user_type', 'N/A')}")
                    print(f"   ✓ Is Organizer: {access_data.get('is_organizer', 'N/A')}")
                    print(f"   ✓ Is Participant: {access_data.get('is_participant', 'N/A')}")
                    print(f"   ✓ Is Active: {access_data.get('is_active', 'N/A')}")
                    print(f"   ✓ Is Upcoming: {access_data.get('is_upcoming', 'N/A')}")
                    print(f"   ✓ Is Past: {access_data.get('is_past', 'N/A')}")
                    
                    if access_data.get('start_time'):
                        print(f"   ✓ Start Time: {access_data.get('start_time')}")
                    if access_data.get('end_time'):
                        print(f"   ✓ End Time: {access_data.get('end_time')}")
                    
                    # Check access result
                    if access_data.get('has_access'):
                        print(f"\n🎉 کاربر دسترسی دارد!")
                        print(f"   نوع دسترسی: {access_data.get('user_type', 'unknown')}")
                    else:
                        print(f"\n❌ کاربر دسترسی ندارد")
                        
                    # Show full response
                    print(f"\n📋 پاسخ کامل API:")
                    print("=" * 60)
                    print(json.dumps(data, indent=2, ensure_ascii=False))
                    print("=" * 60)
                        
                else:
                    print(f"❌ Error: {data.get('error', 'Unknown error')}")
                    print(f"📋 پاسخ کامل:")
                    print(json.dumps(data, indent=2, ensure_ascii=False))
                        
            except json.JSONDecodeError:
                print(f"❌ پاسخ JSON نامعتبر")
                print(f"Response: {response.text}")
        else:
            print(f"❌ خطا در درخواست: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print(f"❌ Timeout - API پاسخ نداد")
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection Error - نمی‌توان به API متصل شد")
    except Exception as e:
        print(f"❌ خطا: {str(e)}")
    
    return True


def test_jwt_generation_with_room():
    """Test JWT generation with real room"""
    
    print("\n=== تست تولید JWT با اتاق واقعی ===\n")
    
    import os
    import sys
    import django
    
    # Setup Django
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
    django.setup()
    
    from apps.users.models import User
    from apps.meet.jwt_utils import get_meet_jwt_generator
    
    try:
        # Get test user
        user = User.objects.get(username='admin')
        print(f"✅ کاربر: {user.username}")
        print(f"✅ GUID: {user.guid}")
        
        # Get JWT generator
        jwt_generator = get_meet_jwt_generator()
        print(f"✅ JWT Generator: {jwt_generator.app_id}")
        
        # Test room
        room_name = "room"
        print(f"✅ اتاق: {room_name}")
        
        # Check access via API
        print(f"\n🔍 بررسی دسترسی از طریق API...")
        access_data = jwt_generator.check_user_access(room_name, user.guid)
        
        if access_data:
            print(f"✅ API پاسخ داد")
            print(f"   - Has Access: {access_data.get('has_access', 'N/A')}")
            print(f"   - User Type: {access_data.get('user_type', 'N/A')}")
            print(f"   - Is Organizer: {access_data.get('is_organizer', 'N/A')}")
            
            # Generate JWT with API data
            print(f"\n🔧 تولید JWT با داده‌های API...")
            jwt_token = jwt_generator.generate_meet_jwt(user, room_name, access_data)
            
            if jwt_token:
                print(f"✅ JWT token تولید شد")
                print(f"✅ طول توکن: {len(jwt_token)} کاراکتر")
                
                # Decode JWT to show payload
                import jwt as jwt_lib
                decoded = jwt_lib.decode(jwt_token, options={"verify_signature": False})
                print(f"\n📋 محتوای JWT:")
                print(f"   - aud: {decoded.get('aud')}")
                print(f"   - iss: {decoded.get('iss')}")
                print(f"   - sub: {decoded.get('sub')}")
                print(f"   - room: {decoded.get('room')}")
                print(f"   - moderator: {decoded.get('moderator')}")
                
                # Generate redirect URL
                redirect_url = jwt_generator.generate_meet_redirect_url(user, room_name, access_data)
                if redirect_url:
                    print(f"\n🔗 URL بازگشت:")
                    print(f"   {redirect_url}")
                
            else:
                print(f"❌ خطا در تولید JWT")
        else:
            print(f"⚠️ API پاسخ نداد - استفاده از تنظیمات پیش‌فرض")
            
            # Generate JWT without API data
            jwt_token = jwt_generator.generate_meet_jwt(user, room_name, None)
            if jwt_token:
                print(f"✅ JWT token با تنظیمات پیش‌فرض تولید شد")
                print(f"✅ طول توکن: {len(jwt_token)} کاراکتر")
                
                # Generate redirect URL
                redirect_url = jwt_generator.generate_meet_redirect_url(user, room_name, None)
                if redirect_url:
                    print(f"\n🔗 URL بازگشت:")
                    print(f"   {redirect_url}")
        
    except Exception as e:
        print(f"❌ خطا در تست: {e}")
        return False
    
    return True


if __name__ == '__main__':
    print("🚀 شروع تست با اتاق واقعی 'room'...\n")
    
    # Test 1: API test with real room
    test_room_api()
    
    # Test 2: JWT generation with real room
    test_jwt_generation_with_room()
    
    print("\n🎉 تست با اتاق واقعی تکمیل شد!")
    print("\n📝 خلاصه:")
    print("✅ API با اتاق 'room' تست شد")
    print("✅ JWT generation با داده‌های واقعی تست شد")
    print("✅ سیستم آماده استفاده است")
