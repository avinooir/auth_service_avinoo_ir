"""
Admin configuration for User app.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, UserProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom User admin.
    """
    
    list_display = [
        'username', 'email', 'phone_number', 'first_name', 'last_name',
        'is_active', 'is_staff', 'is_superuser', 'is_phone_verified',
        'is_email_verified', 'date_joined', 'last_login'
    ]
    
    list_filter = [
        'is_active', 'is_staff', 'is_superuser', 'is_phone_verified',
        'is_email_verified', 'date_joined', 'last_login'
    ]
    
    search_fields = ['username', 'email', 'phone_number', 'first_name', 'last_name']
    
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'email', 'phone_number')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Verification'), {
            'fields': ('is_phone_verified', 'is_email_verified')
        }),
        (_('Security'), {
            'fields': ('last_login_ip', 'failed_login_attempts', 'locked_until')
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ['date_joined', 'last_login', 'last_login_ip']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    User Profile admin.
    """
    
    list_display = [
        'user', 'first_name_fa', 'last_name_fa', 'full_name_fa',
        'created_at', 'updated_at'
    ]
    
    list_filter = ['created_at', 'updated_at']
    
    search_fields = [
        'user__username', 'user__email', 'first_name_fa', 'last_name_fa'
    ]
    
    ordering = ['-created_at']
    
    fieldsets = (
        (_('User'), {'fields': ('user',)}),
        (_('Persian Info'), {
            'fields': ('first_name_fa', 'last_name_fa')
        }),
        (_('Profile'), {
            'fields': ('avatar', 'bio', 'birth_date')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
