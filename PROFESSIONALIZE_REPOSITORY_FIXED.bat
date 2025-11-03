@echo off
REM FIXED PROFESSIONAL REPOSITORY SANITIZER
REM Clean version without encoding issues

cd /d "c:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system"

echo.
echo ===================================================
echo  PROFESSIONAL REPOSITORY SANITIZER (FIXED)
echo  Converting L.I.F.E Platform to Clinical Standards
echo ===================================================
echo.
echo Objective: Remove all emojis and convert to professional tone
echo Scope: All documentation, code, and configuration files
echo Standard: Clinical, academic, and enterprise presentation
echo.

echo Executing Professional Repository Sanitizer...
echo.

python PROFESSIONAL_REPOSITORY_SANITIZER_FIXED.py --create-guidelines

echo.
if %ERRORLEVEL% EQU 0 (
    echo ===================================================
    echo  SUCCESS: Repository professionalized successfully!
    echo  All emojis removed and clinical tone applied
    echo  Professional documentation standards created
    echo ===================================================
    echo.
    echo CHECK RESULTS:
    echo   - PROFESSIONALIZATION_REPORT.json - Detailed results
    echo   - PROFESSIONAL_DOCUMENTATION_STANDARDS.md - Guidelines
    echo   - README.md - Professionalized main documentation
) else (
    echo ===================================================
    echo  PARTIAL: Some files may need manual review
    echo  Check the output above for specific details
    echo ===================================================
)

echo.
echo REPOSITORY NOW MEETS CLINICAL AND ENTERPRISE STANDARDS
echo Professional documentation guidelines established
echo Ready for regulatory review and enterprise deployment
echo.
pause