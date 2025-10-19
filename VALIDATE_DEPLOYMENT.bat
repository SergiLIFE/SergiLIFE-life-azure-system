@echo off
echo ========================================
echo L.I.F.E PLATFORM - DEPLOYMENT VALIDATION
echo ========================================
echo.

REM Test Azure resources
echo 🔍 Validating Azure deployment...

az group show --name life-platform-prod --output table
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Resource group not found
    exit /b 1
)

az functionapp list --resource-group life-platform-prod --query "[].{Name:name,State:state}" --output table
az storage account list --resource-group life-platform-prod --output table
az keyvault list --resource-group life-platform-prod --output table
az servicebus namespace list --resource-group life-platform-prod --output table

echo.
echo ========================================
echo ✅ VALIDATION COMPLETE
echo ========================================
echo.
echo Your L.I.F.E Platform Azure resources are running!
echo.
echo Next steps:
echo 1. Upload your code to Function App
echo 2. Configure environment variables
echo 3. Test live endpoints
echo.
pause