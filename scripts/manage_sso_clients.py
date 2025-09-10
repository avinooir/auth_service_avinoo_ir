#!/usr/bin/env python
"""
Script to manage SSO clients with flexible redirect URI handling
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

def create_flexible_client(name, domain, client_id, client_secret=None):
    """
    Create a new SSO client with allow_any_path enabled
    """
    if not client_secret:
        client_secret = f"{client_id}_secret_2024"
    
    client, created = SSOClient.objects.get_or_create(
        client_id=client_id,
        defaults={
            'name': name,
            'domain': domain,
            'client_secret': client_secret,
            'redirect_uri': f"https://{domain}/callback",
            'allowed_redirect_uris': [],
            'allow_any_path': True,  # Enable flexible redirects
            'is_active': True
        }
    )
    
    if created:
        print(f"✅ Created new flexible client: {name}")
        print(f"   Domain: {domain}")
        print(f"   Client ID: {client_id}")
        print(f"   Allow any path: {client.allow_any_path}")
    else:
        print(f"📋 Client already exists: {name}")
        # Update existing client to enable allow_any_path
        if not client.allow_any_path:
            client.allow_any_path = True
            client.save()
            print(f"   ✅ Enabled allow_any_path for existing client")
    
    return client

def update_client_to_flexible(client_id):
    """
    Update an existing client to use flexible redirect URIs
    """
    try:
        client = SSOClient.objects.get(client_id=client_id)
        client.allow_any_path = True
        client.save()
        print(f"✅ Updated client '{client.name}' to use flexible redirects")
        print(f"   Domain: {client.domain}")
        print(f"   Allow any path: {client.allow_any_path}")
        return client
    except SSOClient.DoesNotExist:
        print(f"❌ Client with ID '{client_id}' not found")
        return None

def list_clients():
    """
    List all SSO clients with their settings
    """
    clients = SSOClient.objects.all()
    
    print("📋 All SSO Clients:")
    print("=" * 80)
    
    for client in clients:
        print(f"\n🔹 {client.name}")
        print(f"   Client ID: {client.client_id}")
        print(f"   Domain: {client.domain}")
        print(f"   Allow any path: {'✅ Yes' if client.allow_any_path else '❌ No'}")
        print(f"   Active: {'✅ Yes' if client.is_active else '❌ No'}")
        print(f"   Redirect URIs: {len(client.allowed_redirect_uris)} patterns")
        if client.allowed_redirect_uris:
            for uri in client.allowed_redirect_uris[:3]:  # Show first 3
                print(f"      - {uri}")
            if len(client.allowed_redirect_uris) > 3:
                print(f"      ... and {len(client.allowed_redirect_uris) - 3} more")

def test_client_redirects(client_id):
    """
    Test redirect URI validation for a specific client
    """
    try:
        client = SSOClient.objects.get(client_id=client_id)
        print(f"🧪 Testing redirect URIs for: {client.name}")
        print(f"   Domain: {client.domain}")
        print(f"   Allow any path: {client.allow_any_path}")
        print("=" * 60)
        
        # Test URLs
        test_urls = [
            f"https://{client.domain}/callback",
            f"https://{client.domain}/sss/callback",
            f"https://{client.domain}/asdas/callback",
            f"https://{client.domain}/test2",
            f"https://{client.domain}/any/path/you/want",
            f"https://{client.domain}/very/long/path/with/many/segments",
            f"https://evil.com/callback",  # Should fail
            f"https://{client.domain}.evil.com/callback",  # Should fail
        ]
        
        for url in test_urls:
            is_allowed = client.is_redirect_uri_allowed(url)
            status = "✅ ALLOWED" if is_allowed else "❌ REJECTED"
            print(f"   {status}: {url}")
            
    except SSOClient.DoesNotExist:
        print(f"❌ Client with ID '{client_id}' not found")

def main():
    """
    Main function with interactive menu
    """
    print("🚀 SSO Client Management Tool")
    print("=" * 40)
    
    while True:
        print("\n📋 Available Commands:")
        print("1. Create flexible client")
        print("2. Update existing client to flexible")
        print("3. List all clients")
        print("4. Test client redirects")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            name = input("Client name: ").strip()
            domain = input("Domain (e.g., meet.avinoo.ir): ").strip()
            client_id = input("Client ID: ").strip()
            client_secret = input("Client secret (optional): ").strip() or None
            
            create_flexible_client(name, domain, client_id, client_secret)
            
        elif choice == '2':
            client_id = input("Client ID to update: ").strip()
            update_client_to_flexible(client_id)
            
        elif choice == '3':
            list_clients()
            
        elif choice == '4':
            client_id = input("Client ID to test: ").strip()
            test_client_redirects(client_id)
            
        elif choice == '5':
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
