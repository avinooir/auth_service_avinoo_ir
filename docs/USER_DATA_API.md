# 📊 API دریافت اطلاعات کاربر - راهنمای کامل

## 🎯 مقدمه

این مستند تمام API های مربوط به دریافت اطلاعات کاربر در سیستم SSO شما را پوشش می‌دهد. این API ها به شما امکان دسترسی به اطلاعات کامل کاربران، نقش‌ها، مجوزها و لاگ‌های سیستم را می‌دهند.

## 🔗 Base URL

```
http://127.0.0.1:8000
```

## 🔐 احراز هویت

تمام API های زیر نیاز به توکن JWT دارند:

```
Authorization: Bearer <access_token>
```

## 📋 فهرست API ها

### 1. دریافت اطلاعات کاربر فعلی

**Endpoint:** `GET /sso/api/user-info/`

**توضیح:** اطلاعات کامل کاربری که توکن متعلق به اوست را برمی‌گرداند.

**Headers:**
```
Authorization: Bearer <access_token>
```

**پاسخ موفق (200 OK):**
```json
{
    "success": true,
    "user": {
        "id": 1,
        "username": "user123",
        "email": "user@example.com",
        "first_name": "علی",
        "last_name": "احمدی",
        "phone_number": "+989123456789",
        "is_active": true,
        "date_joined": "2024-01-01T12:00:00Z",
        "last_login": "2024-01-01T15:30:00Z"
    }
}
```

**پاسخ خطا (401 Unauthorized):**
```json
{
    "success": false,
    "error": "Authentication credentials were not provided."
}
```

### 2. اعتبارسنجی توکن و دریافت اطلاعات کاربر

**Endpoint:** `POST /sso/api/validate-token/`

**توضیح:** توکن JWT را اعتبارسنجی می‌کند و در صورت معتبر بودن، اطلاعات کاربر را برمی‌گرداند.

**درخواست:**
```json
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "client_id": "myapp_client"
}
```

**پاسخ موفق (200 OK):**
```json
{
    "success": true,
    "valid": true,
    "user": {
        "id": 1,
        "username": "user123",
        "email": "user@example.com",
        "first_name": "علی",
        "last_name": "احمدی",
        "is_active": true
    },
    "token_info": {
        "exp": 1640995200,
        "iat": 1640991600,
        "jti": "unique_token_id"
    }
}
```

**پاسخ توکن نامعتبر (200 OK):**
```json
{
    "success": true,
    "valid": false,
    "error": "توکن نامعتبر است"
}
```

### 3. دریافت اطلاعات کاربر در فرآیند ورود

**Endpoint:** `POST /sso/api/login/`

**توضیح:** در فرآیند ورود، اطلاعات کاربر همراه با توکن برمی‌گردد.

**درخواست:**
```json
{
    "username": "user123",
    "password": "password123",
    "client_id": "myapp_client",
    "redirect_uri": "https://myapp.example.com/callback"
}
```

