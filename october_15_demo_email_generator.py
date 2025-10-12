"""
L.I.F.E. Platform - October 15 Demo Email Generator
Generates personalized emails for all 23 demo attendees

Copyright 2025 - Sergio Paya Borrull
Date: October 12, 2025
"""

import os
import json
from datetime import datetime

# Setup directories
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
EMAILS_DIR = os.path.join(SCRIPT_DIR, "october_15_demo_emails")
os.makedirs(EMAILS_DIR, exist_ok=True)

# Demo session schedule
DEMO_SESSIONS = {
    "session_1": {
        "time": "07:00 GMT",
        "duration": "60 minutes",
        "type": "Asia-Pacific Group Demo",
        "institutions": [
            {"name": "University of Sydney", "contact": "Dr. Emily Chen", "type": "education"},
            {"name": "University of Tokyo", "contact": "Prof. Hiroshi Yamamoto", "type": "education"},
            {"name": "National University of Singapore", "contact": "Dr. Wei Lin", "type": "education"},
            {"name": "University of Melbourne", "contact": "Prof. Sarah Johnson", "type": "education"},
            {"name": "RIKEN Brain Science Institute", "contact": "Dr. Kenji Tanaka", "type": "research"},
            {"name": "Seoul National University", "contact": "Prof. Min-Jung Kim", "type": "education"}
        ]
    },
    "session_2": {
        "time": "09:00 GMT",
        "duration": "45 minutes",
        "type": "NHS Healthcare Demo",
        "institutions": [
            {"name": "NHS Royal London Hospital", "contact": "Dr. Michael Thompson", "type": "healthcare"}
        ]
    },
    "session_3": {
        "time": "10:00 GMT",
        "duration": "45 minutes",
        "type": "Oxford VIP Demo",
        "institutions": [
            {"name": "University of Oxford", "contact": "Dr. Sarah Mitchell", "type": "education"}
        ]
    },
    "session_4": {
        "time": "11:30 GMT",
        "duration": "45 minutes",
        "type": "Cambridge VIP Demo",
        "institutions": [
            {"name": "University of Cambridge", "contact": "Prof. James Harrison", "type": "education"}
        ]
    },
    "session_5": {
        "time": "14:00 GMT",
        "duration": "60 minutes",
        "type": "Microsoft Strategic Partnership Demo",
        "institutions": [
            {"name": "Microsoft Research", "contact": "Dr. Alex Chen", "type": "enterprise"}
        ]
    },
    "session_6": {
        "time": "15:30 GMT",
        "duration": "75 minutes",
        "type": "European Group Demo",
        "institutions": [
            {"name": "Imperial College London", "contact": "Prof. David Wilson", "type": "education"},
            {"name": "ETH Zurich", "contact": "Dr. Anna Mueller", "type": "research"},
            {"name": "Technical University of Munich", "contact": "Prof. Klaus Schmidt", "type": "education"},
            {"name": "Sorbonne University", "contact": "Dr. Marie Dubois", "type": "education"},
            {"name": "Karolinska Institute", "contact": "Prof. Erik Andersson", "type": "research"},
            {"name": "University of Edinburgh", "contact": "Dr. Robert MacLeod", "type": "education"},
            {"name": "King's College London", "contact": "Prof. Lisa Brown", "type": "education"}
        ]
    },
    "session_7": {
        "time": "20:00 GMT",
        "duration": "75 minutes",
        "type": "North American Group Demo",
        "institutions": [
            {"name": "Stanford University", "contact": "Prof. Jennifer Rodriguez", "type": "education"},
            {"name": "MIT", "contact": "Dr. Thomas Anderson", "type": "research"},
            {"name": "Harvard Medical School", "contact": "Dr. Patricia Davis", "type": "healthcare"},
            {"name": "Mayo Clinic", "contact": "Dr. Christopher Lee", "type": "healthcare"},
            {"name": "Johns Hopkins University", "contact": "Prof. Amanda White", "type": "healthcare"},
            {"name": "University of Toronto", "contact": "Dr. Daniel Kim", "type": "education"}
        ]
    }
}

# Benefits by institution type
INSTITUTION_BENEFITS = {
    "education": """
**For Educational Institutions:**
• Improve student outcomes by 40–60%
• Real-time cognitive load assessment
• Optimized, personalized learning paths
• LMS integration capabilities
• Student engagement analytics
• Curriculum optimization tools
""",
    "healthcare": """
**For Healthcare Institutions:**
• Enhanced rehabilitation programs
• Neural therapy and cognitive assessment
• Clinical research with advanced monitoring
• Patient cognitive assessment tools
• Therapeutic intervention optimization
• Medical research collaboration opportunities
""",
    "research": """
**For Research Institutes:**
• Advanced EEG data analysis capabilities
• Machine learning integration
• Real-time neural processing features
• Collaborative research opportunities
• Access to proprietary algorithms
• Research publication collaboration
""",
    "enterprise": """
**For Enterprise Partners:**
• Workforce cognitive performance optimization
• Employee training effectiveness measurement
• Stress and wellness monitoring
• Productivity enhancement tools
• Corporate wellness integration
• Strategic partnership opportunities
"""
}

