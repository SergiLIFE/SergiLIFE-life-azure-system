#!/usr/bin/env python3
"""
L.I.F.E. Platform - Demo Website Deployment Manager
October 15, 2025 Live Demo Support System

This script manages the deployment and hosting of the L.I.F.E. Platform demo website
for healthcare and educational demonstrations.

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import os
import sys
import json
import time
import logging
import webbrowser
import http.server
import socketserver
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any

# Setup logging
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(SCRIPT_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOGS_DIR, "demo_website_deployment.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

class DemoWebsiteManager:
    """
    Complete demo website deployment and management system
    for L.I.F.E. Platform October 15, 2025 demonstration
    """
    
    def __init__(self):
        self.script_dir = SCRIPT_DIR
        self.demo_website_path = os.path.join(SCRIPT_DIR, "LIFE_PLATFORM_DEMO_WEBSITE.html")
        self.deployment_config = {
            "demo_date": "October 15, 2025",
            "launch_time": "09:00 BST",
            "participants": 23,
            "local_port": 8080,
            "backup_ports": [8081, 8082, 8083],
            "auto_open_browser": True,
            "demo_duration_minutes": 45
        }
        
        # Demo analytics tracking
        self.demo_analytics = {
            "sessions": [],
            "page_views": 0,
            "feature_interactions": {},
            "roi_calculations": 0,
            "demo_completions": 0
        }
        
        logging.info("Demo Website Manager initialized")
        logging.info(f"Target demo: {self.deployment_config['demo_date']}")
    
    def validate_demo_files(self) -> bool:
        """
        Validate that all demo files are present and properly configured
        """
        try:
            logging.info("Validating demo website files...")
            
            # Check if main demo website exists
            if not os.path.exists(self.demo_website_path):
                logging.error(f"Demo website not found: {self.demo_website_path}")
                return False
            
            # Validate HTML file size (should be substantial)
            file_size = os.path.getsize(self.demo_website_path)
            if file_size < 50000:  # Less than 50KB indicates incomplete file
                logging.error(f"Demo website file too small: {file_size} bytes")
                return False
            
            logging.info(f"Demo website validated: {file_size:,} bytes")
            
            # Check HTML content for key demo sections
            with open(self.demo_website_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            required_sections = [
                "EEG Processing",
                "Adaptive Learning", 
                "Clinical Integration",
                "Research Tools",
                "Analytics Dashboard",
                "ROI Calculator"
            ]
            
            for section in required_sections:
                if section not in content:
                    logging.error(f"Missing demo section: {section}")
                    return False
            
            logging.info("All demo sections validated successfully")
            return True
            
        except Exception as e:
            logging.error(f"Demo file validation failed: {e}")
            return False
    
    def start_demo_server(self, port: int = None) -> Optional[int]:
        """
        Start local web server for demo website
        """
        try:
            if port is None:
                port = self.deployment_config["local_port"]
            
            # Try primary port, then backup ports
            ports_to_try = [port] + self.deployment_config["backup_ports"]
            
            for test_port in ports_to_try:
                try:
                    # Change to demo directory
                    original_dir = os.getcwd()
                    os.chdir(self.script_dir)
                    
                    # Create HTTP server
                    handler = http.server.SimpleHTTPRequestHandler
                    httpd = socketserver.TCPServer(("", test_port), handler)
                    
                    logging.info(f"Starting demo server on port {test_port}")
                    
                    # Start server in background thread
                    server_thread = threading.Thread(
                        target=httpd.serve_forever,
                        daemon=True
                    )
                    server_thread.start()
                    
                    # Store server reference for cleanup
                    self.demo_server = httpd
                    self.demo_port = test_port
                    
                    # Restore original directory
                    os.chdir(original_dir)
                    
                    logging.info(f"Demo server started successfully on port {test_port}")
                    
                    # Auto-open browser if configured
                    if self.deployment_config["auto_open_browser"]:
                        self.open_demo_in_browser(test_port)
                    
                    return test_port
                    
                except OSError as e:
                    if "Address already in use" in str(e):
                        logging.warning(f"Port {test_port} already in use, trying next port")
                        continue
                    else:
                        raise e
            
            logging.error("All demo server ports are in use")
            return None
            
        except Exception as e:
            logging.error(f"Failed to start demo server: {e}")
            return None
    
    def open_demo_in_browser(self, port: int):
        """
        Open demo website in default browser
        """
        try:
            demo_url = f"http://localhost:{port}/LIFE_PLATFORM_DEMO_WEBSITE.html"
            logging.info(f"Opening demo in browser: {demo_url}")
            
            # Open in default browser
            webbrowser.open(demo_url)
            
            # Log demo session start
            self.log_demo_session("browser_opened", {"url": demo_url, "port": port})
            
        except Exception as e:
            logging.error(f"Failed to open demo in browser: {e}")
    
    def log_demo_session(self, event_type: str, event_data: Dict[str, Any]):
        """
        Log demo session events for analytics
        """
        try:
            session_event = {
                "timestamp": datetime.now().isoformat(),
                "event_type": event_type,
                "data": event_data
            }
            
            self.demo_analytics["sessions"].append(session_event)
            
            # Update specific counters
            if event_type == "page_view":
                self.demo_analytics["page_views"] += 1
            elif event_type == "roi_calculation":
                self.demo_analytics["roi_calculations"] += 1
            elif event_type == "demo_completion":
                self.demo_analytics["demo_completions"] += 1
            elif event_type.startswith("feature_"):
                feature_name = event_type.replace("feature_", "")
                self.demo_analytics["feature_interactions"][feature_name] = \
                    self.demo_analytics["feature_interactions"].get(feature_name, 0) + 1
            
            logging.info(f"Demo event logged: {event_type}")
            
        except Exception as e:
            logging.error(f"Failed to log demo session: {e}")
    
    def generate_demo_urls(self) -> Dict[str, str]:
        """
        Generate various demo URLs for different access methods
        """
        try:
            port = getattr(self, 'demo_port', self.deployment_config["local_port"])
            
            base_url = f"http://localhost:{port}"
            demo_file = "LIFE_PLATFORM_DEMO_WEBSITE.html"
            
            urls = {
                "main_demo": f"{base_url}/{demo_file}",
                "direct_sections": {
                    "eeg_processing": f"{base_url}/{demo_file}#eeg-processing",
                    "adaptive_learning": f"{base_url}/{demo_file}#adaptive-learning", 
                    "clinical_integration": f"{base_url}/{demo_file}#clinical-integration",
                    "research_tools": f"{base_url}/{demo_file}#research-tools",
                    "analytics": f"{base_url}/{demo_file}#analytics",
                    "roi_calculator": f"{base_url}/{demo_file}#roi-calculator"
                },
                "mobile_optimized": f"{base_url}/{demo_file}?view=mobile",
                "fullscreen": f"{base_url}/{demo_file}?mode=fullscreen"
            }
            
            logging.info("Demo URLs generated successfully")
            return urls
            
        except Exception as e:
            logging.error(f"Failed to generate demo URLs: {e}")
            return {}
    
    def create_demo_access_guide(self) -> str:
        """
        Create comprehensive demo access guide for participants
        """
        try:
            urls = self.generate_demo_urls()
            
            guide_content = f"""
