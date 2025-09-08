# 🔐 سیستم SSO (Single Sign-On)

یک سرویس احراز هویت مرکزی برای میکروسرویس‌ها

## ⚡ شروع سریع

### 1. نصب
```bash
pip install -r requirements.txt
cp env.example .env  # تنظیمات environment
python manage.py migrate
python manage.py createsuperuser
```

### 2. اجرا
```bash
python manage.py runserver
```

### 3. تست
```
http://127.0.0.1:8000/test/
```

## 🎯 ویژگی‌ها

- ✅ **احراز هویت مرکزی**: یک بار ورود، دسترسی به همه
- ✅ **JWT Token**: امن و قابل اعتماد
- ✅ **RESTful API**: ساده و استاندارد
- ✅ **Session Management**: مدیریت جلسات
- ✅ **Client Registration**: ثبت اپلیکیشن‌های جدید
- ✅ **Audit Logging**: ردیابی فعالیت‌ها

## 📚 مستندات

- [مستندات کامل](docs/SSO_USAGE.md)
- [API Documentation](docs/API.md)
- [Deployment Guide](docs/DEPLOYMENT.md)

## 🔌 API Endpoints

| Method | Endpoint | توضیح |
|--------|----------|-------|
| POST | `/api/login/` | ورود کاربر |
| POST | `/api/register/` | ثبت‌نام کاربر |
| POST | `/api/validate-token/` | اعتبارسنجی token |
| GET/POST | `/api/logout/` | خروج کاربر |
| GET | `/api/user-info/` | اطلاعات کاربر |

## 🌐 صفحات وب

| صفحه | آدرس | توضیح |
|------|-------|-------|
| ورود | `/login/` | صفحه ورود SSO |
| ثبت‌نام | `/register/` | صفحه ثبت‌نام |
| تست | `/test/` | صفحه تست (محافظت شده) |

## 💡 مثال استفاده

### ورود با JavaScript
```javascript
fetch('/api/login/', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
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
        localStorage.setItem('access_token', data.access_token);
        window.location.href = data.redirect_uri;
    }
});
```

### خروج
```javascript
fetch('/api/logout/?client_id=test_page_client&token=' + localStorage.getItem('access_token'))
.then(response => response.json())
.then(data => {
    if (data.success) {
        localStorage.removeItem('access_token');
        window.location.href = '/';
    }
});
```

## 🛠 تنظیمات

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

SSOClient.objects.create(
    name='My App',
    domain=settings.AUTH_SERVICE_DOMAIN,
    client_id='my_app_client',
    client_secret='my_secret',
    redirect_uri=f'http://{settings.AUTH_SERVICE_DOMAIN}/my_app/callback/',
    is_active=True
)
```

## 🔍 Debugging

### بررسی لاگ‌ها
```bash
# Windows
Get-Content logs/django.log -Tail 20

# Linux/Mac
tail -f logs/django.log
```

### Admin Panel
```
http://127.0.0.1:8000/admin/
```

## 📋 Requirements

- Python 3.9+
- Django 4.2+
- djangorestframework
- djangorestframework-simplejwt

## 🚀 Deploy

### Production
```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
SECURE_SSL_REDIRECT = True
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

- 📧 Email: support@example.com
- 📱 Telegram: @support
- 🐛 Issues: GitHub Issues

---

**نسخه**: 1.0  
**تاریخ**: 2025-09-08  
**وضعیت**: ✅ آماده استفاده
