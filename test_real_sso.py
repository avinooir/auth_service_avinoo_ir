#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تست واقعی SSO callback
"""

import os
import sys
import django
import jwt

# تنظیم Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
django.setup()

from sso.models import SSOClient
from sso.views import sso_callback_page
from django.test import RequestFactory
from apps.users.models import User

def test_real_sso():
    """تست واقعی SSO"""
    print("=" * 60)
    print("🧪 تست واقعی SSO Callback")
    print("=" * 60)
    
    try:
        # دریافت کاربر
        user = User.objects.get(email='mohammad.rahimaee@gmail.com')
        print(f"✅ کاربر: {user.username}")
        
        # ایجاد Request
        factory = RequestFactory()
        request = factory.get('/sso/callback/', {
            'client_id': 'meet_avinoo',
            'redirect_uri': 'https://meet.avinoo.ir/room',
            'state': 'test123'
        })
        request.user = user
        
        print(f"✅ Request ایجاد شد")
        print(f"   - Client ID: {request.GET.get('client_id')}")
        print(f"   - Redirect URI: {request.GET.get('redirect_uri')}")
        print(f"   - State: {request.GET.get('state')}")
        
        # تست sso_callback_page
        print(f"\n🔄 تست sso_callback_page...")
        response = sso_callback_page(request)
        
        print(f"✅ Response Status: {response.status_code}")
        
        if hasattr(response, 'url'):
            print(f"✅ Redirect URL: {response.url}")
            
            # بررسی JWT
            if 'jwt=' in response.url:
                jwt_token = response.url.split('jwt=')[1].split('&')[0]
                print(f"✅ JWT Token: {jwt_token[:50]}...")
                
                # رمزگشایی JWT
                decoded = jwt.decode(jwt_token, options={'verify_signature': False})
                print(f"✅ JWT رمزگشایی شد")
                
                # بررسی نوع JWT
                if decoded.get('aud') == 'meet_avinoo':
                    print("🎉 توکن مخصوص meet تولید شد!")
                else:
                    print("❌ توکن معمولی Django تولید شد!")
                    print(f"   - aud: {decoded.get('aud')}")
                    print(f"   - iss: {decoded.get('iss')}")
            else:
                print("❌ JWT در URL یافت نشد!")
        else:
            print("❌ Response URL موجود نیست!")
            
    except Exception as e:
        print(f"❌ خطا: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_real_sso()
