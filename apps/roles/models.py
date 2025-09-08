"""
Role models for authentication service.
"""

import logging
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

logger = logging.getLogger(__name__)
User = get_user_model()


class Role(models.Model):
    """
    Role model for user roles and permissions.
    """
    
    # Role name validator
    name_regex = RegexValidator(
        regex=r'^[a-zA-Z0-9_-]+$',
        message="نام نقش باید شامل حروف انگلیسی، اعداد، خط تیره و زیرخط باشد."
    )
    
    name = models.CharField(
        max_length=50,
        unique=True,
        validators=[name_regex],
        verbose_name="نام نقش"
    )
    
    display_name = models.CharField(
        max_length=100,
        verbose_name="نام نمایشی"
    )
    
    description = models.TextField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name="توضیحات"
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال"
    )
    
    is_system_role = models.BooleanField(
        default=False,
        verbose_name="نقش سیستمی"
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
        verbose_name = "نقش"
        verbose_name_plural = "نقش‌ها"
        db_table = 'roles'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.display_name} ({self.name})"
    
    def save(self, *args, **kwargs):
        """Save role with validation."""
        if not self.display_name:
            self.display_name = self.name.replace('_', ' ').title()
        super().save(*args, **kwargs)


class UserRole(models.Model):
    """
    Many-to-many relationship between User and Role.
    """
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_roles',
        verbose_name="کاربر"
    )
    
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name='role_users',
        verbose_name="نقش"
    )
    
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_roles',
        verbose_name="اختصاص داده شده توسط"
    )
    
    assigned_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ اختصاص"
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
        verbose_name = "نقش کاربر"
        verbose_name_plural = "نقش‌های کاربران"
        db_table = 'user_roles'
        unique_together = ['user', 'role']
        ordering = ['-assigned_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.role.display_name}"
    
    def is_expired(self):
        """Check if role assignment is expired."""
        if self.expires_at:
            from django.utils import timezone
            return timezone.now() > self.expires_at
        return False


class Permission(models.Model):
    """
    Permission model for fine-grained access control.
    """
    
    # Permission name validator
    name_regex = RegexValidator(
        regex=r'^[a-zA-Z0-9_.-]+$',
        message="نام مجوز باید شامل حروف انگلیسی، اعداد، نقطه، خط تیره و زیرخط باشد."
    )
    
    name = models.CharField(
        max_length=100,
        unique=True,
        validators=[name_regex],
        verbose_name="نام مجوز"
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
    
    codename = models.CharField(
        max_length=100,
        verbose_name="کد نام"
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
        verbose_name = "مجوز"
        verbose_name_plural = "مجوزها"
        db_table = 'permissions'
        ordering = ['app_label', 'codename']
    
    def __str__(self):
        return f"{self.display_name} ({self.name})"


class RolePermission(models.Model):
    """
    Many-to-many relationship between Role and Permission.
    """
    
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name='role_permissions',
        verbose_name="نقش"
    )
    
    permission = models.ForeignKey(
        Permission,
        on_delete=models.CASCADE,
        related_name='permission_roles',
        verbose_name="مجوز"
    )
    
    granted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='granted_permissions',
        verbose_name="اعطا شده توسط"
    )
    
    granted_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ اعطا"
    )
    
    class Meta:
        verbose_name = "مجوز نقش"
        verbose_name_plural = "مجوزهای نقش‌ها"
        db_table = 'role_permissions'
        unique_together = ['role', 'permission']
        ordering = ['-granted_at']
    
    def __str__(self):
        return f"{self.role.display_name} - {self.permission.display_name}"
