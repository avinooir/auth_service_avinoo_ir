"""
Send update report to Telegram
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
            print("✅ گزارش به‌روزرسانی با موفقیت به تلگرام ارسال شد")
            return True
        else:
            print(f"❌ خطا در ارسال گزارش: {response.status_code}")
            print(f"پاسخ: {response.text}")
            return False
    except Exception as e:
        print(f"❌ خطا در ارسال گزارش: {e}")
        return False

def send_update_report():
    """Send update report to Telegram"""
    
    report = f"""🔄 *گزارش به‌روزرسانی - سیستم meet.avinoo.ir*

📅 *تاریخ:* 13 ژانویه 2025
🔢 *شماره گزارش:* 03
🎯 *پروژه:* Auth Service - Meet Integration (به‌روزرسانی)

✅ *تغییرات انجام شده:*
مدل‌های غیرضروری حذف شدند و سیستم ساده‌تر شد.

🗑️ *فایل‌های حذف شده:*
• `apps/meet/models.py` - مدل‌های غیرضروری
• `apps/meet/serializers.py` - سریالایزرهای غیرضروری
• `apps/meet/views.py` - ویوهای غیرضروری
• `apps/meet/urls.py` - URL های غیرضروری
• `apps/meet/admin.py` - پنل مدیریت غیرضروری
• `apps/meet/migrations/` - migration های غیرضروری

📁 *فایل‌های باقی‌مانده:*
• `apps/meet/jwt_utils.py` - ابزارهای تولید JWT
• `apps/meet/apps.py` - پیکربندی اپلیکیشن
• `sso/views.py` - اصلاح شده برای meet
• `scripts/create_meet_client.py` - ایجاد کلاینت
• `scripts/setup_meet_production.py` - راه‌اندازی production
• `test_meet_jwt_only.py` - تست ساده JWT

🎯 *مزایای تغییرات:*
• سادگی بیشتر
• کارایی بهتر
• انعطاف‌پذیری بیشتر
• نگهداری آسان‌تر

🔄 *جریان SSO (بدون تغییر):*
1. کاربر روی meet.avinoo.ir/roomname کلیک می‌کند
2. هدایت به auth.avinoo.ir/login
3. بررسی دسترسی از طریق API خارجی
4. تولید JWT token
5. هدایت به meet.avinoo.ir/roomname?jwt=TOKEN

✅ *تست‌های انجام شده:*
تمام تست‌ها با موفقیت انجام شد.

🎉 *نتیجه:* سیستم ساده‌تر و کارآمدتر شد!

---
📅 تهیه شده: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

    return send_telegram_message(report)

if __name__ == '__main__':
    print("📤 ارسال گزارش به‌روزرسانی به تلگرام...")
    if send_update_report():
        print("🎉 گزارش با موفقیت ارسال شد!")
    else:
        print("❌ خطا در ارسال گزارش!")
