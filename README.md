# 🔐 سرویس احراز هویت مرکزی (Auth Service) - Avinoo.ir

یک سیستم احراز هویت میکروسرویسی کامل با Django + DRF که از JWT با RSA برای امنیت بالا استفاده می‌کند.

## 📋 ویژگی‌های کلیدی

### 🌐 معماری میکروسرویس
- **سرویس مرکزی**: `auth.avinoo.ir` - مدیریت تمام احراز هویت‌ها
- **کلاینت‌ها**: `app1.avinoo.ir`, `app2.avinoo.ir` - اپلیکیشن‌های مختلف
- **Single Sign-On (SSO)**: ورود یکباره در تمام اپلیکیشن‌ها
- **JWT با RSA**: امنیت بالا با کلیدهای عمومی/خصوصی

### 🔑 احراز هویت
- **ثبت‌نام و ورود** با اعتبارسنجی کامل
- **JWT Token** با انقضای قابل تنظیم
- **Refresh Token** برای امنیت بیشتر
- **تأیید شماره تلفن و ایمیل**
- **قفل کردن حساب** پس از تلاش‌های ناموفق
- **Rate Limiting** برای جلوگیری از حملات

### 👥 مدیریت نقش‌ها و مجوزها
- **نقش‌های سیستمی و سفارشی**
- **اختصاص نقش به کاربران**
- **مدیریت مجوزهای نقش‌ها**
- **مجوزهای مستقیم کاربران**
- **لاگ حسابرسی کامل**

### 🛡️ امنیت
- **JWT Authentication** با SimpleJWT
- **RSA Key Pair** برای امضای توکن‌ها
- **CORS Configuration** برای میکروسرویس‌ها
- **Rate Limiting** و IP Tracking
- **Audit Logging** کامل
- **Password Validation** پیشرفته

## 🏗️ معماری سیستم

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   app1.avinoo.ir │    │   app2.avinoo.ir │    │  admin.avinoo.ir │
│                 │    │                 │    │                 │
│  Client App 1   │    │  Client App 2   │    │  Admin Panel    │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │                           │
                    │    auth.avinoo.ir         │
                    │                           │
                    │   Auth Service (Django)   │
                    │                           │
                    │  • User Management        │
                    │  • JWT Token Generation   │
                    │  • SSO Authentication     │
                    │  • Role & Permission      │
                    │  • Audit Logging          │
                    └───────────────────────────┘
```

## 🚀 نصب و راه‌اندازی

### پیش‌نیازها
- Python 3.9+
- pip
- Git

### روش 1: نصب خودکار (توصیه شده)

```bash
# کلون کردن پروژه
git clone <repository-url>
cd auth_service

# اجرای اسکریپت نصب خودکار
./setup.sh
```

### روش 2: نصب دستی

```bash
# 1. ایجاد محیط مجازی
python -m venv venv

# 2. فعال‌سازی محیط مجازی
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. نصب وابستگی‌ها
pip install -r requirements.txt

# 4. کپی کردن فایل محیط
cp env.example .env

# 5. ویرایش فایل .env با تنظیمات خود

# 6. ایجاد دایرکتوری‌های لازم
mkdir -p logs media/avatars staticfiles keys

# 7. تولید کلیدهای RSA
python scripts/generate_rsa_keys.py

# 8. اجرای مایگریشن‌ها
python manage.py makemigrations
python manage.py migrate

# 9. ایجاد superuser
python scripts/create_superuser.py

# 10. ایجاد کلاینت‌های SSO
python scripts/create_sso_clients.py

# 11. جمع‌آوری فایل‌های استاتیک
python manage.py collectstatic --noinput

