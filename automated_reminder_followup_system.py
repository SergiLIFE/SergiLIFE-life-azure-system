#!/usr/bin/env python3
"""
L.I.F.E. Platform - Automated Reminder & Follow-up System
October 11, 2025 | Demo Preparation & Conversion Automation

Comprehensive automation system for demo reminders, preparation materials,
and post-demo follow-up sequences for October 15, 2025.
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging

# Setup logging
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AUTOMATION_DIR = os.path.join(SCRIPT_DIR, "automation_system")
REMINDERS_DIR = os.path.join(AUTOMATION_DIR, "reminders")
FOLLOWUP_DIR = os.path.join(AUTOMATION_DIR, "followup")
TEMPLATES_DIR = os.path.join(AUTOMATION_DIR, "email_templates")
LOGS_DIR = os.path.join(SCRIPT_DIR, "logs")

# Create directories
for dir_path in [AUTOMATION_DIR, REMINDERS_DIR, FOLLOWUP_DIR, TEMPLATES_DIR, LOGS_DIR]:
    os.makedirs(dir_path, exist_ok=True)

LOG_FILE = os.path.join(LOGS_DIR, "automation_reminder_system.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

class AutomatedReminderSystem:
    """
    Comprehensive automation system for demo reminders and follow-up sequences
    """
    
    def __init__(self):
        self.demo_date = datetime(2025, 10, 15, 9, 0)  # October 15, 2025, 9:00 AM
        self.reminder_schedule = self._create_reminder_schedule()
        self.followup_schedule = self._create_followup_schedule()
        self.email_templates = self._create_email_templates()
        
        # Load participant data (would integrate with CRM system)
        self.participants = self._load_participant_data()
    
    def _load_participant_data(self) -> Dict[str, Dict[str, Any]]:
        """
        Load participant data for automation
        """
        return {
            "LIFE_001": {
                "organization": "University of Oxford",
                "contact_name": "Dr. Oxford Neuroscience Lead",
                "email": "neuroscience.dept@ox.ac.uk",
                "session": "Session 1: Clinical Professionals",
                "session_time": "09:00-09:45 BST",
                "session_url": "https://meet.google.com/life-clinical-session",
                "customization": "clinical_workflow",
                "priority": "High"
            },
            "LIFE_002": {
                "organization": "Cambridge University", 
                "contact_name": "Dr. Cambridge Brain Sciences Lead",
                "email": "brain.sciences@cam.ac.uk",
                "session": "Session 1: Clinical Professionals",
                "session_time": "09:00-09:45 BST", 
                "session_url": "https://meet.google.com/life-clinical-session",
                "customization": "research_integration",
                "priority": "High"
            },
            "LIFE_003": {
                "organization": "Microsoft Research Cambridge",
                "contact_name": "Microsoft Partnership Lead",
                "email": "partnerships@microsoft.com",
                "session": "Session 2: Research & IT Leadership",
                "session_time": "11:00-11:45 BST",
                "session_url": "https://teams.microsoft.com/life-enterprise-session",
                "customization": "enterprise_partnership",
                "priority": "Critical"
            },
            "LIFE_004": {
                "organization": "NHS Royal London Hospital",
                "contact_name": "NHS Clinical Lead", 
                "email": "neurology.rln@nhs.net",
                "session": "Session 1: Clinical Professionals",
                "session_time": "09:00-09:45 BST",
                "session_url": "https://meet.google.com/life-clinical-session",
                "customization": "nhs_compliance",
                "priority": "Medium"
            },
            "LIFE_005": {
                "organization": "Imperial College London",
                "contact_name": "Imperial Research Lead",
                "email": "bioeng.research@imperial.ac.uk", 
                "session": "Session 2: Research & IT Leadership",
                "session_time": "11:00-11:45 BST",
                "session_url": "https://meet.google.com/life-research-session",
                "customization": "academic_research",
                "priority": "Medium"
            }
        }
    
    def _create_reminder_schedule(self) -> List[Dict[str, Any]]:
        """
        Create comprehensive reminder schedule leading up to demo
        """
        demo_date = self.demo_date.date()
        
        return [
            {
                "name": "Initial Confirmation",
                "trigger_date": (demo_date - timedelta(days=4)).isoformat(),  # Oct 11
                "template": "initial_confirmation",
                "subject": "L.I.F.E. Platform Demo Confirmation - October 15, 2025",
                "priority": "High",
                "includes": ["session_details", "calendar_invite", "preparation_guide"]
            },
            {
                "name": "Preparation Reminder",
                "trigger_date": (demo_date - timedelta(days=2)).isoformat(),  # Oct 13
                "template": "preparation_reminder", 
                "subject": "Demo Preparation Materials - L.I.F.E. Platform (2 Days)",
                "priority": "Medium",
                "includes": ["pre_demo_questionnaire", "technical_requirements", "session_agenda"]
            },
            {
                "name": "Final Reminder",
                "trigger_date": (demo_date - timedelta(days=1)).isoformat(),  # Oct 14
                "template": "final_reminder",
                "subject": "Tomorrow: L.I.F.E. Platform Demo - Final Details",
                "priority": "High", 
                "includes": ["session_links", "contact_information", "backup_options"]
            },
            {
                "name": "Day of Demo",
                "trigger_date": demo_date.isoformat(),  # Oct 15
                "template": "day_of_demo",
                "subject": "Today: L.I.F.E. Platform Demo - Ready to Begin!",
                "priority": "Critical",
                "includes": ["session_links", "support_contact", "last_minute_instructions"]
            }
        ]
    
    def _create_followup_schedule(self) -> List[Dict[str, Any]]:
        """
        Create post-demo follow-up sequence
        """
        demo_date = self.demo_date.date()
        
        return [
            {
                "name": "Immediate Thank You",
                "trigger_date": (demo_date + timedelta(hours=2)).isoformat(),  # 2 hours after
                "template": "immediate_thanks",
                "subject": "Thank You for Attending - L.I.F.E. Platform Demo",
                "priority": "High",
                "includes": ["demo_recording", "next_steps", "trial_access"]
            },
            {
                "name": "Next Day Follow-up", 
                "trigger_date": (demo_date + timedelta(days=1)).isoformat(),  # Oct 16
                "template": "next_day_followup",
                "subject": "L.I.F.E. Platform: Next Steps & Trial Setup",
                "priority": "High",
                "includes": ["personalized_proposal", "trial_setup_link", "implementation_timeline"]
            },
            {
                "name": "One Week Check-in",
                "trigger_date": (demo_date + timedelta(days=7)).isoformat(),  # Oct 22
                "template": "week_checkin",
                "subject": "L.I.F.E. Platform: How's Your Trial Going?",
                "priority": "Medium", 
                "includes": ["usage_analytics", "support_resources", "feature_deep_dive"]
            },
            {
                "name": "Two Week Conversion",
                "trigger_date": (demo_date + timedelta(days=14)).isoformat(),  # Oct 29
                "template": "conversion_push",
                "subject": "L.I.F.E. Platform: Ready to Move Forward?",
                "priority": "High",
                "includes": ["roi_analysis", "implementation_plan", "pricing_options"]
            },
            {
                "name": "One Month Close",
                "trigger_date": (demo_date + timedelta(days=30)).isoformat(),  # Nov 14
                "template": "final_close",
                "subject": "L.I.F.E. Platform: Final Decision Timeline",
                "priority": "Critical",
                "includes": ["final_proposal", "limited_time_offer", "executive_summary"]
            }
        ]
    
    def _create_email_templates(self) -> Dict[str, Dict[str, str]]:
        """
        Create comprehensive email template library
        """
        return {
            "initial_confirmation": {
                "subject": "L.I.F.E. Platform Demo Confirmation - October 15, 2025",
                "body": """
