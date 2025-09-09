"""
Azure Functions Configuration
host.json and function.json for L.I.F.E Theory integration

Copyright 2025 - Sergio Paya Borrull
"""

import json
import os
from pathlib import Path

def create_host_json():
    """Create optimized host.json for L.I.F.E Theory functions"""
    host_config = {
        "version": "2.0",
        "logging": {
            "logLevel": {
                "default": "Information",
                "Function": "Information",
                "Host": "Warning"
            },
            "console": {
                "isEnabled": True
            },
            "applicationInsights": {
                "samplingExcludedTypes": "Request",
                "samplingSettings": {
                    "isEnabled": True
                }
            }
        },
        "functionTimeout": "00:10:00",  # 10 minutes for complex processing
        "httpWorkerSettings": {
            "description": "Configuration for L.I.F.E Theory processing"
        },
        "extensionBundle": {
            "id": "Microsoft.Azure.Functions.ExtensionBundle",
            "version": "[3.*, 4.0.0)"
        },
        "watchDirectories": ["src"],
        "maxOutstandingRequests": 50,
        "maxConcurrentRequests": 25,
        "retry": {
            "strategy": "exponentialBackoff",
            "maxRetryCount": 3,
            "minimumInterval": "00:00:02",
            "maximumInterval": "00:00:30"
        }
    }
    
    return host_config

def create_function_json_templates():
    """Create function.json templates for different endpoints"""
    
    # Main HTTP trigger function
    main_function = {
        "scriptFile": "azure_life_functions.py",
        "entryPoint": "main",
        "bindings": [
            {
                "authLevel": "function",
                "type": "httpTrigger",
                "direction": "in",
                "name": "req",
                "methods": ["get", "post"],
                "route": "life/{route?}"
            },
            {
                "type": "http",
                "direction": "out",
                "name": "$return"
            }
        ]
    }
    
    # EEG processing specific function
    eeg_function = {
        "scriptFile": "azure_life_functions.py",
        "entryPoint": "process_eeg_endpoint",
        "bindings": [
            {
                "authLevel": "function",
                "type": "httpTrigger",
                "direction": "in",
                "name": "req",
                "methods": ["post"],
                "route": "eeg/process"
            },
            {
                "type": "http",
                "direction": "out", 
                "name": "$return"
            }
        ]
    }
    
    # Venturi enhancement function
    venturi_function = {
        "scriptFile": "azure_life_functions.py",
        "entryPoint": "venturi_enhance_endpoint",
        "bindings": [
            {
                "authLevel": "function",
                "type": "httpTrigger",
                "direction": "in",
                "name": "req",
                "methods": ["post"],
                "route": "venturi/enhance"
            },
            {
                "type": "http",
                "direction": "out",
                "name": "$return"
            }
        ]
    }
    
    # Status and health functions
    status_function = {
        "scriptFile": "azure_life_functions.py",
        "entryPoint": "status_endpoint",
        "bindings": [
            {
                "authLevel": "anonymous",  # Public endpoint for monitoring
                "type": "httpTrigger",
                "direction": "in",
                "name": "req",
                "methods": ["get"],
                "route": "status"
            },
            {
                "type": "http",
                "direction": "out",
                "name": "$return"
            }
        ]
    }
    
    return {
        "main": main_function,
        "eeg": eeg_function,
        "venturi": venturi_function,
        "status": status_function
    }

def create_local_settings_template():
    """Create local.settings.json template"""
    local_settings = {
        "IsEncrypted": False,
        "Values": {
            "AzureWebJobsStorage": "UseDevelopmentStorage=true",
            "FUNCTIONS_WORKER_RUNTIME": "python",
            "FUNCTIONS_EXTENSION_VERSION": "~4",
            "LIFE_THEORY_VERSION": "1.0.0",
            "EEG_SAMPLING_RATE": "250.0",
            "VENTURI_FACTOR": "1.2",
            "MAX_EXPERIENCES": "1000",
            "LOGGING_LEVEL": "INFO",
            "AZURE_STORAGE_CONNECTION_STRING": "",
            "APPLICATION_INSIGHTS_KEY": "",
            "COSMOS_DB_CONNECTION_STRING": "",
            "LIFE_ALGORITHM_CONFIG": "{\"learning_rate\": 0.01, \"max_experiences\": 1000}"
        },
        "Host": {
            "LocalHttpPort": 7071,
            "CORS": "*",
            "CORSCredentials": False
        },
        "ConnectionStrings": {}
    }
    
    return local_settings

