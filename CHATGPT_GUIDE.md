# 🤖 راهنمای ChatGPT - سیستم احراز هویت مرکزی

## 📋 خلاصه سیستم

این یک **سرویس احراز هویت مرکزی** است که با Django + JWT + RSA کار می‌کند و از **Single Sign-On (SSO)** پشتیبانی می‌کند.

### 🎯 هدف سیستم
- **یک بار ورود** در تمام اپ‌ها
- **مدیریت مرکزی کاربران**
- **امنیت بالا** با JWT + RSA
- **API کامل** برای اپ‌های مختلف

## 🏗️ معماری ساده

```
کاربر → اپ شما → سرویس احراز هویت → JWT Token → بازگشت به اپ
```

## 🔑 API های اصلی

### 1. ورود کاربر
```http
POST /api/login/
{
    "username": "نام کاربری",
    "password": "رمز عبور",
    "client_id": "شناسه اپ شما",
    "redirect_uri": "آدرس بازگشت"
}
```

### 2. ثبت‌نام کاربر
```http
POST /api/register/
{
    "username": "نام کاربری",
    "email": "ایمیل",
    "password": "رمز عبور",
    "password_confirm": "تکرار رمز",
    "first_name": "نام",
    "last_name": "نام خانوادگی",
    "client_id": "شناسه اپ شما",
    "redirect_uri": "آدرس بازگشت"
}
```

### 3. اعتبارسنجی توکن
```http
POST /api/validate-token/
{
    "token": "JWT_TOKEN",
    "client_id": "شناسه اپ شما"
}
```

### 4. دریافت اطلاعات کاربر
```http
GET /api/user-info/
Authorization: Bearer JWT_TOKEN
```

**پاسخ شامل GUID:**
```json
{
    "id": 1,
    "guid": "550e8400-e29b-41d4-a716-446655440000",
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User"
}
```

### 5. خروج از سیستم
```http
POST /api/logout/
Authorization: Bearer JWT_TOKEN
{
    "client_id": "شناسه اپ شما",
    "redirect_uri": "آدرس بازگشت"
}
```

## 🌐 صفحات وب SSO

### صفحه ورود
```
GET /login/?client_id=شناسه_اپ&redirect_uri=آدرس_بازگشت
```

### صفحه ثبت‌نام
```
GET /register/?client_id=شناسه_اپ&redirect_uri=آدرس_بازگشت
```

### صفحه بازگشت (Callback)
```
GET /callback/?token=JWT_TOKEN&state=random_state
```

## 🔄 جریان کار ساده

### 1. کاربر وارد اپ می‌شود
- اپ بررسی می‌کند که توکن دارد یا نه
- اگر توکن نداشت → ریدایرکت به سرویس احراز هویت

### 2. ورود در سرویس احراز هویت
- کاربر نام کاربری و رمز وارد می‌کند
- سیستم JWT Token تولید می‌کند
- کاربر به اپ بازگردانده می‌شود

### 3. بازگشت به اپ
- اپ توکن را دریافت و ذخیره می‌کند
- از این به بعد با توکن کار می‌کند

## 💻 کد نمونه برای اپ شما

### JavaScript ساده
```javascript
// تنظیمات
const AUTH_CONFIG = {
    authServiceUrl: 'https://auth.avinoo.ir',
    clientId: 'your_app_client',
    redirectUri: window.location.origin + '/callback'
};

// بررسی احراز هویت
function checkAuth() {
    const token = localStorage.getItem('auth_token');
    if (!token) {
        redirectToLogin();
    } else {
        validateToken(token);
    }
}

// ریدایرکت به ورود
function redirectToLogin() {
    const loginUrl = `${AUTH_CONFIG.authServiceUrl}/login/?` +
        `client_id=${AUTH_CONFIG.clientId}&` +
        `redirect_uri=${encodeURIComponent(AUTH_CONFIG.redirectUri)}`;
    window.location.href = loginUrl;
}

// اعتبارسنجی توکن
async function validateToken(token) {
    const response = await fetch(`${AUTH_CONFIG.authServiceUrl}/api/validate-token/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            token: token,
            client_id: AUTH_CONFIG.clientId
        })
    });
    
    const data = await response.json();
    if (!data.valid) {
        redirectToLogin();
    }
}
```

## 🛠️ تنظیمات اولیه

### 1. ایجاد کلاینت در سیستم
```python
# در پنل ادمین یا با کد
from sso.models import SSOClient

