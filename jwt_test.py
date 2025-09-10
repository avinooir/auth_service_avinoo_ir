#!/usr/bin/env python3
import base64
import json
import hmac
import hashlib

# مقدار ثابت برای مثال
app_id = "meet_avinoo"
app_secret = "super_secret_key_98765"

# هدر JWT
header = {
    "alg": "HS256",
    "typ": "JWT"
}
# "room": "testroom",
# پی‌لود
payload = {
    "aud": app_id,
    "iss": app_id,
    "sub": "meet.avinoo.ir",
    "room": "*",
    "exp": 1758397966,  # زمان انقضا (Unix timestamp)
    "context": {
        "user": {
            "name": "John Doe",
            "email": "john@example.com"
        }
    }
}

def b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")

# ساخت بخش‌های JWT
header_b64 = b64url_encode(json.dumps(header, separators=(",", ":")).encode())
payload_b64 = b64url_encode(json.dumps(payload, separators=(",", ":")).encode())

to_sign = f"{header_b64}.{payload_b64}"

signature = hmac.new(
    app_secret.encode("utf-8"),
    to_sign.encode("utf-8"),
    hashlib.sha256
).digest()

signature_b64 = b64url_encode(signature)

jwt_token = f"{to_sign}.{signature_b64}"

print("---- JWT Token ----")
print(jwt_token)
import time

# زمان فعلی به ثانیه
now = int(time.time())

# اضافه کردن 10 روز (10 * 24 * 60 * 60 ثانیه)
exp = now + 10 * 24 * 60 * 60


