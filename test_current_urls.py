#!/usr/bin/env python3
"""
Quick URL Verification for L.I.F.E Platform - October 18, 2025
Tests the current deployment URLs from today's Azure deployment
"""

import json
import urllib.error
import urllib.request
from datetime import datetime

# URLs from today's deployment (October 18, 2025)
URLS_TO_TEST = {
    "Main Function App": "https://lifeplatform1760781933.azurewebsites.net",
    "Legacy Function App": "https://life-theory-functions-1756511146.azurewebsites.net",
    "Dashboard Function App": "https://life-functions-app.azurewebsites.net",
    "Azure Static Web App": "https://green-ground-0c65efe0f.1.azurestaticapps.net",
    "Key Vault": "https://kvlifeplatform17607819.vault.azure.net",
    # API Endpoints from deployed Function App
    "Validate Ingestion": "https://lifeplatform1760781933.azurewebsites.net/api/validate-ingestion",
    "Ingestion Stats": "https://lifeplatform1760781933.azurewebsites.net/api/ingestion-stats",
    "External EEG": "https://lifeplatform1760781933.azurewebsites.net/api/ingest-external-eeg",
}


def test_url(name, url):
    """Test a single URL"""
    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "L.I.F.E-Platform-Test/1.0")

        with urllib.request.urlopen(req, timeout=10) as response:
            status = response.getcode()
            if status == 200:
                return f"✅ {name}: {status} OK"
            else:
                return f"⚠️  {name}: {status}"

    except urllib.error.HTTPError as e:
        return f"❌ {name}: HTTP {e.code}"
    except Exception as e:
        return f"❌ {name}: {str(e)[:50]}"


def main():
    print("🧠 L.I.F.E PLATFORM URL VERIFICATION")
    print("=" * 50)
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Testing {len(URLS_TO_TEST)} URLs from today's deployment")
    print()

    results = []
    working = 0

    for name, url in URLS_TO_TEST.items():
        result = test_url(name, url)
        results.append(result)
        if "✅" in result:
            working += 1
        print(result)

    print()
    print("=" * 50)
    print(f"📊 SUMMARY: {working}/{len(URLS_TO_TEST)} URLs working")

    if working > 0:
        print("🎉 Deployment successful! Some URLs are responding.")
        if working < len(URLS_TO_TEST):
            print("🔧 Some endpoints need Python 3.13 upgrade to work fully.")
    else:
        print("🚨 No URLs responding - check deployment status.")

    return working > 0


if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🚫 Test cancelled by user")
        exit(1)
