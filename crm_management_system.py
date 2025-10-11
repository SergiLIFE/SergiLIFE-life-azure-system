#!/usr/bin/env python3
"""
L.I.F.E. Platform - Comprehensive CRM Management System
October 11, 2025 | Demo Participant Management & Pipeline Tracking

Advanced CRM system for managing demo participants, tracking communications,
and automating follow-up sequences for October 15, 2025 demo.
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging

# Setup logging
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CRM_DIR = os.path.join(SCRIPT_DIR, "crm_database")
COMMUNICATIONS_DIR = os.path.join(CRM_DIR, "communications")
PIPELINE_DIR = os.path.join(CRM_DIR, "pipeline")
AUTOMATION_DIR = os.path.join(CRM_DIR, "automation")
LOGS_DIR = os.path.join(SCRIPT_DIR, "logs")

# Create directories
for dir_path in [CRM_DIR, COMMUNICATIONS_DIR, PIPELINE_DIR, AUTOMATION_DIR, LOGS_DIR]:
    os.makedirs(dir_path, exist_ok=True)

LOG_FILE = os.path.join(LOGS_DIR, "crm_management_system.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

class CRMManagementSystem:
    """
    Comprehensive CRM system for L.I.F.E. Platform demo management
    """
    
    def __init__(self):
        self.demo_date = datetime(2025, 10, 15, 9, 0)  # October 15, 2025, 9:00 AM
        self.crm_database = os.path.join(CRM_DIR, "crm_participant_tracking.json")
        self.communication_log = os.path.join(COMMUNICATIONS_DIR, "communication_history.json")
        self.pipeline_tracker = os.path.join(PIPELINE_DIR, "conversion_pipeline.json")
        
        # Initialize CRM data
        self.participants = self._load_or_initialize_participants()
        self.communication_history = self._load_communication_history()
        self.pipeline_data = self._initialize_pipeline_tracking()
    
    def _load_or_initialize_participants(self) -> Dict[str, Dict[str, Any]]:
        """
        Load existing participant data or initialize new
        """
        if os.path.exists(self.crm_database):
            with open(self.crm_database, 'r') as f:
                return json.load(f)
        
        # Initialize with consolidated participant data
        return {
            "LIFE_001": {
                "organization": "University of Oxford",
                "contact_name": "Dr. Oxford Neuroscience Lead",
                "email": "neuroscience.dept@ox.ac.uk",
                "phone": "+44 1865 272000",
                "status": "Hot Lead",
                "demo_confirmed": True,
                "session_assigned": "Session 1: Clinical Professionals",
                "last_interaction": "2025-10-10",
                "next_action": "Send demo reminder",
                "next_action_date": "2025-10-12",
                "conversion_stage": "Demo Scheduled",
                "priority": "High",
                "revenue_potential": 162500,
                "conversion_probability": 85,
                "notes": ["Premium institution", "High conversion potential", "Active trial user"]
            },
            "LIFE_002": {
                "organization": "Cambridge University",
                "contact_name": "Dr. Cambridge Brain Sciences Lead",
                "email": "brain.sciences@cam.ac.uk",
                "phone": "+44 1223 337733",
                "status": "Hot Lead",
                "demo_confirmed": True,
                "session_assigned": "Session 1: Clinical Professionals",
                "last_interaction": "2025-10-10",
                "next_action": "Send demo reminder + trial setup",
                "next_action_date": "2025-10-12",
                "conversion_stage": "Demo Scheduled",
                "priority": "High",
                "revenue_potential": 150000,
                "conversion_probability": 80,
                "notes": ["Prestigious university", "Research focus", "Multi-department potential"]
            },
            "LIFE_003": {
                "organization": "Microsoft Research Cambridge",
                "contact_name": "Microsoft Partnership Lead",
                "email": "partnerships@microsoft.com",
                "phone": "+44 1223 479700",
                "status": "Enterprise Lead",
                "demo_confirmed": True,
                "session_assigned": "Session 2: Research & IT Leadership",
                "last_interaction": "2025-10-10",
                "next_action": "Partnership discussion prep",
                "next_action_date": "2025-10-12",
                "conversion_stage": "Partnership Track",
                "priority": "Critical",
                "revenue_potential": 475000,
                "conversion_probability": 95,
                "notes": ["DIRECT PARTNERSHIP OPPORTUNITY", "Highest priority", "Strategic alliance potential"]
            },
            "LIFE_004": {
                "organization": "NHS Royal London Hospital",
                "contact_name": "NHS Clinical Lead",
                "email": "neurology.rln@nhs.net",
                "phone": "+44 20 7377 7000",
                "status": "Warm Lead",
                "demo_confirmed": False,
                "session_assigned": "Session 1: Clinical Professionals",
                "last_interaction": "2025-10-10",
                "next_action": "Confirmation call needed",
                "next_action_date": "2025-10-11",
                "conversion_stage": "Follow-up Required",
                "priority": "Medium",
                "revenue_potential": 195000,
                "conversion_probability": 65,
                "notes": ["Large NHS hospital", "Budget approval process", "High patient volume"]
            },
            "LIFE_005": {
                "organization": "Imperial College London",
                "contact_name": "Imperial Research Lead",
                "email": "bioeng.research@imperial.ac.uk",
                "phone": "+44 20 7589 5111",
                "status": "Warm Lead",
                "demo_confirmed": False,
                "session_assigned": "Session 2: Research & IT Leadership",
                "last_interaction": "2025-10-10",
                "next_action": "Research collaboration discussion",
                "next_action_date": "2025-10-12",
                "conversion_stage": "Follow-up Required",
                "priority": "Medium",
                "revenue_potential": 131250,
                "conversion_probability": 70,
                "notes": ["Top engineering school", "Research focused", "Academic partnership potential"]
            }
        }
    
    def _load_communication_history(self) -> List[Dict[str, Any]]:
        """
        Load communication history
        """
        if os.path.exists(self.communication_log):
            with open(self.communication_log, 'r') as f:
                return json.load(f)
        return []
    
    def _initialize_pipeline_tracking(self) -> Dict[str, Any]:
        """
        Initialize conversion pipeline tracking
        """
        return {
            "pipeline_stages": {
                "Lead Generated": {"count": 5, "value": 1113750},
                "Demo Scheduled": {"count": 3, "value": 787500},
                "Demo Completed": {"count": 0, "value": 0},
                "Trial Started": {"count": 1, "value": 162500},
                "Negotiation": {"count": 0, "value": 0},
                "Closed Won": {"count": 0, "value": 0},
                "Closed Lost": {"count": 0, "value": 0}
            },
            "forecast": {
                "total_pipeline_value": 1113750,
                "weighted_forecast": 924688,  # Probability-weighted
                "expected_close_q1_2026": 787500,
                "best_case_scenario": 1113750,
                "worst_case_scenario": 475000  # Microsoft partnership minimum
            },
            "conversion_metrics": {
                "lead_to_demo_rate": 60,  # 3/5 confirmed demos
                "demo_to_trial_rate": 85,  # Expected based on engagement
                "trial_to_customer_rate": 75,  # Industry benchmark
                "average_sales_cycle_days": 90
            }
        }
    
    def log_communication(self, participant_id: str, communication_type: str, 
                         subject: str, content: str, outcome: str) -> None:
        """
        Log communication with participant
        """
        communication = {
            "participant_id": participant_id,
            "timestamp": datetime.now().isoformat(),
            "type": communication_type,
            "subject": subject,
            "content": content,
            "outcome": outcome,
            "follow_up_required": outcome in ["No response", "Requested callback", "Needs more info"]
        }
        
        self.communication_history.append(communication)
        
        # Update participant's last interaction
        if participant_id in self.participants:
            self.participants[participant_id]["last_interaction"] = datetime.now().date().isoformat()
        
        logging.info(f"Communication logged: {participant_id} - {communication_type}")
    
    def update_participant_status(self, participant_id: str, new_status: str, 
                                notes: str = None) -> None:
        """
        Update participant status and stage
        """
        if participant_id in self.participants:
            old_status = self.participants[participant_id]["status"]
            self.participants[participant_id]["status"] = new_status
            
            if notes:
                self.participants[participant_id]["notes"].append(f"{datetime.now().date()}: {notes}")
            
            # Update conversion stage based on status
            stage_mapping = {
                "Cold Lead": "Lead Generated",
                "Warm Lead": "Lead Generated", 
                "Hot Lead": "Demo Scheduled",
                "Enterprise Lead": "Demo Scheduled",
                "Demo Completed": "Demo Completed",
                "Trial User": "Trial Started",
                "Negotiating": "Negotiation",
                "Customer": "Closed Won",
                "Lost": "Closed Lost"
            }
            
            if new_status in stage_mapping:
                self.participants[participant_id]["conversion_stage"] = stage_mapping[new_status]
            
            logging.info(f"Status updated: {participant_id} - {old_status} → {new_status}")
    
    def schedule_follow_up(self, participant_id: str, action: str, 
                          scheduled_date: str, priority: str = "Medium") -> None:
        """
        Schedule follow-up action for participant
        """
        if participant_id in self.participants:
            self.participants[participant_id]["next_action"] = action
            self.participants[participant_id]["next_action_date"] = scheduled_date
            self.participants[participant_id]["priority"] = priority
            
            logging.info(f"Follow-up scheduled: {participant_id} - {action} on {scheduled_date}")
    
    def get_daily_action_items(self, date: str = None) -> List[Dict[str, Any]]:
        """
        Get action items for specific date (defaults to today)
        """
        if date is None:
            date = datetime.now().date().isoformat()
        
        action_items = []
        
        for participant_id, data in self.participants.items():
            if data.get("next_action_date") == date:
                action_items.append({
                    "participant_id": participant_id,
                    "organization": data["organization"],
                    "action": data["next_action"],
                    "priority": data.get("priority", "Medium"),
                    "contact_email": data["email"],
                    "contact_phone": data["phone"],
                    "notes": data.get("notes", [])[-1] if data.get("notes") else "No recent notes"
                })
        
        # Sort by priority
        priority_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
        action_items.sort(key=lambda x: priority_order.get(x["priority"], 2))
        
        return action_items
    
    def generate_pipeline_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive pipeline report
        """
        # Calculate current pipeline metrics
        total_participants = len(self.participants)
        confirmed_demos = len([p for p in self.participants.values() if p["demo_confirmed"]])
        total_revenue_potential = sum([p["revenue_potential"] for p in self.participants.values()])
        weighted_revenue = sum([p["revenue_potential"] * (p["conversion_probability"] / 100) 
                              for p in self.participants.values()])
        
        # Stage breakdown
        stage_counts = {}
        stage_values = {}
        
        for participant in self.participants.values():
            stage = participant["conversion_stage"]
            stage_counts[stage] = stage_counts.get(stage, 0) + 1
            stage_values[stage] = stage_values.get(stage, 0) + participant["revenue_potential"]
        
        return {
            "report_date": datetime.now().isoformat(),
            "demo_date": "2025-10-15",
            "days_to_demo": (self.demo_date - datetime.now()).days,
            "total_participants": total_participants,
            "confirmed_demos": confirmed_demos,
            "demo_confirmation_rate": (confirmed_demos / total_participants) * 100,
            "total_pipeline_value": total_revenue_potential,
            "weighted_forecast": weighted_revenue,
            "stage_breakdown": {
                "counts": stage_counts,
                "values": stage_values
            },
            "top_opportunities": [
                {
                    "participant_id": pid,
                    "organization": data["organization"],
                    "revenue_potential": data["revenue_potential"],
                    "conversion_probability": data["conversion_probability"],
                    "weighted_value": data["revenue_potential"] * (data["conversion_probability"] / 100)
                }
                for pid, data in sorted(self.participants.items(), 
                                     key=lambda x: x[1]["revenue_potential"] * (x[1]["conversion_probability"] / 100),
                                     reverse=True)
            ][:3]
        }
    
    def save_crm_data(self) -> None:
        """
        Save all CRM data to files
        """
        # Save participants data
        with open(self.crm_database, 'w') as f:
            json.dump(self.participants, f, indent=2)
        
        # Save communication history
        with open(self.communication_log, 'w') as f:
            json.dump(self.communication_history, f, indent=2)
        
        # Save pipeline data
        with open(self.pipeline_tracker, 'w') as f:
            json.dump(self.pipeline_data, f, indent=2)
        
        logging.info("CRM data saved successfully")
    
    def generate_crm_dashboard(self) -> None:
        """
        Generate comprehensive CRM dashboard
        """
        print("\n" + "="*80)
        print("🎯 L.I.F.E. PLATFORM - CRM MANAGEMENT DASHBOARD")
        print("="*80)
        print(f"📅 Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🎪 Demo Date: October 15, 2025")
        print(f"⏰ Days to Demo: {(self.demo_date - datetime.now()).days}")
        
        # Pipeline overview
        report = self.generate_pipeline_report()
        print(f"\n📊 PIPELINE OVERVIEW:")
        print(f"   👥 Total Participants: {report['total_participants']}")
        print(f"   ✅ Confirmed Demos: {report['confirmed_demos']} ({report['demo_confirmation_rate']:.1f}%)")
        print(f"   💰 Total Pipeline Value: ${report['total_pipeline_value']:,}")
        print(f"   📈 Weighted Forecast: ${report['weighted_forecast']:,.0f}")
        
        # Today's action items
        today_actions = self.get_daily_action_items()
        print(f"\n📋 TODAY'S ACTION ITEMS ({len(today_actions)}):")
        for i, action in enumerate(today_actions, 1):
            print(f"   {i}. {action['organization']} - {action['priority']} Priority")
            print(f"      📞 Action: {action['action']}")
            print(f"      📧 Contact: {action['contact_email']}")
            print(f"      📝 Note: {action['notes']}")
        
        if not today_actions:
            print("   ✅ No action items for today!")
        
        # Participant status breakdown
        print(f"\n👥 PARTICIPANT STATUS:")
        for participant_id, data in self.participants.items():
            status_emoji = {
                "Hot Lead": "🔥", 
                "Warm Lead": "🌡️", 
                "Enterprise Lead": "🏢",
                "Cold Lead": "❄️"
            }.get(data["status"], "📋")
            
            demo_status = "✅" if data["demo_confirmed"] else "❓"
            
            print(f"   {status_emoji} {data['organization']}")
            print(f"      📧 {data['email']}")
            print(f"      🎪 Demo: {demo_status} {data['session_assigned']}")
            print(f"      📈 Conversion: {data['conversion_probability']}% | ${data['revenue_potential']:,}")
            print(f"      📞 Next: {data['next_action']} ({data['next_action_date']})")
        
        # Top opportunities
        print(f"\n🏆 TOP OPPORTUNITIES:")
        for i, opp in enumerate(report['top_opportunities'], 1):
            print(f"   {i}. {opp['organization']}")
            print(f"      💰 Value: ${opp['revenue_potential']:,}")
            print(f"      📊 Probability: {opp['conversion_probability']}%")
            print(f"      🎯 Weighted: ${opp['weighted_value']:,.0f}")
        
        # Communication summary
        recent_comms = [c for c in self.communication_history if c['timestamp'] >= '2025-10-10']
        print(f"\n📞 RECENT COMMUNICATIONS ({len(recent_comms)}):")
        for comm in recent_comms[-5:]:  # Show last 5
            participant = self.participants.get(comm['participant_id'], {})
            org_name = participant.get('organization', 'Unknown')
            print(f"   📅 {comm['timestamp'][:10]} - {org_name}")
            print(f"      📝 {comm['type']}: {comm['subject']}")
            print(f"      🎯 Outcome: {comm['outcome']}")
        
        print(f"\n📁 CRM FILES:")
        print(f"   📊 Participants: {self.crm_database}")
        print(f"   📞 Communications: {self.communication_log}")
        print(f"   📈 Pipeline: {self.pipeline_tracker}")
        
        print(f"\n🚀 NEXT PRIORITIES:")
        print(f"   1. Complete demo confirmations (NHS, Imperial)")
        print(f"   2. Prepare Microsoft partnership discussion")
        print(f"   3. Send demo reminder emails")
        print(f"   4. Customize demo content for each session")
        print(f"   5. Set up post-demo follow-up automation")

def main():
    """
    Main CRM system execution
    """
    print("🚀 Initializing L.I.F.E. Platform CRM Management System...")
    
    # Create CRM system
    crm = CRMManagementSystem()
    
    # Add sample communications for demo
    crm.log_communication(
        "LIFE_001", 
        "Email", 
        "Demo Invitation - October 15", 
        "Sent demo invitation with session details",
        "Confirmed attendance"
    )
    
    crm.log_communication(
        "LIFE_003",
        "Email",
        "Partnership Discussion Request",
        "Requested meeting to discuss strategic partnership",
        "Very positive response - scheduling call"
    )
    
    # Schedule follow-ups
    crm.schedule_follow_up("LIFE_004", "Confirmation call for demo", "2025-10-11", "High")
    crm.schedule_follow_up("LIFE_001", "Send demo reminder + prep materials", "2025-10-12", "Medium")
    
    # Generate dashboard
    crm.generate_crm_dashboard()
    
    # Save all data
    crm.save_crm_data()
    
    print("\n🎉 CRM Management System Setup Complete!")
    print("📊 All participant data consolidated and tracked.")
    print("🔄 Communication history and pipeline ready.")

if __name__ == "__main__":
    main()