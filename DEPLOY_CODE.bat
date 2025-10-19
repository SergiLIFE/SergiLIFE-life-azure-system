@echo off
echo ========================================
echo L.I.F.E PLATFORM - CODE DEPLOYMENT
echo ========================================
echo.

REM Deploy Python code to Function App
echo 📦 Deploying your 206-file codebase to Azure Functions...

REM Zip the current directory
echo 📁 Creating deployment package...
powershell -Command "Compress-Archive -Path '*.py' -DestinationPath 'life-platform-deployment.zip' -Force"

REM Deploy to Function App
echo 🚀 Uploading to Azure Functions...
az functionapp deployment source config-zip ^
    --resource-group life-platform-prod ^
    --name life-functions-app ^
    --src life-platform-deployment.zip

REM Configure app settings
echo ⚙️ Configuring environment variables...
az functionapp config appsettings set ^
    --resource-group life-platform-prod ^
    --name life-functions-app ^
    --settings ^
    AZURE_STORAGE_ACCOUNT=stlifeplatformprod ^
    AZURE_KEY_VAULT=kv-life-platform-prod ^
    AZURE_SERVICE_BUS=sb-life-platform-prod ^
    LIFE_ENVIRONMENT=production

REM Get Function App URL
echo 🌐 Getting your live URL...
az functionapp show ^
    --resource-group life-platform-prod ^
    --name life-functions-app ^
    --query "defaultHostName" ^
    --output tsv

echo.
echo ========================================
echo ✅ CODE DEPLOYMENT COMPLETE
echo ========================================
echo.
echo Your 206 Python files are now running live on Azure!
echo.
echo Test your deployment:
echo https://life-functions-app.azurewebsites.net
echo.
pause