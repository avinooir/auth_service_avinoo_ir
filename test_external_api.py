"""
Test external API for meet access
"""

import requests
import json
from datetime import datetime


def test_external_api():
    """Test external API for meet access"""
    
    print("=== تست API خارجی meet access ===\n")
    
    # API URL
    api_url = "http://avinoo.ir/api/meets/access/"
    
    # Test parameters
    test_cases = [
        {
            "room_name": "test-room",
            "user_guid": "6f99b0b3-33e7-49da-8ce9-7b1b7450c2bb",  # admin user GUID
            "description": "تست با کاربر admin"
        },
        {
            "room_name": "meeting-123",
            "user_guid": "6f99b0b3-33e7-49da-8ce9-7b1b7450c2bb",
            "description": "تست با اتاق meeting-123"
        },
        {
            "room_name": "invalid-room",
            "user_guid": "6f99b0b3-33e7-49da-8ce9-7b1b7450c2bb",
            "description": "تست با اتاق نامعتبر"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"{i}. {test_case['description']}")
        print(f"   Room: {test_case['room_name']}")
        print(f"   User GUID: {test_case['user_guid']}")
        
        try:
            # Make API request
            response = requests.get(api_url, params={
                'room_name': test_case['room_name'],
                'user_guid': test_case['user_guid']
            }, timeout=10)
            
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"   ✓ پاسخ JSON دریافت شد")
                    print(f"   Success: {data.get('success', 'N/A')}")
                    
                    if data.get('success'):
                        access_data = data.get('data', {})
                        print(f"   Has Access: {access_data.get('has_access', 'N/A')}")
                        print(f"   User Type: {access_data.get('user_type', 'N/A')}")
                        print(f"   Is Organizer: {access_data.get('is_organizer', 'N/A')}")
                        print(f"   Is Participant: {access_data.get('is_participant', 'N/A')}")
                        print(f"   Is Active: {access_data.get('is_active', 'N/A')}")
                        print(f"   Is Upcoming: {access_data.get('is_upcoming', 'N/A')}")
                        print(f"   Is Past: {access_data.get('is_past', 'N/A')}")
                        
                        if access_data.get('start_time'):
                            print(f"   Start Time: {access_data.get('start_time')}")
                        if access_data.get('end_time'):
                            print(f"   End Time: {access_data.get('end_time')}")
                    else:
                        print(f"   Error: {data.get('error', 'Unknown error')}")
                        
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


def test_api_with_different_guids():
    """Test API with different user GUIDs"""
    
    print("=== تست API با GUID های مختلف ===\n")
    
    api_url = "http://avinoo.ir/api/meets/access/"
    room_name = "test-room"
    
    # Test different GUIDs
    test_guids = [
        "6f99b0b3-33e7-49da-8ce9-7b1b7450c2bb",  # admin user
        "00000000-0000-0000-0000-000000000000",  # invalid GUID
        "12345678-1234-1234-1234-123456789012",  # random GUID
    ]
    
    for i, user_guid in enumerate(test_guids, 1):
        print(f"{i}. تست با GUID: {user_guid}")
        
        try:
            response = requests.get(api_url, params={
                'room_name': room_name,
                'user_guid': user_guid
            }, timeout=10)
            
            print(f"   Status Code: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get('success'):
                        access_data = data.get('data', {})
                        print(f"   ✓ Has Access: {access_data.get('has_access', 'N/A')}")
                        print(f"   ✓ User Type: {access_data.get('user_type', 'N/A')}")
                    else:
                        print(f"   ✗ Error: {data.get('error', 'Unknown error')}")
                except json.JSONDecodeError:
                    print(f"   ✗ پاسخ JSON نامعتبر")
            else:
                print(f"   ✗ خطا: {response.status_code}")
                
        except Exception as e:
            print(f"   ✗ خطا: {str(e)}")
        
        print()
    
    return True


def test_api_response_format():
    """Test API response format"""
    
    print("=== تست فرمت پاسخ API ===\n")
    
    api_url = "http://avinoo.ir/api/meets/access/"
    
    try:
        response = requests.get(api_url, params={
            'room_name': 'test-room',
            'user_guid': '6f99b0b3-33e7-49da-8ce9-7b1b7450c2bb'
        }, timeout=10)
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("📋 فرمت پاسخ API:")
                print("=" * 50)
                print(json.dumps(data, indent=2, ensure_ascii=False))
                print("=" * 50)
                
                # Check required fields
                print("\n✅ بررسی فیلدهای مورد نیاز:")
                required_fields = ['success', 'data']
                for field in required_fields:
                    if field in data:
                        print(f"✓ {field}: موجود")
                    else:
                        print(f"✗ {field}: موجود نیست")
                
                if data.get('data'):
                    data_fields = ['has_access', 'user_type', 'start_time', 'end_time', 
                                 'is_organizer', 'is_participant', 'is_active', 
                                 'is_upcoming', 'is_past']
                    for field in data_fields:
                        if field in data['data']:
                            print(f"✓ data.{field}: موجود")
                        else:
                            print(f"✗ data.{field}: موجود نیست")
                
            except json.JSONDecodeError:
                print("✗ پاسخ JSON نامعتبر")
        else:
            print(f"✗ خطا در درخواست: {response.status_code}")
            
    except Exception as e:
        print(f"✗ خطا: {str(e)}")
    
    return True


if __name__ == '__main__':
    print("🚀 شروع تست API خارجی...\n")
    
    # Test 1: Basic API functionality
    test_external_api()
    
    # Test 2: Different GUIDs
    test_api_with_different_guids()
    
    # Test 3: Response format
    test_api_response_format()
    
    print("🎉 تست API خارجی تکمیل شد!")