Dear {contact_name},

Thank you for your interest in the L.I.F.E. Platform! We're excited to confirm your attendance at our exclusive demonstration.

📅 **Demo Details:**
• Date: Wednesday, October 15, 2025
• Session: {session}  
• Time: {session_time}
• Duration: 45 minutes
• Platform: {session_url}

🎯 **What to Expect:**
Your session is specifically tailored for {customization_focus}:
• Live EEG processing demonstration (0.38ms latency)
• Adaptive learning algorithms in action
• Integration with your current systems
• Q&A session with our technical team

📋 **Pre-Demo Preparation:**
1. Complete our brief questionnaire: [Link]
2. Test your audio/video setup: [Tech Check Link] 
3. Review attached agenda and materials
4. Prepare specific questions about your use case

🤝 **Microsoft Partnership Benefits:**
As a Microsoft partner solution, you'll have access to:
• Azure credits for implementation
• Enterprise-grade security and compliance
• Seamless Office 365 integration
• Co-selling opportunities

We've attached a calendar invite and preparation guide. Please confirm your attendance by replying to this email.

Looking forward to showing you how L.I.F.E. can transform your {application_area}!

Best regards,
Sergio Paya Borrull
Founder & CEO, L.I.F.E. Platform
📧 sergi@lifecoach-121.com
🌐 https://lifecoach-121.com

