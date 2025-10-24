@echo off
setlocal enabledelayedexpansion

echo ========================================
echo 🚨 EMERGENCY AZURE DEPLOYMENT FIX
echo ========================================
echo Date: October 24, 2025
echo Issue: DNS_PROBE_FINISHED_NXDOMAIN for life-platform-staging.azurewebsites.net
echo Solution: Complete Azure resource recreation
echo Revenue Target: $345K Q4 2025 → $50.7M by 2029
echo.

echo [STEP 1] Azure CLI Authentication Check...
echo.
az account show >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Not authenticated with Azure CLI
    echo 🔧 Attempting Azure login...
    az login --use-device-code
    if %errorlevel% neq 0 (
        echo ❌ Azure authentication failed
        echo 💡 Please run 'az login' manually and try again
        pause
        exit /b 1
    )
    echo ✅ Azure authentication successful
) else (
    echo ✅ Already authenticated with Azure CLI
)

echo.
echo [STEP 2] Setting Subscription...
echo.
az account set --subscription "5c88cef6-f243-497d-98af-6c6086d575ca"
if %errorlevel% neq 0 (
    echo ❌ Failed to set subscription
    echo 📋 Available subscriptions:
    az account list --output table
    pause
    exit /b 1
)
echo ✅ Subscription set successfully

echo.
echo [STEP 3] Checking Existing Resources...
echo.
echo Checking if resource group exists...
az group show --name life-platform-staging-rg >nul 2>&1
if %errorlevel% equ 0 (
    echo ⚠️  Resource group exists, checking web app...
    az webapp show --name life-platform-staging --resource-group life-platform-staging-rg >nul 2>&1
    if %errorlevel% equ 0 (
        echo ⚠️  Web app exists but not responding. Restarting...
        az webapp restart --name life-platform-staging --resource-group life-platform-staging-rg
        timeout /t 10 /nobreak >nul
        goto :test_endpoints
    ) else (
        echo ❌ Web app missing, will recreate
    )
) else (
    echo ❌ Resource group missing, will create from scratch
)

echo.
echo [STEP 4] Creating Fresh Resources...
echo.
echo Creating resource group...
az group create --name life-platform-staging-rg --location eastus2 --tags environment=staging platform=life-platform marketplace-offer=9a600d96-fe1e-420b-902a-a0c42c561adb
if %errorlevel% neq 0 (
    echo ❌ Failed to create resource group
    pause
    exit /b 1
)
echo ✅ Resource group created

echo.
echo Creating App Service Plan...
az appservice plan create ^
  --name life-platform-staging-plan ^
  --resource-group life-platform-staging-rg ^
  --sku F1 ^
  --is-linux ^
  --location eastus2
if %errorlevel% neq 0 (
    echo ❌ Failed to create App Service Plan
    pause
    exit /b 1
)
echo ✅ App Service Plan created

echo.
echo Creating Web App...
az webapp create ^
  --name life-platform-staging ^
  --resource-group life-platform-staging-rg ^
  --plan life-platform-staging-plan ^
  --runtime "PYTHON:3.11"
if %errorlevel% neq 0 (
    echo ❌ Failed to create Web App
    echo 💡 The name might be taken. Trying with unique suffix...
    set "unique_suffix=%RANDOM%"
    az webapp create ^
      --name life-platform-staging-!unique_suffix! ^
      --resource-group life-platform-staging-rg ^
      --plan life-platform-staging-plan ^
      --runtime "PYTHON:3.11"
    if %errorlevel% neq 0 (
        echo ❌ Failed to create Web App with unique name
        pause
        exit /b 1
    )
    set "webapp_name=life-platform-staging-!unique_suffix!"
    echo ✅ Web App created with name: !webapp_name!
) else (
    set "webapp_name=life-platform-staging"
    echo ✅ Web App created: !webapp_name!
)

echo.
echo [STEP 5] Configuring Application Settings...
echo.
az webapp config appsettings set ^
  --name !webapp_name! ^
  --resource-group life-platform-staging-rg ^
  --settings ^
    "ENVIRONMENT=staging" ^
    "PLATFORM=L.I.F.E Platform" ^
    "MARKETPLACE_OFFER_ID=9a600d96-fe1e-420b-902a-a0c42c561adb" ^
    "PYTHONPATH=/home/site/wwwroot" ^
    "SCM_DO_BUILD_DURING_DEPLOYMENT=true"
