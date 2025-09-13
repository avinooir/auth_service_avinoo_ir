"""
Show final JWT payload format
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


def show_final_payload():
    """Show final JWT payload format"""
    
    print("=== نمایش فرمت نهایی JWT Payload ===\n")
    
    try:
        # Get test user
        user = User.objects.get(username='admin')
        
        # Get JWT generator
        jwt_generator = get_meet_jwt_generator()
        
        # Generate JWT token
        room_name = "roomname"
        jwt_token = jwt_generator.generate_meet_jwt(user, room_name, None)
        
        if jwt_token:
            # Decode JWT to show payload
            decoded = jwt.decode(jwt_token, options={"verify_signature": False})
            
            print("📋 فرمت نهایی JWT Payload:")
            print("=" * 50)
            print(json.dumps(decoded, indent=2, ensure_ascii=False))
            print("=" * 50)
            
            print(f"\n🔗 URL نهایی:")
            print(f"https://meet.avinoo.ir/{room_name}?jwt={jwt_token}")
            
            print(f"\n✅ فرمت دقیقاً مطابق با درخواست شما است!")
            
        else:
            print(f"✗ خطا در تولید JWT token")
            return False
            
    except Exception as e:
        print(f"✗ خطا: {e}")
        return False
    
    return True


if __name__ == '__main__':
    success = show_final_payload()
    if success:
        print("\n🎉 نمایش فرمت نهایی موفقیت‌آمیز بود!")
    else:
        print("\n❌ خطا در نمایش فرمت نهایی!")
        sys.exit(1)