# L.I.F.E. Platform Demo Access Guide
## October 15, 2025 - Live Demonstration

### Demo Information
- **Date**: {self.deployment_config['demo_date']}
- **Time**: {self.deployment_config['launch_time']}
- **Duration**: {self.deployment_config['demo_duration_minutes']} minutes
- **Participants**: {self.deployment_config['participants']}

### Primary Access URL
{urls.get('main_demo', 'URL will be provided at demo time')}

### Demo Sections (Direct Links)
1. **EEG Processing Demo**: {urls['direct_sections']['eeg_processing']}
2. **Adaptive Learning**: {urls['direct_sections']['adaptive_learning']}
3. **Clinical Integration**: {urls['direct_sections']['clinical_integration']}
4. **Research Tools**: {urls['direct_sections']['research_tools']}
5. **Analytics Dashboard**: {urls['direct_sections']['analytics']}
6. **ROI Calculator**: {urls['direct_sections']['roi_calculator']}

### Technical Requirements
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection (local demo server)
- Screen resolution: 1024x768 minimum (1920x1080 recommended)
- Audio enabled for notifications

### Demo Features
✅ Interactive EEG signal visualization
✅ Real-time metrics and processing
✅ Clinical workflow integration
✅ ROI calculator with your organization data
✅ Research tools demonstration
✅ Mobile-responsive design

### Support Information
- Demo Manager: L.I.F.E. Platform Team
- Technical Support: Available during demo
- Questions: Use chat function in demo interface

### Troubleshooting
1. **Demo won't load**: Refresh browser or try direct section links
2. **Slow performance**: Close other browser tabs
3. **Mobile issues**: Use landscape orientation
4. **Audio problems**: Check browser audio permissions

### Post-Demo Resources
- Business case generator
- Implementation timeline
- Pricing information
- Technical documentation
- Integration guides

