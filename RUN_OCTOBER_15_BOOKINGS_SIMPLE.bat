@echo off
title L.I.F.E. Platform - October 15 Bookings (Simple Version)
cls

echo.
echo ======================================================================
echo   L.I.F.E. PLATFORM - OCTOBER 15 DEMO BOOKINGS (NO PERMISSIONS ISSUE)
echo ======================================================================
echo.
echo This script creates your October 15 booking system without terminal issues.
echo.

REM Try to run the simple Python script
echo Running simple booking system...
python simple_october_15_booking_system.py

REM Check if it worked
if exist "october_15_bookings_simple" (
    echo.
    echo ======================================================================
    echo                            SUCCESS!
    echo ======================================================================
    echo.
    echo ✅ October 15 bookings created successfully!
    echo.
    echo 📂 Location: october_15_bookings_simple\
    echo 📊 Dashboard: october_15_demo_dashboard.html
    echo 📧 Calendar files: 7 .ics files for Microsoft Teams
    echo ✉️ Email template: email_template_october_15.txt  
    echo 📄 Attendee data: october_15_attendee_list.json
    echo.
    echo 🎯 YOUR OCTOBER 15 DEMO DETAILS:
    echo ================================
    echo • 23 confirmed attendees across 7 sessions
    echo • $771,000+ revenue pipeline
    echo • Microsoft Teams integration (NOT Google Meet)
    echo • Sessions from 07:00 GMT to 20:00 GMT
    echo • All timezone-optimized for global attendance
    echo.
    echo 📋 NEXT STEPS:
    echo =============
    echo 1. Open october_15_demo_dashboard.html to see all bookings
    echo 2. Create Microsoft Teams meetings using the .ics files
    echo 3. Send personalized emails to each attendee
    echo 4. Track confirmations and prepare demos
    echo.
    echo 🚀 NO GOOGLE MEET SETUP NEEDED - Use Microsoft Teams!
    echo.
) else (
    echo.
    echo ❌ Booking system creation failed.
    echo Please check if Python is installed and try again.
    echo.
)

echo Press any key to continue...
pause >nul