**پاسخ موفق (200 OK):**
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
        "first_name": "علی",
        "last_name": "احمدی"
    }
}
```

### 4. دریافت اطلاعات کاربر در فرآیند ثبت‌نام

**Endpoint:** `POST /sso/api/register/`

**توضیح:** در فرآیند ثبت‌نام، اطلاعات کاربر جدید همراه با توکن برمی‌گردد.

**درخواست:**
```json
{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "password123",
    "password_confirm": "password123",
    "first_name": "محمد",
    "last_name": "رضایی",
    "client_id": "myapp_client",
    "redirect_uri": "https://myapp.example.com/callback"
}
```

**پاسخ موفق (201 Created):**
```json
{
    "success": true,
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "Bearer",
    "expires_in": 900,
    "redirect_uri": "https://myapp.example.com/callback?jwt=TOKEN&state=STATE",
    "user": {
        "id": 2,
        "username": "newuser",
        "email": "newuser@example.com",
        "first_name": "محمد",
        "last_name": "رضایی"
    }
}
```

## 👥 API های مدیریت کاربران (نیاز به دسترسی ادمین)

### 5. لیست کاربران

**Endpoint:** `GET /users/`

**توضیح:** لیست تمام کاربران سیستم را برمی‌گرداند (فقط برای ادمین‌ها).

**Headers:**
```
Authorization: Bearer <admin_access_token>
```

**Query Parameters:**
- `search` (اختیاری): جستجو در نام کاربری، ایمیل، نام و نام خانوادگی
- `page` (اختیاری): شماره صفحه برای pagination
- `page_size` (اختیاری): تعداد آیتم در هر صفحه

**پاسخ موفق (200 OK):**
```json
{
    "results": [
        {
            "id": 1,
            "username": "user123",
            "email": "user@example.com",
            "first_name": "علی",
            "last_name": "احمدی",
            "phone_number": "+989123456789",
            "is_active": true,
            "is_staff": false,
            "is_superuser": false,
            "date_joined": "2024-01-01T12:00:00Z",
            "last_login": "2024-01-01T15:30:00Z",
            "profile": {
                "first_name_fa": "علی",
                "last_name_fa": "احمدی",
                "full_name_fa": "علی احمدی",
                "avatar": null,
                "bio": null,
                "birth_date": null
            }
        }
    ],
    "count": 1,
    "next": null,
    "previous": null
}
```

### 6. جزئیات کاربر خاص

**Endpoint:** `GET /users/{user_id}/`

**توضیح:** اطلاعات کامل یک کاربر خاص را برمی‌گرداند.

**Headers:**
```
Authorization: Bearer <admin_access_token>
```

**پاسخ موفق (200 OK):**
```json
{
    "id": 1,
    "username": "user123",
    "email": "user@example.com",
    "first_name": "علی",
    "last_name": "احمدی",
    "phone_number": "+989123456789",
    "is_active": true,
    "is_staff": false,
    "is_superuser": false,
    "is_phone_verified": false,
    "is_email_verified": false,
    "date_joined": "2024-01-01T12:00:00Z",
    "last_login": "2024-01-01T15:30:00Z",
    "last_login_ip": "192.168.1.100",
    "failed_login_attempts": 0,
    "locked_until": null,
    "profile": {
        "first_name_fa": "علی",
        "last_name_fa": "احمدی",
        "full_name_fa": "علی احمدی",
        "avatar": "https://example.com/avatars/user1.jpg",
        "bio": "برنامه‌نویس و توسعه‌دهنده",
        "birth_date": "1990-05-15",
        "created_at": "2024-01-01T12:00:00Z",
        "updated_at": "2024-01-01T12:00:00Z"
    }
}
```

## 🛡️ API های نقش‌ها و مجوزها

### 7. نقش‌های کاربر

**Endpoint:** `GET /roles/users/{user_id}/roles/`

**توضیح:** تمام نقش‌های اختصاص داده شده به یک کاربر را برمی‌گرداند.

**Headers:**
```
Authorization: Bearer <admin_access_token>
```

**پاسخ موفق (200 OK):**
```json
{
    "user": {
        "id": 1,
        "username": "user123",
        "email": "user@example.com"
    },
    "roles": [
        {
            "id": 1,
            "user": 1,
            "user_username": "user123",
            "role": 1,
            "role_id": 1,
            "role_name": "مدیر",
            "assigned_by": 2,
            "assigned_by_username": "admin",
            "assigned_at": "2024-01-01T12:00:00Z",
            "expires_at": null,
            "is_active": true
        }
    ]
}
```

### 8. مجوزهای کاربر

**Endpoint:** `GET /permissions/users/{user_id}/permissions/`

**توضیح:** تمام مجوزهای مستقیم اختصاص داده شده به یک کاربر را برمی‌گرداند.

**Headers:**
```
Authorization: Bearer <admin_access_token>
```

**پاسخ موفق (200 OK):**
```json
{
    "user": {
        "id": 1,
        "username": "user123",
        "email": "user@example.com"
    },
    "permissions": [
        {
            "id": 1,
            "user": 1,
            "user_username": "user123",
            "permission": 1,
            "permission_id": 1,
            "permission_name": "مشاهده کاربران",
            "granted_by": 2,
            "granted_by_username": "admin",
            "granted_at": "2024-01-01T12:00:00Z",
            "expires_at": null,
            "is_active": true,
            "is_expired": false
        }
    ]
}
```

## 📊 API های لاگ و حسابرسی

### 9. لاگ‌های SSO

**Endpoint:** `GET /sso/api/admin/logs/`

**توضیح:** لاگ‌های فعالیت‌های SSO را برمی‌گرداند (فقط برای ادمین‌ها).

**Headers:**
```
Authorization: Bearer <admin_access_token>
```

**Query Parameters:**
- `user_id` (اختیاری): فیلتر بر اساس شناسه کاربر
- `action` (اختیاری): فیلتر بر اساس نوع عمل
- `client_id` (اختیاری): فیلتر بر اساس شناسه کلاینت

**پاسخ موفق (200 OK):**
```json
{
    "success": true,
    "logs": [
        {
            "id": "uuid-string",
            "user": 1,
            "user_username": "user123",
            "client": "uuid-string",
            "client_name": "My Application",
            "action": "login",
            "ip_address": "192.168.1.100",
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "details": {
                "session_id": "uuid-string"
            },
            "created_at": "2024-01-01T15:30:00Z"
        }
    ]
}
```

### 10. لاگ‌های مجوزها

**Endpoint:** `GET /permissions/audit-logs/`

**توضیح:** لاگ‌های تغییرات مجوزها و نقش‌ها را برمی‌گرداند.

**Headers:**
```
Authorization: Bearer <admin_access_token>
```

**Query Parameters:**
- `user_id` (اختیاری): فیلتر بر اساس شناسه کاربر
- `action` (اختیاری): فیلتر بر اساس نوع عمل (grant, revoke, assign, unassign)
- `target_user_id` (اختیاری): فیلتر بر اساس شناسه کاربر هدف

**پاسخ موفق (200 OK):**
```json
{
    "results": [
        {
            "id": 1,
            "user": 2,
            "user_username": "admin",
            "action": "grant",
            "action_display": "اعطا",
            "target_user": 1,
            "target_user_username": "user123",
            "permission": 1,
            "permission_name": "مشاهده کاربران",
            "role": null,
            "role_name": null,
            "details": {
                "permission_name": "users.view_user",
                "user_username": "user123"
            },
            "ip_address": "192.168.1.100",
            "user_agent": "Mozilla/5.0...",
            "created_at": "2024-01-01T12:00:00Z"
        }
    ],
    "count": 1
}
```

## 🔧 API های مدیریت کلاینت‌ها

### 11. لیست کلاینت‌های SSO

**Endpoint:** `GET /sso/api/admin/clients/`

**توضیح:** لیست تمام کلاینت‌های ثبت شده در SSO را برمی‌گرداند.

**Headers:**
```
Authorization: Bearer <admin_access_token>
```

**پاسخ موفق (200 OK):**
```json
{
    "success": true,
    "clients": [
        {
            "id": "uuid-string",
            "name": "My Application",
            "domain": "myapp.example.com",
            "client_id": "myapp_client",
            "redirect_uri": "https://myapp.example.com/callback",
            "allowed_redirect_uris": [
                "https://myapp.example.com/callback",
                "https://myapp.example.com/auth/callback"
            ],
            "allow_any_path": true,
            "is_active": true,
            "created_at": "2024-01-01T12:00:00Z",
            "updated_at": "2024-01-01T12:00:00Z"
        }
    ]
}
```

### 12. جلسات SSO

**Endpoint:** `GET /sso/api/admin/sessions/`

**توضیح:** لیست جلسات فعال SSO را برمی‌گرداند.

**Headers:**
```
Authorization: Bearer <admin_access_token>
```

**پاسخ موفق (200 OK):**
```json
{
    "success": true,
    "sessions": [
        {
            "id": "uuid-string",
            "user": 1,
            "user_username": "user123",
            "client": "uuid-string",
            "client_name": "My Application",
            "state": "random_state_string",
            "redirect_uri": "https://myapp.example.com/callback",
            "created_at": "2024-01-01T15:30:00Z",
            "expires_at": "2024-01-01T15:40:00Z",
            "is_used": true
        }
    ]
}
```

## 💡 نمونه‌های استفاده عملی

### 1. بررسی احراز هویت کاربر در اپلیکیشن

```javascript
// JavaScript
async function checkUserAuthentication() {
    const token = localStorage.getItem('sso_token');
    
    if (!token) {
        return { authenticated: false, user: null };
    }
    
    try {
        const response = await fetch('http://127.0.0.1:8000/sso/api/validate-token/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                token: token,
                client_id: 'myapp_client'
            })
        });
        
        const data = await response.json();
        
        if (data.success && data.valid) {
            return { authenticated: true, user: data.user };
        } else {
            localStorage.removeItem('sso_token');
            return { authenticated: false, user: null };
        }
    } catch (error) {
        console.error('Authentication check failed:', error);
        return { authenticated: false, user: null };
    }
}
```

### 2. دریافت اطلاعات کامل کاربر

```python
# Python
import requests

