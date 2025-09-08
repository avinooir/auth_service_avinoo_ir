# =============================================================================
# اسکریپت نصب سیستم SSO روی Windows
# =============================================================================

# تنظیمات
$ErrorActionPreference = "Stop"

# Colors for output
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

function Write-Status {
    param([string]$Message)
    Write-ColorOutput "[INFO] $Message" "Cyan"
}

function Write-Success {
    param([string]$Message)
    Write-ColorOutput "[SUCCESS] $Message" "Green"
}

function Write-Warning {
    param([string]$Message)
    Write-ColorOutput "[WARNING] $Message" "Yellow"
}

function Write-Error {
    param([string]$Message)
    Write-ColorOutput "[ERROR] $Message" "Red"
}

# =============================================================================
# شروع اسکریپت
# =============================================================================

Write-ColorOutput "==========================================" "Magenta"
Write-ColorOutput "🚀 نصب سیستم SSO روی Windows" "Magenta"
Write-ColorOutput "==========================================" "Magenta"
Write-Host ""

# Get project directory
$PROJECT_DIR = Get-Location
Write-Status "مسیر پروژه: $PROJECT_DIR"

# Check if we're in the right directory
if (-not (Test-Path "manage.py")) {
    Write-Error "فایل manage.py یافت نشد!"
    Write-Warning "لطفاً در مسیر اصلی پروژه SSO باشید."
    exit 1
}

# =============================================================================
# بررسی و نصب Python
# =============================================================================

Write-Status "بررسی Python..."

try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Python نصب است: $pythonVersion"
    } else {
        throw "Python نصب نیست"
    }
} catch {
    Write-Error "Python نصب نیست!"
    Write-Warning "لطفاً Python 3.9 یا بالاتر را از https://python.org دانلود و نصب کنید."
    Write-Warning "در هنگام نصب، گزینه 'Add Python to PATH' را فعال کنید."
    exit 1
}

# Check Python version
$version = python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
Write-Status "نسخه Python: $version"

if ([float]$version -lt 3.9) {
    Write-Error "Python 3.9 یا بالاتر مورد نیاز است!"
    exit 1
}

# =============================================================================
# ایجاد Virtual Environment
# =============================================================================

Write-Status "ایجاد Virtual Environment..."

if (Test-Path "venv") {
    Write-Warning "Virtual Environment موجود است."
    $response = Read-Host "آیا می‌خواهید آن را حذف و دوباره ایجاد کنید؟ (y/n)"
    if ($response -eq "y" -or $response -eq "Y") {
        Remove-Item -Recurse -Force "venv"
        Write-Status "Virtual Environment قدیمی حذف شد."
    } else {
        Write-Status "استفاده از Virtual Environment موجود..."
    }
}

if (-not (Test-Path "venv")) {
    python -m venv venv
    Write-Success "Virtual Environment ایجاد شد"
}

# Activate virtual environment
& ".\venv\Scripts\Activate.ps1"
Write-Success "Virtual Environment فعال شد"

# Upgrade pip
Write-Status "به‌روزرسانی pip..."
python -m pip install --upgrade pip

# =============================================================================
# نصب Dependencies
# =============================================================================

Write-Status "نصب Dependencies..."

if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
    Write-Success "Dependencies نصب شدند"
} else {
    Write-Error "فایل requirements.txt یافت نشد!"
    exit 1
}

# =============================================================================
# تنظیمات Environment
# =============================================================================

Write-Status "تنظیمات Environment..."

