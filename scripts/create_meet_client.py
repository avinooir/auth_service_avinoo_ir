"""
Script to create meet.avinoo.ir SSO client
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


def create_meet_client():
    """Create meet.avinoo.ir SSO client"""
    
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
        return client
    except SSOClient.DoesNotExist:
        pass
    
    # Create new client
    client = SSOClient.objects.create(
        name='Meet Avinoo',
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
    
    print(f"کلاینت meet.avinoo.ir با موفقیت ایجاد شد:")
    print(f"شناسه کلاینت: {client.client_id}")
    print(f"رمز کلاینت: {client.client_secret}")
    print(f"نام: {client.name}")
    print(f"دامنه: {client.domain}")
    print(f"آدرس بازگشت: {client.redirect_uri}")
    print(f"اجازه هر مسیر: {client.allow_any_path}")
    print(f"فعال: {client.is_active}")
    
    return client


if __name__ == '__main__':
    create_meet_client()
