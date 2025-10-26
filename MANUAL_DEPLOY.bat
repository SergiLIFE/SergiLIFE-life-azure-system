@echo off
echo ======================================================================
echo  MANUAL DEPLOYMENT - Copy and Deploy Files
echo ======================================================================

REM Copy files to temp directory
set DEPLOY_DIR=%USERPROFILE%\manual_deploy
if exist "%DEPLOY_DIR%" rmdir /s /q "%DEPLOY_DIR%"
mkdir "%DEPLOY_DIR%"

copy "function_app_v2.py" "%DEPLOY_DIR%\function_app.py"
copy "host_v2.json" "%DEPLOY_DIR%\host.json"
copy "requirements_v2.txt" "%DEPLOY_DIR%\requirements.txt"

cd /d "%DEPLOY_DIR%"

REM Create ZIP
tar -a -c -f deployment.zip function_app.py host.json requirements.txt

REM Deploy
echo Deploying to life-func-12525...
az functionapp deployment source config-zip --resource-group life-platform-prod --name life-func-12525 --src deployment.zip

echo.
echo Deployment complete! Testing in 60 seconds...
timeout /t 60 /nobreak >nul

echo Testing health endpoint:
python -c "import urllib.request; import json; response = urllib.request.urlopen('https://life-func-12525.azurewebsites.net/api/health', timeout=10); data = json.loads(response.read()); print('SUCCESS:', data)" 2>nul || echo "Health test failed"

echo.
echo Endpoints:
echo Health: https://life-func-12525.azurewebsites.net/api/health
echo EEG:    https://life-func-12525.azurewebsites.net/api/eeg/process

cd /d "C:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system"
rmdir /s /q "%DEPLOY_DIR%"
pause