def create_requirements_azure():
    """Create requirements.txt specifically for Azure Functions"""
    requirements = [
        "azure-functions>=1.15.0",
        "azure-functions-worker>=1.2.0",
        "numpy>=1.21.0",
        "scipy>=1.7.0",
        "scikit-learn>=1.1.0",
        "matplotlib>=3.5.0",
        "pandas>=1.3.0",
        "azure-storage-blob>=12.14.0",
        "azure-cosmos>=4.3.0",
        "azure-monitor-opentelemetry-exporter>=1.0.0",
        "opencensus-ext-azure>=1.1.0",
        "python-dateutil>=2.8.0",
        "requests>=2.28.0",
        "pydantic>=1.10.0",
        "fastapi>=0.100.0",  # For advanced API features
        "uvicorn>=0.20.0",
        "python-multipart>=0.0.5",
        "aiofiles>=0.8.0",
        "httpx>=0.24.0"
    ]
    
    return "\n".join(requirements)

def create_deployment_scripts():
    """Create PowerShell deployment scripts for Azure"""
    
    # PowerShell deployment script
    deploy_ps1 = '''# Azure Functions Deployment Script for L.I.F.E Theory
# Copyright 2025 - Sergio Paya Borrull

param(
    [Parameter(Mandatory=$true)]
    [string]$ResourceGroupName,
    
    [Parameter(Mandatory=$true)]
    [string]$FunctionAppName,
    
    [Parameter(Mandatory=$false)]
    [string]$Location = "East US",
    
    [Parameter(Mandatory=$false)]
    [string]$StorageAccountName = "",
    
    [Parameter(Mandatory=$false)]
    [string]$PythonVersion = "3.9"
)

Write-Host "Deploying L.I.F.E Theory Azure Functions..." -ForegroundColor Green

# Set default storage account name if not provided
if ([string]::IsNullOrEmpty($StorageAccountName)) {
    $StorageAccountName = $FunctionAppName.ToLower() + "storage"
}

try {
    # Check if Azure CLI is installed
    $azVersion = az --version 2>$null
    if (-not $azVersion) {
        Write-Error "Azure CLI is not installed. Please install it first."
        exit 1
    }

    # Login check
    $account = az account show 2>$null | ConvertFrom-Json
    if (-not $account) {
        Write-Host "Please login to Azure..." -ForegroundColor Yellow
        az login
    }

    Write-Host "Current subscription: $($account.name)" -ForegroundColor Cyan

    # Create resource group
    Write-Host "Creating resource group..." -ForegroundColor Yellow
    az group create --name $ResourceGroupName --location $Location

    # Create storage account
    Write-Host "Creating storage account..." -ForegroundColor Yellow
    az storage account create `
        --name $StorageAccountName `
        --resource-group $ResourceGroupName `
        --location $Location `
        --sku Standard_LRS `
        --kind StorageV2

    # Create function app
    Write-Host "Creating Function App..." -ForegroundColor Yellow
    az functionapp create `
        --name $FunctionAppName `
        --resource-group $ResourceGroupName `
        --storage-account $StorageAccountName `
        --runtime python `
        --runtime-version $PythonVersion `
        --consumption-plan-location $Location `
        --os-type Linux

    # Configure app settings
    Write-Host "Configuring app settings..." -ForegroundColor Yellow
    az functionapp config appsettings set `
        --name $FunctionAppName `
        --resource-group $ResourceGroupName `
        --settings "LIFE_THEORY_VERSION=1.0.0" `
                  "EEG_SAMPLING_RATE=250.0" `
                  "VENTURI_FACTOR=1.2" `
                  "MAX_EXPERIENCES=1000" `
                  "LOGGING_LEVEL=INFO"

    # Deploy the function
    Write-Host "Deploying function code..." -ForegroundColor Yellow
    func azure functionapp publish $FunctionAppName --python

    # Get function URL
    $functionUrl = az functionapp show --name $FunctionAppName --resource-group $ResourceGroupName --query "defaultHostName" -o tsv
    
    Write-Host "Deployment completed successfully!" -ForegroundColor Green
    Write-Host "Function App URL: https://$functionUrl" -ForegroundColor Cyan
    Write-Host "Health check: https://$functionUrl/api/status" -ForegroundColor Cyan
    
    # Test the deployment
    Write-Host "Testing deployment..." -ForegroundColor Yellow
    $response = Invoke-RestMethod -Uri "https://$functionUrl/api/status" -Method GET
    Write-Host "Health check response: $($response.status)" -ForegroundColor Green

} catch {
    Write-Error "Deployment failed: $($_.Exception.Message)"
    exit 1
}

Write-Host "L.I.F.E Theory Azure Functions deployment completed!" -ForegroundColor Green
'''

    # Batch script for Windows
    deploy_bat = '''@echo off
REM Azure Functions Deployment Batch Script for L.I.F.E Theory
REM Copyright 2025 - Sergio Paya Borrull

set RESOURCE_GROUP=%1
set FUNCTION_APP=%2
set LOCATION=%3

if "%RESOURCE_GROUP%"=="" (
    echo Usage: deploy.bat [ResourceGroupName] [FunctionAppName] [Location]
    echo Example: deploy.bat life-theory-rg life-theory-functions "East US"
    exit /b 1
)

if "%FUNCTION_APP%"=="" (
    echo Error: Function App name is required
    exit /b 1
)

if "%LOCATION%"=="" (
    set LOCATION=East US
)

echo Deploying L.I.F.E Theory Azure Functions...
echo Resource Group: %RESOURCE_GROUP%
echo Function App: %FUNCTION_APP%
echo Location: %LOCATION%

REM Call PowerShell script
powershell -ExecutionPolicy Bypass -File deploy.ps1 -ResourceGroupName "%RESOURCE_GROUP%" -FunctionAppName "%FUNCTION_APP%" -Location "%LOCATION%"

if %errorlevel% neq 0 (
    echo Deployment failed!
    exit /b 1
)

echo Deployment completed successfully!
'''

    return {
        "deploy.ps1": deploy_ps1,
        "deploy.bat": deploy_bat
    }

