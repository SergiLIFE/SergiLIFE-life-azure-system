@echo off
setlocal enabledelayedexpansion

echo ========================================
echo AZURE FUNCTION APP DIAGNOSIS - 404 ERROR
echo ========================================
echo Date/Time: %DATE% %TIME%
echo.

set FUNC_APP_NAME=life-functions-app-prod
set RESOURCE_GROUP=life-platform-prod

echo [STEP 1] Checking if Function App exists...
echo.
az functionapp show --name %FUNC_APP_NAME% --resource-group %RESOURCE_GROUP% --query "{name:name, state:state, kind:kind, hostNames:hostNames, enabled:siteConfig.enabled}" --output table
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Function App does NOT exist or cannot be accessed!
    echo This explains the 404 error.
    echo.
    goto :create_function_app
) else (
    echo ✅ Function App exists, continuing diagnosis...
)
echo.

echo [STEP 2] Checking Function App detailed status...
echo.
az functionapp show --name %FUNC_APP_NAME% --resource-group %RESOURCE_GROUP% --query "{name:name, state:state, availabilityState:availabilityState, enabled:enabled, httpsOnly:httpsOnly, clientAffinityEnabled:clientAffinityEnabled}" --output table
echo.

echo [STEP 3] Listing deployed functions...
echo.
az functionapp function list --name %FUNC_APP_NAME% --resource-group %RESOURCE_GROUP% --output table
echo.
echo Function count:
az functionapp function list --name %FUNC_APP_NAME% --resource-group %RESOURCE_GROUP% --query "length(@)"
echo.

echo [STEP 4] Checking recent deployments...
echo.
az functionapp deployment list --name %FUNC_APP_NAME% --resource-group %RESOURCE_GROUP% --output table
echo.

echo [STEP 5] Checking Function App logs (last 50 lines)...
echo.
az functionapp log tail --name %FUNC_APP_NAME% --resource-group %RESOURCE_GROUP% --timeout 15
echo.

echo [STEP 6] Testing base Function App URL...
echo.
curl -I https://%FUNC_APP_NAME%.azurewebsites.net --connect-timeout 10 --max-time 20
echo.

echo [STEP 7] Checking Function App configuration...
echo.
az functionapp config show --name %FUNC_APP_NAME% --resource-group %RESOURCE_GROUP% --query "{pythonVersion:pythonVersion, linuxFxVersion:linuxFxVersion, alwaysOn:alwaysOn, use32BitWorkerProcess:use32BitWorkerProcess}" --output table
echo.

goto :end

:create_function_app
echo ========================================
echo FUNCTION APP DOES NOT EXIST - CREATING NOW
echo ========================================
echo.

echo Creating storage account first...
set STORAGE_NAME=stlifeplatform%RANDOM%
az storage account create --name %STORAGE_NAME% --resource-group %RESOURCE_GROUP% --location "East US 2" --sku Standard_LRS --kind StorageV2

echo.
echo Creating Function App...
az functionapp create --resource-group %RESOURCE_GROUP% --consumption-plan-location "East US 2" --runtime python --runtime-version 3.11 --functions-version 4 --name %FUNC_APP_NAME% --storage-account %STORAGE_NAME% --os-type Linux

echo.
echo Waiting 60 seconds for Function App to initialize...
timeout /t 60 /nobreak >nul

echo.
echo Function App created! Now we can deploy functions to it.
echo.

:end
echo ========================================
echo DIAGNOSIS COMPLETE
echo ========================================
echo.
echo Summary:
echo - Function App: %FUNC_APP_NAME%
echo - Resource Group: %RESOURCE_GROUP% 
echo - Expected URL: https://%FUNC_APP_NAME%.azurewebsites.net/api/health_simple
echo.
pause