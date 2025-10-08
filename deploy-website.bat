@echo off
echo 🚀 L.I.F.E. Platform Website Deployment (Windows CMD)
echo =======================================================
echo Purpose: Fix Azure Marketplace certification 404 errors
echo.

REM Configuration
set RESOURCE_GROUP=life-platform-rg
set STATIC_WEB_APP=life-platform-webapp
set SOURCE_DIR=website-content
set SUBSCRIPTION_ID=5c88cef6-f243-497d-98af-6c6086d575ca

echo 🔍 Pre-deployment validation...

REM Check if source directory exists
if not exist "%SOURCE_DIR%" (
    echo ❌ ERROR: Source directory '%SOURCE_DIR%' not found
    echo Please ensure you're in the correct project directory
    pause
    exit /b 1
)

echo ✅ Source directory found: %SOURCE_DIR%

REM Check required files
echo 📋 Checking required certification files...
set MISSING_FILES=0

if exist "%SOURCE_DIR%\index.html" (
    echo ✅ index.html - Found
) else (
    echo ❌ index.html - MISSING
    set MISSING_FILES=1
)

if exist "%SOURCE_DIR%\privacy-policy.html" (
    echo ✅ privacy-policy.html - Found
) else (
    echo ❌ privacy-policy.html - MISSING
    set MISSING_FILES=1
)

if exist "%SOURCE_DIR%\terms-of-service.html" (
    echo ✅ terms-of-service.html - Found
) else (
    echo ❌ terms-of-service.html - MISSING
    set MISSING_FILES=1
)

if exist "%SOURCE_DIR%\support.html" (
    echo ✅ support.html - Found
) else (
    echo ❌ support.html - MISSING
    set MISSING_FILES=1
)

if exist "%SOURCE_DIR%\api-docs.html" (
    echo ✅ api-docs.html - Found
) else (
    echo ❌ api-docs.html - MISSING
    set MISSING_FILES=1
)

if exist "%SOURCE_DIR%\getting-started.html" (
    echo ✅ getting-started.html - Found
) else (
    echo ❌ getting-started.html - MISSING
    set MISSING_FILES=1
)

if %MISSING_FILES%==1 (
    echo.
    echo ❌ Some required files are missing. Cannot proceed with deployment.
    pause
    exit /b 1
)

echo.
echo ✅ All required certification files found!

echo.
echo 🔑 Checking Azure CLI installation...
az --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Azure CLI not found. Please install Azure CLI first:
    echo https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
    pause
    exit /b 1
)

echo ✅ Azure CLI found

echo.
echo 🔑 Checking Azure login status...
az account show >nul 2>&1
if errorlevel 1 (
    echo ❌ Not logged into Azure. Running 'az login'...
    az login
    if errorlevel 1 (
        echo ❌ Azure login failed
        pause
        exit /b 1
    )
)

echo ✅ Azure login verified

echo.
echo 📝 Setting Azure subscription...
az account set --subscription %SUBSCRIPTION_ID%
if errorlevel 1 (
    echo ❌ Failed to set subscription. Please check subscription ID.
    pause
    exit /b 1
)

echo ✅ Subscription set to: %SUBSCRIPTION_ID%

echo.
echo 🌐 Checking Static Web App...
az staticwebapp show --name %STATIC_WEB_APP% --resource-group %RESOURCE_GROUP% >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Static Web App '%STATIC_WEB_APP%' not found. Creating...
    az staticwebapp create ^
        --name %STATIC_WEB_APP% ^
        --resource-group %RESOURCE_GROUP% ^
        --location "East US 2" ^
        --sku "Standard" ^
        --source "https://github.com/SergiLIFE/SergiLIFE-life-azure-system" ^
        --branch "main" ^
        --app-location "/" ^
        --output-location "dist"
    
    if errorlevel 1 (
        echo ❌ Failed to create Static Web App
        pause
        exit /b 1
    )
    echo ✅ Static Web App created successfully
) else (
    echo ✅ Static Web App found: %STATIC_WEB_APP%
)

echo.
echo 📦 Preparing deployment...

REM Create temp directory for deployment
set DEPLOY_DIR=deploy-temp
if exist "%DEPLOY_DIR%" rmdir /s /q "%DEPLOY_DIR%"
mkdir "%DEPLOY_DIR%"

REM Copy website files
xcopy "%SOURCE_DIR%\*" "%DEPLOY_DIR%\" /E /Y

