@echo off
echo ========================================
echo 🌐 L.I.F.E PLATFORM - GLOBAL AZURE DEPLOYMENT
echo ========================================
echo.
echo 🎯 OBJECTIVE: Host L.I.F.E Platform globally on Azure
echo    • Clinical Platform (Cambridge-grade)
echo    • AI Platform (Machine Learning Integration)
echo    • Education Platform (K-12 + University)
echo    • Research Platform (Academic Tools)
echo.

echo 📋 DEPLOYMENT OPTIONS:
echo [1] Azure Static Web Apps (Recommended - Global CDN)
echo [2] Azure App Service (Alternative - Web Hosting)
echo [3] Check Authorization Status Only
echo [4] Exit
echo.

set /p choice="Choose deployment option (1-4): "

if "%choice%"=="1" goto static_web_app
if "%choice%"=="2" goto app_service  
if "%choice%"=="3" goto check_auth
if "%choice%"=="4" goto end
goto invalid

:static_web_app
echo.
echo ========================================
echo 🚀 DEPLOYING TO AZURE STATIC WEB APPS
echo ========================================
echo.
echo ✅ Benefits:
echo   • Global CDN for worldwide performance
echo   • Automatic HTTPS and custom domains
echo   • Perfect for HTML/JavaScript platforms
echo   • Cost-effective (Free tier available)
echo.
call DEPLOY_AZURE_STATIC_WEB_APP.bat
goto end

:app_service
echo.
echo ========================================
echo 🌐 DEPLOYING TO AZURE APP SERVICE
echo ========================================
echo.
echo ✅ Benefits:
echo   • Traditional web hosting
echo   • Good compatibility
echo   • Reliable deployment
echo   • Global accessibility
echo.
call DEPLOY_AZURE_APP_SERVICE.bat
goto end

:check_auth
echo.
echo ========================================
echo 🔍 CHECKING AZURE AUTHORIZATION STATUS
echo ========================================
echo.

echo [1] Current Azure Login:
az account show --query "{name:name, id:id, tenantId:tenantId}" --output table

echo.
echo [2] Resource Group Permissions:
az group list --query "[].{Name:name, Location:location}" --output table

echo.
echo [3] Static Web Apps Provider:
az provider show --namespace Microsoft.Web --query "{namespace:namespace, registrationState:registrationState}" --output table

echo.
echo [4] Testing Resource Creation:
echo Checking if we can create resources...
az group create --name test-permissions-check --location "East US 2" --dry-run 2>nul
if %ERRORLEVEL% EQU 0 (
    echo ✅ Resource creation permissions: GRANTED
) else (
    echo ❌ Resource creation permissions: DENIED or LIMITED
    echo.
    echo 💡 SOLUTION:
    echo    Contact Azure Administrator to request:
    echo    • Contributor role for resource creation
    echo    • Static Web Apps deployment permissions
    echo    • App Service deployment permissions
)

echo.
echo ========================================
echo AUTHORIZATION CHECK COMPLETE
echo ========================================
pause
goto end

:invalid
echo.
echo ❌ Invalid choice. Please select 1-4.
echo.
pause
goto end

:end
echo.
echo 🎯 L.I.F.E PLATFORM GLOBAL DEPLOYMENT TOOL
echo.
echo Current Status:
echo • Local Platforms: ✅ Working (HTML files)
echo • Azure Hosting: ⏳ Deployment in progress
echo • Global Access: 🎯 Target achieved when deployed
echo.
echo 📞 Support: Azure Administrator for permissions
echo 🎉 Objective: $345K Q4 2025 → $50.7M by 2029
echo.
pause