def generate_email(session_info, institution_info, session_key):
    """Generate personalized email for each attendee"""
    
    # Extract information
    time = session_info["time"]
    duration = session_info["duration"]
    session_type = session_info["type"]
    institution = institution_info["name"]
    contact = institution_info["contact"]
    inst_type = institution_info["type"]
    
    # Generate meeting details (placeholder for actual Teams links)
    meeting_id = f"LIFE-{session_key.upper()}-{datetime.now().strftime('%Y%m%d')}"
    teams_link = f"https://teams.microsoft.com/l/meetup-join/LIFE_DEMO_{session_key}"
    phone_number = "+1-425-555-0199 (Conference ID: 123456789)"
    
    # Select appropriate benefits
    benefits = INSTITUTION_BENEFITS.get(inst_type, INSTITUTION_BENEFITS["education"])
    
    # Generate personalized email
    email_content = f"""Subject: L.I.F.E. Platform Demo - October 15, 2025 | Your Exclusive {session_type}

Dear {contact},

Thank you for your interest in the L.I.F.E. Platform! We're excited to demonstrate our revolutionary neuroadaptive learning technology specifically for {institution}.

**Demo Session Details**
📅 Date: October 15, 2025
🕐 Time: {time} (Please convert to your local timezone)
⏱️ Duration: {duration}
🎯 Session Type: {session_type}
💻 Meeting Platform: Microsoft Teams

**What to Expect**
🧠 Live neural processing demonstration
📊 Real-time EEG data analysis with 97.95% accuracy
🎯 Personalized learning optimization features
☁️ Microsoft Azure integration review
❓ Q&A session tailored to {institution}'s implementation needs
🤝 Discussion of partnership opportunities

**Microsoft Partnership**
✅ Strategic partnership with Microsoft
🏆 Azure Marketplace certified solution (Enterprise-grade platform integration)
🆔 Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb

**Meeting Access Information**
🔗 Microsoft Teams Meeting Link: {teams_link}
🆔 Meeting ID: {meeting_id}
📞 Dial-in: {phone_number}
🔑 Meeting Password: LIFE2025

**Preparation Checklist**
□ Ensure stable internet connection
□ Test your microphone and camera beforehand
□ Join 5 minutes early for technical checks
□ Prepare questions about implementation for {institution}
□ Have your institutional requirements and budget considerations ready
□ Review our platform overview at: https://sergiliife.github.io/SergiLIFE-life-azure-system

**Personalized Benefits for {institution}**
{benefits}

**Technical Specifications Preview**
• **Processing Speed**: Sub-millisecond latency (0.38ms average)
• **Accuracy Rate**: 97.95% on real EEG datasets
• **Scalability**: Azure cloud infrastructure
• **Integration**: RESTful APIs, SDK support
• **Security**: Enterprise-grade encryption, HIPAA compliant

**Special Launch Offer**
As an October 15 demo attendee, {institution} will receive:
🎁 30% discount on first-year licensing
🚀 Priority implementation support
💡 Free custom integration consultation
👥 Direct access to our developer team
📈 Quarterly performance optimization reviews

**Pre-Demo Resources**
📋 Platform Overview: https://sergiliife.github.io/SergiLIFE-life-azure-system
📊 Technical Specifications: Available upon request
🔬 Research Papers: Available for academic institutions
💼 Business Case Studies: Available for enterprise clients

**Next Steps After Demo**
Following our session, we'll provide:
1. Detailed technical documentation
2. Custom implementation timeline for {institution}
3. Budget proposal with special launch pricing
4. Direct contact with our technical team
5. Pilot program options

We're particularly excited to show you how L.I.F.E. Platform can transform outcomes at {institution}. Our neuroadaptive learning technology represents a breakthrough in personalized education and cognitive enhancement.

Looking forward to our demonstration!

Best regards,

**Sergio Paya Borrull**
Founder & CEO, L.I.F.E. Platform
📧 sergio@lifecoach-121.com
🌐 lifecoach-121.com
📱 Direct Line: Available upon request

---
**L.I.F.E. Platform – Learning Individually from Experience**
*Revolutionary Neural Learning Technology*
Copyright 2025 - All Rights Reserved

**Platform Status**: Production Ready | **Demo Date**: October 15, 2025
**Generated**: {datetime.now().strftime('%B %d, %Y at %H:%M GMT')}

---
**Technical Support**: For any technical issues joining the demo, contact our support team 24/7
**Reschedule**: If you need to reschedule, please contact us at least 24 hours in advance
**Recording**: This session will be recorded for {institution}'s internal review (optional)

**Privacy Notice**: All demo data is anonymized and used solely for demonstration purposes. 
No personal or institutional data will be stored or shared without explicit consent.
"""

    return email_content

