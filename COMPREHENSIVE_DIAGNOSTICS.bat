@echo off
setlocal enabledelayedexpansion

echo ========================================
echo COMPREHENSIVE AZURE FUNCTION DIAGNOSTICS
echo ========================================
echo Date/Time: %DATE% %TIME%
echo.

set FUNC_APP_NAME=life-functions-app-prod
set RESOURCE_GROUP=life-platform-prod
set BASE_URL=https://%FUNC_APP_NAME%.azurewebsites.net

echo [1] CHECKING FUNCTION APP STATUS...
echo.
az functionapp show --name %FUNC_APP_NAME% --resource-group %RESOURCE_GROUP% --query "{name:name, state:state, kind:kind, enabled:siteConfig.enabled}" --output table
echo.

echo [2] LISTING DEPLOYED FUNCTIONS...
echo.
az functionapp function list --name %FUNC_APP_NAME% --resource-group %RESOURCE_GROUP% --output table
echo.

echo [3] CHECKING FUNCTION APP LOGS...
echo.
az functionapp log tail --name %FUNC_APP_NAME% --resource-group %RESOURCE_GROUP% --timeout 10
echo.

echo [4] TESTING BASE URL CONNECTIVITY...
echo.
curl -v %BASE_URL% --connect-timeout 15 --max-time 30
echo.

echo [5] TESTING HEALTH ENDPOINTS...
echo.
echo Testing %BASE_URL%/api/health
curl -v %BASE_URL%/api/health --connect-timeout 15 --max-time 30
echo.
echo.

echo Testing %BASE_URL%/api/health_simple  
curl -v %BASE_URL%/api/health_simple --connect-timeout 15 --max-time 30
echo.
echo.

echo [6] CHECKING DEPLOYMENT STATUS...
echo.
az functionapp deployment list --name %FUNC_APP_NAME% --resource-group %RESOURCE_GROUP% --output table
echo.

echo [7] CHECKING FUNCTION APP SETTINGS...
echo.
az functionapp config appsettings list --name %FUNC_APP_NAME% --resource-group %RESOURCE_GROUP% --output table
echo.

echo [8] PYTHON TEST (if curl failed)...
echo.
python -c "
import urllib.request
import urllib.error
import json

urls = [
    'https://%FUNC_APP_NAME%.azurewebsites.net',
    'https://%FUNC_APP_NAME%.azurewebsites.net/api/health', 
    'https://%FUNC_APP_NAME%.azurewebsites.net/api/health_simple'
]

for url in urls:
    print(f'Testing: {url}')
    try:
        response = urllib.request.urlopen(url, timeout=30)
        content = response.read().decode('utf-8')
        print(f'  ✅ Status: {response.getcode()}')
        print(f'  📄 Content: {content[:200]}...' if len(content) > 200 else f'  📄 Content: {content}')
    except urllib.error.HTTPError as e:
        print(f'  ❌ HTTP Error: {e.code} - {e.reason}')
        try:
            error_content = e.read().decode('utf-8')
            print(f'  📄 Error Content: {error_content[:200]}...' if len(error_content) > 200 else f'  📄 Error Content: {error_content}')
        except:
            pass
    except Exception as e:
        print(f'  ❌ Error: {str(e)}')
    print()
"

echo.
echo ========================================
echo DIAGNOSTICS COMPLETE
echo ========================================
echo.
echo If functions are listed but URLs return errors:
echo - Check if Function App is in 'Running' state
echo - Verify deployment completed successfully  
echo - Check function trigger configuration
echo.
echo If no functions are listed:
echo - Deployment may have failed
echo - Need to redeploy with correct structure
echo.
pause