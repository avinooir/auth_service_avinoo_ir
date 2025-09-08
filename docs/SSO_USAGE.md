# مستندات سیستم SSO (Single Sign-On)

## 📋 فهرست مطالب
- [معرفی سیستم](#معرفی-سیستم)
- [نصب و راه‌اندازی](#نصب-و-راه‌اندازی)
- [استفاده از API](#استفاده-از-api)
- [صفحات وب](#صفحات-وب)
- [مثال‌های کاربردی](#مثال‌های-کاربردی)
- [خطاها و راه‌حل](#خطاها-و-راه‌حل)

## 🚀 معرفی سیستم

سیستم SSO یک سرویس احراز هویت مرکزی است که به کاربران اجازه می‌دهد با یک بار ورود، به تمام اپلیکیشن‌های متصل دسترسی داشته باشند.

### ویژگی‌های کلیدی:
- ✅ احراز هویت مرکزی
- ✅ JWT Token Support
- ✅ Session Management
- ✅ Client Registration
- ✅ Audit Logging
- ✅ RESTful API

## 🛠 نصب و راه‌اندازی

### 1. نصب Dependencies
```bash
pip install -r requirements.txt
```

### 2. تنظیم Environment Variables
```bash
# کپی کردن فایل نمونه
cp env.example .env

# ویرایش تنظیمات (اختیاری)
# AUTH_SERVICE_DOMAIN=127.0.0.1:8000  # برای development
# AUTH_SERVICE_DOMAIN=auth.avinoo.ir  # برای production
```

### 3. تنظیم Database
```bash
python manage.py migrate
```

### 4. ایجاد Superuser
```bash
python manage.py createsuperuser
```

### 5. اجرای سرور
```bash
python manage.py runserver
```

## 🔌 استفاده از API

### Base URL
```
http://127.0.0.1:8000/
```

### 1. ورود (Login)

#### POST `/api/login/`
```json
{
    "username": "mohammad",
    "password": "1",
    "client_id": "test_page_client",
    "redirect_uri": "http://127.0.0.1:8000/test/callback/",
    "state": "optional_state"
}
```

#### پاسخ موفق:
```json
{
    "success": true,
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "Bearer",
    "expires_in": 3600,
    "redirect_uri": "http://127.0.0.1:8000/test/callback/?token=...&state=...",
    "user": {
        "id": 3,
        "username": "mohammad",
        "email": "mohammad.rahimaee@gmail.com",
        "first_name": "",
        "last_name": ""
    }
}
```

### 2. ثبت‌نام (Register)

#### POST `/api/register/`
```json
{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "password123",
    "password_confirm": "password123",
    "client_id": "test_page_client",
    "redirect_uri": "http://127.0.0.1:8000/test/callback/"
}
```

### 3. اعتبارسنجی Token

#### POST `/api/validate-token/`
```json
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "client_id": "test_page_client"
}
```

### 4. خروج (Logout)

#### GET `/api/logout/`
```
GET /api/logout/?client_id=test_page_client&redirect_uri=http://127.0.0.1:8000/test/&token=your_token
```

#### POST `/api/logout/`
```json
{
    "client_id": "test_page_client",
    "redirect_uri": "http://127.0.0.1:8000/test/",
    "token": "your_token"
}
```

### 5. اطلاعات کاربر

#### GET `/api/user-info/`
```
GET /api/user-info/?token=your_token
```

## 🌐 صفحات وب

### 1. صفحه ورود
```
http://127.0.0.1:8000/login/?client_id=test_page_client&redirect_uri=http://127.0.0.1:8000/test/callback/
```

### 2. صفحه ثبت‌نام
```
http://127.0.0.1:8000/register/?client_id=test_page_client&redirect_uri=http://127.0.0.1:8000/test/callback/
```

### 3. صفحه تست (محافظت شده)
```
http://127.0.0.1:8000/test/
```

## 📝 مثال‌های کاربردی

### مثال 1: ورود با JavaScript
```javascript
// ورود
fetch('/api/login/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({
        username: 'mohammad',
        password: '1',
        client_id: 'test_page_client',
        redirect_uri: 'http://127.0.0.1:8000/test/callback/'
    })
})
.then(response => response.json())
.then(data => {
    if (data.success) {
        // ذخیره token
        localStorage.setItem('access_token', data.access_token);
        // انتقال به callback
        window.location.href = data.redirect_uri;
    }
});
```

### مثال 2: خروج با JavaScript
```javascript
// خروج
fetch('/api/logout/?client_id=test_page_client&token=' + localStorage.getItem('access_token'))
.then(response => response.json())
.then(data => {
    if (data.success) {
        // پاک کردن token
        localStorage.removeItem('access_token');
        // انتقال به صفحه اصلی
        window.location.href = '/';
    }
});
```

### مثال 3: اعتبارسنجی Token
```javascript
// اعتبارسنجی token
fetch('/api/validate-token/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        token: localStorage.getItem('access_token'),
        client_id: 'test_page_client'
    })
})
.then(response => response.json())
.then(data => {
    if (data.valid) {
        console.log('کاربر معتبر:', data.user);
    } else {
        console.log('کاربر نامعتبر');
    }
});
```

## 🔧 تنظیمات Client

### تنظیمات Environment
```bash
# در فایل .env
AUTH_SERVICE_DOMAIN=127.0.0.1:8000  # برای development
AUTH_SERVICE_DOMAIN=auth.avinoo.ir  # برای production
```

### ایجاد Client جدید
```python
from sso.models import SSOClient
from django.conf import settings

client = SSOClient.objects.create(
    name='My App',
    domain=settings.AUTH_SERVICE_DOMAIN,
    client_id='my_app_client',
    client_secret='my_secret_key',
    redirect_uri=f'http://{settings.AUTH_SERVICE_DOMAIN}/my_app/callback/',
    is_active=True
)
```

### تنظیمات JWT
```python
# در settings.py
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': SECRET_KEY,
}
```

## ❌ خطاها و راه‌حل

### خطای 400: اطلاعات ورودی نامعتبر
```json
{
    "success": false,
    "error": "اطلاعات ورودی نامعتبر است",
    "errors": {
        "username": ["این فیلد الزامی است."]
    }
}
```
**راه‌حل**: بررسی کنید تمام فیلدهای الزامی ارسال شده باشند.

### خطای 401: عدم احراز هویت
```json
{
    "detail": "اطلاعات برای اعتبارسنجی ارسال نشده است."
}
```
**راه‌حل**: token معتبر ارسال کنید یا از `AllowAny` permission استفاده کنید.

### خطای 500: خطای سرور
```json
{
    "success": false,
    "error": "خطا در ورود به سیستم"
}
```
**راه‌حل**: لاگ‌های سرور را بررسی کنید.

## 🔍 Debugging

### فعال‌سازی Logging
```python
# در settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/django.log',
        },
    },
    'loggers': {
        'sso': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### بررسی لاگ‌ها
```bash
# Windows PowerShell
Get-Content logs/django.log -Tail 20

# Linux/Mac
tail -f logs/django.log
```

## 📊 مدیریت Admin

### دسترسی به Admin Panel
```
http://127.0.0.1:8000/admin/
```

### مدیریت SSO Clients
- ایجاد client جدید
- ویرایش تنظیمات client
- فعال/غیرفعال کردن client

### مدیریت Sessions
- مشاهده جلسات فعال
- حذف جلسات منقضی شده

### Audit Logs
- مشاهده لاگ‌های فعالیت
- ردیابی ورود/خروج کاربران

## 🚀 Deploy

### تنظیمات Production
```python
# در settings.py
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']

# تنظیمات امنیتی
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### Docker
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 📞 پشتیبانی

برای سوالات و مشکلات:
1. بررسی لاگ‌های سیستم
2. تست endpoint ها با Postman
3. بررسی تنظیمات client
4. تماس با تیم توسعه

---

**نسخه**: 1.0  
**تاریخ**: 2025-09-08  
**نویسنده**: تیم توسعه SSO
