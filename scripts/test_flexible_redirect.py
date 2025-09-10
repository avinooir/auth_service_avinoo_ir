#!/usr/bin/env python
"""
Test script for flexible redirect URI validation
"""

import os
import sys
import django
import requests
import json

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
django.setup()

from sso.models import SSOClient

def test_redirect_uris():
    """
    Test various redirect URIs with the meet client
    """
    print("🧪 Testing Flexible Redirect URI Validation")
    print("=" * 50)
    
    # Test URLs that should be allowed for meet.avinoo.ir
    allowed_urls = [
        "https://meet.avinoo.ir/sss/callback",
        "https://meet.avinoo.ir/asdas/callback", 
        "https://meet.avinoo.ir/test2",
        "https://meet.avinoo.ir/team1",
        "https://meet.avinoo.ir/",
        "https://meet.avinoo.ir/callback",
        "https://meet.avinoo.ir/sss/",
        "https://meet.avinoo.ir/asdas/",
        "https://meet.avinoo.ir/any/path/you/want",
        "https://meet.avinoo.ir/random123",
        "https://meet.avinoo.ir/very/long/path/with/many/segments",
        "https://meet.avinoo.ir/",
        "https://meet.avinoo.ir/anything",
    ]
    
    # Test URLs that should be rejected
    rejected_urls = [
        "https://evil.com/callback",
        "https://meet.evil.com/callback",
        "https://avinoo.ir/callback",  # Different domain
        "https://meet.avinoo.ir.malicious.com/callback",  # Subdomain attack
    ]
    
    try:
        # Get or create meet client
        client, created = SSOClient.objects.get_or_create(
            client_id='meet',
            defaults={
                'name': 'Jitsi Meet Application',
                'domain': 'meet.avinoo.ir',
                'client_secret': 'jitsi_meet_secret_2024',
                'redirect_uri': 'https://meet.avinoo.ir/callback',
                'allowed_redirect_uris': [
                    'https://meet.avinoo.ir/callback',
                    'https://meet.avinoo.ir/sss/',
                    'https://meet.avinoo.ir/asdas/',
                    'https://meet.avinoo.ir/test2',
                ],
                'is_active': True
            }
        )
        
        if created:
            print(f"✅ Created new meet client")
        else:
            print(f"📋 Using existing meet client: {client.name}")
        
        print(f"\n🔍 Testing ALLOWED URLs:")
        for url in allowed_urls:
            is_allowed = client.is_redirect_uri_allowed(url)
            status = "✅ PASS" if is_allowed else "❌ FAIL"
            print(f"   {status}: {url}")
        
        print(f"\n🚫 Testing REJECTED URLs:")
        for url in rejected_urls:
            is_allowed = client.is_redirect_uri_allowed(url)
            status = "✅ PASS" if not is_allowed else "❌ FAIL"
            print(f"   {status}: {url}")
        
        # Test API endpoints
        print(f"\n🌐 Testing API Endpoints:")
        test_api_endpoints(client)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

def test_api_endpoints(client):
    """
    Test the actual API endpoints
    """
    base_url = "http://127.0.0.1:8000"
    
    # Test URLs
    test_cases = [
        {
            'name': 'Valid callback',
            'redirect_uri': 'https://meet.avinoo.ir/sss/callback',
            'should_pass': True
        },
        {
            'name': 'Valid path',
            'redirect_uri': 'https://meet.avinoo.ir/test2',
            'should_pass': True
        },
        {
            'name': 'Invalid domain',
            'redirect_uri': 'https://evil.com/callback',
            'should_pass': False
        }
    ]
    
    for test_case in test_cases:
        print(f"\n   🧪 Testing: {test_case['name']}")
        print(f"      URL: {test_case['redirect_uri']}")
        
        # Test SSO login endpoint
        login_data = {
            'username': 'test_user',  # You might need to create this user
            'password': 'test_pass',
            'client_id': 'meet',
            'redirect_uri': test_case['redirect_uri']
        }
        
        try:
            response = requests.post(
                f"{base_url}/sso/api/login/",
                json=login_data,
                timeout=5
            )
            
            if test_case['should_pass']:
                # Should not return 400 for redirect URI validation
                if response.status_code == 400:
                    error_data = response.json()
                    if 'آدرس بازگشت مجاز نیست' in str(error_data):
                        print(f"      ❌ FAIL: Redirect URI rejected (should be allowed)")
                    else:
                        print(f"      ✅ PASS: Other validation error (expected)")
                else:
                    print(f"      ✅ PASS: Request processed (status: {response.status_code})")
            else:
                # Should return 400 for redirect URI validation
                if response.status_code == 400:
                    error_data = response.json()
                    if 'آدرس بازگشت مجاز نیست' in str(error_data):
                        print(f"      ✅ PASS: Redirect URI correctly rejected")
                    else:
                        print(f"      ⚠️  PARTIAL: Other validation error")
                else:
                    print(f"      ❌ FAIL: Request should have been rejected")
                    
        except requests.exceptions.RequestException as e:
            print(f"      ⚠️  SKIP: Could not test API ({str(e)})")

def create_test_user():
    """
    Create a test user for API testing
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    try:
        user = User.objects.get(username='test_user')
        print(f"📋 Using existing test user: {user.username}")
    except User.DoesNotExist:
        user = User.objects.create_user(
            username='test_user',
            email='test@example.com',
            password='test_pass',
            first_name='Test',
            last_name='User'
        )
        print(f"✅ Created test user: {user.username}")

if __name__ == '__main__':
    try:
        create_test_user()
        test_redirect_uris()
        print("\n✨ Testing completed!")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
