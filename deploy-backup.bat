@echo off
REM L.I.F.E. Platform - Azure Backup Deployment (Batch File)
REM For when PowerShell/Terminal isn't working
REM Azure Subscription: 5c88cef6-f243-497d-98af-6c6086d575ca

echo.
echo ========================================================
echo  L.I.F.E. Platform - Azure Backup System Deployment
echo ========================================================
echo  Subscription: 5c88cef6-f243-497d-98af-6c6086d575ca
echo  Admin: sergiomiguelpaya@sergiomiguelpayaborrullmsn.onmicrosoft.com
echo  This will save ALL your work to Azure safely!
echo ========================================================
echo.

REM Check if Azure CLI is installed
where az >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Azure CLI not found!
    echo.
    echo Please install Azure CLI first:
    echo 1. Go to: https://aka.ms/installazurecliwindows
    echo 2. Download and install Azure CLI
    echo 3. Restart this script
    echo.
    pause
    exit /b 1
)

echo Step 1: Authenticating to Azure...
az login --use-device-code
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Azure authentication failed!
    pause
    exit /b 1
)

echo.
echo Step 2: Setting correct subscription...
az account set --subscription "5c88cef6-f243-497d-98af-6c6086d575ca"
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Could not set subscription!
    pause
    exit /b 1
)

echo.
echo Step 3: Creating resource group...
az group create --name "life-platform-rg" --location "eastus2" --tags "project=L.I.F.E. Platform" "purpose=backup"
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: Resource group creation failed or already exists
)

echo.
echo Step 4: Previewing deployment...
az deployment group what-if --resource-group "life-platform-rg" --template-file "infra\backup-infrastructure.bicep" --parameters "@infra\backup-infrastructure.parameters.json"

echo.
echo ========================================================
echo  DEPLOYMENT PREVIEW COMPLETE
echo ========================================================
echo  This will create Azure resources to backup your repository
echo  Estimated cost: $8-18/month
echo  Your work will be SAFE in Azure forever!
echo ========================================================
echo.

set /p CONFIRM="Continue with deployment? (Y/N): "
if /i "%CONFIRM%" NEQ "Y" (
    echo Deployment cancelled.
    pause
    exit /b 0
)

echo.
echo Step 5: Deploying backup infrastructure...
az deployment group create --resource-group "life-platform-rg" --name "life-backup-%date:~-4,4%%date:~-10,2%%date:~-7,2%-%time:~0,2%%time:~3,2%%time:~6,2%" --template-file "infra\backup-infrastructure.bicep" --parameters "@infra\backup-infrastructure.parameters.json" --verbose

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================================
    echo  SUCCESS! Azure Backup Infrastructure Deployed!
    echo ========================================================
    echo  Your L.I.F.E. Platform repository is now protected!
    echo.
    echo  Next steps:
    echo  1. Run: python azure_repository_backup_sync.py
    echo  2. Check Azure Portal: https://portal.azure.com
    echo  3. Look for Storage Account: stlifeplatformprod
    echo.
    echo  Your work is now SAFE in Azure!
    echo ========================================================
) else (
    echo.
    echo ERROR: Deployment failed!
    echo Please check the error messages above.
    echo.
)

echo.
echo Press any key to exit...
pause >nul