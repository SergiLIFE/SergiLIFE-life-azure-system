#!/usr/bin/env python3
"""
L.I.F.E. Platform Demo - Final Deployment Validation
October 10, 2025 - 5 Days Before Live Demo
"""

import os
import sys
import webbrowser
from pathlib import Path

def validate_demo_deployment():
    """
    Final validation check for October 15, 2025 demo deployment
    """
    print("🚀 L.I.F.E. Platform Demo - Final Deployment Validation")
    print("=" * 60)
    print("📅 Target Demo Date: October 15, 2025")
    print("👥 Expected Participants: 23 healthcare professionals")
    print("⏰ Demo Time: 09:00 BST (45 minutes)")
    print("=" * 60)
    
    # Check current directory and demo files
    current_dir = os.path.dirname(os.path.abspath(__file__))
    demo_file = "LIFE_PLATFORM_DEMO_WEBSITE.html"
    demo_path = os.path.join(current_dir, demo_file)
    
    print(f"\n📁 Working Directory: {current_dir}")
    
    # Validation checks
    validation_results = {}
    
    # 1. Check demo website exists
    if os.path.exists(demo_path):
        file_size = os.path.getsize(demo_path)
        validation_results["demo_website"] = {
            "status": "✅ PASS",
            "size": f"{file_size:,} bytes",
            "details": "Main demo website file found"
        }
    else:
        validation_results["demo_website"] = {
            "status": "❌ FAIL", 
            "size": "0 bytes",
            "details": "Demo website file missing!"
        }
    
    # 2. Check deployment managers exist
    managers = [
        "demo_website_deployment_manager.py",
        "simple_demo_launcher.py"
    ]
    
    for manager in managers:
        manager_path = os.path.join(current_dir, manager)
        if os.path.exists(manager_path):
            validation_results[manager] = {
                "status": "✅ PASS",
                "details": "Deployment script ready"
            }
        else:
            validation_results[manager] = {
                "status": "❌ FAIL",
                "details": "Deployment script missing!"
            }
    
    # 3. Check demo sections (sample HTML content)
    if os.path.exists(demo_path):
        try:
            with open(demo_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            required_sections = [
                "EEG Processing",
                "Adaptive Learning", 
                "Clinical Integration",
                "Research Tools",
                "Analytics Dashboard", 
                "ROI Calculator"
            ]
            
            missing_sections = []
            for section in required_sections:
                if section not in content:
                    missing_sections.append(section)
            
            if not missing_sections:
                validation_results["demo_sections"] = {
                    "status": "✅ PASS",
                    "details": f"All {len(required_sections)} demo sections found"
                }
            else:
                validation_results["demo_sections"] = {
                    "status": "⚠️ WARNING",
                    "details": f"Missing sections: {', '.join(missing_sections)}"
                }
                
        except Exception as e:
            validation_results["demo_sections"] = {
                "status": "❌ FAIL",
                "details": f"Could not validate sections: {e}"
            }
    
    # 4. Check interactive features
    if os.path.exists(demo_path):
        try:
            with open(demo_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            interactive_features = [
                "onclick=",  # Interactive buttons
                "onchange=", # Form controls
                "animation:", # CSS animations
                "function ", # JavaScript functions
                "eeg-wave",  # EEG animations
                "progress-fill" # Progress bars
            ]
            
            found_features = []
            for feature in interactive_features:
                if feature in content:
                    found_features.append(feature)
            
            validation_results["interactive_features"] = {
                "status": "✅ PASS" if len(found_features) >= 4 else "⚠️ WARNING",
                "details": f"{len(found_features)}/{len(interactive_features)} interactive features found"
            }
            
        except Exception as e:
            validation_results["interactive_features"] = {
                "status": "❌ FAIL", 
                "details": f"Could not check interactivity: {e}"
            }
    
    # Display validation results
    print("\n🔍 DEPLOYMENT VALIDATION RESULTS:")
    print("-" * 60)
    
    overall_status = "READY"
    for component, result in validation_results.items():
        print(f"{result['status']} {component}")
        print(f"   {result['details']}")
        if "size" in result:
            print(f"   File size: {result['size']}")
        
        if result['status'].startswith("❌"):
            overall_status = "NOT READY"
        elif result['status'].startswith("⚠️") and overall_status == "READY":
            overall_status = "READY WITH WARNINGS"
    
    print("\n" + "=" * 60)
    
    if overall_status == "READY":
        print("🎉 DEPLOYMENT STATUS: ✅ READY FOR OCTOBER 15, 2025 DEMO!")
        print("\n🚀 Quick Launch Commands:")
        print("   python simple_demo_launcher.py")
        print("   python demo_website_deployment_manager.py")
        print(f"\n🔗 Demo URL (when server running): http://localhost:8080/{demo_file}")
        
        # Offer to open demo now
        response = input("\n❓ Would you like to open the demo now? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            try:
                # Try to open directly in browser
                demo_url = f"file://{demo_path}"
                print(f"🌐 Opening demo: {demo_url}")
                webbrowser.open(demo_url)
                print("✅ Demo opened in your default browser!")
                print("\n📋 Demo Navigation:")
                print("   • Click tabs at top to switch between sections")
                print("   • Try the ROI Calculator with your organization data")
                print("   • Watch the EEG signal animations")
                print("   • Test interactive buttons and controls")
            except Exception as e:
                print(f"❌ Could not open demo: {e}")
                print("💡 Try running: python simple_demo_launcher.py")
        
    elif overall_status == "READY WITH WARNINGS":
        print("⚠️ DEPLOYMENT STATUS: READY WITH WARNINGS")
        print("Demo can proceed but some features may be limited.")
        
    else:
        print("❌ DEPLOYMENT STATUS: NOT READY")
        print("Critical issues must be resolved before demo.")
    
    print("\n" + "=" * 60)
    
    return overall_status == "READY"

def main():
    """
    Main function for deployment validation
    """
    try:
        is_ready = validate_demo_deployment()
        
        if is_ready:
            print("✅ L.I.F.E. Platform demo is ready for October 15, 2025!")
            print("🎯 All systems validated for healthcare demonstration.")
            sys.exit(0)
        else:
            print("❌ Demo deployment needs attention before October 15.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⚠️ Validation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Validation error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()