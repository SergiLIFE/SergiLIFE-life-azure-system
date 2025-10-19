@echo off
REM Azure Resources Status Checker for L.I.F.E Platform

echo.
echo ================================================================================
echo      L.I.F.E PLATFORM - AZURE RESOURCES STATUS
echo ================================================================================
echo.

SET SUBSCRIPTION_ID=5c88cef6-f243-497d-98af-6c6086d575ca
SET RESOURCE_GROUP=life-platform-rg

echo Checking Azure subscription...
az account set --subscription %SUBSCRIPTION_ID%
az account show --query "{Name:name, SubscriptionId:id, State:state}" --output table

echo.
echo Checking resource group...
az group exists --name %RESOURCE_GROUP% > temp_exists.txt
set /p GROUP_EXISTS=<temp_exists.txt
del temp_exists.txt

if "%GROUP_EXISTS%"=="true" (
    echo [OK] Resource group '%RESOURCE_GROUP%' EXISTS
    echo.
    echo Resources in group:
    az resource list --resource-group %RESOURCE_GROUP% --output table
    echo.
    echo Resource count:
    az resource list --resource-group %RESOURCE_GROUP% --query "length(@)"
) else (
    echo [WARN] Resource group '%RESOURCE_GROUP%' does NOT exist
    echo Run DEPLOY_AZURE_FULL.bat to deploy
)

echo.
pause
