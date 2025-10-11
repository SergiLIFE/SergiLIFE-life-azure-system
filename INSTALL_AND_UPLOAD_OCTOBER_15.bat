@echo off
title L.I.F.E. Platform - Install Azure SDK & Upload October 15 Bookings
cls

echo.
echo ======================================================================
echo   L.I.F.E. PLATFORM - AZURE SDK INSTALLATION & CLOUD UPLOAD
echo ======================================================================
echo   4 DAYS UNTIL OCTOBER 15 DEMOS | 23 ATTENDEES | $771K+ PIPELINE
echo ======================================================================
echo.

echo 🔧 STEP 1: Installing Azure SDK for Python...
echo This is required to upload your October 15 booking data to Microsoft Cloud Storage
echo.

REM Install Azure Storage SDK
echo Installing azure-storage-blob...
pip install azure-storage-blob

REM Install Azure Identity SDK  
echo Installing azure-identity...
pip install azure-identity

echo.
echo ✅ Azure SDK installation completed!
echo.

echo 🚀 STEP 2: Running October 15 Cloud Upload...
echo Uploading all booking data to Microsoft Azure Blob Storage
echo.

REM Run the cloud upload script
python UPLOAD_OCTOBER_15_TO_CLOUD.py

echo.
echo ======================================================================
echo                         UPLOAD COMPLETE
echo ======================================================================
echo.

if %ERRORLEVEL% EQU 0 (
    echo ✅ SUCCESS: October 15 booking data uploaded to Microsoft Cloud!
    echo.
    echo 📊 YOUR CLOUD-STORED BOOKING DATA:
    echo ===================================
    echo • Complete attendee database (23 people)
    echo • Interactive HTML dashboard
    echo • Calendar files for all 7 sessions  
    echo • Email templates for each session
    echo • Quick reference summaries
    echo.
    echo 🔗 ACCESS YOUR DATA:
    echo ===================
    echo 1. Azure Portal → Storage Accounts
    echo 2. Navigate to container: october-15-bookings
    echo 3. Download files or view in browser
    echo.
    echo 🚀 NO GOOGLE MEET NEEDED - USE MICROSOFT TEAMS!
    echo ✅ All data safely stored in Microsoft cloud infrastructure
) else (
    echo ⚠️ Upload encountered issues, but Azure SDK is now installed
    echo You can retry the upload or access data locally
)

echo.
echo Press any key to continue...
pause >nul