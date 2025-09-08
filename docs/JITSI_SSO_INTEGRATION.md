# Jitsi Meet SSO Integration

این مستند نحوه ادغام Jitsi Meet با سیستم SSO آوینو را توضیح می‌دهد.

## 🔧 تنظیمات انجام شده

### 1. اصلاح SSO Callback
- پارامتر `next` به callback page اضافه شد
- بعد از لاگین موفق، کاربر به URL مشخص شده هدایت می‌شود

### 2. ایجاد کلاینت SSO برای Jitsi Meet
- کلاینت با ID: `meet`
- Domain: `meet.avinoo.ir`
- Redirect URI: `https://meet.avinoo.ir/callback`

### 3. فایل‌های نمونه
- `client_apps/jitsi_meet/index.html` - صفحه اصلی
- `client_apps/jitsi_meet/callback.html` - صفحه callback

## 🚀 نحوه استفاده

### مرحله ۱: ریدایرکت به SSO
وقتی کاربر می‌خواهد وارد جلسه `/team1` شود:

```
https://auth.avinoo.ir/sso/login/?client_id=meet&redirect_uri=https://meet.avinoo.ir/callback&next=/team1
```

### مرحله ۲: بعد از لاگین موفق
SSO کاربر را به callback هدایت می‌کند:

```
https://meet.avinoo.ir/callback?token=JWT_TOKEN&next=/team1
```

### مرحله ۳: Callback Processing
- توکن اعتبارسنجی می‌شود
- اطلاعات کاربر نمایش داده می‌شود
- کاربر به جلسه `/team1` هدایت می‌شود

## 📋 مثال کامل

### 1. کاربر می‌خواهد وارد جلسه `team1` شود:

```javascript
// در Jitsi Meet application
const loginUrl = `https://auth.avinoo.ir/sso/login/?client_id=meet&redirect_uri=https://meet.avinoo.ir/callback&next=/team1`;
window.location.href = loginUrl;
```

### 2. بعد از لاگین موفق، callback دریافت می‌کند:

```javascript
// در callback.html
const urlParams = new URLSearchParams(window.location.search);
const token = urlParams.get('token');
const next = urlParams.get('next') || '/';

// اعتبارسنجی توکن
const response = await fetch('https://auth.avinoo.ir/sso/api/validate-token/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        token: token,
        client_id: 'meet'
    })
});

// ذخیره توکن و هدایت به جلسه
localStorage.setItem('jitsi_token', token);
window.location.href = next;
```

### 3. در جلسه Jitsi Meet:

```javascript
// استفاده از توکن برای Jitsi Meet API
const token = localStorage.getItem('jitsi_token');
const roomName = 'team1';

// راه‌اندازی Jitsi Meet با توکن
const domain = 'meet.avinoo.ir';
const options = {
    roomName: roomName,
    jwt: token,
    parentNode: document.querySelector('#jitsi-container')
};

const api = new JitsiMeetExternalAPI(domain, options);
```

## 🔐 امنیت

### 1. اعتبارسنجی توکن
- هر توکن قبل از استفاده اعتبارسنجی می‌شود
- توکن‌های منقضی یا نامعتبر رد می‌شوند

### 2. محدودیت دسترسی
- فقط کلاینت‌های مجاز می‌توانند از SSO استفاده کنند
- Redirect URI باید دقیقاً مطابق باشد

### 3. Logging
- تمام فعالیت‌های SSO ثبت می‌شوند
- شامل لاگین، لاگاوت، و اعتبارسنجی توکن

## 🛠️ API Endpoints

### 1. اعتبارسنجی توکن
```
POST https://auth.avinoo.ir/sso/api/validate-token/
Content-Type: application/json

{
    "token": "JWT_TOKEN",
    "client_id": "meet"
}
```

### 2. لاگاوت
```
GET https://auth.avinoo.ir/sso/api/logout/?client_id=meet&redirect_uri=https://meet.avinoo.ir/
```

### 3. اطلاعات کاربر
```
GET https://auth.avinoo.ir/sso/api/user-info/
Authorization: Bearer JWT_TOKEN
```

## 📝 نکات مهم

1. **توکن JWT**: توکن‌ها دارای زمان انقضا هستند
2. **Refresh Token**: برای تمدید توکن استفاده می‌شود
3. **Error Handling**: خطاها باید به درستی مدیریت شوند
4. **Logout**: توکن‌ها باید هنگام خروج پاک شوند

## 🔄 Flow Diagram

```
User → Jitsi Meet → SSO Login → Callback → Jitsi Room
  ↓         ↓           ↓          ↓          ↓
/team1 → Redirect → Auth → Token → /team1
```

## 🧪 تست

### 1. تست لاگین
```bash
curl -X POST https://auth.avinoo.ir/sso/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test_user",
    "password": "test_pass",
    "client_id": "meet",
    "redirect_uri": "https://meet.avinoo.ir/callback"
  }'
```

### 2. تست اعتبارسنجی
```bash
curl -X POST https://auth.avinoo.ir/sso/api/validate-token/ \
  -H "Content-Type: application/json" \
  -d '{
    "token": "JWT_TOKEN",
    "client_id": "meet"
  }'
```

## 📞 پشتیبانی

برای سوالات و مشکلات:
- ایمیل: support@avinoo.ir
- تلفن: +98-21-12345678
