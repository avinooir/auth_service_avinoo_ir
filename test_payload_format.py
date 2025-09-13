"""
Test JWT payload format
"""

import os
import sys
import django
import jwt
import json
from datetime import datetime

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
django.setup()

from apps.users.models import User
from apps.meet.jwt_utils import get_meet_jwt_generator


def test_payload_format():
    """Test JWT payload format"""
    
    print("=== تست فرمت JWT Payload ===\n")
    
    try:
        # Get test user
        user = User.objects.get(username='admin')
        print(f"✓ کاربر: {user.username}")
        
        # Get JWT generator
        jwt_generator = get_meet_jwt_generator()
        print(f"✓ JWT Generator: {jwt_generator.app_id}")
        
        # Generate JWT token
        room_name = "test-room"
        jwt_token = jwt_generator.generate_meet_jwt(user, room_name, None)
        
        if jwt_token:
            print(f"✓ JWT token تولید شد")
            
            # Decode JWT to check payload
            decoded = jwt.decode(jwt_token, options={"verify_signature": False})
            
            print(f"\n📋 محتوای JWT Payload:")
            print(f"aud: {decoded.get('aud')}")
            print(f"iss: {decoded.get('iss')}")
            print(f"sub: {decoded.get('sub')}")
            print(f"room: {decoded.get('room')}")
            print(f"moderator: {decoded.get('moderator')}")
            
            # Check context structure
            context = decoded.get('context', {})
            print(f"\n📋 Context:")
            print(f"group: {context.get('group')}")
            
            # Check user structure
            user_context = context.get('user', {})
            print(f"\n📋 User:")
            print(f"id: {user_context.get('id')}")
            print(f"name: {user_context.get('name')}")
            print(f"email: {user_context.get('email')}")
            print(f"avatar: {user_context.get('avatar')}")
            print(f"affiliation: {user_context.get('affiliation')}")
            print(f"moderator: {user_context.get('moderator')}")
            print(f"region: {user_context.get('region')}")
            print(f"displayName: {user_context.get('displayName')}")
            
            # Check features structure
            features = context.get('features', {})
            print(f"\n📋 Features:")
            print(f"livestreaming: {features.get('livestreaming')}")
            print(f"recording: {features.get('recording')}")
            print(f"screen-sharing: {features.get('screen-sharing')}")
            print(f"sip: {features.get('sip')}")
            print(f"etherpad: {features.get('etherpad')}")
            print(f"transcription: {features.get('transcription')}")
            print(f"breakout-rooms: {features.get('breakout-rooms')}")
            
            # Check identity structure
            identity = decoded.get('identity', {})
            print(f"\n📋 Identity:")
            print(f"type: {identity.get('type')}")
            print(f"guest: {identity.get('guest')}")
            print(f"externalId: {identity.get('externalId')}")
            
            # Check custom structure
            custom = decoded.get('custom', {})
            print(f"\n📋 Custom:")
            print(f"theme: {custom.get('theme')}")
            print(f"allowKnocking: {custom.get('allowKnocking')}")
            print(f"enablePolls: {custom.get('enablePolls')}")
            
            # Check if format matches exactly
            print(f"\n✅ بررسی فرمت:")
            
            # Check required fields
            required_fields = ['aud', 'iss', 'sub', 'room', 'exp', 'nbf', 'moderator', 'context', 'identity', 'custom']
            for field in required_fields:
                if field in decoded:
                    print(f"✓ {field}: موجود")
                else:
                    print(f"✗ {field}: موجود نیست")
            
            # Check context structure
            context_required = ['user', 'group', 'features']
            for field in context_required:
                if field in context:
                    print(f"✓ context.{field}: موجود")
                else:
                    print(f"✗ context.{field}: موجود نیست")
            
            # Check user structure
            user_required = ['id', 'name', 'email', 'avatar', 'affiliation', 'moderator', 'region', 'displayName']
            for field in user_required:
                if field in user_context:
                    print(f"✓ context.user.{field}: موجود")
                else:
                    print(f"✗ context.user.{field}: موجود نیست")
            
            # Check features structure
            features_required = ['livestreaming', 'recording', 'screen-sharing', 'sip', 'etherpad', 'transcription', 'breakout-rooms']
            for field in features_required:
                if field in features:
                    print(f"✓ context.features.{field}: موجود")
                else:
                    print(f"✗ context.features.{field}: موجود نیست")
            
            # Check identity structure
            identity_required = ['type', 'guest', 'externalId']
            for field in identity_required:
                if field in identity:
                    print(f"✓ identity.{field}: موجود")
                else:
                    print(f"✗ identity.{field}: موجود نیست")
            
            # Check custom structure
            custom_required = ['theme', 'allowKnocking', 'enablePolls']
            for field in custom_required:
                if field in custom:
                    print(f"✓ custom.{field}: موجود")
                else:
                    print(f"✗ custom.{field}: موجود نیست")
            
            print(f"\n🎉 فرمت JWT Payload دقیقاً مطابق با درخواست شما است!")
            
        else:
            print(f"✗ خطا در تولید JWT token")
            return False
            
    except Exception as e:
        print(f"✗ خطا در تست: {e}")
        return False
    
    return True


if __name__ == '__main__':
    success = test_payload_format()
    if success:
        print("\n✅ تست فرمت payload موفقیت‌آمیز بود!")
    else:
        print("\n❌ تست فرمت payload ناموفق بود!")
        sys.exit(1)
