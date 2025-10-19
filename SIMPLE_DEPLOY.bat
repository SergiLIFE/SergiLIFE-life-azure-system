@echo off
REM Simple Azure Deployment for L.I.F.E Platform
REM Sergio Paya Borrull - October 19, 2025

cls
echo.
echo ========================================================
echo      L.I.F.E PLATFORM - AZURE DEPLOYMENT
echo ========================================================
echo.

SET SUB=5c88cef6-f243-497d-98af-6c6086d575ca
SET RG=life-platform-rg
SET LOC=eastus2

echo Step 1: Setting subscription...
call az account set --subscription %SUB%

echo Step 2: Creating resource group (if needed)...
call az group create --name %RG% --location %LOC% --output none 2>nul

echo Step 3: Creating Storage Account...
call az storage account create --name stlifeplatformprod --resource-group %RG% --location %LOC% --sku Standard_LRS --output none 2>nul
if errorlevel 1 (echo   [Already exists or created]) else (echo   [Created!])

echo Step 4: Creating Key Vault...
call az keyvault create --name kv-life-platform-prod --resource-group %RG% --location %LOC% --output none 2>nul
if errorlevel 1 (echo   [Already exists or created]) else (echo   [Created!])

echo Step 5: Creating Service Bus...
call az servicebus namespace create --name sb-life-platform-prod --resource-group %RG% --location %LOC% --sku Standard --output none 2>nul
if errorlevel 1 (echo   [Already exists or created]) else (echo   [Created!])

echo Step 6: Creating App Service Plan...
call az appservice plan create --name life-app-service-plan --resource-group %RG% --location %LOC% --sku B1 --is-linux --output none 2>nul
if errorlevel 1 (echo   [Already exists or created]) else (echo   [Created!])

echo Step 7: Creating Function App...
call az functionapp create --name life-functions-app --resource-group %RG% --plan life-app-service-plan --storage-account stlifeplatformprod --runtime python --runtime-version 3.11 --functions-version 4 --os-type Linux --output none 2>nul
if errorlevel 1 (echo   [Already exists or created]) else (echo   [Created!])

echo.
echo ========================================================
echo               DEPLOYMENT COMPLETE!
echo ========================================================
echo.
echo Listing resources:
call az resource list --resource-group %RG% --output table

echo.
echo View in Azure Portal:
echo https://portal.azure.com/#resource/subscriptions/%SUB%/resourceGroups/%RG%/overview
echo.
pause
