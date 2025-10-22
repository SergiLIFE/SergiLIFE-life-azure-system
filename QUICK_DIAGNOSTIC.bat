@echo off
echo ========================================
echo QUICK DIAGNOSTIC CHECK
echo ========================================

echo Step 1: Function App State
az functionapp show --name life-functions-app-prod --resource-group life-platform-prod --query "state" --output tsv

echo.
echo Step 2: Functions List  
az functionapp function list --name life-functions-app-prod --resource-group life-platform-prod --output table

echo.
echo Step 3: Test Health Endpoint
python -c "import urllib.request; print('Testing...'); response = urllib.request.urlopen('https://life-functions-app-prod.azurewebsites.net/api/health', timeout=10); print('Response:', response.read().decode())"

echo.
echo ========================================
echo Diagnostic Complete - Press Enter
echo ========================================
pause