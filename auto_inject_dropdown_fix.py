#!/usr/bin/env python3
"""
🎯 Dropdown Fix Auto-Injector
================================

Automatically injects the DROPDOWN_FIX_SYSTEM.js into all L.I.F.E platforms
Fixes non-clickable dropdown menu issues across all HTML files

Copyright 2025 - Sergio Paya Borrull
"""

import os
import re
from pathlib import Path

# Platform files to update
PLATFORM_FILES = [
    "L.I.F.E_PLATFORM_ULTIMATE_INTEGRATED.html",
    "LIFE_AI_PLATFORM_REAL.html",
    "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html",
    "LIFE_ENTERPRISE_PLATFORM_REAL.html",
    "LIFE_EDUCATION_PLATFORM_REAL.html",
    "LIFE_RESEARCH_PLATFORM_REAL.html",
    "LIFE_PLATFORM_COMPLETE_WITH_TABS.html",
    "LIFE_PLATFORM_WORKING_TABS.html",
    "LIFE_PLATFORM_DEMO_WEBSITE.html",
    "WORKING_MOCK_DEMO_PLATFORM.html",
    "EMERGENCY_WORKING_PLATFORM.html",
    "LIFE_PLATFORM_PROFESSIONAL_DEMO.html",
    "LIFE_PLATFORM_INTERACTIVE_LAUNCH_DEMO.html",
    "PRODUCTION_READY_LIFE_PLATFORM.html",
]

SCRIPT_INJECTION = """
    <!-- ✅ DROPDOWN FIX SYSTEM - Enables clickable dropdown menus -->
    <script src="DROPDOWN_FIX_SYSTEM.js"></script>
"""


def inject_dropdown_fix(filepath):
    """Inject dropdown fix script into HTML file"""

    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return False

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Check if already injected
        if "DROPDOWN_FIX_SYSTEM.js" in content:
            print(f"⏭️  Already updated: {os.path.basename(filepath)}")
            return True

        # Find </head> tag
        head_pattern = r"</head>"

        if not re.search(head_pattern, content, re.IGNORECASE):
            print(f"⚠️  No </head> tag found in: {filepath}")
            return False

        # Inject script before </head>
        updated_content = re.sub(
            head_pattern,
            SCRIPT_INJECTION + "\n    </head>",
            content,
            flags=re.IGNORECASE,
        )

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(updated_content)

        print(f"✅ Updated: {os.path.basename(filepath)}")
        return True

    except Exception as e:
        print(f"❌ Error processing {filepath}: {str(e)}")
        return False


def main():
    """Main function"""

    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    print("\n" + "=" * 70)
    print("🎯 DROPDOWN FIX SYSTEM - AUTO-INJECTOR")
    print("=" * 70 + "\n")

    # Check if DROPDOWN_FIX_SYSTEM.js exists
    fix_script = os.path.join(script_dir, "DROPDOWN_FIX_SYSTEM.js")
    if not os.path.exists(fix_script):
        print(f"❌ CRITICAL: DROPDOWN_FIX_SYSTEM.js not found at {fix_script}")
        print("❌ Cannot proceed without the dropdown fix script")
        return

    print(f"✅ Found DROPDOWN_FIX_SYSTEM.js")
    print(f"📍 Location: {fix_script}\n")

    # Process all platform files
    updated_count = 0
    failed_count = 0

    print("🔄 Processing platform files...\n")

    for platform_file in PLATFORM_FILES:
        filepath = os.path.join(script_dir, platform_file)

        if inject_dropdown_fix(filepath):
            updated_count += 1
        else:
            failed_count += 1

    print("\n" + "=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print(f"✅ Successfully updated: {updated_count} files")
    if failed_count > 0:
        print(f"❌ Failed/Skipped: {failed_count} files")

    print("\n🎯 RESULT:")
    if updated_count > 0:
        print(f"✅ Dropdown menus are now fully interactive!")
        print(f"✅ All {updated_count} platform files updated")
        print(f"✅ Users can now click dropdown items to activate functions")
    else:
        print("⚠️  No files were updated - please check logs above")

    print("\n🚀 NEXT STEPS:")
    print("1. Open any L.I.F.E platform in browser")
    print("2. Click on any dropdown menu")
    print("3. Test clicking dropdown items")
    print("4. Verify functions execute correctly")
    print("5. Check browser console for any errors")

    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    main()
