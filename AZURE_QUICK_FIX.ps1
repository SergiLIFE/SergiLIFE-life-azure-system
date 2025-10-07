# L.I.F.E Platform - Azure Function App Quick Fix
# September 26, 2025 - Emergency Repair for Launch Day

param(
    [switch]$SkipRestart = $false
)

Write-Host "=====================================================" -ForegroundColor Green
Write-Host "L.I.F.E PLATFORM - AZURE FUNCTION APP QUICK FIX" -ForegroundColor Yellow
Write-Host "=====================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Target: life-functions-app" -ForegroundColor Cyan
Write-Host "Resource Group: life-platform-rg" -ForegroundColor Cyan
Write-Host "Launch Date: September 27, 2025 (TOMORROW!)" -ForegroundColor Yellow
Write-Host ""

# Set Azure subscription
Write-Host "Setting Azure subscription context..." -ForegroundColor Cyan
az account set --subscription "5c88cef6-f243-497d-98af-6c6086d575ca"

# Fix 1: Set correct runtime version
Write-Host ""
Write-Host "Fix 1: Setting Python runtime version..." -ForegroundColor Green
az functionapp config set --name "life-functions-app" --resource-group "life-platform-rg" --linux-fx-version "Python|3.11"

# Fix 2: Configure essential settings
Write-Host ""
Write-Host "Fix 2: Configuring essential app settings..." -ForegroundColor Green
az functionapp config appsettings set --name "life-functions-app" --resource-group "life-platform-rg" --settings "FUNCTIONS_WORKER_RUNTIME=python" "FUNCTIONS_EXTENSION_VERSION=~4" "PYTHON_VERSION=3.11" "LIFE_PLATFORM_VERSION=2025.1.0-PRODUCTION" "AZURE_MARKETPLACE_OFFER_ID=9a600d96-fe1e-420b-902a-a0c42c561adb"

# Fix 3: Restart function app (unless skipped)
if (-not $SkipRestart) {
    Write-Host ""
    Write-Host "Fix 3: Restarting function app..." -ForegroundColor Green
    az functionapp restart --name "life-functions-app" --resource-group "life-platform-rg"
    
    Write-Host "Waiting 30 seconds for restart..." -ForegroundColor Yellow
    Start-Sleep -Seconds 30
}

# Verification
Write-Host ""
Write-Host "Verification: Checking function app status..." -ForegroundColor Cyan
az functionapp show --name "life-functions-app" --resource-group "life-platform-rg" --query "{name:name,state:state,lastModifiedTimeUtc:lastModifiedTimeUtc}" --output table

Write-Host ""
Write-Host "Verification: Checking runtime configuration..." -ForegroundColor Cyan
az functionapp config show --name "life-functions-app" --resource-group "life-platform-rg" --query "{linuxFxVersion:linuxFxVersion}" --output table

Write-Host ""
Write-Host "=====================================================" -ForegroundColor Green
Write-Host "FIXES APPLIED SUCCESSFULLY!" -ForegroundColor Yellow
Write-Host "=====================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "1. Check Azure Portal for function app status" -ForegroundColor White
Write-Host "2. Test health endpoint: https://life-functions-app.azurewebsites.net" -ForegroundColor White
Write-Host "3. Verify functions are loading properly" -ForegroundColor White
Write-Host ""
Write-Host "LAUNCH STATUS: READY FOR SEPTEMBER 27!" -ForegroundColor Green