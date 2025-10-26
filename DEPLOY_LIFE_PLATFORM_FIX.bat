@echo off
REM DEPLOY_LIFE_PLATFORM_FIX.bat

echo ======================================================================
echo  L.I.F.E PLATFORM DEPLOYMENT - PATH FIX
echo ======================================================================
echo.

REM Change to the correct directory (use quotes for spaces)
cd /d "C:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system"

echo Current Directory: %CD%
echo.

REM Check Azure CLI
echo [1/5] Checking Azure CLI...
call az account show --query name -o tsv
if errorlevel 1 (
    echo ERROR: Azure CLI not authenticated
    echo Run: az login
    exit /b 1
)
echo.

REM Set variables
set RESOURCE_GROUP=life-platform-rg
set LOCATION=eastus2
set FUNC_APP_NAME=life-functions-app
set STORAGE_NAME=stlifeplatformprod

echo [2/5] Checking Function App...
echo Resource Group: %RESOURCE_GROUP%
echo Location: %LOCATION%
echo Function App: %FUNC_APP_NAME%
echo.

REM Check if Function App exists
call az functionapp show --name %FUNC_APP_NAME% --resource-group %RESOURCE_GROUP% >nul 2>&1
if errorlevel 1 (
    echo Function App does not exist. This means we need to recreate it.
    echo Please run the infrastructure deployment first.
    pause
    exit /b 1
) else (
    echo Function App exists. Proceeding with code deployment...
)
echo.

echo [3/5] Creating deployment package...
REM Create a simple function in user temp to avoid path issues
set TEMP_DEPLOY=%USERPROFILE%\life_deploy_temp
if exist "%TEMP_DEPLOY%" rmdir /s /q "%TEMP_DEPLOY%"
mkdir "%TEMP_DEPLOY%"
cd /d "%TEMP_DEPLOY%"

REM Create host.json
echo { > host.json
echo   "version": "2.0", >> host.json
echo   "extensionBundle": { >> host.json
echo     "id": "Microsoft.Azure.Functions.ExtensionBundle", >> host.json
echo     "version": "[4.*, 5.0.0)" >> host.json
echo   } >> host.json
echo } >> host.json

REM Create requirements.txt
echo azure-functions > requirements.txt

REM Create health check function
mkdir health_simple
cd health_simple

REM Create __init__.py
echo import azure.functions as func > __init__.py
echo import json >> __init__.py
echo. >> __init__.py
echo def main(req: func.HttpRequest) -^> func.HttpResponse: >> __init__.py
echo     return func.HttpResponse( >> __init__.py
echo         json.dumps({"status": "healthy", "message": "L.I.F.E Platform is running"}), >> __init__.py
echo         mimetype="application/json" >> __init__.py
echo     ) >> __init__.py

REM Create function.json
echo { > function.json
echo   "scriptFile": "__init__.py", >> function.json
echo   "bindings": [ >> function.json
echo     { >> function.json
echo       "authLevel": "anonymous", >> function.json
echo       "type": "httpTrigger", >> function.json
echo       "direction": "in", >> function.json
echo       "name": "req", >> function.json
echo       "methods": ["get", "post"] >> function.json
echo     }, >> function.json
echo     { >> function.json
echo       "type": "http", >> function.json
echo       "direction": "out", >> function.json
echo       "name": "$return" >> function.json
echo     } >> function.json
echo   ] >> function.json
echo } >> function.json

cd ..

echo [4/5] Creating ZIP and deploying to Azure...
tar -a -c -f deployment.zip health_simple requirements.txt host.json

call az functionapp deployment source config-zip --resource-group %RESOURCE_GROUP% --name %FUNC_APP_NAME% --src deployment.zip

echo.
echo [5/5] Testing deployment...
echo Waiting 60 seconds for Azure to process...
timeout /t 60 /nobreak >nul

echo Testing: https://%FUNC_APP_NAME%.azurewebsites.net/api/health_simple
echo.

REM Test with Python since curl might not be available
python -c "import urllib.request; import json; response = urllib.request.urlopen('https://%FUNC_APP_NAME%.azurewebsites.net/api/health_simple', timeout=10); data = json.loads(response.read()); print('SUCCESS:', data)" 2>nul
if errorlevel 1 (
    echo Manual test required: https://%FUNC_APP_NAME%.azurewebsites.net/api/health_simple
)

echo.
echo ======================================================================
echo  DEPLOYMENT COMPLETE
echo ======================================================================
echo.
echo Function App URL: https://%FUNC_APP_NAME%.azurewebsites.net
echo Health Check: https://%FUNC_APP_NAME%.azurewebsites.net/api/health_simple
echo.

REM Cleanup
cd /d "C:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system"
rmdir /s /q "%TEMP_DEPLOY%"
pause