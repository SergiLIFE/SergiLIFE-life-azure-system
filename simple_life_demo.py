"""
L.I.F.E. Platform - Simple Demo Server for October 15, 2025
Works with any L.I.F.E. dashboard file
Teams-ready for 23 colleagues
"""

import http.server
import webbrowser
import os
from pathlib import Path

def find_dashboard():
    """Find any L.I.F.E. dashboard file"""
    print("🔍 Searching for L.I.F.E. dashboard files...")
    
    # Possible dashboard names
    dashboard_files = [
        "LIFE_CLINICAL_GRADE_DASHBOARD.html",
        "LIFE_AI_ENHANCED_PHYSIONET_DASHBOARD.html", 
        "L.I.F.E. Platform - Core Algorithm Dashboard.html",
        "life_dashboard.html"
    ]
    
    # Check current directory first
    for filename in dashboard_files:
        if os.path.exists(filename):
            print(f"   ✅ Found: {filename}")
            return filename
    
    # Check for any HTML file with L.I.F.E. in the name
    for html_file in Path(".").glob("*.html"):
        if "life" in html_file.name.lower() or "l.i.f.e" in html_file.name.lower():
            print(f"   ✅ Found L.I.F.E. file: {html_file.name}")
            return str(html_file)
    
    # Check for any HTML file
    html_files = list(Path(".").glob("*.html"))
    if html_files:
        largest = max(html_files, key=lambda x: x.stat().st_size)
        print(f"   📄 Using largest HTML file: {largest.name}")
        return str(largest)
    
    return None

def start_demo():
    """Start the L.I.F.E. demo server"""
    print("🧠 L.I.F.E. PLATFORM - SIMPLE DEMO SERVER 🚀")
    print("📅 October 15, 2025 University Teams Demo")
    print("👥 Ready for 23 colleagues!")
    print("=" * 50)
    
    dashboard = find_dashboard()
    
    if not dashboard:
        print("\n❌ No dashboard files found!")
        print("\n💡 SOLUTIONS:")
        print("1. Copy your dashboard HTML file to this directory")
        print("2. Rename it to 'life_dashboard.html'")
        print("3. Or run from the directory containing your dashboard")
        print("\n📂 Current directory files:")
        for file in Path(".").iterdir():
            if file.is_file():
                print(f"   • {file.name}")
        return
    
    print(f"\n🎯 Using dashboard: {dashboard}")
    print(f"📊 File size: {os.path.getsize(dashboard)/1024:.1f} KB")
    
    # Start simple HTTP server
    port = 8080
    print(f"\n🚀 Starting server on port {port}...")
    print(f"🔗 URL: http://localhost:{port}")
    print(f"📱 Teams sharing ready!")
    
    try:
        # Change to directory containing the dashboard
        os.chdir(os.path.dirname(os.path.abspath(dashboard)))
        
        # Start server
        server = http.server.HTTPServer(('localhost', port), http.server.SimpleHTTPRequestHandler)
        
        # Open browser
        dashboard_url = f"http://localhost:{port}/{os.path.basename(dashboard)}"
        print(f"\n🌐 Opening: {dashboard_url}")
        webbrowser.open(dashboard_url)
        
        print("\n✅ Demo server running!")
        print("📢 TEAMS INSTRUCTIONS:")
        print("1. Share your screen in Teams")  
        print("2. Show the browser with L.I.F.E. dashboard")
        print("3. Demo is ready for 23 colleagues!")
        print("\nPress Ctrl+C to stop...")
        
        server.serve_forever()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Demo completed!")
        print("🎉 Thank you for using L.I.F.E. Platform!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Try running: python -m http.server 8080")

if __name__ == "__main__":
    start_demo()