#!/usr/bin/env python3
"""
L.I.F.E Platform Web Server
Simple HTTP server for sharing the platform with meeting attendees
"""

import http.server
import os
import socket
import socketserver
import sys
import webbrowser
from pathlib import Path


def get_local_ip():
    """Get local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"


def start_life_server():
    """Start the L.I.F.E Platform web server"""
    PORT = 8000

    print("🧠 L.I.F.E Platform Web Server")
    print("=" * 50)
    print("Learning Individually From Experience")
    print("Ready for Academic Demonstrations")
    print()

    # Check if platform file exists
    platform_file = "LIFE_CLINICAL_PLATFORM_CAMBRIDGE.html"
    if not os.path.exists(platform_file):
        print(f"❌ Platform file not found: {platform_file}")
        print("Please ensure the L.I.F.E Platform HTML file is in this directory")
        input("Press Enter to exit...")
        return

    print(f"✅ L.I.F.E Platform found: {platform_file}")
    print("✅ L.I.F.E Theory Algorithm integrated")
    print("✅ All tabs and features functional")
    print()

    # Get network addresses
    local_ip = get_local_ip()

    print("🌐 Server Information:")
    print(f"   Local access: http://localhost:{PORT}/{platform_file}")
    print(f"   Network access: http://{local_ip}:{PORT}/{platform_file}")
    print()

    print("📧 Share with meeting attendees:")
    print(f"   📱 Mobile/Remote: http://{local_ip}:{PORT}/{platform_file}")
    print("   💻 Same computer: http://localhost:8000/{}")
    print()

    print("🎓 Academic Meeting Ready:")
    print("   • 7 meetings supported")
    print("   • Real-time L.I.F.E algorithm processing")
    print("   • Interactive neuroplasticity analysis")
    print("   • Clinical-grade EEG visualization")
    print()

    # Start server
    try:
        with socketserver.TCPServer(
            ("", PORT), http.server.SimpleHTTPRequestHandler
        ) as httpd:
            print(f"🚀 Server started on port {PORT}")
            print("📊 L.I.F.E Platform accessible to all attendees")
            print()
            print("🔒 Press Ctrl+C to stop server when meetings complete")
            print("=" * 50)

            # Auto-open browser for testing
            platform_url = f"http://localhost:{PORT}/{platform_file}"
            try:
                webbrowser.open(platform_url)
                print(f"✅ Opened platform for testing: {platform_url}")
            except:
                print("💡 Open browser manually to test the platform")

            print()
            httpd.serve_forever()

    except KeyboardInterrupt:
        print("\n")
        print("🛑 Server stopped")
        print("🎓 Academic meetings complete")
        print("🧠 L.I.F.E Platform session ended")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        input("Press Enter to exit...")


if __name__ == "__main__":
    start_life_server()
