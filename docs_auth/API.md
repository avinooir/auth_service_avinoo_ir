# 📚 API Documentation - Auth Service

## Overview

This document provides comprehensive API documentation for the Auth Service microservice. The service provides authentication, authorization, and user management capabilities using JWT tokens.

## Base URL

```
http://localhost:8000
```

## Authentication

The API uses JWT (JSON Web Token) for authentication. Include the access token in the Authorization header:

```
Authorization: Bearer <access_token>
```

## Response Format

All API responses follow a consistent format:

### Success Response
```json
{
    "message": "Success message",
    "data": { ... },
    "status": "success"
}
```

### Error Response
```json
{
    "error": "Error message",
    "details": { ... },
    "status": "error"
}
```

## Rate Limiting

- **Registration**: 5 requests per minute per IP
- **Login**: 10 requests per minute per IP
- **General API**: 100 requests per hour for anonymous users, 1000 requests per hour for authenticated users

## Endpoints

### 🔐 Authentication Endpoints

#### POST /auth/register/

Register a new user account.

**Request Body:**
```json
{
    "username": "string (required, unique)",
    "email": "string (required, unique, valid email)",
    "phone_number": "string (optional, valid phone number)",
    "password": "string (required, min 8 characters)",
    "password_confirm": "string (required, must match password)",
    "first_name": "string (optional)",
    "last_name": "string (optional)"
}
```

**Response (201 Created):**
```json
{
    "message": "ثبت‌نام با موفقیت انجام شد.",
    "user": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "phone_number": "+989123456789",
        "first_name": "Test",
        "last_name": "User",
        "is_phone_verified": false,
        "is_email_verified": false,
        "is_active": true,
        "date_joined": "2024-01-01T12:00:00Z",
        "last_login": null,
        "profile": {
            "first_name_fa": null,
            "last_name_fa": null,
            "full_name_fa": null,
            "avatar": null,
            "bio": null,
            "birth_date": null,
            "created_at": "2024-01-01T12:00:00Z",
            "updated_at": "2024-01-01T12:00:00Z"
        }
    },
    "tokens": {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
}
```

#### POST /auth/login/

Authenticate user and return JWT tokens.

**Request Body:**
```json
{
    "username": "string (required, username or email)",
    "password": "string (required)"
}
```

**Response (200 OK):**
```json
{
    "message": "ورود با موفقیت انجام شد.",
    "user": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "phone_number": "+989123456789",
        "first_name": "Test",
        "last_name": "User",
        "is_phone_verified": false,
        "is_email_verified": false,
        "is_active": true,
        "date_joined": "2024-01-01T12:00:00Z",
        "last_login": "2024-01-01T12:00:00Z",
        "profile": { ... }
    },
    "tokens": {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
}
```

#### POST /auth/refresh/

Refresh access token using refresh token.

**Request Body:**
```json
{
    "refresh": "string (required, refresh token)"
}
```

**Response (200 OK):**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### GET /auth/me/

Get current user information.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
    "user": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "phone_number": "+989123456789",
        "first_name": "Test",
        "last_name": "User",
        "full_name": "Test User",
        "is_phone_verified": false,
        "is_email_verified": false,
        "is_active": true,
        "date_joined": "2024-01-01T12:00:00Z",
        "last_login": "2024-01-01T12:00:00Z",
        "profile": { ... }
    }
}
```

#### POST /auth/change-password/

Change user password.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
    "old_password": "string (required)",
    "new_password": "string (required, min 8 characters)",
    "new_password_confirm": "string (required, must match new_password)"
}
```

**Response (200 OK):**
```json
{
    "message": "رمز عبور با موفقیت تغییر کرد."
}
```

#### POST /auth/logout/

Logout user by blacklisting refresh token.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
    "refresh_token": "string (required, refresh token)"
}
```

**Response (200 OK):**
```json
{
    "message": "خروج با موفقیت انجام شد."
}
```

### 👥 Role Management Endpoints

#### GET /roles/

Get list of roles.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `search` (optional): Search in role name, display name, or description

**Response (200 OK):**
```json
{
    "roles": [
        {
            "id": 1,
            "name": "admin",
            "display_name": "مدیر",
            "description": "مدیریت کاربران، نقش‌ها و مجوزها",
            "is_active": true,
            "is_system_role": true,
            "permissions": [ ... ],
            "permission_count": 10,
            "user_count": 5,
            "created_at": "2024-01-01T12:00:00Z",
            "updated_at": "2024-01-01T12:00:00Z"
        }
    ],
    "count": 1
}
```

#### POST /roles/

Create a new role.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
    "name": "string (required, unique)",
    "display_name": "string (required)",
    "description": "string (optional)",
    "is_active": "boolean (optional, default: true)"
}
```

**Response (201 Created):**
```json
{
    "message": "نقش با موفقیت ایجاد شد.",
    "role": {
        "id": 2,
        "name": "editor",
        "display_name": "ویرایشگر",
        "description": "نقش ویرایشگر محتوا",
        "is_active": true,
        "is_system_role": false,
        "permissions": [],
        "permission_count": 0,
        "user_count": 0,
        "created_at": "2024-01-01T12:00:00Z",
        "updated_at": "2024-01-01T12:00:00Z"
    }
}
```

#### GET /roles/{id}/

