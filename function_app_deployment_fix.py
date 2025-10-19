#!/usr/bin/env python3
"""
Fix Azure Function App Deployment - Serve L.I.F.E Platform HTML
October 18, 2025 - Complete Platform Integration

This script fixes the Function App to serve the L.I.F.E Platform instead of the generic page.
"""

import json
import os
import shutil
from pathlib import Path

print("🔧 Fixing Azure Function App Deployment - October 18, 2025")
print("=" * 70)

# Define paths
SCRIPT_DIR = Path(__file__).parent
HTML_FILE = SCRIPT_DIR / "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html"
FUNCTION_DIR = SCRIPT_DIR / "function_app"
WWWROOT_DIR = FUNCTION_DIR / "wwwroot"


def create_function_app_structure():
    """Create proper Function App structure to serve HTML"""

    print("📂 Creating Function App structure...")

    # Create directories
    FUNCTION_DIR.mkdir(exist_ok=True)
    WWWROOT_DIR.mkdir(exist_ok=True)

    # Copy HTML file to wwwroot as index.html
    if HTML_FILE.exists():
        shutil.copy2(HTML_FILE, WWWROOT_DIR / "index.html")
        print(f"✅ Copied {HTML_FILE.name} to wwwroot/index.html")
        print(f"   Size: {HTML_FILE.stat().st_size:,} bytes")
    else:
        print(f"❌ HTML file not found: {HTML_FILE}")
        return False

    # Create host.json for Function App configuration
    host_config = {
        "version": "2.0",
        "logging": {
            "applicationInsights": {
                "samplingSettings": {"isEnabled": True, "excludedTypes": "Request"}
            }
        },
        "extensionBundle": {
            "id": "Microsoft.Azure.Functions.ExtensionBundle",
            "version": "[3.*, 4.0.0)",
        },
        "staticWebAssets": {"enabled": True},
    }

    with open(FUNCTION_DIR / "host.json", "w") as f:
        json.dump(host_config, f, indent=2)
    print("✅ Created host.json configuration")

    # Create requirements.txt
    requirements = [
        "azure-functions>=1.11.0",
        "azure-storage-blob>=12.0.0",
        "azure-identity>=1.12.0",
    ]

    with open(FUNCTION_DIR / "requirements.txt", "w") as f:
        f.write("\n".join(requirements))
    print("✅ Created requirements.txt")

    # Create HTTP trigger function to serve the HTML
    http_function_dir = FUNCTION_DIR / "HttpTrigger"
    http_function_dir.mkdir(exist_ok=True)

    # Function definition
    function_json = {
        "scriptFile": "__init__.py",
        "bindings": [
            {
                "authLevel": "anonymous",
                "type": "httpTrigger",
                "direction": "in",
                "name": "req",
                "methods": ["get", "post"],
                "route": "{*route:alpha?}",
            },
            {"type": "http", "direction": "out", "name": "$return"},
        ],
    }

    with open(http_function_dir / "function.json", "w") as f:
        json.dump(function_json, f, indent=2)
    print("✅ Created HTTP trigger function.json")

    # Function code to serve HTML
    function_code = """import logging
import azure.functions as func
import os
from pathlib import Path

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('L.I.F.E Platform HTTP trigger function processed a request.')
    
    try:
        # Get the HTML file path
        html_path = Path(__file__).parent.parent / "wwwroot" / "index.html"
        
        if html_path.exists():
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            return func.HttpResponse(
                html_content,
                status_code=200,
                mimetype="text/html"
            )
        else:
            return func.HttpResponse(
                "<h1>L.I.F.E Platform Loading...</h1><p>HTML file not found. Deployment in progress.</p>",
                status_code=200,
                mimetype="text/html"
            )
            
    except Exception as e:
        logging.error(f"Error serving L.I.F.E Platform: {str(e)}")
        return func.HttpResponse(
            f"<h1>L.I.F.E Platform Error</h1><p>Error loading platform: {str(e)}</p>",
            status_code=500,
            mimetype="text/html"
        )
"""

    with open(http_function_dir / "__init__.py", "w") as f:
        f.write(function_code)
    print("✅ Created HTTP trigger function code")

    return True


def create_deployment_script():
    """Create deployment script for Azure CLI"""

    deployment_script = f"""@echo off
REM Deploy L.I.F.E Platform to Azure Function App
REM October 18, 2025 - Complete Integration

echo 🚀 Deploying L.I.F.E Platform to Azure Function App...
echo Function App: lifeplatform1760781933.azurewebsites.net
echo.

REM Ensure logged in to Azure
az account show >nul 2>&1
if errorlevel 1 (
    echo ❌ Not logged in to Azure. Please run: az login
    pause
    exit /b 1
)

echo ✅ Azure CLI authenticated

REM Deploy the function app
echo 📦 Deploying Function App...
cd function_app
func azure functionapp publish lifeplatform1760781933 --python

if errorlevel 1 (
    echo ❌ Deployment failed
    pause
    exit /b 1
)

echo.
echo ✅ L.I.F.E Platform deployed successfully!
echo 🌐 Function App URL: https://lifeplatform1760781933.azurewebsites.net
echo 🌐 Static Web App URL: https://green-ground-0c65efe0f.1.azurestaticapps.net
echo.
echo The L.I.F.E Platform should now be accessible at both URLs.
pause
"""

    script_path = SCRIPT_DIR / "deploy_to_function_app.bat"
    with open(script_path, "w") as f:
        f.write(deployment_script)
    print(f"✅ Created deployment script: {script_path}")


def main():
    """Main execution"""

    try:
        # Create Function App structure
        if create_function_app_structure():
            print("\n📦 Function App Structure Created Successfully!")

            # Create deployment script
            create_deployment_script()

            print(f"\n🎯 NEXT STEPS:")
            print(f"1. Run: deploy_to_function_app.bat")
            print(f"2. Or manually deploy using Azure CLI:")
            print(f"   cd function_app")
            print(f"   func azure functionapp publish lifeplatform1760781933 --python")
            print(f"")
            print(f"🌐 URLs after deployment:")
            print(f"   Function App: https://lifeplatform1760781933.azurewebsites.net")
            print(
                f"   Static Web App: https://green-ground-0c65efe0f.1.azurestaticapps.net"
            )
            print(f"")
            print(f"✅ Both should serve the complete L.I.F.E Platform with:")
            print(f"   - October 18, 2025 updates")
            print(f"   - Complete experimentP2L algorithm integration")
            print(f"   - 100-cycle test functionality")
            print(f"   - Real-time EEG processing")

        else:
            print("❌ Failed to create Function App structure")

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

    print("=" * 70)
    return True


if __name__ == "__main__":
    main()
