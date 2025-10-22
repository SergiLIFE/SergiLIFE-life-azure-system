@echo off
echo ========================================
echo 🚀 L.I.F.E PLATFORM - LIMITED PERMISSIONS DEPLOYMENT
echo ========================================
echo Deployment strategy for Azure admins with constraints
echo.

echo [STEP 1] Finding Available Resources...
echo.

echo Listing your accessible resource groups:
az group list --query "[].name" --output table > available_rgs.txt
echo.

echo Available resource groups:
type available_rgs.txt

set /p SELECTED_RG="Enter resource group name to use (or 'new' to create): "

if /i "%SELECTED_RG%"=="new" goto create_rg
goto use_existing_rg

:create_rg
echo.
echo [STEP 2A] Creating New Resource Group...
echo.
set /p NEW_RG_NAME="Enter new resource group name: "
set /p LOCATION="Enter location (default: East US 2): "
if "%LOCATION%"=="" set LOCATION="East US 2"

echo Creating resource group: %NEW_RG_NAME%
az group create --name %NEW_RG_NAME% --location %LOCATION%

if %ERRORLEVEL% EQU 0 (
    set SELECTED_RG=%NEW_RG_NAME%
    echo ✅ Resource group created successfully!
    goto deploy_platform
) else (
    echo ❌ Resource group creation failed!
    echo.
    echo FALLBACK OPTIONS:
    echo 1. Use existing resource group from list above
    echo 2. Request resource group creation permissions
    echo 3. Deploy using alternative method
    goto select_fallback
)

:use_existing_rg
echo.
echo [STEP 2B] Using Existing Resource Group: %SELECTED_RG%
echo.

echo Validating resource group access...
az group show --name %SELECTED_RG% --query "{name:name, location:location}" --output table

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Cannot access resource group: %SELECTED_RG%
    echo Please check the name and try again.
    pause
    exit /b 1
)

goto deploy_platform

:deploy_platform
echo.
echo [STEP 3] Deploying L.I.F.E Platform...
echo.

set STATIC_APP_NAME=life-platform-%RANDOM%
echo Deploying to: %SELECTED_RG%
echo App name: %STATIC_APP_NAME%
echo.

echo Attempting Azure Static Web Apps deployment...
az staticwebapp create ^
  --name %STATIC_APP_NAME% ^
  --resource-group %SELECTED_RG% ^
  --location "East US 2" ^
  --source . ^
  --sku Free

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ SUCCESS! L.I.F.E Platform deployed to Azure!
    echo.
    echo Getting deployment URL...
    az staticwebapp show --name %STATIC_APP_NAME% --resource-group %SELECTED_RG% --query "defaultHostname" --output tsv > deployment_url.txt
    set /p DEPLOYMENT_URL=<deployment_url.txt
    
    echo.
    echo 🌐 L.I.F.E PLATFORM GLOBAL URLS:
    echo ================================
    echo Main Platform: https://%DEPLOYMENT_URL%
    echo Clinical: https://%DEPLOYMENT_URL%/LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html
    echo AI Platform: https://%DEPLOYMENT_URL%/LIFE_AI_PLATFORM_REAL.html
    echo Education: https://%DEPLOYMENT_URL%/LIFE_EDUCATION_PLATFORM_REAL.html
    echo Research: https://%DEPLOYMENT_URL%/LIFE_RESEARCH_PLATFORM_REAL.html
    echo.
    echo 🎉 L.I.F.E Platform is now globally accessible!
    echo.
    echo Opening main platform...
    start https://%DEPLOYMENT_URL%
    
    del deployment_url.txt
    goto success
) else (
    echo ❌ Static Web Apps deployment failed!
    echo Trying App Service deployment as fallback...
    goto try_app_service
)

:try_app_service
echo.
echo [STEP 4] Fallback: App Service Deployment...
echo.

set APP_SERVICE_PLAN=life-plan-%RANDOM%
set WEB_APP_NAME=life-app-%RANDOM%

echo Creating App Service Plan...
az appservice plan create ^
  --name %APP_SERVICE_PLAN% ^
  --resource-group %SELECTED_RG% ^
  --location "East US 2" ^
  --sku FREE

