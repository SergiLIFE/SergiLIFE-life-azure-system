@echo off
echo ================================================================
echo 🐍 L.I.F.E Platform - Python 3.13 Deployment Fix
echo ================================================================
echo.
echo 🎯 Target Function App: lifeplatform1760781933
echo 📦 Resource Group: life-platform-prod
echo 🐍 Python Version: 3.13
echo.

SET FUNC_APP_NAME=lifeplatform1760781933
SET RESOURCE_GROUP=life-platform-prod

echo 📝 Step 1: Updating Function App settings for Python 3.13...
call az functionapp config appsettings set ^
    --resource-group %RESOURCE_GROUP% ^
    --name %FUNC_APP_NAME% ^
    --settings ^
    FUNCTIONS_WORKER_RUNTIME=python ^
    FUNCTIONS_WORKER_RUNTIME_VERSION=3.13 ^
    FUNCTIONS_EXTENSION_VERSION=~4 ^
    LIFE_PLATFORM_VERSION=2025.1.0-PRODUCTION ^
    AZURE_STORAGE_ACCOUNT=stlifeplatformprod ^
    AZURE_KEY_VAULT=kv-life-platform-prod ^
    AZURE_SERVICE_BUS=sb-life-platform-prod ^
    LIFE_ENVIRONMENT=production

if %errorlevel% neq 0 (
    echo ❌ Failed to update app settings
    pause
    exit /b 1
)

echo ✅ App settings updated successfully
echo.

echo 📦 Step 2: Creating deployment package...
if exist deployment.zip del deployment.zip
powershell -Command "Compress-Archive -Path @('LifePlatformAPI', 'host_python313.json', 'requirements.txt') -DestinationPath deployment.zip -Force -CompressionLevel Optimal"

if not exist deployment.zip (
    echo ❌ Failed to create deployment package
    pause
    exit /b 1
)

echo ✅ Deployment package created
echo.

echo 🚀 Step 3: Deploying to Azure Functions...
call az functionapp deployment source config-zip ^
    --resource-group %RESOURCE_GROUP% ^
    --name %FUNC_APP_NAME% ^
    --src deployment.zip

if %errorlevel% neq 0 (
    echo ❌ Deployment failed
    pause
    exit /b 1
)

echo ✅ Deployment initiated successfully
echo.

echo ⏳ Step 4: Waiting for deployment to complete...
timeout /t 45 /nobreak
echo.

echo 🧪 Step 5: Testing API endpoints...
echo Testing validation endpoint...
curl -s "https://%FUNC_APP_NAME%.azurewebsites.net/api/validate-ingestion" 
echo.
echo.

echo Testing ingestion stats...
curl -s "https://%FUNC_APP_NAME%.azurewebsites.net/api/ingestion-stats"
echo.
echo.

echo Testing EEG ingestion (POST)...
curl -s -X POST "https://%FUNC_APP_NAME%.azurewebsites.net/api/ingest-external-eeg" -H "Content-Type: application/json" -d "{\"mode\": \"full_cycle\"}"
echo.
echo.

echo ================================================================
echo 🎉 Python 3.13 Deployment Complete!
echo ================================================================
echo.
echo 🔗 Function App URLs:
echo   Main: https://%FUNC_APP_NAME%.azurewebsites.net
echo   Validate: https://%FUNC_APP_NAME%.azurewebsites.net/api/validate-ingestion
echo   Stats: https://%FUNC_APP_NAME%.azurewebsites.net/api/ingestion-stats
echo   Ingest: https://%FUNC_APP_NAME%.azurewebsites.net/api/ingest-external-eeg
echo.
echo 📋 Next Steps:
echo   1. Test endpoints in Enhanced Dashboard
echo   2. Monitor Azure Function App logs
echo   3. Verify Python 3.13 runtime in Azure portal
echo.
echo ✅ Ready for production use with Python 3.13!
echo ================================================================
pause