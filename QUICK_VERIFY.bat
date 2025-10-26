@echo off
echo ========================================
echo QUICK ENDPOINT VERIFICATION
echo ========================================
echo.

echo Testing: https://life-functions-app-prod.azurewebsites.net/api/health_simple
echo.

python -c "import urllib.request, urllib.error, json; url='https://life-functions-app-prod.azurewebsites.net/api/health_simple'; print('Testing:', url); response = urllib.request.urlopen(url, timeout=30); data = json.loads(response.read()); print('✅ SUCCESS! Response:', data)"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ ENDPOINT IS WORKING!
    echo The health_simple function is responding correctly.
) else (
    echo.
    echo ❌ ENDPOINT FAILED
    echo The function may still be deploying or there's a configuration issue.
)

echo.
echo Direct URL to test in browser:
echo https://life-functions-app-prod.azurewebsites.net/api/health_simple
echo.
pause