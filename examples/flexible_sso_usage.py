#!/usr/bin/env python
"""
Example usage of flexible SSO for any domain
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
django.setup()

from sso.models import SSOClient

def create_flexible_clients():
    """
    Create examples of flexible SSO clients for different domains
    """
    print("🚀 Creating Flexible SSO Clients")
    print("=" * 50)
    
    # Example 1: Jitsi Meet
    meet_client, created = SSOClient.objects.get_or_create(
        client_id='meet',
        defaults={
            'name': 'Jitsi Meet Application',
            'domain': 'meet.avinoo.ir',
            'client_secret': 'jitsi_meet_secret_2024',
            'redirect_uri': 'https://meet.avinoo.ir/callback',
            'allowed_redirect_uris': [],
            'allow_any_path': True,  # Enable flexible redirects
            'is_active': True
        }
    )
    
    if created:
        print("✅ Created meet.avinoo.ir client")
    else:
        print("📋 meet.avinoo.ir client already exists")
    
    # Example 2: Another domain (e.g., if you change domain)
    new_domain_client, created = SSOClient.objects.get_or_create(
        client_id='new_domain',
        defaults={
            'name': 'New Domain Application',
            'domain': 'newdomain.avinoo.ir',  # Your new domain
            'client_secret': 'new_domain_secret_2024',
            'redirect_uri': 'https://newdomain.avinoo.ir/callback',
            'allowed_redirect_uris': [],
            'allow_any_path': True,  # Enable flexible redirects
            'is_active': True
        }
    )
    
    if created:
        print("✅ Created newdomain.avinoo.ir client")
    else:
        print("📋 newdomain.avinoo.ir client already exists")
    
    # Example 3: External domain
    external_client, created = SSOClient.objects.get_or_create(
        client_id='external',
        defaults={
            'name': 'External Application',
            'domain': 'external.com',
            'client_secret': 'external_secret_2024',
            'redirect_uri': 'https://external.com/callback',
            'allowed_redirect_uris': [],
            'allow_any_path': True,  # Enable flexible redirects
            'is_active': True
        }
    )
    
    if created:
        print("✅ Created external.com client")
    else:
        print("📋 external.com client already exists")

def test_flexible_redirects():
    """
    Test flexible redirect URI validation for different clients
    """
    print("\n🧪 Testing Flexible Redirect URI Validation")
    print("=" * 60)
    
    # Test different clients
    test_clients = [
        ('meet', 'meet.avinoo.ir'),
        ('new_domain', 'newdomain.avinoo.ir'),
        ('external', 'external.com'),
    ]
    
    for client_id, domain in test_clients:
        try:
            client = SSOClient.objects.get(client_id=client_id)
            print(f"\n🔹 Testing {client.name} ({domain})")
            print(f"   Allow any path: {'✅ Yes' if client.allow_any_path else '❌ No'}")
            
            # Test URLs for this domain
            test_urls = [
                f"https://{domain}/callback",
                f"https://{domain}/sss/callback",
                f"https://{domain}/asdas/callback",
                f"https://{domain}/test2",
                f"https://{domain}/any/path/you/want",
                f"https://{domain}/very/long/path/with/many/segments",
                f"https://evil.com/callback",  # Should fail
                f"https://{domain}.evil.com/callback",  # Should fail
            ]
            
            for url in test_urls:
                is_allowed = client.is_redirect_uri_allowed(url)
                status = "✅ ALLOWED" if is_allowed else "❌ REJECTED"
                print(f"   {status}: {url}")
                
        except SSOClient.DoesNotExist:
            print(f"❌ Client '{client_id}' not found")

def show_usage_examples():
    """
    Show practical usage examples for different domains
    """
    print("\n📚 Practical Usage Examples")
    print("=" * 60)
    
    print("""
1. For meet.avinoo.ir (any path allowed):
   https://auth.avinoo.ir/sso/login/?client_id=meet&redirect_uri=https://meet.avinoo.ir/room/team1&next=/team1
   https://auth.avinoo.ir/sso/login/?client_id=meet&redirect_uri=https://meet.avinoo.ir/sss/callback&next=/dashboard

2. For newdomain.avinoo.ir (any path allowed):
   https://auth.avinoo.ir/sso/login/?client_id=new_domain&redirect_uri=https://newdomain.avinoo.ir/any/path&next=/home
   https://auth.avinoo.ir/sso/login/?client_id=new_domain&redirect_uri=https://newdomain.avinoo.ir/callback&next=/profile

3. For external.com (any path allowed):
   https://auth.avinoo.ir/sso/login/?client_id=external&redirect_uri=https://external.com/oauth/callback&next=/dashboard
   https://auth.avinoo.ir/sso/login/?client_id=external&redirect_uri=https://external.com/api/auth/callback&next=/home

4. API Usage (any domain with allow_any_path=True):
   POST https://auth.avinoo.ir/sso/api/login/
   {
     "username": "user123",
     "password": "pass123",
     "client_id": "meet",
     "redirect_uri": "https://meet.avinoo.ir/any/path/you/want"
   }

5. JavaScript Integration (dynamic domain):
   const domain = 'meet.avinoo.ir';  // Can be any domain
   const loginUrl = `https://auth.avinoo.ir/sso/login/?client_id=meet&redirect_uri=${encodeURIComponent('https://' + domain + '/callback')}&next=${encodeURIComponent('/room/' + roomName)}`;
   window.location.href = loginUrl;
""")

def show_admin_usage():
    """
    Show how to manage clients in Django admin
    """
    print("\n🔧 Admin Management")
    print("=" * 60)
    
    print("""
To manage SSO clients in Django admin:

1. Go to: http://127.0.0.1:8000/admin/sso/ssoclient/
2. Create new client or edit existing one
3. Set 'Allow any path' to True for flexible redirects
4. Set 'Domain' to your desired domain
5. Save the client

Or use the management script:
   python scripts/manage_sso_clients.py

Key fields:
- Domain: The domain that will accept any path
- Allow any path: Enable/disable flexible redirects
- Client ID: Unique identifier for the client
- Client Secret: Secret key for authentication
""")

if __name__ == '__main__':
    print("🚀 Flexible SSO Usage Examples")
    print("=" * 60)
    
    create_flexible_clients()
    test_flexible_redirects()
    show_usage_examples()
    show_admin_usage()
    
    print("\n✨ All examples completed!")
    print("💡 Key Point: Set 'allow_any_path=True' for any domain to accept flexible redirects!")
