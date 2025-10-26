@echo off
echo ========================================
echo 🔍 AZURE DEPLOYMENT DIAGNOSTIC
echo ========================================
echo Checking why life-platform-staging.azurewebsites.net is not accessible
echo DNS_PROBE_FINISHED_NXDOMAIN troubleshooting
echo.

echo [CHECK 1] Azure CLI Authentication Status
az account show --output table 2>nul
if %errorlevel% neq 0 (
    echo ❌ Not authenticated with Azure CLI
    echo 🔧 Logging in now...
    az login
) else (
    echo ✅ Authenticated with Azure CLI
)

echo.
echo [CHECK 2] Azure Subscription Resources  
echo Looking for life-platform resources...
az group list --output table --query "[?contains(name, 'life')]" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Failed to list resource groups
) else (
    echo ✅ Resource groups listed above
)

echo.
echo [CHECK 3] Checking Specific Web App
az webapp show --name life-platform-staging --resource-group life-platform-staging-rg --output table 2>nul
if %errorlevel% neq 0 (
    echo ❌ life-platform-staging web app does NOT exist
    echo 💡 This confirms the DNS error - the resource was never created
) else (
    echo ✅ life-platform-staging web app exists
)

echo.
echo [CHECK 4] Alternative: Check if any L.I.F.E web apps exist
echo Looking for web apps with 'life' in the name...
az webapp list --output table --query "[?contains(name, 'life')]" 2>nul

echo.
echo [CHECK 5] Network Connectivity Test
echo Testing if azurewebsites.net domain is reachable...
ping -n 2 microsoft.com >nul
if %errorlevel% equ 0 (
    echo ✅ Internet connectivity working
) else (
    echo ❌ Network connectivity issues
)

echo.
echo Testing Azure domain resolution...
nslookup google.azurewebsites.net >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Azure domain resolution working
) else (
    echo ❌ Azure domain resolution issues
)

echo.
echo ========================================
echo 🚨 DIAGNOSIS COMPLETE
echo ========================================
echo.
echo 💡 LIKELY CAUSE:
echo The Azure Web App 'life-platform-staging' was never successfully created.
echo Previous deployment commands failed silently.
echo.
echo 🔧 SOLUTION:
echo Run the emergency deployment script to create resources:
echo    EMERGENCY_AZURE_FIX.bat
echo OR
echo    powershell -ExecutionPolicy Bypass -File EMERGENCY_AZURE_FIX.ps1
echo.
echo 📋 WHAT WILL HAPPEN:
echo 1. Create new resource group: life-platform-staging-rg
echo 2. Create App Service Plan with F1 (Free) tier
echo 3. Create Web App with unique name (may include timestamp)
echo 4. Deploy staging_health_app.py application
echo 5. Configure proper startup and environment settings
echo.
echo 💰 BUSINESS IMPACT:
echo This is blocking the $345K Q4 2025 revenue target.
echo Staging deployment validates production readiness.
echo.
pause