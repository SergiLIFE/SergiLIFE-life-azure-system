#!/usr/bin/env python3
"""
L.I.F.E Platform - October 24 Response Tracker
Real-time tracking of the 23 interested prospects from today's outreach campaign
"""

import asyncio
import json
import logging
import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional

# Setup logging
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(SCRIPT_DIR, "logs")
TRACKING_DIR = os.path.join(SCRIPT_DIR, "tracking_data", "oct24_responses")
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(TRACKING_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOGS_DIR, "response_tracker_oct24.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


class ResponseStatus(Enum):
    """Response status tracking"""

    EMAIL_SENT = "email_sent"
    OPENED = "opened"
    RESPONDED_INTERESTED = "responded_interested"
    RESPONDED_NOT_NOW = "responded_not_now"
    DEMO_SCHEDULED = "demo_scheduled"
    DEMO_COMPLETED = "demo_completed"
    TRIAL_STARTED = "trial_started"
    CUSTOMER_SIGNED = "customer_signed"
    NO_RESPONSE = "no_response"


class ProspectTier(Enum):
    """Prospect priority tier"""

    VIP = "vip"  # Microsoft, Oxford, Cambridge
    HIGH = "high"  # NHS, Imperial, Major Universities
    MEDIUM = "medium"  # Regional institutions
    STANDARD = "standard"  # General prospects


@dataclass
class Prospect:
    """Individual prospect tracking"""

    prospect_id: str
    name: str
    institution: str
    email: str
    tier: ProspectTier
    pipeline_value: str
    status: ResponseStatus
    email_sent_date: datetime
    last_contact: Optional[datetime] = None
    response_date: Optional[datetime] = None
    demo_date: Optional[datetime] = None
    notes: str = ""
    follow_up_date: Optional[datetime] = None


class October24ResponseTracker:
    """Track responses from October 24 outreach campaign"""

    def __init__(self):
        self.prospects: Dict[str, Prospect] = {}
        self.campaign_metrics = {
            "total_prospects": 23,
            "emails_sent": 23,
            "responses_received": 0,
            "demos_scheduled": 0,
            "trials_started": 0,
            "customers_signed": 0,
            "total_pipeline": "£6.4M+",
            "campaign_start": datetime.now(),
        }

        self.load_known_prospects()
        logger.info("October 24 Response Tracker initialized")

    def load_known_prospects(self) -> None:
        """Load the 23 known interested prospects"""

        # VIP Tier prospects (confirmed from October 15)
        vip_prospects = [
            Prospect(
                prospect_id="OXFORD_001",
                name="Dr. Sarah Mitchell",
                institution="Oxford University",
                email="neuroscience.dept@ox.ac.uk",
                tier=ProspectTier.VIP,
                pipeline_value="£850K",
                status=ResponseStatus.EMAIL_SENT,
                email_sent_date=datetime(2025, 10, 24, 9, 0),
                follow_up_date=datetime(2025, 10, 26, 9, 0),
                notes="October 15 demo participant - warm lead",
            ),
            Prospect(
                prospect_id="CAMBRIDGE_001",
                name="Prof. James Harrison",
                institution="Cambridge University",
                email="brain.sciences@cam.ac.uk",
                tier=ProspectTier.VIP,
                pipeline_value="£950K",
                status=ResponseStatus.EMAIL_SENT,
                email_sent_date=datetime(2025, 10, 24, 9, 0),
                follow_up_date=datetime(2025, 10, 26, 9, 0),
                notes="October 15 demo participant - very interested",
            ),
            Prospect(
                prospect_id="MICROSOFT_001",
                name="Dr. Alex Chen",
                institution="Microsoft Research Cambridge",
                email="partnerships@microsoft.com",
                tier=ProspectTier.VIP,
                pipeline_value="£2.5M",
                status=ResponseStatus.EMAIL_SENT,
                email_sent_date=datetime(2025, 10, 24, 9, 0),
                follow_up_date=datetime(2025, 10, 26, 9, 0),
                notes="CRITICAL PARTNERSHIP - October 15 strategic session",
            ),
            Prospect(
                prospect_id="NHS_ROYAL_001",
                name="Digital Health Team",
                institution="NHS Royal London Hospital",
                email="neurology.rln@nhs.net",
                tier=ProspectTier.HIGH,
                pipeline_value="£450K",
                status=ResponseStatus.EMAIL_SENT,
                email_sent_date=datetime(2025, 10, 24, 9, 0),
                follow_up_date=datetime(2025, 10, 26, 9, 0),
                notes="NHS pilot program potential",
            ),
            Prospect(
                prospect_id="IMPERIAL_001",
                name="Research Team",
                institution="Imperial College London",
                email="bioeng.research@imperial.ac.uk",
                tier=ProspectTier.HIGH,
                pipeline_value="£650K",
                status=ResponseStatus.EMAIL_SENT,
                email_sent_date=datetime(2025, 10, 24, 9, 0),
                follow_up_date=datetime(2025, 10, 26, 9, 0),
                notes="Research innovation focus",
            ),
        ]

        # Add VIP prospects to tracking
        for prospect in vip_prospects:
            self.prospects[prospect.prospect_id] = prospect

        # Additional 18 prospects (placeholders for user to populate)
        additional_prospects = []
        for i in range(6, 24):  # Prospects 6-23
            prospect = Prospect(
                prospect_id=f"PROSPECT_{i:03d}",
                name=f"Contact {i}",
                institution=f"Institution {i}",
                email=f"contact{i}@example.com",
                tier=ProspectTier.MEDIUM,
                pipeline_value="£100K",
                status=ResponseStatus.EMAIL_SENT,
                email_sent_date=datetime(2025, 10, 24, 9, 0),
                follow_up_date=datetime(2025, 10, 26, 9, 0),
                notes="Update with actual prospect details",
            )
            additional_prospects.append(prospect)
            self.prospects[prospect.prospect_id] = prospect

        logger.info(f"Loaded {len(self.prospects)} prospects for tracking")

    def update_prospect_status(
        self, prospect_id: str, new_status: ResponseStatus, notes: str = ""
    ) -> bool:
        """Update prospect response status"""
        if prospect_id not in self.prospects:
            logger.warning(f"Prospect {prospect_id} not found")
            return False

        prospect = self.prospects[prospect_id]
        old_status = prospect.status
        prospect.status = new_status
        prospect.last_contact = datetime.now()

        if notes:
            prospect.notes += f" | {datetime.now().strftime('%Y-%m-%d %H:%M')}: {notes}"

        # Update metrics
        if (
            new_status == ResponseStatus.RESPONDED_INTERESTED
            and old_status != new_status
        ):
            self.campaign_metrics["responses_received"] += 1
        elif new_status == ResponseStatus.DEMO_SCHEDULED and old_status != new_status:
            self.campaign_metrics["demos_scheduled"] += 1
        elif new_status == ResponseStatus.TRIAL_STARTED and old_status != new_status:
            self.campaign_metrics["trials_started"] += 1
        elif new_status == ResponseStatus.CUSTOMER_SIGNED and old_status != new_status:
            self.campaign_metrics["customers_signed"] += 1

        logger.info(f"Updated {prospect_id}: {old_status.value} → {new_status.value}")
        return True

    def get_prospects_needing_followup(self) -> List[Prospect]:
        """Get prospects that need follow-up contact"""
        current_time = datetime.now()
        return [
            prospect
            for prospect in self.prospects.values()
            if (
                prospect.follow_up_date
                and prospect.follow_up_date <= current_time
                and prospect.status
                in [
                    ResponseStatus.EMAIL_SENT,
                    ResponseStatus.OPENED,
                    ResponseStatus.NO_RESPONSE,
                ]
            )
        ]

    def get_campaign_summary(self) -> Dict[str, Any]:
        """Generate campaign performance summary"""

        # Calculate response rate
        total_sent = self.campaign_metrics["emails_sent"]
        responses = self.campaign_metrics["responses_received"]
        response_rate = (responses / total_sent * 100) if total_sent > 0 else 0

        # Status breakdown
        status_breakdown = {}
        for status in ResponseStatus:
            count = sum(1 for p in self.prospects.values() if p.status == status)
            status_breakdown[status.value] = count

        # Tier breakdown
        tier_breakdown = {}
        for tier in ProspectTier:
            count = sum(1 for p in self.prospects.values() if p.tier == tier)
            tier_breakdown[tier.value] = count

        # Pipeline calculation
        total_pipeline = sum(
            int(
                p.pipeline_value.replace("£", "")
                .replace("K", "000")
                .replace("M", "000000")
                .replace(",", "")
            )
            for p in self.prospects.values()
            if p.status
            in [
                ResponseStatus.RESPONDED_INTERESTED,
                ResponseStatus.DEMO_SCHEDULED,
                ResponseStatus.TRIAL_STARTED,
            ]
        )

        return {
            "campaign_date": "October 24, 2025",
            "total_prospects": len(self.prospects),
            "response_metrics": {
                "emails_sent": total_sent,
                "responses_received": responses,
                "response_rate_percent": round(response_rate, 1),
                "demos_scheduled": self.campaign_metrics["demos_scheduled"],
                "trials_started": self.campaign_metrics["trials_started"],
                "customers_signed": self.campaign_metrics["customers_signed"],
            },
            "status_breakdown": status_breakdown,
            "tier_breakdown": tier_breakdown,
            "active_pipeline_value": f"£{total_pipeline:,}",
            "prospects_needing_followup": len(self.get_prospects_needing_followup()),
            "top_prospects": [
                {
                    "id": p.prospect_id,
                    "institution": p.institution,
                    "value": p.pipeline_value,
                    "status": p.status.value,
                }
                for p in sorted(
                    self.prospects.values(),
                    key=lambda x: (x.tier.value, x.pipeline_value),
                    reverse=True,
                )[:5]
            ],
        }

    def save_tracking_data(self) -> None:
        """Save current tracking data to files"""

        # Save prospects data
        prospects_file = os.path.join(TRACKING_DIR, "prospects_oct24.json")
        prospects_data = {
            pid: {
                "prospect_id": p.prospect_id,
                "name": p.name,
                "institution": p.institution,
                "email": p.email,
                "tier": p.tier.value,
                "pipeline_value": p.pipeline_value,
                "status": p.status.value,
                "email_sent_date": (
                    p.email_sent_date.isoformat() if p.email_sent_date else None
                ),
                "last_contact": p.last_contact.isoformat() if p.last_contact else None,
                "response_date": (
                    p.response_date.isoformat() if p.response_date else None
                ),
                "demo_date": p.demo_date.isoformat() if p.demo_date else None,
                "follow_up_date": (
                    p.follow_up_date.isoformat() if p.follow_up_date else None
                ),
                "notes": p.notes,
            }
            for pid, p in self.prospects.items()
        }

        with open(prospects_file, "w") as f:
            json.dump(prospects_data, f, indent=2)

        # Save campaign metrics
        metrics_file = os.path.join(TRACKING_DIR, "campaign_metrics_oct24.json")
        with open(metrics_file, "w") as f:
            json.dump(self.get_campaign_summary(), f, indent=2)

        logger.info(f"Tracking data saved to {TRACKING_DIR}")

    def display_dashboard(self) -> None:
        """Display real-time campaign dashboard"""

        summary = self.get_campaign_summary()

        print("=" * 80)
        print("🚀 L.I.F.E PLATFORM - OCTOBER 24 RESPONSE TRACKER DASHBOARD")
        print("=" * 80)
        print(f"📅 Campaign Date: {summary['campaign_date']}")
        print(f"📧 Total Prospects: {summary['total_prospects']}")
        print(f"💰 Active Pipeline: {summary['active_pipeline_value']}")
        print()

        print("📊 RESPONSE METRICS:")
        print("-" * 40)
        metrics = summary["response_metrics"]
        print(f"  Emails Sent: {metrics['emails_sent']}")
        print(
            f"  Responses: {metrics['responses_received']} ({metrics['response_rate_percent']}%)"
        )
        print(f"  Demos Scheduled: {metrics['demos_scheduled']}")
        print(f"  Trials Started: {metrics['trials_started']}")
        print(f"  Customers Signed: {metrics['customers_signed']}")
        print()

        print("🎯 TOP 5 PROSPECTS:")
        print("-" * 40)
        for i, prospect in enumerate(summary["top_prospects"], 1):
            print(
                f"  {i}. {prospect['institution']} ({prospect['value']}) - {prospect['status']}"
            )
        print()

        # Follow-up alerts
        followup_needed = self.get_prospects_needing_followup()
        if followup_needed:
            print(f"⚠️  FOLLOW-UP NEEDED: {len(followup_needed)} prospects")
            print("-" * 40)
            for prospect in followup_needed[:3]:
                print(f"  • {prospect.institution} - Follow up due")
            if len(followup_needed) > 3:
                print(f"  ... and {len(followup_needed) - 3} more")
            print()

        print("🎯 NEXT ACTIONS:")
        print("-" * 40)
        print("1. Check Info@lifecoach121.com for responses")
        print("2. Update prospect status as responses come in")
        print("3. Schedule demos for interested prospects")
        print("4. Send follow-ups on October 26 if no response")
        print()
        print(
            "💡 Use: tracker.update_prospect_status('OXFORD_001', ResponseStatus.RESPONDED_INTERESTED)"
        )
        print("=" * 80)


async def main():
    """Main execution function"""

    print("🚀 INITIALIZING OCTOBER 24 RESPONSE TRACKER...")
    tracker = October24ResponseTracker()

    # Display initial dashboard
    tracker.display_dashboard()

    # Save initial tracking data
    tracker.save_tracking_data()

    print("\n✅ RESPONSE TRACKER READY!")
    print("\n📧 As responses come in, update with:")
    print(
        "   tracker.update_prospect_status('PROSPECT_ID', ResponseStatus.RESPONDED_INTERESTED)"
    )
    print("\n💾 Tracking data saved to:", TRACKING_DIR)

    return tracker


if __name__ == "__main__":
    tracker = asyncio.run(main())
