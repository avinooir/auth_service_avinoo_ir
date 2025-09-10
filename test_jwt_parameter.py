#!/usr/bin/env python
"""
Test script for JWT parameter in redirect URLs
"""

import os
import sys
import django
import requests
import json

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
django.setup()

from sso.models import SSOClient

def test_jwt_parameter():
    """
    Test JWT parameter in redirect URLs
    """
    print("🧪 Testing JWT Parameter in Redirect URLs")
    print("=" * 60)
    
    # Create or get meet client
    client, created = SSOClient.objects.get_or_create(
        client_id='meet',
        defaults={
            'name': 'Jitsi Meet Application',
            'domain': 'meet.avinoo.ir',
            'client_secret': 'jitsi_meet_secret_2024',
            'redirect_uri': 'https://meet.avinoo.ir/callback',
            'allowed_redirect_uris': [],
            'allow_any_path': True,
            'is_active': True
        }
    )
    
    if created:
        print("✅ Created meet client")
    else:
        print("📋 Using existing meet client")
    
    print(f"Client: {client.name}")
    print(f"Domain: {client.domain}")
    print()
    
    # Test different redirect URIs with JWT parameter
    test_cases = [
        {
            'name': 'Basic callback',
            'redirect_uri': 'https://meet.avinoo.ir/callback',
            'expected': 'https://meet.avinoo.ir/callback?jwt=TOKEN&state=STATE'
        },
        {
            'name': 'Test room',
            'redirect_uri': 'https://meet.avinoo.ir/testroom',
            'expected': 'https://meet.avinoo.ir/testroom?jwt=TOKEN&state=STATE'
        },
        {
            'name': 'SSS callback',
            'redirect_uri': 'https://meet.avinoo.ir/sss/callback',
            'expected': 'https://meet.avinoo.ir/sss/callback?jwt=TOKEN&state=STATE'
        },
        {
            'name': 'Team room',
            'redirect_uri': 'https://meet.avinoo.ir/room/team1',
            'expected': 'https://meet.avinoo.ir/room/team1?jwt=TOKEN&state=STATE'
        },
        {
            'name': 'Any path',
            'redirect_uri': 'https://meet.avinoo.ir/any/path/you/want',
            'expected': 'https://meet.avinoo.ir/any/path/you/want?jwt=TOKEN&state=STATE'
        }
    ]
    
    print("📋 Testing redirect URI generation:")
    for test_case in test_cases:
        print(f"\n🔹 {test_case['name']}")
        print(f"   Input:  {test_case['redirect_uri']}")
        print(f"   Expected: {test_case['expected']}")
        
        # Test if redirect URI is allowed
        is_allowed = client.is_redirect_uri_allowed(test_case['redirect_uri'])
        status = "✅ ALLOWED" if is_allowed else "❌ REJECTED"
        print(f"   Status: {status}")

def test_api_response():
    """
    Test API response format
    """
    print("\n🌐 Testing API Response Format")
    print("=" * 60)
    
    base_url = "http://127.0.0.1:8000"
    
    # Test SSO login API
    login_data = {
        'username': 'test_user',  # You might need to create this user
        'password': 'test_pass',
        'client_id': 'meet',
        'redirect_uri': 'https://meet.avinoo.ir/testroom'
    }
    
    print("📋 Testing SSO Login API:")
    print(f"   URL: {base_url}/sso/api/login/")
    print(f"   Data: {json.dumps(login_data, indent=2)}")
    
    try:
        response = requests.post(
            f"{base_url}/sso/api/login/",
            json=login_data,
            timeout=10
        )
        
        print(f"\n📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Login successful!")
                print(f"   Access Token: {data.get('access_token', 'N/A')[:50]}...")
                print(f"   Redirect URI: {data.get('redirect_uri', 'N/A')}")
                
                # Check if redirect URI contains jwt parameter
                redirect_uri = data.get('redirect_uri', '')
                if '?jwt=' in redirect_uri:
                    print("✅ JWT parameter found in redirect URI!")
                else:
                    print("❌ JWT parameter NOT found in redirect URI")
            else:
                print(f"❌ Login failed: {data.get('error', 'Unknown error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Request Error: {str(e)}")
        print("   (Make sure the server is running)")

def show_usage_examples():
    """
    Show usage examples with JWT parameter
    """
    print("\n📚 Usage Examples with JWT Parameter")
    print("=" * 60)
    
    print("""
1. Web-based SSO Login:
   https://auth.avinoo.ir/sso/login/?client_id=meet&redirect_uri=https://meet.avinoo.ir/testroom&next=/team1
   
   After successful login, user will be redirected to:
   https://meet.avinoo.ir/testroom?jwt=JWT_TOKEN&state=STATE&next=/team1

2. API Login:
   POST https://auth.avinoo.ir/sso/api/login/
   {
     "username": "user123",
     "password": "pass123",
     "client_id": "meet",
     "redirect_uri": "https://meet.avinoo.ir/testroom"
   }
   
   Response will contain:
   {
     "success": true,
     "redirect_uri": "https://meet.avinoo.ir/testroom?jwt=JWT_TOKEN&state=STATE",
     "access_token": "JWT_TOKEN",
     ...
   }

3. JavaScript Integration:
   const loginUrl = `https://auth.avinoo.ir/sso/login/?client_id=meet&redirect_uri=${encodeURIComponent('https://meet.avinoo.ir/testroom')}&next=${encodeURIComponent('/team1')}`;
   window.location.href = loginUrl;
   
   After login, the page will receive:
   https://meet.avinoo.ir/testroom?jwt=JWT_TOKEN&state=STATE&next=/team1

4. Jitsi Meet Integration:
   // Extract JWT from URL
   const urlParams = new URLSearchParams(window.location.search);
   const jwt = urlParams.get('jwt');
   
   if (jwt) {
     // Use JWT for Jitsi Meet
     const domain = 'meet.avinoo.ir';
     const options = {
       roomName: 'testroom',
       jwt: jwt,
       parentNode: document.querySelector('#jitsi-container')
     };
     const api = new JitsiMeetExternalAPI(domain, options);
   }
""")

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
        test_jwt_parameter()
        test_api_response()
        show_usage_examples()
        print("\n✨ Testing completed!")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
