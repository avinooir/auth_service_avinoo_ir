"""
SSO Models for microservice authentication
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid

User = get_user_model()


class SSOClient(models.Model):
    """
    Model for registered client applications that can use SSO
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, verbose_name="نام اپلیکیشن")
    domain = models.CharField(max_length=255, unique=True, verbose_name="دامنه")
    client_id = models.CharField(max_length=100, unique=True, verbose_name="شناسه کلاینت")
    client_secret = models.CharField(max_length=255, verbose_name="رمز کلاینت")
    redirect_uri = models.URLField(verbose_name="آدرس بازگشت")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ به‌روزرسانی")
    
    class Meta:
        verbose_name = "کلاینت SSO"
        verbose_name_plural = "کلاینت‌های SSO"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.domain})"


class SSOSession(models.Model):
    """
    Model for tracking SSO sessions and redirects
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    client = models.ForeignKey(SSOClient, on_delete=models.CASCADE, verbose_name="کلاینت")
    state = models.CharField(max_length=255, null=True, blank=True, verbose_name="وضعیت")
    redirect_uri = models.URLField(verbose_name="آدرس بازگشت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    expires_at = models.DateTimeField(verbose_name="تاریخ انقضا")
    is_used = models.BooleanField(default=False, verbose_name="استفاده شده")
    
    class Meta:
        verbose_name = "جلسه SSO"
        verbose_name_plural = "جلسات SSO"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"SSO Session: {self.user.username} -> {self.client.name}"
    
    def is_expired(self):
        return timezone.now() > self.expires_at


class SSOAuditLog(models.Model):
    """
    Model for auditing SSO activities
    """
    ACTION_CHOICES = [
        ('login', 'ورود'),
        ('logout', 'خروج'),
        ('token_issued', 'صدور توکن'),
        ('token_validated', 'اعتبارسنجی توکن'),
        ('redirect', 'انتقال'),
        ('error', 'خطا'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="کاربر")
    client = models.ForeignKey(SSOClient, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="کلاینت")
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, verbose_name="عمل")
    ip_address = models.GenericIPAddressField(verbose_name="آدرس IP")
    user_agent = models.TextField(blank=True, verbose_name="User Agent")
    details = models.JSONField(default=dict, blank=True, verbose_name="جزئیات")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    
    class Meta:
        verbose_name = "لاگ حسابرسی SSO"
        verbose_name_plural = "لاگ‌های حسابرسی SSO"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.action}: {self.user.username if self.user else 'Anonymous'} -> {self.client.name if self.client else 'Unknown'}"
