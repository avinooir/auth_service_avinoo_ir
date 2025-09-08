"""
Permission models for authentication service.
"""

import logging
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

logger = logging.getLogger(__name__)
User = get_user_model()


class UserPermission(models.Model):
    """
    Direct user permissions (bypassing roles).
    """
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='direct_permissions',
        verbose_name="کاربر"
    )
    
    permission = models.ForeignKey(
        'roles.Permission',
        on_delete=models.CASCADE,
        related_name='permission_users',
        verbose_name="مجوز"
    )
    
    granted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='granted_user_permissions',
        verbose_name="اعطا شده توسط"
    )
    
    granted_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ اعطا"
    )
    
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="تاریخ انقضا"
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال"
    )
    
    class Meta:
        verbose_name = "مجوز کاربر"
        verbose_name_plural = "مجوزهای کاربران"
        db_table = 'user_permissions'
        unique_together = ['user', 'permission']
        ordering = ['-granted_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.permission.display_name}"
    
    def is_expired(self):
        """Check if permission is expired."""
        if self.expires_at:
            from django.utils import timezone
            return timezone.now() > self.expires_at
        return False


class PermissionGroup(models.Model):
    """
    Group of permissions for easier management.
    """
    
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="نام گروه"
    )
    
    display_name = models.CharField(
        max_length=150,
        verbose_name="نام نمایشی"
    )
    
    description = models.TextField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name="توضیحات"
    )
    
    app_label = models.CharField(
        max_length=50,
        verbose_name="برچسب اپلیکیشن"
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ بروزرسانی"
    )
    
    class Meta:
        verbose_name = "گروه مجوز"
        verbose_name_plural = "گروه‌های مجوز"
        db_table = 'permission_groups'
        ordering = ['app_label', 'name']
    
    def __str__(self):
        return f"{self.display_name} ({self.name})"


class PermissionGroupPermission(models.Model):
    """
    Many-to-many relationship between PermissionGroup and Permission.
    """
    
    group = models.ForeignKey(
        PermissionGroup,
        on_delete=models.CASCADE,
        related_name='group_permissions',
        verbose_name="گروه"
    )
    
    permission = models.ForeignKey(
        'roles.Permission',
        on_delete=models.CASCADE,
        related_name='permission_groups',
        verbose_name="مجوز"
    )
    
    added_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='added_group_permissions',
        verbose_name="اضافه شده توسط"
    )
    
    added_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ اضافه شدن"
    )
    
    class Meta:
        verbose_name = "مجوز گروه"
        verbose_name_plural = "مجوزهای گروه‌ها"
        db_table = 'permission_group_permissions'
        unique_together = ['group', 'permission']
        ordering = ['-added_at']
    
    def __str__(self):
        return f"{self.group.display_name} - {self.permission.display_name}"


class AuditLog(models.Model):
    """
    Audit log for permission changes.
    """
    
    ACTION_CHOICES = [
        ('grant', 'اعطا'),
        ('revoke', 'لغو'),
        ('assign_role', 'اختصاص نقش'),
        ('remove_role', 'حذف نقش'),
        ('create_role', 'ایجاد نقش'),
        ('delete_role', 'حذف نقش'),
        ('update_role', 'بروزرسانی نقش'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs',
        verbose_name="کاربر"
    )
    
    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES,
        verbose_name="عمل"
    )
    
    target_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='target_audit_logs',
        verbose_name="کاربر هدف"
    )
    
    permission = models.ForeignKey(
        'roles.Permission',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="مجوز"
    )
    
    role = models.ForeignKey(
        'roles.Role',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="نقش"
    )
    
    details = models.JSONField(
        null=True,
        blank=True,
        verbose_name="جزئیات"
    )
    
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="آدرس IP"
    )
    
    user_agent = models.TextField(
        null=True,
        blank=True,
        verbose_name="User Agent"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )
    
    class Meta:
        verbose_name = "لاگ حسابرسی"
        verbose_name_plural = "لاگ‌های حسابرسی"
        db_table = 'audit_logs'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_action_display()} - {self.user} - {self.created_at}"
