@echo off
echo ========================================
echo TRADITIONAL v1 STRUCTURE DEPLOYMENT
echo ========================================

set FUNC_APP_NAME=life-functions-app-prod
set RESOURCE_GROUP=life-platform-prod

echo Creating traditional Azure Functions v1 structure...
set DEPLOY_DIR=%USERPROFILE%\traditional_deploy
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

REM Create health function folder
echo Creating health function folder...
mkdir health
cd health

REM Create function.json for health endpoint
echo Creating function.json...
(
echo {
echo   "scriptFile": "__init__.py",
echo   "bindings": [
echo     {
echo       "authLevel": "anonymous",
echo       "route": "health",
echo       "type": "httpTrigger",
echo       "direction": "in",
echo       "name": "req",
echo       "methods": ["get"]
echo     },
echo     {
echo       "type": "http",
echo       "direction": "out",
echo       "name": "$return"
echo     }
echo   ]
echo }
) > function.json

REM Create __init__.py with function code
echo Creating __init__.py...
(
echo import azure.functions as func
echo import json
echo import logging
echo.
echo def main^(req: func.HttpRequest^) -^> func.HttpResponse:
echo     logging.info^('Health check function processed a request.'^)
echo     return func.HttpResponse^(
echo         json.dumps^({"status": "healthy", "app": "L.I.F.E Platform", "structure": "v1"}^),
echo         mimetype="application/json"
echo     ^)
) > __init__.py

cd ..

REM Create health_simple function folder too
echo Creating health_simple function folder...
mkdir health_simple
cd health_simple

REM Create function.json for health_simple endpoint  
echo Creating function.json for health_simple...
(
echo {
echo   "scriptFile": "__init__.py",
echo   "bindings": [
echo     {
echo       "authLevel": "anonymous",
echo       "route": "health_simple",
echo       "type": "httpTrigger",
echo       "direction": "in",
echo       "name": "req",
echo       "methods": ["get"]
echo     },
echo     {
echo       "type": "http",
echo       "direction": "out",
echo       "name": "$return"
echo     }
echo   ]
echo }
) > function.json

REM Create __init__.py for health_simple
echo Creating __init__.py for health_simple...
(
echo import azure.functions as func
echo import json
echo import logging
echo.
echo def main^(req: func.HttpRequest^) -^> func.HttpResponse:
echo     logging.info^('Health simple function processed a request.'^)
echo     return func.HttpResponse^(
echo         json.dumps^({"status": "healthy", "app": "L.I.F.E Platform", "endpoint": "health_simple"}^),
echo         mimetype="application/json"
echo     ^)
) > __init__.py

cd ..

echo.
echo Deploying traditional structure...
tar -a -c -f traditional.zip host.json requirements.txt health health_simple
az functionapp deployment source config-zip --resource-group %RESOURCE_GROUP% --name %FUNC_APP_NAME% --src traditional.zip

echo.
echo Waiting 2 minutes for deployment...
timeout /t 120 /nobreak >nul

echo.
echo Testing both endpoints:
echo.
echo Testing /api/health:
python -c "import urllib.request; import json; try: response = urllib.request.urlopen('https://life-functions-app-prod.azurewebsites.net/api/health', timeout=10); data = json.loads(response.read()); print('✅ /api/health WORKS:', data); except Exception as e: print('❌ /api/health failed:', str(e))"

echo.
echo Testing /api/health_simple:
python -c "import urllib.request; import json; try: response = urllib.request.urlopen('https://life-functions-app-prod.azurewebsites.net/api/health_simple', timeout=10); data = json.loads(response.read()); print('✅ /api/health_simple WORKS:', data); except Exception as e: print('❌ /api/health_simple failed:', str(e))"

echo.
echo ========================================
echo DEPLOYMENT COMPLETE
echo ========================================
echo.
echo Working URLs:
echo https://life-functions-app-prod.azurewebsites.net/api/health
echo https://life-functions-app-prod.azurewebsites.net/api/health_simple
echo.

cd /d "C:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system"
rmdir /s /q "%DEPLOY_DIR%"
pause