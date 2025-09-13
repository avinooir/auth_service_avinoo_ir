# 🔗 راهنمای کامل اتصال اپلیکیشن‌ها به سیستم SSO

## 📋 فهرست مطالب

1. [مقدمه](#مقدمه)
2. [نحوه کارکرد SSO](#نحوه-کارکرد-sso)
3. [مراحل اتصال](#مراحل-اتصال)
4. [API های موجود](#api-های-موجود)
5. [نمونه‌های عملی](#نمونه‌های-عملی)
6. [مدیریت کلاینت‌ها](#مدیریت-کلاینت‌ها)
7. [امنیت](#امنیت)
8. [عیب‌یابی](#عیب‌یابی)

## 🎯 مقدمه

سیستم SSO شما امکان احراز هویت یکپارچه برای چندین اپلیکیشن را فراهم می‌کند. کاربران فقط یک بار وارد می‌شوند و به تمام اپلیکیشن‌های متصل دسترسی دارند.

### مزایای استفاده از SSO:
- **تجربه کاربری بهتر**: یک بار ورود برای همه اپلیکیشن‌ها
- **امنیت بالاتر**: مدیریت متمرکز احراز هویت
- **مدیریت آسان‌تر**: کنترل دسترسی‌ها از یک مکان
- **کاهش پیچیدگی**: نیازی به پیاده‌سازی سیستم احراز هویت در هر اپلیکیشن

## 🔄 نحوه کارکرد SSO

### فرآیند کلی:
1. **کاربر به اپلیکیشن مراجعه می‌کند**
2. **اپلیکیشن کاربر را به SSO هدایت می‌کند**
3. **کاربر در SSO وارد می‌شود**
4. **SSO توکن JWT تولید می‌کند**
5. **کاربر با توکن به اپلیکیشن بازمی‌گردد**
6. **اپلیکیشن توکن را اعتبارسنجی می‌کند**
7. **اطلاعات کاربر از SSO دریافت می‌شود**

## 🚀 مراحل اتصال

### مرحله 1: ثبت کلاینت در SSO

ابتدا باید اپلیکیشن خود را در سیستم SSO ثبت کنید:

#### روش 1: از طریق Django Admin
```bash
# دسترسی به پنل مدیریت
http://127.0.0.1:8000/admin/sso/ssoclient/
```

#### روش 2: از طریق اسکریپت مدیریت
```bash
python scripts/manage_sso_clients.py
```

#### روش 3: از طریق API (برای توسعه‌دهندگان)
```python
import requests

# ایجاد کلاینت جدید
response = requests.post('http://127.0.0.1:8000/sso/api/admin/clients/', {
    'name': 'My Application',
    'domain': 'myapp.example.com',
    'client_id': 'myapp_client',
    'client_secret': 'myapp_secret_2024',
    'redirect_uri': 'https://myapp.example.com/callback',
    'allow_any_path': True,  # برای انعطاف بیشتر
    'is_active': True
}, headers={'Authorization': 'Bearer YOUR_ADMIN_TOKEN'})
```

### مرحله 2: تنظیمات کلاینت

هر کلاینت باید این اطلاعات را داشته باشد:

```json
{
    "client_id": "myapp_client",
    "client_secret": "myapp_secret_2024",
    "domain": "myapp.example.com",
    "redirect_uri": "https://myapp.example.com/callback",
    "allow_any_path": true
}
```

### مرحله 3: پیاده‌سازی در اپلیکیشن

## 📡 API های موجود

### 1. API ورود (Login)

**Endpoint:** `POST /sso/api/login/`

**درخواست:**
```json
{
    "username": "user123",
    "password": "password123",
    "client_id": "myapp_client",
    "redirect_uri": "https://myapp.example.com/callback",
    "state": "optional_state_parameter"
}
```

**پاسخ موفق:**
```json
{
    "success": true,
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "Bearer",
    "expires_in": 900,
    "redirect_uri": "https://myapp.example.com/callback?jwt=TOKEN&state=STATE",
    "user": {
        "id": 1,
        "username": "user123",
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe"
    }
}
```

### 2. API ثبت‌نام (Register)

**Endpoint:** `POST /sso/api/register/`

**درخواست:**
```json
{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "password123",
    "password_confirm": "password123",
    "first_name": "New",
    "last_name": "User",
    "client_id": "myapp_client",
    "redirect_uri": "https://myapp.example.com/callback"
}
```

### 3. API اعتبارسنجی توکن

**Endpoint:** `POST /sso/api/validate-token/`

**درخواست:**
```json
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "client_id": "myapp_client"
}
```

**پاسخ موفق:**
```json
{
    "success": true,
    "valid": true,
    "user": {
        "id": 1,
        "username": "user123",
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "is_active": true
    },
    "token_info": {
        "exp": 1640995200,
        "iat": 1640991600,
        "jti": "token_id"
    }
}
```

### 4. API اطلاعات کاربر

**Endpoint:** `GET /sso/api/user-info/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**پاسخ:**
```json
{
    "success": true,
    "user": {
        "id": 1,
        "username": "user123",
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "+989123456789",
        "is_active": true,
        "date_joined": "2024-01-01T12:00:00Z",
        "last_login": "2024-01-01T12:00:00Z"
    }
}
```

### 5. API خروج (Logout)

**Endpoint:** `POST /sso/api/logout/`

**درخواست:**
```json
{
    "client_id": "myapp_client",
    "redirect_uri": "https://myapp.example.com/",
    "jwt": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## 💻 نمونه‌های عملی

### 1. اتصال اپلیکیشن React

```javascript
// SSO Service
class SSOService {
    constructor(baseURL, clientId) {
        this.baseURL = baseURL;
        this.clientId = clientId;
    }

    // هدایت به صفحه ورود SSO
    redirectToLogin(redirectUri, state = null) {
        const params = new URLSearchParams({
            client_id: this.clientId,
            redirect_uri: redirectUri
        });
        
        if (state) {
            params.append('state', state);
        }

        window.location.href = `${this.baseURL}/sso/login/?${params.toString()}`;
    }

    // اعتبارسنجی توکن
    async validateToken(token) {
        try {
            const response = await fetch(`${this.baseURL}/sso/api/validate-token/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    token: token,
                    client_id: this.clientId
                })
            });

            return await response.json();
        } catch (error) {
            console.error('Token validation error:', error);
            return { success: false, error: error.message };
        }
    }

    // دریافت اطلاعات کاربر
    async getUserInfo(token) {
        try {
            const response = await fetch(`${this.baseURL}/sso/api/user-info/`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            return await response.json();
        } catch (error) {
            console.error('Get user info error:', error);
            return { success: false, error: error.message };
        }
    }

    // خروج از سیستم
    async logout(token, redirectUri) {
        try {
            const response = await fetch(`${this.baseURL}/sso/api/logout/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    client_id: this.clientId,
                    redirect_uri: redirectUri,
                    jwt: token
                })
            });

            return await response.json();
        } catch (error) {
            console.error('Logout error:', error);
            return { success: false, error: error.message };
        }
    }
}

// استفاده در کامپوننت React
import React, { useEffect, useState } from 'react';

const App = () => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    
    const ssoService = new SSOService('http://127.0.0.1:8000', 'myapp_client');

    useEffect(() => {
        // بررسی وجود توکن در URL
        const urlParams = new URLSearchParams(window.location.search);
        const token = urlParams.get('jwt');
        
        if (token) {
            // ذخیره توکن
            localStorage.setItem('sso_token', token);
            
            // پاک کردن پارامترها از URL
            window.history.replaceState({}, document.title, window.location.pathname);
            
            // دریافت اطلاعات کاربر
            loadUserInfo(token);
        } else {
            // بررسی توکن موجود
            const existingToken = localStorage.getItem('sso_token');
            if (existingToken) {
                loadUserInfo(existingToken);
            } else {
                setLoading(false);
            }
        }
    }, []);

    const loadUserInfo = async (token) => {
        try {
            // اعتبارسنجی توکن
            const validation = await ssoService.validateToken(token);
            
            if (validation.success && validation.valid) {
                // دریافت اطلاعات کاربر
                const userInfo = await ssoService.getUserInfo(token);
                
                if (userInfo.success) {
                    setUser(userInfo.user);
                } else {
                    // توکن نامعتبر
                    localStorage.removeItem('sso_token');
                }
            } else {
                // توکن نامعتبر
                localStorage.removeItem('sso_token');
            }
        } catch (error) {
            console.error('Error loading user info:', error);
            localStorage.removeItem('sso_token');
        } finally {
            setLoading(false);
        }
    };

    const handleLogin = () => {
        const redirectUri = window.location.origin + window.location.pathname;
        ssoService.redirectToLogin(redirectUri);
    };

    const handleLogout = async () => {
        const token = localStorage.getItem('sso_token');
        if (token) {
            const redirectUri = window.location.origin;
            await ssoService.logout(token, redirectUri);
        }
        
        localStorage.removeItem('sso_token');
        setUser(null);
    };

    if (loading) {
        return <div>در حال بارگذاری...</div>;
    }

    if (!user) {
        return (
            <div>
                <h1>خوش آمدید</h1>
                <button onClick={handleLogin}>ورود</button>
            </div>
        );
    }

    return (
        <div>
            <h1>خوش آمدید، {user.first_name} {user.last_name}</h1>
            <p>ایمیل: {user.email}</p>
            <p>نام کاربری: {user.username}</p>
            <button onClick={handleLogout}>خروج</button>
        </div>
    );
};

export default App;
```

### 2. اتصال اپلیکیشن Python (Flask)

```python
import os
import requests
from flask import Flask, request, redirect, session, render_template, jsonify
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# تنظیمات SSO
SSO_BASE_URL = 'http://127.0.0.1:8000'
CLIENT_ID = 'myapp_client'
CLIENT_SECRET = 'myapp_secret_2024'

class SSOService:
    def __init__(self, base_url, client_id, client_secret):
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret

    def get_login_url(self, redirect_uri, state=None):
        """تولید URL ورود SSO"""
        params = {
            'client_id': self.client_id,
            'redirect_uri': redirect_uri
        }
        if state:
            params['state'] = state
        
        param_string = '&'.join([f'{k}={v}' for k, v in params.items()])
        return f'{self.base_url}/sso/login/?{param_string}'

    def validate_token(self, token):
        """اعتبارسنجی توکن"""
        try:
            response = requests.post(
                f'{self.base_url}/sso/api/validate-token/',
                json={
                    'token': token,
                    'client_id': self.client_id
                }
            )
            return response.json()
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def get_user_info(self, token):
        """دریافت اطلاعات کاربر"""
        try:
            response = requests.get(
                f'{self.base_url}/sso/api/user-info/',
                headers={'Authorization': f'Bearer {token}'}
            )
            return response.json()
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def logout(self, token, redirect_uri):
        """خروج از سیستم"""
        try:
            response = requests.post(
                f'{self.base_url}/sso/api/logout/',
                json={
                    'client_id': self.client_id,
                    'redirect_uri': redirect_uri,
                    'jwt': token
                }
            )
            return response.json()
        except Exception as e:
            return {'success': False, 'error': str(e)}

# ایجاد نمونه SSO Service
sso_service = SSOService(SSO_BASE_URL, CLIENT_ID, CLIENT_SECRET)

def login_required(f):
    """دکوراتور برای صفحات نیازمند ورود"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = session.get('sso_token')
        if not token:
            return redirect_to_login()
        
        # اعتبارسنجی توکن
        validation = sso_service.validate_token(token)
        if not validation.get('success') or not validation.get('valid'):
            session.pop('sso_token', None)
            return redirect_to_login()
        
        return f(*args, **kwargs)
    return decorated_function

def redirect_to_login():
    """هدایت به صفحه ورود SSO"""
    redirect_uri = request.url_root + 'callback'
    login_url = sso_service.get_login_url(redirect_uri)
    return redirect(login_url)

@app.route('/')
def index():
    """صفحه اصلی"""
    token = session.get('sso_token')
    if not token:
        return render_template('login.html')
    
    # دریافت اطلاعات کاربر
    user_info = sso_service.get_user_info(token)
    if user_info.get('success'):
        return render_template('dashboard.html', user=user_info['user'])
    else:
        session.pop('sso_token', None)
        return redirect_to_login()

@app.route('/callback')
def callback():
    """صفحه بازگشت از SSO"""
    token = request.args.get('jwt')
    state = request.args.get('state')
    
    if not token:
        return render_template('error.html', error='توکن دریافت نشد')
    
    # اعتبارسنجی توکن
    validation = sso_service.validate_token(token)
    if validation.get('success') and validation.get('valid'):
        session['sso_token'] = token
        return redirect('/')
    else:
        return render_template('error.html', error='توکن نامعتبر است')

@app.route('/dashboard')
@login_required
def dashboard():
    """صفحه داشبورد (نیازمند ورود)"""
    token = session.get('sso_token')
    user_info = sso_service.get_user_info(token)
    
    if user_info.get('success'):
        return render_template('dashboard.html', user=user_info['user'])
    else:
        return render_template('error.html', error='خطا در دریافت اطلاعات کاربر')

@app.route('/logout')
def logout():
    """خروج از سیستم"""
    token = session.get('sso_token')
    if token:
        redirect_uri = request.url_root
        sso_service.logout(token, redirect_uri)
    
    session.pop('sso_token', None)
    return redirect('/')

@app.route('/api/user')
@login_required
def api_user():
    """API دریافت اطلاعات کاربر"""
    token = session.get('sso_token')
    user_info = sso_service.get_user_info(token)
    
    if user_info.get('success'):
        return jsonify(user_info['user'])
    else:
        return jsonify({'error': 'خطا در دریافت اطلاعات کاربر'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### 3. اتصال اپلیکیشن PHP

```php
<?php
class SSOService {
    private $baseUrl;
    private $clientId;
    private $clientSecret;
    
    public function __construct($baseUrl, $clientId, $clientSecret) {
        $this->baseUrl = $baseUrl;
        $this->clientId = $clientId;
        $this->clientSecret = $clientSecret;
    }
    
    public function getLoginUrl($redirectUri, $state = null) {
        $params = [
            'client_id' => $this->clientId,
            'redirect_uri' => $redirectUri
        ];
        
        if ($state) {
            $params['state'] = $state;
        }
        
        return $this->baseUrl . '/sso/login/?' . http_build_query($params);
    }
    
    public function validateToken($token) {
        $data = [
            'token' => $token,
            'client_id' => $this->clientId
        ];
        
        $response = $this->makeRequest('/sso/api/validate-token/', 'POST', $data);
        return json_decode($response, true);
    }
    
    public function getUserInfo($token) {
        $headers = [
            'Authorization: Bearer ' . $token
        ];
        
        $response = $this->makeRequest('/sso/api/user-info/', 'GET', null, $headers);
        return json_decode($response, true);
    }
    
    public function logout($token, $redirectUri) {
        $data = [
            'client_id' => $this->clientId,
            'redirect_uri' => $redirectUri,
            'jwt' => $token
        ];
        
        $response = $this->makeRequest('/sso/api/logout/', 'POST', $data);
        return json_decode($response, true);
    }
    
    private function makeRequest($endpoint, $method = 'GET', $data = null, $headers = []) {
        $url = $this->baseUrl . $endpoint;
        
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, array_merge([
            'Content-Type: application/json'
        ], $headers));
        
        if ($method === 'POST' && $data) {
            curl_setopt($ch, CURLOPT_POST, true);
            curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
        }
        
        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        
        if ($httpCode !== 200) {
            throw new Exception('HTTP Error: ' . $httpCode);
        }
        
        return $response;
    }
}

// استفاده
session_start();

$ssoService = new SSOService('http://127.0.0.1:8000', 'myapp_client', 'myapp_secret_2024');

// بررسی توکن در URL
if (isset($_GET['jwt'])) {
    $token = $_GET['jwt'];
    
    // اعتبارسنجی توکن
    $validation = $ssoService->validateToken($token);
    
    if ($validation['success'] && $validation['valid']) {
        $_SESSION['sso_token'] = $token;
        
        // پاک کردن پارامترها از URL
        header('Location: ' . strtok($_SERVER["REQUEST_URI"], '?'));
        exit;
    }
}

// بررسی توکن موجود
$token = $_SESSION['sso_token'] ?? null;

if (!$token) {
    // هدایت به ورود
    $redirectUri = 'http://' . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI'];
    $loginUrl = $ssoService->getLoginUrl($redirectUri);
    header('Location: ' . $loginUrl);
    exit;
}

// اعتبارسنجی توکن
$validation = $ssoService->validateToken($token);

if (!$validation['success'] || !$validation['valid']) {
    // توکن نامعتبر
    unset($_SESSION['sso_token']);
    $redirectUri = 'http://' . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI'];
    $loginUrl = $ssoService->getLoginUrl($redirectUri);
    header('Location: ' . $loginUrl);
    exit;
}

// دریافت اطلاعات کاربر
$userInfo = $ssoService->getUserInfo($token);

if (!$userInfo['success']) {
    die('خطا در دریافت اطلاعات کاربر');
}

$user = $userInfo['user'];
?>

<!DOCTYPE html>
<html>
<head>
    <title>داشبورد</title>
    <meta charset="utf-8">
</head>
<body>
    <h1>خوش آمدید، <?php echo htmlspecialchars($user['first_name'] . ' ' . $user['last_name']); ?></h1>
    <p>ایمیل: <?php echo htmlspecialchars($user['email']); ?></p>
    <p>نام کاربری: <?php echo htmlspecialchars($user['username']); ?></p>
    
    <a href="logout.php">خروج</a>
</body>
</html>
```

## 🔧 مدیریت کلاینت‌ها

### ایجاد کلاینت جدید

```python
# اسکریپت ایجاد کلاینت
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
django.setup()

from sso.models import SSOClient

def create_client():
    client = SSOClient.objects.create(
        name='My New Application',
        domain='myapp.example.com',
        client_id='myapp_client_2024',
        client_secret='myapp_secret_2024',
        redirect_uri='https://myapp.example.com/callback',
        allowed_redirect_uris=[
            'https://myapp.example.com/callback',
            'https://myapp.example.com/auth/callback'
        ],
        allow_any_path=True,  # برای انعطاف بیشتر
        is_active=True
    )
    
    print(f"✅ کلاینت ایجاد شد: {client.name}")
    print(f"   Client ID: {client.client_id}")
    print(f"   Domain: {client.domain}")
    print(f"   Allow any path: {client.allow_any_path}")

if __name__ == '__main__':
    create_client()
```

### لیست کلاینت‌های موجود

```python
from sso.models import SSOClient

def list_clients():
    clients = SSOClient.objects.filter(is_active=True)
    
    print("📋 کلاینت‌های فعال:")
    for client in clients:
        print(f"\n🔹 {client.name}")
        print(f"   Client ID: {client.client_id}")
        print(f"   Domain: {client.domain}")
        print(f"   Allow any path: {'✅ Yes' if client.allow_any_path else '❌ No'}")
        print(f"   Created: {client.created_at}")

if __name__ == '__main__':
    list_clients()
```

## 🔒 امنیت

### نکات امنیتی مهم:

1. **استفاده از HTTPS**: همیشه از HTTPS برای ارتباطات استفاده کنید
2. **محافظت از Client Secret**: Client Secret را در محیط production محفوظ نگه دارید
3. **اعتبارسنجی توکن**: همیشه توکن‌ها را قبل از استفاده اعتبارسنجی کنید
4. **مدیریت Session**: توکن‌ها را به صورت امن ذخیره کنید
5. **Rate Limiting**: محدودیت درخواست‌ها را رعایت کنید

### مثال امن ذخیره توکن:

```javascript
// ذخیره امن توکن
class SecureTokenStorage {
    static setToken(token) {
        // استفاده از httpOnly cookie در production
        if (process.env.NODE_ENV === 'production') {
            // تنظیم cookie امن
            document.cookie = `sso_token=${token}; secure; httpOnly; sameSite=strict`;
        } else {
            // استفاده از localStorage در development
            localStorage.setItem('sso_token', token);
        }
    }
    
    static getToken() {
        if (process.env.NODE_ENV === 'production') {
            // خواندن از cookie
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                const [name, value] = cookie.trim().split('=');
                if (name === 'sso_token') {
                    return value;
                }
            }
            return null;
        } else {
            return localStorage.getItem('sso_token');
        }
    }
    
    static removeToken() {
        if (process.env.NODE_ENV === 'production') {
            document.cookie = 'sso_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
        } else {
            localStorage.removeItem('sso_token');
        }
    }
}
```

## 🐛 عیب‌یابی

### مشکلات رایج و راه‌حل‌ها:

#### 1. خطای "کلاینت نامعتبر است"
```bash
# بررسی وجود کلاینت
python manage.py shell
>>> from sso.models import SSOClient
>>> SSOClient.objects.filter(client_id='your_client_id')
```

#### 2. خطای "آدرس بازگشت مجاز نیست"
```bash
# بررسی تنظیمات redirect_uri
>>> client = SSOClient.objects.get(client_id='your_client_id')
>>> client.is_redirect_uri_allowed('https://yourdomain.com/callback')
```

#### 3. خطای "توکن نامعتبر است"
```python
# بررسی توکن
import jwt
from django.conf import settings

def decode_token(token):
    try:
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return decoded
    except jwt.ExpiredSignatureError:
        return {'error': 'توکن منقضی شده'}
    except jwt.InvalidTokenError:
        return {'error': 'توکن نامعتبر'}
```

#### 4. لاگ‌های سیستم
```bash
# مشاهده لاگ‌های SSO
tail -f logs/django.log | grep SSO
```

### ابزارهای عیب‌یابی:

```python
# اسکریپت عیب‌یابی
import requests
import json

def debug_sso_connection():
    base_url = 'http://127.0.0.1:8000'
    client_id = 'your_client_id'
    
    print("🔍 عیب‌یابی اتصال SSO")
    print("=" * 50)
    
    # تست 1: بررسی دسترسی به SSO
    try:
        response = requests.get(f'{base_url}/sso/api/user-info/')
        print(f"✅ SSO در دسترس است (Status: {response.status_code})")
    except Exception as e:
        print(f"❌ SSO در دسترس نیست: {e}")
        return
    
    # تست 2: بررسی کلاینت
    try:
        response = requests.post(f'{base_url}/sso/api/validate-token/', json={
            'token': 'test_token',
            'client_id': client_id
        })
        print(f"✅ کلاینت معتبر است (Status: {response.status_code})")
    except Exception as e:
        print(f"❌ خطا در کلاینت: {e}")
    
    # تست 3: بررسی تنظیمات
    print(f"\n📋 تنظیمات فعلی:")
    print(f"   Base URL: {base_url}")
    print(f"   Client ID: {client_id}")
    print(f"   Redirect URI: https://yourdomain.com/callback")

if __name__ == '__main__':
    debug_sso_connection()
```

## 📞 پشتیبانی

برای دریافت کمک بیشتر:

1. **مستندات کامل**: `docs/API.md`
2. **نمونه‌های بیشتر**: `examples/`
3. **اسکریپت‌های مدیریت**: `scripts/`
4. **لاگ‌های سیستم**: `logs/django.log`

---

**نکته مهم**: این راهنما برای نسخه فعلی سیستم SSO شما تهیه شده است. برای به‌روزرسانی‌ها و تغییرات جدید، مستندات را بررسی کنید.
