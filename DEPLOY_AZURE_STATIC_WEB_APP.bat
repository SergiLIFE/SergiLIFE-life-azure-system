@echo off
echo ========================================
echo 🌐 L.I.F.E PLATFORM - AZURE GLOBAL DEPLOYMENT
echo ========================================
echo.

set RESOURCE_GROUP=life-platform-global
set STATIC_APP_NAME=life-platform-global
set LOCATION="East US 2"

echo [STEP 1] Checking Azure CLI authentication...
az account show --query "{name:name, id:id}" --output table
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Not logged into Azure CLI
    echo Please run: az login
    pause
    exit /b 1
)

echo.
echo [STEP 2] Creating Resource Group...
az group create --name %RESOURCE_GROUP% --location %LOCATION%

echo.
echo [STEP 3] Checking Static Web Apps permissions...
az provider show --namespace Microsoft.Web --query "{namespace:namespace, registrationState:registrationState}" --output table

echo.
echo [STEP 4] Creating Azure Static Web App...
echo.
echo 🎯 Creating global L.I.F.E Platform deployment...
echo    • Name: %STATIC_APP_NAME%
echo    • Resource Group: %RESOURCE_GROUP%
echo    • Location: %LOCATION%
echo    • Files: All L.I.F.E HTML platforms
echo.

az staticwebapp create ^
  --name %STATIC_APP_NAME% ^
  --resource-group %RESOURCE_GROUP% ^
  --location %LOCATION% ^
  --source . ^
  --sku Free

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ SUCCESS! L.I.F.E Platform deployed to Azure!
    echo.
    echo Getting deployment URL...
    az staticwebapp show --name %STATIC_APP_NAME% --resource-group %RESOURCE_GROUP% --query "defaultHostname" --output tsv > temp_url.txt
    set /p DEPLOYMENT_URL=<temp_url.txt
    del temp_url.txt
    
    echo.
    echo 🌐 GLOBAL L.I.F.E PLATFORM URLS:
    echo ================================
    echo Main Platform: https://%DEPLOYMENT_URL%
    echo Clinical: https://%DEPLOYMENT_URL%/LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html
    echo AI Platform: https://%DEPLOYMENT_URL%/LIFE_AI_PLATFORM_REAL.html
    echo Education: https://%DEPLOYMENT_URL%/LIFE_EDUCATION_PLATFORM_REAL.html
    echo Research: https://%DEPLOYMENT_URL%/LIFE_RESEARCH_PLATFORM_REAL.html
    echo.
    echo 🎉 L.I.F.E Platform is now globally accessible!
    echo 🚀 Powered by Azure Global CDN for worldwide performance
    
) else (
    echo.
    echo ❌ DEPLOYMENT FAILED
    echo.
    echo Possible reasons:
    echo 1. Insufficient Azure permissions
    echo 2. Static Web Apps not enabled in subscription
    echo 3. Resource quota exceeded
    echo.
    echo 💡 ALTERNATIVE: Try Azure App Service deployment
    echo    Run: DEPLOY_AZURE_APP_SERVICE.bat
)

echo.
echo ========================================
echo DEPLOYMENT COMPLETE
echo ========================================
pause