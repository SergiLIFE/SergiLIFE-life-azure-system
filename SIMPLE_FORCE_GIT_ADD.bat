@echo off
echo ========================================
echo SIMPLE FORCE GIT TRACK ALL FILES
echo ========================================

echo 💡 Files exist but git shows crossed over - forcing git to track them all

echo Step 1: Count existing files...
for /f %%i in ('dir /b ^| find /c /v ""') do set total_files=%%i
echo "Total files found: %total_files%"

echo.
echo Step 2: Force git to add everything...
git reset --mixed HEAD 2>nul
git add . --force
git add -A --force
git add --all --force

echo.
echo Step 3: Check what git staged...
for /f %%i in ('git diff --cached --name-only ^| find /c /v ""') do set staged_files=%%i
echo "Files staged by git: %staged_files%"

echo.
echo Step 4: Commit all staged files...
if %staged_files% GTR 0 (
    git commit -m "FORCE ADD: All %staged_files% existing files properly tracked - L.I.F.E Platform complete #178"
    
    if %ERRORLEVEL% EQU 0 (
        echo "✅ Committed %staged_files% files!"
        
        echo "Pushing to GitHub..."
        git push origin main
        
        if %ERRORLEVEL% EQU 0 (
            echo "🎉 SUCCESS! %staged_files% files pushed to GitHub"
        else (
            echo "⚠️ Files committed locally but push failed"
        )
    ) else (
        echo "❌ Commit failed"
    )
) else (
    echo "ℹ️ No files to commit"
)

echo.
echo Final status:
git status --short

echo.
echo "========================================"
echo "OPERATION COMPLETE"
echo "========================================"
pause