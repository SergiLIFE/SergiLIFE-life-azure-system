"""
Local Test Server for L.I.F.E. Platform Field-Specific Dashboard
Serves the dashboard HTML file for testing purposes
"""

import http.server
import os
import socketserver
import webbrowser
from pathlib import Path


def start_local_server():
    """Start a local HTTP server to serve the dashboard"""

    # Get the directory containing the dashboard file
    dashboard_dir = Path(__file__).parent

    # Change to the dashboard directory
    os.chdir(dashboard_dir)

    # Set up the server
    PORT = 8080
    Handler = http.server.SimpleHTTPRequestHandler

    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print(f"🚀 L.I.F.E. Platform Dashboard Server")
            print(f"📍 Serving at http://localhost:{PORT}")
            print(f"📁 Directory: {dashboard_dir}")
            print(
                f"🌐 Dashboard URL: http://localhost:{PORT}/field-specific-dashboard.html"
            )
            print("\n" + "=" * 60)
            print("📚 EDUCATION FIELD DASHBOARD - READY FOR TESTING")
            print("=" * 60)
            print("\n✅ Features Available:")
            print("   • Field-specific tabs (Education active)")
            print("   • Role-based interface")
            print("   • Azure Marketplace integration")
            print("   • Subscription plans")
            print("   • Real-time metrics simulation")
            print("   • Responsive design")
            print("\n🔍 Test Instructions:")
            print("   1. Click 'Education' tab to see active field")
            print("   2. Try other tabs to see 'Coming Soon' notifications")
            print("   3. Check subscription plans and pricing")
            print("   4. Monitor real-time metric updates")
            print("\n⚡ Press Ctrl+C to stop the server")
            print("-" * 60)

            # Automatically open the dashboard in browser
            dashboard_url = f"http://localhost:{PORT}/field-specific-dashboard.html"
            webbrowser.open(dashboard_url)

            # Start the server
            httpd.serve_forever()

    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        print("✅ Dashboard test session completed")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {PORT} is already in use")
            print(f"💡 Try a different port or stop the existing service")
        else:
            print(f"❌ Error starting server: {e}")


if __name__ == "__main__":
    start_local_server()