---
L.I.F.E. Platform: Learning Individually from Experience
Azure Marketplace Partner | Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
                """,
                "attachments": ["calendar_invite.ics", "demo_preparation_guide.pdf", "technical_requirements.pdf"]
            },
            
            "preparation_reminder": {
                "subject": "Demo Preparation Materials - L.I.F.E. Platform (2 Days)",
                "body": """
Dear {contact_name},

Your L.I.F.E. Platform demo is in 2 days! Here's everything you need to prepare for an exceptional experience.

🎪 **Demo Reminder:**
• Date: Wednesday, October 15, 2025
• Time: {session_time}
• Session: {session}
• Join Link: {session_url}

✅ **Pre-Demo Checklist:**
□ Complete questionnaire (5 minutes): [Link]
□ Test your connection: [Tech Check Link]
□ Review session agenda (attached)
□ Prepare your specific questions
□ Invite relevant colleagues

📊 **What We'll Cover:**
Based on your organization's focus, we'll demonstrate:
• {customization_point_1}
• {customization_point_2} 
• {customization_point_3}
• ROI calculations for your use case

🛠 **Technical Requirements:**
• Stable internet connection (minimum 5 Mbps)
• Chrome, Firefox, Safari, or Edge browser
• Audio/video capability for interaction
• Optional: Second monitor for better experience

❓ **Questions Before the Demo?**
Reply to this email or call: +44 7123 456 789

See you on Wednesday!

Best regards,
Sergio Paya Borrull
L.I.F.E. Platform Team
                """,
                "attachments": ["demo_agenda_personalized.pdf", "roi_calculator.xlsx"]
            },
            
            "final_reminder": {
                "subject": "Tomorrow: L.I.F.E. Platform Demo - Final Details", 
                "body": """
Dear {contact_name},

Your L.I.F.E. Platform demo is TOMORROW! We're excited to show you how our neuroadaptive learning technology can transform your work.

🚀 **Tomorrow's Session:**
• Date: Wednesday, October 15, 2025
• Time: {session_time} 
• Join: {session_url}
• Duration: 45 minutes

🎯 **Session Focus:** {customization}
We've prepared a personalized demonstration based on your organization's needs and the information you've shared with us.

⚡ **Quick Reminders:**
• Join 5 minutes early to test your connection
• Have your questions ready - we love engagement!
• Bring colleagues who might benefit
• We'll record the session for your team

🔗 **Join Links:**
• Primary: {session_url}
• Backup: {backup_url}
• Phone: +44 20 7946 0958 (PIN: {session_pin})

📞 **Need Help?**
• Technical support: +44 7123 456 789
• Demo questions: Reply to this email
• Emergency contact: Sergio directly

Can't wait to meet you tomorrow and show you the future of adaptive learning!

Best regards,
Sergio & the L.I.F.E. Platform Team

P.S. We'll have some exciting announcements about our Microsoft partnership during the demo!
                """,
                "attachments": ["session_backup_options.pdf"]
            },
            
            "immediate_thanks": {
                "subject": "Thank You for Attending - L.I.F.E. Platform Demo",
                "body": """
Dear {contact_name},

Thank you for joining our L.I.F.E. Platform demonstration today! It was fantastic to meet you and your team.

🎉 **What's Next:**
1. **Demo Recording:** Available here: [Link]
2. **Trial Access:** Set up your account: [Trial Link]
3. **Personalized Proposal:** Coming within 24 hours
4. **Follow-up Call:** Scheduled for [Date/Time]

