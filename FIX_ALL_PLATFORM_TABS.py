"""
🔧 MASTER TAB FIX SCRIPT - Fixes tab functionality across ALL L.I.F.E Platforms
October 17, 2025

PROBLEM: Tabs don't work because showTab(tabName) tries to use event.target
SOLUTION: Replace with reliable button finding logic
"""

import os
import re
from pathlib import Path

# ============================================================================
# BROKEN TAB FUNCTION PATTERN (What we're fixing FROM)
# ============================================================================
BROKEN_PATTERN = r"""        // Tab Management
        function showTab\(tabName\) \{
            const tabs = document\.querySelectorAll\('\.tab-content'\);
            tabs\.forEach\(tab => tab\.classList\.remove\('active'\)\);

            const navTabs = document\.querySelectorAll\('\.nav-tab'\);
            navTabs\.forEach\(tab => tab\.classList\.remove\('active'\)\);

            document\.getElementById\(tabName\)\.classList\.add\('active'\);
            event\.target\.classList\.add\('active'\);"""

# ============================================================================
# FIXED TAB FUNCTION (What we're fixing TO)
# ============================================================================
FIXED_FUNCTION = """        // Tab Management - FIXED VERSION
        function showTab(tabName) {
            // Hide all tab content
            const tabs = document.querySelectorAll('.tab-content');
            tabs.forEach(tab => tab.classList.remove('active'));

            // Remove active class from all buttons
            const navTabs = document.querySelectorAll('.nav-tab');
            navTabs.forEach(tab => tab.classList.remove('active'));

            // Show selected tab content
            const selectedTab = document.getElementById(tabName);
            if (selectedTab) {
                selectedTab.classList.add('active');
            }

            // Mark the clicked button as active (RELIABLE METHOD)
            const buttons = document.querySelectorAll('.nav-tab');
            buttons.forEach(btn => {
                if (btn.getAttribute('onclick') && btn.getAttribute('onclick').includes(`'${tabName}'`)) {
                    btn.classList.add('active');
                }
            });

            // Special handling for neural network tab
            if (tabName === 'neural-networks') {
                if (typeof generateNeuralNetwork === 'function') {
                    generateNeuralNetwork();
                }
            }
        }"""

# ============================================================================
# FIND ALL PLATFORM FILES
# ============================================================================
WORKSPACE = r"c:\Users\Sergio Paya Borrull\OneDrive\Documents\GitHub\.vscode\New folder\SergiLIFE-life-azure-system\SergiLIFE-life-azure-system"


def find_platform_files():
    """Find all HTML platform files"""
    platforms = []
    for file in Path(WORKSPACE).glob("*.html"):
        filename = file.name.upper()
        if "PLATFORM" in filename or "LIFE" in filename:
            platforms.append(str(file))
    return sorted(platforms)


def fix_tabs_in_file(filepath):
    """Fix tab function in a single file"""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Check if file already has the fixed version
        if "FIXED VERSION" in content:
            return "ALREADY_FIXED", 0

        # Check if file has the broken pattern
        if "event.target.classList.add" in content:
            # Replace the broken function with fixed one
            original_length = len(content)

            # More flexible pattern matching
            broken_pattern_flexible = r"function showTab\(tabName\) \{[^}]*event\.target\.classList\.add[^}]*\}"

            # Try regex replacement first
            if re.search(broken_pattern_flexible, content, re.DOTALL):
                content = re.sub(
                    broken_pattern_flexible, FIXED_FUNCTION, content, flags=re.DOTALL
                )
                new_length = len(content)

                # Write the fixed content back
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)

                return "FIXED", abs(new_length - original_length)

        # Check if it's already using the fixed pattern (querySelector approach)
        if "getAttribute('onclick')" in content and "showTab" in content:
            return "ALREADY_MODERN", 0

        return "NO_MATCH", 0

    except Exception as e:
        return "ERROR", str(e)


# ============================================================================
# MAIN EXECUTION
# ============================================================================
def main():
    print("=" * 80)
    print("🔧 L.I.F.E PLATFORM TAB FIX MASTER SCRIPT")
    print("=" * 80)
    print()

    platforms = find_platform_files()
    print(f"📁 Found {len(platforms)} platform files to check\n")

    results = {
        "FIXED": [],
        "ALREADY_FIXED": [],
        "ALREADY_MODERN": [],
        "NO_MATCH": [],
        "ERROR": [],
    }

    for platform_path in platforms:
        filename = Path(platform_path).name
        status, info = fix_tabs_in_file(platform_path)
        results[status].append((filename, info))

        # Print progress
        status_emoji = {
            "FIXED": "✅",
            "ALREADY_FIXED": "⏭️",
            "ALREADY_MODERN": "🆕",
            "NO_MATCH": "❓",
            "ERROR": "❌",
        }

        print(f"{status_emoji.get(status, '❓')} {filename:50} {status:15} {info}")

    print()
    print("=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    print(f"✅ Fixed:            {len(results['FIXED']):3} files")
    print(f"⏭️  Already Fixed:    {len(results['ALREADY_FIXED']):3} files")
    print(f"🆕 Already Modern:   {len(results['ALREADY_MODERN']):3} files")
    print(f"❓ No Match:         {len(results['NO_MATCH']):3} files")
    print(f"❌ Errors:           {len(results['ERROR']):3} files")
    print()

    if results["FIXED"]:
        print("✅ FIXED FILES:")
        for filename, info in results["FIXED"]:
            print(f"   - {filename} (Δ {info} bytes)")

    if results["ERROR"]:
        print("\n❌ ERROR FILES:")
        for filename, error in results["ERROR"]:
            print(f"   - {filename}: {error}")

    print()
    print("=" * 80)
    print("🎉 TAB FIX COMPLETE!")
    print("=" * 80)
    print()
    print("🧪 NEXT STEPS:")
    print("   1. Reload all platform pages in your browser (F5)")
    print("   2. Click on different tabs - they should NOW WORK")
    print("   3. Report any remaining tab issues with specific platform name")
    print()


if __name__ == "__main__":
    main()
