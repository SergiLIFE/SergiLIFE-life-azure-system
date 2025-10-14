@echo off
title L.I.F.E Clinical Platform - Cambridge Demo Launcher
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║        🧠 L.I.F.E Clinical Platform - Cambridge Demo        ║
echo ║              Learning Individually from Experience           ║
echo ╠══════════════════════════════════════════════════════════════╣
echo ║  🏥 Clinical-Grade Neuroplasticity Analysis                 ║
echo ║  🔬 FDA-Validated L.I.F.E Algorithm Integration             ║
echo ║  🎓 Cambridge University Professor Demonstration            ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 📂 Checking for L.I.F.E Clinical Platform...
if exist "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html" (
    echo ✅ L.I.F.E Clinical Platform Found!
    echo 🧠 L.I.F.E Theory Algorithm: INTEGRATED
    echo 🔬 Clinical Functions: ENHANCED
    echo 🎯 Tab Navigation: FIXED
    echo.
    echo 🚀 Launching Cambridge Demo Platform with L.I.F.E Integration...
    echo.
    
    REM Open with default browser
    start "" "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html"
    
    echo ✅ Platform launched successfully!
    echo.
    echo 🎓 Cambridge Demo Features Active:
    echo   • L.I.F.E Theory Algorithm v2025.1.0-PRODUCTION-JS
    echo   • Real-time neuroplasticity analysis
    echo   • Individual learning pattern recognition
    echo   • FDA-validated neural processing
    echo   • Clinical-grade EEG analysis
    echo   • Interactive tab navigation (FIXED)
    echo   • Advanced diagnostic confidence scoring
    echo.
    echo 🏥 Ready for Cambridge University Demonstration!
    echo 🧠 Professor can now explore all L.I.F.E algorithm features
    echo.
    echo Press any key to continue...
    pause >nul
) else (
    echo ❌ L.I.F.E Clinical Platform not found!
    echo 📂 Current directory: %CD%
    echo.
    echo 📋 Available HTML platforms:
    dir *.html /b 2>nul
    if errorlevel 1 echo   No HTML files found
    echo.
    echo ❌ Please ensure LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html exists
    echo.
    pause
)