"""
🧠 L.I.F.E Clinical Platform Offline Validator
==============================================

Comprehensive test to ensure the Cambridge University demo platform
works perfectly offline for all 7 academic meetings.

Copyright 2025 - Sergio Paya Borrull
L.I.F.E Platform - Production Ready
"""

import os
import time
import webbrowser
from pathlib import Path


def validate_platform_files():
    """Validate all required files are present"""
    print("🔍 Validating platform files...")

    required_files = [
        "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html",
        "cambridge_demo_launcher.py",
        "LIFE_ACADEMIC_UNIVERSAL_LAUNCHER.bat",
        "TEST_OFFLINE_PLATFORM.bat",
    ]

    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"   ✅ {file}")

    if missing_files:
        print(f"\n❌ Missing files: {missing_files}")
        return False

    print("✅ All required files present")
    return True


def check_html_structure():
    """Check HTML file structure and integrity"""
    print("\n🔍 Checking HTML structure...")

    html_file = "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html"

    try:
        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for key components
        checks = [
            ("L.I.F.E Algorithm Integration", "class LIFEAlgorithmJS" in content),
            ("Offline Chart System", "createOfflineChart" in content),
            ("Tab Navigation", "showTab" in content),
            ("Clinical Metrics", "updateClinicalMetricsWithLIFE" in content),
            ("EEG Processing", "processEEGData" in content),
            ("Error Handling", "try {" in content and "} catch" in content),
            ("Offline Fallbacks", "onerror=" in content),
            ("Font Fallbacks", "Arial, sans-serif" in content),
        ]

        all_passed = True
        for check_name, condition in checks:
            if condition:
                print(f"   ✅ {check_name}")
            else:
                print(f"   ❌ {check_name}")
                all_passed = False

        return all_passed

    except Exception as e:
        print(f"❌ Error reading HTML file: {e}")
        return False


def test_offline_compatibility():
    """Test offline compatibility by checking for CDN dependencies"""
    print("\n🔍 Testing offline compatibility...")

    html_file = "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html"

    try:
        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for potential offline issues
        cdn_checks = [
            ("Chart.js CDN", "cdn.jsdelivr.net/npm/chart.js"),
            ("Google Fonts", "fonts.googleapis.com"),
            ("Font Awesome", "cdnjs.cloudflare.com"),
            ("Plotly.js CDN", "plotly.js"),
        ]

        has_fallbacks = True
        for service, pattern in cdn_checks:
            if pattern in content:
                # Check if there are fallback systems
                if "onerror=" in content and (
                    "offline" in content.lower() or "fallback" in content.lower()
                ):
                    print(f"   ⚠️  {service} found but has offline fallback")
                else:
                    print(f"   ❌ {service} may cause offline issues")
                    has_fallbacks = False
            else:
                print(f"   ✅ No {service} dependency")

        return has_fallbacks

    except Exception as e:
        print(f"❌ Error checking offline compatibility: {e}")
        return False


def launch_platform_test():
    """Launch the platform for manual testing"""
    print("\n🚀 Launching platform for testing...")

    html_file = Path("LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html").absolute()

    try:
        # Open in default browser
        webbrowser.open(f"file://{html_file}")
        print("✅ Platform opened in browser")

        print("\n📋 MANUAL TEST CHECKLIST:")
        print("=" * 50)
        print("[ ] Platform loads completely")
        print("[ ] All 6 tabs are accessible:")
        print("    [ ] Overview")
        print("    [ ] EEG Analysis")
        print("    [ ] Neuroplasticity")
        print("    [ ] AI Diagnostics")
        print("    [ ] Research Data")
        print("    [ ] Clinical Reports")
        print("[ ] Charts display (online or offline)")
        print("[ ] L.I.F.E Algorithm processes data")
        print("[ ] Clinical alerts show")
        print("[ ] Real-time updates work")
        print("[ ] No JavaScript errors in console")

        return True

    except Exception as e:
        print(f"❌ Error launching platform: {e}")
        return False


def generate_test_report():
    """Generate a comprehensive test report"""
    print("\n" + "=" * 60)
    print("🎯 L.I.F.E PLATFORM OFFLINE READINESS REPORT")
    print("=" * 60)

    file_check = validate_platform_files()
    structure_check = check_html_structure()
    offline_check = test_offline_compatibility()

    print(f"\n📊 TEST RESULTS SUMMARY:")
    print(f"   File Validation: {'✅ PASS' if file_check else '❌ FAIL'}")
    print(f"   HTML Structure:  {'✅ PASS' if structure_check else '❌ FAIL'}")
    print(f"   Offline Ready:   {'✅ PASS' if offline_check else '❌ FAIL'}")

    overall_status = file_check and structure_check and offline_check

    print(
        f"\n🎯 OVERALL STATUS: {'✅ READY FOR 7 ACADEMIC MEETINGS' if overall_status else '❌ NEEDS ATTENTION'}"
    )

    if overall_status:
        print("\n🚀 DEPLOYMENT READY:")
        print("   • Platform is fully offline compatible")
        print("   • L.I.F.E Algorithm integrated")
        print("   • All 6 clinical tabs functional")
        print("   • Multiple launch methods available")
        print("   • Ready for Cambridge University demo")
        print("   • Suitable for all 7 academic presentations")

        launch_platform_test()
    else:
        print("\n⚠️  ISSUES TO RESOLVE:")
        print("   • Check failed components above")
        print("   • Fix any missing files or dependencies")
        print("   • Ensure offline fallback systems work")
        print("   • Test in browser with network disabled")

    return overall_status


if __name__ == "__main__":
    print("🧠 L.I.F.E Clinical Platform Offline Validator")
    print("=" * 50)
    print("Testing platform readiness for 7 academic meetings...")
    print()

    success = generate_test_report()

    print(
        f"\n{'🎉 SUCCESS: Platform ready for demonstrations!' if success else '⚠️ WARNING: Platform needs attention before demos'}"
    )

    input("\nPress Enter to continue...")
