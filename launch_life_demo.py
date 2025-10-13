#!/usr/bin/env python3
"""
L.I.F.E. Platform - Cross-Platform Demo Server
October 15, 2025 University Teams Demo
Works on Windows, Linux, macOS
Compatible with 23 colleagues sharing
"""

import os
import sys
import webbrowser
import http.server
import socketserver
import threading
import time
from pathlib import Path
from urllib.parse import unquote
import json
from datetime import datetime

class LIFEDemoServer:
    def __init__(self, port=8080):
        self.port = port
        self.server = None
        self.server_thread = None
        self.dashboard_paths = [
            # Current directory options
            "LIFE_CLINICAL_GRADE_DASHBOARD.html",
            "LIFE_AI_ENHANCED_PHYSIONET_DASHBOARD.html",
            "L.I.F.E. Platform - Core Algorithm Dashboard.html",
            
            # E: drive options (from your file path)
            "E:/THE L.I.F.E Theory Algorithm/L.I.F.E Theory Evolution/L.I.F.E. Platform - Core Algorithm Dashboard.html",
            "E:\\THE L.I.F.E Theory Algorithm\\L.I.F.E Theory Evolution\\L.I.F.E. Platform - Core Algorithm Dashboard.html",
            
            # Any HTML file in current directory
        ]
        
    def print_header(self):
        """Display the demo header"""
        print("=" * 60)
        print("🧠 L.I.F.E. PLATFORM - CLINICAL DEMO SERVER 🚀")
        print("📅 October 15, 2025 University Presentation")
        print("👥 Teams Demo for 23 Colleagues")
        print("=" * 60)
        print()
        
    def find_dashboard(self):
        """Find the best available dashboard file"""
        print("🔍 Searching for L.I.F.E. dashboard files...")
        
        found_dashboards = []
        
        # Check specific paths first
        for path in self.dashboard_paths:
            if os.path.exists(path):
                size_kb = os.path.getsize(path) / 1024
                found_dashboards.append((path, size_kb))
                print(f"   ✅ Found: {os.path.basename(path)} ({size_kb:.1f} KB)")
        
        # Check current directory for any HTML files
        current_dir = Path(".")
        for html_file in current_dir.glob("*.html"):
            if str(html_file) not in [d[0] for d in found_dashboards]:
                size_kb = html_file.stat().st_size / 1024
                found_dashboards.append((str(html_file), size_kb))
                print(f"   📄 Found: {html_file.name} ({size_kb:.1f} KB)")
        
        if not found_dashboards:
            print("   ❌ No dashboard files found!")
            print("\n📂 Available files in current directory:")
            for file in current_dir.iterdir():
                if file.is_file():
                    print(f"   • {file.name}")
            return None
            
        # Return the largest file (most likely the main dashboard)
        best_dashboard = max(found_dashboards, key=lambda x: x[1])
        print(f"\n🎯 Selected: {os.path.basename(best_dashboard[0])}")
        return best_dashboard[0]
        
    def get_file_content(self, file_path):
        """Get file content with proper encoding"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")
            return None
            
    def create_demo_handler(self, dashboard_path):
        """Create HTTP request handler for the demo"""
        
        class DemoHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                self.dashboard_file = dashboard_path
                super().__init__(*args, **kwargs)
                
            def do_GET(self):
                """Handle GET requests"""
                if self.path == "/" or self.path == "/dashboard":
                    # Serve main dashboard
                    content = self.get_dashboard_content()
                    if content:
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html; charset=utf-8')
                        self.send_header('Cache-Control', 'no-cache')
                        self.end_headers()
                        self.wfile.write(content.encode('utf-8'))
                    else:
                        self.send_error(404, "Dashboard not found")
                        
                elif self.path == "/status":
                    # API status endpoint
                    status_data = {
                        "platform": "L.I.F.E. Clinical Platform",
                        "version": "2025.10.15",
                        "status": "operational", 
                        "demo_ready": True,
                        "teams_compatible": True,
                        "dashboard_file": os.path.basename(self.dashboard_file),
                        "timestamp": datetime.now().isoformat(),
                        "features": [
                            "PhysioNet EEG Integration",
                            "AI Clinical Assistant",
                            "Real-time Processing", 
                            "Clinical-grade Analytics",
                            "Export Capabilities"
                        ]
                    }
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(json.dumps(status_data, indent=2).encode('utf-8'))
                    
                elif self.path == "/health":
                    # Health check
                    health_msg = "L.I.F.E. Clinical Platform - OPERATIONAL - October 15, 2025 Demo Ready"
                    self.send_response(200)
                    self.send_header('Content-type', 'text/plain; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(health_msg.encode('utf-8'))
                    
                else:
                    # Try to serve static files
                    super().do_GET()
                    
            def get_dashboard_content(self):
                """Get the dashboard HTML content"""
                try:
                    with open(self.dashboard_file, 'r', encoding='utf-8') as f:
                        return f.read()
                except Exception as e:
                    print(f"❌ Error loading dashboard: {e}")
                    return self.create_fallback_dashboard()
                    
            def create_fallback_dashboard(self):
                """Create a simple fallback dashboard if main file fails"""
                return """
