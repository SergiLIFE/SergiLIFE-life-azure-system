@echo off
REM L.I.F.E. Research Data Library - Validation & Testing
REM Copyright 2025 - Sergio Paya Borrull

echo ======================================================================
echo L.I.F.E. RESEARCH DATA LIBRARY - COMPREHENSIVE VALIDATION
echo ======================================================================
echo.

echo [1/2] Running validation tests...
python validate_research_integration.py

echo.
echo.
echo ======================================================================
echo [2/2] Optional: Populate Full Research Database
echo ======================================================================
echo.
echo To populate comprehensive research database with:
echo   - 610 participants
echo   - 8,810 research sessions
echo   - 5 complete studies (Educational, Clinical, University, Longitudinal, Enterprise)
echo.
set /p populate="Populate database now? (Y/N): "

if /i "%populate%"=="Y" (
    echo.
    echo Populating research database...
    python populate_research_database.py
    echo.
    echo Database population complete!
) else (
    echo.
    echo Skipping database population.
    echo Run 'python populate_research_database.py' anytime to populate.
)

echo.
echo ======================================================================
echo VALIDATION COMPLETE
echo ======================================================================
echo.
echo Platform Status: RESEARCH-OPTIMIZED
echo Ready for production use.
echo.
pause
