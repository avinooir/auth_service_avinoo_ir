"""
User models for authentication service.
"""

import logging
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

logger = logging.getLogger(__name__)


class User(AbstractUser):
    """
    Custom User model with additional fields for authentication service.
    """
    
    # Phone number validator
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="شماره تلفن باید در فرمت صحیح وارد شود. مثال: '+989123456789'"
    )
    
    # Global Unique Identifier
    guid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        verbose_name="شناسه یکتا جهانی"
    )
    
    # Additional fields
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        unique=True,
        null=True,
        blank=True,
        verbose_name="شماره تلفن"
    )
    
    is_phone_verified = models.BooleanField(
        default=False,
        verbose_name="تأیید شماره تلفن"
    )
    
    is_email_verified = models.BooleanField(
        default=False,
        verbose_name="تأیید ایمیل"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ بروزرسانی"
    )
    
    last_login_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="آخرین IP ورود"
    )
    
    failed_login_attempts = models.PositiveIntegerField(
        default=0,
        verbose_name="تعداد تلاش‌های ناموفق ورود"
    )
    
    locked_until = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="قفل شده تا"
    )
    
    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
        db_table = 'users'
    
    def __str__(self):
        return f"{self.username} ({self.email})"
    
    def is_locked(self):
        """Check if user account is locked."""
        if self.locked_until and self.locked_until > timezone.now():
            return True
        return False
    
    def lock_account(self, minutes=30):
        """Lock user account for specified minutes."""
        self.locked_until = timezone.now() + timezone.timedelta(minutes=minutes)
        self.save(update_fields=['locked_until'])
        logger.warning(f"User {self.username} account locked until {self.locked_until}")
    
    def unlock_account(self):
        """Unlock user account."""
        self.locked_until = None
        self.failed_login_attempts = 0
        self.save(update_fields=['locked_until', 'failed_login_attempts'])
        logger.info(f"User {self.username} account unlocked")
    
    def increment_failed_login(self):
        """Increment failed login attempts."""
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:  # Lock after 5 failed attempts
            self.lock_account()
        self.save(update_fields=['failed_login_attempts'])
    
    def reset_failed_login(self):
        """Reset failed login attempts."""
        self.failed_login_attempts = 0
        self.save(update_fields=['failed_login_attempts'])
    
    def update_last_login_ip(self, ip_address):
        """Update last login IP address."""
        self.last_login_ip = ip_address
        self.save(update_fields=['last_login_ip'])


class UserProfile(models.Model):
    """
    Extended user profile information.
    """
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name="کاربر"
    )
    
    first_name_fa = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="نام (فارسی)"
    )
    
    last_name_fa = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="نام خانوادگی (فارسی)"
    )
    
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        verbose_name="تصویر پروفایل"
    )
    
    bio = models.TextField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name="بیوگرافی"
    )
    
    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="تاریخ تولد"
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
        verbose_name = "پروفایل کاربر"
        verbose_name_plural = "پروفایل‌های کاربران"
        db_table = 'user_profiles'
    
    def __str__(self):
        return f"Profile of {self.user.username}"
    
    @property
    def full_name_fa(self):
        """Return full name in Persian."""
        if self.first_name_fa and self.last_name_fa:
            return f"{self.first_name_fa} {self.last_name_fa}"
        return None
