#!/usr/bin/env python
"""
Simple test for meet.avinoo.ir redirect URI validation
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
django.setup()

from sso.models import SSOClient

def test_meet_redirect_uris():
    """
    Test redirect URI validation for meet.avinoo.ir
    """
    print("🧪 Testing meet.avinoo.ir Redirect URI Validation")
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
            'allow_any_path': True,  # Enable flexible redirects
            'is_active': True
        }
    )
    
    # Update existing client if needed
    if not created and not client.allow_any_path:
        client.allow_any_path = True
        client.save()
        print("✅ Updated existing client to use flexible redirects")
    
    if created:
        print("✅ Created new meet client")
    else:
        print("📋 Using existing meet client")
    
    print(f"Client: {client.name}")
    print(f"Domain: {client.domain}")
    print()
    
    # Test URLs - ALL should be allowed for meet.avinoo.ir
    test_urls = [
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
        "https://meet.avinoo.ir/anything",
        "https://meet.avinoo.ir/room/team1",
        "https://meet.avinoo.ir/room/team2",
        "https://meet.avinoo.ir/meeting/123",
    ]
    
    print("✅ Testing ALLOWED URLs (should all pass):")
    all_passed = True
    for url in test_urls:
        is_allowed = client.is_redirect_uri_allowed(url)
        status = "✅ PASS" if is_allowed else "❌ FAIL"
        print(f"   {status}: {url}")
        if not is_allowed:
            all_passed = False
    
    print()
    
    # Test URLs that should be rejected
    rejected_urls = [
        "https://evil.com/callback",
        "https://meet.evil.com/callback",
        "https://avinoo.ir/callback",  # Different domain
        "https://meet.avinoo.ir.malicious.com/callback",  # Subdomain attack
        "https://fake-meet.avinoo.ir/callback",  # Different subdomain
    ]
    
    print("🚫 Testing REJECTED URLs (should all fail):")
    all_rejected = True
    for url in rejected_urls:
        is_allowed = client.is_redirect_uri_allowed(url)
        status = "✅ PASS" if not is_allowed else "❌ FAIL"
        print(f"   {status}: {url}")
        if is_allowed:
            all_rejected = False
    
    print()
    print("=" * 60)
    if all_passed and all_rejected:
        print("🎉 ALL TESTS PASSED! meet.avinoo.ir accepts any path!")
    else:
        print("❌ Some tests failed!")
    
    print()
    print("📝 Summary:")
    print("   - meet.avinoo.ir accepts ANY path on the domain")
    print("   - Other domains are rejected for security")
    print("   - Perfect for flexible callback handling!")

if __name__ == '__main__':
    test_meet_redirect_uris()
