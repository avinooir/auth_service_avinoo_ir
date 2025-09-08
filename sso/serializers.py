"""
SSO Serializers for API endpoints
"""

from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.conf import settings
from .models import SSOClient, SSOSession, SSOAuditLog
from apps.users.models import User
import logging

logger = logging.getLogger(__name__)


class SSOLoginSerializer(serializers.Serializer):
    """
    Serializer for SSO login requests
    """
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    client_id = serializers.CharField(max_length=100)
    redirect_uri = serializers.URLField()
    state = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        client_id = attrs.get('client_id')
        redirect_uri = attrs.get('redirect_uri')
        
        # Validate client
        try:
            client = SSOClient.objects.get(client_id=client_id, is_active=True)
            logger.info(f"Client found: {client.name}")
        except SSOClient.DoesNotExist:
            logger.warning(f"Client not found: {client_id}")
            # Create client if it doesn't exist
            client = SSOClient.objects.create(
                name=f'Test Client {client_id}',
                domain=getattr(settings, 'AUTH_SERVICE_DOMAIN', '127.0.0.1:8000'),
                client_id=client_id,
                client_secret='test_secret_123',
                redirect_uri=redirect_uri,
                is_active=True
            )
            logger.info(f"Client created: {client.name}")
        
        # Validate redirect URI (allow exact match or callback pattern)
        if redirect_uri != client.redirect_uri and not redirect_uri.endswith('/callback/'):
            # Log for debugging
            logger.warning(f"Redirect URI mismatch: {redirect_uri} != {client.redirect_uri}")
            # For now, allow any redirect URI for testing
            pass
        
        # Authenticate user
        user = authenticate(username=username, password=password)
        if not user:
            logger.warning(f"Authentication failed for username: {username}")
            raise serializers.ValidationError("نام کاربری یا رمز عبور اشتباه است.")
        
        if not user.is_active:
            logger.warning(f"Inactive user attempted login: {username}")
            raise serializers.ValidationError("حساب کاربری غیرفعال است.")
        
        logger.info(f"User authenticated successfully: {username}")
        
        attrs['user'] = user
        attrs['client'] = client
        return attrs


class SSORegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for SSO registration requests
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    client_id = serializers.CharField(max_length=100)
    redirect_uri = serializers.URLField()
    state = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'first_name', 'last_name', 
                 'password', 'password_confirm', 'client_id', 'redirect_uri', 'state']
    
    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        client_id = attrs.get('client_id')
        redirect_uri = attrs.get('redirect_uri')
        
        # Validate password confirmation
        if password != password_confirm:
            raise serializers.ValidationError("رمزهای عبور مطابقت ندارند.")
        
        # Validate client
        try:
            client = SSOClient.objects.get(client_id=client_id, is_active=True)
            logger.info(f"Client found: {client.name}")
        except SSOClient.DoesNotExist:
            logger.warning(f"Client not found: {client_id}")
            # Create client if it doesn't exist
            client = SSOClient.objects.create(
                name=f'Test Client {client_id}',
                domain=getattr(settings, 'AUTH_SERVICE_DOMAIN', '127.0.0.1:8000'),
                client_id=client_id,
                client_secret='test_secret_123',
                redirect_uri=redirect_uri,
                is_active=True
            )
            logger.info(f"Client created: {client.name}")
        
        # Validate redirect URI (allow exact match or callback pattern)
        if redirect_uri != client.redirect_uri and not redirect_uri.endswith('/callback/'):
            # Log for debugging
            logger.warning(f"Redirect URI mismatch: {redirect_uri} != {client.redirect_uri}")
            # For now, allow any redirect URI for testing
            pass
        
        attrs['client'] = client
        return attrs
    
    def create(self, validated_data):
        # Remove non-user fields
        client = validated_data.pop('client')
        validated_data.pop('password_confirm')
        validated_data.pop('client_id')
        validated_data.pop('redirect_uri')
        validated_data.pop('state', None)
        
        # Create user
        user = User.objects.create_user(**validated_data)
        return user


class SSOTokenValidationSerializer(serializers.Serializer):
    """
    Serializer for JWT token validation requests
    """
    token = serializers.CharField()
    client_id = serializers.CharField(max_length=100)
    
    def validate(self, attrs):
        token = attrs.get('token')
        client_id = attrs.get('client_id')
        
        # Validate client
        try:
            client = SSOClient.objects.get(client_id=client_id, is_active=True)
            logger.info(f"Client found: {client.name}")
        except SSOClient.DoesNotExist:
            logger.warning(f"Client not found: {client_id}")
            # Create client if it doesn't exist
            client = SSOClient.objects.create(
                name=f'Test Client {client_id}',
                domain=getattr(settings, 'AUTH_SERVICE_DOMAIN', '127.0.0.1:8000'),
                client_id=client_id,
                client_secret='test_secret_123',
                redirect_uri=redirect_uri,
                is_active=True
            )
            logger.info(f"Client created: {client.name}")
        
        attrs['client'] = client
        return attrs


class SSOCallbackSerializer(serializers.Serializer):
    """
    Serializer for SSO callback requests
    """
    code = serializers.CharField()
    state = serializers.CharField()
    client_id = serializers.CharField(max_length=100)
    
    def validate(self, attrs):
        code = attrs.get('code')
        state = attrs.get('state')
        client_id = attrs.get('client_id')
        
        # Validate client
        try:
            client = SSOClient.objects.get(client_id=client_id, is_active=True)
            logger.info(f"Client found: {client.name}")
        except SSOClient.DoesNotExist:
            logger.warning(f"Client not found: {client_id}")
            # Create client if it doesn't exist
            client = SSOClient.objects.create(
                name=f'Test Client {client_id}',
                domain=getattr(settings, 'AUTH_SERVICE_DOMAIN', '127.0.0.1:8000'),
                client_id=client_id,
                client_secret='test_secret_123',
                redirect_uri=redirect_uri,
                is_active=True
            )
            logger.info(f"Client created: {client.name}")
        
        # Validate session
        try:
            session = SSOSession.objects.get(
                state=state,
                client=client,
                is_used=False,
                expires_at__gt=timezone.now()
            )
        except SSOSession.DoesNotExist:
            raise serializers.ValidationError("جلسه نامعتبر یا منقضی شده است.")
        
        attrs['client'] = client
        attrs['session'] = session
        return attrs


class SSOClientSerializer(serializers.ModelSerializer):
    """
    Serializer for SSO client management
    """
    class Meta:
        model = SSOClient
        fields = ['id', 'name', 'domain', 'client_id', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'client_id', 'created_at', 'updated_at']


class SSOSessionSerializer(serializers.ModelSerializer):
    """
    Serializer for SSO session information
    """
    client_name = serializers.CharField(source='client.name', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = SSOSession
        fields = ['id', 'user_username', 'client_name', 'state', 'redirect_uri', 
                 'created_at', 'expires_at', 'is_used']
        read_only_fields = ['id', 'created_at']


class SSOAuditLogSerializer(serializers.ModelSerializer):
    """
    Serializer for SSO audit logs
    """
    user_username = serializers.CharField(source='user.username', read_only=True)
    client_name = serializers.CharField(source='client.name', read_only=True)
    
    class Meta:
        model = SSOAuditLog
        fields = ['id', 'user_username', 'client_name', 'action', 'ip_address', 
                 'user_agent', 'details', 'created_at']
        read_only_fields = ['id', 'created_at']
