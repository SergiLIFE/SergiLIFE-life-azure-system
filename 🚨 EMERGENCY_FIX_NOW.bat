@echo off
cls
echo ================================================================
echo 🚨 EMERGENCY PLATFORM FIX - October 11, 2025
echo ================================================================
echo Target: Fix Azure Static Web App showing default Microsoft page
echo Demo: October 15, 2025 ^| 23 Participants ^| $771K+ Pipeline
echo ================================================================
echo.

echo 🔍 Current Issue: Platform showing "Congratulations on your new site!"
echo 🎯 Target: L.I.F.E. Platform interface with October 15 countdown
echo 📍 URL: https://green-ground-0c65efe0f.1.azurestaticapps.net

echo.
echo 🚀 STEP 1: Adding emergency deployment timestamp...
echo ^<!-- Emergency Fix: %date% %time% --^> >> index.html

echo.
echo 📝 STEP 2: Committing changes...
git add index.html
git commit -m "🚨 EMERGENCY FIX: Force redeploy - Platform showing Microsoft default page instead of L.I.F.E. interface"

echo.
echo 🌐 STEP 3: Pushing to GitHub (triggers Azure deployment)...
git push origin main

echo.
echo ⏱️  STEP 4: Deployment initiated! 
echo Expected processing time: 2-5 minutes
echo Monitor: https://github.com/SergiLIFE/SergiLIFE-life-azure-system/actions

echo.
echo 🔄 STEP 5: Testing deployment...
echo Please wait 3 minutes, then test these URLs:

echo.
echo Primary URL (refresh with Ctrl+F5):
echo https://green-ground-0c65efe0f.1.azurestaticapps.net
echo.
echo Alternative test URLs:
echo https://green-ground-0c65efe0f.1.azurestaticapps.net/index.html
echo https://green-ground-0c65efe0f.1.azurestaticapps.net/?v=oct11

echo.
echo 📋 SUCCESS CRITERIA:
echo ✅ Platform shows L.I.F.E. interface (not Microsoft default)
echo ✅ "October 15, 2025" countdown visible
echo ✅ "23 Participants" messaging displayed
echo ✅ EEG animations working

echo.
echo 🎯 If this fix works, your October 15 demo is ready!
echo 🔧 If still showing default page, run alternative solutions.

echo.
echo ================================================================
echo 🚨 EMERGENCY FIX DEPLOYED - CHECK PLATFORM IN 3 MINUTES!
echo ================================================================
pause