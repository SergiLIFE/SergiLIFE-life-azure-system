@echo off
echo ========================================
echo IMMEDIATE FILE CHECK & RECOVERY
echo Quick Assessment of Current State
echo ========================================

echo 🔍 STEP 1: Quick file inventory...
echo "Current directory contents:"
dir /b

echo.
echo 🔍 STEP 2: Check if key L.I.F.E files exist..."
if exist "experimentP2L*.py" (
    echo "✅ L.I.F.E algorithm files found"
) else (
    echo "❌ L.I.F.E algorithm files MISSING"
)

if exist "life*.py" (
    echo "✅ L.I.F.E platform files found"
) else (
    echo "❌ L.I.F.E platform files MISSING"
)

if exist "requirements.txt" (
    echo "✅ Requirements file found"
) else (
    echo "❌ Requirements file MISSING"
)

if exist ".github\" (
    echo "✅ GitHub workflows folder found"
) else (
    echo "❌ GitHub workflows folder MISSING"
)

if exist "*.html" (
    echo "✅ HTML files found"
) else (
    echo "❌ HTML files MISSING"
)

echo.
echo 🔍 STEP 3: Git status check...
git status --porcelain

echo.
echo 🔍 STEP 4: Check recent git history...
git log --oneline -3

echo.
echo 🔍 STEP 5: Files count...
for /f %%i in ('dir /b ^| find /c /v ""') do set file_count=%%i
echo "Total files in directory: %file_count%"

if %file_count% LSS 10 (
    echo "🚨 CRITICAL: Very few files detected - major deletion occurred"
    echo "🔧 Running emergency recovery now..."
    call EMERGENCY_FILE_RECOVERY.bat
) else (
    echo "ℹ️ Reasonable number of files detected"
    echo "Files may just need to be re-staged for git"
    
    echo.
    echo "Adding all current files to git..."
    git add -A
    git status --porcelain
)

echo.
echo "========================================"
echo "ASSESSMENT COMPLETE"
echo "========================================"
pause