"""
🐍 Python 3.13 Upgrade & Azure Functions API Fix
Comprehensive solution to upgrade to Python 3.13 and fix API endpoints

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import json
import os
from datetime import datetime
from pathlib import Path

# Azure Function App configuration
FUNCTION_APP_NAME = "lifeplatform1760781933"
RESOURCE_GROUP = "life-platform-prod"
PYTHON_VERSION = "3.13"


def create_function_app_structure():
    """Create proper Azure Functions structure with Python 3.13"""

    print("🏗️ Creating Azure Functions structure with Python 3.13...")

    # Create main function directory
    func_dir = Path("LifePlatformAPI")
    func_dir.mkdir(exist_ok=True)

    # Create function.json for HTTP trigger
    function_json = {
        "scriptFile": "__init__.py",
        "bindings": [
            {
                "authLevel": "anonymous",
                "type": "httpTrigger",
                "direction": "in",
                "name": "req",
                "methods": ["GET", "POST"],
                "route": "{*route:alpha?}",
            },
            {"type": "http", "direction": "out", "name": "$return"},
        ],
    }

    with open(func_dir / "function.json", "w") as f:
        json.dump(function_json, f, indent=2)

    print(f"✅ Created function.json in {func_dir}")

    # Create __init__.py with proper routing
    init_py_content = '''"""
L.I.F.E. Platform Azure Functions Entry Point
Python 3.13 Compatible Implementation
"""

import json
import logging
import azure.functions as func
from typing import Dict, Any
import sys
import os

# Add parent directory to path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/..")))

try:
    from life_platform_api import LIFEPlatformAPI, APIResponse
except ImportError as e:
    logging.error(f"Failed to import L.I.F.E Platform API: {e}")
    # Fallback implementation
    class LIFEPlatformAPI:
        def process_request(self, method: str, path: str, body: Dict[str, Any] = None) -> Dict[str, Any]:
            return {
                "status": "error", 
                "message": f"Module import failed: {e}",
                "timestamp": "2025-10-18T10:00:00Z"
            }

# Initialize API instance
api_instance = LIFEPlatformAPI()

def main(req: func.HttpRequest) -> func.HttpResponse:
    """Main Azure Function entry point"""
    
    logging.info("L.I.F.E Platform API request received")
    
    try:
        # Get request details
        method = req.method.upper()
        url = req.url
        path = req.route_params.get('route', '')
        
        # Handle root path
        if not path:
            if 'api/' in url:
                path = url.split('api/')[-1].split('?')[0]
            else:
                path = ""
        
        # Add leading slash if missing
        if path and not path.startswith('/'):
            path = '/' + path
        
        # Convert to full API path
        if path and not path.startswith('/api/'):
            if path.startswith('/'):
                path = '/api' + path
            else:
                path = '/api/' + path
        
        logging.info(f"Processing {method} request to {path}")
        
        # Get request body
        body = None
        if method in ['POST', 'PUT', 'PATCH']:
            try:
                body_str = req.get_body().decode('utf-8')
                if body_str:
                    body = json.loads(body_str)
            except Exception as e:
                logging.warning(f"Failed to parse request body: {e}")
                body = {}
        
        # Process the request
        response = api_instance.process_request(method, path, body)
        
        # Ensure response has required fields
        if not isinstance(response, dict):
            response = {"status": "error", "message": "Invalid response format"}
        
        # Add metadata
        response.setdefault("timestamp", datetime.now().isoformat())
        response.setdefault("python_version", f"{sys.version_info.major}.{sys.version_info.minor}")
        response.setdefault("platform", "Azure Functions")
        
        # Return JSON response
        return func.HttpResponse(
            json.dumps(response, indent=2),
            status_code=200 if response.get("status") == "success" else 500,
            headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization"
            }
        )
        
    except Exception as e:
        logging.error(f"L.I.F.E Platform API error: {str(e)}", exc_info=True)
        
        error_response = {
            "status": "error",
            "message": f"API processing failed: {str(e)}",
            "timestamp": datetime.now().isoformat(),
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}",
            "error_type": type(e).__name__
        }
        
        return func.HttpResponse(
            json.dumps(error_response, indent=2),
            status_code=500,
            headers={"Content-Type": "application/json"}
        )
'''

    with open(func_dir / "__init__.py", "w") as f:
        f.write(init_py_content)

    print(f"✅ Created __init__.py in {func_dir}")
    return func_dir


def update_host_json():
    """Update host.json for Python 3.13 compatibility"""

    print("📝 Updating host.json for Python 3.13...")

    host_config = {
        "version": "2.0",
        "logging": {
            "applicationInsights": {
                "samplingSettings": {"isEnabled": True, "excludedTypes": "Request"},
                "enableLiveMetricsFilters": True,
            },
            "logLevel": {
                "default": "Information",
                "Host.Results": "Information",
                "Function": "Information",
                "Host.Aggregator": "Information",
            },
        },
        "extensionBundle": {
            "id": "Microsoft.Azure.Functions.ExtensionBundle",
            "version": "[4.*, 5.0.0)",
        },
        "functionTimeout": "00:10:00",
        "retry": {
            "strategy": "exponentialBackoff",
            "maxRetryCount": 3,
            "minimumInterval": "00:00:02",
            "maximumInterval": "00:00:30",
        },
        "healthMonitor": {
            "enabled": True,
            "healthCheckInterval": "00:00:10",
            "healthCheckWindow": "00:02:00",
            "healthCheckThreshold": 6,
            "counterThreshold": 0.80,
        },
        "http": {
            "routePrefix": "",
            "maxOutstandingRequests": 200,
            "maxConcurrentRequests": 100,
            "dynamicThrottlesEnabled": True,
        },
    }

    with open("host.json", "w") as f:
        json.dump(host_config, f, indent=2)

    print("✅ Updated host.json")


def update_requirements_txt():
    """Update requirements.txt for Python 3.13 compatibility"""

    print("📦 Updating requirements.txt for Python 3.13...")

    requirements = """# L.I.F.E Platform - Python 3.13 Compatible Dependencies
