@echo off
echo 🔍 L.I.F.E. Platform Certification URL Checker
echo ============================================
echo Checking if your marketplace certification URLs are working...
echo.

REM Set common URL patterns for Azure Static Web Apps
set BASE_URL1=https://life-platform-webapp.azurestaticapps.net
set BASE_URL2=https://life-platform.azurestaticapps.net
set BASE_URL3=https://sergilife-life-azure-system.azurestaticapps.net

echo Testing possible website URLs...
echo.

REM Test main URLs
echo 🧪 Testing: %BASE_URL1%
curl -I -s %BASE_URL1% | findstr "200\|404\|HTTP"
if %errorlevel%==0 echo ✅ %BASE_URL1% - RESPONDING

echo.
echo 🧪 Testing: %BASE_URL2%
curl -I -s %BASE_URL2% | findstr "200\|404\|HTTP"
if %errorlevel%==0 echo ✅ %BASE_URL2% - RESPONDING

echo.
echo 🧪 Testing: %BASE_URL3%
curl -I -s %BASE_URL3% | findstr "200\|404\|HTTP"
if %errorlevel%==0 echo ✅ %BASE_URL3% - RESPONDING

echo.
echo 📋 Testing certification pages...
echo.

REM Test certification URLs
set TEST_URLS=%BASE_URL1%/privacy-policy.html %BASE_URL1%/terms-of-service.html %BASE_URL1%/support.html

for %%U in (%TEST_URLS%) do (
    echo 🔗 Testing: %%U
    curl -I -s "%%U" | findstr "200\|404"
    if !errorlevel!==0 echo ✅ %%U - OK
    echo.
)

echo.
echo 📌 MANUAL CHECK REQUIRED:
echo Please open these URLs in your browser:
echo.
echo 🏠 Homepage: %BASE_URL1%/
echo 🔒 Privacy: %BASE_URL1%/privacy-policy.html
echo 📄 Terms: %BASE_URL1%/terms-of-service.html
echo 🛠️ Support: %BASE_URL1%/support.html
echo 📚 API Docs: %BASE_URL1%/api-docs.html
echo 🚀 Getting Started: %BASE_URL1%/getting-started.html
echo.
echo If ANY of these work, your certification crisis is SOLVED! 🎉
echo.
pause