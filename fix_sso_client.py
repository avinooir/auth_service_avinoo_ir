#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اصلاح SSO Client برای meet.avinoo.ir
"""

import os
import sys
import django

# تنظیم Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
django.setup()

from sso.models import SSOClient

def fix_sso_client():
    """اصلاح SSO Client"""
    try:
        # دریافت SSO client
        client = SSOClient.objects.get(client_id='meet_avinoo')
        print(f"✅ SSO Client یافت شد: {client.client_id}")
        print(f"   - Redirect URI فعلی: {client.redirect_uri}")
        print(f"   - Domain: {client.domain}")
        print(f"   - Allow Any Path: {client.allow_any_path}")
        
        # اصلاح redirect_uri
        client.redirect_uri = 'https://meet.avinoo.ir/room'
        client.save()
        
        print(f"\n✅ SSO Client اصلاح شد!")
        print(f"   - Redirect URI جدید: {client.redirect_uri}")
        
        return True
        
    except SSOClient.DoesNotExist:
        print("❌ SSO Client یافت نشد!")
        return False
    except Exception as e:
        print(f"❌ خطا: {e}")
        return False

if __name__ == "__main__":
    fix_sso_client()
