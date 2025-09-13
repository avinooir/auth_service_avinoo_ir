"""
Show complete URL with JWT token
"""

import os
import sys
import django
import jwt
import json
from datetime import datetime

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
django.setup()

from apps.users.models import User
from apps.meet.jwt_utils import get_meet_jwt_generator


def show_url_with_token():
    """Show complete URL with JWT token"""
    
    print("=== نمایش URL کامل با JWT Token ===\n")
    
    try:
        # Get mohammad user
        user = User.objects.get(email='mohammad.rahimaee@gmail.com')
        print(f"✅ کاربر: {user.username}")
        print(f"✅ ایمیل: {user.email}")
        print(f"✅ GUID: {user.guid}")
        
        # Get JWT generator
        jwt_generator = get_meet_jwt_generator()
        print(f"✅ JWT Generator: {jwt_generator.app_id}")
        
        # Test room
        room_name = "room"
        print(f"✅ اتاق: {room_name}")
        
        # Generate JWT token
        jwt_token = jwt_generator.generate_meet_jwt(user, room_name, None)
        
        if jwt_token:
            print(f"✅ JWT token تولید شد")
            print(f"✅ طول توکن: {len(jwt_token)} کاراکتر")
            
            # Generate complete URL
            complete_url = f"https://meet.avinoo.ir/{room_name}?jwt={jwt_token}"
            
            print(f"\n🔗 URL کامل با توکن:")
            print("=" * 80)
            print(complete_url)
            print("=" * 80)
            
            # Decode JWT to show payload
            decoded = jwt.decode(jwt_token, options={"verify_signature": False})
            print(f"\n📋 محتوای JWT:")
            print(f"   - aud: {decoded.get('aud')}")
            print(f"   - iss: {decoded.get('iss')}")
            print(f"   - sub: {decoded.get('sub')}")
            print(f"   - room: {decoded.get('room')}")
            print(f"   - moderator: {decoded.get('moderator')}")
            print(f"   - exp: {datetime.fromtimestamp(decoded.get('exp'))}")
            print(f"   - nbf: {datetime.fromtimestamp(decoded.get('nbf'))}")
            
            # Show user info
            user_context = decoded.get('context', {}).get('user', {})
            print(f"\n👤 اطلاعات کاربر:")
            print(f"   - ID: {user_context.get('id')}")
            print(f"   - Name: {user_context.get('name')}")
            print(f"   - Email: {user_context.get('email')}")
            print(f"   - Affiliation: {user_context.get('affiliation')}")
            print(f"   - Moderator: {user_context.get('moderator')}")
            print(f"   - Region: {user_context.get('region')}")
            print(f"   - Display Name: {user_context.get('displayName')}")
            
            # Show features
            features = decoded.get('context', {}).get('features', {})
            print(f"\n⚙️ ویژگی‌ها:")
            print(f"   - Livestreaming: {features.get('livestreaming')}")
            print(f"   - Recording: {features.get('recording')}")
            print(f"   - Screen Sharing: {features.get('screen-sharing')}")
            print(f"   - Etherpad: {features.get('etherpad')}")
            print(f"   - Transcription: {features.get('transcription')}")
            print(f"   - Breakout Rooms: {features.get('breakout-rooms')}")
            
            # Show identity
            identity = decoded.get('identity', {})
            print(f"\n🆔 هویت:")
            print(f"   - Type: {identity.get('type')}")
            print(f"   - Guest: {identity.get('guest')}")
            print(f"   - External ID: {identity.get('externalId')}")
            
            # Show custom settings
            custom = decoded.get('custom', {})
            print(f"\n🎨 تنظیمات سفارشی:")
            print(f"   - Theme: {custom.get('theme')}")
            print(f"   - Allow Knocking: {custom.get('allowKnocking')}")
            print(f"   - Enable Polls: {custom.get('enablePolls')}")
            
            print(f"\n🎉 URL کامل با توکن آماده است!")
            
        else:
            print(f"❌ خطا در تولید JWT token")
            return False
            
    except Exception as e:
        print(f"❌ خطا: {e}")
        return False
    
    return True


def show_url_for_different_rooms():
    """Show URLs for different rooms"""
    
    print("\n=== نمایش URL برای اتاق‌های مختلف ===\n")
    
    try:
        # Get mohammad user
        user = User.objects.get(email='mohammad.rahimaee@gmail.com')
        jwt_generator = get_meet_jwt_generator()
        
        # Test different rooms
        test_rooms = [
            "room",
            "test-room",
            "meeting-123",
            "demo-meeting"
        ]
        
        for i, room_name in enumerate(test_rooms, 1):
            print(f"{i}. اتاق: {room_name}")
            
            # Generate JWT token
            jwt_token = jwt_generator.generate_meet_jwt(user, room_name, None)
            
            if jwt_token:
                # Generate complete URL
                complete_url = f"https://meet.avinoo.ir/{room_name}?jwt={jwt_token}"
                print(f"   🔗 URL: {complete_url}")
            else:
                print(f"   ❌ خطا در تولید توکن")
            
            print()
        
    except Exception as e:
        print(f"❌ خطا: {e}")


if __name__ == '__main__':
    print("🚀 نمایش URL کامل با JWT Token...\n")
    
    # Show main URL with token
    success = show_url_with_token()
    
    if success:
        # Show URLs for different rooms
        show_url_for_different_rooms()
        
        print("🎉 نمایش URL ها تکمیل شد!")
    else:
        print("❌ خطا در نمایش URL!")
        sys.exit(1)
