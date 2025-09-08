"""
Serializers for Role app.
"""

import logging
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Role, UserRole, Permission, RolePermission

logger = logging.getLogger(__name__)
User = get_user_model()


class PermissionSerializer(serializers.ModelSerializer):
    """
    Serializer for Permission model.
    """
    
    class Meta:
        model = Permission
        fields = [
            'id', 'name', 'display_name', 'description', 'app_label',
            'codename', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RoleSerializer(serializers.ModelSerializer):
    """
    Serializer for Role model.
    """
    
    permissions = PermissionSerializer(many=True, read_only=True)
    permission_count = serializers.SerializerMethodField()
    user_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Role
        fields = [
            'id', 'name', 'display_name', 'description', 'is_active',
            'is_system_role', 'permissions', 'permission_count', 'user_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_permission_count(self, obj):
        """Get count of permissions for this role."""
        return obj.role_permissions.count()
    
    def get_user_count(self, obj):
        """Get count of users with this role."""
        return obj.role_users.filter(is_active=True).count()


class RoleCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating Role.
    """
    
    class Meta:
        model = Role
        fields = ['name', 'display_name', 'description', 'is_active']
    
    def validate_name(self, value):
        """Validate role name."""
        if Role.objects.filter(name=value).exists():
            raise serializers.ValidationError('نقشی با این نام قبلاً وجود دارد.')
        return value


class UserRoleSerializer(serializers.ModelSerializer):
    """
    Serializer for UserRole model.
    """
    
    role_name = serializers.CharField(source='role.display_name', read_only=True)
    role_id = serializers.IntegerField(source='role.id', read_only=True)
    assigned_by_username = serializers.CharField(source='assigned_by.username', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserRole
        fields = [
            'id', 'user', 'user_username', 'role', 'role_id', 'role_name',
            'assigned_by', 'assigned_by_username', 'assigned_at', 'expires_at',
            'is_active'
        ]
        read_only_fields = ['id', 'assigned_at']


class UserRoleCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating UserRole.
    """
    
    class Meta:
        model = UserRole
        fields = ['user', 'role', 'expires_at', 'is_active']
    
    def validate(self, attrs):
        """Validate user role assignment."""
        user = attrs['user']
        role = attrs['role']
        
        # Check if user already has this role
        if UserRole.objects.filter(user=user, role=role).exists():
            raise serializers.ValidationError({
                'role': 'کاربر قبلاً این نقش را دارد.'
            })
        
        # Check if role is active
        if not role.is_active:
            raise serializers.ValidationError({
                'role': 'نقش انتخاب شده غیرفعال است.'
            })
        
        return attrs


class RolePermissionSerializer(serializers.ModelSerializer):
    """
    Serializer for RolePermission model.
    """
    
    permission_name = serializers.CharField(source='permission.display_name', read_only=True)
    permission_id = serializers.IntegerField(source='permission.id', read_only=True)
    role_name = serializers.CharField(source='role.display_name', read_only=True)
    granted_by_username = serializers.CharField(source='granted_by.username', read_only=True)
    
    class Meta:
        model = RolePermission
        fields = [
            'id', 'role', 'role_name', 'permission', 'permission_id',
            'permission_name', 'granted_by', 'granted_by_username', 'granted_at'
        ]
        read_only_fields = ['id', 'granted_at']


class RolePermissionCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating RolePermission.
    """
    
    class Meta:
        model = RolePermission
        fields = ['role', 'permission']
    
    def validate(self, attrs):
        """Validate role permission assignment."""
        role = attrs['role']
        permission = attrs['permission']
        
        # Check if role already has this permission
        if RolePermission.objects.filter(role=role, permission=permission).exists():
            raise serializers.ValidationError({
                'permission': 'نقش قبلاً این مجوز را دارد.'
            })
        
        # Check if role is active
        if not role.is_active:
            raise serializers.ValidationError({
                'role': 'نقش انتخاب شده غیرفعال است.'
            })
        
        # Check if permission is active
        if not permission.is_active:
            raise serializers.ValidationError({
                'permission': 'مجوز انتخاب شده غیرفعال است.'
            })
        
        return attrs


class UserRoleSummarySerializer(serializers.ModelSerializer):
    """
    Serializer for user role summary.
    """
    
    role_name = serializers.CharField(source='role.display_name', read_only=True)
    role_id = serializers.IntegerField(source='role.id', read_only=True)
    is_expired = serializers.SerializerMethodField()
    
    class Meta:
        model = UserRole
        fields = [
            'id', 'role_id', 'role_name', 'assigned_at', 'expires_at',
            'is_active', 'is_expired'
        ]
    
    def get_is_expired(self, obj):
        """Check if role assignment is expired."""
        return obj.is_expired()


class UserWithRolesSerializer(serializers.ModelSerializer):
    """
    Serializer for user with their roles.
    """
    
    roles = UserRoleSummarySerializer(source='user_roles', many=True, read_only=True)
    active_roles = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'is_active', 'roles', 'active_roles'
        ]
    
    def get_active_roles(self, obj):
        """Get active roles for user."""
        active_roles = obj.user_roles.filter(is_active=True)
        return UserRoleSummarySerializer(active_roles, many=True).data
