@echo off
echo ======================================================================
echo  VERIFIED DEPLOYMENT - Check Function App First
echo ======================================================================
echo.

REM Step 1: Verify Function App exists before deploying
echo [1/4] Verifying Function App exists...
az functionapp show --name life-functions-app-prod --resource-group life-platform-prod --query "name" --output tsv >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ ERROR: Function App 'life-functions-app-prod' not found in 'life-platform-prod'
    echo Available Function Apps:
    az functionapp list --resource-group life-platform-prod --query "[].name" --output table
    pause
    exit /b 1
)
echo ✅ Function App 'life-functions-app-prod' verified

REM Step 2: Create deployment directory (no symlinks needed)
echo [2/4] Preparing deployment files...
set DEPLOY_DIR=%USERPROFILE%\verified_deploy_%DATE:~-4,4%%DATE:~-10,2%%DATE:~-7,2%_%TIME:~0,2%%TIME:~3,2%
set DEPLOY_DIR=%DEPLOY_DIR: =0%
if exist "%DEPLOY_DIR%" rmdir /s /q "%DEPLOY_DIR%"
mkdir "%DEPLOY_DIR%"
cd /d "%DEPLOY_DIR%"

REM Step 3: Create Python v2 Function App files
echo Creating function_app.py...
(
echo import azure.functions as func
echo import json
echo.
echo app = func.FunctionApp^(^)
echo.
echo @app.route^(route="health", auth_level=func.AuthLevel.ANONYMOUS, methods=["GET"]^)
echo async def health_check^(req: func.HttpRequest^) -^> func.HttpResponse:
echo     return func.HttpResponse^(
echo         json.dumps^({"status": "healthy", "platform": "L.I.F.E Platform", "version": "2.0.0"}^),
echo         mimetype="application/json"
echo     ^)
echo.
echo @app.route^(route="eeg/process", auth_level=func.AuthLevel.FUNCTION, methods=["POST"]^)
echo async def eeg_processor^(req: func.HttpRequest^) -^> func.HttpResponse:
echo     return func.HttpResponse^(
echo         json.dumps^({"status": "success", "message": "EEG processor ready"}^),
echo         mimetype="application/json"
echo     ^)
) > function_app.py

echo Creating host.json...
(
echo {
echo   "version": "2.0",
echo   "extensionBundle": {
echo     "id": "Microsoft.Azure.Functions.ExtensionBundle",
echo     "version": "[4.*, 5.0.0)"
echo   }
echo }
) > host.json

echo Creating requirements.txt...
echo azure-functions > requirements.txt

REM Step 4: Deploy to verified Function App
echo [3/4] Creating ZIP and deploying to VERIFIED Function App...
tar -a -c -f deployment.zip function_app.py host.json requirements.txt

echo Deploying to: life-functions-app-prod (verified exists)
az functionapp deployment source config-zip --resource-group life-platform-prod --name life-functions-app-prod --src deployment.zip

if %ERRORLEVEL% neq 0 (
    echo ❌ Deployment failed
    pause
    exit /b 1
)

REM Step 5: Test deployment
echo [4/4] Testing deployment after 60 seconds...
timeout /t 60 /nobreak >nul

echo Testing health endpoint (anonymous access):
python -c "import urllib.request; import json; response = urllib.request.urlopen('https://life-functions-app-prod.azurewebsites.net/api/health', timeout=15); data = json.loads(response.read()); print('✅ HEALTH SUCCESS:', data)" 2>nul || echo "❌ Health endpoint test failed"

echo.
echo ======================================================================
echo  DEPLOYMENT COMPLETE - Verified Function App
echo ======================================================================
echo.
echo ✅ Function App: life-functions-app-prod (verified exists)
echo ✅ Resource Group: life-platform-prod (verified exists)
echo.
echo 🌐 Health (anonymous): https://life-functions-app-prod.azurewebsites.net/api/health
echo 🔒 EEG (auth required): https://life-functions-app-prod.azurewebsites.net/api/eeg/process
echo.
echo Next: Retrieve function keys for EEG endpoint access
echo Command: az functionapp keys list --name life-functions-app-prod --resource-group life-platform-prod
echo.

REM Cleanup and return to workspace
cd /d "C:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system"
rmdir /s /q "%DEPLOY_DIR%"
pause