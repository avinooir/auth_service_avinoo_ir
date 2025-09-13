import jwt
import time

# اطلاعات اصلی
APP_ID = "meet_avinoo"          # همون که توی prosody ست کردی
APP_SECRET = "super_secret_key_98765"  # کلید مخفی
DOMAIN = "meet.avinoo.ir"     # دامنه Jitsi
ROOM = "*"                      # می‌تونی بذاری * یا اسم اتاق خاص

# زمان‌ها
now = int(time.time())
exp = now + 3600   # توکن 1 ساعت اعتبار داشته باشه
nbf = now - 500

# payload کامل
payload = {
    "aud": APP_ID,
    "iss": APP_ID,
    "sub": DOMAIN,
    "room": ROOM,
    "exp": exp,
    "nbf": nbf,
    "moderator": True,
    "context": {
        "user": {
            "id": "12345",
            "name": "Ali",
            "email": "ali@example.com",
            "avatar": "https://example.com/avatar.png",
            "affiliation": "owner",
            "moderator": True,
            "region": "us-east",
            "displayName": "Ali M."
        },
        "group": "dev-team",
        "features": {
            "livestreaming": True,
            "recording": True,
            "screen-sharing": True,
            "sip": False,
            "etherpad": False,
            "transcription": True,
            "breakout-rooms": True
        }
    },
    "identity": {
        "type": "user",
        "guest": False,
        "externalId": "ext-123456"
    },
    "custom": {
        "theme": "green",
        "allowKnocking": True,
        "enablePolls": True
    }
}

# ساخت توکن
token = jwt.encode(payload, APP_SECRET, algorithm="HS256")

print("Jitsi JWT Token:\n", token)
