"""
🧠 L.I.F.E Platform Enhanced Dashboard Server
Serves the enhanced dashboard with tabbed navigation
"""

import http.server
import socketserver
import threading
import time
import webbrowser
from pathlib import Path


class QuietHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP Request Handler with minimal logging"""
    
    def log_message(self, format, *args):
        # Only log errors, suppress normal requests
        if "404" in str(args) or "500" in str(args):
            super().log_message(format, *args)

def start_server():
    """Start the HTTP server for the enhanced dashboard"""
    
    PORT = 8082
    current_dir = Path(__file__).parent
    
    print("🧠 Starting Enhanced L.I.F.E Platform Dashboard Server...")
    print(f"📂 Serving from: {current_dir}")
    print(f"🌐 Server starting on port: {PORT}")
    
    # Change to the current directory
    import os
    os.chdir(current_dir)
    
    try:
        with socketserver.TCPServer(("", PORT), QuietHTTPRequestHandler) as httpd:
            print(f"✅ Server running at: http://localhost:{PORT}")
            print(f"🎯 Enhanced Dashboard: http://localhost:{PORT}/life_enhanced_dashboard.html")
            
            # Start server in background thread
            server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
            server_thread.start()
            
            # Wait a moment for server to start
            time.sleep(1)
            
            # Open the enhanced dashboard in browser
            dashboard_url = f"http://localhost:{PORT}/life_enhanced_dashboard.html"
            print(f"\n🚀 Opening Enhanced Dashboard: {dashboard_url}")
            webbrowser.open(dashboard_url)
            
            print("\n🎉 Enhanced Dashboard Features:")
            print("   🎯 Tabbed Interface Navigation")
            print("   📊 External EEG Ingestion Tab")
            print("   🧠 Neural Processing Metrics")
            print("   📈 Real-time Learning Analytics")
            print("   🔍 System Monitoring")
            
            print("\n📋 Usage Instructions:")
            print("   1. Click the 'Ingest EEG Data' tab")
            print("   2. Click 'Start External EEG Ingestion'")
            print("   3. Watch real-time progress and statistics")
            print("   4. Explore other tabs for comprehensive metrics")
            
            print(f"\n🔗 Dashboard URL: {dashboard_url}")
            print("Press Ctrl+C to stop the server...")
            
            # Keep server running
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Server stopped by user")
                
    except OSError as e:
        if e.errno == 10048:  # Address already in use on Windows
            print(f"❌ Port {PORT} is already in use. Try a different port or stop the existing server.")
        else:
            print(f"❌ Server error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    print("=" * 70)
    print("🧠 L.I.F.E Platform - Enhanced Dashboard Server")
    print("=" * 70)
    
    start_server()    start_server()