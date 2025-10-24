@echo off
echo ========================================
echo 🔐 L.I.F.E PLATFORM - GitHub Secrets Setup Guide
echo ========================================
echo Revenue Target: $345K Q4 2025 → $50.7M by 2029
echo Azure Marketplace ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
echo.

echo [STEP 1] Opening GitHub Repository Secrets Page...
echo.
echo Opening: https://github.com/SergiLIFE/SergiLIFE-life-azure-system/settings/secrets/actions
start "" "https://github.com/SergiLIFE/SergiLIFE-life-azure-system/settings/secrets/actions"
timeout /t 3 >nul

echo.
echo [STEP 2] Azure Service Principal Instructions
echo.
echo 🌐 Open Azure Cloud Shell: https://shell.azure.com
echo    OR use local Azure CLI if installed
echo.
echo 📋 Run this command to create service principal:
echo.
echo az ad sp create-for-rbac \
echo   --name "sp-life-platform-staging" \
echo   --role "Contributor" \
echo   --scopes "/subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca" \
echo   --sdk-auth
echo.
echo ⚠️  IMPORTANT: Copy the ENTIRE JSON output from the command above
echo.

echo [STEP 3] Configure These 5 GitHub Secrets:
echo.
echo 🔑 Secret 1: AZURE_CREDENTIALS
echo    Value: [Paste the entire JSON output from Step 2]
echo.
echo 🔑 Secret 2: AZURE_SUBSCRIPTION_ID
echo    Value: 5c88cef6-f243-497d-98af-6c6086d575ca
echo.
echo 🔑 Secret 3: AZURE_RG_STAGING
echo    Value: life-platform-staging-rg
echo.
echo 🔑 Secret 4: AZURE_WEBAPP_NAME_STAGING
echo    Value: life-platform-staging
echo.
echo 🔑 Secret 5: AZURE_LOCATION
echo    Value: eastus2
echo.

echo [STEP 4] Trigger Deployment
echo.
echo After configuring all 5 secrets, run:
echo.
echo git add .
echo git commit -m "L.I.F.E Platform staging deployment ready"
echo git push origin main
echo.

echo [STEP 5] Monitor Deployment
echo.
echo 📊 GitHub Actions: https://github.com/SergiLIFE/SergiLIFE-life-azure-system/actions
echo 🏥 Health Check: https://life-platform-staging.azurewebsites.net/health
echo.

echo ========================================
echo 📋 QUICK REFERENCE
echo ========================================
echo.
echo ✅ GitHub Secrets URL:
echo https://github.com/SergiLIFE/SergiLIFE-life-azure-system/settings/secrets/actions
echo.
echo ✅ Azure Cloud Shell:
echo https://shell.azure.com
echo.
echo ✅ Expected Health Response:
echo {"status": "healthy", "platform": "L.I.F.E Platform", "environment": "staging"}
echo.
echo ✅ Business Impact:
echo • Enables $345K Q4 2025 revenue target
echo • Validates $50.7M by 2029 scaling pathway  
echo • First neuroadaptive learning platform on Azure Marketplace
echo.

echo 🎯 TROUBLESHOOTING
echo.
echo If service principal creation fails:
echo 1. Try a different name: sp-life-platform-staging-YYYYMMDD
echo 2. Check Azure permissions (must be Owner or Contributor)
echo 3. Verify subscription ID is correct
echo.
echo If GitHub Actions fails:
echo 1. Verify all 5 secrets are configured correctly
echo 2. Check AZURE_CREDENTIALS is valid JSON
echo 3. Ensure service principal has Contributor role
echo.

echo ========================================
echo ✅ L.I.F.E PLATFORM STAGING DEPLOYMENT READY!
echo ========================================
echo.
echo 🚀 Next: Configure GitHub secrets and push to deploy
echo 💰 Revenue: $345K Q4 2025 → $50.7M by 2029
echo 🎯 Status: Production-ready neuroadaptive learning platform
echo.

echo Would you like to open the detailed configuration guide? (Y/N)
set /p openGuide="Press Y to open GITHUB_SECRETS_CONFIGURATION_GUIDE.md: "
if /i "%openGuide%"=="Y" (
    start "" "GITHUB_SECRETS_CONFIGURATION_GUIDE.md"
)

echo.
echo 🎉 Setup guide complete! Ready for L.I.F.E Platform deployment.
pause