# 12. اجرای سرور
python manage.py runserver
```

## ⚙️ پیکربندی

### فایل .env

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,auth.avinoo.ir

# Microservice Configuration
AUTH_SERVICE_DOMAIN=auth.avinoo.ir
ALLOWED_CLIENT_DOMAINS=app1.avinoo.ir,app2.avinoo.ir

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=7
JWT_PRIVATE_KEY_PATH=keys/private_key.pem
JWT_PUBLIC_KEY_PATH=keys/public_key.pem

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://app1.avinoo.ir,http://app2.avinoo.ir

# Logging
LOG_LEVEL=INFO
```

## 📚 API Endpoints

### 🔐 احراز هویت SSO

#### ثبت‌نام
```bash
POST /api/register/
Content-Type: application/json

{
    "username": "testuser",
    "email": "test@example.com",
    "phone_number": "+989123456789",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "first_name": "Test",
    "last_name": "User",
    "client_id": "app1_client",
    "redirect_uri": "https://app1.avinoo.ir/callback"
}
```

#### ورود
```bash
POST /api/login/
Content-Type: application/json

{
    "username": "testuser",
    "password": "securepassword123",
    "client_id": "app1_client",
    "redirect_uri": "https://app1.avinoo.ir/callback"
}
```

#### اعتبارسنجی توکن
```bash
POST /api/validate-token/
Content-Type: application/json

{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...",
    "client_id": "app1_client"
}
```

#### دریافت اطلاعات کاربر
```bash
GET /api/user-info/
Authorization: Bearer <access_token>
```

#### خروج
```bash
POST /api/logout/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "client_id": "app1_client",
    "redirect_uri": "https://app1.avinoo.ir"
}
```

### 🌐 صفحات وب SSO

#### صفحه ورود
```
GET /login/?client_id=app1_client&redirect_uri=https://app1.avinoo.ir/callback&state=random_state
```

#### صفحه ثبت‌نام
```
GET /register/?client_id=app1_client&redirect_uri=https://app1.avinoo.ir/callback&state=random_state
```

#### صفحه بازگشت
```
GET /callback/?token=JWT_TOKEN&state=random_state&client_id=app1_client
```

## 🔄 جریان SSO

### 1. ورود کاربر به اپلیکیشن کلاینت
```
کاربر → app1.avinoo.ir → بررسی توکن → اگر توکن نداشت → ریدایرکت به auth.avinoo.ir
```

### 2. احراز هویت در سرویس مرکزی
```
auth.avinoo.ir/login?client_id=app1_client&redirect_uri=https://app1.avinoo.ir/callback
```

### 3. ورود موفق و تولید JWT
```
کاربر وارد می‌شود → JWT تولید می‌شود → ریدایرکت به کلاینت با توکن
```

### 4. بازگشت به اپلیکیشن کلاینت
```
app1.avinoo.ir/callback?token=JWT_TOKEN → ذخیره توکن → ورود به اپلیکیشن
```

## 🧪 تست سیستم

### تست API ها
```bash
# اجرای تست‌های API
python scripts/test_sso_api.py
```

### تست رابط کاربری
1. **Auth Service**: http://127.0.0.1:8000
2. **App1**: http://127.0.0.1:8000/client_apps/app1/index.html
3. **App2**: http://127.0.0.1:8000/client_apps/app2/index.html

### تست با cURL

#### ثبت‌نام
```bash
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpassword123",
    "password_confirm": "testpassword123",
    "first_name": "Test",
    "last_name": "User",
    "client_id": "app1_client",
    "redirect_uri": "https://app1.avinoo.ir/callback"
  }'
```

#### ورود
```bash
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpassword123",
    "client_id": "app1_client",
    "redirect_uri": "https://app1.avinoo.ir/callback"
  }'
```

#### اعتبارسنجی توکن
```bash
curl -X POST http://127.0.0.1:8000/api/validate-token/ \
  -H "Content-Type: application/json" \
  -d '{
    "token": "YOUR_JWT_TOKEN",
    "client_id": "app1_client"
  }'
```

## 🔧 توسعه