def get_user_info(token):
    """دریافت اطلاعات کامل کاربر"""
    try:
        response = requests.get(
            'http://127.0.0.1:8000/sso/api/user-info/',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                return data['user']
        
        return None
    except Exception as e:
        print(f"Error getting user info: {e}")
        return None

# استفاده
user_info = get_user_info('your_jwt_token')
if user_info:
    print(f"User: {user_info['first_name']} {user_info['last_name']}")
    print(f"Email: {user_info['email']}")
    print(f"Phone: {user_info['phone_number']}")
```

### 3. بررسی نقش‌ها و مجوزهای کاربر

```python
# Python - بررسی نقش‌ها و مجوزها
def check_user_permissions(user_id, admin_token):
    """بررسی نقش‌ها و مجوزهای کاربر"""
    try:
        # دریافت نقش‌ها
        roles_response = requests.get(
            f'http://127.0.0.1:8000/roles/users/{user_id}/roles/',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        
        # دریافت مجوزها
        permissions_response = requests.get(
            f'http://127.0.0.1:8000/permissions/users/{user_id}/permissions/',
            headers={'Authorization': f'Bearer {admin_token}'}
        )
        
        roles = roles_response.json() if roles_response.status_code == 200 else {}
        permissions = permissions_response.json() if permissions_response.status_code == 200 else {}
        
        return {
            'roles': roles.get('roles', []),
            'permissions': permissions.get('permissions', [])
        }
    except Exception as e:
        print(f"Error checking permissions: {e}")
        return {'roles': [], 'permissions': []}
```

## ⚠️ نکات مهم

### 1. امنیت
- همیشه از HTTPS در محیط production استفاده کنید
- توکن‌ها را به صورت امن ذخیره کنید
- توکن‌ها را به صورت منظم اعتبارسنجی کنید

### 2. مدیریت خطا
- همیشه پاسخ‌های API را بررسی کنید
- در صورت خطای 401، کاربر را به صفحه ورود هدایت کنید
- خطاهای شبکه را مدیریت کنید

### 3. Performance
- توکن‌ها را cache کنید
- از pagination برای لیست‌های بزرگ استفاده کنید
- درخواست‌های غیرضروری را کاهش دهید

### 4. Rate Limiting
- محدودیت درخواست‌ها را رعایت کنید
- در صورت رسیدن به حد مجاز، کمی صبر کنید

## 🔍 کدهای خطا

| کد | توضیح | راه‌حل |
|----|-------|--------|
| 200 | موفق | - |
| 400 | درخواست نامعتبر | پارامترها را بررسی کنید |
| 401 | عدم احراز هویت | توکن معتبر ارسال کنید |
| 403 | عدم دسترسی | دسترسی ادمین مورد نیاز است |
| 404 | یافت نشد | شناسه کاربر یا منبع را بررسی کنید |
| 429 | محدودیت درخواست | کمی صبر کنید |
| 500 | خطای سرور | با پشتیبانی تماس بگیرید |

---

**نکته:** این مستند برای نسخه فعلی سیستم SSO شما تهیه شده است. برای به‌روزرسانی‌ها، مستندات را بررسی کنید.