# Azure Marketplace Ready - Enterprise Neural Processing System
# Copyright 2025 - Sergio Paya Borrull

# Azure Functions Runtime
azure-functions>=1.19.0
azure-functions-worker>=1.2.0

# Core Scientific Computing (Python 3.13 compatible)
numpy>=1.26.0
pandas>=2.1.0
scipy>=1.11.0
scikit-learn>=1.3.0

# Neural Processing & Machine Learning
tensorflow>=2.15.0
torch>=2.1.0
mne>=1.5.0  # EEG/MEG analysis
nilearn>=0.10.2  # Neuroimaging
joblib>=1.3.2

# Azure SDK Components (Latest versions)
azure-identity>=1.15.0
azure-storage-blob>=12.19.0
azure-keyvault-secrets>=4.7.0
azure-servicebus>=7.11.0
azure-monitor-opentelemetry>=1.2.0

# Data Processing & Analysis
asyncio-mqtt>=0.13.0
aiohttp>=3.9.0
fastapi>=0.104.0
pydantic>=2.5.0

# Monitoring & Logging
applicationinsights>=0.11.10
opencensus-ext-azure>=1.1.13

# Development & Testing
pytest>=7.4.0
pytest-asyncio>=0.21.0
black>=23.10.0
flake8>=6.1.0

# Performance & Optimization
psutil>=5.9.6
memory-profiler>=0.61.0
line-profiler>=4.1.0
"""

    with open("requirements.txt", "w") as f:
        f.write(requirements)

    print("✅ Updated requirements.txt")


def create_local_settings():
    """Create local.settings.json for development"""

    print("⚙️ Creating local.settings.json...")

    local_settings = {
        "IsEncrypted": False,
        "Values": {
            "AzureWebJobsStorage": "",
            "FUNCTIONS_WORKER_RUNTIME": "python",
            "FUNCTIONS_WORKER_RUNTIME_VERSION": "3.13",
            "FUNCTIONS_EXTENSION_VERSION": "~4",
            "AZURE_STORAGE_ACCOUNT": "stlifeplatformprod",
            "AZURE_KEY_VAULT": "kv-life-platform-prod",
            "AZURE_SERVICE_BUS": "sb-life-platform-prod",
            "LIFE_ENVIRONMENT": "production",
            "LIFE_PLATFORM_VERSION": "2025.1.0-PRODUCTION",
            "APPINSIGHTS_INSTRUMENTATIONKEY": "",
            "APPLICATIONINSIGHTS_CONNECTION_STRING": "",
        },
        "Host": {"LocalHttpPort": 7071, "CORS": "*", "CORSCredentials": False},
    }

    with open("local.settings.json", "w") as f:
        json.dump(local_settings, f, indent=2)

    print("✅ Created local.settings.json")


def create_deployment_script():
    """Create Azure deployment script with Python 3.13"""

    print("🚀 Creating deployment script...")

    script_content = f"""#!/bin/bash
