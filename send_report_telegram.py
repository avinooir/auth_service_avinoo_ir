"""
Send report to Telegram
"""

import requests
import os
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

def send_report():
    """Send the report to Telegram"""
    
    # Read the report file
    try:
        with open('Report-02-2025-01-13.md', 'r', encoding='utf-8') as f:
            report_content = f.read()
    except Exception as e:
        print(f"❌ خطا در خواندن فایل گزارش: {e}")
        return False
    
    # Split message if too long (Telegram limit is 4096 characters)
    max_length = 4000
    if len(report_content) > max_length:
        # Split into chunks
        chunks = []
        current_chunk = ""
        
        lines = report_content.split('\n')
        for line in lines:
            if len(current_chunk + line + '\n') > max_length:
                if current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = line + '\n'
                else:
                    # Single line is too long, split it
                    chunks.append(line[:max_length])
                    current_chunk = line[max_length:] + '\n'
            else:
                current_chunk += line + '\n'
        
        if current_chunk:
            chunks.append(current_chunk)
    else:
        chunks = [report_content]
    
    # Send each chunk
    success = True
    for i, chunk in enumerate(chunks):
        if len(chunks) > 1:
            chunk_header = f"📋 گزارش جامع - بخش {i+1}/{len(chunks)}\n\n"
            chunk = chunk_header + chunk
        
        if not send_telegram_message(chunk):
            success = False
            break
    
    return success

if __name__ == '__main__':
    print("📤 ارسال گزارش به تلگرام...")
    if send_report():
        print("🎉 گزارش با موفقیت ارسال شد!")
    else:
        print("❌ خطا در ارسال گزارش!")
