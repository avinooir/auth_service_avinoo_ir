#!/bin/bash

# Bash script to run GUID migration fix
# اسکریپت Bash برای اجرای حل مشکل مایگریشن GUID

echo "================================================"
echo "GUID Migration Fix for Russian Server"
echo "حل مشکل مایگریشن GUID برای سرور روسی"
echo "================================================"

# بررسی وجود Python
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "Error: Python not found. Please install Python first."
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "Using Python: $($PYTHON_CMD --version)"

# بررسی وجود فایل اسکریپت
if [ ! -f "fix_guid_migration_ru.py" ]; then
    echo "Error: fix_guid_migration_ru.py not found!"
    exit 1
fi

# بررسی وجود virtual environment
if [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
elif [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "No virtual environment found. Using system Python."
fi

# اجرای اسکریپت
echo "Running GUID migration fix..."
echo "اجرای حل مشکل مایگریشن GUID..."

$PYTHON_CMD fix_guid_migration_ru.py

if [ $? -eq 0 ]; then
    echo "================================================"
    echo "✅ GUID Migration Fix Completed Successfully!"
    echo "✅ حل مشکل مایگریشن GUID با موفقیت تکمیل شد!"
    echo "================================================"
    
    # نمایش لاگ
    if [ -f "guid_migration_fix.log" ]; then
        echo ""
        echo "Log file created: guid_migration_fix.log"
        echo "فایل لاگ ایجاد شد: guid_migration_fix.log"
    fi
    
else
    echo "================================================"
    echo "❌ GUID Migration Fix Failed!"
    echo "❌ حل مشکل مایگریشن GUID ناموفق بود!"
    echo "================================================"
    exit 1
fi