if (-not (Test-Path ".env")) {
    if (Test-Path "env.example") {
        Copy-Item "env.example" ".env"
        Write-Success "فایل .env از env.example ایجاد شد"
    } else {
        Write-Warning "فایل env.example یافت نشد. ایجاد فایل .env..."
        @"
# Django Settings
SECRET_KEY=django-insecure-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Microservice Configuration
AUTH_SERVICE_DOMAIN=127.0.0.1:8000
ALLOWED_CLIENT_DOMAINS=127.0.0.1:8000,localhost:3000

# SSO Configuration
SSO_REDIRECT_URL=http://{domain}/callback
SSO_LOGIN_URL=http://{domain}/login
SSO_LOGOUT_URL=http://{domain}/logout

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=7

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://127.0.0.1:8000

# Logging
LOG_LEVEL=INFO
"@ | Out-File -FilePath ".env" -Encoding UTF8
        Write-Success "فایل .env ایجاد شد"
    }
} else {
    Write-Warning "فایل .env موجود است"
}

# =============================================================================
# تنظیمات Database
# =============================================================================

Write-Status "تنظیمات Database..."
Write-Status "استفاده از SQLite (پیش‌فرض)"

# =============================================================================
# Migration و Setup
# =============================================================================

Write-Status "اجرای Migration..."

# Create logs directory
if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs"
}

# Run migrations
python manage.py makemigrations
python manage.py migrate

Write-Success "Migration ها اجرا شدند"

# =============================================================================
# ایجاد Superuser
# =============================================================================

Write-Status "ایجاد Superuser..."

$response = Read-Host "آیا می‌خواهید Superuser ایجاد کنید؟ (y/n)"
if ($response -eq "y" -or $response -eq "Y") {
    $username = Read-Host "نام کاربری (پیش‌فرض: admin)"
    if ([string]::IsNullOrEmpty($username)) {
        $username = "admin"
    }
    
    $email = Read-Host "ایمیل (پیش‌فرض: admin@example.com)"
    if ([string]::IsNullOrEmpty($email)) {
        $email = "admin@example.com"
    }
    
    Write-Host "رمز عبور را وارد کنید:"
    python manage.py createsuperuser --username $username --email $email
    
    Write-Success "Superuser ایجاد شد"
} else {
    Write-Warning "Superuser ایجاد نشد. می‌توانید بعداً با دستور زیر ایجاد کنید:"
    Write-Warning "python manage.py createsuperuser"
}

# =============================================================================
# ایجاد کلیدهای RSA
# =============================================================================

Write-Status "ایجاد کلیدهای RSA..."

# Create keys directory
if (-not (Test-Path "keys")) {
    New-Item -ItemType Directory -Path "keys"
}

# Generate RSA keys
$pythonScript = @"
from sso.utils import generate_rsa_keys
try:
    generate_rsa_keys()
    print('کلیدهای RSA ایجاد شدند')
except Exception as e:
    print(f'خطا در ایجاد کلیدهای RSA: {e}')
"@

$pythonScript | python

# =============================================================================
# ایجاد Windows Service
# =============================================================================

$response = Read-Host "آیا می‌خواهید Windows Service ایجاد کنید؟ (y/n)"
if ($response -eq "y" -or $response -eq "Y") {
    Write-Status "ایجاد Windows Service..."
    
    # Install NSSM (Non-Sucking Service Manager)
    if (-not (Get-Command "nssm" -ErrorAction SilentlyContinue)) {
        Write-Status "دانلود و نصب NSSM..."
        
        $nssmUrl = "https://nssm.cc/release/nssm-2.24.zip"
        $nssmZip = "nssm.zip"
        $nssmDir = "nssm"
        
        Invoke-WebRequest -Uri $nssmUrl -OutFile $nssmZip
        Expand-Archive -Path $nssmZip -DestinationPath $nssmDir -Force
        
        # Copy NSSM to system32
        $nssmExe = Get-ChildItem -Path $nssmDir -Recurse -Name "nssm.exe" | Select-Object -First 1
        Copy-Item "$nssmDir\$nssmExe" "C:\Windows\System32\nssm.exe"
        
        # Cleanup
        Remove-Item $nssmZip -Force
        Remove-Item $nssmDir -Recurse -Force
        
        Write-Success "NSSM نصب شد"
    }
    
    $serviceName = "SSO-Service"
    $servicePath = $PROJECT_DIR
    $pythonPath = "$servicePath\venv\Scripts\python.exe"
    $scriptPath = "$servicePath\manage.py"
    
    # Create service
    nssm install $serviceName $pythonPath
    nssm set $serviceName Parameters "runserver 0.0.0.0:8000"
    nssm set $serviceName AppDirectory $servicePath
    nssm set $serviceName DisplayName "SSO Authentication Service"
    nssm set $serviceName Description "SSO Authentication Service for microservices"
    nssm set $serviceName Start SERVICE_AUTO_START
    
    Write-Success "Windows Service ایجاد شد"
    Write-Status "برای شروع سرویس: Start-Service $serviceName"
    Write-Status "برای توقف سرویس: Stop-Service $serviceName"
    Write-Status "برای وضعیت سرویس: Get-Service $serviceName"
}

