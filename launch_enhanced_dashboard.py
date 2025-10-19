"""
🧠 Enhanced L.I.F.E Platform Dashboard Launcher
Launch the enhanced tabbed dashboard with External EEG Ingestion
"""

import webbrowser
from pathlib import Path


def launch_enhanced_dashboard():
    """Launch the enhanced L.I.F.E Platform dashboard"""
    
    # Get the current directory
    current_dir = Path(__file__).parent
    dashboard_file = current_dir / "life_enhanced_dashboard.html"
    
    print("🧠 Launching Enhanced L.I.F.E Platform Dashboard...")
    print(f"📂 Dashboard location: {dashboard_file}")
    
    if dashboard_file.exists():
        # Try to open the file directly first
        try:
            file_url = f"file:///{dashboard_file.as_posix()}"
            print(f"🌐 Opening dashboard: {file_url}")
            webbrowser.open(file_url)
            
            print("\n✅ Enhanced Dashboard Features:")
            print("   🎯 Tabbed Interface Navigation")
            print("   📊 External EEG Ingestion Tab")
            print("   🧠 Neural Processing Metrics")
            print("   📈 Real-time Learning Analytics")
            print("   🔍 System Monitoring")
            
            print("\n🎉 Enhanced dashboard launched successfully!")
            print("🔗 Click the 'Ingest EEG Data' tab to access the new functionality")
            
            return True
            
        except Exception as e:
            print(f"❌ Error launching dashboard: {e}")
            return False
    else:
        print(f"❌ Dashboard file not found: {dashboard_file}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🧠 L.I.F.E Platform - Enhanced Dashboard Launcher")
    print("=" * 60)
    
    success = launch_enhanced_dashboard()
    
    if success:
        print("\n" + "=" * 60)
        print("✅ Launch completed! Check your browser.")
        print("📋 Features available:")
        print("   • Dashboard overview with live metrics")
        print("   • Neural processing real-time data")
        print("   • Learning analytics and efficiency")
        print("   • External EEG data ingestion")
        print("   • System monitoring and health")
        print("=" * 60)
    else:
        print("\n❌ Launch failed. Please check the files and try again.")        print("\n❌ Launch failed. Please check the files and try again.")