if %ERRORLEVEL% EQU 0 (
    echo Creating Web App...
    az webapp create ^
      --name %WEB_APP_NAME% ^
      --resource-group %SELECTED_RG% ^
      --plan %APP_SERVICE_PLAN%
    
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo Preparing deployment package...
        tar -a -c -f life-platform.zip *.html *.json
        
        echo Deploying L.I.F.E Platform...
        az webapp deployment source config-zip ^
          --resource-group %SELECTED_RG% ^
          --name %WEB_APP_NAME% ^
          --src life-platform.zip
        
        if %ERRORLEVEL% EQU 0 (
            echo.
            echo ✅ SUCCESS! L.I.F.E Platform deployed via App Service!
            echo.
            echo 🌐 L.I.F.E PLATFORM URLs:
            echo Main: https://%WEB_APP_NAME%.azurewebsites.net
            echo.
            echo Opening platform...
            start https://%WEB_APP_NAME%.azurewebsites.net
            
            del life-platform.zip
            goto success
        )
    )
)

echo ❌ App Service deployment also failed!
goto select_fallback

:select_fallback
echo.
echo ========================================
echo 🔄 FALLBACK OPTIONS FOR LIMITED PERMISSIONS
echo ========================================
echo.
echo Your Azure permissions are more limited than expected.
echo Here are alternative deployment strategies:
echo.
echo [1] GitHub Pages (Free, No Azure Permissions Needed)
echo [2] Vercel Static Hosting (Free, Simple Upload)
echo [3] Request Additional Azure Permissions
echo [4] Local Demonstration Mode
echo.

set /p fallback_choice="Select fallback option (1-4): "

if "%fallback_choice%"=="1" goto github_pages
if "%fallback_choice%"=="2" goto vercel_info  
if "%fallback_choice%"=="3" goto permission_request
if "%fallback_choice%"=="4" goto local_demo

:github_pages
echo.
echo 📋 GITHUB PAGES DEPLOYMENT GUIDE:
echo.
echo 1. Push L.I.F.E Platform files to GitHub repository
echo 2. Go to repository Settings → Pages
echo 3. Select source branch (main)
echo 4. Platform will be live at: https://[username].github.io/[repo]
echo.
echo This requires NO Azure permissions and is completely free!
goto end

:vercel_info
echo.
echo 📋 VERCEL DEPLOYMENT GUIDE:
echo.
echo 1. Go to: https://vercel.com
echo 2. Sign up with GitHub account
echo 3. Import your L.I.F.E Platform repository
echo 4. Deploy automatically - gets global URL
echo.
echo Benefits: Free, global CDN, custom domains available
goto end

:permission_request
echo.
echo 📧 PERMISSION REQUEST TEMPLATE:
echo.
echo Subject: L.I.F.E Platform Deployment - Additional Azure Permissions Required
echo.
echo Hi [Senior Administrator],
echo.
echo I need additional Azure permissions to deploy our revenue-generating L.I.F.E Platform:
echo.
echo Current Issue: %SELECTED_RG% resource group deployment failed
echo Required Permission: Static Web Apps or App Service creation
echo Business Impact: $345K Q4 2025 revenue target blocked
echo.
echo Specific Request:
echo - Static Web Apps creation permission, OR
echo - App Service creation permission  
echo - Resource Group: %SELECTED_RG%
echo.
echo The platform is complete and ready - only needs hosting deployment.
echo Can we resolve this quickly to unblock our Q4 revenue target?
echo.
goto end

:local_demo
echo.
echo 📋 LOCAL DEMONSTRATION SETUP:
echo.
echo Running L.I.F.E Platform locally for demonstration:
echo.
start LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html
start LIFE_AI_PLATFORM_REAL.html
start LIFE_EDUCATION_PLATFORM_REAL.html  
start LIFE_RESEARCH_PLATFORM_REAL.html
echo.
echo ✅ All L.I.F.E Platform interfaces opened locally!
echo Use these for demonstrations while Azure permissions are resolved.
goto end

:success
echo.
echo ========================================
echo 🎉 DEPLOYMENT SUCCESSFUL!
echo ========================================
echo.
echo L.I.F.E Platform Status: GLOBALLY DEPLOYED ✅
echo Revenue Target: $345K Q4 2025 → ON TRACK 🎯
echo Next Step: Azure Marketplace listing setup
echo.

:end
if exist available_rgs.txt del available_rgs.txt
echo.
echo ========================================
echo DEPLOYMENT PROCESS COMPLETE
echo ========================================
pause