def generate_azure_functions_config():
    """Generate all Azure Functions configuration files"""
    
    print("Generating Azure Functions configuration for L.I.F.E Theory...")
    
    # Create configuration directory structure
    config_dir = Path("azure_functions_config")
    config_dir.mkdir(exist_ok=True)
    
    # Generate host.json
    host_config = create_host_json()
    with open(config_dir / "host.json", "w") as f:
        json.dump(host_config, f, indent=2)
    print("✓ Generated host.json")
    
    # Generate function.json templates
    function_templates = create_function_json_templates()
    functions_dir = config_dir / "functions"
    functions_dir.mkdir(exist_ok=True)
    
    for name, config in function_templates.items():
        func_dir = functions_dir / name
        func_dir.mkdir(exist_ok=True)
        with open(func_dir / "function.json", "w") as f:
            json.dump(config, f, indent=2)
        print(f"✓ Generated function.json for {name}")
    
    # Generate local.settings.json template
    local_settings = create_local_settings_template()
    with open(config_dir / "local.settings.json.template", "w") as f:
        json.dump(local_settings, f, indent=2)
    print("✓ Generated local.settings.json template")
    
    # Generate requirements.txt for Azure
    requirements = create_requirements_azure()
    with open(config_dir / "requirements_azure.txt", "w") as f:
        f.write(requirements)
    print("✓ Generated requirements_azure.txt")
    
    # Generate deployment scripts
    scripts = create_deployment_scripts()
    scripts_dir = config_dir / "deployment"
    scripts_dir.mkdir(exist_ok=True)
    
    for name, content in scripts.items():
        with open(scripts_dir / name, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✓ Generated {name}")
    
    # Generate README for configuration
    readme_content = '''# Azure Functions Configuration for L.I.F.E Theory

This directory contains all configuration files needed to deploy L.I.F.E Theory to Azure Functions.

## Files Generated:

### Core Configuration
- `host.json` - Function app host configuration
- `local.settings.json.template` - Local development settings template
- `requirements_azure.txt` - Python dependencies for Azure

### Function Definitions
- `functions/main/function.json` - Main HTTP trigger with routing
- `functions/eeg/function.json` - EEG processing endpoint  
- `functions/venturi/function.json` - Venturi enhancement endpoint
- `functions/status/function.json` - Status and health check endpoint

### Deployment Scripts
- `deployment/deploy.ps1` - PowerShell deployment script
- `deployment/deploy.bat` - Windows batch deployment script

## Quick Start:

1. Copy `local.settings.json.template` to `local.settings.json` and configure
2. Install Azure Functions Core Tools: `npm install -g azure-functions-core-tools@4 --unsafe-perm true`
3. Run locally: `func start`
4. Deploy: `./deployment/deploy.ps1 -ResourceGroupName "your-rg" -FunctionAppName "your-app"`

## Endpoints:

- `GET /api/status` - Health check and system status
- `POST /api/life/process-eeg` - Process EEG data through L.I.F.E Theory
- `POST /api/life/venturi-enhance` - Apply Venturi enhancement to signals  
- `POST /api/life/life-process` - General L.I.F.E algorithm processing

## Environment Variables:

Configure these in your Azure Function App settings:
- `LIFE_THEORY_VERSION` - Version identifier
- `EEG_SAMPLING_RATE` - Default EEG sampling rate (250.0)
- `VENTURI_FACTOR` - Venturi enhancement factor (1.2)
- `MAX_EXPERIENCES` - Maximum experiences for learning (1000)
- `LOGGING_LEVEL` - Logging level (INFO)

Copyright 2025 - Sergio Paya Borrull
'''
    
    with open(config_dir / "README.md", "w") as f:
        f.write(readme_content)
    print("✓ Generated README.md")
    
    print(f"\nConfiguration generated successfully in: {config_dir.absolute()}")
    print("\nNext steps:")
    print("1. Copy generated files to your Azure Functions project")
    print("2. Configure local.settings.json with your values")
    print("3. Run 'func start' for local testing")
    print("4. Use deployment scripts for Azure deployment")

if __name__ == "__main__":
    generate_azure_functions_config()
