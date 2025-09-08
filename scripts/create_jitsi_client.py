#!/usr/bin/env python3
"""
Script to create SSO client for Jitsi Meet application
"""

import os
import sys
import django
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
django.setup()

from sso.models import SSOClient
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_jitsi_client():
    """
    Create SSO client for Jitsi Meet application
    """
    try:
        # Check if client already exists
        client_id = 'meet'
        try:
            existing_client = SSOClient.objects.get(client_id=client_id)
            logger.info(f"Client '{client_id}' already exists. Updating...")
            
            # Update existing client
            existing_client.name = 'Jitsi Meet Application'
            existing_client.domain = 'meet.avinoo.ir'
            existing_client.redirect_uri = 'https://meet.avinoo.ir/callback'
            existing_client.is_active = True
            existing_client.save()
            
            logger.info(f"Client '{client_id}' updated successfully!")
            return existing_client
            
        except SSOClient.DoesNotExist:
            # Create new client
            client = SSOClient.objects.create(
                name='Jitsi Meet Application',
                domain='meet.avinoo.ir',
                client_id=client_id,
                client_secret='jitsi_meet_secret_2024',
                redirect_uri='https://meet.avinoo.ir/callback',
                is_active=True
            )
            
            logger.info(f"Client '{client_id}' created successfully!")
            return client
            
    except Exception as e:
        logger.error(f"Error creating Jitsi client: {str(e)}")
        raise

def main():
    """
    Main function
    """
    try:
        logger.info("Creating SSO client for Jitsi Meet...")
        
        client = create_jitsi_client()
        
        logger.info("=" * 50)
        logger.info("Jitsi Meet SSO Client Configuration:")
        logger.info("=" * 50)
        logger.info(f"Client ID: {client.client_id}")
        logger.info(f"Client Secret: {client.client_secret}")
        logger.info(f"Domain: {client.domain}")
        logger.info(f"Redirect URI: {client.redirect_uri}")
        logger.info(f"Active: {client.is_active}")
        logger.info("=" * 50)
        
        logger.info("\nExample SSO Login URL:")
        logger.info(f"https://auth.avinoo.ir/sso/login/?client_id={client.client_id}&redirect_uri={client.redirect_uri}&next=/team1")
        
        logger.info("\nExample Callback URL after login:")
        logger.info(f"{client.redirect_uri}?token=JWT_TOKEN&next=/team1")
        
        logger.info("\n✅ Jitsi Meet SSO client setup completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
