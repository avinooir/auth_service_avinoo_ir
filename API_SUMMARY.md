# 📡 خلاصه API - سیستم احراز هویت

## 🔐 احراز هویت

### ورود
```http
POST /api/login/
Content-Type: application/json

{
    "username": "نام کاربری",
    "password": "رمز عبور",
    "client_id": "شناسه اپ",
    "redirect_uri": "آدرس بازگشت"
}
```

### ثبت‌نام
```http
POST /api/register/
Content-Type: application/json

{
    "username": "نام کاربری",
    "email": "ایمیل",
    "phone_number": "+989123456789",
    "password": "رمز عبور",
    "password_confirm": "تکرار رمز",
    "first_name": "نام",
    "last_name": "نام خانوادگی",
    "client_id": "شناسه اپ",
    "redirect_uri": "آدرس بازگشت"
}
```

### اعتبارسنجی توکن
```http
POST /api/validate-token/
Content-Type: application/json

{
    "token": "JWT_TOKEN",
    "client_id": "شناسه اپ"
}
```

### دریافت اطلاعات کاربر
```http
GET /api/user-info/
Authorization: Bearer JWT_TOKEN
```

### خروج
```http
POST /api/logout/
Authorization: Bearer JWT_TOKEN
Content-Type: application/json

{
    "client_id": "شناسه اپ",
    "redirect_uri": "آدرس بازگشت"
}
```

## 🌐 صفحات وب

### ورود
```
GET /login/?client_id=شناسه_اپ&redirect_uri=آدرس_بازگشت&state=random_state
```

### ثبت‌نام
```
GET /register/?client_id=شناسه_اپ&redirect_uri=آدرس_بازگشت&state=random_state
```

### بازگشت
```
GET /callback/?token=JWT_TOKEN&state=random_state&client_id=شناسه_اپ
```

## 📊 پاسخ‌های API

### موفق
```json
{
    "success": true,
    "message": "پیام موفقیت",
    "data": {
        "token": "JWT_TOKEN",
        "user": {
            "id": 1,
            "guid": "550e8400-e29b-41d4-a716-446655440000",
            "username": "testuser",
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User"
        }
    }
}
```

### خطا
```json
{
    "success": false,
    "error": "پیام خطا",
    "details": "جزئیات خطا"
}
```

## 🆔 GUID (Global Unique Identifier)

هر کاربر یک GUID یکتا دارد که در تمام API ها و JWT Token ها موجود است:

### ویژگی‌های GUID:
- **یکتا**: هر کاربر یک GUID منحصر به فرد دارد
- **غیرقابل تغییر**: پس از ایجاد، تغییر نمی‌کند
- **در JWT**: در تمام توکن‌های JWT موجود است
- **در API**: در تمام پاسخ‌های API موجود است

### استفاده از GUID:
```javascript
// دریافت GUID از JWT Token
const token = localStorage.getItem('auth_token');
const decoded = jwt.decode(token);
const userGuid = decoded.guid;

// استفاده در API calls
fetch('/api/user-info/', {
    headers: {
        'Authorization': `Bearer ${token}`,
        'X-User-GUID': userGuid
    }
});
```

## 🔑 کدهای وضعیت HTTP

- **200**: موفق
- **400**: خطای درخواست
- **401**: عدم احراز هویت
- **403**: عدم دسترسی
- **404**: یافت نشد
- **500**: خطای سرور
