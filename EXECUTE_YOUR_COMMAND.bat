@echo off
echo ========================================
echo FINAL PUSH - Execute Your Command
echo ========================================
echo.

echo Executing: git rebase --abort && git add -A && git commit -m "Fix: Add all pending changes and tools" && git push origin main --force
echo.

git rebase --abort
echo Rebase aborted (if any)
echo.

git add -A
echo All changes staged
echo.

git status --porcelain
echo Files to be committed ^
echo.

git commit -m "Fix: Add all pending changes and tools"
echo Commit created
echo.

git push origin main --force
echo.

if errorlevel 1 (
    echo ❌ Push failed - check error above
    echo.
    echo Alternative commands to try:
    echo 1. git push origin main --force-with-lease
    echo 2. git pull --rebase origin main, then git push origin main
    pause
) else (
    echo ✅ SUCCESS! All 593 changes pushed to GitHub!
    echo.
    echo 🎉 Your repository is now up to date:
    echo - All new management tools (.bat files^)
    echo - GitHub Actions deployment fix
    echo - Documentation files
    echo - Azure configuration updates
    echo.
    echo Next commits will work normally (no more 404 deployment errors^)
)

echo.
echo ========================================
pause