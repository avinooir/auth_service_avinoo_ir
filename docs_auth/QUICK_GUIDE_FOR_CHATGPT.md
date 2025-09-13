# 🚀 راهنمای سریع SSO برای ChatGPT

## 📋 خلاصه سیستم SSO

سیستم SSO شما یک سرویس احراز هویت متمرکز است که:
- از JWT tokens استفاده می‌کند
- Django REST Framework دارد
- چندین کلاینت را پشتیبانی می‌کند
- اطلاعات کاربر، نقش‌ها و مجوزها را مدیریت می‌کند

## 🏗️ ساختار اصلی

### Models موجود:
```python
# User Model (apps/users/models.py)
class User(AbstractUser):
    phone_number = models.CharField(max_length=17, unique=True, null=True)
    is_phone_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    last_login_ip = models.GenericIPAddressField(null=True)
    failed_login_attempts = models.PositiveIntegerField(default=0)
    locked_until = models.DateTimeField(null=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name_fa = models.CharField(max_length=50)
    last_name_fa = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='avatars/')
    bio = models.TextField(max_length=500)
    birth_date = models.DateField()

# SSO Models (sso/models.py)
class SSOClient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    domain = models.CharField(max_length=255, unique=True)
    client_id = models.CharField(max_length=100, unique=True)
    client_secret = models.CharField(max_length=255)
    redirect_uri = models.URLField()
    allowed_redirect_uris = models.JSONField(default=list)
    allow_any_path = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

class SSOSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(SSOClient, on_delete=models.CASCADE)
    state = models.CharField(max_length=255)
    redirect_uri = models.URLField()
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

class SSOAuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    client = models.ForeignKey(SSOClient, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    details = models.JSONField(default=dict)
```

## 🔗 API Endpoints اصلی

### SSO APIs:
```
POST /sso/api/login/          # ورود کاربر
POST /sso/api/register/       # ثبت‌نام کاربر
POST /sso/api/validate-token/ # اعتبارسنجی توکن
GET  /sso/api/user-info/      # اطلاعات کاربر
POST /sso/api/logout/         # خروج کاربر
GET  /sso/login/              # صفحه ورود وب
GET  /sso/callback/           # صفحه بازگشت
```

### User Management APIs:
```
GET  /users/                  # لیست کاربران
GET  /users/{id}/             # جزئیات کاربر
POST /users/                  # ایجاد کاربر
PUT  /users/{id}/             # ویرایش کاربر
```

### Role & Permission APIs:
```
GET  /roles/                  # لیست نقش‌ها
POST /roles/                  # ایجاد نقش
GET  /roles/users/{id}/roles/ # نقش‌های کاربر
POST /permissions/user-permissions/ # اعطای مجوز
```

## 📝 نمونه درخواست‌ها

### ورود کاربر:
```json
POST /sso/api/login/
{
    "username": "user123",
    "password": "password123",
    "client_id": "myapp_client",
    "redirect_uri": "https://myapp.com/callback"
}
```

### پاسخ موفق:
```json
{
    "success": true,
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "Bearer",
    "expires_in": 900,
    "user": {
        "id": 1,
        "username": "user123",
        "email": "user@example.com",
        "first_name": "علی",
        "last_name": "احمدی"
    }
}
```

### اعتبارسنجی توکن:
```json
POST /sso/api/validate-token/
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "client_id": "myapp_client"
}
```

## 🎯 درخواست از ChatGPT

**از ChatGPT بخواهید:**

"بر اساس سیستم SSO Django که توضیح دادم، یک مدل جدید برای [نام مدل] بنویس که:

1. **با User model ارتباط داشته باشد** (ForeignKey یا OneToOneField)
2. **از JWT authentication استفاده کند** (IsAuthenticated permission)
3. **API endpoints داشته باشد** (CRUD operations)
4. **Serializer مناسب داشته باشد**
5. **Admin interface داشته باشد**
6. **Validation rules داشته باشد**
7. **Audit logging داشته باشد** (مانند SSOAuditLog)
8. **Permissions مناسب داشته باشد** (برای دسترسی‌های مختلف)

**ویژگی‌های خاص مدل:**
- [ویژگی‌های مورد نظر خود را اینجا بنویسید]

**مثال:**
- اگر می‌خواهید مدل "Product" بنویسید:
  - با User ارتباط داشته باشد (مالک محصول)
  - قیمت، نام، توضیحات داشته باشد
  - API برای لیست، ایجاد، ویرایش، حذف
  - فقط مالک بتواند ویرایش کند

**فرمت خروجی:**
- Model class کامل
- Serializer class
- ViewSet class
- URL patterns
- Admin class
- Migration file"

## 🔧 نکات مهم برای ChatGPT

### 1. ساختار فایل‌ها:
```
apps/
├── users/           # مدیریت کاربران
├── roles/           # مدیریت نقش‌ها  
├── permissions/     # مدیریت مجوزها
└── [new_app]/       # اپ جدید شما
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    └── admin.py
```

### 2. Import های ضروری:
```python
from django.db import models
from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib import admin
from django.utils import timezone
import uuid

User = get_user_model()
```

### 3. Permission Classes:
```python
# برای احراز هویت
permission_classes = [IsAuthenticated]

# برای مالکیت
permission_classes = [IsOwnerOrReadOnly]

# برای ادمین
permission_classes = [IsAdminUser]
```

### 4. Serializer Patterns:
```python
class ModelSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = YourModel
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
```

### 5. ViewSet Patterns:
```python
class ModelViewSet(viewsets.ModelViewSet):
    serializer_class = ModelSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return YourModel.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
```

## 📚 مثال کامل

**درخواست نمونه:**
"بر اساس SSO Django من، یک مدل 'Task' بنویس که:
- هر کاربر بتواند task های خودش را ببیند
- task ها title، description، status، due_date داشته باشند
- status choices: pending، in_progress، completed
- API کامل CRUD داشته باشد
- فقط مالک task بتواند ویرایش کند
- admin interface داشته باشد"

**ChatGPT باید این‌ها را تولید کند:**
1. Task model با فیلدهای مناسب
2. TaskSerializer
3. TaskViewSet با permissions
4. URL patterns
5. TaskAdmin
6. Migration file

---

**نکته:** این راهنما را کپی کنید و به ChatGPT بدهید تا مدل‌های مناسب سیستم SSO شما را بنویسد! 🚀
