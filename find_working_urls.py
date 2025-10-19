#!/usr/bin/env python3
"""
Find ACTUAL working L.I.F.E Platform URLs - October 18, 2025
Tests real URLs to see what's actually deployed and accessible
"""

import urllib.error
import urllib.request

# URLs based on your actual deployment from today
TEST_URLS = [
    # From your terminal output - confirmed deployed
    "https://lifeplatform1760781933.azurewebsites.net",
    # Common Azure patterns
    "https://life-theory-functions-1756511146.azurewebsites.net",
    "https://life-functions-app.azurewebsites.net",
    # Static web apps
    "https://green-ground-0c65efe0f.1.azurestaticapps.net",
    "https://life-platform-webapp.azurestaticapps.net",
    "https://life-platform-webapp.azurewebsites.net",
    # Your actual resource names from deployment
    "https://kvlifeplatform17607819.vault.azure.net",
    "https://stlifeplatform1760781772.blob.core.windows.net",
]


def test_url_simple(url):
    """Simple URL test - just check if it responds"""
    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "L.I.F.E-Test/1.0")

        with urllib.request.urlopen(req, timeout=5) as response:
            return f"✅ WORKING: {url} -> HTTP {response.getcode()}"

    except urllib.error.HTTPError as e:
        if e.code == 404:
            return f"🔶 DEPLOYED (404): {url} -> Function app exists but no content"
        else:
            return f"🔶 DEPLOYED ({e.code}): {url} -> HTTP {e.code}"
    except urllib.error.URLError:
        return f"❌ NOT FOUND: {url} -> Connection failed"
    except Exception as e:
        return f"❌ ERROR: {url} -> {str(e)[:50]}"


def main():
    print("🔍 L.I.F.E PLATFORM - REAL URL DISCOVERY")
    print("=" * 50)
    print("Testing URLs to find what's actually working...")
    print()

    working_urls = []
    deployed_but_empty = []
    not_found = []

    for url in CONFIRMED_WORKING_URLS:
        result = test_url_simple(url)
        print(result)

        if "✅ WORKING" in result:
            working_urls.append(url)
        elif "🔶 DEPLOYED" in result:
            deployed_but_empty.append(url)
        else:
            not_found.append(url)

    print("\n" + "=" * 50)
    print("📊 SUMMARY:")
    print(f"✅ Working URLs: {len(working_urls)}")
    for url in working_urls:
        print(f"   {url}")

    print(f"\n🔶 Deployed but empty: {len(deployed_but_empty)}")
    for url in deployed_but_empty:
        print(f"   {url}")

    print(f"\n❌ Not found: {len(not_found)}")

    if working_urls:
        print(f"\n🎉 GOOD NEWS: {len(working_urls)} URLs are actually working!")
        print("Use these URLs in your application.")
    else:
        print("\n🚨 No URLs are responding with 200 OK.")
        print("Check your Azure deployment status.")

    return working_urls


if __name__ == "__main__":
    working = main()
    print(f"\n✅ Found {len(working)} working URLs")
