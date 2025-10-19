@echo off
REM L.I.F.E. Education Platform - Integration Test Launcher
REM Tests: Algorithm Integration, Latency, Accuracy

echo.
echo ====================================================================
echo L.I.F.E. Education Platform - Integration Test Suite
echo ====================================================================
echo.
echo Testing:
echo   - L.I.F.E. Theory Algorithm Integration
echo   - Latency Performance (target: ^<0.5ms per equation)
echo   - Accuracy with Real EEG Data (target: ^>95%%)
echo   - Full Pipeline Integration
echo   - High Throughput Stress Test
echo.
echo Starting tests...
echo.

python test_life_education_platform_integration.py

echo.
echo ====================================================================
echo Test Complete - Check results above and in test_results/ directory
echo ====================================================================
echo.
pause
