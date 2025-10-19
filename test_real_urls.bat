@echo off
echo ================================================================
echo 🔍 L.I.F.E Platform - REAL URL Testing (October 18, 2025)
echo ================================================================
echo Testing actual Azure deployment URLs to find what works...
echo.

echo 📝 Testing Main Function App Base URL...
curl -I "https://lifeplatform1760781933.azurewebsites.net" --connect-timeout 5 --max-time 10
echo.

echo 📝 Testing Legacy Function App...
curl -I "https://life-theory-functions-1756511146.azurewebsites.net" --connect-timeout 5 --max-time 10
echo.

echo 📝 Testing Enhanced Dashboard Function App...
curl -I "https://life-functions-app.azurewebsites.net" --connect-timeout 5 --max-time 10
echo.

echo 📝 Testing Azure Static Web App...
curl -I "https://green-ground-0c65efe0f.1.azurestaticapps.net" --connect-timeout 5 --max-time 10
echo.

echo 📝 Testing Alternative Static Web App...
curl -I "https://life-platform-webapp.azurestaticapps.net" --connect-timeout 5 --max-time 10
echo.

echo ================================================================
echo 🎯 API Endpoint Tests (might return 404 if not configured)
echo ================================================================

echo 📝 Testing Main API Validate Endpoint...
curl -I "https://lifeplatform1760781933.azurewebsites.net/api/validate-ingestion" --connect-timeout 5 --max-time 10
echo.

echo 📝 Testing Dashboard API...
curl -I "https://life-functions-app.azurewebsites.net/api/dashboard" --connect-timeout 5 --max-time 10
echo.

echo ================================================================
echo 💡 SUMMARY: Look for "200 OK" responses above
echo    - 200 OK = Working URL
echo    - 404 Not Found = Deployed but endpoint missing  
echo    - Connection refused/timeout = URL doesn't exist
echo ================================================================
pause