# L.I.F.E Platform - Python 3.13 Deployment Script
# Azure Marketplace Ready Deployment

set -e

echo "🧠 L.I.F.E Platform - Python 3.13 Deployment"
echo "============================================="

# Configuration
FUNC_APP_NAME="{FUNCTION_APP_NAME}"
RESOURCE_GROUP="{RESOURCE_GROUP}"
PYTHON_VERSION="{PYTHON_VERSION}"

# Update Function App settings for Python 3.13
echo "📝 Updating Function App settings for Python 3.13..."
az functionapp config appsettings set \\
    --resource-group $RESOURCE_GROUP \\
    --name $FUNC_APP_NAME \\
    --settings \\
    FUNCTIONS_WORKER_RUNTIME=python \\
    FUNCTIONS_WORKER_RUNTIME_VERSION=$PYTHON_VERSION \\
    FUNCTIONS_EXTENSION_VERSION=~4 \\
    LIFE_PLATFORM_VERSION=2025.1.0-PRODUCTION \\
    AZURE_STORAGE_ACCOUNT=stlifeplatformprod \\
    AZURE_KEY_VAULT=kv-life-platform-prod \\
    AZURE_SERVICE_BUS=sb-life-platform-prod \\
    LIFE_ENVIRONMENT=production

echo "✅ Updated Function App settings"

# Create deployment package
echo "📦 Creating deployment package..."
zip -r deployment.zip . -x "*.git*" "*.vscode*" "__pycache__/*" "*.pyc" "venv/*" "env/*"

echo "🚀 Deploying to Azure Functions..."
az functionapp deployment source config-zip \\
    --resource-group $RESOURCE_GROUP \\
    --name $FUNC_APP_NAME \\
    --src deployment.zip

echo "⏳ Waiting for deployment to complete..."
sleep 30

# Test the deployment
echo "🧪 Testing deployment..."
echo "Testing validation endpoint..."
curl -s "https://$FUNC_APP_NAME.azurewebsites.net/api/validate-ingestion" | jq . || echo "Validation test failed"

echo "Testing ingestion stats..."
curl -s "https://$FUNC_APP_NAME.azurewebsites.net/api/ingestion-stats" | jq . || echo "Stats test failed"

echo "Testing EEG ingestion..."
curl -s -X POST "https://$FUNC_APP_NAME.azurewebsites.net/api/ingest-external-eeg" \\
     -H "Content-Type: application/json" \\
     -d '{{"mode": "full_cycle"}}' | jq . || echo "Ingestion test failed"

echo ""
echo "🎉 Deployment completed!"
echo "=================================="
echo "Function App: https://$FUNC_APP_NAME.azurewebsites.net"
echo "API Endpoints:"
echo "  - Validate: https://$FUNC_APP_NAME.azurewebsites.net/api/validate-ingestion"
echo "  - Stats: https://$FUNC_APP_NAME.azurewebsites.net/api/ingestion-stats"  
echo "  - Ingest: https://$FUNC_APP_NAME.azurewebsites.net/api/ingest-external-eeg"
echo "=================================="
"""

    with open("deploy_python313.sh", "w") as f:
        f.write(script_content)

    # Make executable
    os.chmod("deploy_python313.sh", 0o755)

    # Also create Windows batch version
    batch_content = f"""@echo off
REM L.I.F.E Platform - Python 3.13 Deployment Script (Windows)
REM Azure Marketplace Ready Deployment

