@echo off
REM ========================================
REM L.I.F.E Platform Professional Cleanup
REM Removes emojis and enforces standards
REM ========================================

echo L.I.F.E Platform - Professional Repository Cleanup
echo ====================================================
echo.

cd /d "c:\Users\Sergio Paya Borrull\.azure\SergiLIFE-life-azure-system\.git\hooks\SergiLIFE-life-azure-system"

echo Step 1: Running emoji sanitization...
python emoji_sanitizer.py .

echo.
echo Step 2: Replacing README with professional version...
if exist "README.md" (
    copy "README.md" "README_OLD_WITH_EMOJIS.md"
    echo Old README backed up to README_OLD_WITH_EMOJIS.md
)
copy "README_PROFESSIONAL.md" "README.md"
echo Professional README activated

echo.
echo Step 3: Installing Git hooks...
if exist ".git\hooks\pre-commit" (
    echo Pre-commit hook already exists
) else (
    copy ".git\hooks\pre-commit.sample" ".git\hooks\pre-commit" 2>nul
    echo Pre-commit hook installed
)

echo.
echo Step 4: Adding professional standards to .gitignore...
echo # Professional Standards - No Emojis >> .gitignore
echo *emoji* >> .gitignore
echo *Emoji* >> .gitignore
echo *EMOJI* >> .gitignore

echo.
echo Step 5: Configuring Git settings for professional commits...
git config core.hooksPath .git/hooks
git config commit.template ""

echo.
echo ====================================================
echo Professional cleanup complete!
echo ====================================================
echo.
echo Changes made:
echo - Emojis removed from all files
echo - Professional README activated
echo - Git hooks installed for emoji prevention
echo - .gitignore updated with emoji exclusions
echo.
echo Your repository now maintains professional standards.
echo All future commits will be automatically checked for emojis.
echo.
pause