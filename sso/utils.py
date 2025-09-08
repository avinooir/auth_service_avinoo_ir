"""
SSO Utility functions
"""

import logging
from django.conf import settings
from django.utils import timezone
from .models import SSOAuditLog

logger = logging.getLogger(__name__)


def get_client_ip(request):
    """
    Get client IP address from request
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def log_sso_activity(user, client, action, request, details=None):
    """
    Log SSO activity for audit purposes
    """
    try:
        SSOAuditLog.objects.create(
            user=user,
            client=client,
            action=action,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            details=details or {}
        )
    except Exception as e:
        logger.error(f"Failed to log SSO activity: {str(e)}")


def validate_redirect_uri(redirect_uri, allowed_domains):
    """
    Validate redirect URI against allowed domains
    """
    from urllib.parse import urlparse
    
    try:
        parsed_uri = urlparse(redirect_uri)
        domain = parsed_uri.netloc.lower()
        
        # Check if domain is in allowed domains
        for allowed_domain in allowed_domains:
            if domain == allowed_domain.lower() or domain.endswith(f'.{allowed_domain.lower()}'):
                return True
        
        return False
    except Exception:
        return False


def generate_state():
    """
    Generate a random state parameter for OAuth-like flow
    """
    import secrets
    return secrets.token_urlsafe(32)


def create_sso_session(user, client, redirect_uri, state=None):
    """
    Create a new SSO session
    """
    from .models import SSOSession
    
    if not state:
        state = generate_state()
    
    session = SSOSession.objects.create(
        user=user,
        client=client,
        state=state,
        redirect_uri=redirect_uri,
        expires_at=timezone.now() + timezone.timedelta(minutes=10)
    )
    
    return session


def cleanup_expired_sessions():
    """
    Clean up expired SSO sessions
    """
    from .models import SSOSession
    
    expired_sessions = SSOSession.objects.filter(
        expires_at__lt=timezone.now()
    )
    
    count = expired_sessions.count()
    expired_sessions.delete()
    
    if count > 0:
        logger.info(f"Cleaned up {count} expired SSO sessions")
    
    return count
