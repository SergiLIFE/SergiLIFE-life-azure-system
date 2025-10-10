"""
L.I.F.E. PLATFORM DEMO PREPARATION EMAIL TEMPLATE
For sending 24-hour reminder and preparation confirmation
"""

# 24-Hour Reminder Email Template
DEMO_REMINDER_EMAIL = """
Subject: Tomorrow's L.I.F.E. Platform Demo - Google Meet Link & Final Details

Dear [Prospect Name],

I'm excited about our L.I.F.E. Platform demonstration tomorrow, October 15th at [Time] Europe/Lisbon time zone.

🎯 **Demo Details:**
• Platform: Google Meet
• Link: https://meet.google.com/dkg-fyri-bvc
• Duration: 45 minutes
• Format: Live interactive demonstration

🚀 **What You'll See Tomorrow:**
• Real-time EEG data processing (880x faster than traditional methods)
• Live accuracy validation (95.8% on real datasets)  
• Sub-millisecond processing demonstration
• Custom ROI calculations for your organization
• Risk-free pilot program proposal

💡 **Prepare for Success:**
To maximize our time together, please have ready:
• Your current EEG analysis challenges and bottlenecks
• Volume of data you typically process
• Current processing times you experience
• Any specific use cases you'd like to see demonstrated

🎯 **Expected Outcome:**
By the end of our session, you'll have a clear path to implement L.I.F.E. Platform in your organization with a risk-free pilot program.

Technical requirements: Just a web browser - no downloads needed!

Looking forward to showing you how L.I.F.E. Platform can revolutionize your EEG analysis workflow.

Best regards,
Sergio Paya Borrull
Chief Technology Officer & Founder
L.I.F.E. Platform
Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb

P.S. - If you have any technical issues joining, please call me directly at [Your Phone Number]
"""

# Post-Demo Follow-Up Template  
POST_DEMO_FOLLOWUP = """
Subject: L.I.F.E. Platform Pilot Program - Next Steps [Action Required]

Dear [Prospect Name],

Thank you for the excellent demo session today! Your questions about [specific topics discussed] showed great insight into how L.I.F.E. Platform can transform your EEG analysis workflow.

🎯 **Key Results from Today's Demo:**
• Confirmed 880x performance improvement for your use case
• Validated 95.8% accuracy meets your requirements  
• Calculated ROI: [Specific ROI calculation]
• Implementation timeline: 2-week pilot program

📋 **Next Steps (Action Required):**

1. **Pilot Agreement** (attached)
   - Investment: $[Amount] for 2-week pilot
   - Risk-free guarantee: Full refund if not satisfied
   - Includes: Full platform access, training, and support

2. **Technical Requirements** 
   - Azure subscription (can use yours or ours)
   - EEG data samples for testing
   - 1 technical contact from your team

3. **Implementation Timeline**
   - Week 1: Platform setup and data integration
   - Week 2: Training and validation testing  
   - Week 3: Results evaluation and optimization

🚀 **Special Limited-Time Offer:**
As discussed, this pilot pricing is only available until October 20th. After that, our standard enterprise pricing applies.

💪 **Why Move Forward Now:**
• Production-ready platform (live on Azure Marketplace)
• Proven results on real datasets
• Direct CTO support (unique in the industry) 
• Risk-free guarantee removes all concerns
• Immediate competitive advantage

📞 **Ready to Proceed?**
Simply reply "YES - Let's start the pilot" and I'll send the technical setup details immediately.

Questions? Call me directly: [Your Phone Number]

Looking forward to revolutionizing your EEG analysis capabilities!

Best regards,
Sergio Paya Borrull
Chief Technology Officer & Founder  
L.I.F.E. Platform

---
Transform your EEG analysis: 880x faster, 95.8% accurate, risk-free guarantee
Azure Marketplace: 9a600d96-fe1e-420b-902a-a0c42c561adb
"""

# Emergency Backup Communication
TECHNICAL_ISSUES_EMAIL = """
Subject: L.I.F.E. Platform Demo - Alternative Options [Immediate Response]

Dear [Prospect Name],

I'm experiencing some technical difficulties with Google Meet for our scheduled L.I.F.E. Platform demonstration.

🔧 **Alternative Options (Choose One):**

1. **Phone + Screen Share**
   - Call: [Your Phone Number]
   - I'll share screen via alternative platform

2. **Reschedule for Later Today**  
   - Available: [Time slots]
   - Same Google Meet link once resolved

3. **Pre-Recorded Demo + Live Q&A**
   - I'll send high-quality demo recording
   - Follow with live discussion call

⚡ **Immediate Action:**
Please reply with your preference, and I'll implement immediately. Your time is valuable, and I want to ensure you see the full L.I.F.E. Platform capabilities.

📞 **Direct Contact:** [Your Phone Number]

The technology demonstration is too important to miss due to technical issues!

Apologies for the inconvenience,
Sergio Paya Borrull
Chief Technology Officer & Founder
L.I.F.E. Platform
"""

def print_email_templates():
    """Display all email templates for the demo"""
    print("="*80)
    print("📧 L.I.F.E. PLATFORM DEMO EMAIL TEMPLATES")
    print("="*80)
    
    print("\n1. 24-HOUR REMINDER EMAIL:")
    print("-" * 50)
    print(DEMO_REMINDER_EMAIL)
    
    print("\n2. POST-DEMO FOLLOW-UP EMAIL:")
    print("-" * 50)
    print(POST_DEMO_FOLLOWUP)
    
    print("\n3. TECHNICAL ISSUES BACKUP EMAIL:")
    print("-" * 50)
    print(TECHNICAL_ISSUES_EMAIL)
    
    print("\n" + "="*80)
    print("✅ All email templates ready for October 15th demo!")
    print("📅 Use these to maximize conversion success!")
    print("="*80)

if __name__ == "__main__":
    print_email_templates()