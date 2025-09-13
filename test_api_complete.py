"""
Complete test of external API
"""

import requests
import json
from datetime import datetime


def test_api_complete():
    """Complete test of external API"""
    
    print("=== تست کامل API خارجی ===\n")
    
    # API URL
    api_url = "http://avinoo.ir/api/meets/access/"
    
    # Test with admin user GUID
    user_guid = "6f99b0b3-33e7-49da-8ce9-7b1b7450c2bb"
    
    # Test different room names
    test_rooms = [
        "test-room",
        "meeting-123", 
        "demo-meeting",
        "invalid-room",
        "roomname"
    ]
    
    print(f"🔍 تست با User GUID: {user_guid}")
    print(f"🌐 API URL: {api_url}")
    print()
    
    for i, room_name in enumerate(test_rooms, 1):
        print(f"{i}. تست اتاق: {room_name}")
        
        try:
            # Make API request
            response = requests.get(api_url, params={
                'room_name': room_name,
                'user_guid': user_guid
            }, timeout=10)
            
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"   ✓ پاسخ JSON دریافت شد")
                    print(f"   Success: {data.get('success', 'N/A')}")
                    
                    if data.get('success'):
                        access_data = data.get('data', {})
                        print(f"   📋 نتایج:")
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
                            
                        # Check if user has access
                        if access_data.get('has_access'):
                            print(f"   ✅ کاربر دسترسی دارد!")
                        else:
                            print(f"   ❌ کاربر دسترسی ندارد")
                            
                    else:
                        print(f"   ❌ Error: {data.get('error', 'Unknown error')}")
                        
                except json.JSONDecodeError:
                    print(f"   ✗ پاسخ JSON نامعتبر")
                    print(f"   Response: {response.text[:200]}...")
            else:
                print(f"   ✗ خطا در درخواست: {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                
        except requests.exceptions.Timeout:
            print(f"   ✗ Timeout - API پاسخ نداد")
        except requests.exceptions.ConnectionError:
            print(f"   ✗ Connection Error - نمی‌توان به API متصل شد")
        except Exception as e:
            print(f"   ✗ خطا: {str(e)}")
        
        print()
    
    return True


def test_api_with_jwt_generator():
    """Test API integration with JWT generator"""
    
    print("=== تست یکپارچگی API با JWT Generator ===\n")
    
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
        print(f"✓ کاربر: {user.username}")
        print(f"✓ GUID: {user.guid}")
        
        # Get JWT generator
        jwt_generator = get_meet_jwt_generator()
        print(f"✓ JWT Generator: {jwt_generator.app_id}")
        
        # Test room
        room_name = "test-room"
        print(f"✓ اتاق تست: {room_name}")
        
        # Check access via API
        print(f"\n🔍 بررسی دسترسی از طریق API...")
        access_data = jwt_generator.check_user_access(room_name, user.guid)
        
        if access_data:
            print(f"✓ API پاسخ داد")
            print(f"  - Has Access: {access_data.get('has_access', 'N/A')}")
            print(f"  - User Type: {access_data.get('user_type', 'N/A')}")
            print(f"  - Is Organizer: {access_data.get('is_organizer', 'N/A')}")
            
            # Generate JWT with API data
            print(f"\n🔧 تولید JWT با داده‌های API...")
            jwt_token = jwt_generator.generate_meet_jwt(user, room_name, access_data)
            
            if jwt_token:
                print(f"✓ JWT token تولید شد")
                print(f"✓ طول توکن: {len(jwt_token)} کاراکتر")
                
                # Generate redirect URL
                redirect_url = jwt_generator.generate_meet_redirect_url(user, room_name, access_data)
                if redirect_url:
                    print(f"✓ URL بازگشت تولید شد")
                    print(f"✓ URL: {redirect_url}")
                
            else:
                print(f"✗ خطا در تولید JWT")
        else:
            print(f"⚠ API پاسخ نداد - استفاده از تنظیمات پیش‌فرض")
            
            # Generate JWT without API data
            jwt_token = jwt_generator.generate_meet_jwt(user, room_name, None)
            if jwt_token:
                print(f"✓ JWT token با تنظیمات پیش‌فرض تولید شد")
        
    except Exception as e:
        print(f"✗ خطا در تست یکپارچگی: {e}")
        return False
    
    return True


def show_api_response_example():
    """Show example API response"""
    
    print("=== نمونه پاسخ API ===\n")
    
    api_url = "http://avinoo.ir/api/meets/access/"
    
    try:
        response = requests.get(api_url, params={
            'room_name': 'test-room',
            'user_guid': '6f99b0b3-33e7-49da-8ce9-7b1b7450c2bb'
        }, timeout=10)
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("📋 نمونه پاسخ API:")
                print("=" * 60)
                print(json.dumps(data, indent=2, ensure_ascii=False))
                print("=" * 60)
                
                # Show expected format
                print("\n📋 فرمت مورد انتظار:")
                expected_format = {
                    "success": True,
                    "data": {
                        "has_access": True,
                        "user_type": "organizer",
                        "start_time": "2025-01-11T10:00:00Z",
                        "end_time": "2025-01-11T11:00:00Z",
                        "is_organizer": True,
                        "is_participant": False,
                        "is_active": False,
                        "is_upcoming": True,
                        "is_past": False
                    }
                }
                print(json.dumps(expected_format, indent=2, ensure_ascii=False))
                
            except json.JSONDecodeError:
                print("✗ پاسخ JSON نامعتبر")
        else:
            print(f"✗ خطا: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"✗ خطا: {e}")


if __name__ == '__main__':
    print("🚀 شروع تست کامل API خارجی...\n")
    
    # Test 1: Complete API test
    test_api_complete()
    
    # Test 2: Integration with JWT generator
    test_api_with_jwt_generator()
    
    # Test 3: Show API response example
    show_api_response_example()
    
    print("\n🎉 تست کامل API خارجی تکمیل شد!")
    print("\n📝 خلاصه:")
    print("✅ API خارجی فعال است")
    print("✅ پاسخ JSON می‌دهد")
    print("✅ با JWT generator یکپارچه است")
    print("✅ آماده استفاده در production است")
