# 🔗 راهنمای اتصال اپ‌های دیگر به سیستم احراز هویت

## 📋 خلاصه سیستم

این سیستم یک **سرویس احراز هویت مرکزی** است که با استفاده از **JWT + RSA** و **Single Sign-On (SSO)** کار می‌کند.

### 🏗️ معماری کلی
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   اپ شما        │    │   اپ دیگری      │    │  پنل ادمین      │
│                 │    │                 │    │                 │
│  your-app.com   │    │  other-app.com  │    │  admin.com      │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │                           │
                    │    auth.avinoo.ir         │
                    │                           │
                    │   سرویس احراز هویت        │
                    │                           │
                    │  • ورود/ثبت‌نام           │
                    │  • تولید JWT Token        │
                    │  • اعتبارسنجی توکن        │
                    │  • مدیریت کاربران         │
                    └───────────────────────────┘
```

## 🚀 مراحل اتصال اپ شما

### مرحله 1: دریافت اطلاعات کلاینت

ابتدا باید یک **کلاینت** در سیستم ثبت کنید:

```bash
# اجرای اسکریپت ایجاد کلاینت
python scripts/create_sso_clients.py
```

یا از طریق پنل ادمین:
1. برو به `http://auth.avinoo.ir/admin/`
2. بخش `SSO Clients` را باز کن
3. `Add SSO Client` را کلیک کن
4. اطلاعات زیر را پر کن:

```
Name: نام اپ شما
Domain: your-app.com
Client ID: your_app_client
Client Secret: یک رمز قوی
Redirect URI: https://your-app.com/callback
Is Active: ✅
```

### مرحله 2: تنظیم CORS

در فایل `.env` سرویس احراز هویت، دامنه اپ خود را اضافه کن:

```env
CORS_ALLOWED_ORIGINS=https://your-app.com,https://www.your-app.com
```

### مرحله 3: پیاده‌سازی در اپ شما

#### 3.1 تنظیمات اولیه

```javascript
// config.js
const AUTH_CONFIG = {
    // آدرس سرویس احراز هویت
    authServiceUrl: 'https://auth.avinoo.ir',
    
    // اطلاعات کلاینت شما
    clientId: 'your_app_client',
    
    // آدرس بازگشت بعد از ورود
    redirectUri: window.location.origin + '/callback',
    
    // نام اپ شما
    appName: 'نام اپ شما'
};
```

#### 3.2 بررسی احراز هویت

