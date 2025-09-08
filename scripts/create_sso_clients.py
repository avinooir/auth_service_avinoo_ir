#!/usr/bin/env python
"""
Script to create initial SSO clients for microservice architecture
"""

import os
import sys
import django
from django.conf import settings

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
django.setup()

from sso.models import SSOClient
import secrets
import string


def generate_client_secret():
    """Generate a secure client secret"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(64))


def create_sso_clients():
    """Create initial SSO clients for the microservice architecture"""
    
    clients_data = [
        {
            'name': 'جلسه',
            'domain': 'meet.avinoo.ir',
            'client_id': 'app1_client',
            'redirect_uri': 'https://app1.avinoo.ir/callback'
        },
        {
            'name': 'App2 - اپلیکیشن دوم',
            'domain': 'app2.avinoo.ir',
            'client_id': 'app2_client',
            'redirect_uri': 'https://app2.avinoo.ir/callback'
        },
        {
            'name': 'Admin Panel - پنل مدیریت',
            'domain': 'admin.avinoo.ir',
            'client_id': 'admin_client',
            'redirect_uri': 'https://admin.avinoo.ir/callback'
        }
    ]
    
    created_clients = []
    
    for client_data in clients_data:
        # Check if client already exists
        if SSOClient.objects.filter(client_id=client_data['client_id']).exists():
            print(f"⚠️  کلاینت {client_data['name']} از قبل موجود است.")
            continue
        
        # Generate client secret
        client_secret = generate_client_secret()
        
        # Create client
        client = SSOClient.objects.create(
            name=client_data['name'],
            domain=client_data['domain'],
            client_id=client_data['client_id'],
            client_secret=client_secret,
            redirect_uri=client_data['redirect_uri'],
            is_active=True
        )
        
        created_clients.append({
            'client': client,
            'secret': client_secret
        })
        
        print(f"✅ کلاینت {client.name} ایجاد شد:")
        print(f"   - Client ID: {client.client_id}")
        print(f"   - Client Secret: {client_secret}")
        print(f"   - Domain: {client.domain}")
        print(f"   - Redirect URI: {client.redirect_uri}")
        print()
    
    if created_clients:
        print("🔐 اطلاعات کلاینت‌ها:")
        print("=" * 50)
        for item in created_clients:
            client = item['client']
            secret = item['secret']
            print(f"نام: {client.name}")
            print(f"Client ID: {client.client_id}")
            print(f"Client Secret: {secret}")
            print(f"Domain: {client.domain}")
            print(f"Redirect URI: {client.redirect_uri}")
            print("-" * 30)
        
        print("\n📝 نکات مهم:")
        print("1. Client Secret ها را در جای امن نگهداری کنید")
        print("2. این اطلاعات را در فایل‌های تنظیمات اپلیکیشن‌های کلاینت قرار دهید")
        print("3. در Production، Client Secret ها را رمزنگاری کنید")
        print("4. برای امنیت بیشتر، از HTTPS استفاده کنید")
    else:
        print("ℹ️  همه کلاینت‌ها از قبل موجود هستند.")


if __name__ == '__main__':
    create_sso_clients()
