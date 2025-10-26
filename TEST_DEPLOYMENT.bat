@echo off
echo ============================================================
echo  L.I.F.E PLATFORM - DEPLOYMENT VERIFICATION
echo ============================================================
echo.

REM Test 1: Check Function App Status
echo [Test 1/5] Checking Function App status...
az functionapp show --name life-functions-app --resource-group life-platform-rg --query state --output tsv
echo.

REM Test 2: List Deployed Functions
echo [Test 2/5] Listing deployed functions...
az functionapp function list --name life-functions-app --resource-group life-platform-rg --output table
echo.

REM Test 3: Check Recent Deployments
echo [Test 3/5] Checking deployment history...
az functionapp deployment list --name life-functions-app --resource-group life-platform-rg --output table
echo.

REM Test 4: Get Function App URL
echo [Test 4/5] Function App URL:
echo https://life-functions-app.azurewebsites.net
echo.

REM Test 5: Test Health Endpoint (using Python)
echo [Test 5/5] Testing health endpoint with Python...
python -c "import urllib.request; import json; response = urllib.request.urlopen('https://life-functions-app.azurewebsites.net/api/health'); print(json.dumps(json.loads(response.read()), indent=2))"
if %errorlevel% == 0 (
    echo.
    echo ============================================================
    echo  SUCCESS! Your L.I.F.E Platform is LIVE!
    echo ============================================================
) else (
    echo.
    echo ============================================================
    echo  Health endpoint test failed - checking deployment status
    echo ============================================================
    echo.
    echo Possible reasons:
    echo   1. Deployment still in progress ^(wait 1-2 minutes^)
    echo   2. Functions not synced ^(restart may be needed^)
    echo   3. Application error ^(check logs^)
    echo.
    echo To restart Function App:
    echo   az functionapp restart --name life-functions-app --resource-group life-platform-rg
    echo.
    echo To view logs:
    echo   az webapp log tail --name life-functions-app --resource-group life-platform-rg
    echo.
)

echo.
echo ============================================================
echo  View in Azure Portal:
echo ============================================================
echo https://portal.azure.com/#resource/subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca/resourceGroups/life-platform-rg/providers/Microsoft.Web/sites/life-functions-app
echo.
pause
