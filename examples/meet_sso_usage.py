#!/usr/bin/env python
"""
Example usage of flexible SSO for meet.avinoo.ir
"""

import requests
import json

def test_meet_sso_login():
    """
    Test SSO login with different redirect URIs for meet.avinoo.ir
    """
    base_url = "http://127.0.0.1:8000"  # Change to your auth service URL
    
    # Different callback URLs that should all work
    callback_urls = [
        "https://meet.avinoo.ir/sss/callback",
        "https://meet.avinoo.ir/asdas/callback",
        "https://meet.avinoo.ir/test2",
        "https://meet.avinoo.ir/team1",
        "https://meet.avinoo.ir/room/team1",
        "https://meet.avinoo.ir/meeting/123",
        "https://meet.avinoo.ir/any/path/you/want",
    ]
    
    print("🧪 Testing SSO Login with different callback URLs")
    print("=" * 60)
    
    for callback_url in callback_urls:
        print(f"\n📋 Testing: {callback_url}")
        
        # SSO Login request
        login_data = {
            'username': 'test_user',  # Replace with real credentials
            'password': 'test_pass',
            'client_id': 'meet',
            'redirect_uri': callback_url
        }
        
        try:
            response = requests.post(
                f"{base_url}/sso/api/login/",
                json=login_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"   ✅ SUCCESS: Login successful")
                    print(f"   🔗 Redirect URL: {data.get('redirect_uri', 'N/A')}")
                else:
                    print(f"   ❌ FAILED: {data.get('error', 'Unknown error')}")
            elif response.status_code == 400:
                data = response.json()
                if 'آدرس بازگشت مجاز نیست' in str(data):
                    print(f"   ❌ FAILED: Redirect URI rejected")
                else:
                    print(f"   ⚠️  OTHER ERROR: {data.get('error', 'Unknown error')}")
            else:
                print(f"   ⚠️  HTTP {response.status_code}: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ⚠️  REQUEST ERROR: {str(e)}")

def test_web_redirect():
    """
    Test web-based SSO redirect
    """
    print("\n🌐 Testing Web-based SSO Redirect")
    print("=" * 60)
    
    # Example URLs for web redirect
    web_urls = [
        "https://auth.avinoo.ir/sso/login/?client_id=meet&redirect_uri=https://meet.avinoo.ir/sss/callback&next=/team1",
        "https://auth.avinoo.ir/sso/login/?client_id=meet&redirect_uri=https://meet.avinoo.ir/asdas/callback&next=/team2",
        "https://auth.avinoo.ir/sso/login/?client_id=meet&redirect_uri=https://meet.avinoo.ir/test2&next=/meeting/123",
    ]
    
    for url in web_urls:
        print(f"📋 Web redirect URL: {url}")
        print("   (Copy this URL to browser to test)")

def show_usage_examples():
    """
    Show practical usage examples
    """
    print("\n📚 Practical Usage Examples")
    print("=" * 60)
    
    print("""
1. Jitsi Meet Room Access:
   https://auth.avinoo.ir/sso/login/?client_id=meet&redirect_uri=https://meet.avinoo.ir/room/team1&next=/team1

2. Custom Callback:
   https://auth.avinoo.ir/sso/login/?client_id=meet&redirect_uri=https://meet.avinoo.ir/sss/callback&next=/dashboard

3. API Login:
   POST https://auth.avinoo.ir/sso/api/login/
   {
     "username": "user123",
     "password": "pass123",
     "client_id": "meet",
     "redirect_uri": "https://meet.avinoo.ir/any/path/you/want"
   }

4. JavaScript Integration:
   const loginUrl = `https://auth.avinoo.ir/sso/login/?client_id=meet&redirect_uri=${encodeURIComponent(window.location.origin + '/callback')}&next=${encodeURIComponent('/room/' + roomName)}`;
   window.location.href = loginUrl;
""")

if __name__ == '__main__':
    print("🚀 meet.avinoo.ir SSO Usage Examples")
    print("=" * 60)
    
    # Uncomment to test API (requires running server)
    # test_meet_sso_login()
    
    test_web_redirect()
    show_usage_examples()
    
    print("\n✨ All examples shown!")
    print("💡 Key Point: meet.avinoo.ir accepts ANY path as redirect_uri!")
