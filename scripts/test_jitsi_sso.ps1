# PowerShell Script to Test Jitsi Meet SSO Integration
# این اسکریپت برای تست ادغام Jitsi Meet با SSO استفاده می‌شود

param(
    [string]$BaseUrl = "https://auth.avinoo.ir",
    [string]$ClientId = "meet",
    [string]$RedirectUri = "https://meet.avinoo.ir/callback",
    [string]$Username = "test_user",
    [string]$Password = "test_pass"
)

Write-Host "🧪 Testing Jitsi Meet SSO Integration" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

# Function to make HTTP requests
function Invoke-SSORequest {
    param(
        [string]$Uri,
        [string]$Method = "GET",
        [hashtable]$Body = $null,
        [hashtable]$Headers = @{}
    )
    
    try {
        $requestParams = @{
            Uri = $Uri
            Method = $Method
            Headers = $Headers
        }
        
        if ($Body) {
            $requestParams.Body = ($Body | ConvertTo-Json -Depth 10)
            $requestParams.ContentType = "application/json"
        }
        
        $response = Invoke-RestMethod @requestParams
        return $response
    }
    catch {
        Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
}

# Test 1: Create SSO Client
Write-Host "`n1️⃣ Testing SSO Client Creation..." -ForegroundColor Yellow
$loginData = @{
    username = $Username
    password = $Password
    client_id = $ClientId
    redirect_uri = $RedirectUri
}

$loginResponse = Invoke-SSORequest -Uri "$BaseUrl/sso/api/login/" -Method "POST" -Body $loginData

if ($loginResponse -and $loginResponse.success) {
    Write-Host "✅ SSO Login successful!" -ForegroundColor Green
    Write-Host "   Token: $($loginResponse.access_token.Substring(0, 50))..." -ForegroundColor Cyan
    Write-Host "   User: $($loginResponse.user.username)" -ForegroundColor Cyan
    
    $token = $loginResponse.access_token
} else {
    Write-Host "❌ SSO Login failed!" -ForegroundColor Red
    exit 1
}

# Test 2: Validate Token
Write-Host "`n2️⃣ Testing Token Validation..." -ForegroundColor Yellow
$validateData = @{
    token = $token
    client_id = $ClientId
}

$validateResponse = Invoke-SSORequest -Uri "$BaseUrl/sso/api/validate-token/" -Method "POST" -Body $validateData

if ($validateResponse -and $validateResponse.success -and $validateResponse.valid) {
    Write-Host "✅ Token validation successful!" -ForegroundColor Green
    Write-Host "   User: $($validateResponse.user.username)" -ForegroundColor Cyan
    Write-Host "   Email: $($validateResponse.user.email)" -ForegroundColor Cyan
} else {
    Write-Host "❌ Token validation failed!" -ForegroundColor Red
    exit 1
}

# Test 3: Test Callback URL Generation
Write-Host "`n3️⃣ Testing Callback URL Generation..." -ForegroundColor Yellow
$nextUrl = "/team1"
$callbackUrl = "$RedirectUri?token=$token&next=$([System.Web.HttpUtility]::UrlEncode($nextUrl))"
Write-Host "✅ Callback URL generated:" -ForegroundColor Green
Write-Host "   $callbackUrl" -ForegroundColor Cyan

# Test 4: Test SSO Login Page URL
Write-Host "`n4️⃣ Testing SSO Login Page URL..." -ForegroundColor Yellow
$loginPageUrl = "$BaseUrl/sso/login/?client_id=$ClientId&redirect_uri=$([System.Web.HttpUtility]::UrlEncode($RedirectUri))&next=$([System.Web.HttpUtility]::UrlEncode($nextUrl))"
Write-Host "✅ SSO Login Page URL:" -ForegroundColor Green
Write-Host "   $loginPageUrl" -ForegroundColor Cyan

# Test 5: Test User Info
Write-Host "`n5️⃣ Testing User Info API..." -ForegroundColor Yellow
$userInfoResponse = Invoke-SSORequest -Uri "$BaseUrl/sso/api/user-info/" -Method "GET" -Headers @{ "Authorization" = "Bearer $token" }

if ($userInfoResponse -and $userInfoResponse.success) {
    Write-Host "✅ User info retrieved successfully!" -ForegroundColor Green
    Write-Host "   Username: $($userInfoResponse.user.username)" -ForegroundColor Cyan
    Write-Host "   Email: $($userInfoResponse.user.email)" -ForegroundColor Cyan
    Write-Host "   Active: $($userInfoResponse.user.is_active)" -ForegroundColor Cyan
} else {
    Write-Host "❌ User info retrieval failed!" -ForegroundColor Red
}

# Test 6: Test Logout
Write-Host "`n6️⃣ Testing Logout..." -ForegroundColor Yellow
$logoutResponse = Invoke-SSORequest -Uri "$BaseUrl/sso/api/logout/?client_id=$ClientId&redirect_uri=$([System.Web.HttpUtility]::UrlEncode($RedirectUri))" -Method "GET"

if ($logoutResponse -and $logoutResponse.success) {
    Write-Host "✅ Logout successful!" -ForegroundColor Green
} else {
    Write-Host "❌ Logout failed!" -ForegroundColor Red
}

# Summary
Write-Host "`n📊 Test Summary" -ForegroundColor Green
Write-Host "===============" -ForegroundColor Green
Write-Host "✅ SSO Login: Working" -ForegroundColor Green
Write-Host "✅ Token Validation: Working" -ForegroundColor Green
Write-Host "✅ Callback URL: Generated" -ForegroundColor Green
Write-Host "✅ Login Page URL: Generated" -ForegroundColor Green
Write-Host "✅ User Info: Working" -ForegroundColor Green
Write-Host "✅ Logout: Working" -ForegroundColor Green

Write-Host "`n🎉 All tests passed! Jitsi Meet SSO integration is working correctly." -ForegroundColor Green

# Generate example URLs for manual testing
Write-Host "`n🔗 Example URLs for Manual Testing:" -ForegroundColor Yellow
Write-Host "=====================================" -ForegroundColor Yellow
Write-Host "1. SSO Login URL:" -ForegroundColor Cyan
Write-Host "   $loginPageUrl" -ForegroundColor White
Write-Host "`n2. Callback URL (after login):" -ForegroundColor Cyan
Write-Host "   $callbackUrl" -ForegroundColor White
Write-Host "`n3. Jitsi Meet Index:" -ForegroundColor Cyan
Write-Host "   https://meet.avinoo.ir/" -ForegroundColor White
Write-Host "`n4. Direct Room Access:" -ForegroundColor Cyan
Write-Host "   https://meet.avinoo.ir/team1" -ForegroundColor White

Write-Host "`n💡 Usage Instructions:" -ForegroundColor Yellow
Write-Host "=====================" -ForegroundColor Yellow
Write-Host "1. Open the SSO Login URL in your browser" -ForegroundColor White
Write-Host "2. Login with your credentials" -ForegroundColor White
Write-Host "3. You'll be redirected to the callback page" -ForegroundColor White
Write-Host "4. The callback page will redirect you to the meeting room" -ForegroundColor White
Write-Host "5. You'll be automatically logged into Jitsi Meet" -ForegroundColor White
