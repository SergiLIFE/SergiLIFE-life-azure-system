@echo off
echo ========================================
echo CORRECTED HEALTH ENDPOINT DEPLOYMENT
echo ========================================

set FUNC_APP_NAME=life-functions-app-prod
set RESOURCE_GROUP=life-platform-prod

echo Creating corrected function structure...
set DEPLOY_DIR=%USERPROFILE%\corrected_deploy
if exist "%DEPLOY_DIR%" rmdir /s /q "%DEPLOY_DIR%"
mkdir "%DEPLOY_DIR%"
cd /d "%DEPLOY_DIR%"

REM Create host.json
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

REM Create requirements.txt
echo Creating requirements.txt...
echo azure-functions > requirements.txt

REM Create health_simple function folder (EXACTLY as specified)
echo Creating health_simple function folder...
mkdir health_simple
cd health_simple

REM Create function.json with EXACT route configuration
echo Creating function.json with correct route...
(
echo {
echo   "scriptFile": "__init__.py",
echo   "bindings": [
echo     {
echo       "authLevel": "anonymous",
echo       "type": "httpTrigger",
echo       "direction": "in",
echo       "name": "req",
echo       "methods": ["get", "post"],
echo       "route": "health_simple"
echo     },
echo     {
echo       "type": "http",
echo       "direction": "out",
echo       "name": "$return"
echo     }
echo   ]
echo }
) > function.json

REM Create __init__.py with working function code
echo Creating __init__.py...
(
echo import azure.functions as func
echo import json
echo import logging
echo.
echo def main^(req: func.HttpRequest^) -^> func.HttpResponse:
echo     logging.info^('Health simple function processed a request.'^)
echo     
echo     result = {
echo         "status": "healthy",
echo         "app": "L.I.F.E Platform", 
echo         "endpoint": "health_simple",
echo         "timestamp": func.datetime.utcnow^(^).isoformat^(^),
echo         "message": "Function endpoint working correctly"
echo     }
echo     
echo     return func.HttpResponse^(
echo         json.dumps^(result^),
echo         mimetype="application/json",
echo         status_code=200
echo     ^)
) > __init__.py

cd ..

echo.
echo Creating deployment zip...
tar -a -c -f deploy.zip host.json requirements.txt health_simple

echo.
echo Deploying to Azure Function App...
az functionapp deployment source config-zip --resource-group %RESOURCE_GROUP% --name %FUNC_APP_NAME% --src deploy.zip

echo.
echo Waiting 90 seconds for deployment to complete...
timeout /t 90 /nobreak >nul

echo.
echo ========================================
echo TESTING DEPLOYED ENDPOINT
echo ========================================
echo.
echo Testing: https://%FUNC_APP_NAME%.azurewebsites.net/api/health_simple
echo.

python -c "import urllib.request, json; response = urllib.request.urlopen('https://%FUNC_APP_NAME%.azurewebsites.net/api/health_simple', timeout=10); data = json.loads(response.read()); print('✅ SUCCESS:', data)"

echo.
echo ========================================
echo DEPLOYMENT COMPLETE
echo ========================================
echo.
echo Working URL: https://%FUNC_APP_NAME%.azurewebsites.net/api/health_simple
echo.

cd /d "C:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system"
rmdir /s /q "%DEPLOY_DIR%"
pause