"""
L.I.F.E. Platform - Cross-Platform Clinical Demo Server
October 15, 2025 University Presentation
Compatible with Windows, Linux, macOS, and WSL
"""

import http.server
import socketserver
import webbrowser
import os
import sys
import socket
import json
from datetime import datetime
from pathlib import Path

class LIFEDemoServer:
    def __init__(self, port=8080, dashboard_file="LIFE_CLINICAL_GRADE_DASHBOARD.html"):
        self.port = port
        self.dashboard_file = dashboard_file
        self.script_dir = Path(__file__).parent
        self.dashboard_path = self.script_dir / dashboard_file
        
    def print_header(self):
        """Display demo header"""
        print("\n" + "="*50)
        print("   L.I.F.E. PLATFORM CLINICAL DEMO SERVER")
        print("   October 15, 2025 University Presentation")
        print("   Teams Demo for 23 Colleagues")
        print("="*50)
        print(f"\n🎯 Demo Mode: Clinical Grade EEG Analysis")
        print(f"👥 Audience: 23 University Colleagues")
        print(f"📅 Date: October 15, 2025")
        print(f"⏰ Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
    def check_dashboard_file(self):
        """Verify dashboard file exists"""
        print("🔍 Pre-flight Checks:")
        
        if self.dashboard_path.exists():
            file_size = self.dashboard_path.stat().st_size / 1024  # KB
            print(f"   ✅ Clinical dashboard file found")
            print(f"   📊 File size: {file_size:.1f} KB")
            return True
        else:
            print(f"   ❌ Clinical dashboard file missing!")
            print(f"   Expected: {self.dashboard_file}")
            print("\nAvailable HTML files:")
            html_files = list(self.script_dir.glob("*.html"))
            if html_files:
                for file in html_files:
                    print(f"   • {file.name}")
            else:
                print("   No HTML files found")
            print(f"\nPlease ensure {self.dashboard_file} is in the current directory.")
            input("Press Enter to exit...")
            return False
            
    def check_templates(self):
        """Check for template files"""
        if (self.script_dir / "teams_chat_templates.txt").exists():
            print("   ✅ Teams chat templates ready")
        else:
            print("   ⚠️  Teams templates missing (optional)")
            
        if (self.script_dir / "professional_email_templates.md").exists():
            print("   ✅ Email templates prepared")
        else:
            print("   ⚠️  Email templates missing (optional)")
            
    def get_local_ip(self):
        """Get local IP address"""
        try:
            # Connect to a remote server to determine local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except:
            return "localhost"
            
    def check_port_available(self):
        """Check if port is available"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("127.0.0.1", self.port))
                return True
        except:
            return False
            
    def create_custom_handler(self):
        """Create custom HTTP handler for L.I.F.E. dashboard"""
        
        class LIFEHTTPHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, dashboard_file=None, **kwargs):
                self.dashboard_file = dashboard_file
                super().__init__(*args, **kwargs)
                
            def do_GET(self):
                if self.path == "/":
                    self.path = f"/{self.dashboard_file}"
                elif self.path == "/status":
                    self.send_status_response()
                    return
                elif self.path == "/health":
                    self.send_health_response()
                    return
                    
                # Log request
                client_ip = self.client_address[0]
                timestamp = datetime.now().strftime('%H:%M:%S')
                print(f"[{timestamp}] 📡 Request from {client_ip} - {self.path}")
                
                super().do_GET()
                
            def send_status_response(self):
                """Send JSON status response"""
                status_data = {
                    "platform": "L.I.F.E. Clinical Platform",
                    "version": "2025.10.15",
                    "status": "operational",
                    "demo_ready": True,
                    "teams_compatible": True,
                    "gdpr_compliant": True,
                    "timestamp": datetime.now().isoformat(),
                    "features": [
                        "PhysioNet EEG Integration",
                        "AI Clinical Assistant",
                        "Real-time Processing", 
                        "Clinical-grade Analytics",
                        "Export Capabilities"
                    ]
                }
                
                response = json.dumps(status_data, indent=2).encode('utf-8')
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Content-length', len(response))
                self.end_headers()
                self.wfile.write(response)
                
                print("    📊 Status API called")
                
            def send_health_response(self):
                """Send health check response"""
                health_msg = "L.I.F.E. Clinical Platform - OPERATIONAL - October 15, 2025 Demo Ready"
                response = health_msg.encode('utf-8')
                
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.send_header('Content-length', len(response))
                self.end_headers()
                self.wfile.write(response)
                
                print("    💚 Health check OK")
                
            def log_message(self, format, *args):
                # Suppress default logging to avoid duplicates
                pass
                
        return lambda *args, **kwargs: LIFEHTTPHandler(*args, dashboard_file=self.dashboard_file, **kwargs)
        
    def start_server(self, auto_open=True):
        """Start the HTTP server"""
        print("🚀 Launching Clinical Demo Server...")
        print()
        
        # Check port availability
        if not self.check_port_available():
            print(f"⚠️  Port {self.port} is already in use. Trying port {self.port + 1}...")
            self.port += 1
            if not self.check_port_available():
                print(f"❌ Port {self.port} is also in use. Please close other servers.")
                input("Press Enter to exit...")
                return False
                
        local_ip = self.get_local_ip()
        
        print("🌐 Network Configuration:")
        print(f"   Local Access: http://localhost:{self.port}")
        print(f"   Network Access: http://{local_ip}:{self.port}")
        print(f"   Dashboard URL: http://localhost:{self.port}/{self.dashboard_file}")
        print("   Teams Compatible: Yes ✅")
        print("   GDPR Compliant: Local hosting only ✅")
        print()
        
        print("📢 TEAMS SHARING GUIDE:")
        print("1. Click 'Share Screen' in Teams meeting")
        print("2. Select 'Chrome/Browser Window'")
        print(f"3. Navigate to: http://localhost:{self.port}")
        print("4. Copy chat message from teams_chat_templates.txt")
        print("5. Paste in Teams chat for 23 colleagues")
        print()
        
        try:
            # Change to dashboard directory
            os.chdir(self.script_dir)
            
            # Create custom handler
            handler_class = self.create_custom_handler()
            
            # Start server
            with socketserver.TCPServer(("127.0.0.1", self.port), handler_class) as httpd:
                print(f"✅ Server started successfully!")
                print(f"🎯 DEMO STATUS: Ready for October 15th presentation")
                print(f"⏰ Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print()
                print("Press Ctrl+C to stop the server...")
                print()
                
                # Auto-open browser
                if auto_open:
                    dashboard_url = f"http://localhost:{self.port}/{self.dashboard_file}"
                    print("🌐 Opening dashboard in default browser...")
                    try:
                        webbrowser.open(dashboard_url)
                    except:
                        print(f"   Manual access: {dashboard_url}")
                    print()
                
                # Server loop
                try:
                    httpd.serve_forever()
                except KeyboardInterrupt:
                    print("\n🛑 Clinical Demo Server stopped.")
                    print("Thank you for using L.I.F.E. Platform!")
                    return True
                    
        except Exception as e:
            print(f"❌ Server error: {e}")
            print()
            print("💡 TROUBLESHOOTING:")
            print("• Check if another program is using the port")
            print("• Ensure dashboard file exists in current directory")
            print("• Try running as administrator/sudo if needed")
            input("Press Enter to exit...")
            return False
            
    def run_demo(self):
        """Main demo execution"""
        self.print_header()
        
        if not self.check_dashboard_file():
            return False
            
        self.check_templates()
        print()
        
        print("🎯 READY TO LAUNCH CLINICAL DEMO!")
        print()
        
        launch = input("Press Enter to start demo server, or 'q' to quit: ").strip().lower()
        if launch == 'q':
            print("Demo cancelled by user.")
            return False
            
        return self.start_server()

def main():
    """Main entry point"""
    try:
        # Check command line arguments
        port = 8080
        dashboard_file = "LIFE_CLINICAL_GRADE_DASHBOARD.html"
        
        if len(sys.argv) > 1:
            try:
                port = int(sys.argv[1])
            except ValueError:
                print(f"Invalid port number: {sys.argv[1]}")
                sys.exit(1)
                
        if len(sys.argv) > 2:
            dashboard_file = sys.argv[2]
            
        # Create and run server
        server = LIFEDemoServer(port=port, dashboard_file=dashboard_file)
        success = server.run_demo()
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\nDemo cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()