echo 🧠 L.I.F.E Platform - Python 3.13 Deployment
echo =============================================

SET FUNC_APP_NAME={FUNCTION_APP_NAME}
SET RESOURCE_GROUP={RESOURCE_GROUP}
SET PYTHON_VERSION={PYTHON_VERSION}

echo 📝 Updating Function App settings for Python 3.13...
call az functionapp config appsettings set ^
    --resource-group %RESOURCE_GROUP% ^
    --name %FUNC_APP_NAME% ^
    --settings ^
    FUNCTIONS_WORKER_RUNTIME=python ^
    FUNCTIONS_WORKER_RUNTIME_VERSION=%PYTHON_VERSION% ^
    FUNCTIONS_EXTENSION_VERSION=~4 ^
    LIFE_PLATFORM_VERSION=2025.1.0-PRODUCTION ^
    AZURE_STORAGE_ACCOUNT=stlifeplatformprod ^
    AZURE_KEY_VAULT=kv-life-platform-prod ^
    AZURE_SERVICE_BUS=sb-life-platform-prod ^
    LIFE_ENVIRONMENT=production

echo ✅ Updated Function App settings

echo 📦 Creating deployment package...
powershell -Command "Compress-Archive -Path . -DestinationPath deployment.zip -Force -CompressionLevel Optimal"

echo 🚀 Deploying to Azure Functions...
call az functionapp deployment source config-zip ^
    --resource-group %RESOURCE_GROUP% ^
    --name %FUNC_APP_NAME% ^
    --src deployment.zip

echo ⏳ Waiting for deployment to complete...
timeout /t 30 /nobreak

echo 🧪 Testing deployment...
curl "https://%FUNC_APP_NAME%.azurewebsites.net/api/validate-ingestion"
curl "https://%FUNC_APP_NAME%.azurewebsites.net/api/ingestion-stats"
curl -X POST "https://%FUNC_APP_NAME%.azurewebsites.net/api/ingest-external-eeg" -H "Content-Type: application/json" -d "{{\\"mode\\": \\"full_cycle\\"}}"

echo.
echo 🎉 Deployment completed!
echo ==================================
echo Function App: https://%FUNC_APP_NAME%.azurewebsites.net
echo API Endpoints:
echo   - Validate: https://%FUNC_APP_NAME%.azurewebsites.net/api/validate-ingestion
echo   - Stats: https://%FUNC_APP_NAME%.azurewebsites.net/api/ingestion-stats
echo   - Ingest: https://%FUNC_APP_NAME%.azurewebsites.net/api/ingest-external-eeg
echo ==================================
pause
"""

    with open("deploy_python313.bat", "w") as f:
        f.write(batch_content)

    print("✅ Created deployment scripts")


def main():
    """Main execution function"""

    print("=" * 70)
    print("🐍 L.I.F.E Platform - Python 3.13 Upgrade & API Fix")
    print("=" * 70)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Target: {FUNCTION_APP_NAME}")
    print(f"🐍 Python Version: {PYTHON_VERSION}")
    print("=" * 70)

    try:
        # Create all necessary files
        create_function_app_structure()
        update_host_json()
        update_requirements_txt()
        create_local_settings()
        create_deployment_script()

        print("\n✅ ALL FILES CREATED SUCCESSFULLY!")
        print("\n📋 Next Steps:")
        print(
            "1. Run: deploy_python313.bat (Windows) or ./deploy_python313.sh (Linux/Mac)"
        )
        print("2. Wait for deployment to complete")
        print("3. Test API endpoints")
        print("4. Update Enhanced Dashboard to use new endpoints")

        print("\n🔗 Your Function App URLs:")
        print(f"  Main: https://{FUNCTION_APP_NAME}.azurewebsites.net")
        print(f"  API: https://{FUNCTION_APP_NAME}.azurewebsites.net/api/")

        print("\n🎉 Ready for Python 3.13 deployment!")

    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        return False

    return True


if __name__ == "__main__":
    success = main()
    if success:
        print("\n🚀 Execute deploy_python313.bat to deploy with Python 3.13!")
    else:
        print("\n💥 Setup failed. Please check the errors above.")