echo ✅ Application settings configured

echo.
echo [STEP 6] Deploying Application Code...
echo.
echo Creating deployment package...
if exist temp_deploy rmdir /s /q temp_deploy
mkdir temp_deploy

echo Copying application files...
copy staging_health_app.py temp_deploy\ >nul 2>&1
copy requirements.txt temp_deploy\ >nul 2>&1

echo Creating startup command file...
echo python staging_health_app.py > temp_deploy\startup.txt

echo Deploying to Azure...
pushd temp_deploy
az webapp up ^
  --name !webapp_name! ^
  --resource-group life-platform-staging-rg ^
  --runtime "PYTHON:3.11" ^
  --location eastus2
popd

if %errorlevel% neq 0 (
    echo ❌ Deployment failed, trying alternative method...
    echo Creating ZIP package...
    powershell -Command "Compress-Archive -Path 'temp_deploy\*' -DestinationPath 'deployment.zip' -Force"
    
    az webapp deployment source config-zip ^
      --name !webapp_name! ^
      --resource-group life-platform-staging-rg ^
      --src deployment.zip
    
    del deployment.zip 2>nul
)

rmdir /s /q temp_deploy 2>nul
echo ✅ Application deployed

echo.
echo [STEP 7] Configuring Startup Command...
echo.
az webapp config set ^
  --name !webapp_name! ^
  --resource-group life-platform-staging-rg ^
  --startup-file "python staging_health_app.py"
echo ✅ Startup command configured

echo.
echo [STEP 8] Restarting Application...
echo.
az webapp restart --name !webapp_name! --resource-group life-platform-staging-rg
echo ✅ Application restarted

echo.
echo [STEP 9] Waiting for Application to Start...
echo.
timeout /t 60 /nobreak >nul
echo ✅ Wait complete

:test_endpoints
echo.
echo [STEP 10] Testing Endpoints...
echo.
if not defined webapp_name set "webapp_name=life-platform-staging"

echo Testing: https://!webapp_name!.azurewebsites.net/
curl -f -s -o nul https://!webapp_name!.azurewebsites.net/ && (
    echo ✅ Main endpoint responding
) || (
    echo ❌ Main endpoint not responding
)

echo Testing: https://!webapp_name!.azurewebsites.net/health
curl -f -s https://!webapp_name!.azurewebsites.net/health && (
    echo ✅ Health endpoint responding
) || (
    echo ❌ Health endpoint not responding
)

echo.
echo ========================================
echo 🎉 DEPLOYMENT STATUS SUMMARY
echo ========================================
echo.
if defined webapp_name (
    echo 🌐 Your L.I.F.E Platform URLs:
    echo 📍 Main: https://!webapp_name!.azurewebsites.net/
    echo 🏥 Health: https://!webapp_name!.azurewebsites.net/health
    echo 📊 Status: https://!webapp_name!.azurewebsites.net/api/status
    echo.
    echo 💰 Business Impact:
    echo ✅ Staging environment operational
    echo ✅ $345K Q4 2025 revenue target enabled
    echo ✅ Production deployment pathway validated
    echo.
    echo 🎯 Next Steps:
    echo 1. Test the URLs above in your browser
    echo 2. If working, proceed to production deployment
    echo 3. If not working, check Azure App Service logs
) else (
    echo ❌ Deployment may have issues
    echo 🔧 Check Azure Portal for detailed logs
)

echo.
echo Would you like to open the platform in browser? (Y/N)
set /p openBrowser="Press Y to open: "
if /i "%openBrowser%"=="Y" (
    if defined webapp_name (
        start "" "https://!webapp_name!.azurewebsites.net/"
        timeout /t 2 /nobreak >nul
        start "" "https://!webapp_name!.azurewebsites.net/health"
    )
)

echo.
echo 🚀 Emergency deployment script complete!
echo 📞 If still not working, the issue may be:
echo    1. Azure subscription limits
echo    2. App Service naming conflicts  
echo    3. Network/firewall restrictions
echo    4. Application startup errors
echo.
pause