@echo off
REM Microsoft Partnership Demo - Bicep Validation Script (Windows)
REM Validates the infrastructure template before deployment

setlocal enabledelayedexpansion

REM Configuration
set RESOURCE_GROUP_NAME=rg-life-microsoft-demo
set LOCATION=eastus2
set TEMPLATE_FILE=infra\microsoft-partnership-clean.bicep
set PARAMETERS_FILE=infra\microsoft-partnership-clean.parameters.json
set SUBSCRIPTION_ID=5c88cef6-f243-497d-98af-6c6086d575ca

echo 🔍 Microsoft Partnership Demo - Bicep Validation
echo ================================================

REM Check if Azure CLI is installed
az --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Azure CLI is not installed. Please install it first.
    exit /b 1
)

REM Login check
echo 🔐 Checking Azure CLI authentication...
az account show >nul 2>&1
if errorlevel 1 (
    echo ❌ Not logged into Azure CLI. Please run 'az login' first.
    exit /b 1
)

REM Set subscription
echo 📋 Setting subscription: %SUBSCRIPTION_ID%
az account set --subscription "%SUBSCRIPTION_ID%"
if errorlevel 1 (
    echo ❌ Failed to set subscription
    exit /b 1
)

echo ✅ Subscription set successfully

REM Create resource group if it doesn't exist
echo 🏗️  Checking resource group: %RESOURCE_GROUP_NAME%
az group show --name "%RESOURCE_GROUP_NAME%" >nul 2>&1
if errorlevel 1 (
    echo 📦 Creating resource group...
    az group create --name "%RESOURCE_GROUP_NAME%" --location "%LOCATION%" --tags Environment=microsoft-demo Project=L.I.F.E-Platform Partnership=Microsoft-Demo
    if errorlevel 1 (
        echo ❌ Failed to create resource group
        exit /b 1
    )
    echo ✅ Resource group created successfully
) else (
    echo ✅ Resource group already exists
)

REM Validate Bicep template syntax
echo 🧪 Validating Bicep template syntax...
az bicep build --file "%TEMPLATE_FILE%" --stdout >nul 2>&1
if errorlevel 1 (
    echo ❌ Bicep template syntax validation failed
    exit /b 1
)
echo ✅ Bicep template syntax is valid

REM Validate template with parameters
echo 🔬 Validating template deployment...
az deployment group validate --resource-group "%RESOURCE_GROUP_NAME%" --template-file "%TEMPLATE_FILE%" --parameters "@%PARAMETERS_FILE%" >nul 2>&1
if errorlevel 1 (
    echo ❌ Template validation failed
    az deployment group validate --resource-group "%RESOURCE_GROUP_NAME%" --template-file "%TEMPLATE_FILE%" --parameters "@%PARAMETERS_FILE%"
    exit /b 1
)

echo ✅ Template validation successful

REM What-if deployment preview
echo 👀 Generating deployment preview (what-if)...
az deployment group what-if --resource-group "%RESOURCE_GROUP_NAME%" --template-file "%TEMPLATE_FILE%" --parameters "@%PARAMETERS_FILE%" --result-format FullResourcePayloads

echo.
echo 🎉 Validation Complete!
echo ========================
echo ✅ Azure CLI authenticated
echo ✅ Subscription configured: %SUBSCRIPTION_ID%
echo ✅ Resource group ready: %RESOURCE_GROUP_NAME%
echo ✅ Bicep template syntax valid
echo ✅ Template parameters valid
echo ✅ Deployment preview generated
echo.
echo 🚀 Ready for deployment! Run the following command to deploy:
echo az deployment group create ^
echo     --resource-group "%RESOURCE_GROUP_NAME%" ^
echo     --template-file "%TEMPLATE_FILE%" ^
echo     --parameters "@%PARAMETERS_FILE%"
echo.
echo 💡 Or use the Azure Portal deployment option with the generated template.

pause