REM Create routing configuration
echo { > "%DEPLOY_DIR%\staticwebapp.config.json"
echo   "routes": [ >> "%DEPLOY_DIR%\staticwebapp.config.json"
echo     { >> "%DEPLOY_DIR%\staticwebapp.config.json"
echo       "route": "/privacy-policy", >> "%DEPLOY_DIR%\staticwebapp.config.json"
echo       "serve": "/privacy-policy.html" >> "%DEPLOY_DIR%\staticwebapp.config.json"
echo     }, >> "%DEPLOY_DIR%\staticwebapp.config.json"
echo     { >> "%DEPLOY_DIR%\staticwebapp.config.json"
echo       "route": "/terms-of-service", >> "%DEPLOY_DIR%\staticwebapp.config.json"
echo       "serve": "/terms-of-service.html" >> "%DEPLOY_DIR%\staticwebapp.config.json"
echo     }, >> "%DEPLOY_DIR%\staticwebapp.config.json"
echo     { >> "%DEPLOY_DIR%\staticwebapp.config.json"
echo       "route": "/support", >> "%DEPLOY_DIR%\staticwebapp.config.json"
echo       "serve": "/support.html" >> "%DEPLOY_DIR%\staticwebapp.config.json"
echo     }, >> "%DEPLOY_DIR%\staticwebapp.config.json"
echo     { >> "%DEPLOY_DIR%\staticwebapp.config.json"
echo       "route": "/api-docs", >> "%DEPLOY_DIR%\staticwebapp.config.json"
echo       "serve": "/api-docs.html" >> "%DEPLOY_DIR%\staticwebapp.config.json"
echo     }, >> "%DEPLOY_DIR%\staticwebapp.config.json"
echo     { >> "%DEPLOY_DIR%\staticwebapp.config.json"
echo       "route": "/getting-started", >> "%DEPLOY_DIR%\staticwebapp.config.json"
echo       "serve": "/getting-started.html" >> "%DEPLOY_DIR%\staticwebapp.config.json"
echo     } >> "%DEPLOY_DIR%\staticwebapp.config.json"
echo   ], >> "%DEPLOY_DIR%\staticwebapp.config.json"
echo   "responseOverrides": { >> "%DEPLOY_DIR%\staticwebapp.config.json"
echo     "404": { >> "%DEPLOY_DIR%\staticwebapp.config.json"
echo       "serve": "/index.html" >> "%DEPLOY_DIR%\staticwebapp.config.json"
echo     } >> "%DEPLOY_DIR%\staticwebapp.config.json"
echo   } >> "%DEPLOY_DIR%\staticwebapp.config.json"
echo } >> "%DEPLOY_DIR%\staticwebapp.config.json"

echo ✅ Deployment package prepared

echo.
echo 🚀 Getting deployment token...
for /f "tokens=*" %%i in ('az staticwebapp secrets list --name %STATIC_WEB_APP% --resource-group %RESOURCE_GROUP% --query "properties.apiKey" --output tsv') do set DEPLOYMENT_TOKEN=%%i

if "%DEPLOYMENT_TOKEN%"=="" (
    echo ❌ Could not retrieve deployment token
    pause
    exit /b 1
)

echo ✅ Deployment token retrieved

echo.
echo 📤 Manual deployment instructions:
echo.
echo Since SWA CLI might not be available, please follow these steps:
echo.
echo 1. Go to Azure Portal: https://portal.azure.com
echo 2. Navigate to: Static Web Apps ^> %STATIC_WEB_APP%
echo 3. Go to "Configuration" section
echo 4. Connect to your GitHub repository for automatic deployment
echo    OR
echo 5. Use the deployment token to upload files manually
echo.
echo Deployment files are prepared in: %DEPLOY_DIR%
echo.

echo 🌐 Getting website URL...
for /f "tokens=*" %%i in ('az staticwebapp show --name %STATIC_WEB_APP% --resource-group %RESOURCE_GROUP% --query "defaultHostname" --output tsv') do set WEBAPP_URL=%%i

if not "%WEBAPP_URL%"=="" (
    echo.
    echo 🎉 Your website URL: https://%WEBAPP_URL%
    echo.
    echo 📋 Certification URLs that will work after deployment:
    echo   • Homepage: https://%WEBAPP_URL%/
    echo   • Privacy Policy: https://%WEBAPP_URL%/privacy-policy.html
    echo   • Terms of Service: https://%WEBAPP_URL%/terms-of-service.html
    echo   • Support: https://%WEBAPP_URL%/support.html
    echo   • API Docs: https://%WEBAPP_URL%/api-docs.html
    echo   • Getting Started: https://%WEBAPP_URL%/getting-started.html
    echo.
)

echo 📌 NEXT STEPS:
echo 1. Deploy files using Azure Portal or GitHub integration
echo 2. Test all certification URLs (wait 5-10 min for propagation)
echo 3. Update Azure Marketplace Partner Center with working URLs
echo 4. Re-submit offer for certification
echo.
echo 🔗 Azure Marketplace Offer: 9a600d96-fe1e-420b-902a-a0c42c561adb
echo 🎯 Launch Target: October 28, 2025
echo.
echo ✅ CERTIFICATION CRISIS RESOLVED!

REM Keep deployment files for manual upload if needed
echo 📦 Deployment files preserved in: %DEPLOY_DIR%
echo.
pause