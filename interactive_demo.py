"""
L.I.F.E Platform Interactive Demo & Walkthrough
Shows how users interact with the neuroadaptive learning system
Windows-compatible version
"""

import os
import time
from datetime import datetime

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("ERROR: Pillow not installed!")
    print("Run: pip install Pillow")
    exit(1)


class LIFEInteractiveDemo:
    """Interactive demo showing user journey through L.I.F.E Platform"""

    def __init__(self):
        self.output_dir = "demo_assets"
        os.makedirs(self.output_dir, exist_ok=True)

    def print_header(self, title):
        """Print section header"""
        print("\n" + "=" * 70)
        print(f"  {title}")
        print("=" * 70 + "\n")

    def print_step(self, step_num, title, description):
        """Print step in journey"""
        print(f"\n{'─'*70}")
        print(f"STEP {step_num}: {title}")
        print(f"{'─'*70}")
        print(f"{description}\n")

    def create_interface_screenshot(self, interface_type, content):
        """Generate interface screenshot"""
        width, height = 1280, 720
        img = Image.new("RGB", (width, height), color="#F0F0F0")
        draw = ImageDraw.Draw(img)

        # Azure blue header
        draw.rectangle([(0, 0), (width, 80)], fill="#0078D4")

        # Try to use Arial, fallback to default
        try:
            header_font = ImageFont.truetype("arial.ttf", 32)
            title_font = ImageFont.truetype("arial.ttf", 24)
            text_font = ImageFont.truetype("arial.ttf", 18)
        except:
            header_font = ImageFont.load_default()
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()

        # Draw header text
        draw.text((40, 25), "L.I.F.E Platform", fill="white", font=header_font)

        # Draw content area
        content_y = 120
        for line in content:
            draw.text((40, content_y), line, fill="#333333", font=text_font)
            content_y += 35

        # Save screenshot
        filename = (
            f"interface_{interface_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        )
        filepath = os.path.join(self.output_dir, filename)
        img.save(filepath, "PNG", quality=95)

        return filepath

    def show_user_journey(self):
        """Complete user journey walkthrough"""

        self.print_header("🚀 L.I.F.E PLATFORM - USER INTERACTION GUIDE")

        print("This demo shows how different users interact with L.I.F.E Platform")
        print("from initial discovery through active learning sessions.\n")

        input("Press Enter to start the walkthrough... ")

        # STEP 1: Discovery
        self.print_step(
            1,
            "DISCOVERY - Azure Marketplace",
            "Users discover L.I.F.E Platform on Azure Marketplace\n"
            + "→ Search: 'neuroadaptive learning' or 'EEG learning platform'\n"
            + "→ See: 95.8% accuracy, 0.42ms latency, 880x faster\n"
            + "→ Read: Customer testimonials and performance benchmarks\n"
            + "→ Click: 'Get It Now' or 'Free Trial'",
        )

        screenshot1 = self.create_interface_screenshot(
            "marketplace",
            [
                "L.I.F.E Platform - Neuroadaptive Learning System",
                "",
                "✅ Real-time EEG Processing",
                "✅ 95.8% Accuracy | 0.42ms Latency",
                "✅ 880x Faster than Traditional Systems",
                "",
                "Starting at $15/user/month",
                "30-Day Free Trial Available",
                "",
                "[Get It Now]  [Free Trial]  [Contact Sales]",
            ],
        )
        print(f"✅ Generated: {screenshot1}")

        input("\nPress Enter to continue to Step 2... ")

        # STEP 2: Onboarding
        self.print_step(
            2,
            "ONBOARDING - Account Setup",
            "New users complete quick 5-minute setup:\n"
            + "→ Sign in with Azure AD / Microsoft account\n"
            + "→ Select organization type (Education, Healthcare, Enterprise)\n"
            + "→ Configure number of users\n"
            + "→ Choose subscription plan (Basic/Professional/Enterprise)\n"
            + "→ Auto-provisioning of Azure resources",
        )

        screenshot2 = self.create_interface_screenshot(
            "onboarding",
            [
                "Welcome to L.I.F.E Platform!",
                "",
                "Organization Setup:",
                "  • Organization Type: [Education v]",
                "  • Number of Users: [50________]",
                "  • Subscription: [Professional - $30/user/month v]",
                "",
                "Azure Integration:",
                "  ✅ Azure AD Connected",
                "  ✅ Storage Provisioned",
                "  ✅ Service Bus Configured",
                "",
                "[Complete Setup]",
            ],
        )
        print(f"✅ Generated: {screenshot2}")

        input("\nPress Enter to continue to Step 3... ")

        # STEP 3: Dashboard
        self.print_step(
            3,
            "MAIN DASHBOARD - System Overview",
            "Users land on personalized dashboard showing:\n"
            + "→ Active learning sessions and students\n"
            + "→ Real-time performance metrics\n"
            + "→ Recent insights and recommendations\n"
            + "→ Quick actions (Start Session, View Analytics, Settings)",
        )

        screenshot3 = self.create_interface_screenshot(
            "dashboard",
            [
                "Dashboard - Overview",
                "",
                "Active Sessions: 12        Students: 847",
                "Avg Accuracy: 94.2%       Processing Latency: 0.41ms",
                "",
                "Recent Activity:",
                "  • Student cohort 'Biology 101' - 89% learning efficiency",
                "  • Clinical trial 'Memory Training' - 95% engagement",
                "  • Enterprise training 'Safety Protocol' - 97% completion",
                "",
                "[Start New Session]  [View Analytics]  [Settings]",
            ],
        )
        print(f"✅ Generated: {screenshot3}")

        input("\nPress Enter to continue to Step 4... ")

        # STEP 4: EEG Setup
        self.print_step(
            4,
            "EEG DEVICE SETUP - Hardware Connection",
            "Instructors/clinicians connect EEG devices:\n"
            + "→ Supported devices: Emotiv, OpenBCI, NeuroSky, Research-grade\n"
            + "→ Bluetooth or USB connection\n"
            + "→ Auto-calibration and signal quality check\n"
            + "→ Channel mapping verification",
        )

        screenshot4 = self.create_interface_screenshot(
            "eeg_setup",
            [
                "EEG Device Configuration",
                "",
                "Device Status:",
                "  ✅ Emotiv Insight - Connected",
                "  ✅ Signal Quality: 95% (Excellent)",
                "  ✅ Channels: 5/5 Active",
                "  ✅ Battery: 87%",
                "",
                "Calibration:",
                "  Alpha (8-12Hz): ████████ 98%",
                "  Beta (12-30Hz): ████████ 96%",
                "  Theta (4-8Hz):  ████████ 94%",
                "",
                "[Start Calibration]  [Test Signal]  [Proceed to Session]",
            ],
        )
        print(f"✅ Generated: {screenshot4}")

        input("\nPress Enter to continue to Step 5... ")

        # STEP 5: Learning Session
        self.print_step(
            5,
            "ACTIVE LEARNING SESSION - Real-Time Adaptation",
            "During active learning session:\n"
            + "→ Real-time EEG data streaming (0.42ms latency)\n"
            + "→ Continuous attention and engagement monitoring\n"
            + "→ Dynamic content difficulty adjustment\n"
            + "→ Break recommendations when fatigue detected\n"
            + "→ Live performance metrics for instructor",
        )

        screenshot5 = self.create_interface_screenshot(
            "session",
            [
                "Active Learning Session - 'Advanced Mathematics'",
                "",
                "Student: John Smith        Duration: 23 minutes",
                "Attention Level: ████████░ 87%  (High)",
                "Learning Efficiency: 92%",
                "Engagement: Optimal",
                "",
                "Current Topic: Calculus - Derivatives",
                "Difficulty Level: Auto-adjusted to 'Advanced'",
                "",
                "Recommendations:",
                "  ✅ Student ready for advanced concepts",
                "  ⚠ Consider 5-min break in 12 minutes",
                "",
                "[Pause Session]  [View Details]  [End Session]",
            ],
        )
        print(f"✅ Generated: {screenshot5}")

        input("\nPress Enter to continue to Step 6... ")

        # STEP 6: Analytics
        self.print_step(
            6,
            "ANALYTICS & INSIGHTS - Performance Review",
            "After sessions, users access comprehensive analytics:\n"
            + "→ Individual student learning curves\n"
            + "→ Cohort performance comparison\n"
            + "→ Optimal learning time identification\n"
            + "→ Content effectiveness analysis\n"
            + "→ Exportable reports (PDF, CSV, Excel)",
        )

        screenshot6 = self.create_interface_screenshot(
            "analytics",
            [
                "Analytics Dashboard - Last 30 Days",
                "",
                "Overall Metrics:",
                "  • Total Sessions: 342",
                "  • Avg Learning Efficiency: 89.4%",
                "  • Engagement Rate: 94.7%",
                "  • Completion Rate: 91.2%",
                "",
                "Top Insights:",
                "  1. Students perform best between 10 AM - 12 PM",
                "  2. Interactive content shows 23% higher retention",
                "  3. Short breaks (5 min) improve focus by 31%",
                "",
                "[Export Report]  [View Details]  [Share]",
            ],
        )
        print(f"✅ Generated: {screenshot6}")

        input("\nPress Enter to continue to Step 7... ")

        # STEP 7: Admin Settings
        self.print_step(
            7,
            "ADMINISTRATION - System Management",
            "Administrators manage organization settings:\n"
            + "→ User management (add/remove, roles, permissions)\n"
            + "→ Billing and subscription management\n"
            + "→ Integration settings (Azure, LMS, HRIS)\n"
            + "→ Compliance and data retention policies\n"
            + "→ API access and webhooks",
        )

        screenshot7 = self.create_interface_screenshot(
            "admin",
            [
                "Administration - Settings",
                "",
                "Organization: L.I.F.ECoach121.com Limited",
                "Subscription: Professional Plan - $30/user/month",
                "Active Users: 47/50",
                "",
                "Quick Actions:",
                "  • Add New Users",
                "  • Manage Roles & Permissions",
                "  • View Billing & Invoices",
                "  • Configure Integrations",
                "  • Export Compliance Reports",
                "",
                "[Manage]  [Billing]  [Security]  [Support]",
            ],
        )
        print(f"✅ Generated: {screenshot7}")

        input("\nPress Enter to see integration options... ")

        # STEP 8: Integrations
        self.print_step(
            8,
            "INTEGRATIONS - Ecosystem Connectivity",
            "L.I.F.E Platform integrates with existing systems:\n"
            + "→ Learning Management Systems (Canvas, Blackboard, Moodle)\n"
            + "→ Student Information Systems (PowerSchool, Infinite Campus)\n"
            + "→ Healthcare EMR Systems (Epic, Cerner)\n"
            + "→ Enterprise HRIS (Workday, SAP SuccessFactors)\n"
            + "→ Microsoft Teams, Zoom for virtual learning",
        )

        screenshot8 = self.create_interface_screenshot(
            "integrations",
            [
                "Available Integrations",
                "",
                "Learning Management Systems:",
                "  ✅ Canvas LMS - Connected",
                "  ⚪ Blackboard - Available",
                "  ⚪ Moodle - Available",
                "",
                "Communication Platforms:",
                "  ✅ Microsoft Teams - Connected",
                "  ⚪ Zoom - Available",
                "",
                "Enterprise Systems:",
                "  ✅ Azure AD - Connected",
                "",
                "[Connect New Integration]  [Manage Existing]",
            ],
        )
        print(f"✅ Generated: {screenshot8}")

        input("\nPress Enter to see API access... ")

        # STEP 9: Developer API
        self.print_step(
            9,
            "DEVELOPER API - Custom Integrations",
            "Developers can build custom integrations:\n"
            + "→ RESTful API with comprehensive documentation\n"
            + "→ Webhooks for real-time event notifications\n"
            + "→ SDKs for Python, JavaScript, C#\n"
            + "→ Rate limits: 10,000 requests/hour (Professional plan)\n"
            + "→ Sandbox environment for testing",
        )

        screenshot9 = self.create_interface_screenshot(
            "api",
            [
                "Developer API - Documentation",
                "",
                "Endpoints:",
                "  GET  /api/v1/sessions          - List learning sessions",
                "  POST /api/v1/sessions          - Create new session",
                "  GET  /api/v1/analytics/{id}    - Get session analytics",
                "  POST /api/v1/webhooks          - Register webhook",
                "",
                "Authentication: Bearer Token (OAuth 2.0)",
                "Rate Limit: 10,000 req/hour",
                "",
                "API Key: life_prod_************************",
                "",
                "[View Full Docs]  [Generate New Key]  [Test Endpoint]",
            ],
        )
        print(f"✅ Generated: {screenshot9}")

        input("\nPress Enter to see support options... ")

        # STEP 10: Support
        self.print_step(
            10,
            "SUPPORT & TRAINING - Getting Help",
            "Users access multiple support channels:\n"
            + "→ 24/7 chat support (Professional/Enterprise plans)\n"
            + "→ Email support with 4-hour SLA\n"
            + "→ Video training library (50+ tutorials)\n"
            + "→ Live onboarding sessions (weekly)\n"
            + "→ Knowledge base with 200+ articles\n"
            + "→ Community forum for peer support",
        )

        screenshot10 = self.create_interface_screenshot(
            "support",
            [
                "Support Center",
                "",
                "Get Help:",
                "  💬 Live Chat Support - Available 24/7",
                "  📧 Email Support - Response in 4 hours",
                "  📚 Knowledge Base - 200+ articles",
                "  🎥 Video Tutorials - 50+ training videos",
                "  👥 Community Forum - Ask the community",
                "",
                "Upcoming Training:",
                "  • Oct 2, 2025 - Getting Started Webinar",
                "  • Oct 5, 2025 - Advanced Analytics Deep Dive",
                "",
                "[Contact Support]  [Browse Knowledge Base]  [Join Community]",
            ],
        )
        print(f"✅ Generated: {screenshot10}")

        # Summary
        self.print_header("📊 USER INTERACTION SUMMARY")

        print(
            "L.I.F.E Platform provides a complete neuroadaptive learning experience:\n"
        )
        print("✅ DISCOVERY      → Find on Azure Marketplace, see performance metrics")
        print("✅ ONBOARDING     → Quick 5-minute setup with Azure AD")
        print("✅ DASHBOARD      → Personalized overview of all activities")
        print("✅ EEG SETUP      → Connect devices with auto-calibration")
        print("✅ LEARNING       → Real-time adaptation during sessions (0.42ms)")
        print("✅ ANALYTICS      → Comprehensive insights and reports")
        print("✅ ADMINISTRATION → Full organizational management")
        print("✅ INTEGRATIONS   → Connect with existing systems")
        print("✅ API ACCESS     → Build custom solutions")
        print("✅ SUPPORT        → 24/7 assistance and training")

        print("\n" + "=" * 70)
        print(f"Generated {10} interface screenshots in: {self.output_dir}/")
        print("=" * 70)

        return True


def main():
    """Run interactive demo"""
    demo = LIFEInteractiveDemo()

    print("\n" + "=" * 70)
    print("  L.I.F.E PLATFORM - INTERACTIVE DEMO & WALKTHROUGH")
    print("=" * 70)
    print("\nThis demo will:")
    print("  1. Show you how users discover and interact with L.I.F.E Platform")
    print("  2. Walk through the complete user journey (10 steps)")
    print("  3. Generate interface screenshots for each step")
    print("\nTotal time: ~5-10 minutes (you control the pace)")
    print("=" * 70 + "\n")

    response = input("Ready to start? (yes/no): ").strip().lower()

    if response in ["yes", "y"]:
        demo.show_user_journey()
        print("\n✅ Demo complete! Check the 'demo_assets' folder for screenshots.")
    else:
        print("\nDemo cancelled. Run again when ready!")

    input("\nPress Enter to exit... ")


if __name__ == "__main__":
    main()
