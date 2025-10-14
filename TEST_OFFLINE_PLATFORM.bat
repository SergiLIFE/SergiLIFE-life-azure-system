@echo off
echo ========================================
echo 🧠 L.I.F.E Clinical Platform Offline Test
echo ========================================
echo.
echo Testing offline compatibility...
echo Opening platform in browser...
echo.

REM Open the platform in the default browser
start "" "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html"

echo ✅ Platform opened in browser
echo.
echo 📋 OFFLINE TEST CHECKLIST:
echo [ ] Platform loads without internet connection
echo [ ] All 6 tabs are functional
echo [ ] Charts display (either Chart.js or offline fallback)
echo [ ] L.I.F.E Algorithm processes EEG data
echo [ ] Clinical alerts display properly
echo [ ] All interactive elements work
echo.
echo 🎯 If any issues occur, check browser console for errors
echo.
pause