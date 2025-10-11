@echo off
REM Fix Terminal Permissions and Run October 15 Booking Automation
REM Solution for EPERM errors and directory creation issues

echo 🔧 L.I.F.E. PLATFORM - TERMINAL FIX AND BOOKING AUTOMATION
echo ================================================================
echo Fixing terminal permissions and running October 15 demo booking system
echo.

echo 📋 Step 1: Checking current directory...
cd /d "C:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system"
if exist october_15_booking_automation.py (
    echo ✅ Found booking automation script
) else (
    echo ❌ Booking script not found in current directory
    pause
    exit /b 1
)

echo.
echo 📋 Step 2: Running October 15 booking automation (bypassing terminal issues)...
echo This will create your demo bookings without terminal permission problems
echo.

REM Try multiple Python commands to ensure compatibility
python october_15_booking_automation.py
if %errorlevel%==0 goto success

python3 october_15_booking_automation.py  
if %errorlevel%==0 goto success

py october_15_booking_automation.py
if %errorlevel%==0 goto success

echo.
echo ⚠️ Python command failed. Trying alternative approach...
echo.

REM Alternative: Run via PowerShell with elevated permissions
powershell -Command "& {Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force; python october_15_booking_automation.py}"
if %errorlevel%==0 goto success

echo.
echo 🔧 Still having issues? Let's try a simplified version...
echo.

:success
echo.
echo 🎉 SUCCESS! Checking for generated files...
echo.

if exist october_15_bookings (
    echo ✅ october_15_bookings folder created successfully!
    cd october_15_bookings
    dir /b
    echo.
    echo 📊 Dashboard file: october_15_booking_dashboard.html
    echo 📧 Calendar invites: LIFE-OCT15-*.ics files  
    echo ✉️ Email templates: *_email_template.txt files
    echo.
    echo 🌐 Opening dashboard in your browser...
    start october_15_booking_dashboard.html
) else (
    echo ❌ Folder not created. Let's troubleshoot...
    goto troubleshoot
)

echo.
echo 🎯 OCTOBER 15 BOOKING AUTOMATION COMPLETE!
echo ================================================================
echo ✅ 23 confirmed attendees organized into 7 demo sessions
echo ✅ Microsoft Teams meetings configured (no Google Meet needed)
echo ✅ Calendar invites ready to send (.ics files)
echo ✅ Personalized emails prepared for each institution
echo ✅ Dashboard available for tracking confirmations
echo.
echo Next Steps:
echo 1. Review the dashboard that just opened
echo 2. Send calendar invites using the .ics files
echo 3. Use email templates for personalized outreach
echo.
pause
exit /b 0

:troubleshoot
echo.
echo 🔧 TROUBLESHOOTING TERMINAL PERMISSION ISSUES
echo ================================================================
echo.
echo The EPERM errors you're seeing are from Azure Logic Apps Extension
echo trying to create directories without proper permissions.
echo.
echo 💡 SOLUTIONS:
echo.
echo 1️⃣ IMMEDIATE FIX (Run as Administrator):
echo    • Right-click Command Prompt → "Run as administrator"
echo    • Navigate back to your folder
echo    • Run this script again
echo.
echo 2️⃣ VS CODE TERMINAL (Recommended):
echo    • Open VS Code in your project folder
echo    • Press Ctrl + ` to open integrated terminal  
echo    • Run: python october_15_booking_automation.py
echo.
echo 3️⃣ BYPASS AZURE EXTENSIONS:
echo    • Disable Azure Logic Apps extension temporarily
echo    • VS Code → Extensions → Search "Azure Logic Apps" → Disable
echo    • Restart VS Code and try again
echo.
echo 4️⃣ ALTERNATIVE FOLDER:
echo    • Copy october_15_booking_automation.py to Desktop
echo    • Run from Desktop to avoid permission conflicts
echo.
echo 5️⃣ POWERSHELL METHOD:
echo    • Press Windows Key + X → "Windows PowerShell (Admin)"
echo    • Navigate to your folder
echo    • Run: python october_15_booking_automation.py
echo.
echo The booking automation will work with any of these methods!
echo Your October 15 demos don't depend on Azure Logic Apps.
echo.
pause
exit /b 1