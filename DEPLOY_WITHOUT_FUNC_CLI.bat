@echo off
echo ============================================================
echo  L.I.F.E PLATFORM - DEPLOY VIA AZURE CLI (NO FUNC NEEDED)
echo ============================================================
echo.
echo This will deploy your Function App using Azure CLI only
echo No need for Azure Functions Core Tools!
echo.
echo ============================================================
echo.

REM Step 1: Create deployment package
echo [1/4] Creating deployment package...
echo.

REM Create a temporary directory for deployment files
if not exist "temp_deploy" mkdir temp_deploy

REM Copy necessary files
echo   Copying files...
copy function_app.py temp_deploy\ >nul
copy host.json temp_deploy\ >nul
copy requirements.txt temp_deploy\ >nul
copy azure_config.py temp_deploy\ >nul 2>nul
copy experimentP2L*.py temp_deploy\ >nul 2>nul
copy venturi_gates_system.py temp_deploy\ >nul 2>nul
copy lifetheory.py temp_deploy\ >nul 2>nul

echo   ✅ Files copied
echo.

REM Step 2: Create ZIP package
echo [2/4] Creating ZIP package...
powershell -Command "Compress-Archive -Path temp_deploy\* -DestinationPath deployment.zip -Force"
if %errorlevel% == 0 (
    echo   ✅ deployment.zip created
) else (
    echo   ❌ Failed to create ZIP
    goto cleanup
)
echo.

REM Step 3: Deploy to Azure
echo [3/4] Deploying to Azure Function App...
echo   This may take 2-3 minutes...
echo.
az functionapp deployment source config-zip --resource-group life-platform-rg --name life-functions-app --src deployment.zip

if %errorlevel% == 0 (
    echo.
    echo   ✅ Deployment successful!
) else (
    echo.
    echo   ❌ Deployment failed
    echo   Check if you're logged in to Azure: az login
    goto cleanup
)
echo.

REM Step 4: Verify deployment
echo [4/4] Verifying deployment...
echo.
az functionapp show --name life-functions-app --resource-group life-platform-rg --query "state" --output tsv
echo.

REM Cleanup
:cleanup
echo [Cleanup] Removing temporary files...
if exist "temp_deploy" rmdir /s /q temp_deploy
if exist "deployment.zip" del deployment.zip
echo   ✅ Cleanup complete
echo.

echo ============================================================
echo  DEPLOYMENT COMPLETE
echo ============================================================
echo.
echo Your Function App URL:
echo   https://life-functions-app.azurewebsites.net
echo.
echo Test the health endpoint:
echo   curl https://life-functions-app.azurewebsites.net/api/health
echo.
echo View logs:
echo   az webapp log tail --name life-functions-app --resource-group life-platform-rg
echo.
echo ============================================================
pause