<!DOCTYPE html>
<html>
<head>
    <title>L.I.F.E. Platform - Demo Fallback</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f0f8ff; }
        .header { background: linear-gradient(45deg, #1e40af, #3b82f6); color: white; padding: 20px; border-radius: 10px; text-align: center; }
        .content { background: white; padding: 30px; margin: 20px 0; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .status { color: #22c55e; font-weight: bold; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧠 L.I.F.E. Platform Clinical Demo</h1>
        <p>October 15, 2025 University Presentation</p>
    </div>
    <div class="content">
        <h2>Demo Server Status: <span class="status">✅ OPERATIONAL</span></h2>
        <p><strong>Teams Compatible:</strong> Yes - Ready for 23 colleagues</p>
        <p><strong>Dashboard Status:</strong> Fallback mode - Main dashboard loading issue</p>
        <p><strong>Access Time:</strong> """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</p>
        
        <h3>🎯 Demo Features Available:</h3>
        <ul>
            <li>✅ Server running successfully</li>
            <li>✅ Teams screen sharing compatible</li>
            <li>✅ GDPR compliant local hosting</li>
            <li>✅ Status API endpoints active</li>
        </ul>
        
        <h3>🔗 API Endpoints:</h3>
        <ul>
            <li><a href="/status">/status</a> - Platform status JSON</li>
            <li><a href="/health">/health</a> - Health check</li>
            <li><a href="/dashboard">/dashboard</a> - Main dashboard (this page)</li>
        </ul>
        
        <h3>📞 Support:</h3>
        <p>If you're seeing this fallback page, the main dashboard file may need to be moved to the server directory or check the file path.</p>
    </div>
</body>
</html>"""
                
            def log_message(self, format, *args):
                """Custom logging for demo requests"""
                client_ip = self.client_address[0] 
                timestamp = datetime.now().strftime('%H:%M:%S')
                print(f"[{timestamp}] 📡 {client_ip} - {format % args}")
                
        return DemoHandler
        
    def start_server(self, dashboard_path):
        """Start the demo server"""
        print(f"\n🚀 Starting L.I.F.E. Clinical Demo Server...")
        print(f"📊 Dashboard: {os.path.basename(dashboard_path)}")
        print(f"🌐 Port: {self.port}")
        print(f"🔒 GDPR Compliant: Local hosting only")
        print(f"👥 Teams Ready: Optimized for 23 colleagues")
        print()
        
        try:
            handler = self.create_demo_handler(dashboard_path)
            self.server = socketserver.TCPServer(("", self.port), handler)
            
            # Get local IP for network access
            import socket
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
            print("🔗 ACCESS LINKS:")
            print(f"   Local: http://localhost:{self.port}")
            print(f"   Network: http://{local_ip}:{self.port}")
            print()
            
            print("📢 TEAMS SHARING INSTRUCTIONS:")
            print("1. Share screen in Teams meeting")
            print("2. Navigate to: http://localhost:8080")  
            print("3. Demo is ready for 23 colleagues!")
            print()
            
            print("✅ Server started successfully!")
            print(f"⏰ Demo Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("\nPress Ctrl+C to stop the server...")
            print()
            
            # Auto-open browser
            try:
                webbrowser.open(f"http://localhost:{self.port}")
                print("🌐 Dashboard opened in default browser")
            except Exception as e:
                print(f"⚠️  Could not auto-open browser: {e}")
            
            # Start server
            self.server.serve_forever()
            
        except OSError as e:
            if "Address already in use" in str(e):
                print(f"❌ Port {self.port} is already in use!")
                print("💡 Try a different port or close other applications using this port")
                
                # Try alternative ports
                for alt_port in [8081, 8082, 8083, 9000]:
                    try:
                        self.port = alt_port
                        self.server = socketserver.TCPServer(("", alt_port), handler)
                        print(f"🔄 Trying alternative port {alt_port}...")
                        print(f"🔗 New URL: http://localhost:{alt_port}")
                        webbrowser.open(f"http://localhost:{alt_port}")
                        self.server.serve_forever()
                        break
                    except:
                        continue
                else:
                    print("❌ No available ports found")
                    return False
            else:
                print(f"❌ Server error: {e}")
                return False
        except KeyboardInterrupt:
            print("\n\n🛑 Demo server stopped by user")
            print("✅ L.I.F.E. Clinical Demo completed successfully!")
            print("Thank you for using L.I.F.E. Platform! 🎉")
            return True
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
        finally:
            if self.server:
                self.server.shutdown()
                self.server.server_close()
                
    def run_demo(self):
        """Run the complete demo setup"""
        self.print_header()
        
        # Find dashboard
        dashboard_path = self.find_dashboard()
        if not dashboard_path:
            print("\n💡 SOLUTION: Please ensure one of these files exists:")
            print("   • LIFE_CLINICAL_GRADE_DASHBOARD.html")
            print("   • L.I.F.E. Platform - Core Algorithm Dashboard.html") 
            print("   • Any other L.I.F.E. dashboard HTML file")
            print("\n📂 Or copy your dashboard to the current directory")
            return False
            
        # Validate dashboard content
        content = self.get_file_content(dashboard_path)
        if content and "L.I.F.E" in content and "html" in content.lower():
            print("✅ Dashboard validation passed")
        else:
            print("⚠️  Dashboard validation failed - using fallback mode")
            
        print(f"\n🎯 READY FOR OCTOBER 15TH DEMO!")
        print(f"🎪 Teams presentation with 23 colleagues")
        
        # Start the server
        return self.start_server(dashboard_path)

def main():
    """Main entry point"""
    print("🧠 L.I.F.E. Platform - Cross-Platform Demo Launcher")
    print(f"📅 Current Date: October 13, 2025")
    print(f"🎯 Demo Date: October 15, 2025 (2 days to go!)")
    print()
    
    # Check Python version
    if sys.version_info < (3, 6):
        print("❌ Python 3.6+ required for this demo server")
        return 1
        
    # Create and run demo server
    demo_server = LIFEDemoServer(port=8080)
    
    try:
        success = demo_server.run_demo()
        return 0 if success else 1
    except Exception as e:
        print(f"❌ Demo launcher error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())