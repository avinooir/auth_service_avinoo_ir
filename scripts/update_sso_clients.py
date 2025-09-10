#!/usr/bin/env python
"""
Script to update existing SSO clients with allowed_redirect_uris
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
django.setup()

from sso.models import SSOClient
import logging

logger = logging.getLogger(__name__)

def update_sso_clients():
    """
    Update existing SSO clients with allowed_redirect_uris
    """
    print("🔄 Updating SSO clients with allowed_redirect_uris...")
    
    # Get all existing clients
    clients = SSOClient.objects.all()
    
    for client in clients:
        print(f"\n📋 Processing client: {client.name} ({client.client_id})")
        print(f"   Domain: {client.domain}")
        print(f"   Current redirect_uri: {client.redirect_uri}")
        
        # Initialize allowed_redirect_uris if not set
        if not hasattr(client, 'allowed_redirect_uris') or client.allowed_redirect_uris is None:
            client.allowed_redirect_uris = []
        
        # Add current redirect_uri to allowed list if not already there
        if client.redirect_uri not in client.allowed_redirect_uris:
            client.allowed_redirect_uris.append(client.redirect_uri)
        
        # Add common callback patterns for the domain
        domain_patterns = [
            f"https://{client.domain}/callback",
            f"https://{client.domain}/callback/",
            f"https://{client.domain}/sss/callback",
            f"https://{client.domain}/sss/callback/",
            f"https://{client.domain}/asdas/callback",
            f"https://{client.domain}/asdas/callback/",
            f"https://{client.domain}/test2/callback",
            f"https://{client.domain}/test2/callback/",
        ]
        
        for pattern in domain_patterns:
            if pattern not in client.allowed_redirect_uris:
                client.allowed_redirect_uris.append(pattern)
        
        # Special handling for meet.avinoo.ir - enable allow_any_path
        if client.domain == 'meet.avinoo.ir':
            client.allow_any_path = True
            print(f"   ✅ Enabled allow_any_path for {client.domain}")
        
        # Save the client
        client.save()
        
        print(f"   ✅ Updated allowed_redirect_uris: {len(client.allowed_redirect_uris)} patterns")
        for uri in client.allowed_redirect_uris:
            print(f"      - {uri}")
    
    print(f"\n🎉 Successfully updated {clients.count()} SSO clients!")

def test_redirect_uri_validation():
    """
    Test the new redirect URI validation
    """
    print("\n🧪 Testing redirect URI validation...")
    
    # Test URLs
    test_urls = [
        "https://meet.avinoo.ir/sss/callback",
        "https://meet.avinoo.ir/asdas/callback",
        "https://meet.avinoo.ir/test2",
        "https://meet.avinoo.ir/team1",
        "https://meet.avinoo.ir/",
        "https://meet.avinoo.ir/callback",
        "https://invalid.avinoo.ir/callback",  # Should fail
        "https://meet.avinoo.ir/malicious",   # Should fail
    ]
    
    try:
        client = SSOClient.objects.get(client_id='meet')
        print(f"Testing with client: {client.name}")
        
        for url in test_urls:
            is_allowed = client.is_redirect_uri_allowed(url)
            status = "✅ ALLOWED" if is_allowed else "❌ REJECTED"
            print(f"   {status}: {url}")
            
    except SSOClient.DoesNotExist:
        print("   ⚠️  No 'meet' client found for testing")

if __name__ == '__main__':
    try:
        update_sso_clients()
        test_redirect_uri_validation()
        print("\n✨ All done!")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
