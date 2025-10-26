@echo off
echo ================================================
echo DIAGNOSTIC AND FIX DEPLOYMENT
echo ================================================

set FUNC_APP_NAME=life-functions-app-prod
set RESOURCE_GROUP=life-platform-prod

echo [1] Checking Function App status...
az functionapp show --name %FUNC_APP_NAME% --resource-group %RESOURCE_GROUP% --query "{name:name, state:state, kind:kind}" --output table

echo.
echo [2] Checking if any functions are deployed...
az functionapp function list --name %FUNC_APP_NAME% --resource-group %RESOURCE_GROUP% --output table

echo.
echo [3] Checking recent deployments...
az functionapp deployment list --name %FUNC_APP_NAME% --resource-group %RESOURCE_GROUP% --query "[0].{Status:status, Message:message, Time:receivedTime}" --output table

echo.
echo [4] Creating and deploying CORRECTED function...
set TEMP_DIR=%USERPROFILE%\diagnostic_deploy
if exist "%TEMP_DIR%" rmdir /s /q "%TEMP_DIR%"
mkdir "%TEMP_DIR%"
cd /d "%TEMP_DIR%"

echo Creating corrected function_app.py...
(
echo import azure.functions as func
echo import json
echo.
echo app = func.FunctionApp^(^)
echo.
echo @app.route^(route="health", auth_level=func.AuthLevel.ANONYMOUS, methods=["GET"]^)
echo async def health_check^(req: func.HttpRequest^) -^> func.HttpResponse:
echo     return func.HttpResponse^(
echo         json.dumps^({"status": "healthy", "app": "L.I.F.E Platform", "timestamp": "working"}^),
echo         mimetype="application/json"
echo     ^)
) > function_app.py

echo Creating host.json...
(
echo {
echo   "version": "2.0",
echo   "extensionBundle": {
echo     "id": "Microsoft.Azure.Functions.ExtensionBundle",
echo     "version": "[4.*, 5.0.0^)"
echo   }
echo }
) > host.json

echo Creating requirements.txt...
echo azure-functions > requirements.txt

echo.
echo [5] Deploying corrected version...
tar -a -c -f corrected.zip function_app.py host.json requirements.txt
az functionapp deployment source config-zip --resource-group %RESOURCE_GROUP% --name %FUNC_APP_NAME% --src corrected.zip

echo.
echo [6] Waiting 2 minutes for deployment to complete...
timeout /t 120 /nobreak >nul

echo.
echo [7] Testing endpoint after deployment...
python -c "import urllib.request; import json; try: response = urllib.request.urlopen('https://life-functions-app-prod.azurewebsites.net/api/health', timeout=15); data = json.loads(response.read()); print('✅ SUCCESS:', data); except Exception as e: print('❌ FAILED:', str(e))"

echo.
echo [8] Checking deployed functions again...
az functionapp function list --name %FUNC_APP_NAME% --resource-group %RESOURCE_GROUP% --output table

echo.
echo ================================================
echo DIAGNOSTIC COMPLETE
echo ================================================
echo.
echo If successful, test in browser:
echo https://life-functions-app-prod.azurewebsites.net/api/health
echo.

cd /d "C:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system"
rmdir /s /q "%TEMP_DIR%"
pause