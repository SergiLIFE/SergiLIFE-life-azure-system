@echo off
echo.
echo ========================================
echo   DEPLOYMENT DIAGNOSTICS
echo ========================================
echo.

echo [1/5] Checking Function App Status...
az functionapp show --name life-functions-app --resource-group life-platform-rg --query "{state:state, defaultHostName:defaultHostName}" --output table
echo.

echo [2/5] Checking Deployment Source...
az functionapp deployment source show --name life-functions-app --resource-group life-platform-rg --query "{repoUrl:repoUrl, branch:branch, isManualIntegration:isManualIntegration}" --output table
echo.

echo [3/5] Listing Deployed Functions...
az functionapp function list --name life-functions-app --resource-group life-platform-rg --query "[].{Name:name, Language:config.language, Disabled:config.disabled}" --output table
echo.

echo [4/5] Checking App Settings...
az functionapp config appsettings list --name life-functions-app --resource-group life-platform-rg --query "[?name=='FUNCTIONS_WORKER_RUNTIME'].{name:name, value:value}" --output table
echo.

echo [5/5] Checking Sync Status...
az functionapp sync --name life-functions-app --resource-group life-platform-rg
echo.

echo ========================================
echo   Diagnostic Check Complete
echo ========================================
echo.
echo Next Steps:
echo 1. If functions are listed above, wait 2 minutes and test again
echo 2. If no functions listed, run: func azure functionapp publish life-functions-app --python --build remote
echo 3. If still failing, check deployment logs in Azure Portal
echo.
pause
