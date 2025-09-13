# PowerShell script to run GUID migration fix
# اسکریپت PowerShell برای اجرای حل مشکل مایگریشن GUID

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "GUID Migration Fix for Russian Server" -ForegroundColor Cyan
Write-Host "حل مشکل مایگریشن GUID برای سرور روسی" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

# بررسی وجود Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Python not found. Please install Python first." -ForegroundColor Red
    exit 1
}

# بررسی وجود فایل اسکریپت
if (-not (Test-Path "fix_guid_migration_ru.py")) {
    Write-Host "Error: fix_guid_migration_ru.py not found!" -ForegroundColor Red
    exit 1
}

# بررسی وجود virtual environment
if (Test-Path ".venv") {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & .venv\Scripts\Activate.ps1
} elseif (Test-Path "venv") {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & venv\Scripts\Activate.ps1
} else {
    Write-Host "No virtual environment found. Using system Python." -ForegroundColor Yellow
}

# اجرای اسکریپت
Write-Host "Running GUID migration fix..." -ForegroundColor Yellow
Write-Host "اجرای حل مشکل مایگریشن GUID..." -ForegroundColor Yellow

try {
    python fix_guid_migration_ru.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "================================================" -ForegroundColor Green
        Write-Host "✅ GUID Migration Fix Completed Successfully!" -ForegroundColor Green
        Write-Host "✅ حل مشکل مایگریشن GUID با موفقیت تکمیل شد!" -ForegroundColor Green
        Write-Host "================================================" -ForegroundColor Green
        
        # نمایش لاگ
        if (Test-Path "guid_migration_fix.log") {
            Write-Host "`nLog file created: guid_migration_fix.log" -ForegroundColor Cyan
            Write-Host "فایل لاگ ایجاد شد: guid_migration_fix.log" -ForegroundColor Cyan
        }
        
    } else {
        Write-Host "================================================" -ForegroundColor Red
        Write-Host "❌ GUID Migration Fix Failed!" -ForegroundColor Red
        Write-Host "❌ حل مشکل مایگریشن GUID ناموفق بود!" -ForegroundColor Red
        Write-Host "================================================" -ForegroundColor Red
    }
    
} catch {
    Write-Host "Error running script: $_" -ForegroundColor Red
    exit 1
}

# انتظار برای فشردن کلید
Write-Host "`nPress any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