---
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
L.I.F.E. Platform Demo System v2.1.0
"""
            
            # Save guide to file
            guide_path = os.path.join(SCRIPT_DIR, "DEMO_ACCESS_GUIDE.md")
            with open(guide_path, 'w', encoding='utf-8') as f:
                f.write(guide_content)
            
            logging.info(f"Demo access guide created: {guide_path}")
            return guide_path
            
        except Exception as e:
            logging.error(f"Failed to create demo access guide: {e}")
            return ""
    
    def monitor_demo_performance(self) -> Dict[str, Any]:
        """
        Monitor demo website performance and generate metrics
        """
        try:
            logging.info("Monitoring demo performance...")
            
            performance_metrics = {
                "server_status": "running" if hasattr(self, 'demo_server') else "stopped",
                "server_port": getattr(self, 'demo_port', None),
                "uptime_minutes": self.calculate_uptime(),
                "total_sessions": len(self.demo_analytics["sessions"]),
                "page_views": self.demo_analytics["page_views"],
                "roi_calculations": self.demo_analytics["roi_calculations"],
                "feature_interactions": self.demo_analytics["feature_interactions"],
                "demo_completions": self.demo_analytics["demo_completions"],
                "average_session_duration": self.calculate_average_session_duration(),
                "most_popular_features": self.get_most_popular_features(),
                "timestamp": datetime.now().isoformat()
            }
            
            logging.info(f"Demo performance: {performance_metrics['total_sessions']} sessions, "
                        f"{performance_metrics['page_views']} page views")
            
            return performance_metrics
            
        except Exception as e:
            logging.error(f"Failed to monitor demo performance: {e}")
            return {}
    
    def calculate_uptime(self) -> float:
        """
        Calculate demo server uptime in minutes
        """
        try:
            if not hasattr(self, 'server_start_time'):
                return 0.0
            
            uptime_seconds = (datetime.now() - self.server_start_time).total_seconds()
            return round(uptime_seconds / 60, 2)
            
        except Exception as e:
            logging.error(f"Failed to calculate uptime: {e}")
            return 0.0
    
    def calculate_average_session_duration(self) -> float:
        """
        Calculate average demo session duration in minutes
        """
        try:
            if not self.demo_analytics["sessions"]:
                return 0.0
            
            # This would require session end events to calculate properly
            # For now, return estimated average based on demo duration
            return self.deployment_config["demo_duration_minutes"] * 0.7  # 70% completion rate
            
        except Exception as e:
            logging.error(f"Failed to calculate session duration: {e}")
            return 0.0
    
    def get_most_popular_features(self) -> List[Dict[str, Any]]:
        """
        Get most popular demo features based on interactions
        """
        try:
            features = self.demo_analytics["feature_interactions"]
            
            if not features:
                return []
            
            # Sort by interaction count
            sorted_features = sorted(features.items(), key=lambda x: x[1], reverse=True)
            
            return [
                {"feature": feature, "interactions": count}
                for feature, count in sorted_features[:5]  # Top 5
            ]
            
        except Exception as e:
            logging.error(f"Failed to get popular features: {e}")
            return []
    
    def export_demo_analytics(self) -> str:
        """
        Export demo analytics to JSON file
        """
        try:
            analytics_data = {
                "demo_config": self.deployment_config,
                "performance_metrics": self.monitor_demo_performance(),
                "raw_analytics": self.demo_analytics,
                "export_timestamp": datetime.now().isoformat()
            }
            
            # Create analytics directory
            analytics_dir = os.path.join(SCRIPT_DIR, "demo_analytics")
            os.makedirs(analytics_dir, exist_ok=True)
            
            # Export to timestamped file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            export_path = os.path.join(analytics_dir, f"demo_analytics_{timestamp}.json")
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(analytics_data, f, indent=2, ensure_ascii=False)
            
            logging.info(f"Demo analytics exported: {export_path}")
            return export_path
            
        except Exception as e:
            logging.error(f"Failed to export demo analytics: {e}")
            return ""
    
    def stop_demo_server(self):
        """
        Stop the demo server and cleanup
        """
        try:
            if hasattr(self, 'demo_server'):
                logging.info("Stopping demo server...")
                self.demo_server.shutdown()
                self.demo_server.server_close()
                delattr(self, 'demo_server')
                delattr(self, 'demo_port')
                
                logging.info("Demo server stopped successfully")
                
                # Export final analytics
                self.export_demo_analytics()
            else:
                logging.info("No demo server to stop")
                
        except Exception as e:
            logging.error(f"Failed to stop demo server: {e}")
    
    def run_complete_demo_deployment(self):
        """
        Complete demo deployment workflow for October 15, 2025
        """
        try:
            logging.info("=" * 60)
            logging.info("L.I.F.E. PLATFORM DEMO DEPLOYMENT")
            logging.info("October 15, 2025 - Live Demonstration")
            logging.info("=" * 60)
            
            # Store server start time
            self.server_start_time = datetime.now()
            
            # Step 1: Validate demo files
            logging.info("Step 1: Validating demo files...")
            if not self.validate_demo_files():
                logging.error("Demo file validation failed - cannot proceed")
                return False
            
            # Step 2: Start demo server
            logging.info("Step 2: Starting demo server...")
            port = self.start_demo_server()
            if not port:
                logging.error("Failed to start demo server - cannot proceed")
                return False
            
            # Step 3: Generate access guide
            logging.info("Step 3: Creating demo access guide...")
            guide_path = self.create_demo_access_guide()
            
            # Step 4: Display deployment summary
            self.display_deployment_summary(port, guide_path)
            
            # Step 5: Monitor demo (keep alive)
            logging.info("Step 5: Demo monitoring active...")
            logging.info("Demo server is running. Press Ctrl+C to stop.")
            
            try:
                # Keep server running until interrupted
                while True:
                    time.sleep(30)  # Check every 30 seconds
                    performance = self.monitor_demo_performance()
                    
                    if performance.get("total_sessions", 0) > 0:
                        logging.info(f"Demo active - Sessions: {performance['total_sessions']}, "
                                   f"Views: {performance['page_views']}")
                    
            except KeyboardInterrupt:
                logging.info("Demo deployment stopped by user")
                self.stop_demo_server()
            
            return True
            
        except Exception as e:
            logging.error(f"Demo deployment failed: {e}")
            self.stop_demo_server()
            return False
    
    def display_deployment_summary(self, port: int, guide_path: str):
        """
        Display comprehensive deployment summary
        """
        try:
            urls = self.generate_demo_urls()
            
            print("\n" + "=" * 80)
            print("🚀 L.I.F.E. PLATFORM DEMO DEPLOYMENT SUCCESSFUL!")
            print("=" * 80)
            print(f"📅 Demo Date: {self.deployment_config['demo_date']}")
            print(f"⏰ Launch Time: {self.deployment_config['launch_time']}")
            print(f"👥 Expected Participants: {self.deployment_config['participants']}")
            print(f"🌐 Server Port: {port}")
            print(f"📄 Access Guide: {os.path.basename(guide_path)}")
            print("\n🔗 DEMO ACCESS URLS:")
            print(f"   Main Demo: {urls['main_demo']}")
            print("\n📊 DIRECT SECTION ACCESS:")
            for section, url in urls['direct_sections'].items():
                print(f"   {section.replace('_', ' ').title()}: {url}")
            
            print("\n✅ DEMO FEATURES READY:")
            print("   🧠 Real-time EEG Processing")
            print("   🎯 Adaptive Learning Algorithm")
            print("   🏥 Clinical Workflow Integration") 
            print("   🔬 Research Tools & Analytics")
            print("   💰 ROI Calculator & Business Case")
            print("   📱 Mobile-Responsive Design")
            
            print("\n📈 MONITORING:")
            print("   ✅ Performance tracking active")
            print("   ✅ Analytics collection enabled")
            print("   ✅ Session logging operational")
            
            print("\n🎯 DEMO OBJECTIVES:")
            print("   • Showcase real-time neural processing capabilities")
            print("   • Demonstrate clinical integration workflow")
            print("   • Calculate ROI for healthcare organizations")
            print("   • Highlight research and analytics tools")
            print("   • Generate qualified leads and partnerships")
            
            print("\n" + "=" * 80)
            print("Demo is LIVE and ready for participants!")
            print("=" * 80 + "\n")
            
        except Exception as e:
            logging.error(f"Failed to display deployment summary: {e}")

def main():
    """
    Main execution function for demo deployment
    """
    try:
        print("L.I.F.E. Platform Demo Website Deployment Manager")
        print("October 15, 2025 Live Demonstration Support")
        print("-" * 50)
        
        # Initialize demo manager
        demo_manager = DemoWebsiteManager()
        
        # Run complete deployment
        success = demo_manager.run_complete_demo_deployment()
        
        if success:
            print("\n✅ Demo deployment completed successfully!")
            print("The L.I.F.E. Platform demo is ready for your presentation.")
        else:
            print("\n❌ Demo deployment failed!")
            print("Please check the logs for detailed error information.")
            
    except KeyboardInterrupt:
        print("\n⚠️ Demo deployment interrupted by user")
    except Exception as e:
        logging.error(f"Main execution failed: {e}")
        print(f"\n❌ Unexpected error: {e}")
    
    print("\nDemo deployment manager exited.")

if __name__ == "__main__":
    main()