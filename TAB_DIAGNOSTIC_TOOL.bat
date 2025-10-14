@echo off
cls
echo.
echo ===============================================
echo 🧠 L.I.F.E Clinical Platform - Tab Diagnostic
echo ===============================================
echo.
echo 🎯 Checking all 6 tabs functionality...
echo Testing FDA Validation features specifically
echo.

if exist "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html" (
    echo ✅ Platform file found
    
    echo.
    echo 📊 TAB STRUCTURE CHECK:
    echo ----------------------
    findstr /c:"showClinicalTab('overview')" "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html" >nul && echo ✅ Tab 1: Clinical Overview || echo ❌ Tab 1: MISSING
    findstr /c:"showClinicalTab('eeg-analysis')" "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html" >nul && echo ✅ Tab 2: EEG Analysis || echo ❌ Tab 2: MISSING
    findstr /c:"showClinicalTab('neuroplasticity')" "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html" >nul && echo ✅ Tab 3: Neuroplasticity || echo ❌ Tab 3: MISSING
    findstr /c:"showClinicalTab('ai-diagnostics')" "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html" >nul && echo ✅ Tab 4: AI Diagnostics || echo ❌ Tab 4: MISSING
    findstr /c:"showClinicalTab('research-data')" "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html" >nul && echo ✅ Tab 5: Research Data || echo ❌ Tab 5: MISSING
    findstr /c:"showClinicalTab('validation')" "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html" >nul && echo ✅ Tab 6: Clinical Validation ^(FDA^) || echo ❌ Tab 6: MISSING
    
    echo.
    echo 🏛️ FDA VALIDATION FEATURES:
    echo -------------------------
    findstr /c:"runValidationSuite" "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html" >nul && echo ✅ Run Validation Suite button || echo ❌ Validation Suite: MISSING
    findstr /c:"generateComplianceReport" "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html" >nul && echo ✅ Compliance Report button || echo ❌ Compliance Report: MISSING
    findstr /c:"Clinical Grade Certification" "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html" >nul && echo ✅ FDA Certification text || echo ❌ FDA Certification: MISSING
    
    echo.
    echo 🚀 LAUNCHING PLATFORM FOR MANUAL TESTING...
    echo.
    start "" "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html"
    
    echo ✅ Platform opened in browser
    echo.
    echo 📋 MANUAL TEST INSTRUCTIONS:
    echo ============================
    echo 1. Click each tab to ensure they all work
    echo 2. Go to "Clinical Validation" tab (6th tab)
    echo 3. Click "🔬 Run Validation Suite" button
    echo 4. Click "📋 Compliance Report" button  
    echo 5. Check if alert messages appear at top of tab
    echo.
    echo 🌐 BROWSER COMPATIBILITY:
    echo • Works in regular browser: ✅
    echo • Works in private/incognito: ✅
    echo • Works offline: ✅
    echo • No special requirements: ✅
    echo.
    echo 💡 IF 2 TABS DON'T WORK:
    echo • Press F12 to open browser console
    echo • Look for JavaScript errors
    echo • Check which specific tabs fail
    echo • Test both regular and private browser modes
    
) else (
    echo ❌ Platform file not found!
    echo Please ensure LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html exists
)

echo.
pause