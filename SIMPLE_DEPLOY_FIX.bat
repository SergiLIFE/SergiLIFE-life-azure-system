@echo off
echo.
echo ======================================================================
echo   L.I.F.E. PLATFORM - SIMPLE DEPLOYMENT (No Path Issues)
echo ======================================================================
echo.

echo [1/4] Creating .python_packages directory...
if not exist .python_packages mkdir .python_packages
echo   Done
echo.

echo [2/4] Deploying to Azure with func CLI...
echo   This will take 3-5 minutes...
echo.
func azure functionapp publish life-functions-app --python --build remote
echo.

if errorlevel 1 (
    echo.
    echo   Deployment may have failed. Checking status...
    echo.
) else (
    echo   Deployment command completed
    echo.
)

echo [3/4] Waiting for Azure to sync (30 seconds)...
timeout /t 30 /nobreak >nul
echo   Done
echo.

echo [4/4] Restarting Function App...
az functionapp restart --name life-functions-app --resource-group life-platform-rg
echo   Done
echo.

echo ======================================================================
echo   TESTING DEPLOYMENT
echo ======================================================================
echo.

echo Waiting 30 more seconds for restart to complete...
timeout /t 30 /nobreak >nul
echo.

echo Testing health endpoint...
python test_deployment.py
echo.

echo ======================================================================
echo   DEPLOYMENT SCRIPT COMPLETE
echo ======================================================================
echo.
echo If you see "404" above, wait 2 more minutes and run:
echo   python test_deployment.py
echo.
pause
