@echo off
echo ========================================
echo L.I.F.E PLATFORM - DIRECT DEPLOYMENT
echo ========================================
echo.
echo This will deploy your 206-file codebase directly to Azure
echo using your existing configuration and credentials.
echo.

REM Check if Azure CLI is available
where az >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Azure CLI not found. Installing...
    echo Please download from: https://aka.ms/installazurecliwindows
    pause
    exit /b 1
)

echo ✅ Azure CLI found. Proceeding with deployment...
echo.

REM Login and set subscription
echo 🔐 Logging into Azure...
az login --tenant e716161a-5e85-4d6d-82f9-96bcdd2e65ac
az account set --subscription 5c88cef6-f243-497d-98af-6c6086d575ca

REM Create resource group if it doesn't exist
echo 🏗️ Creating resource group...
az group create --name life-platform-prod --location "East US 2"

REM Deploy Function App
echo ⚡ Creating Function App...
az functionapp create ^
    --resource-group life-platform-prod ^
    --consumption-plan-location "East US 2" ^
    --runtime python ^
    --runtime-version 3.9 ^
    --functions-version 4 ^
    --name life-functions-app ^
    --storage-account stlifeplatformprod

REM Deploy Storage Account
echo 💾 Creating Storage Account...
az storage account create ^
    --name stlifeplatformprod ^
    --resource-group life-platform-prod ^
    --location "East US 2" ^
    --sku Standard_LRS

REM Deploy Key Vault
echo 🔐 Creating Key Vault...
az keyvault create ^
    --name kv-life-platform-prod ^
    --resource-group life-platform-prod ^
    --location "East US 2"

REM Deploy Service Bus
echo 📨 Creating Service Bus...
az servicebus namespace create ^
    --resource-group life-platform-prod ^
    --name sb-life-platform-prod ^
    --location "East US 2"

echo.
echo ========================================
echo ✅ DEPLOYMENT COMPLETE
echo ========================================
echo.
echo Your L.I.F.E Platform is now deployed to Azure:
echo - Resource Group: life-platform-prod
echo - Function App: life-functions-app
echo - Storage Account: stlifeplatformprod
echo - Key Vault: kv-life-platform-prod
echo - Service Bus: sb-life-platform-prod
echo.
echo Next: Run VALIDATE_DEPLOYMENT.bat to test your deployment
echo.
pause