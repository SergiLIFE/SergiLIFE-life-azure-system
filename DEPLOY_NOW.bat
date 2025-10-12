@echo off
echo 🚀 L.I.F.E. Platform Force Deployment - January 10, 2025 16:45 UTC
echo 📅 Target Demo: October 15, 2025 ^| 23 Participants ^| $771K+ Pipeline
echo.

cd /d "%~dp0"
echo 📍 Working Directory: %CD%

echo.
echo 🔍 Checking Git Status:
git status

echo.
echo 📝 Adding changes:
git add index.html force_deploy.ps1 EMERGENCY_DEPLOYMENT_STATUS.md

echo.
echo 💾 Committing changes:
git commit -m "🚀 FORCE DEPLOY: L.I.F.E. Platform January 10, 2025 16:45 UTC - October 15 Demo Ready"

echo.
echo 🌐 Pushing to GitHub:
git push origin main

echo.
echo ✅ DEPLOYMENT TRIGGERED!
echo.
echo 🎯 Next Steps:
echo 1. Monitor GitHub Actions: https://github.com/SergiLIFE/SergiLIFE-life-azure-system/actions
echo 2. Wait 2-5 minutes for Azure Static Web App rebuild
echo 3. Verify platform: https://green-ground-0c65efe0f.1.azurestaticapps.net
echo 4. Demo ready for October 15, 2025!

echo.
pause