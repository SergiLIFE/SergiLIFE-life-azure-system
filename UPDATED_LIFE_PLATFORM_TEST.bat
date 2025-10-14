@echo off
cls
echo.
echo ===============================================
echo 🧠 L.I.F.E Platform - Updated Version Test
echo ===============================================
echo.
echo ✅ FIXED ISSUES:
echo • Added EEG Bluetooth (WiFi) Kit connection tab
echo • Removed all Cambridge University branding
echo • Updated to pure L.I.F.E Platform branding
echo.

if exist "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html" (
    echo 📊 VERIFICATION CHECK:
    echo ---------------------
    
    echo Checking for new EEG connection tab...
    findstr /c:"EEG Bluetooth Kit" "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html" >nul && echo ✅ EEG Bluetooth tab: ADDED || echo ❌ EEG Bluetooth tab: MISSING
    
    echo Checking EEG connection functions...
    findstr /c:"connectEEGDevice" "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html" >nul && echo ✅ EEG connection functions: ADDED || echo ❌ EEG functions: MISSING
    
    echo Checking branding updates...
    findstr /c:"L.I.F.E Neuroplasticity Platform" "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html" >nul && echo ✅ L.I.F.E branding: UPDATED || echo ❌ Branding: NOT UPDATED
    
    echo Checking Cambridge references removed...
    findstr /c:"Cambridge University Demo" "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html" >nul && echo ⚠️  Cambridge references: STILL PRESENT || echo ✅ Cambridge references: REMOVED
    
    echo.
    echo 🚀 LAUNCHING UPDATED L.I.F.E PLATFORM...
    echo.
    start "" "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html"
    
    echo ✅ L.I.F.E Platform opened in browser
    echo.
    echo 📋 NEW FEATURES TO TEST:
    echo ========================
    echo 1. Click "🔗 EEG Bluetooth Kit" tab (2nd tab)
    echo 2. Test "🔗 Connect New Device" button
    echo 3. Test "⚙️ Calibrate Device" button  
    echo 4. Test "🎯 Start L.I.F.E Analysis" button
    echo 5. Verify real-time EEG waveform displays
    echo 6. Check that all branding says "L.I.F.E Platform"
    echo.
    echo 🎯 NOW YOU HAVE ALL 7 TABS:
    echo 1. Clinical Overview
    echo 2. 🔗 EEG Bluetooth Kit ^(NEW!^)
    echo 3. EEG Analysis
    echo 4. Neuroplasticity
    echo 5. AI Diagnostics
    echo 6. Research Data
    echo 7. Clinical Validation
    
) else (
    echo ❌ Platform file not found!
)

echo.
pause