💡 **Key Takeaways from Today:**
• {key_benefit_1}
• {key_benefit_2}
• {key_benefit_3}
• Estimated ROI: {roi_calculation}

🚀 **Immediate Actions:**
□ Access your free 30-day trial
□ Download the demo materials
□ Share recording with your team
□ Schedule implementation planning call

📊 **Your Personalized Results:**
Based on today's discussion, L.I.F.E. Platform could help {organization} achieve:
• {specific_benefit_1}
• {specific_benefit_2}
• {specific_benefit_3}

I'll send your detailed proposal tomorrow morning with pricing, implementation timeline, and next steps.

Questions? Just reply to this email!

Best regards,
Sergio Paya Borrull
Founder, L.I.F.E. Platform
📧 sergi@lifecoach-121.com

---
Ready to transform your {application_area}? Let's make it happen!
                """,
                "attachments": ["demo_materials.zip", "trial_setup_guide.pdf"]
            }
        }
    
    def generate_reminder_sequence(self, participant_id: str) -> List[Dict[str, Any]]:
        """
        Generate personalized reminder sequence for participant
        """
        if participant_id not in self.participants:
            return []
        
        participant = self.participants[participant_id]
        sequence = []
        
        for reminder in self.reminder_schedule:
            # Personalize the reminder
            personalized_reminder = {
                "participant_id": participant_id,
                "organization": participant["organization"],
                "trigger_date": reminder["trigger_date"],
                "template_name": reminder["template"],
                "subject": reminder["subject"],
                "priority": reminder["priority"],
                "personalized_content": self._personalize_template(
                    reminder["template"], 
                    participant
                )
            }
            sequence.append(personalized_reminder)
        
        return sequence
    
    def generate_followup_sequence(self, participant_id: str) -> List[Dict[str, Any]]:
        """
        Generate personalized follow-up sequence for participant
        """
        if participant_id not in self.participants:
            return []
        
        participant = self.participants[participant_id]
        sequence = []
        
        for followup in self.followup_schedule:
            # Personalize the follow-up
            personalized_followup = {
                "participant_id": participant_id,
                "organization": participant["organization"],
                "trigger_date": followup["trigger_date"],
                "template_name": followup["template"],
                "subject": followup["subject"],
                "priority": followup["priority"],
                "personalized_content": self._personalize_template(
                    followup["template"],
                    participant
                )
            }
            sequence.append(personalized_followup)
        
        return sequence
    
    def _personalize_template(self, template_name: str, participant: Dict[str, Any]) -> str:
        """
        Personalize email template for specific participant
        """
        if template_name not in self.email_templates:
            return ""
        
        template = self.email_templates[template_name]["body"]
        
        # Basic personalization
        template = template.replace("{contact_name}", participant["contact_name"])
        template = template.replace("{organization}", participant["organization"])
        template = template.replace("{session}", participant["session"])
        template = template.replace("{session_time}", participant["session_time"])
        template = template.replace("{session_url}", participant["session_url"])
        
        # Customization-specific content
        customization_map = {
            "clinical_workflow": {
                "customization_focus": "clinical workflow optimization",
                "application_area": "patient care",
                "customization_point_1": "EEG processing in clinical settings",
                "customization_point_2": "Patient workflow integration",
                "customization_point_3": "Clinical decision support"
            },
            "research_integration": {
                "customization_focus": "research and data integration",
                "application_area": "research operations", 
                "customization_point_1": "Multi-site research collaboration",
                "customization_point_2": "Advanced data analytics",
                "customization_point_3": "Research workflow automation"
            },
            "enterprise_partnership": {
                "customization_focus": "enterprise capabilities and partnership",
                "application_area": "enterprise operations",
                "customization_point_1": "Scalable enterprise deployment",
                "customization_point_2": "Partnership integration opportunities", 
                "customization_point_3": "Enterprise security and compliance"
            }
        }
        
        customization = participant.get("customization", "clinical_workflow")
        if customization in customization_map:
            for key, value in customization_map[customization].items():
                template = template.replace("{" + key + "}", value)
        
        return template
    
    def export_automation_sequences(self) -> None:
        """
        Export all automation sequences to files
        """
        all_sequences = {}
        
        for participant_id in self.participants.keys():
            all_sequences[participant_id] = {
                "reminders": self.generate_reminder_sequence(participant_id),
                "followups": self.generate_followup_sequence(participant_id)
            }
        
        # Save sequences
        sequences_file = os.path.join(AUTOMATION_DIR, "automation_sequences.json")
        with open(sequences_file, 'w') as f:
            json.dump(all_sequences, f, indent=2)
        
        # Save templates
        templates_file = os.path.join(TEMPLATES_DIR, "email_templates.json")
        with open(templates_file, 'w') as f:
            json.dump(self.email_templates, f, indent=2)
        
        logging.info(f"Automation sequences exported to: {sequences_file}")
        logging.info(f"Email templates saved to: {templates_file}")
    
    def generate_automation_summary(self) -> None:
        """
        Generate comprehensive automation summary
        """
        print("\n" + "="*80)
        print("🤖 L.I.F.E. PLATFORM - AUTOMATED REMINDER & FOLLOW-UP SYSTEM")
        print("="*80)
        print(f"📅 Setup Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🎪 Demo Date: October 15, 2025")
        print(f"⏰ Days to Demo: {(self.demo_date - datetime.now()).days}")
        
        print(f"\n📧 REMINDER SCHEDULE:")
        for i, reminder in enumerate(self.reminder_schedule, 1):
            print(f"   {i}. {reminder['name']}")
            print(f"      📅 Date: {reminder['trigger_date']}")
            print(f"      📝 Template: {reminder['template']}")
            print(f"      🎯 Priority: {reminder['priority']}")
            print(f"      📎 Includes: {', '.join(reminder['includes'])}")
        
        print(f"\n🔄 FOLLOW-UP SCHEDULE:")
        for i, followup in enumerate(self.followup_schedule, 1):
            print(f"   {i}. {followup['name']}")
            print(f"      📅 Date: {followup['trigger_date']}")
            print(f"      📝 Template: {followup['template']}")
            print(f"      🎯 Priority: {followup['priority']}")
            print(f"      📎 Includes: {', '.join(followup['includes'])}")
        
        print(f"\n👥 PARTICIPANT AUTOMATION:")
        for participant_id, participant in self.participants.items():
            print(f"   {participant['organization']}:")
            print(f"      📧 Email: {participant['email']}")
            print(f"      📅 Session: {participant['session']}")
            print(f"      🎯 Priority: {participant['priority']}")
            print(f"      🛠 Customization: {participant['customization']}")
            
            # Show next reminder
            reminders = self.generate_reminder_sequence(participant_id)
            next_reminder = next((r for r in reminders if r['trigger_date'] >= datetime.now().date().isoformat()), None)
            if next_reminder:
                print(f"      📨 Next: {next_reminder['template_name']} on {next_reminder['trigger_date']}")
        
        print(f"\n📄 EMAIL TEMPLATES ({len(self.email_templates)}):")
        for template_name, template_data in self.email_templates.items():
            print(f"   📧 {template_name}")
            print(f"      📝 Subject: {template_data['subject'][:50]}...")
            print(f"      📎 Attachments: {len(template_data.get('attachments', []))}")
        
        print(f"\n📁 AUTOMATION FILES:")
        print(f"   🤖 Sequences: automation_system/automation_sequences.json")
        print(f"   📧 Templates: automation_system/email_templates/")
        print(f"   📊 Logs: logs/automation_reminder_system.log")
        
        print(f"\n🚀 AUTOMATION STATUS:")
        print(f"   ✅ {len(self.participants)} participants configured")
        print(f"   ✅ {len(self.reminder_schedule)} reminder stages")
        print(f"   ✅ {len(self.followup_schedule)} follow-up stages")
        print(f"   ✅ {len(self.email_templates)} email templates")
        print(f"   ✅ All sequences personalized and ready")

def main():
    """
    Main automation system execution
    """
    print("🤖 Initializing L.I.F.E. Platform Automated Reminder System...")
    
    # Create automation system
    automation = AutomatedReminderSystem()
    
    # Export sequences and templates
    automation.export_automation_sequences()
    
    # Generate summary
    automation.generate_automation_summary()
    
    print("\n🎉 Automated Reminder & Follow-up System Complete!")
    print("📨 All email sequences configured and personalized.")
    print("🔄 Pre-demo and post-demo automation ready.")

if __name__ == "__main__":
    main()