@echo off
echo ========================================
echo 🔍 AZURE ADMIN LIMITATION DIAGNOSTIC
echo ========================================
echo For L.I.F.E Platform Deployment Planning
echo.

echo [STEP 1] Current Azure Account Information...
echo.
az account show --query "{name:name, id:id, tenantId:tenantId, state:state, user:user.name}" --output table

echo.
echo [STEP 2] Your Role Assignments...
echo.
echo Checking your permissions across subscription...
az role assignment list --assignee %USERNAME% --output table 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Checking with current user context...
    az role assignment list --assignee $(az account show --query user.name -o tsv) --output table 2>nul
)

echo.
echo [STEP 3] Resource Provider Status...
echo.
echo Checking required providers for L.I.F.E Platform:
az provider list --query "[?namespace=='Microsoft.Web' || namespace=='Microsoft.Storage' || namespace=='Microsoft.MarketplaceOrdering'].{Namespace:namespace, State:registrationState}" --output table

echo.
echo [STEP 4] Available Resource Groups...
echo.
echo Resource groups you can access:
az group list --query "[].{Name:name, Location:location, ManagedBy:managedBy}" --output table

echo.
echo [STEP 5] Testing Resource Creation Permissions...
echo.
echo Testing if you can create resource groups:
az group create --name test-life-permissions --location "East US 2" --dry-run 2>temp_error.txt
if %ERRORLEVEL% EQU 0 (
    echo ✅ Resource Group Creation: ALLOWED
) else (
    echo ❌ Resource Group Creation: BLOCKED
    echo Error details:
    type temp_error.txt
)

echo.
echo Testing if you can create App Services:
az webapp create --name test-life-app --resource-group test-rg --plan test-plan --dry-run 2>temp_error2.txt
if %ERRORLEVEL% EQU 0 (
    echo ✅ App Service Creation: ALLOWED
) else (
    echo ❌ App Service Creation: BLOCKED or REQUIRES EXISTING RG
    echo Error details:
    type temp_error2.txt 2>nul
)

echo.
echo [STEP 6] Subscription Quotas and Limits...
echo.
echo Current resource usage:
az vm list-usage --location "East US 2" --query "[?contains(localName, 'App') || contains(localName, 'Web')].{Resource:localName, Current:currentValue, Limit:limit}" --output table 2>nul

echo.
echo [STEP 7] Available Regions...
echo.
echo Regions available to you:
az account list-locations --query "[].{Name:name, DisplayName:displayName}" --output table

echo.
echo [STEP 8] L.I.F.E Platform Deployment Options...
echo.

echo Testing Static Web Apps capability:
az staticwebapp list --output table 2>nul
if %ERRORLEVEL% EQU 0 (
    echo ✅ Static Web Apps: Available
    echo 🎯 RECOMMENDATION: Use Azure Static Web Apps for L.I.F.E Platform
) else (
    echo ❌ Static Web Apps: Not available or blocked
)

echo.
echo Testing App Service capability:
az webapp list --output table 2>nul
if %ERRORLEVEL% EQU 0 (
    echo ✅ App Service: Available  
    echo 🎯 ALTERNATIVE: Use Azure App Service for L.I.F.E Platform
) else (
    echo ❌ App Service: Not available or blocked
)

echo.
echo ========================================
echo 📊 DIAGNOSTIC SUMMARY
echo ========================================
echo.

if exist temp_error.txt (
    echo ⚠️  LIMITATIONS DETECTED:
    echo.
    echo Primary Constraint: Resource Group Creation Blocked
    echo Impact: Cannot create new resources, must use existing
    echo Workaround: Deploy to existing resource groups
    echo.
    del temp_error.txt
)

if exist temp_error2.txt (
    del temp_error2.txt
)

echo 🎯 L.I.F.E PLATFORM DEPLOYMENT STRATEGY:
echo.
echo Based on your permissions, here are your options:
echo.
echo [OPTION 1] Deploy to Existing Resource Group
echo   • Use: Existing RG from list above
echo   • Service: Azure Static Web Apps (if available)
echo   • Command: az staticwebapp create --resource-group [EXISTING-RG]
echo.
echo [OPTION 2] Request Specific Permission
echo   • Ask for: Static Web Apps creation rights
echo   • Scope: Single resource group
echo   • Justification: $345K Q4 2025 revenue target
echo.
echo [OPTION 3] Alternative Deployment
echo   • GitHub Pages (free, no Azure permissions needed)
echo   • Vercel (free static hosting)
echo   • Local demonstration until permissions granted
echo.

echo 📞 NEXT STEPS:
echo 1. Choose deployment option based on available permissions
echo 2. If blocked, escalate with specific error messages above
echo 3. Run: DEPLOY_WITH_LIMITED_PERMISSIONS.bat (coming next)
echo.

echo 💡 KEY INSIGHT:
echo Your L.I.F.E Platform is READY - we just need to work within
echo your Azure constraints to get it deployed and generating revenue!
echo.
pause