@echo off
echo ========================================
echo QUICK STATUS CHECK
echo ========================================

echo Testing current endpoints...
echo.

echo [1] Testing /api/health:
python -c "import urllib.request; import json; try: response = urllib.request.urlopen('https://life-functions-app-prod.azurewebsites.net/api/health', timeout=10); data = json.loads(response.read()); print('✅ SUCCESS:', data); except Exception as e: print('❌ FAILED:', str(e))"

echo.
echo [2] Testing /api/health_simple:
python -c "import urllib.request; import json; try: response = urllib.request.urlopen('https://life-functions-app-prod.azurewebsites.net/api/health_simple', timeout=10); data = json.loads(response.read()); print('✅ SUCCESS:', data); except Exception as e: print('❌ FAILED:', str(e))"

echo.
echo [3] Testing Function App base URL:
python -c "import urllib.request; try: response = urllib.request.urlopen('https://life-functions-app-prod.azurewebsites.net', timeout=10); print('✅ Function App is reachable'); except Exception as e: print('❌ Function App not reachable:', str(e))"

echo.
echo [4] Listing deployed functions:
az functionapp function list --name life-functions-app-prod --resource-group life-platform-prod --output table

echo.
echo ========================================
echo STATUS CHECK COMPLETE
echo ========================================
pause