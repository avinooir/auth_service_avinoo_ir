"""
Send short report to Telegram
"""

import requests
from datetime import datetime

def send_telegram_message(message):
    """Send message to Telegram"""
    
    # Telegram Bot configuration
    bot_token = "7677902649:AAHBEOz_aOn_fhrPYXIsiPQwikDXgca2FX8"
    chat_id = "7285454186"
    
    # Telegram API URL
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    # Message data
    data = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print("✅ گزارش با موفقیت به تلگرام ارسال شد")
            return True
        else:
            print(f"❌ خطا در ارسال گزارش: {response.status_code}")
            print(f"پاسخ: {response.text}")
            return False
    except Exception as e:
        print(f"❌ خطا در ارسال گزارش: {e}")
        return False

def send_short_report():
    """Send short report to Telegram"""
    
    report = f"""📋 *گزارش جامع - پیاده‌سازی سیستم احراز هویت meet.avinoo.ir*

📅 *تاریخ:* 13 ژانویه 2025
🔢 *شماره گزارش:* 02
🎯 *پروژه:* Auth Service - Meet Integration

✅ *خلاصه اجرایی:*
سیستم احراز هویت برای اپلیکیشن جلسات meet.avinoo.ir با موفقیت پیاده‌سازی شد.

📁 *فایل‌های ایجاد شده:*
• `apps/meet/` - اپلیکیشن meet integration
• `apps/meet/jwt_utils.py` - ابزارهای تولید JWT
• `scripts/create_meet_client.py` - ایجاد کلاینت SSO
• `scripts/setup_meet_production.py` - راه‌اندازی production
• `test_meet_integration.py` - تست یکپارچگی
• `test_meet_sso_flow.py` - تست جریان SSO

🔧 *تغییرات مهم:*
• اضافه شدن فیلدهای avatar_url، region، display_name به مدل User
• پیاده‌سازی JWT generator مخصوص meet
• اصلاح SSO flow برای کلاینت meet
• ایجاد API endpoints برای مدیریت جلسات

🔄 *جریان SSO:*
1. کاربر روی meet.avinoo.ir/roomname کلیک می‌کند
2. هدایت به auth.avinoo.ir/login
3. بررسی دسترسی از طریق API خارجی
4. تولید JWT token
5. هدایت به meet.avinoo.ir/roomname?jwt=TOKEN

⚙️ *تنظیمات Production:*
• کلاینت SSO: meet_avinoo
• دامنه: meet.avinoo.ir
• API خارجی: http://avinoo.ir/api/meets/access/
• JWT Secret: meet_secret_key_2024

✅ *تست‌های انجام شده:*
تمام تست‌ها با موفقیت انجام شد و سیستم آماده production است.

📝 *نکات مهم:*
• مطمئن شوید API خارجی در دسترس است
• JWT secret را در production تغییر دهید
• لاگ‌ها را برای نظارت بررسی کنید

🎉 *نتیجه:* سیستم با موفقیت پیاده‌سازی شد و آماده deployment است!

---
📅 تهیه شده: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

    return send_telegram_message(report)

if __name__ == '__main__':
    print("📤 ارسال گزارش کوتاه به تلگرام...")
    if send_short_report():
        print("🎉 گزارش با موفقیت ارسال شد!")
    else:
        print("❌ خطا در ارسال گزارش!")