# =============================================================================
# جمع‌آوری Static Files
# =============================================================================

Write-Status "جمع‌آوری Static Files..."

python manage.py collectstatic --noinput

Write-Success "Static Files جمع‌آوری شدند"

# =============================================================================
# تست سیستم
# =============================================================================

Write-Status "تست سیستم..."

# Test database connection
python manage.py check

if ($LASTEXITCODE -eq 0) {
    Write-Success "تست سیستم موفق بود"
} else {
    Write-Error "خطا در تست سیستم!"
    exit 1
}

# =============================================================================
# خلاصه نصب
# =============================================================================

Write-Host ""
Write-ColorOutput "==========================================" "Magenta"
Write-ColorOutput "✅ نصب سیستم SSO تکمیل شد!" "Magenta"
Write-ColorOutput "==========================================" "Magenta"
Write-Host ""
Write-ColorOutput "📁 مسیر پروژه: $PROJECT_DIR" "White"
Write-ColorOutput "🐍 Virtual Environment: $PROJECT_DIR\venv" "White"
Write-ColorOutput "⚙️  تنظیمات: $PROJECT_DIR\.env" "White"
Write-ColorOutput "📊 دیتابیس: SQLite (پیش‌فرض)" "White"
Write-Host ""
Write-ColorOutput "🚀 برای شروع:" "White"
Write-ColorOutput "   cd $PROJECT_DIR" "White"
Write-ColorOutput "   .\venv\Scripts\Activate.ps1" "White"
Write-ColorOutput "   python manage.py runserver" "White"
Write-Host ""
Write-ColorOutput "🌐 آدرس‌های مفید:" "White"
Write-ColorOutput "   - صفحه تست: http://127.0.0.1:8000/test/" "White"
Write-ColorOutput "   - صفحه ورود: http://127.0.0.1:8000/login/" "White"
Write-ColorOutput "   - Admin Panel: http://127.0.0.1:8000/admin/" "White"
Write-Host ""
Write-ColorOutput "📚 مستندات:" "White"
Write-ColorOutput "   - README: $PROJECT_DIR\README_SSO.md" "White"
Write-ColorOutput "   - راهنمای کامل: $PROJECT_DIR\docs\SSO_USAGE.md" "White"
Write-ColorOutput "   - تنظیمات: $PROJECT_DIR\docs\CONFIGURATION.md" "White"
Write-Host ""
Write-ColorOutput "🔧 مدیریت سرویس:" "White"
if (Get-Service "SSO-Service" -ErrorAction SilentlyContinue) {
    Write-ColorOutput "   Start-Service SSO-Service" "White"
    Write-ColorOutput "   Stop-Service SSO-Service" "White"
    Write-ColorOutput "   Get-Service SSO-Service" "White"
}
Write-Host ""
Write-ColorOutput "📝 لاگ‌ها:" "White"
Write-ColorOutput "   Get-Content $PROJECT_DIR\logs\django.log -Tail 20" "White"
Write-Host ""
Write-ColorOutput "==========================================" "Magenta"
Write-Success "نصب کامل شد! 🎉"
Write-ColorOutput "==========================================" "Magenta"
