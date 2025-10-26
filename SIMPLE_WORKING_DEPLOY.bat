@echo off
echo ========================================
echo SIMPLE WORKING DEPLOYMENT
echo ========================================

REM Use the Function App we KNOW exists
set FUNC_APP_NAME=life-functions-app-prod
set RESOURCE_GROUP=life-platform-prod

echo Step 1: Verify Function App exists
az functionapp show --name %FUNC_APP_NAME% --resource-group %RESOURCE_GROUP% --query "name" --output tsv
if %ERRORLEVEL% neq 0 (
    echo ERROR: Function App not found
    pause
    exit /b 1
)
echo SUCCESS: Function App found

echo Step 2: Create simple deployment files
set TEMP_DIR=%USERPROFILE%\simple_deploy
if exist "%TEMP_DIR%" rmdir /s /q "%TEMP_DIR%"
mkdir "%TEMP_DIR%"
cd /d "%TEMP_DIR%"

echo Creating function_app.py...
echo import azure.functions as func > function_app.py
echo import json >> function_app.py
echo. >> function_app.py
echo app = func.FunctionApp() >> function_app.py
echo. >> function_app.py
echo @app.route(route="health", auth_level=func.AuthLevel.ANONYMOUS, methods=["GET"]) >> function_app.py
echo def health_check(req): >> function_app.py
echo     return func.HttpResponse(json.dumps({"status": "healthy", "app": "L.I.F.E Platform"}), mimetype="application/json") >> function_app.py

echo Creating host.json...
echo {"version": "2.0"} > host.json

echo Creating requirements.txt...
echo azure-functions > requirements.txt

echo Step 3: Deploy
tar -a -c -f deploy.zip function_app.py host.json requirements.txt
az functionapp deployment source config-zip --resource-group %RESOURCE_GROUP% --name %FUNC_APP_NAME% --src deploy.zip

echo Step 4: Wait and test
echo Waiting 90 seconds for deployment...
timeout /t 90 /nobreak >nul

echo Testing endpoint:
python -c "import urllib.request; import json; response = urllib.request.urlopen('https://life-functions-app-prod.azurewebsites.net/api/health', timeout=10); data = json.loads(response.read()); print('SUCCESS:', data)"

echo.
echo DEPLOYMENT COMPLETE
echo URL: https://life-functions-app-prod.azurewebsites.net/api/health
echo.

cd /d "C:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system"
rmdir /s /q "%TEMP_DIR%"
pause