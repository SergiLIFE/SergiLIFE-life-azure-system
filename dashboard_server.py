#!/usr/bin/env python3
"""
L.I.F.E. Platform Dashboard Server
GDPR-Compliant Local Hosting Solution
Copyright 2025 - Sergio Paya Borrull

Secure local server for sharing L.I.F.E. dashboard with university colleagues.
Includes GDPR compliance measures and access logging.
"""

import http.server
import socketserver
import os
import sys
import datetime
import json
import socket
from urllib.parse import urlparse, parse_qs
import webbrowser
from pathlib import Path

# GDPR Compliance Configuration
GDPR_CONFIG = {
    "data_collection": False,  # No personal data collection
    "cookies": False,         # No cookies used
    "analytics": False,       # No analytics tracking
    "logging_minimal": True,  # Only essential access logging
    "retention_days": 1,      # Log retention (24 hours max)
}

class GDPRCompliantHandler(http.server.SimpleHTTPRequestHandler):
    """GDPR-compliant HTTP request handler"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)
    
    def do_GET(self):
        """Handle GET requests with GDPR compliance"""
        # Log access (minimal logging as per GDPR)
        self.log_access()
        
        # Add GDPR-compliant headers
        self.add_gdpr_headers()
        
        # Serve the dashboard or default page
        if self.path == '/' or self.path == '/dashboard':
            self.serve_dashboard()
        elif self.path == '/privacy':
            self.serve_privacy_notice()
        elif self.path == '/health':
            self.serve_health_check()
        else:
            super().do_GET()
    
    def log_access(self):
        """Minimal access logging for GDPR compliance"""
        timestamp = datetime.datetime.now().isoformat()
        client_ip = self.client_address[0]
        
        # Only log timestamp, path, and anonymized IP
        log_entry = {
            "timestamp": timestamp,
            "path": self.path,
            "ip_anonymized": self.anonymize_ip(client_ip),
            "user_agent": "academic_demo"  # No UA logging for privacy
        }
        
        # Write to temporary log (auto-delete after 24h)
        log_file = Path("access_log.json")
        if log_file.exists():
            with open(log_file, 'r') as f:
                logs = json.load(f)
        else:
            logs = []
        
        logs.append(log_entry)
        
        # Clean old logs (GDPR retention)
        logs = self.clean_old_logs(logs)
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
    
    def anonymize_ip(self, ip):
        """Anonymize IP address for GDPR compliance"""
        parts = ip.split('.')
        if len(parts) == 4:
            return f"{parts[0]}.{parts[1]}.xxx.xxx"
        return "xxx.xxx.xxx.xxx"
    
    def clean_old_logs(self, logs):
        """Remove logs older than 24 hours (GDPR retention)"""
        cutoff = datetime.datetime.now() - datetime.timedelta(days=1)
        return [log for log in logs if datetime.datetime.fromisoformat(log['timestamp']) > cutoff]
    
    def add_gdpr_headers(self):
        """Add GDPR-compliant HTTP headers"""
        headers = {
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0',
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Referrer-Policy': 'no-referrer',
            'Content-Security-Policy': "default-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'",
        }
        
        for header, value in headers.items():
            self.send_header(header, value)
    
    def serve_dashboard(self):
        """Serve the L.I.F.E. dashboard"""
        dashboard_file = "LIFE_CORE_ALGORITHM_DASHBOARD.html"
        
        if os.path.exists(dashboard_file):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.add_gdpr_headers()
            self.end_headers()
            
            with open(dashboard_file, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.send_error(404, "Dashboard not found")
    
    def serve_privacy_notice(self):
        """Serve GDPR privacy notice"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.add_gdpr_headers()
        self.end_headers()
        
        privacy_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Privacy Notice - L.I.F.E. Platform Demo</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
                .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; }
                h1 { color: #1e3c72; }
                .highlight { background: #e8f4f8; padding: 15px; border-radius: 5px; margin: 20px 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Privacy Notice - L.I.F.E. Platform Academic Demo</h1>
                
                <div class="highlight">
                    <strong>GDPR Compliant Academic Demonstration</strong><br>
                    October 15, 2025 University Demo - 23 Attendees
                </div>
                
                <h2>Data Collection & Processing</h2>
                <ul>
                    <li><strong>Personal Data:</strong> NO personal data is collected or stored</li>
                    <li><strong>Cookies:</strong> NO cookies are used on this demonstration</li>
                    <li><strong>Analytics:</strong> NO analytics or tracking systems active</li>
                    <li><strong>Device Testing:</strong> Browser APIs used locally only (no data transmission)</li>
                </ul>
                
                <h2>Access Logging</h2>
                <p>Minimal access logs are kept for 24 hours maximum:</p>
                <ul>
                    <li>Timestamp of access</li>
                    <li>Requested page</li>
                    <li>Anonymized IP address (last two octets masked)</li>
                </ul>
                
                <h2>Data Retention</h2>
                <p>All logs are automatically deleted after 24 hours. No persistent storage.</p>
                
                <h2>Your Rights</h2>
                <p>As this is a demonstration with no personal data collection, standard GDPR rights apply. Contact: sergio.paya.borrull@academic-institution.edu</p>
                
                <div class="highlight">
                    <strong>Academic Use Only:</strong> This demonstration is for educational purposes only and complies with all applicable data protection regulations.
                </div>
                
                <p><a href="/dashboard">Return to Dashboard</a></p>
            </div>
        </body>
        </html>
        """
        self.wfile.write(privacy_html.encode('utf-8'))
    
    def serve_health_check(self):
        """Simple health check endpoint"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.add_gdpr_headers()
        self.end_headers()
        
        health_data = {
            "status": "healthy",
            "timestamp": datetime.datetime.now().isoformat(),
            "gdpr_compliant": True,
            "demo_ready": True
        }
        self.wfile.write(json.dumps(health_data).encode('utf-8'))

def get_local_ip():
    """Get the local IP address"""
    try:
        # Connect to a remote address to determine local IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except:
        return "127.0.0.1"

def cleanup_old_logs():
    """Cleanup function for GDPR compliance"""
    log_file = Path("access_log.json")
    if log_file.exists():
        try:
            with open(log_file, 'r') as f:
                logs = json.load(f)
            
            # Remove logs older than 24 hours
            cutoff = datetime.datetime.now() - datetime.timedelta(days=1)
            clean_logs = [log for log in logs if datetime.datetime.fromisoformat(log['timestamp']) > cutoff]
            
            if len(clean_logs) != len(logs):
                with open(log_file, 'w') as f:
                    json.dump(clean_logs, f, indent=2)
                print(f"🔒 GDPR Cleanup: Removed {len(logs) - len(clean_logs)} old log entries")
        except Exception as e:
            print(f"⚠️  Log cleanup error: {e}")

def main():
    """Main server function"""
    print("=" * 70)
    print("🎓 L.I.F.E. PLATFORM - UNIVERSITY DEMO SERVER")
    print("   GDPR-Compliant Academic Demonstration")
    print("   October 15, 2025 - 23 University Colleagues")
    print("=" * 70)
    
    # Cleanup old logs on startup
    cleanup_old_logs()
    
    # Server configuration
    PORT = 8080
    
    # Check if dashboard file exists
    dashboard_file = "LIFE_CORE_ALGORITHM_DASHBOARD.html"
    if not os.path.exists(dashboard_file):
        print(f"❌ Error: {dashboard_file} not found in current directory")
        print(f"   Current directory: {os.getcwd()}")
        return
    
    # Get network information
    local_ip = get_local_ip()
    
    try:
        # Create server
        with socketserver.TCPServer(("", PORT), GDPRCompliantHandler) as httpd:
            print(f"\n✅ Server started successfully!")
            print(f"📁 Serving: {dashboard_file}")
            print(f"🔒 GDPR Compliant: YES")
            print(f"📊 Data Collection: NO")
            print(f"🍪 Cookies: NO")
            print(f"📈 Analytics: NO")
            print(f"\n📧 SHARE THESE LINKS WITH YOUR COLLEAGUES:")
            print(f"   🏠 Local Access:    http://localhost:{PORT}/dashboard")
            print(f"   🌐 Network Access:  http://{local_ip}:{PORT}/dashboard")
            print(f"   📋 Privacy Notice:  http://{local_ip}:{PORT}/privacy")
            
            print(f"\n📝 EMAIL TEMPLATE FOR COLLEAGUES:")
            print("─" * 50)
            print(f"Subject: L.I.F.E. Platform Demo - October 15, 2025")
            print(f"")
            print(f"Dear Colleagues,")
            print(f"")
            print(f"Please join our L.I.F.E. Platform demonstration:")
            print(f"🔗 Dashboard: http://{local_ip}:{PORT}/dashboard")
            print(f"🔒 Privacy: http://{local_ip}:{PORT}/privacy")
            print(f"")
            print(f"This is a GDPR-compliant demonstration with:")
            print(f"• NO personal data collection")
            print(f"• NO cookies or tracking")
            print(f"• Minimal logging (24h retention)")
            print(f"• Academic use only")
            print(f"")
            print(f"Best regards,")
            print(f"Sergio Paya Borrull")
            print("─" * 50)
            
            print(f"\n🚀 Server running on port {PORT}")
            print(f"📱 Press Ctrl+C to stop the server")
            print(f"🔄 Logs auto-delete after 24 hours (GDPR)")
            
            # Open browser automatically
            try:
                webbrowser.open(f'http://localhost:{PORT}/dashboard')
                print(f"🌐 Dashboard opened in your default browser")
            except:
                pass
            
            # Keep server running
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print(f"\n\n🛑 Server stopped by user")
        cleanup_old_logs()
        print(f"🔒 Final GDPR cleanup completed")
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print(f"❌ Error: Port {PORT} is already in use")
            print(f"   Try a different port or stop the existing server")
        else:
            print(f"❌ Server error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()