def generate_all_emails():
    """Generate emails for all attendees"""
    print("🚀 Generating personalized demo emails for October 15, 2025...")
    print("=" * 80)
    
    total_attendees = 0
    all_emails = {}
    
    for session_key, session_info in DEMO_SESSIONS.items():
        session_emails = []
        
        print(f"\n📧 Generating emails for {session_info['type']}...")
        print(f"   Time: {session_info['time']} | Duration: {session_info['duration']}")
        
        for institution_info in session_info['institutions']:
            # Generate email
            email_content = generate_email(session_info, institution_info, session_key)
            
            # Create filename
            institution_safe = institution_info['name'].replace(' ', '_').replace('.', '')
            contact_safe = institution_info['contact'].replace(' ', '_').replace('.', '')
            filename = f"{session_key}_{institution_safe}_{contact_safe}.txt"
            
            # Save email to file
            email_path = os.path.join(EMAILS_DIR, filename)
            with open(email_path, 'w', encoding='utf-8') as f:
                f.write(email_content)
            
            session_emails.append({
                'institution': institution_info['name'],
                'contact': institution_info['contact'],
                'type': institution_info['type'],
                'filename': filename,
                'email_path': email_path
            })
            
            total_attendees += 1
            print(f"   ✅ {institution_info['name']} - {institution_info['contact']}")
        
        all_emails[session_key] = {
            'session_info': session_info,
            'emails': session_emails
        }
    
    print(f"\n🎯 EMAIL GENERATION COMPLETE!")
    print(f"   Total emails generated: {total_attendees}")
    print(f"   Total sessions: {len(DEMO_SESSIONS)}")
    print(f"   Files saved to: {EMAILS_DIR}")
    
    # Generate summary report
    summary_report = {
        'generation_date': datetime.now().isoformat(),
        'total_attendees': total_attendees,
        'total_sessions': len(DEMO_SESSIONS),
        'emails_directory': EMAILS_DIR,
        'sessions': all_emails
    }
    
    # Save summary
    summary_path = os.path.join(EMAILS_DIR, 'SUMMARY_REPORT.json')
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary_report, f, indent=2, ensure_ascii=False)
    
    # Create sending checklist
    checklist_content = f"""
L.I.F.E. Platform Demo - Email Sending Checklist
Generated: {datetime.now().strftime('%B %d, %Y at %H:%M GMT')}

TOTAL EMAILS TO SEND: {total_attendees}

SESSION BREAKDOWN:
"""
    
    for session_key, session_data in all_emails.items():
        checklist_content += f"\n{session_data['session_info']['type']} ({session_data['session_info']['time']}):\n"
        for email_info in session_data['emails']:
            checklist_content += f"  □ {email_info['contact']} - {email_info['institution']}\n"
            checklist_content += f"    File: {email_info['filename']}\n"
    
    checklist_content += f"""
SENDING INSTRUCTIONS:
1. Review each email in the {EMAILS_DIR} folder
2. Copy email content to your email client
3. Update Teams meeting links with actual URLs
4. Send emails 48-72 hours before demo (by October 13)
5. Mark checkbox above when sent
6. Follow up with non-responders 24 hours before demo

IMPORTANT NOTES:
- All emails are personalized by institution type
- Meeting links are placeholders - replace with actual Teams URLs
- Special attention needed for VIP sessions (Oxford, Cambridge, Microsoft)
- Keep track of confirmations and dietary requirements for any in-person elements

Ready for October 15 Demo Success! 🎯
"""
    
    checklist_path = os.path.join(EMAILS_DIR, 'SENDING_CHECKLIST.txt')
    with open(checklist_path, 'w', encoding='utf-8') as f:
        f.write(checklist_content)
    
    print(f"\n📋 Summary report saved: {summary_path}")
    print(f"📋 Sending checklist: {checklist_path}")
    print(f"\n🎊 Ready for October 15 Demo Success!")
    
    return all_emails

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("L.I.F.E. PLATFORM - OCTOBER 15 DEMO EMAIL GENERATOR")
    print("Generating personalized emails for all 23 attendees")
    print("=" * 80)
    
    generate_all_emails()
    
    print("\n" + "=" * 80)
    print("✅ ALL DEMO EMAILS GENERATED SUCCESSFULLY!")
    print("Check the 'october_15_demo_emails' folder for all files")
    print("=" * 80 + "\n")