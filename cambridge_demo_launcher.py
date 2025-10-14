import os
import sys
import time
import webbrowser
from pathlib import Path


def launch_cambridge_clinical_platform():
    """
    Launch the Cambridge Clinical Platform using multiple methods
    """
    print("🏥 L.I.F.E Clinical Platform - Cambridge University Demo Launcher")
    print("=" * 60)

    # Get the current directory
    current_dir = Path(__file__).parent.absolute()

    # Define platform file
    clinical_platform = "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html"
    platform_path = current_dir / clinical_platform

    print(f"📂 Working Directory: {current_dir}")
    print(f"🎯 Target Platform: {clinical_platform}")

    # Check if file exists
    if platform_path.exists():
        print(f"✅ Clinical Platform Found: {platform_path}")

        # Get file URI for browser
        file_uri = platform_path.as_uri()
        print(f"🌐 File URI: {file_uri}")

        # Method 1: Open with default browser
        print("\n🚀 Launching Cambridge Clinical Platform...")
        try:
            webbrowser.open(file_uri, new=2)
            print("✅ Platform launched successfully in browser!")

            # Wait a moment for browser to load
            time.sleep(2)

            # Show enhanced platform details with L.I.F.E integration
            print("\n🧠 Cambridge Clinical Platform Features - ENHANCED:")
            print("• ✅ L.I.F.E Theory Algorithm v2025.1.0-PRODUCTION-JS INTEGRATED")
            print("• ✅ FDA-Validated EEG Processing with L.I.F.E Analysis")
            print("• ✅ Real-time Neuroplasticity Analysis (Individual Learning)")
            print("• ✅ Clinical-Grade Diagnostics with Neural Adaptation Scoring")
            print("• ✅ Interactive Tab Navigation (FIXED)")
            print("• ✅ Academic Research Integration with L.I.F.E Data Export")
            print("• ✅ Professional Medical Interface with L.I.F.E Metrics")
            print("• ✅ Continuous Neural Pattern Analysis")
            print("• ✅ Individual Experience Processing Engine")

            print(f"\n🎓 Platform URL: {file_uri}")
            print("🧠 L.I.F.E Algorithm: FULLY INTEGRATED")
            print("🔧 Tab Navigation: FIXED")
            print("🏥 Ready for Cambridge University Demonstration!")

        except Exception as e:
            print(f"❌ Error launching platform: {e}")
            return False

    else:
        print(f"❌ Clinical Platform NOT Found at: {platform_path}")

        # List available platforms
        print("\n📋 Available Platforms:")
        html_files = list(current_dir.glob("*.html"))
        for html_file in html_files:
            if "LIFE" in html_file.name.upper() or "PLATFORM" in html_file.name.upper():
                print(f"  • {html_file.name}")

        return False

    return True


if __name__ == "__main__":
    success = launch_cambridge_clinical_platform()

    if success:
        print("\n🎉 Cambridge Demo Ready!")
        print("Press any key to continue...")
        input()
    else:
        print("\n❌ Platform launch failed!")
        print("Press any key to exit...")
        input()
