@echo off
echo ================================================================
echo 🧠 L.I.F.E Platform - API Endpoint Test (October 18, 2025)
echo ================================================================
echo.
echo 🎯 Testing Function App: lifeplatform1760781933.azurewebsites.net
echo 📅 Date: %date% %time%
echo.

SET BASE_URL=https://lifeplatform1760781933.azurewebsites.net

echo 📝 Testing Base URL...
echo URL: %BASE_URL%
curl -I %BASE_URL% --connect-timeout 10
echo.

echo 📝 Testing API Endpoint: /api/validate-ingestion
echo URL: %BASE_URL%/api/validate-ingestion
curl -I %BASE_URL%/api/validate-ingestion --connect-timeout 10
echo.

echo 📝 Testing API Endpoint: /api/ingestion-stats  
echo URL: %BASE_URL%/api/ingestion-stats
curl -I %BASE_URL%/api/ingestion-stats --connect-timeout 10
echo.

echo 📝 Testing API Endpoint: /api/ingest-external-eeg
echo URL: %BASE_URL%/api/ingest-external-eeg
curl -I %BASE_URL%/api/ingest-external-eeg --connect-timeout 10
echo.

echo ================================================================
echo 🔍 Diagnosis: If you see "404 Not Found" errors, the Function App
echo    needs Python 3.13 upgrade. Run: deploy_python313.bat
echo.
echo 🚀 If you see "200 OK" responses, the API is working!
echo ================================================================
pause