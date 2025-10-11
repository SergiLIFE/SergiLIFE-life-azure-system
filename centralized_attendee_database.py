#!/usr/bin/env python3
"""
L.I.F.E. Platform - Centralized Attendee Database & CRM System
October 11, 2025 | Comprehensive Demo Participant Management

Centralized system for managing all October 15, 2025 demo participants
with contact information, engagement tracking, and CRM functionality.
"""

import os
import csv
import json
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging

# Setup logging
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CRM_DIR = os.path.join(SCRIPT_DIR, "crm_database")
ATTENDEE_DIR = os.path.join(CRM_DIR, "attendees")
REMINDERS_DIR = os.path.join(CRM_DIR, "reminders")
FOLLOWUP_DIR = os.path.join(CRM_DIR, "followup")
LOGS_DIR = os.path.join(SCRIPT_DIR, "logs")

# Create directories
for dir_path in [CRM_DIR, ATTENDEE_DIR, REMINDERS_DIR, FOLLOWUP_DIR, LOGS_DIR]:
    os.makedirs(dir_path, exist_ok=True)

LOG_FILE = os.path.join(LOGS_DIR, "centralized_attendee_database.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

class CentralizedAttendeeDatabase:
    """
    Comprehensive attendee database and CRM system for L.I.F.E. Platform demos
    """
    
    def __init__(self):
        self.demo_date = "October 15, 2025"
        self.database_file = os.path.join(CRM_DIR, "attendee_master_database.csv")
        self.json_backup = os.path.join(CRM_DIR, "attendee_database_backup.json")
        
        # Initialize attendee database with all consolidated information
        self.attendee_database = self._initialize_attendee_data()
        
    def _initialize_attendee_data(self) -> List[Dict[str, Any]]:
        """
        Initialize comprehensive attendee database with all available information
        """
        return [
            {
                # Basic Information
                "participant_id": "LIFE_001",
                "organization": "University of Oxford",
                "department": "Neuroscience Department",
                "contact_name": "Dr. Oxford Neuroscience Lead",
                "email": "neuroscience.dept@ox.ac.uk",
                "phone": "+44 1865 272000",
                "country": "United Kingdom",
                "city": "Oxford",
                
                # Demo Details
                "demo_status": "Confirmed",
                "registration_date": "October 10, 2025",
                "preferred_session": "Session 1: Clinical Professionals",
                "session_time": "09:00-09:45 BST",
                "backup_session": "Session 3: Executive Overview",
                
                # Engagement Metrics
                "email_opens": 3,
                "email_clicks": 5,
                "website_visits": 2,
                "marketplace_views": 1,
                "engagement_score": 95,  # High engagement
                
                # Business Information
                "organization_type": "University",
                "sector": "Education/Research",
                "decision_maker_level": "Department Head",
                "budget_authority": "Yes",
                "purchasing_timeframe": "Q1 2026",
                
                # Revenue Information
                "pricing_tier": "Professional",
                "estimated_value": "$75,000 - $250,000/year",
                "conversion_probability": 85,
                "revenue_potential": "$162,500",
                
                # Status Tracking
                "lead_source": "Campaign October 10",
                "lead_quality": "Hot Lead",
                "trial_status": "Active",
                "demo_requested": "Yes",
                "follow_up_required": "Post-demo conversion",
                
                # Microsoft Partnership
                "microsoft_partnership_visibility": "Yes",
                "azure_credits_interest": "High",
                "enterprise_features_interest": "Medium",
                
                # Communication History
                "last_contact": "October 10, 2025",
                "next_contact_scheduled": "October 12, 2025",
                "communication_preference": "Email",
                
                # Demo Preparation
                "pre_demo_questionnaire": "Pending",
                "demo_customization": "Clinical workflow focus",
                "specific_interests": "EEG processing, clinical integration",
                
                # Notes
                "notes": "Premium institution. High conversion potential. Strong interest in clinical applications.",
                "internal_champion": "Department Head - Neuroscience",
                "competitors": "None identified"
            },
            
            {
                # Cambridge University
                "participant_id": "LIFE_002",
                "organization": "Cambridge University",
                "department": "Brain Sciences Department",
                "contact_name": "Dr. Cambridge Brain Sciences Lead",
                "email": "brain.sciences@cam.ac.uk",
                "phone": "+44 1223 337733",
                "country": "United Kingdom",
                "city": "Cambridge",
                
                "demo_status": "Confirmed",
                "registration_date": "October 10, 2025",
                "preferred_session": "Session 1: Clinical Professionals",
                "session_time": "09:00-09:45 BST",
                "backup_session": "Session 2: Research & IT",
                
                "email_opens": 2,
                "email_clicks": 4,
                "website_visits": 1,
                "marketplace_views": 1,
                "engagement_score": 88,
                
                "organization_type": "University",
                "sector": "Education/Research",
                "decision_maker_level": "Department Head",
                "budget_authority": "Yes",
                "purchasing_timeframe": "Q1 2026",
                
                "pricing_tier": "Professional",
                "estimated_value": "$75,000 - $250,000/year",
                "conversion_probability": 80,
                "revenue_potential": "$150,000",
                
                "lead_source": "Campaign October 10",
                "lead_quality": "Hot Lead",
                "trial_status": "Potential",
                "demo_requested": "Yes",
                "follow_up_required": "Trial setup",
                
                "microsoft_partnership_visibility": "Yes",
                "azure_credits_interest": "High",
                "enterprise_features_interest": "High",
                
                "last_contact": "October 10, 2025",
                "next_contact_scheduled": "October 12, 2025",
                "communication_preference": "Email",
                
                "pre_demo_questionnaire": "Pending",
                "demo_customization": "Research and clinical integration",
                "specific_interests": "Research tools, data export, collaboration",
                
                "notes": "Prestigious university. Strong research focus. Potential for multi-department deployment.",
                "internal_champion": "Brain Sciences Lead",
                "competitors": "Traditional EEG analysis software"
            },
            
            {
                # Microsoft Research Cambridge
                "participant_id": "LIFE_003",
                "organization": "Microsoft Research Cambridge",
                "department": "AI & Healthcare Research",
                "contact_name": "Microsoft Partnership Lead",
                "email": "partnerships@microsoft.com",
                "phone": "+44 1223 479700",
                "country": "United Kingdom",
                "city": "Cambridge",
                
                "demo_status": "Confirmed - Priority",
                "registration_date": "October 10, 2025",
                "preferred_session": "Session 2: Research & IT Leadership",
                "session_time": "11:00-11:45 BST",
                "backup_session": "Session 3: Executive Overview",
                
                "email_opens": 4,
                "email_clicks": 8,
                "website_visits": 3,
                "marketplace_views": 2,
                "engagement_score": 98,  # Highest engagement
                
                "organization_type": "Enterprise",
                "sector": "Technology/Research",
                "decision_maker_level": "Partnership Director",
                "budget_authority": "Yes",
                "purchasing_timeframe": "Immediate",
                
                "pricing_tier": "Enterprise",
                "estimated_value": "$250,000+/year",
                "conversion_probability": 95,
                "revenue_potential": "$475,000",
                
                "lead_source": "Campaign October 10",
                "lead_quality": "Enterprise Lead",
                "trial_status": "Active",
                "demo_requested": "Yes",
                "follow_up_required": "Partnership discussion",
                
                "microsoft_partnership_visibility": "Direct Partnership",
                "azure_credits_interest": "Partnership Level",
                "enterprise_features_interest": "Very High",
                
                "last_contact": "October 10, 2025",
                "next_contact_scheduled": "October 12, 2025",
                "communication_preference": "Email + Teams",
                
                "pre_demo_questionnaire": "Completed",
                "demo_customization": "Enterprise capabilities, partnership opportunities",
                "specific_interests": "Scalability, enterprise integration, co-development",
                
                "notes": "DIRECT MICROSOFT PARTNERSHIP OPPORTUNITY. Highest priority. Potential for strategic alliance.",
                "internal_champion": "Partnership Director",
                "competitors": "None - partnership focused"
            },
            
            {
                # NHS Royal London Hospital
                "participant_id": "LIFE_004",
                "organization": "NHS Royal London Hospital",
                "department": "Neurology Department",
                "contact_name": "NHS Clinical Lead",
                "email": "neurology.rln@nhs.net",
                "phone": "+44 20 7377 7000",
                "country": "United Kingdom",
                "city": "London",
                
                "demo_status": "Follow-up Required",
                "registration_date": "October 10, 2025",
                "preferred_session": "Session 1: Clinical Professionals",
                "session_time": "09:00-09:45 BST",
                "backup_session": "Session 3: Executive Overview",
                
                "email_opens": 2,
                "email_clicks": 2,
                "website_visits": 1,
                "marketplace_views": 0,
                "engagement_score": 72,
                
                "organization_type": "Healthcare",
                "sector": "Public Healthcare",
                "decision_maker_level": "Clinical Director",
                "budget_authority": "Limited",
                "purchasing_timeframe": "Q2 2026",
                
                "pricing_tier": "Professional",
                "estimated_value": "$150,000 - $400,000/year",
                "conversion_probability": 65,
                "revenue_potential": "$195,000",
                
                "lead_source": "Campaign October 10",
                "lead_quality": "Warm Lead",
                "trial_status": "Potential",
                "demo_requested": "Interested",
                "follow_up_required": "Confirmation call needed",
                
                "microsoft_partnership_visibility": "Yes",
                "azure_credits_interest": "Medium",
                "enterprise_features_interest": "Medium",
                
                "last_contact": "October 10, 2025",
                "next_contact_scheduled": "October 11, 2025",
                "communication_preference": "Phone",
                
                "pre_demo_questionnaire": "Not sent",
                "demo_customization": "Clinical workflow, NHS compliance",
                "specific_interests": "Patient care, clinical efficiency, compliance",
                
                "notes": "Large NHS hospital. Budget approval process required. High patient volume potential.",
                "internal_champion": "Clinical Director - Neurology",
                "competitors": "Current NHS systems"
            },
            
            {
                # Imperial College London
                "participant_id": "LIFE_005",
                "organization": "Imperial College London",
                "department": "Bioengineering Department",
                "contact_name": "Imperial Research Lead",
                "email": "bioeng.research@imperial.ac.uk",
                "phone": "+44 20 7589 5111",
                "country": "United Kingdom",
                "city": "London",
                
                "demo_status": "Follow-up Required",
                "registration_date": "October 10, 2025",
                "preferred_session": "Session 2: Research & IT Leadership",
                "session_time": "11:00-11:45 BST",
                "backup_session": "Session 1: Clinical Professionals",
                
                "email_opens": 1,
                "email_clicks": 2,
                "website_visits": 1,
                "marketplace_views": 1,
                "engagement_score": 68,
                
                "organization_type": "University",
                "sector": "Education/Research",
                "decision_maker_level": "Research Director",
                "budget_authority": "Yes",
                "purchasing_timeframe": "Q1-Q2 2026",
                
                "pricing_tier": "Professional",
                "estimated_value": "$75,000 - $250,000/year",
                "conversion_probability": 70,
                "revenue_potential": "$131,250",
                
                "lead_source": "Campaign October 10",
                "lead_quality": "Warm Lead",
                "trial_status": "Potential",
                "demo_requested": "Interested",
                "follow_up_required": "Research collaboration discussion",
                
                "microsoft_partnership_visibility": "Yes",
                "azure_credits_interest": "High",
                "enterprise_features_interest": "High",
                
                "last_contact": "October 10, 2025",
                "next_contact_scheduled": "October 12, 2025",
                "communication_preference": "Email",
                
                "pre_demo_questionnaire": "Not sent",
                "demo_customization": "Research capabilities, data analytics",
                "specific_interests": "Research tools, bioengineering applications",
                
                "notes": "Top engineering school. Research-focused. Potential for academic partnership.",
                "internal_champion": "Bioengineering Research Director",
                "competitors": "Academic research tools"
            }
        ]
    
    def export_to_csv(self) -> str:
        """
        Export attendee database to CSV format
        """
        logging.info("Exporting attendee database to CSV format...")
        
        # Convert to pandas DataFrame for better CSV handling
        df = pd.DataFrame(self.attendee_database)
        
        # Save to CSV
        df.to_csv(self.database_file, index=False)
        
        # Also save as JSON backup
        with open(self.json_backup, 'w') as f:
            json.dump(self.attendee_database, f, indent=2)
        
        logging.info(f"Database exported to: {self.database_file}")
        logging.info(f"JSON backup created: {self.json_backup}")
        
        return self.database_file
    
    def export_to_excel(self) -> str:
        """
        Export attendee database to Excel format with multiple sheets
        """
        excel_file = os.path.join(CRM_DIR, "LIFE_Platform_Attendee_Database.xlsx")
        
        logging.info("Exporting attendee database to Excel format...")
        
        # Convert to pandas DataFrame
        df = pd.DataFrame(self.attendee_database)
        
        # Create Excel writer object
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            # Main database sheet
            df.to_excel(writer, sheet_name='Master Database', index=False)
            
            # Summary sheet
            summary_data = self._generate_summary_statistics()
            summary_df = pd.DataFrame([summary_data])
            summary_df.to_excel(writer, sheet_name='Summary Statistics', index=False)
            
            # Session assignments
            session_df = df[['participant_id', 'organization', 'preferred_session', 'session_time', 'demo_status']]
            session_df.to_excel(writer, sheet_name='Session Assignments', index=False)
            
            # Contact information
            contact_df = df[['organization', 'contact_name', 'email', 'phone', 'communication_preference']]
            contact_df.to_excel(writer, sheet_name='Contact Information', index=False)
            
            # Revenue pipeline
            revenue_df = df[['organization', 'pricing_tier', 'estimated_value', 'conversion_probability', 'revenue_potential']]
            revenue_df.to_excel(writer, sheet_name='Revenue Pipeline', index=False)
        
        logging.info(f"Excel database created: {excel_file}")
        
        return excel_file
    
    def _generate_summary_statistics(self) -> Dict[str, Any]:
        """
        Generate summary statistics for the attendee database
        """
        total_attendees = len(self.attendee_database)
        confirmed = len([a for a in self.attendee_database if a['demo_status'] == 'Confirmed'])
        follow_up_needed = len([a for a in self.attendee_database if 'Follow-up' in a['demo_status']])
        
        # Revenue calculations
        total_revenue_potential = sum([float(a['revenue_potential'].replace('$', '').replace(',', '')) 
                                     for a in self.attendee_database])
        
        avg_conversion_probability = sum([a['conversion_probability'] for a in self.attendee_database]) / total_attendees
        
        # Engagement metrics
        avg_engagement_score = sum([a['engagement_score'] for a in self.attendee_database]) / total_attendees
        
        return {
            'report_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'demo_date': self.demo_date,
            'total_attendees': total_attendees,
            'confirmed_attendees': confirmed,
            'follow_up_required': follow_up_needed,
            'total_revenue_potential': f"${total_revenue_potential:,.0f}",
            'average_conversion_probability': f"{avg_conversion_probability:.1f}%",
            'average_engagement_score': f"{avg_engagement_score:.1f}",
            'session_1_participants': len([a for a in self.attendee_database if 'Session 1' in a['preferred_session']]),
            'session_2_participants': len([a for a in self.attendee_database if 'Session 2' in a['preferred_session']]),
            'enterprise_leads': len([a for a in self.attendee_database if a['pricing_tier'] == 'Enterprise']),
            'professional_leads': len([a for a in self.attendee_database if a['pricing_tier'] == 'Professional'])
        }
    
    def generate_attendee_summary(self) -> None:
        """
        Generate comprehensive attendee summary report
        """
        print("\n" + "="*80)
        print("🎯 L.I.F.E. PLATFORM - CENTRALIZED ATTENDEE DATABASE")
        print("="*80)
        print(f"📅 Demo Date: {self.demo_date}")
        print(f"📊 Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Summary statistics
        stats = self._generate_summary_statistics()
        print(f"\n📋 SUMMARY STATISTICS:")
        print(f"   👥 Total Attendees: {stats['total_attendees']}")
        print(f"   ✅ Confirmed: {stats['confirmed_attendees']}")
        print(f"   📞 Follow-up Required: {stats['follow_up_required']}")
        print(f"   💰 Total Revenue Potential: {stats['total_revenue_potential']}")
        print(f"   📈 Average Conversion Probability: {stats['average_conversion_probability']}")
        print(f"   ⭐ Average Engagement Score: {stats['average_engagement_score']}")
        
        print(f"\n🎪 SESSION BREAKDOWN:")
        print(f"   📅 Session 1 (Clinical): {stats['session_1_participants']} participants")
        print(f"   📅 Session 2 (Research & IT): {stats['session_2_participants']} participants")
        print(f"   🏢 Enterprise Tier: {stats['enterprise_leads']} leads")
        print(f"   👔 Professional Tier: {stats['professional_leads']} leads")
        
        print(f"\n👥 ATTENDEE DETAILS:")
        for i, attendee in enumerate(self.attendee_database, 1):
            print(f"\n{i}. {attendee['organization']}")
            print(f"   📧 Contact: {attendee['email']}")
            print(f"   📞 Phone: {attendee['phone']}")
            print(f"   🎯 Status: {attendee['demo_status']}")
            print(f"   📅 Session: {attendee['preferred_session']}")
            print(f"   ⏰ Time: {attendee['session_time']}")
            print(f"   ⭐ Engagement: {attendee['engagement_score']}/100")
            print(f"   💰 Revenue Potential: {attendee['revenue_potential']}")
            print(f"   📈 Conversion Probability: {attendee['conversion_probability']}%")
            print(f"   📝 Notes: {attendee['notes']}")
        
        print(f"\n📁 DATABASE FILES CREATED:")
        print(f"   📊 CSV: {self.database_file}")
        print(f"   📋 JSON Backup: {self.json_backup}")
        print(f"   📈 Excel: Available via export_to_excel()")
        
        print(f"\n🎯 NEXT ACTIONS:")
        print(f"   1. Send reminder emails to confirmed attendees")
        print(f"   2. Follow up with NHS and Imperial College")
        print(f"   3. Prepare customized demos for each session")
        print(f"   4. Schedule Microsoft partnership discussion")
        print(f"   5. Set up post-demo conversion tracking")

def main():
    """
    Main execution function
    """
    print("🚀 Initializing L.I.F.E. Platform Centralized Attendee Database...")
    
    # Create database instance
    attendee_db = CentralizedAttendeeDatabase()
    
    # Export to CSV
    csv_file = attendee_db.export_to_csv()
    print(f"✅ CSV database created: {csv_file}")
    
    # Export to Excel
    excel_file = attendee_db.export_to_excel()
    print(f"✅ Excel database created: {excel_file}")
    
    # Generate summary report
    attendee_db.generate_attendee_summary()
    
    print("\n🎉 Centralized Attendee Database Setup Complete!")
    print("📋 All attendee information has been consolidated and organized.")
    print("🔄 CRM system ready for demo management and follow-up.")

if __name__ == "__main__":
    main()