@echo off
echo ========================================
echo 🌐 L.I.F.E PLATFORM - AZURE APP SERVICE DEPLOYMENT
echo ========================================
echo.

set RESOURCE_GROUP=life-platform-global
set APP_SERVICE_PLAN=life-platform-plan
set WEB_APP_NAME=life-platform-web
set LOCATION="East US 2"

echo [STEP 1] Checking Azure CLI authentication...
az account show --query "{name:name, id:id}" --output table

echo.
echo [STEP 2] Creating Resource Group...
az group create --name %RESOURCE_GROUP% --location %LOCATION%

echo.
echo [STEP 3] Creating App Service Plan...
az appservice plan create ^
  --name %APP_SERVICE_PLAN% ^
  --resource-group %RESOURCE_GROUP% ^
  --location %LOCATION% ^
  --sku FREE

echo.
echo [STEP 4] Creating Web App...
az webapp create ^
  --name %WEB_APP_NAME% ^
  --resource-group %RESOURCE_GROUP% ^
  --plan %APP_SERVICE_PLAN%

echo.
echo [STEP 5] Preparing deployment package...
echo Creating ZIP file with L.I.F.E Platform files...

tar -a -c -f life-platform-deployment.zip ^
  index.html ^
  LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html ^
  LIFE_AI_PLATFORM_REAL.html ^
  LIFE_EDUCATION_PLATFORM_REAL.html ^
  LIFE_RESEARCH_PLATFORM_REAL.html ^
  staticwebapp.config.json

echo.
echo [STEP 6] Deploying L.I.F.E Platform to Azure...
az webapp deployment source config-zip ^
  --resource-group %RESOURCE_GROUP% ^
  --name %WEB_APP_NAME% ^
  --src life-platform-deployment.zip

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ SUCCESS! L.I.F.E Platform deployed to Azure App Service!
    echo.
    echo 🌐 GLOBAL L.I.F.E PLATFORM URLS:
    echo ================================
    echo Main Platform: https://%WEB_APP_NAME%.azurewebsites.net
    echo Clinical: https://%WEB_APP_NAME%.azurewebsites.net/LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html
    echo AI Platform: https://%WEB_APP_NAME%.azurewebsites.net/LIFE_AI_PLATFORM_REAL.html
    echo Education: https://%WEB_APP_NAME%.azurewebsites.net/LIFE_EDUCATION_PLATFORM_REAL.html
    echo Research: https://%WEB_APP_NAME%.azurewebsites.net/LIFE_RESEARCH_PLATFORM_REAL.html
    echo.
    echo 🎉 L.I.F.E Platform is now globally accessible!
    echo 🚀 Hosted on Azure with global reach
    
    echo.
    echo Opening main platform in browser...
    start https://%WEB_APP_NAME%.azurewebsites.net
    
) else (
    echo.
    echo ❌ DEPLOYMENT FAILED
    echo Check Azure permissions and try again
)

echo.
echo Cleaning up deployment files...
del life-platform-deployment.zip

echo.
echo ========================================
echo DEPLOYMENT COMPLETE
echo ========================================
pause