### ساختار پروژه
```
auth_service/
├── apps/                    # اپلیکیشن‌های داخلی
│   ├── users/              # مدیریت کاربران
│   ├── roles/              # مدیریت نقش‌ها
│   └── permissions/        # مدیریت مجوزها
├── sso/                    # اپلیکیشن SSO
│   ├── models.py           # مدل‌های SSO
│   ├── views.py            # ویوهای SSO
│   ├── serializers.py      # سریالایزرهای SSO
│   ├── urls.py             # URL های SSO
│   └── utils.py            # توابع کمکی
├── client_apps/            # اپلیکیشن‌های کلاینت نمونه
│   ├── app1/               # اپلیکیشن اول
│   └── app2/               # اپلیکیشن دوم
├── auth_service/           # تنظیمات اصلی پروژه
├── templates/              # قالب‌های HTML
├── keys/                   # کلیدهای RSA
├── scripts/                # اسکریپت‌ها
├── logs/                   # فایل‌های لاگ
├── media/                  # فایل‌های رسانه
├── staticfiles/            # فایل‌های استاتیک
├── requirements.txt        # وابستگی‌های اصلی
├── env.example            # نمونه فایل محیط
└── README.md              # این فایل
```

### اضافه کردن کلاینت جدید

#### 1. ایجاد کلاینت در دیتابیس
```python
from sso.models import SSOClient

client = SSOClient.objects.create(
    name='New App',
    domain='newapp.avinoo.ir',
    client_id='newapp_client',
    client_secret='your_secret_here',
    redirect_uri='https://newapp.avinoo.ir/callback',
    is_active=True
)
```

#### 2. به‌روزرسانی تنظیمات CORS
```env
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://app1.avinoo.ir,http://app2.avinoo.ir,http://newapp.avinoo.ir
```

#### 3. پیاده‌سازی در اپلیکیشن کلاینت
```javascript
const APP_CONFIG = {
    name: 'New App',
    domain: 'newapp.avinoo.ir',
    clientId: 'newapp_client',
    authServiceUrl: 'https://auth.avinoo.ir',
    redirectUri: window.location.origin + '/callback'
};
```

## 📊 مانیتورینگ و لاگ‌ها

### فایل‌های لاگ
- `logs/django.log` - لاگ‌های اصلی Django
- لاگ‌های حسابرسی SSO در دیتابیس

### سطح‌های لاگ
- DEBUG: جزئیات کامل
- INFO: اطلاعات عمومی
- WARNING: هشدارها
- ERROR: خطاها
- CRITICAL: خطاهای بحرانی

### مانیتورینگ SSO
```bash
# مشاهده لاگ‌های SSO
python manage.py shell
>>> from sso.models import SSOAuditLog
>>> logs = SSOAuditLog.objects.all()[:10]
>>> for log in logs:
...     print(f"{log.action}: {log.user} -> {log.client} at {log.created_at}")
```

## 🚀 استقرار در Production

### تنظیمات Production
```env
DEBUG=False
ALLOWED_HOSTS=auth.avinoo.ir,www.auth.avinoo.ir
SECRET_KEY=your-production-secret-key
AUTH_SERVICE_DOMAIN=auth.avinoo.ir
CORS_ALLOWED_ORIGINS=https://app1.avinoo.ir,https://app2.avinoo.ir
```

### اجرا با Gunicorn
```bash
gunicorn auth_service.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### استفاده از Nginx
```nginx
server {
    listen 80;
    server_name auth.avinoo.ir;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static/ {
        alias /path/to/staticfiles/;
    }
    
    location /media/ {
        alias /path/to/media/;
    }
}
```

### SSL/HTTPS
```bash
# نصب SSL با Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d auth.avinoo.ir
```

## 🔒 امنیت

### بهترین روش‌ها
- استفاده از HTTPS در Production
- تغییر SECRET_KEY و کلیدهای RSA
- محدود کردن ALLOWED_HOSTS
- استفاده از فایروال مناسب
- پشتیبان‌گیری منظم از دیتابیس
- نظارت بر لاگ‌های امنیتی

### Rate Limiting
- 5 درخواست در دقیقه برای ثبت‌نام
- 10 درخواست در دقیقه برای ورود
- 100 درخواست در ساعت برای کاربران ناشناس
- 1000 درخواست در ساعت برای کاربران احراز هویت شده

### کلیدهای RSA
```bash
# تولید کلیدهای جدید
python scripts/generate_rsa_keys.py