```javascript
// auth.js
class AuthService {
    constructor() {
        this.config = AUTH_CONFIG;
        this.token = localStorage.getItem('auth_token');
    }

    // بررسی اینکه کاربر وارد شده یا نه
    isAuthenticated() {
        return !!this.token;
    }

    // ریدایرکت به صفحه ورود
    redirectToLogin() {
        const loginUrl = `${this.config.authServiceUrl}/login/?` +
            `client_id=${this.config.clientId}&` +
            `redirect_uri=${encodeURIComponent(this.config.redirectUri)}&` +
            `state=${this.generateState()}`;
        
        window.location.href = loginUrl;
    }

    // تولید state برای امنیت
    generateState() {
        return Math.random().toString(36).substring(2, 15);
    }

    // اعتبارسنجی توکن
    async validateToken() {
        if (!this.token) return false;

        try {
            const response = await fetch(`${this.config.authServiceUrl}/api/validate-token/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    token: this.token,
                    client_id: this.config.clientId
                })
            });

            const data = await response.json();
            return data.valid;
        } catch (error) {
            console.error('خطا در اعتبارسنجی توکن:', error);
            return false;
        }
    }

    // دریافت اطلاعات کاربر
    async getUserInfo() {
        if (!this.token) return null;

        try {
            const response = await fetch(`${this.config.authServiceUrl}/api/user-info/`, {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            return await response.json();
        } catch (error) {
            console.error('خطا در دریافت اطلاعات کاربر:', error);
            return null;
        }
    }

    // خروج از سیستم
    async logout() {
        try {
            await fetch(`${this.config.authServiceUrl}/api/logout/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    client_id: this.config.clientId,
                    redirect_uri: window.location.origin
                })
            });
        } catch (error) {
            console.error('خطا در خروج:', error);
        } finally {
            localStorage.removeItem('auth_token');
            this.token = null;
            window.location.href = '/';
        }
    }
}
```

#### 3.3 صفحه اصلی اپ

```html
<!-- index.html -->
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>اپ شما</title>
    <style>
        body { font-family: 'Tahoma', sans-serif; margin: 0; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        .header { background: #007bff; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .user-info { background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .btn { background: #dc3545; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        .btn:hover { background: #c82333; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏠 اپ شما</h1>
            <p>خوش آمدید به اپلیکیشن ما</p>
        </div>

        <div id="user-info" class="user-info" style="display: none;">
            <h3>👤 اطلاعات کاربر</h3>
            <div id="user-details"></div>
            <button class="btn" onclick="authService.logout()">🚪 خروج</button>
        </div>

        <div id="login-prompt" style="text-align: center; padding: 40px;">
            <h3>🔐 برای استفاده از اپ، ابتدا وارد شوید</h3>
            <button class="btn" onclick="authService.redirectToLogin()" style="background: #28a745;">
                🔑 ورود / ثبت‌نام
            </button>
        </div>
    </div>

    <script src="config.js"></script>
    <script src="auth.js"></script>
    <script>
        const authService = new AuthService();

        // بررسی احراز هویت هنگام بارگذاری صفحه
        window.addEventListener('load', async () => {
            if (authService.isAuthenticated()) {
                const isValid = await authService.validateToken();
                if (isValid) {
                    showUserInfo();
                } else {
                    authService.redirectToLogin();
                }
            } else {
                showLoginPrompt();
            }
        });

        async function showUserInfo() {
            const userInfo = await authService.getUserInfo();
            if (userInfo) {
                document.getElementById('user-details').innerHTML = `
                    <p><strong>نام کاربری:</strong> ${userInfo.username}</p>
                    <p><strong>ایمیل:</strong> ${userInfo.email}</p>
                    <p><strong>نام:</strong> ${userInfo.first_name} ${userInfo.last_name}</p>
                    <p><strong>شماره تلفن:</strong> ${userInfo.phone_number || 'ثبت نشده'}</p>
                `;
                document.getElementById('user-info').style.display = 'block';
                document.getElementById('login-prompt').style.display = 'none';
            }
        }

        function showLoginPrompt() {
            document.getElementById('user-info').style.display = 'none';
            document.getElementById('login-prompt').style.display = 'block';
        }
    </script>
</body>
</html>
```

#### 3.4 صفحه بازگشت (Callback)

```html
<!-- callback.html -->
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>در حال ورود...</title>
    <style>
        body { font-family: 'Tahoma', sans-serif; text-align: center; padding: 50px; }
        .loading { color: #007bff; }
        .error { color: #dc3545; }
        .success { color: #28a745; }
    </style>
</head>
<body>
    <div id="status" class="loading">
        <h2>⏳ در حال ورود...</h2>
        <p>لطفاً صبر کنید...</p>
    </div>

    <script src="config.js"></script>
    <script>
        // دریافت پارامترهای URL
        const urlParams = new URLSearchParams(window.location.search);
        const token = urlParams.get('token');
        const state = urlParams.get('state');
        const error = urlParams.get('error');

        if (error) {
            // خطا در ورود
            document.getElementById('status').innerHTML = `
                <h2 class="error">❌ خطا در ورود</h2>
                <p>${error}</p>
                <button onclick="window.location.href='/'">بازگشت به صفحه اصلی</button>
            `;
        } else if (token) {
            // ذخیره توکن و بازگشت به صفحه اصلی
            localStorage.setItem('auth_token', token);
            document.getElementById('status').innerHTML = `
                <h2 class="success">✅ ورود موفق</h2>
                <p>در حال انتقال به صفحه اصلی...</p>
            `;
            
            // انتقال به صفحه اصلی بعد از 2 ثانیه
            setTimeout(() => {
                window.location.href = '/';
            }, 2000);
        } else {
            // پارامترهای لازم موجود نیست
            document.getElementById('status').innerHTML = `
                <h2 class="error">❌ خطا</h2>
                <p>پارامترهای لازم موجود نیست</p>
                <button onclick="window.location.href='/'">بازگشت به صفحه اصلی</button>
            `;
        }
    </script>
</body>
</html>
```

## 🔧 تنظیمات پیشرفته

### استفاده در React

```jsx
// AuthContext.jsx
import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within AuthProvider');
    }
    return context;
};

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    const AUTH_CONFIG = {
        authServiceUrl: 'https://auth.avinoo.ir',
        clientId: 'your_app_client',
        redirectUri: window.location.origin + '/callback'
    };

    useEffect(() => {
        checkAuth();
    }, []);

    const checkAuth = async () => {
        const token = localStorage.getItem('auth_token');
        if (token) {
            try {
                const response = await fetch(`${AUTH_CONFIG.authServiceUrl}/api/validate-token/`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        token,
                        client_id: AUTH_CONFIG.clientId
                    })
                });

                const data = await response.json();
                if (data.valid) {
                    const userInfo = await getUserInfo();
                    setUser(userInfo);
                    setIsAuthenticated(true);
                } else {
                    localStorage.removeItem('auth_token');
                }
            } catch (error) {
                console.error('خطا در بررسی احراز هویت:', error);
                localStorage.removeItem('auth_token');
            }
        }
        setLoading(false);
    };

    const getUserInfo = async () => {
        const token = localStorage.getItem('auth_token');
        const response = await fetch(`${AUTH_CONFIG.authServiceUrl}/api/user-info/`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        return await response.json();
    };

    const login = () => {
        const loginUrl = `${AUTH_CONFIG.authServiceUrl}/login/?` +
            `client_id=${AUTH_CONFIG.clientId}&` +
            `redirect_uri=${encodeURIComponent(AUTH_CONFIG.redirectUri)}`;
        window.location.href = loginUrl;
    };

    const logout = async () => {
        const token = localStorage.getItem('auth_token');
        try {
            await fetch(`${AUTH_CONFIG.authServiceUrl}/api/logout/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    client_id: AUTH_CONFIG.clientId,
                    redirect_uri: window.location.origin
                })
            });
        } catch (error) {
            console.error('خطا در خروج:', error);
        } finally {
            localStorage.removeItem('auth_token');
            setUser(null);
            setIsAuthenticated(false);
        }
    };

    const value = {
        user,
        isAuthenticated,
        loading,
        login,
        logout
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};
```

### استفاده در Vue.js

```vue
<!-- AuthMixin.vue -->
<template>
  <div>
    <div v-if="loading">در حال بارگذاری...</div>
    <div v-else-if="!isAuthenticated">
      <h3>برای استفاده از اپ، ابتدا وارد شوید</h3>
      <button @click="login">ورود / ثبت‌نام</button>
    </div>
    <div v-else>
      <h3>خوش آمدید {{ user.first_name }}!</h3>
      <button @click="logout">خروج</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      user: null,
      isAuthenticated: false,
      loading: true,
      AUTH_CONFIG: {
        authServiceUrl: 'https://auth.avinoo.ir',
        clientId: 'your_app_client',
        redirectUri: window.location.origin + '/callback'
      }
    };
  },
  async mounted() {
    await this.checkAuth();
  },
  methods: {
    async checkAuth() {
      const token = localStorage.getItem('auth_token');
      if (token) {
        try {
          const response = await fetch(`${this.AUTH_CONFIG.authServiceUrl}/api/validate-token/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              token,
              client_id: this.AUTH_CONFIG.clientId
            })
          });

          const data = await response.json();
          if (data.valid) {
            await this.getUserInfo();
            this.isAuthenticated = true;
          } else {
            localStorage.removeItem('auth_token');
          }
        } catch (error) {
          console.error('خطا در بررسی احراز هویت:', error);
          localStorage.removeItem('auth_token');
        }
      }
      this.loading = false;
    },

    async getUserInfo() {
      const token = localStorage.getItem('auth_token');
      const response = await fetch(`${this.AUTH_CONFIG.authServiceUrl}/api/user-info/`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      this.user = await response.json();
    },

    login() {
      const loginUrl = `${this.AUTH_CONFIG.authServiceUrl}/login/?` +
        `client_id=${this.AUTH_CONFIG.clientId}&` +
        `redirect_uri=${encodeURIComponent(this.AUTH_CONFIG.redirectUri)}`;
      window.location.href = loginUrl;
    },

    async logout() {
      const token = localStorage.getItem('auth_token');
      try {
        await fetch(`${this.AUTH_CONFIG.authServiceUrl}/api/logout/`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            client_id: this.AUTH_CONFIG.clientId,
            redirect_uri: window.location.origin
          })
        });
      } catch (error) {
        console.error('خطا در خروج:', error);
      } finally {
        localStorage.removeItem('auth_token');
        this.user = null;
        this.isAuthenticated = false;
      }
    }
  }
};
</script>
```

## 📡 API Endpoints

### 1. ورود
```http
POST /api/login/
Content-Type: application/json

{
    "username": "نام کاربری",
    "password": "رمز عبور",
    "client_id": "your_app_client",
    "redirect_uri": "https://your-app.com/callback"
}
```

### 2. ثبت‌نام
```http
POST /api/register/
Content-Type: application/json

{
    "username": "نام کاربری",
    "email": "email@example.com",
    "phone_number": "+989123456789",
    "password": "رمز عبور",
    "password_confirm": "تکرار رمز عبور",
    "first_name": "نام",
    "last_name": "نام خانوادگی",
    "client_id": "your_app_client",
    "redirect_uri": "https://your-app.com/callback"
}
```

### 3. اعتبارسنجی توکن
```http
POST /api/validate-token/
Content-Type: application/json

{
    "token": "JWT_TOKEN",
    "client_id": "your_app_client"
}
```

### 4. دریافت اطلاعات کاربر
```http
GET /api/user-info/
Authorization: Bearer JWT_TOKEN
```

### 5. خروج
```http
POST /api/logout/
Authorization: Bearer JWT_TOKEN
Content-Type: application/json

{
    "client_id": "your_app_client",
    "redirect_uri": "https://your-app.com"
}
```

## 🔒 امنیت

### نکات مهم امنیتی:

1. **همیشه از HTTPS استفاده کنید** در Production
2. **Client Secret را محرمانه نگه دارید**
3. **توکن‌ها را در localStorage ذخیره کنید** (نه در cookie)
4. **State parameter را برای CSRF protection استفاده کنید**
5. **توکن‌ها را منظم اعتبارسنجی کنید**

### مثال اعتبارسنجی منظم:

```javascript
// هر 5 دقیقه یکبار توکن را بررسی کن
setInterval(async () => {
    if (authService.isAuthenticated()) {
        const isValid = await authService.validateToken();
        if (!isValid) {
            authService.logout();
        }
    }
}, 5 * 60 * 1000);
```

## 🧪 تست

### تست با cURL:

```bash
# تست ورود
curl -X POST https://auth.avinoo.ir/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123",
    "client_id": "your_app_client",
    "redirect_uri": "https://your-app.com/callback"
  }'

# تست اعتبارسنجی
curl -X POST https://auth.avinoo.ir/api/validate-token/ \
  -H "Content-Type: application/json" \
  -d '{
    "token": "YOUR_JWT_TOKEN",
    "client_id": "your_app_client"
  }'
```

## 🆘 عیب‌یابی

### مشکلات رایج:

#### 1. خطای CORS
```
Access to fetch at 'https://auth.avinoo.ir/api/login/' from origin 'https://your-app.com' has been blocked by CORS policy
```
**راه حل**: دامنه اپ خود را به `CORS_ALLOWED_ORIGINS` اضافه کنید

#### 2. خطای Client Not Found
```
Client not found or inactive
```
**راه حل**: کلاینت خود را در پنل ادمین بررسی کنید

#### 3. خطای Invalid Token
```
Token is invalid or expired
```
**راه حل**: توکن را دوباره دریافت کنید

## 📞 پشتیبانی

برای سوالات و مشکلات:
- ایمیل: support@avinoo.ir
- مستندات کامل: [لینک مستندات]

---

**نکته**: این راهنما برای اتصال سریع و آسان اپ‌های شما به سیستم احراز هویت طراحی شده است. برای تنظیمات پیشرفته‌تر، به مستندات کامل مراجعه کنید.
