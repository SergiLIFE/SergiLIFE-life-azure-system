git add .
git add -A
git status --short
echo.
echo Files staged for commit:
git diff --cached --name-only
echo.
pause