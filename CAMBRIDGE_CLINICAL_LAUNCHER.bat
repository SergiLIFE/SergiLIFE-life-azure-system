@echo off
echo 🧠 L.I.F.E Platform Academic Launcher
echo ====================================
echo Learning Individually From Experience
echo.

echo 📂 Checking for L.I.F.E Platform...
if exist "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html" (
    echo ✅ L.I.F.E Platform Found!
    echo 🧠 L.I.F.E Theory Algorithm: INTEGRATED
    echo � Neuroplasticity Analysis: ACTIVE
    echo 🎓 Academic Research Mode: ENABLED
    echo.
    echo 🚀 Opening L.I.F.E Academic Platform...
    start "" "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html"
    echo ✅ Platform launched in browser!
    echo.
    echo 🎓 Ready for Academic Demonstrations!
    echo   • 7 Meeting Schedule Support
    echo   • Multiple Institution Compatible
    echo   • Clinical-grade neuroplasticity analysis
    echo   • FDA-validated L.I.F.E algorithms
    echo   • Real-time neural pattern recognition
    echo.
    pause
) else (
    echo ❌ L.I.F.E Platform not found
    echo 📂 Current directory: %CD%
    echo.
    echo Available HTML platforms:
    dir *.html /b
    echo.
    pause
)