@echo off
echo ======================================================================
echo  QUICK FULL DEPLOYMENT - Standardized Names
echo ======================================================================
echo.

REM Standardized resource names for all scripts
set FUNC_APP_NAME=life-functions-app-prod
set RESOURCE_GROUP=life-platform-prod

REM Step 1: Verify Function App exists before deploying
echo [VERIFY] Checking Function App existence...
echo Checking: %FUNC_APP_NAME% in %RESOURCE_GROUP%
az functionapp show --name %FUNC_APP_NAME% --resource-group %RESOURCE_GROUP% --query "name" --output tsv >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ ERROR: Function App '%FUNC_APP_NAME%' not found in '%RESOURCE_GROUP%'
    echo Available Function Apps:
    az functionapp list --resource-group %RESOURCE_GROUP% --query "[].name" --output table
    pause
    exit /b 1
)
echo ✅ Function App '%FUNC_APP_NAME%' verified exists

REM Step 2: Check if symlink exists before creating (avoid mklink errors)
if exist "C:\LIFE-Platform" (
    echo ℹ️  Symlink C:\LIFE-Platform already exists, skipping creation
) else (
    echo Creating symlink C:\LIFE-Platform...
    mklink /D "C:\LIFE-Platform" "C:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system"
)

REM Step 3: Use the EXACT same method that worked for health_simple
set TEMP_DEPLOY=%USERPROFILE%\life_quick_deploy
if exist "%TEMP_DEPLOY%" rmdir /s /q "%TEMP_DEPLOY%"
mkdir "%TEMP_DEPLOY%"
cd /d "%TEMP_DEPLOY%"

echo [1/3] Creating function_app.py with Python v2 model...

REM Create the Python v2 model function_app.py directly
echo import azure.functions as func > function_app.py
echo import json >> function_app.py
echo import logging >> function_app.py
echo from datetime import datetime, timezone >> function_app.py
echo. >> function_app.py
echo app = func.FunctionApp() >> function_app.py
echo. >> function_app.py
echo @app.route(route="health", auth_level=func.AuthLevel.ANONYMOUS, methods=["GET"]) >> function_app.py
echo async def health_check(req: func.HttpRequest) -^> func.HttpResponse: >> function_app.py
echo     return func.HttpResponse( >> function_app.py
echo         json.dumps({"status": "healthy", "platform": "L.I.F.E Platform", "version": "2.0.0"}), >> function_app.py
echo         mimetype="application/json" >> function_app.py
echo     ) >> function_app.py
echo. >> function_app.py
echo @app.route(route="eeg/process", auth_level=func.AuthLevel.FUNCTION, methods=["POST"]) >> function_app.py
echo async def eeg_processor(req: func.HttpRequest) -^> func.HttpResponse: >> function_app.py
echo     return func.HttpResponse( >> function_app.py
echo         json.dumps({"status": "success", "message": "EEG processor ready"}), >> function_app.py
echo         mimetype="application/json" >> function_app.py
echo     ) >> function_app.py

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

echo [2/3] Creating ZIP and deploying...
tar -a -c -f deployment.zip function_app.py requirements.txt host.json

REM Deploy using standardized names
echo Deploying to: %FUNC_APP_NAME% in %RESOURCE_GROUP%
az functionapp deployment source config-zip --resource-group %RESOURCE_GROUP% --name %FUNC_APP_NAME% --src deployment.zip

if %ERRORLEVEL% neq 0 (
    echo ❌ Deployment failed! Check Azure CLI output above.
    pause
    exit /b 1
)
echo ✅ Deployment command completed successfully

echo [3/3] Testing after 60 seconds...
timeout /t 60 /nobreak >nul

echo Testing health endpoint:
python -c "import urllib.request; import json; response = urllib.request.urlopen('https://%FUNC_APP_NAME%.azurewebsites.net/api/health', timeout=10); data = json.loads(response.read()); print('✅ SUCCESS:', data)" 2>nul || echo "❌ Health test failed"

echo.
echo ======================================================================
echo  DEPLOYMENT COMPLETE - L.I.F.E Platform v2.0
echo ======================================================================
echo.
echo Health: https://%FUNC_APP_NAME%.azurewebsites.net/api/health
echo EEG:    https://%FUNC_APP_NAME%.azurewebsites.net/api/eeg/process
echo.

cd /d "C:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system"
rmdir /s /q "%TEMP_DEPLOY%"
pause