"""
Custom JWT token serializers with GUID support.
"""

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT token serializer that includes user GUID in token claims.
    """
    
    @classmethod
    def get_token(cls, user):
        """
        Generate JWT token with custom claims including GUID.
        """
        token = super().get_token(user)
        
        # Add custom claims
        token['guid'] = str(user.guid)
        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser
        token['is_phone_verified'] = user.is_phone_verified
        token['is_email_verified'] = user.is_email_verified
        
        return token


class CustomRefreshToken(RefreshToken):
    """
    Custom refresh token that includes user GUID.
    """
    
    @classmethod
    def for_user(cls, user):
        """
        Generate refresh token with custom claims including GUID.
        """
        token = super().for_user(user)
        
        # Add custom claims to access token
        token['guid'] = str(user.guid)
        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser
        token['is_phone_verified'] = user.is_phone_verified
        token['is_email_verified'] = user.is_email_verified
        
        return token
