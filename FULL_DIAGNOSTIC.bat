@echo off
echo.
echo ======================================================================
echo   COMPREHENSIVE AZURE DIAGNOSTIC
echo ======================================================================
echo.

echo [1/6] Checking Azure CLI authentication...
az account show --query "{name:name, id:id, state:state}" --output table
echo.

echo [2/6] Checking resource group...
az group show --name life-platform-rg --query "{name:name, location:location, provisioningState:provisioningState}" --output table
echo.

echo [3/6] Listing all resources in resource group...
az resource list --resource-group life-platform-rg --output table
echo.

echo [4/6] Checking Function App specifically...
az functionapp show --name life-functions-app --resource-group life-platform-rg 2>nul
if errorlevel 1 (
    echo   Function App NOT FOUND or not accessible
) else (
    echo   Function App exists
)
echo.

echo [5/6] Testing basic connectivity...
ping -n 1 life-functions-app.azurewebsites.net
echo.

echo [6/6] Checking subscription limits...
az vm list-usage --location eastus2 --query "[?name.value=='cores'].{name:name.localizedValue, currentValue:currentValue, limit:limit}" --output table
echo.

echo ======================================================================
echo   DIAGNOSTIC COMPLETE
echo ======================================================================
echo.
pause