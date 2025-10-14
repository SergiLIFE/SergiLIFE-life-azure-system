"""
Simple L.I.F.E Theory Platform Launcher
Works with existing HTML files and provides easy access

Copyright 2025 - Sergio Paya Borrull
"""

import os
import webbrowser
from pathlib import Path


def main():
    print("=" * 60)
    print("🧠 L.I.F.E Theory Platform - Simple Launcher")
    print("=" * 60)
    print("Learning Individually From Experience")
    print("Revolutionary Neuroplasticity Dashboard")
    print("=" * 60)
    print()

    # Look for platform files
    html_files = list(Path(".").glob("*.html"))

    if not html_files:
        print("❌ No HTML files found in current directory")
        return

    print("🔍 Available Platform Files:")
    for i, file in enumerate(html_files, 1):
        print(f"   {i}. {file.name}")

    print()

    # Try to find the main platform file
    platform_files = [
        f for f in html_files if "life" in f.name.lower() or "LIFE" in f.name
    ]

    if platform_files:
        main_file = platform_files[0]
        print(f"🎯 Auto-detected main platform: {main_file.name}")
    else:
        main_file = html_files[0] if html_files else None
        print(f"🎯 Using first available file: {main_file.name}")

    if main_file:
        print(f"🚀 Launching {main_file.name}...")
        try:
            webbrowser.open(str(main_file.absolute()))
            print("✅ Platform opened in default browser successfully!")
            print()
            print("🌟 L.I.F.E Platform Features:")
            print("   📊 Real-time Performance Metrics")
            print("   🧬 Neuroplasticity Analysis")
            print("   ⚡ Quantum-Enhanced Processing")
            print("   🤖 10 Core Algorithm Suite")
            print("   📈 Exponential Learning Engine")
            print()
            print("🎉 Platform is now running!")
        except Exception as e:
            print(f"❌ Error opening platform: {e}")
            print("💡 Try opening the file manually in your browser")

    print()
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