# بررسی کلیدها
openssl rsa -in keys/private_key.pem -text -noout
openssl rsa -in keys/public_key.pem -pubin -text -noout
```

## 🐛 عیب‌یابی

### مشکلات رایج

#### 1. خطای CORS
```
Access to fetch at 'http://127.0.0.1:8000/api/login/' from origin 'http://localhost:3000' has been blocked by CORS policy
```
**راه حل**: اضافه کردن دامنه به `CORS_ALLOWED_ORIGINS`

#### 2. خطای JWT
```
Token is invalid or expired
```
**راه حل**: بررسی انقضای توکن و کلیدهای RSA

#### 3. خطای کلاینت
```
Client not found or inactive
```
**راه حل**: بررسی وجود و فعال بودن کلاینت در دیتابیس

### لاگ‌های مفید
```bash
# مشاهده لاگ‌های Django
tail -f logs/django.log

# مشاهده لاگ‌های SSO
python manage.py shell
>>> from sso.models import SSOAuditLog
>>> SSOAuditLog.objects.filter(action='error').order_by('-created_at')[:5]
```

## 📝 مجوزها

این پروژه تحت مجوز MIT منتشر شده است.

## 🤝 مشارکت

برای مشارکت در پروژه:
1. Fork کنید
2. Branch جدید ایجاد کنید
3. تغییرات خود را commit کنید
4. Pull Request ارسال کنید

## 📞 پشتیبانی

برای پشتیبانی و سوالات:
- ایمیل: support@avinoo.ir
- GitHub Issues: [لینک Issues]

## 🎯 مثال کامل استفاده

### 1. راه‌اندازی اولیه
```bash
# نصب و راه‌اندازی
git clone <repository-url>
cd auth_service
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python scripts/generate_rsa_keys.py
python manage.py migrate
python scripts/create_superuser.py
python scripts/create_sso_clients.py
python manage.py runserver
```

### 2. تست سیستم
```bash
# تست API
python scripts/test_sso_api.py

# باز کردن مرورگر
# http://127.0.0.1:8000/client_apps/app1/index.html
```

### 3. استفاده در اپلیکیشن کلاینت
```javascript
// تنظیمات کلاینت
const APP_CONFIG = {
    name: 'My App',
    domain: 'myapp.avinoo.ir',
    clientId: 'myapp_client',
    authServiceUrl: 'https://auth.avinoo.ir',
    redirectUri: window.location.origin + '/callback'
};

// بررسی احراز هویت
function checkAuth() {
    const token = localStorage.getItem('auth_token');
    if (token) {
        validateToken(token);
    } else {
        redirectToLogin();
    }
}

// ریدایرکت به صفحه ورود
function redirectToLogin() {
    const loginUrl = `${APP_CONFIG.authServiceUrl}/login/?client_id=${APP_CONFIG.clientId}&redirect_uri=${encodeURIComponent(APP_CONFIG.redirectUri)}`;
    window.location.href = loginUrl;
}
```

---

**نکته مهم**: این سرویس برای استفاده در محیط Production طراحی شده و شامل تمام ویژگی‌های امنیتی و مدیریتی مورد نیاز برای یک سیستم احراز هویت میکروسرویسی می‌باشد.

**آخرین به‌روزرسانی**: 2024
**نسخه**: 1.0.0
**توسعه‌دهنده**: تیم Avinoo.ir