Get role details.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
    "id": 1,
    "name": "admin",
    "display_name": "مدیر",
    "description": "مدیریت کاربران، نقش‌ها و مجوزها",
    "is_active": true,
    "is_system_role": true,
    "permissions": [ ... ],
    "permission_count": 10,
    "user_count": 5,
    "created_at": "2024-01-01T12:00:00Z",
    "updated_at": "2024-01-01T12:00:00Z"
}
```

#### PUT /roles/{id}/

Update role.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
    "name": "string (required)",
    "display_name": "string (required)",
    "description": "string (optional)",
    "is_active": "boolean (optional)"
}
```

#### DELETE /roles/{id}/

Delete role (soft delete).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
    "message": "نقش با موفقیت غیرفعال شد."
}
```

#### POST /roles/user-roles/

Assign role to user.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
    "user": "integer (required, user ID)",
    "role": "integer (required, role ID)",
    "expires_at": "string (optional, ISO datetime)",
    "is_active": "boolean (optional, default: true)"
}
```

**Response (201 Created):**
```json
{
    "message": "نقش با موفقیت به کاربر اختصاص داده شد.",
    "user_role": {
        "id": 1,
        "user": 1,
        "user_username": "testuser",
        "role": 1,
        "role_id": 1,
        "role_name": "مدیر",
        "assigned_by": 2,
        "assigned_by_username": "admin",
        "assigned_at": "2024-01-01T12:00:00Z",
        "expires_at": null,
        "is_active": true
    }
}
```

#### GET /roles/users/{user_id}/roles/

Get user roles.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
    "user": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com"
    },
    "roles": [
        {
            "id": 1,
            "user": 1,
            "user_username": "testuser",
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

### 🛡️ Permission Management Endpoints

#### GET /permissions/permissions/

Get list of permissions.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `app_label` (optional): Filter by app label
- `search` (optional): Search in permission name, display name, or description

**Response (200 OK):**
```json
{
    "results": [
        {
            "id": 1,
            "name": "users.view_user",
            "display_name": "مشاهده کاربران",
            "description": "اجازه مشاهده لیست کاربران",
            "app_label": "users",
            "codename": "view_user",
            "is_active": true,
            "created_at": "2024-01-01T12:00:00Z",
            "updated_at": "2024-01-01T12:00:00Z"
        }
    ],
    "count": 1
}
```

#### POST /permissions/user-permissions/

Grant permission directly to user.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
    "user": "integer (required, user ID)",
    "permission": "integer (required, permission ID)",
    "expires_at": "string (optional, ISO datetime)",
    "is_active": "boolean (optional, default: true)"
}
```

**Response (201 Created):**
```json
{
    "message": "مجوز با موفقیت به کاربر اعطا شد.",
    "user_permission": {
        "id": 1,
        "user": 1,
        "user_username": "testuser",
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
}
```

#### GET /permissions/users/{user_id}/permissions/

Get user permissions.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
    "user": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com"
    },
    "permissions": [
        {
            "id": 1,
            "user": 1,
            "user_username": "testuser",
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

#### GET /permissions/audit-logs/

Get audit logs.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `user_id` (optional): Filter by user ID
- `action` (optional): Filter by action type
- `target_user_id` (optional): Filter by target user ID

**Response (200 OK):**
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
            "target_user_username": "testuser",
            "permission": 1,
            "permission_name": "مشاهده کاربران",
            "role": null,
            "role_name": null,
            "details": {
                "permission_name": "users.view_user",
                "user_username": "testuser"
            },
            "ip_address": "127.0.0.1",
            "user_agent": "Mozilla/5.0...",
            "created_at": "2024-01-01T12:00:00Z"
        }
    ],
    "count": 1
}
```

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid request data |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error - Server error |

## Common Error Responses

### Validation Error (400)
```json
{
    "error": "Validation failed",
    "details": {
        "field_name": ["Error message"]
    }
}
```

### Authentication Error (401)
```json
{
    "error": "Authentication credentials were not provided."
}
```

### Permission Error (403)
```json
{
    "error": "You do not have permission to perform this action."
}
```

### Rate Limit Error (429)
```json
{
    "error": "تعداد درخواست‌های شما بیش از حد مجاز است. لطفاً کمی صبر کنید."
}
```

## Examples

### Complete Authentication Flow

1. **Register a new user:**
```bash
curl -X POST http://localhost:8000/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "first_name": "New",
    "last_name": "User"
  }'
```

2. **Login:**
```bash
curl -X POST http://localhost:8000/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "password": "securepassword123"
  }'
```

3. **Get user profile:**
```bash
curl -X GET http://localhost:8000/auth/me/ \
  -H "Authorization: Bearer <access_token>"
```

4. **Assign role to user:**
```bash
curl -X POST http://localhost:8000/roles/user-roles/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "user": 1,
    "role": 2
  }'
```

5. **Grant permission to user:**
```bash
curl -X POST http://localhost:8000/permissions/user-permissions/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "user": 1,
    "permission": 3
  }'
```

6. **Logout:**
```bash
curl -X POST http://localhost:8000/auth/logout/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "<refresh_token>"
  }'
```

## Notes

- All timestamps are in ISO 8601 format (UTC)
- JWT access tokens expire after 15 minutes by default
- JWT refresh tokens expire after 7 days by default
- All text responses are in Persian (Farsi)
- The API supports both Persian and English content
- Rate limiting is applied per IP address and per user
- All sensitive operations are logged in the audit system
