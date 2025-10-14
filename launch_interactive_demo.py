"""
L.I.F.E Platform Interactive Demo Launcher
Launches the comprehensive interactive demo with full feature set

Copyright 2025 - Sergio Paya Borrull
Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import os
import webbrowser
from pathlib import Path


def main():
    print("=" * 70)
    print("🚀 L.I.F.E PLATFORM - INTERACTIVE LAUNCH DEMO")
    print("=" * 70)
    print("Learning Individually From Experience")
    print("Revolutionary Neuroplasticity & EEG Analysis Platform")
    print("October 15, 2025 - Interactive Demo Ready")
    print("=" * 70)
    print()

    # Check for the interactive demo file
    demo_file = Path("LIFE_PLATFORM_INTERACTIVE_LAUNCH_DEMO.html")

    if demo_file.exists():
        print("✅ Interactive Demo Platform detected!")
        print(f"📂 File: {demo_file.name}")
        print(f"📏 Size: {demo_file.stat().st_size / 1024:.1f} KB")
        print()

        print("🌟 Interactive Demo Features:")
        print("   🎭 Interactive Launch Demonstrations")
        print("   📊 Real-time Performance Analytics")
        print("   🔧 Admin Intelligence Panel")
        print("   🔍 Personal Search Integration")
        print("   🧠 Neuroplasticity Visualization")
        print("   ⚡ EEG Processing Analysis")
        print("   ☁️ Azure Marketplace Integration")
        print("   📈 Educational Scenario Demos")
        print()

        print("🚀 Launching Interactive Demo Platform...")

        try:
            # Open in default browser
            webbrowser.open(str(demo_file.absolute()))

            print("✅ Interactive Demo launched successfully!")
            print()
            print("🎉 Platform Status: ACTIVE")
            print("🌐 Opened in default browser")
            print()
            print("💡 Demo Navigation Tips:")
            print("   • Use the admin panel for advanced features")
            print("   • Try the personal search functionality")
            print("   • Explore different demo scenarios")
            print("   • Check real-time performance metrics")
            print()
            print("🔗 Direct file access:")
            print(f"   file:///{demo_file.absolute()}")

        except Exception as e:
            print(f"❌ Error launching demo: {e}")
            print("💡 Try opening the file manually in your browser")
            print(f"File location: {demo_file.absolute()}")

    else:
        print("❌ Interactive Demo Platform not found!")
        print("Expected file: LIFE_PLATFORM_INTERACTIVE_LAUNCH_DEMO.html")
        print()

        # Look for alternative files
        html_files = list(Path(".").glob("*.html"))
        if html_files:
            print("📋 Available HTML files:")
            for file in html_files[:10]:  # Show first 10
                print(f"   • {file.name}")
            if len(html_files) > 10:
                print(f"   ... and {len(html_files) - 10} more files")
        else:
            print("No HTML files found in current directory")

    print()
    print("=" * 70)
    print("🎊 L.I.F.E Platform Interactive Demo Session")
    print("=" * 70)
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
