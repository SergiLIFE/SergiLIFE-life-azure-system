@echo off
echo ========================================
echo L.I.F.E. Platform Pre-Demo Validation
echo October 14-15, 2025
echo ========================================
echo.

echo Testing Python environment...
python --version
echo.

echo Running registration system validation...
python quick_validation.py
echo.

echo ========================================
echo Validation Complete - Review Results Above
echo ========================================

pause