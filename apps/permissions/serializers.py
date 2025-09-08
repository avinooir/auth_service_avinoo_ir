"""
Serializers for Permissions app.
"""

import logging
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserPermission, PermissionGroup, PermissionGroupPermission, AuditLog

logger = logging.getLogger(__name__)
User = get_user_model()


class UserPermissionSerializer(serializers.ModelSerializer):
    """
    Serializer for UserPermission model.
    """
    
    permission_name = serializers.CharField(source='permission.display_name', read_only=True)
    permission_id = serializers.IntegerField(source='permission.id', read_only=True)
    granted_by_username = serializers.CharField(source='granted_by.username', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    is_expired = serializers.SerializerMethodField()
    
    class Meta:
        model = UserPermission
        fields = [
            'id', 'user', 'user_username', 'permission', 'permission_id',
            'permission_name', 'granted_by', 'granted_by_username',
            'granted_at', 'expires_at', 'is_active', 'is_expired'
        ]
        read_only_fields = ['id', 'granted_at']
    
    def get_is_expired(self, obj):
        """Check if permission is expired."""
        return obj.is_expired()


class UserPermissionCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating UserPermission.
    """
    
    class Meta:
        model = UserPermission
        fields = ['user', 'permission', 'expires_at', 'is_active']
    
    def validate(self, attrs):
        """Validate user permission assignment."""
        user = attrs['user']
        permission = attrs['permission']
        
        # Check if user already has this permission
        if UserPermission.objects.filter(user=user, permission=permission).exists():
            raise serializers.ValidationError({
                'permission': 'کاربر قبلاً این مجوز را دارد.'
            })
        
        # Check if permission is active
        if not permission.is_active:
            raise serializers.ValidationError({
                'permission': 'مجوز انتخاب شده غیرفعال است.'
            })
        
        return attrs


class PermissionGroupSerializer(serializers.ModelSerializer):
    """
    Serializer for PermissionGroup model.
    """
    
    permission_count = serializers.SerializerMethodField()
    
    class Meta:
        model = PermissionGroup
        fields = [
            'id', 'name', 'display_name', 'description', 'app_label',
            'is_active', 'permission_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_permission_count(self, obj):
        """Get count of permissions in this group."""
        return obj.group_permissions.count()


class PermissionGroupCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating PermissionGroup.
    """
    
    class Meta:
        model = PermissionGroup
        fields = ['name', 'display_name', 'description', 'app_label', 'is_active']
    
    def validate_name(self, value):
        """Validate group name."""
        if PermissionGroup.objects.filter(name=value).exists():
            raise serializers.ValidationError('گروهی با این نام قبلاً وجود دارد.')
        return value


class PermissionGroupPermissionSerializer(serializers.ModelSerializer):
    """
    Serializer for PermissionGroupPermission model.
    """
    
    permission_name = serializers.CharField(source='permission.display_name', read_only=True)
    permission_id = serializers.IntegerField(source='permission.id', read_only=True)
    group_name = serializers.CharField(source='group.display_name', read_only=True)
    added_by_username = serializers.CharField(source='added_by.username', read_only=True)
    
    class Meta:
        model = PermissionGroupPermission
        fields = [
            'id', 'group', 'group_name', 'permission', 'permission_id',
            'permission_name', 'added_by', 'added_by_username', 'added_at'
        ]
        read_only_fields = ['id', 'added_at']


class PermissionGroupPermissionCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating PermissionGroupPermission.
    """
    
    class Meta:
        model = PermissionGroupPermission
        fields = ['group', 'permission']
    
    def validate(self, attrs):
        """Validate group permission assignment."""
        group = attrs['group']
        permission = attrs['permission']
        
        # Check if group already has this permission
        if PermissionGroupPermission.objects.filter(group=group, permission=permission).exists():
            raise serializers.ValidationError({
                'permission': 'گروه قبلاً این مجوز را دارد.'
            })
        
        # Check if group is active
        if not group.is_active:
            raise serializers.ValidationError({
                'group': 'گروه انتخاب شده غیرفعال است.'
            })
        
        # Check if permission is active
        if not permission.is_active:
            raise serializers.ValidationError({
                'permission': 'مجوز انتخاب شده غیرفعال است.'
            })
        
        return attrs


class AuditLogSerializer(serializers.ModelSerializer):
    """
    Serializer for AuditLog model.
    """
    
    user_username = serializers.CharField(source='user.username', read_only=True)
    target_user_username = serializers.CharField(source='target_user.username', read_only=True)
    permission_name = serializers.CharField(source='permission.display_name', read_only=True)
    role_name = serializers.CharField(source='role.display_name', read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    
    class Meta:
        model = AuditLog
        fields = [
            'id', 'user', 'user_username', 'action', 'action_display',
            'target_user', 'target_user_username', 'permission', 'permission_name',
            'role', 'role_name', 'details', 'ip_address', 'user_agent', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class UserPermissionSummarySerializer(serializers.ModelSerializer):
    """
    Serializer for user permission summary.
    """
    
    permission_name = serializers.CharField(source='permission.display_name', read_only=True)
    permission_id = serializers.IntegerField(source='permission.id', read_only=True)
    is_expired = serializers.SerializerMethodField()
    
    class Meta:
        model = UserPermission
        fields = [
            'id', 'permission_id', 'permission_name', 'granted_at', 'expires_at',
            'is_active', 'is_expired'
        ]
    
    def get_is_expired(self, obj):
        """Check if permission is expired."""
        return obj.is_expired()


class UserWithPermissionsSerializer(serializers.ModelSerializer):
    """
    Serializer for user with their permissions.
    """
    
    permissions = UserPermissionSummarySerializer(source='direct_permissions', many=True, read_only=True)
    active_permissions = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'is_active', 'permissions', 'active_permissions'
        ]
    
    def get_active_permissions(self, obj):
        """Get active permissions for user."""
        active_permissions = obj.direct_permissions.filter(is_active=True)
        return UserPermissionSummarySerializer(active_permissions, many=True).data
