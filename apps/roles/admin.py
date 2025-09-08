"""
Admin configuration for Role app.
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Role, UserRole, Permission, RolePermission


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """
    Role admin.
    """
    
    list_display = [
        'name', 'display_name', 'is_active', 'is_system_role',
        'created_at', 'updated_at'
    ]
    
    list_filter = ['is_active', 'is_system_role', 'created_at']
    
    search_fields = ['name', 'display_name', 'description']
    
    ordering = ['name']
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'display_name', 'description')
        }),
        (_('Status'), {
            'fields': ('is_active', 'is_system_role')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    """
    UserRole admin.
    """
    
    list_display = [
        'user', 'role', 'assigned_by', 'assigned_at', 'expires_at',
        'is_active'
    ]
    
    list_filter = ['is_active', 'assigned_at', 'expires_at']
    
    search_fields = [
        'user__username', 'user__email', 'role__name', 'role__display_name'
    ]
    
    ordering = ['-assigned_at']
    
    fieldsets = (
        (_('Assignment'), {
            'fields': ('user', 'role', 'assigned_by')
        }),
        (_('Status'), {
            'fields': ('is_active', 'expires_at')
        }),
        (_('Timestamps'), {
            'fields': ('assigned_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['assigned_at']


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    """
    Permission admin.
    """
    
    list_display = [
        'name', 'display_name', 'app_label', 'codename', 'is_active',
        'created_at'
    ]
    
    list_filter = ['is_active', 'app_label', 'created_at']
    
    search_fields = ['name', 'display_name', 'description', 'app_label', 'codename']
    
    ordering = ['app_label', 'codename']
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'display_name', 'description')
        }),
        (_('Technical Details'), {
            'fields': ('app_label', 'codename')
        }),
        (_('Status'), {
            'fields': ('is_active',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    """
    RolePermission admin.
    """
    
    list_display = [
        'role', 'permission', 'granted_by', 'granted_at'
    ]
    
    list_filter = ['granted_at']
    
    search_fields = [
        'role__name', 'role__display_name', 'permission__name', 'permission__display_name'
    ]
    
    ordering = ['-granted_at']
    
    fieldsets = (
        (_('Assignment'), {
            'fields': ('role', 'permission', 'granted_by')
        }),
        (_('Timestamps'), {
            'fields': ('granted_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['granted_at']
