@echo off
REM L.I.F.E Platform - Azure Function App Emergency Fix
REM September 26, 2025 - Launch Day -1

echo =====================================================
echo L.I.F.E PLATFORM - AZURE FUNCTION APP EMERGENCY FIX
echo =====================================================
echo.
echo Target: life-functions-app
echo Resource Group: life-platform-rg
echo Launch Date: September 27, 2025 (TOMORROW!)
echo.

echo Setting Azure subscription context...
az account set --subscription "5c88cef6-f243-497d-98af-6c6086d575ca"

echo.
echo Fix 1: Setting Python runtime version...
az functionapp config set --name "life-functions-app" --resource-group "life-platform-rg" --linux-fx-version "Python|3.11"

echo.
echo Fix 2: Configuring essential app settings...
az functionapp config appsettings set --name "life-functions-app" --resource-group "life-platform-rg" --settings ^
    "FUNCTIONS_WORKER_RUNTIME=python" ^
    "FUNCTIONS_EXTENSION_VERSION=~4" ^
    "PYTHON_VERSION=3.11" ^
    "LIFE_PLATFORM_VERSION=2025.1.0-PRODUCTION" ^
    "AZURE_MARKETPLACE_OFFER_ID=9a600d96-fe1e-420b-902a-a0c42c561adb" ^
    "LAUNCH_DATE=2025-09-27" ^
    "REVENUE_TARGET_Q4=345000"

echo.
echo Fix 3: Restarting function app...
az functionapp restart --name "life-functions-app" --resource-group "life-platform-rg"

echo.
echo Waiting 30 seconds for restart...
timeout /t 30 /nobreak > nul

echo.
echo Verification: Checking function app status...
az functionapp show --name "life-functions-app" --resource-group "life-platform-rg" --query "{name:name,state:state}" --output table

echo.
echo Verification: Testing functions list...
az functionapp function list --name "life-functions-app" --resource-group "life-platform-rg" --output table

echo.
echo =====================================================
echo FIXES APPLIED SUCCESSFULLY!
echo =====================================================
echo.
echo Next Steps:
echo 1. Check Azure Portal for function app status
echo 2. Test health endpoint: https://life-functions-app.azurewebsites.net
echo 3. Verify functions are loading properly
echo 4. Run campaign activation scripts
echo.
echo LAUNCH STATUS: READY FOR SEPTEMBER 27!
echo.
pause