"""
Admin configuration for Permissions app.
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import UserPermission, PermissionGroup, PermissionGroupPermission, AuditLog


@admin.register(UserPermission)
class UserPermissionAdmin(admin.ModelAdmin):
    """
    UserPermission admin.
    """
    
    list_display = [
        'user', 'permission', 'granted_by', 'granted_at', 'expires_at',
        'is_active'
    ]
    
    list_filter = ['is_active', 'granted_at', 'expires_at']
    
    search_fields = [
        'user__username', 'user__email', 'permission__name', 'permission__display_name'
    ]
    
    ordering = ['-granted_at']
    
    fieldsets = (
        (_('Assignment'), {
            'fields': ('user', 'permission', 'granted_by')
        }),
        (_('Status'), {
            'fields': ('is_active', 'expires_at')
        }),
        (_('Timestamps'), {
            'fields': ('granted_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['granted_at']


@admin.register(PermissionGroup)
class PermissionGroupAdmin(admin.ModelAdmin):
    """
    PermissionGroup admin.
    """
    
    list_display = [
        'name', 'display_name', 'app_label', 'is_active', 'created_at'
    ]
    
    list_filter = ['is_active', 'app_label', 'created_at']
    
    search_fields = ['name', 'display_name', 'description']
    
    ordering = ['app_label', 'name']
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'display_name', 'description', 'app_label')
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


@admin.register(PermissionGroupPermission)
class PermissionGroupPermissionAdmin(admin.ModelAdmin):
    """
    PermissionGroupPermission admin.
    """
    
    list_display = [
        'group', 'permission', 'added_by', 'added_at'
    ]
    
    list_filter = ['added_at']
    
    search_fields = [
        'group__name', 'group__display_name', 'permission__name', 'permission__display_name'
    ]
    
    ordering = ['-added_at']
    
    fieldsets = (
        (_('Assignment'), {
            'fields': ('group', 'permission', 'added_by')
        }),
        (_('Timestamps'), {
            'fields': ('added_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['added_at']


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """
    AuditLog admin.
    """
    
    list_display = [
        'user', 'action', 'target_user', 'permission', 'role', 'created_at'
    ]
    
    list_filter = ['action', 'created_at']
    
    search_fields = [
        'user__username', 'target_user__username', 'permission__name', 'role__name'
    ]
    
    ordering = ['-created_at']
    
    fieldsets = (
        (_('Action Details'), {
            'fields': ('user', 'action', 'target_user')
        }),
        (_('Targets'), {
            'fields': ('permission', 'role')
        }),
        (_('Additional Info'), {
            'fields': ('details', 'ip_address', 'user_agent')
        }),
        (_('Timestamps'), {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at']
