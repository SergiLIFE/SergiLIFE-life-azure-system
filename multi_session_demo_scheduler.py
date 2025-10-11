#!/usr/bin/env python3
"""
L.I.F.E. Platform - Multi-Session Demo Scheduler
October 15, 2025 - Three Targeted Demo Sessions

Strategic scheduling system for running 3 specialized demo sessions
targeting different healthcare professional groups.
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Setup logging
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(SCRIPT_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOGS_DIR, "multi_session_demo_scheduler.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

class MultiSessionDemoScheduler:
    """
    Manage three specialized demo sessions for different healthcare audiences
    """
    
    def __init__(self):
        self.demo_date = "October 15, 2025"
        self.total_participants = 23
        
        # Three specialized demo sessions
        self.demo_sessions = {
            "Session 1: Clinical Professionals": {
                "time": "09:00 - 09:45 BST",
                "duration_minutes": 45,
                "target_audience": "Direct patient care providers",
                "participants": {
                    "Neurology Departments": 6,
                    "Psychiatry & Mental Health": 5,
                    "Pediatric Neurology": 4,
                    "Rehabilitation & Therapy": 2
                },
                "total_participants": 17,
                "percentage": 73.9,
                "primary_focus": "Clinical workflow and patient care optimization",
                "demo_sections_emphasis": [
                    "EEG Processing (15 min)",
                    "Adaptive Learning (12 min)", 
                    "Clinical Integration (10 min)",
                    "Analytics Dashboard (5 min)",
                    "Q&A (3 min)"
                ],
                "key_messages": [
                    "Real-time EEG processing with 0.38ms latency",
                    "Improved patient outcomes through adaptive learning", 
                    "Seamless integration with clinical workflows",
                    "Evidence-based treatment optimization"
                ],
                "pricing_tier": "Professional ($75,000/year)",
                "expected_conversions": 3.9,
                "revenue_potential": "$351,000"
            },
            
            "Session 2: Research & IT Leadership": {
                "time": "11:00 - 11:45 BST",
                "duration_minutes": 45,
                "target_audience": "Research directors and IT decision makers",
                "participants": {
                    "Clinical Research": 3,
                    "Hospital IT & Administration": 3
                },
                "total_participants": 6,
                "percentage": 26.1,
                "primary_focus": "Enterprise capabilities and research innovation",
                "demo_sections_emphasis": [
                    "Research Tools (15 min)",
                    "Clinical Integration (12 min)",
                    "Analytics Dashboard (10 min)",
                    "EEG Processing (5 min)",
                    "Q&A (3 min)"
                ],
                "key_messages": [
                    "Multi-site research collaboration capabilities",
                    "Enterprise-grade security and compliance",
                    "Advanced analytics and data export options",
                    "Scalable deployment for large organizations"
                ],
                "pricing_tier": "Enterprise ($250,000/year)",
                "expected_conversions": 1.4,
                "revenue_potential": "$420,000"
            },
            
            "Session 3: Executive & Strategic Overview": {
                "time": "14:00 - 14:30 BST",
                "duration_minutes": 30,
                "target_audience": "All participants - strategic overview and Q&A",
                "participants": {
                    "All Fields Combined": 23
                },
                "total_participants": 23,
                "percentage": 100.0,
                "primary_focus": "Strategic value, ROI, and implementation planning",
                "demo_sections_emphasis": [
                    "ROI Calculator (10 min)",
                    "Analytics Dashboard (8 min)",
                    "Implementation Overview (7 min)",
                    "Strategic Q&A (5 min)"
                ],
                "key_messages": [
                    "Comprehensive ROI analysis and business case",
                    "Strategic implementation roadmap",
                    "Long-term partnership and growth opportunities",
                    "Risk mitigation through pilot programs"
                ],
                "pricing_tier": "Both tiers with custom options",
                "expected_conversions": 5.3,
                "revenue_potential": "$771,000"
            }
        }
        
        # Session-specific customizations
        self.session_customizations = {
            "Session 1: Clinical Professionals": {
                "demo_website_focus": [
                    "eeg-processing (primary landing)",
                    "adaptive-learning", 
                    "clinical-integration",
                    "analytics"
                ],
                "roi_calculator_presets": {
                    "organization_size": "medium",
                    "current_methods": "basic",
                    "monthly_assessments": 200,
                    "current_cost": 125
                },
                "presentation_style": "Hands-on clinical demonstration",
                "technical_depth": "Moderate - focus on usability",
                "interaction_level": "High - encourage questions during demo"
            },
            
            "Session 2: Research & IT Leadership": {
                "demo_website_focus": [
                    "research-tools (primary landing)",
                    "clinical-integration",
                    "analytics", 
                    "eeg-processing"
                ],
                "roi_calculator_presets": {
                    "organization_size": "large",
                    "current_methods": "advanced",
                    "monthly_assessments": 500,
                    "current_cost": 200
                },
                "presentation_style": "Technical deep-dive and architecture",
                "technical_depth": "High - detailed technical specifications",
                "interaction_level": "Moderate - structured Q&A at end"
            },
            
            "Session 3: Executive & Strategic Overview": {
                "demo_website_focus": [
                    "roi-calculator (primary landing)",
                    "analytics",
                    "clinical-integration",
                    "research-tools"
                ],
                "roi_calculator_presets": {
                    "organization_size": "enterprise",
                    "current_methods": "multiple", 
                    "monthly_assessments": 1000,
                    "current_cost": 175
                },
                "presentation_style": "Strategic business presentation",
                "technical_depth": "Low - focus on outcomes and ROI",
                "interaction_level": "Very high - open discussion format"
            }
        }
        
        logging.info("Multi-session demo scheduler initialized")
        logging.info(f"Configured for {len(self.demo_sessions)} sessions on {self.demo_date}")
    
    def generate_session_urls(self, session_name: str) -> Dict[str, str]:
        """
        Generate session-specific URLs with landing page customization
        """
        try:
            if session_name not in self.session_customizations:
                logging.error(f"Session not found: {session_name}")
                return {}
            
            customization = self.session_customizations[session_name]
            primary_section = customization["demo_website_focus"][0]
            
            base_url = "http://localhost:8080/LIFE_PLATFORM_DEMO_WEBSITE.html"
            
            session_urls = {
                "main_demo": f"{base_url}#{primary_section}",
                "backup_url": f"{base_url}",
                "direct_sections": {}
            }
            
            # Generate direct section URLs for this session's focus
            for section in customization["demo_website_focus"]:
                section_name = section.replace("-", " ").title()
                session_urls["direct_sections"][section_name] = f"{base_url}#{section}"
            
            logging.info(f"Generated URLs for {session_name}")
            return session_urls
            
        except Exception as e:
            logging.error(f"Failed to generate session URLs: {e}")
            return {}
    
    def create_session_schedule(self) -> Dict[str, Any]:
        """
        Create comprehensive session schedule with timing and logistics
        """
        try:
            logging.info("Creating comprehensive session schedule...")
            
            schedule = {
                "demo_date": self.demo_date,
                "total_sessions": len(self.demo_sessions),
                "total_participants": self.total_participants,
                "session_details": {},
                "logistics": {
                    "setup_time": "08:30 - 08:55 BST (25 minutes)",
                    "break_between_sessions": "15 minutes",
                    "total_demo_duration": "3 hours 30 minutes",
                    "technical_support": "Available throughout all sessions"
                },
                "preparation_checklist": {
                    "technical": [
                        "Demo website tested on all target sections",
                        "ROI calculator presets configured for each session",
                        "Backup demo server ready on port 8081",
                        "Screen sharing and audio tested",
                        "Internet connection verified"
                    ],
                    "content": [
                        "Session-specific talking points prepared",
                        "Field-specific use cases ready",
                        "Pricing materials customized per audience", 
                        "Follow-up materials prepared for each session",
                        "Pilot program agreements ready"
                    ],
                    "logistics": [
                        "Participant lists confirmed for each session",
                        "Calendar invites sent with session-specific URLs",
                        "Recording permissions obtained if needed",
                        "Follow-up scheduling system ready",
                        "Contact capture system prepared"
                    ]
                }
            }
            
            # Generate detailed schedule for each session
            for session_name, session_data in self.demo_sessions.items():
                session_urls = self.generate_session_urls(session_name)
                customization = self.session_customizations.get(session_name, {})
                
                session_schedule = {
                    "session_info": session_data,
                    "customization": customization,
                    "urls": session_urls,
                    "timeline": self._generate_session_timeline(session_data),
                    "materials_needed": self._generate_session_materials(session_name),
                    "success_metrics": self._generate_session_metrics(session_data)
                }
                
                schedule["session_details"][session_name] = session_schedule
            
            logging.info("Session schedule created successfully")
            return schedule
            
        except Exception as e:
            logging.error(f"Failed to create session schedule: {e}")
            return {}
    
    def _generate_session_timeline(self, session_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Generate minute-by-minute timeline for a session
        """
        try:
            timeline = []
            
            # Parse start time
            start_time = session_data["time"].split(" - ")[0]
            duration = session_data["duration_minutes"]
            
            if duration == 45:  # Full sessions
                timeline = [
                    {"time": f"{start_time}", "activity": "Welcome & Introduction", "duration": "3 min"},
                    {"time": f"{start_time}+03", "activity": "Primary Demo Section", "duration": "15 min"},
                    {"time": f"{start_time}+18", "activity": "Secondary Demo Section", "duration": "12 min"},
                    {"time": f"{start_time}+30", "activity": "Supporting Demo Section", "duration": "10 min"},
                    {"time": f"{start_time}+40", "activity": "Analytics & ROI", "duration": "5 min"},
                    {"time": f"{start_time}+45", "activity": "Q&A & Next Steps", "duration": "Open"}
                ]
            else:  # 30-minute executive session
                timeline = [
                    {"time": f"{start_time}", "activity": "Strategic Overview", "duration": "5 min"},
                    {"time": f"{start_time}+05", "activity": "ROI Analysis", "duration": "10 min"},
                    {"time": f"{start_time}+15", "activity": "Analytics Dashboard", "duration": "8 min"},
                    {"time": f"{start_time}+23", "activity": "Implementation Planning", "duration": "7 min"},
                    {"time": f"{start_time}+30", "activity": "Strategic Discussion", "duration": "Open"}
                ]
            
            return timeline
            
        except Exception as e:
            logging.error(f"Failed to generate timeline: {e}")
            return []
    
    def _generate_session_materials(self, session_name: str) -> Dict[str, List[str]]:
        """
        Generate list of materials needed for each session
        """
        base_materials = {
            "presentation": [
                "Demo website ready on primary URL",
                "ROI calculator with session-specific presets",
                "Field-specific talking points",
                "Pricing tier information"
            ],
            "follow_up": [
                "Custom ROI reports template",
                "Pilot program agreements", 
                "Technical integration assessment forms",
                "Implementation timeline documents"
            ]
        }
        
        # Add session-specific materials
        if "Clinical" in session_name:
            base_materials["presentation"].extend([
                "Clinical workflow integration demo",
                "Patient outcome case studies",
                "EHR integration examples"
            ])
        elif "Research" in session_name:
            base_materials["presentation"].extend([
                "Multi-site collaboration examples",
                "Research protocol templates", 
                "Data export format samples"
            ])
        elif "Executive" in session_name:
            base_materials["presentation"].extend([
                "Business case presentation",
                "Strategic roadmap overview",
                "Partnership opportunity materials"
            ])
        
        return base_materials
    
    def _generate_session_metrics(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate success metrics for each session
        """
        return {
            "participation_target": f"{session_data['total_participants']} confirmed attendees",
            "engagement_target": "90% active participation throughout session",
            "conversion_target": f"{session_data['expected_conversions']} qualified leads",
            "follow_up_target": "100% follow-up within 24 hours",
            "revenue_target": session_data['revenue_potential']
        }
    
    def export_session_guide(self) -> str:
        """
        Export comprehensive session guide for demo preparation
        """
        try:
            logging.info("Exporting session guide...")
            
            schedule = self.create_session_schedule()
            
            # Create session guide directory
            guide_dir = os.path.join(SCRIPT_DIR, "multi_session_demo")
            os.makedirs(guide_dir, exist_ok=True)
            
            # Export main schedule
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            main_guide_path = os.path.join(guide_dir, f"multi_session_demo_guide_{timestamp}.json")
            
            with open(main_guide_path, 'w', encoding='utf-8') as f:
                json.dump(schedule, f, indent=2, ensure_ascii=False)
            
            # Create individual session files
            for session_name, session_details in schedule["session_details"].items():
                session_filename = session_name.lower().replace(" ", "_").replace(":", "") + ".json"
                session_path = os.path.join(guide_dir, session_filename)
                
                with open(session_path, 'w', encoding='utf-8') as f:
                    json.dump({session_name: session_details}, f, indent=2, ensure_ascii=False)
            
            logging.info(f"Session guide exported: {main_guide_path}")
            return main_guide_path
            
        except Exception as e:
            logging.error(f"Failed to export session guide: {e}")
            return ""
    
    def display_session_overview(self):
        """
        Display formatted overview of all three demo sessions
        """
        try:
            print("🎯 L.I.F.E. PLATFORM - MULTI-SESSION DEMO SCHEDULE")
            print("=" * 80)
            print(f"📅 Demo Date: {self.demo_date}")
            print(f"👥 Total Participants: {self.total_participants}")
            print(f"🎪 Total Sessions: {len(self.demo_sessions)}")
            print("=" * 80)
            
            for session_name, session_data in self.demo_sessions.items():
                print(f"\n🎭 {session_name.upper()}")
                print(f"⏰ Time: {session_data['time']}")
                print(f"👥 Participants: {session_data['total_participants']} ({session_data['percentage']:.1f}%)")
                print(f"🎯 Focus: {session_data['primary_focus']}")
                print(f"💰 Tier: {session_data['pricing_tier']}")
                print(f"📈 Revenue Potential: {session_data['revenue_potential']}")
                
                print("   📊 Participant Breakdown:")
                for field, count in session_data['participants'].items():
                    print(f"     • {field}: {count} participants")
                
                print("   🎪 Demo Sections:")
                for section in session_data['demo_sections_emphasis']:
                    print(f"     • {section}")
                
                # Show session URLs
                session_urls = self.generate_session_urls(session_name)
                if session_urls:
                    print(f"   🔗 Primary URL: {session_urls.get('main_demo', 'TBD')}")
            
            print(f"\n📋 LOGISTICS OVERVIEW:")
            print("   🕘 Setup Time: 08:30 - 08:55 BST (25 minutes)")
            print("   ⏸️ Break Between Sessions: 15 minutes")
            print("   🏁 Total Duration: 3 hours 30 minutes")
            print("   🔧 Technical Support: Available throughout")
            
            print(f"\n🎯 COMBINED SUCCESS TARGETS:")
            total_expected = sum(session['expected_conversions'] for session in self.demo_sessions.values())
            total_revenue = "$771,000"  # From previous calculation
            print(f"   📈 Expected Conversions: {total_expected:.1f} organizations")
            print(f"   💰 Total Revenue Pipeline: {total_revenue}")
            print(f"   🎪 Demo Completion Rate Target: 95%")
            print(f"   📞 Follow-up Rate Target: 100% within 24 hours")
            
            print("\n" + "=" * 80)
            print("✅ Multi-session demo schedule ready for October 15, 2025!")
            print("=" * 80)
            
        except Exception as e:
            logging.error(f"Failed to display session overview: {e}")

def main():
    """
    Main execution function for multi-session demo scheduler
    """
    try:
        print("L.I.F.E. Platform Multi-Session Demo Scheduler")
        print("October 15, 2025 - Three Specialized Sessions")
        print("-" * 60)
        
        # Initialize scheduler
        scheduler = MultiSessionDemoScheduler()
        
        # Display session overview
        scheduler.display_session_overview()
        
        # Export detailed guide
        guide_path = scheduler.export_session_guide()
        if guide_path:
            print(f"\n📄 Detailed session guide exported: {os.path.basename(guide_path)}")
        
        print("\n✅ Multi-session demo schedule complete!")
        print("\n🎯 NEXT STEPS:")
        print("   1. Review each session's customized approach")
        print("   2. Test demo website with session-specific URLs")
        print("   3. Prepare session-specific materials")
        print("   4. Send calendar invites with appropriate URLs")
        print("   5. Configure ROI calculator presets for each session")
        
    except Exception as e:
        logging.error(f"Main execution failed: {e}")
        print(f"\n❌ Scheduler error: {e}")

if __name__ == "__main__":
    main()