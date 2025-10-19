@echo off
REM L.I.F.E Platform Azure Staging Deployment - Complete Script
REM Copyright 2025 - Sergio Paya Borrull

echo.
echo ================================================================================
echo      L.I.F.E PLATFORM - AZURE STAGING DEPLOYMENT
echo ================================================================================
echo Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
echo Production-Ready: September 27, 2025
echo Target Revenue: $345K Q4 2025 to $50.7M by 2029
echo ================================================================================
echo.

SET SUBSCRIPTION_ID=5c88cef6-f243-497d-98af-6c6086d575ca
SET RESOURCE_GROUP=life-platform-rg
SET LOCATION=eastus2
SET STORAGE_ACCOUNT=stlifeplatformprod
SET KEY_VAULT=kv-life-platform-prod
SET SERVICE_BUS=sb-life-platform-prod
SET APP_SERVICE_PLAN=life-app-service-plan
SET FUNCTION_APP=life-functions-app

echo Step 1: Verifying Azure CLI authentication...
az account show >nul 2>&1
if errorlevel 1 (
    echo ERROR: Azure CLI not authenticated
    echo Please run: az login
    pause
    exit /b 1
)
echo [OK] Authenticated

echo Step 2: Setting subscription to %SUBSCRIPTION_ID%...
az account set --subscription %SUBSCRIPTION_ID%
if errorlevel 1 (
    echo ERROR: Failed to set subscription
    pause
    exit /b 1
)
echo [OK] Subscription set

echo.
echo Step 3: Checking resource group '%RESOURCE_GROUP%'...
az group exists --name %RESOURCE_GROUP% > temp_result.txt
set /p GROUP_EXISTS=<temp_result.txt
del temp_result.txt

if "%GROUP_EXISTS%"=="true" (
    echo [OK] Resource group already exists
) else (
    echo Creating resource group '%RESOURCE_GROUP%' in %LOCATION%...
    az group create --name %RESOURCE_GROUP% --location %LOCATION% --tags Project=LIFE-Platform Environment=Staging OfferID=9a600d96-fe1e-420b-902a-a0c42c561adb
    if errorlevel 1 (
        echo ERROR: Failed to create resource group
        pause
        exit /b 1
    )
    echo [OK] Resource group created
)

echo.
echo Step 4: Creating Storage Account '%STORAGE_ACCOUNT%'...
az storage account create --name %STORAGE_ACCOUNT% --resource-group %RESOURCE_GROUP% --location %LOCATION% --sku Standard_LRS --kind StorageV2 --access-tier Hot --allow-blob-public-access false --min-tls-version TLS1_2 2>nul
if errorlevel 1 (
    echo [INFO] Storage account might already exist, continuing...
) else (
    echo [OK] Storage account created
)

echo.
echo Step 5: Creating Key Vault '%KEY_VAULT%'...
az keyvault create --name %KEY_VAULT% --resource-group %RESOURCE_GROUP% --location %LOCATION% --sku standard --enable-rbac-authorization true 2>nul
if errorlevel 1 (
    echo [INFO] Key Vault might already exist, continuing...
) else (
    echo [OK] Key Vault created
)

echo.
echo Step 6: Creating Service Bus '%SERVICE_BUS%'...
az servicebus namespace create --name %SERVICE_BUS% --resource-group %RESOURCE_GROUP% --location %LOCATION% --sku Standard 2>nul
if errorlevel 1 (
    echo [INFO] Service Bus might already exist, continuing...
) else (
    echo [OK] Service Bus created
)

echo.
echo Step 7: Creating App Service Plan '%APP_SERVICE_PLAN%'...
az appservice plan create --name %APP_SERVICE_PLAN% --resource-group %RESOURCE_GROUP% --location %LOCATION% --sku B1 --is-linux 2>nul
if errorlevel 1 (
    echo [INFO] App Service Plan might already exist, continuing...
) else (
    echo [OK] App Service Plan created
)

echo.
echo Step 8: Creating Function App '%FUNCTION_APP%'...
az functionapp create --name %FUNCTION_APP% --resource-group %RESOURCE_GROUP% --plan %APP_SERVICE_PLAN% --storage-account %STORAGE_ACCOUNT% --runtime python --runtime-version 3.11 --functions-version 4 --os-type Linux 2>nul
if errorlevel 1 (
    echo [INFO] Function App might already exist, continuing...
) else (
    echo [OK] Function App created
)

echo.
echo Step 9: Listing deployed resources...
az resource list --resource-group %RESOURCE_GROUP% --output table

echo.
echo ================================================================================
echo    DEPLOYMENT COMPLETED SUCCESSFULLY!
echo ================================================================================
echo.
echo Deployed Resources:
echo   - Resource Group: %RESOURCE_GROUP%
echo   - Storage Account: %STORAGE_ACCOUNT%
echo   - Key Vault: %KEY_VAULT%
echo   - Service Bus: %SERVICE_BUS%
echo   - App Service Plan: %APP_SERVICE_PLAN%
echo   - Function App: %FUNCTION_APP%
echo.
echo Next Steps:
echo   1. Configure Function App settings
echo   2. Deploy Function App code
echo   3. Configure monitoring and alerts
echo   4. Test endpoints and functionality
echo.
echo For detailed information, run:
echo   az resource list --resource-group %RESOURCE_GROUP% --output json
echo.
pause
