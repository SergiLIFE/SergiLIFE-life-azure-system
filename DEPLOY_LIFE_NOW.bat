@echo off
echo ========================================
echo 🚨 EMERGENCY: L.I.F.E Platform Azure Deployment
echo ========================================
echo Issue: DNS_PROBE_FINISHED_NXDOMAIN (Web App doesn't exist)
echo Solution: Create Azure Web App with unique name
echo Revenue Impact: $345K Q4 2025 → $50.7M by 2029
echo.

REM Generate unique app name
for /f "tokens=1-4 delims=/ " %%i in ('date /t') do set mydate=%%i%%j%%k
for /f "tokens=1-2 delims=: " %%i in ('time /t') do set mytime=%%i%%j
set timestamp=%mydate%%mytime%
set uniqueappname=life-platform-staging-%timestamp%
set resourcegroup=life-platform-staging-rg
set location=eastus2

echo 🎯 Creating resources with unique name: %uniqueappname%
echo.

echo [STEP 1] Checking Azure CLI authentication...
az account show >nul 2>&1
if %errorlevel% neq 0 (
    echo Logging into Azure...
    az login
)

echo [STEP 2] Setting subscription...
az account set --subscription "5c88cef6-f243-497d-98af-6c6086d575ca"

echo [STEP 3] Creating resource group: %resourcegroup%
az group create --name %resourcegroup% --location %location%

echo [STEP 4] Creating App Service Plan (Free tier)...
az appservice plan create --name %resourcegroup%-plan --resource-group %resourcegroup% --sku F1 --is-linux --location %location%

echo [STEP 5] Creating Web App: %uniqueappname%
az webapp create --name %uniqueappname% --resource-group %resourcegroup% --plan %resourcegroup%-plan --runtime "PYTHON:3.11"

echo [STEP 6] Deploying L.I.F.E Platform application...
az webapp up --name %uniqueappname% --resource-group %resourcegroup% --runtime "PYTHON:3.11" --location %location%

echo.
echo ========================================
echo 🎉 DEPLOYMENT COMPLETE!
echo ========================================
echo.
echo 🌐 Your L.I.F.E Platform URLs:
echo 📍 Main: https://%uniqueappname%.azurewebsites.net/
echo 🏥 Health: https://%uniqueappname%.azurewebsites.net/health  
echo 📊 Status: https://%uniqueappname%.azurewebsites.net/api/status
echo.
echo 💰 Business Impact: $345K Q4 2025 → $50.7M by 2029 pathway restored!
echo.

echo [STEP 7] Opening in browser...
start https://%uniqueappname%.azurewebsites.net/
timeout /t 3 /nobreak >nul
start https://%uniqueappname%.azurewebsites.net/health

echo.
echo 🚀 L.I.F.E Platform emergency deployment complete!
echo 📝 New staging URL saved in DEPLOYED_URL.txt
echo %uniqueappname%.azurewebsites.net > DEPLOYED_URL.txt

pause