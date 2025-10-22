@echo off
echo ======================================================================
echo  SIMPLE TEST DEPLOYMENT - Verify Working
echo ======================================================================
echo.

set FUNC_APP_NAME=life-functions-app-prod
set RESOURCE_GROUP=life-platform-prod

echo Testing current Function App state...
echo.

echo [1] Checking if Function App exists:
az functionapp show --name %FUNC_APP_NAME% --resource-group %RESOURCE_GROUP% --query "state" --output tsv

echo.
echo [2] Listing deployed functions:
az functionapp function list --name %FUNC_APP_NAME% --resource-group %RESOURCE_GROUP% --output table

echo.
echo [3] Testing health endpoint:
python -c "import urllib.request; import json; try: response = urllib.request.urlopen('https://life-functions-app-prod.azurewebsites.net/api/health', timeout=15); data = json.loads(response.read()); print('✅ SUCCESS:', data); except Exception as e: print('❌ ERROR:', str(e))"

echo.
echo [4] Testing with curl (alternative):
curl -s "https://life-functions-app-prod.azurewebsites.net/api/health" || echo "Curl failed"

echo.
echo [5] Checking deployment status:
az functionapp deployment list --name %FUNC_APP_NAME% --resource-group %RESOURCE_GROUP% --query "[0].{Status:status, Author:author, Message:message}" --output table

echo.
echo ======================================================================
echo  Diagnostic Complete
echo ======================================================================
pause