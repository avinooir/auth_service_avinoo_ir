"""
SSO Admin Configuration
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import SSOClient, SSOSession, SSOAuditLog


@admin.register(SSOClient)
class SSOClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'domain', 'client_id', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'domain', 'client_id']
    readonly_fields = ['id', 'client_id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('اطلاعات کلاینت', {
            'fields': ('name', 'domain', 'client_id', 'client_secret')
        }),
        ('تنظیمات', {
            'fields': ('redirect_uri', 'is_active')
        }),
        ('اطلاعات سیستم', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SSOSession)
class SSOSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'client', 'state', 'is_used', 'created_at', 'expires_at']
    list_filter = ['is_used', 'created_at', 'expires_at']
    search_fields = ['user__username', 'client__name', 'state']
    readonly_fields = ['id', 'created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'client')


@admin.register(SSOAuditLog)
class SSOAuditLogAdmin(admin.ModelAdmin):
    list_display = ['action', 'user', 'client', 'ip_address', 'created_at']
    list_filter = ['action', 'created_at']
    search_fields = ['user__username', 'client__name', 'ip_address']
    readonly_fields = ['id', 'created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'client')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
