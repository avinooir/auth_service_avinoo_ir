#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
دیباگ SSO Flow
"""

import os
import sys
import django

# تنظیم Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
django.setup()

from sso.models import SSOClient
from sso.views import sso_callback_page
from django.test import RequestFactory
from apps.users.models import User

def debug_sso_flow():
    """دیباگ SSO Flow"""
    print("=" * 60)
    print("🔍 دیباگ SSO Flow")
    print("=" * 60)
    
    try:
        # 1. بررسی SSO Client
        print("\n1️⃣ بررسی SSO Client...")
        try:
            client = SSOClient.objects.get(client_id='meet_avinoo')
            print(f"✅ Client یافت شد: {client.client_id}")
            print(f"   - Redirect URI: {client.redirect_uri}")
            print(f"   - Domain: {client.domain}")
            print(f"   - Is Active: {client.is_active}")
        except SSOClient.DoesNotExist:
            print("❌ Client یافت نشد!")
            return
        
        # 2. شبیه‌سازی Request
        print("\n2️⃣ شبیه‌سازی Request...")
        factory = RequestFactory()
        user = User.objects.get(email='mohammad.rahimaee@gmail.com')
        
        # شبیه‌سازی URL واقعی
        request = factory.get('/sso/callback/', {
            'client_id': 'meet_avinoo',
            'redirect_uri': 'https://meet.avinoo.ir/room',
            'state': 'test123'
        })
        request.user = user
        
        print(f"✅ Request ایجاد شد")
        print(f"   - Client ID: {request.GET.get('client_id')}")
        print(f"   - Redirect URI: {request.GET.get('redirect_uri')}")
        print(f"   - User: {request.user.username}")
        
        # 3. تست sso_callback_page
        print("\n3️⃣ تست sso_callback_page...")
        print("🔄 در حال اجرای sso_callback_page...")
        
        response = sso_callback_page(request)
        
        print(f"✅ Response Status: {response.status_code}")
        
        if hasattr(response, 'url'):
            print(f"✅ Redirect URL: {response.url}")
            
            # بررسی نوع JWT
            if 'jwt=' in response.url:
                jwt_token = response.url.split('jwt=')[1].split('&')[0]
                print(f"✅ JWT Token: {jwt_token[:50]}...")
                
                # رمزگشایی JWT
                import jwt
                decoded = jwt.decode(jwt_token, options={'verify_signature': False})
                
                print(f"\n📋 JWT Analysis:")
                print(f"   - aud: {decoded.get('aud')}")
                print(f"   - iss: {decoded.get('iss')}")
                print(f"   - sub: {decoded.get('sub')}")
                print(f"   - room: {decoded.get('room')}")
                
                if decoded.get('aud') == 'meet_avinoo':
                    print("🎉 توکن مخصوص meet تولید شد!")
                else:
                    print("❌ توکن معمولی Django تولید شد!")
                    print("   - احتمالاً شرط client_id == 'meet_avinoo' کار نمی‌کند")
            else:
                print("❌ JWT در URL یافت نشد!")
        else:
            print("❌ Response URL موجود نیست!")
            
    except Exception as e:
        print(f"❌ خطا: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_sso_flow()
