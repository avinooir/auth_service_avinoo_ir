#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تست کامل SSO Flow برای meet.avinoo.ir
"""

import os
import sys
import django
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

def test_sso_flow():
    """تست کامل SSO Flow"""
    print("=" * 60)
    print("🔄 تست کامل SSO Flow برای meet.avinoo.ir")
    print("=" * 60)
    
    try:
        # 1. بررسی SSO Client
        print("\n1️⃣ بررسی SSO Client...")
        try:
            client = SSOClient.objects.get(client_id='meet_avinoo')
            print("✅ SSO Client یافت شد")
            print(f"   - Client ID: {client.client_id}")
            print(f"   - Domain: {client.domain}")
            print(f"   - Redirect URI: {client.redirect_uri}")
            print(f"   - Allow Any Path: {client.allow_any_path}")
        except SSOClient.DoesNotExist:
            print("❌ SSO Client یافت نشد!")
            return False
        
        # 2. بررسی کاربر
        print("\n2️⃣ بررسی کاربر...")
        user = User.objects.get(email='mohammad.rahimaee@gmail.com')
        print("✅ کاربر یافت شد")
        print(f"   - Username: {user.username}")
        print(f"   - Email: {user.email}")
        print(f"   - GUID: {user.guid}")
        
        # 3. شبیه‌سازی Request
        print("\n3️⃣ شبیه‌سازی Request...")
        factory = RequestFactory()
        request = factory.get('/sso/callback/')
        request.user = user
        
        # 4. تست handle_meet_callback
        print("\n4️⃣ تست handle_meet_callback...")
        try:
            # شبیه‌سازی callback با room name
            state = "test_state_123"
            next_url = "https://meet.avinoo.ir/room"
            
            response = handle_meet_callback(request, client, state, next_url)
            
            if response.status_code == 302:  # Redirect
                redirect_url = response.url
                print("✅ Redirect موفق")
                print(f"   - Status Code: {response.status_code}")
                print(f"   - Redirect URL: {redirect_url}")
                
                # بررسی JWT در URL
                if 'jwt=' in redirect_url:
                    jwt_token = redirect_url.split('jwt=')[1].split('&')[0]
                    print(f"   - JWT Token: {jwt_token[:50]}...")
                    print(f"   - JWT Length: {len(jwt_token)} کاراکتر")
                    
                    # رمزگشایی JWT
                    import jwt
                    decoded = jwt.decode(jwt_token, options={'verify_signature': False})
                    print("   - JWT رمزگشایی شد")
                    print(f"   - Room: {decoded.get('room')}")
                    print(f"   - User ID: {decoded.get('context', {}).get('user', {}).get('id')}")
                    print(f"   - Moderator: {decoded.get('moderator')}")
                else:
                    print("❌ JWT در URL یافت نشد!")
                    
            else:
                print(f"❌ Redirect ناموفق - Status Code: {response.status_code}")
                
        except Exception as e:
            print(f"❌ خطا در handle_meet_callback: {e}")
            import traceback
            traceback.print_exc()
        
        # 5. تست URL های مختلف
        print("\n5️⃣ تست URL های مختلف...")
        test_rooms = ['room', 'test-room', 'meeting-123']
        
        for room in test_rooms:
            try:
                # تغییر redirect_uri برای room جدید
                original_redirect = client.redirect_uri
                client.redirect_uri = f"https://meet.avinoo.ir/{room}"
                
                response = handle_meet_callback(request, client, state, next_url)
                
                if response.status_code == 302 and 'jwt=' in response.url:
                    print(f"✅ Room '{room}': موفق")
                else:
                    print(f"❌ Room '{room}': ناموفق")
                
                # بازگردانی redirect_uri
                client.redirect_uri = original_redirect
                
            except Exception as e:
                print(f"❌ Room '{room}': خطا - {e}")
        
        print("\n" + "=" * 60)
        print("🎉 تست SSO Flow کامل انجام شد!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ خطا در تست SSO Flow: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_sso_flow()
