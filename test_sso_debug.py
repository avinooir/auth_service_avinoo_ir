#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تست دیباگ SSO برای meet.avinoo.ir
"""

import os
import sys
import django
import jwt
import json

# تنظیم Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
django.setup()

from apps.users.models import User
from sso.models import SSOClient
from sso.views import handle_meet_callback
from django.test import RequestFactory
from django.contrib.auth import get_user_model

def test_sso_debug():
    """تست دیباگ SSO"""
    print("=" * 60)
    print("🔍 تست دیباگ SSO برای meet.avinoo.ir")
    print("=" * 60)
    
    try:
        # 1. بررسی SSO Client
        print("\n1️⃣ بررسی SSO Client...")
        client = SSOClient.objects.get(client_id='meet_avinoo')
        print(f"✅ Client ID: {client.client_id}")
        print(f"✅ Redirect URI: {client.redirect_uri}")
        print(f"✅ Domain: {client.domain}")
        print(f"✅ Allow Any Path: {client.allow_any_path}")
        
        # 2. بررسی کاربر
        print("\n2️⃣ بررسی کاربر...")
        user = User.objects.get(email='mohammad.rahimaee@gmail.com')
        print(f"✅ کاربر: {user.username} ({user.email})")
        print(f"✅ GUID: {user.guid}")
        
        # 3. شبیه‌سازی Request
        print("\n3️⃣ شبیه‌سازی Request...")
        factory = RequestFactory()
        
        # شبیه‌سازی URL: http://127.0.0.1:8000/login/?client_id=meet_avinoo&redirect_uri=https://meet.avinoo.ir/room
        request = factory.get('/login/', {
            'client_id': 'meet_avinoo',
            'redirect_uri': 'https://meet.avinoo.ir/room',
            'state': 'test_state_123'
        })
        request.user = user
        
        print(f"✅ Request URL: {request.get_full_path()}")
        print(f"✅ Client ID: {request.GET.get('client_id')}")
        print(f"✅ Redirect URI: {request.GET.get('redirect_uri')}")
        print(f"✅ State: {request.GET.get('state')}")
        
        # 4. تست handle_meet_callback
        print("\n4️⃣ تست handle_meet_callback...")
        try:
            response = handle_meet_callback(request, client, 'test_state_123', None)
            
            if response.status_code == 302:  # Redirect
                redirect_url = response.url
                print("✅ Redirect موفق")
                print(f"✅ Status Code: {response.status_code}")
                print(f"✅ Redirect URL: {redirect_url}")
                
                # بررسی JWT در URL
                if 'jwt=' in redirect_url:
                    jwt_token = redirect_url.split('jwt=')[1].split('&')[0]
                    print(f"✅ JWT Token: {jwt_token[:50]}...")
                    print(f"✅ JWT Length: {len(jwt_token)} کاراکتر")
                    
                    # رمزگشایی JWT
                    decoded = jwt.decode(jwt_token, options={'verify_signature': False})
                    print("✅ JWT رمزگشایی شد")
                    
                    # بررسی ساختار JWT
                    print(f"\n📋 ساختار JWT:")
                    print(f"✅ aud: {decoded.get('aud')}")
                    print(f"✅ iss: {decoded.get('iss')}")
                    print(f"✅ sub: {decoded.get('sub')}")
                    print(f"✅ room: {decoded.get('room')}")
                    print(f"✅ moderator: {decoded.get('moderator')}")
                    
                    if decoded.get('aud') == 'meet_avinoo' and decoded.get('iss') == 'meet_avinoo':
                        print("🎉 توکن مخصوص meet تولید شد!")
                    else:
                        print("❌ توکن معمولی Django تولید شد!")
                        
                else:
                    print("❌ JWT در URL یافت نشد!")
                    
            else:
                print(f"❌ Redirect ناموفق - Status Code: {response.status_code}")
                
        except Exception as e:
            print(f"❌ خطا در handle_meet_callback: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n" + "=" * 60)
        print("🎯 تست دیباگ کامل شد!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ خطا در تست: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_sso_debug()
