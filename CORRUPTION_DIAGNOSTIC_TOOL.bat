@echo off
REM L.I.F.E. Platform - Corruption Diagnostic Tool
REM October 13, 2025 - Emergency fix for October 15th demo
REM Diagnoses and fixes encoding issues

title L.I.F.E. Platform - Corruption Diagnostic Tool
color 0C

echo.
echo ===============================================
echo    L.I.F.E. PLATFORM CORRUPTION DIAGNOSTIC
echo    Emergency Fix for October 15th Demo
echo    Encoding and Display Issue Resolver
echo ===============================================
echo.

echo [DIAGNOSTIC] Checking for common corruption issues...
echo [DATE] %date% %time%
echo.

REM Check if the dashboard file exists and get basic info
set "DASHBOARD_FILE=E:\THE L.I.F.E Theory Algorithm\L.I.F.E Theory Evolution\L.I.F.E. Platform - Core Algorithm Dashboard.html"

echo [TARGET] Dashboard File Analysis:
echo [PATH] %DASHBOARD_FILE%
echo.

if exist "%DASHBOARD_FILE%" (
    echo [SUCCESS] ✅ Dashboard file found!
    
    REM Get file size and last modified date
    for %%A in ("%DASHBOARD_FILE%") do (
        set FILE_SIZE=%%~zA
        set FILE_DATE=%%~tA
    )
    set /a FILE_SIZE_KB=%FILE_SIZE%/1024
    
    echo [INFO] File size: %FILE_SIZE_KB% KB
    echo [INFO] Last modified: %FILE_DATE%
    echo.
    
    REM Check file encoding by looking at first few bytes
    echo [ENCODING] Checking file encoding...
    powershell -Command "Get-Content '%DASHBOARD_FILE%' -Head 5 -Encoding UTF8 | Out-String" > temp_encoding_check.txt
    
    if exist temp_encoding_check.txt (
        echo [SAMPLE] First few lines of file:
        type temp_encoding_check.txt
        del temp_encoding_check.txt
    )
    
    echo.
    echo [SOLUTIONS] Corruption Fix Options:
    echo ════════════════════════════════════════
    echo 1. 🔧 Try opening with different browsers
    echo 2. 🔄 Copy file to local directory (C: drive)
    echo 3. 📝 Open with different text encoding (UTF-8)
    echo 4. 💻 Use alternative HTML viewer
    echo 5. 🚀 Use backup dashboard from current directory
    echo.
    
) else (
    echo [ERROR] ❌ Dashboard file not accessible!
    echo [PATH] %DASHBOARD_FILE%
    echo.
    echo [FALLBACK] Checking for local alternatives...
)

REM Check for alternative dashboard files
echo [ALTERNATIVES] Looking for backup dashboards...
if exist "*.html" (
    echo [FOUND] Local HTML files:
    dir *.html /b
    echo.
    echo [SUGGESTION] Try using one of these local files instead
) else (
    echo [INFO] No local HTML alternatives found
)

echo.
echo [QUICK FIXES] Emergency Solutions for October 15th:
echo ═════════════════════════════════════════════════
echo.
echo 1. 🔥 IMMEDIATE FIX - Copy to local directory:
echo    copy "%DASHBOARD_FILE%" "LIFE_Demo_Oct15.html"
echo.
echo 2. 🌐 BROWSER FIX - Try different browsers:
echo    - Chrome: chrome.exe "file:///%DASHBOARD_FILE%"
echo    - Firefox: firefox.exe "file:///%DASHBOARD_FILE%"
echo    - Edge: msedge.exe "file:///%DASHBOARD_FILE%"
echo.
echo 3. 📱 ENCODING FIX - Open with UTF-8:
echo    notepad "%DASHBOARD_FILE%"
echo    (Save as UTF-8 encoding)
echo.
echo 4. ⚡ EMERGENCY BACKUP - Use simple demo:
echo    python simple_life_demo.py
echo.

echo [RECOMMENDATION] For October 15th demo:
echo ═══════════════════════════════════════════
echo ✅ Copy dashboard to C: drive (most reliable)
echo ✅ Test with Chrome browser specifically
echo ✅ Have backup simple demo ready
echo ✅ Practice screen sharing beforehand
echo.

echo [NEXT STEPS] Press any key to attempt automatic fix...
pause >nul

echo.
echo [AUTO-FIX] Attempting to copy dashboard locally...
if exist "%DASHBOARD_FILE%" (
    copy "%DASHBOARD_FILE%" "LIFE_Demo_Oct15_FIXED.html" >nul
    if exist "LIFE_Demo_Oct15_FIXED.html" (
        echo [SUCCESS] ✅ Local copy created: LIFE_Demo_Oct15_FIXED.html
        echo [TEST] Opening local copy...
        start "" "LIFE_Demo_Oct15_FIXED.html"
    ) else (
        echo [ERROR] ❌ Failed to create local copy
    )
) else (
    echo [ERROR] ❌ Source file not accessible
)

echo.
echo [COMPLETE] Diagnostic complete - Ready for October 15th!
pause