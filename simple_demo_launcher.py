#!/usr/bin/env python3
"""
Simple Demo Website Launcher
Quick deployment for L.I.F.E. Platform October 15, 2025 demo
"""

import os
import sys
import webbrowser
import http.server
import socketserver
import threading
from pathlib import Path

def launch_demo():
    """Launch the L.I.F.E. Platform demo website"""
    print("🚀 L.I.F.E. Platform Demo Launcher")
    print("=" * 40)
    
    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    demo_file = "LIFE_PLATFORM_DEMO_WEBSITE.html"
    demo_path = os.path.join(script_dir, demo_file)
    
    # Check if demo file exists
    if not os.path.exists(demo_path):
        print(f"❌ Demo file not found: {demo_file}")
        return False
    
    print(f"✅ Demo file found: {demo_file}")
    print(f"📁 Location: {script_dir}")
    
    # Try to start simple HTTP server
    port = 8080
    try:
        print(f"🌐 Starting server on port {port}...")
        
        # Change to script directory
        os.chdir(script_dir)
        
        # Create handler
        handler = http.server.SimpleHTTPRequestHandler
        
        # Create server
        with socketserver.TCPServer(("", port), handler) as httpd:
            demo_url = f"http://localhost:{port}/{demo_file}"
            
            print(f"✅ Server started successfully!")
            print(f"🔗 Demo URL: {demo_url}")
            print("📱 Opening in browser...")
            
            # Open in browser
            webbrowser.open(demo_url)
            
            print("\n🎯 DEMO READY FOR OCTOBER 15, 2025!")
            print("   - Real-time EEG processing simulation")
            print("   - Interactive clinical workflow")
            print("   - ROI calculator for healthcare orgs")
            print("   - Research tools demonstration")
            print("\n⚠️  Press Ctrl+C to stop the demo server")
            
            # Keep server running
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n🛑 Demo server stopped")
                return True
    
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"⚠️  Port {port} is already in use")
            # Try direct file opening
            print("🔄 Opening demo file directly...")
            webbrowser.open(f"file://{demo_path}")
            return True
        else:
            print(f"❌ Server error: {e}")
            return False
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = launch_demo()
    if not success:
        print("\n❌ Demo launch failed")
        sys.exit(1)
    else:
        print("\n✅ Demo launched successfully")