SSOClient.objects.create(
    name='نام اپ شما',
    domain='your-app.com',
    client_id='your_app_client',
    client_secret='رمز_محرمانه',
    redirect_uri='https://your-app.com/callback',
    is_active=True
)
```

### 2. تنظیم CORS
```env
CORS_ALLOWED_ORIGINS=https://your-app.com
```

## 📱 مثال کامل HTML

```html
<!DOCTYPE html>
<html>
<head>
    <title>اپ شما</title>
</head>
<body>
    <div id="app">
        <div id="login-section">
            <h2>برای استفاده وارد شوید</h2>
            <button onclick="login()">ورود</button>
        </div>
        
        <div id="user-section" style="display:none">
            <h2>خوش آمدید!</h2>
            <div id="user-info"></div>
            <button onclick="logout()">خروج</button>
        </div>
    </div>

    <script>
        const AUTH_CONFIG = {
            authServiceUrl: 'https://auth.avinoo.ir',
            clientId: 'your_app_client',
            redirectUri: window.location.origin + '/callback'
        };

        // بررسی احراز هویت
        window.onload = function() {
            const token = localStorage.getItem('auth_token');
            if (token) {
                showUserSection();
            } else {
                showLoginSection();
            }
        };

        function login() {
            const loginUrl = `${AUTH_CONFIG.authServiceUrl}/login/?` +
                `client_id=${AUTH_CONFIG.clientId}&` +
                `redirect_uri=${encodeURIComponent(AUTH_CONFIG.redirectUri)}`;
            window.location.href = loginUrl;
        }

        function logout() {
            localStorage.removeItem('auth_token');
            showLoginSection();
        }

        function showLoginSection() {
            document.getElementById('login-section').style.display = 'block';
            document.getElementById('user-section').style.display = 'none';
        }

        function showUserSection() {
            document.getElementById('login-section').style.display = 'none';
            document.getElementById('user-section').style.display = 'block';
        }
    </script>
</body>
</html>
```

## 🔧 نصب و راه‌اندازی

### مراحل نصب
```bash
# 1. نصب وابستگی‌ها
pip install -r requirements.txt

# 2. تولید کلیدهای RSA
python scripts/generate_rsa_keys.py

# 3. اجرای مایگریشن‌ها
python manage.py migrate

# 4. ایجاد superuser
python scripts/create_superuser.py

# 5. ایجاد کلاینت‌های SSO
python scripts/create_sso_clients.py

# 6. اجرای سرور
python manage.py runserver
```

## 🧪 تست سریع

### تست API
```bash
# تست ورود
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123",
    "client_id": "app1_client",
    "redirect_uri": "https://app1.avinoo.ir/callback"
  }'
```

### تست صفحات
- **صفحه اصلی**: http://127.0.0.1:8000
- **پنل ادمین**: http://127.0.0.1:8000/admin
- **اپ نمونه 1**: http://127.0.0.1:8000/client_apps/app1/index.html

## 🚨 نکات مهم

### امنیت
- همیشه از HTTPS استفاده کنید
- Client Secret را محرمانه نگه دارید
- توکن‌ها را در localStorage ذخیره کنید

### عیب‌یابی
- **خطای CORS**: دامنه را به CORS_ALLOWED_ORIGINS اضافه کنید
- **خطای Client**: کلاینت را در پنل ادمین بررسی کنید
- **خطای Token**: توکن را دوباره دریافت کنید

## 📞 پشتیبانی

- **مستندات کامل**: [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)
- **API کامل**: [docs/API.md](docs/API.md)
- **ایمیل**: support@avinoo.ir

---

**خلاصه**: این سیستم یک سرویس احراز هویت مرکزی است که با JWT + SSO کار می‌کند. اپ‌های شما فقط نیاز دارند که کاربران را به این سرویس ریدایرکت کنند و JWT Token دریافت کنند.
