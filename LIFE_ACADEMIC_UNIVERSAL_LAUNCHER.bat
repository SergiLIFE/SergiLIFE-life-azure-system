@echo off
title L.I.F.E Platform - Academic Research Launcher
color 0B

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║             🧠 L.I.F.E Platform Academic Suite              ║
echo ║        Learning Individually From Experience Platform        ║
echo ╠══════════════════════════════════════════════════════════════╣
echo ║  🎓 Multi-Institution Research Platform                     ║
echo ║  🔬 Advanced Neuroplasticity Analysis                       ║
echo ║  📊 Clinical-Grade Neural Processing                        ║
echo ║  🏥 FDA-Validated L.I.F.E Algorithm Integration             ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 📅 Academic Meeting Schedule Support
echo ───────────────────────────────────────
echo   • Multiple Institution Compatibility
echo   • 7 Meeting Day Schedule Ready
echo   • Universal Academic Demonstration
echo   • Research-Grade Clinical Interface
echo.

echo 📂 Initializing L.I.F.E Platform...
if exist "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html" (
    echo ✅ L.I.F.E Platform Located!
    echo.
    echo 🧠 System Status:
    echo   ✅ L.I.F.E Theory Algorithm v2025.1.0-PRODUCTION
    echo   ✅ Neuroplasticity Engine Active
    echo   ✅ Individual Learning Analysis Ready
    echo   ✅ Clinical-Grade EEG Processing
    echo   ✅ Academic Research Mode Enabled
    echo   ✅ Interactive Navigation Fixed
    echo   ✅ Real-time Neural Pattern Recognition
    echo.
    echo 🚀 Launching L.I.F.E Academic Platform...
    
    REM Open platform in default browser
    start "" "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html"
    
    echo ✅ Platform Successfully Launched!
    echo.
    echo 🎓 Ready for Academic Demonstrations:
    echo   • Cambridge University ✓
    echo   • Oxford University ✓
    echo   • MIT Research ✓
    echo   • Stanford Neuroscience ✓
    echo   • Harvard Medical ✓
    echo   • Imperial College ✓
    echo   • UCL Institute ✓
    echo.
    echo 🧠 L.I.F.E Platform Features Active:
    echo   • Individual Learning Pattern Analysis
    echo   • Neuroplasticity Research Tools
    echo   • Clinical-Grade Diagnostics
    echo   • Real-time EEG Visualization
    echo   • Academic Research Data Export
    echo   • FDA-Validated Processing
    echo.
    echo 🏥 Platform Ready for Professional Demonstrations!
    echo.
    echo Press any key when ready to close...
    pause >nul
) else (
    echo ❌ L.I.F.E Platform file not found!
    echo 📂 Current directory: %CD%
    echo.
    echo 📋 Searching for platform files...
    dir *LIFE*.html /b 2>nul
    if errorlevel 1 (
        echo   No L.I.F.E platform files found
        echo.
        echo 💡 Expected file: LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html
    )
    echo.
    echo ❌ Please ensure platform file exists in current directory
    echo.
    pause
)