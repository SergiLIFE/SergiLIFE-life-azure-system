#!/usr/bin/env python3
"""
L.I.F.E. Platform - Session Launcher
Automated launcher for three demo sessions on October 15, 2025
"""

import os
import sys
import webbrowser
import subprocess
import time
import logging
from datetime import datetime

# Setup logging
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(SCRIPT_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOGS_DIR, "session_launcher.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

class SessionLauncher:
    """
    Launch and manage the three demo sessions
    """
    
    def __init__(self):
        self.base_url = "http://localhost:8080"
        self.demo_file = "LIFE_PLATFORM_DEMO_WEBSITE.html"
        self.server_process = None
        
        self.sessions = {
            "1": {
                "name": "Clinical Professionals",
                "time": "09:00 - 09:45 BST",
                "url_section": "eeg-processing",
                "participants": 17,
                "focus": "Clinical workflow and patient care optimization",
                "tier": "Professional ($75,000/year)"
            },
            "2": {
                "name": "Research & IT Leadership", 
                "time": "11:00 - 11:45 BST",
                "url_section": "research-tools",
                "participants": 6,
                "focus": "Enterprise capabilities and research innovation",
                "tier": "Enterprise ($250,000/year)"
            },
            "3": {
                "name": "Executive & Strategic Overview",
                "time": "14:00 - 14:30 BST", 
                "url_section": "roi-calculator",
                "participants": 23,
                "focus": "Strategic value, ROI, and implementation planning",
                "tier": "Both tiers with custom options"
            }
        }
    
    def start_demo_server(self):
        """
        Start the demo website server
        """
        try:
            logging.info("Starting demo server...")
            
            # Check if demo file exists
            demo_path = os.path.join(SCRIPT_DIR, self.demo_file)
            if not os.path.exists(demo_path):
                logging.error(f"Demo file not found: {demo_path}")
                return False
            
            # Start Python HTTP server
            import http.server
            import socketserver
            import threading
            
            class Handler(http.server.SimpleHTTPRequestHandler):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, directory=SCRIPT_DIR, **kwargs)
            
            # Try port 8080, fallback to 8081
            ports_to_try = [8080, 8081, 8082]
            server_started = False
            
            for port in ports_to_try:
                try:
                    httpd = socketserver.TCPServer(("", port), Handler)
                    self.base_url = f"http://localhost:{port}"
                    
                    # Start server in background thread
                    server_thread = threading.Thread(target=httpd.serve_forever)
                    server_thread.daemon = True
                    server_thread.start()
                    
                    logging.info(f"Demo server started on {self.base_url}")
                    print(f"🌐 Demo server running: {self.base_url}")
                    server_started = True
                    break
                    
                except OSError as e:
                    if "Address already in use" in str(e):
                        logging.warning(f"Port {port} already in use, trying next port...")
                        continue
                    else:
                        raise e
            
            if not server_started:
                logging.error("Could not start server on any available port")
                return False
            
            # Give server time to start
            time.sleep(2)
            return True
            
        except Exception as e:
            logging.error(f"Failed to start demo server: {e}")
            return False
    
    def launch_session(self, session_number: str):
        """
        Launch a specific demo session
        """
        try:
            if session_number not in self.sessions:
                print(f"❌ Invalid session number: {session_number}")
                return False
            
            session = self.sessions[session_number]
            session_url = f"{self.base_url}/{self.demo_file}#{session['url_section']}"
            
            print(f"\n🎯 LAUNCHING SESSION {session_number}")
            print("=" * 60)
            print(f"📋 Session: {session['name']}")
            print(f"⏰ Time: {session['time']}")
            print(f"👥 Participants: {session['participants']}")
            print(f"🎯 Focus: {session['focus']}")
            print(f"💰 Tier: {session['tier']}")
            print(f"🔗 URL: {session_url}")
            print("=" * 60)
            
            # Open session in browser
            print("🌐 Opening session in browser...")
            webbrowser.open(session_url)
            
            logging.info(f"Launched Session {session_number}: {session['name']}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to launch session {session_number}: {e}")
            return False
    
    def show_session_menu(self):
        """
        Display session selection menu
        """
        print("\n🎭 L.I.F.E. PLATFORM - DEMO SESSION LAUNCHER")
        print("October 15, 2025 | Three Specialized Sessions")
        print("=" * 70)
        
        for num, session in self.sessions.items():
            print(f"\n{num}. {session['name']}")
            print(f"   ⏰ {session['time']}")
            print(f"   👥 {session['participants']} participants")
            print(f"   🎯 {session['focus']}")
            print(f"   💰 {session['tier']}")
        
        print("\n" + "=" * 70)
        print("Additional Options:")
        print("s - Start demo server only")
        print("a - Launch all sessions (opens 3 browser tabs)")
        print("q - Quit")
        print("=" * 70)
    
    def launch_all_sessions(self):
        """
        Launch all three sessions (opens multiple browser tabs)
        """
        try:
            print("\n🚀 LAUNCHING ALL THREE SESSIONS")
            print("This will open 3 browser tabs...")
            
            for session_num in ["1", "2", "3"]:
                session = self.sessions[session_num]
                session_url = f"{self.base_url}/{self.demo_file}#{session['url_section']}"
                
                print(f"🌐 Opening Session {session_num}: {session['name']}")
                webbrowser.open_new_tab(session_url)
                time.sleep(1)  # Brief delay between tabs
            
            print("✅ All sessions launched!")
            logging.info("Launched all three demo sessions")
            return True
            
        except Exception as e:
            logging.error(f"Failed to launch all sessions: {e}")
            return False
    
    def check_demo_file(self):
        """
        Check if demo website file exists and is ready
        """
        try:
            demo_path = os.path.join(SCRIPT_DIR, self.demo_file)
            
            if not os.path.exists(demo_path):
                print(f"❌ Demo file not found: {self.demo_file}")
                print("   Please ensure LIFE_PLATFORM_DEMO_WEBSITE.html is in the current directory")
                return False
            
            # Check file size (should be substantial)
            file_size = os.path.getsize(demo_path)
            if file_size < 10000:  # Less than 10KB probably means empty/incomplete
                print(f"⚠️ Demo file seems small ({file_size} bytes)")
                print("   Please verify the demo website is complete")
                return False
            
            print(f"✅ Demo file ready: {self.demo_file} ({file_size:,} bytes)")
            return True
            
        except Exception as e:
            logging.error(f"Failed to check demo file: {e}")
            return False
    
    def run_interactive_launcher(self):
        """
        Run interactive session launcher
        """
        try:
            # Check demo file first
            if not self.check_demo_file():
                return False
            
            # Start server automatically
            if not self.start_demo_server():
                print("❌ Could not start demo server")
                return False
            
            while True:
                self.show_session_menu()
                
                choice = input("\nSelect session to launch (1-3, s, a, q): ").strip().lower()
                
                if choice == 'q':
                    print("👋 Goodbye! Demo server will continue running...")
                    break
                elif choice == 's':
                    print(f"✅ Demo server is running: {self.base_url}")
                    print("You can now manually navigate to session URLs")
                elif choice == 'a':
                    self.launch_all_sessions()
                elif choice in ['1', '2', '3']:
                    self.launch_session(choice)
                else:
                    print("❌ Invalid selection. Please choose 1-3, s, a, or q")
                
                input("\nPress Enter to continue...")
            
            return True
            
        except KeyboardInterrupt:
            print("\n\n👋 Launcher interrupted. Demo server will continue running...")
            return True
        except Exception as e:
            logging.error(f"Interactive launcher failed: {e}")
            return False

def main():
    """
    Main execution function
    """
    try:
        launcher = SessionLauncher()
        
        # Check for command line arguments
        if len(sys.argv) > 1:
            session_arg = sys.argv[1].strip()
            
            if session_arg in ['1', '2', '3']:
                # Direct session launch
                print("L.I.F.E. Platform Session Launcher")
                print("-" * 40)
                
                if launcher.check_demo_file() and launcher.start_demo_server():
                    launcher.launch_session(session_arg)
                else:
                    print("❌ Could not start session")
                return
            
            elif session_arg.lower() == 'all':
                # Launch all sessions
                if launcher.check_demo_file() and launcher.start_demo_server():
                    launcher.launch_all_sessions()
                else:
                    print("❌ Could not start sessions")
                return
        
        # Interactive mode
        launcher.run_interactive_launcher()
        
    except Exception as e:
        logging.error(f"Main execution failed: {e}")
        print(f"❌ Launcher error: {e}")

if __name__ == "__main__":
    main()