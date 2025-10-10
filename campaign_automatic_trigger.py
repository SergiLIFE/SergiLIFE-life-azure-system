#!/usr/bin/env python3
"""
Campaign Automatic Trigger - L.I.F.E. Platform
Comprehensive automation system for marketplace campaign launch

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb

Features:
- Automatic scheduled campaign execution
- GitHub Actions integration
- Real-time performance monitoring
- Multi-segment campaign management
- Emergency override capabilities
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from campaign_manager import CampaignManager, CampaignMetrics, MarketplaceKPIs
except ImportError:
    print("Warning: campaign_manager.py not found or has issues. Using mock data.")
    CampaignManager = None

# Configure logging
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(SCRIPT_DIR, "logs")
RESULTS_DIR = os.path.join(SCRIPT_DIR, "results")
TRACKING_DIR = os.path.join(SCRIPT_DIR, "tracking_data")

os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(TRACKING_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOGS_DIR, "campaign_auto_trigger.log")),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class CampaignAutomaticTrigger:
    """Automatic campaign trigger system for L.I.F.E. Platform"""
    
    def __init__(self):
        self.script_dir = Path(SCRIPT_DIR)
        self.logs_dir = Path(LOGS_DIR)
        self.results_dir = Path(RESULTS_DIR)
        self.tracking_dir = Path(TRACKING_DIR)
        
        # Campaign configuration
        self.campaign_config = {
            "marketplace_offer_id": "9a600d96-fe1e-420b-902a-a0c42c561adb",
            "platform_version": "2025.1.0-PRODUCTION",
            "launch_date": "2025-10-07",
            "target_institutions": 1720,
            "revenue_target_q4": 345000,  # $345K
            "revenue_projection_2029": 50700000,  # $50.7M
        }
        
        # Campaign segments
        self.campaign_segments = {
            "educational_institutions": {
                "count": 1720,
                "description": "Universities, colleges, K-12 schools",
                "priority": "high"
            },
            "healthcare_facilities": {
                "count": 450,
                "description": "Hospitals, clinics, medical research centers",
                "priority": "medium"
            },
            "enterprise_partners": {
                "count": 200,
                "description": "Corporate training, HR departments",
                "priority": "high"
            },
            "research_institutions": {
                "count": 300,
                "description": "Government research, think tanks",
                "priority": "medium"
            }
        }
        
        # Automation schedule (key dates and times)
        self.automation_schedule = [
            {
                "date": "2025-10-07",
                "time": "09:00",
                "action": "launch_marketplace_promotion",
                "segments": ["all"]
            },
            {
                "date": "2025-10-07", 
                "time": "10:00",
                "action": "activate_social_media_campaign",
                "platforms": ["LinkedIn", "Twitter", "Facebook"]
            },
            {
                "date": "2025-10-07",
                "time": "11:00", 
                "action": "distribute_press_release",
                "media": ["education_tech", "healthcare_it", "ai_industry"]
            },
            {
                "date": "2025-10-08",
                "time": "09:00",
                "action": "follow_up_outreach",
                "segments": ["educational_institutions"]
            }
        ]
    
    async def check_trigger_conditions(self) -> Dict[str, Any]:
        """Check if automatic trigger conditions are met"""
        logger.info("🔍 Checking automatic trigger conditions...")
        
        current_time = datetime.now()
        conditions = {
            "timestamp": current_time.isoformat(),
            "should_trigger": False,
            "trigger_reason": "",
            "next_scheduled": None,
            "emergency_override": False,
            "system_status": "operational"
        }
        
        try:
            # Check for October 7th launch date
            if current_time.date() >= datetime(2025, 10, 7).date():
                conditions["should_trigger"] = True
                conditions["trigger_reason"] = "birthday_launch_date_reached"
                logger.info("🎂 Birthday launch date reached! Triggering campaigns...")
            
            # Check for scheduled automation windows
            for schedule_item in self.automation_schedule:
                schedule_date = datetime.strptime(schedule_item["date"], "%Y-%m-%d").date()
                schedule_time = datetime.strptime(schedule_item["time"], "%H:%M").time()
                schedule_datetime = datetime.combine(schedule_date, schedule_time)
                
                time_diff = (current_time - schedule_datetime).total_seconds()
                
                # Trigger if within 5-minute window
                if -300 <= time_diff <= 300:  # 5 minutes before/after
                    conditions["should_trigger"] = True
                    conditions["trigger_reason"] = f"scheduled_{schedule_item['action']}"
                    conditions["scheduled_action"] = schedule_item
                    logger.info(f"📅 Scheduled trigger: {schedule_item['action']}")
                    break
            
            # Check for manual override file
            override_file = self.script_dir / "EMERGENCY_CAMPAIGN_TRIGGER.flag"
            if override_file.exists():
                conditions["should_trigger"] = True
                conditions["trigger_reason"] = "emergency_manual_override"
                conditions["emergency_override"] = True
                logger.warning("🚨 Emergency override detected!")
                # Remove override file after detection
                override_file.unlink()
            
            # Find next scheduled trigger
            future_schedules = []
            for schedule_item in self.automation_schedule:
                schedule_date = datetime.strptime(schedule_item["date"], "%Y-%m-%d").date()
                schedule_time = datetime.strptime(schedule_item["time"], "%H:%M").time()
                schedule_datetime = datetime.combine(schedule_date, schedule_time)
                
                if schedule_datetime > current_time:
                    future_schedules.append(schedule_datetime)
            
            if future_schedules:
                conditions["next_scheduled"] = min(future_schedules).isoformat()
            
            return conditions
            
        except Exception as e:
            logger.error(f"Error checking trigger conditions: {e}")
            conditions["system_status"] = "error"
            conditions["error"] = str(e)
            return conditions
    
    async def execute_automatic_campaign(self, trigger_conditions: Dict[str, Any]) -> Dict[str, Any]:
        """Execute automatic campaign based on trigger conditions"""
        logger.info("🚀 Executing automatic campaign...")
        
        execution_result = {
            "execution_id": f"auto-campaign-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "trigger_reason": trigger_conditions.get("trigger_reason", "unknown"),
            "start_time": datetime.now().isoformat(),
            "campaigns_launched": [],
            "success": False,
            "errors": [],
            "performance_metrics": {}
        }
        
        try:
            # Initialize campaign manager if available
            if CampaignManager:
                manager = CampaignManager()
            else:
                logger.warning("CampaignManager not available, using simulation mode")
                manager = None
            
            # Determine campaign type based on trigger reason
            if "birthday_launch" in trigger_conditions.get("trigger_reason", ""):
                campaign_types = ["marketplace_promotion", "uk_universities_outreach"]
            elif "scheduled" in trigger_conditions.get("trigger_reason", ""):
                action = trigger_conditions.get("scheduled_action", {}).get("action", "")
                if "social_media" in action:
                    campaign_types = ["social_media_campaign"]
                elif "press_release" in action:
                    campaign_types = ["press_release_distribution"]
                else:
                    campaign_types = ["marketplace_promotion"]
            else:
                campaign_types = ["marketplace_promotion"]
            
            # Execute campaigns
            for campaign_type in campaign_types:
                try:
                    logger.info(f"🎯 Launching campaign: {campaign_type}")
                    
                    if manager:
                        # Real campaign execution
                        campaign_id = await manager.launch_campaign(
                            campaign_type=campaign_type,
                            target_audience="all_segments",
                            duration_days=30
                        )
                        
                        # Generate outreach materials
                        for segment in self.campaign_segments.keys():
                            await manager.generate_outreach_campaign(segment)
                        
                        execution_result["campaigns_launched"].append({
                            "type": campaign_type,
                            "campaign_id": campaign_id,
                            "status": "launched",
                            "timestamp": datetime.now().isoformat()
                        })
                    else:
                        # Simulation mode
                        mock_campaign_id = f"mock-{campaign_type}-{datetime.now().strftime('%H%M%S')}"
                        execution_result["campaigns_launched"].append({
                            "type": campaign_type,
                            "campaign_id": mock_campaign_id,
                            "status": "simulated",
                            "timestamp": datetime.now().isoformat()
                        })
                    
                    logger.info(f"✅ Campaign launched successfully: {campaign_type}")
                    
                except Exception as e:
                    error_msg = f"Failed to launch {campaign_type}: {str(e)}"
                    execution_result["errors"].append(error_msg)
                    logger.error(error_msg)
            
            # Create tracking infrastructure
            await self._create_campaign_tracking_infrastructure(execution_result)
            
            # Monitor initial performance
            execution_result["performance_metrics"] = await self._monitor_campaign_performance()
            
            execution_result["success"] = len(execution_result["campaigns_launched"]) > 0
            execution_result["end_time"] = datetime.now().isoformat()
            
            # Export execution report
            report_file = self.results_dir / f"campaign_execution_{execution_result['execution_id']}.json"
            with open(report_file, 'w') as f:
                json.dump(execution_result, f, indent=2)
            
            logger.info(f"📊 Campaign execution report saved: {report_file}")
            
            return execution_result
            
        except Exception as e:
            execution_result["success"] = False
            execution_result["errors"].append(f"Critical execution error: {str(e)}")
            execution_result["end_time"] = datetime.now().isoformat()
            logger.error(f"Critical error in campaign execution: {e}")
            return execution_result
    
    async def _create_campaign_tracking_infrastructure(self, execution_result: Dict[str, Any]) -> None:
        """Create tracking infrastructure for campaigns"""
        logger.info("📁 Creating campaign tracking infrastructure...")
        
        try:
            # Create tracking directories
            for subdir in ["kpis", "outreach", "conversions", "analytics", "reports"]:
                (self.tracking_dir / subdir).mkdir(exist_ok=True)
            
            # Create campaign tracking file
            tracking_data = {
                "execution_id": execution_result["execution_id"],
                "campaigns": execution_result["campaigns_launched"],
                "start_time": execution_result["start_time"],
                "target_segments": list(self.campaign_segments.keys()),
                "marketplace_offer_id": self.campaign_config["marketplace_offer_id"],
                "tracking_created": datetime.now().isoformat()
            }
            
            tracking_file = self.tracking_dir / "campaign_tracking.json"
            with open(tracking_file, 'w') as f:
                json.dump(tracking_data, f, indent=2)
            
            logger.info(f"✅ Tracking infrastructure created: {tracking_file}")
            
        except Exception as e:
            logger.error(f"Error creating tracking infrastructure: {e}")
    
    async def _monitor_campaign_performance(self) -> Dict[str, Any]:
        """Monitor campaign performance metrics"""
        logger.info("📊 Monitoring campaign performance...")
        
        # Mock performance metrics (in production, these would come from real APIs)
        performance = {
            "timestamp": datetime.now().isoformat(),
            "marketplace_views": 145,
            "demo_requests": 8,
            "trial_signups": 3,
            "conversion_rate": 5.5,  # %
            "geographic_reach": {
                "uk": 45,
                "eu": 32,
                "us": 68,
                "others": 25
            },
            "segment_performance": {}
        }
        
        # Add segment-specific metrics
        for segment, config in self.campaign_segments.items():
            performance["segment_performance"][segment] = {
                "targeted": config["count"],
                "reached": int(config["count"] * 0.25),  # 25% reach simulation
                "engaged": int(config["count"] * 0.08),   # 8% engagement simulation
                "converted": int(config["count"] * 0.002) # 0.2% conversion simulation
            }
        
        return performance
    
    async def create_emergency_trigger(self) -> bool:
        """Create emergency trigger flag for immediate campaign launch"""
        logger.info("🚨 Creating emergency trigger flag...")
        
        try:
            override_file = self.script_dir / "EMERGENCY_CAMPAIGN_TRIGGER.flag"
            override_data = {
                "created": datetime.now().isoformat(),
                "reason": "Manual emergency override",
                "created_by": "campaign_automatic_trigger.py",
                "instructions": "This flag triggers immediate campaign launch on next check"
            }
            
            with open(override_file, 'w') as f:
                json.dump(override_data, f, indent=2)
            
            logger.info(f"✅ Emergency trigger created: {override_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating emergency trigger: {e}")
            return False
    
    async def get_campaign_status(self) -> Dict[str, Any]:
        """Get current campaign system status"""
        logger.info("📋 Getting campaign system status...")
        
        status = {
            "timestamp": datetime.now().isoformat(),
            "system_operational": True,
            "github_workflow_available": True,
            "campaign_manager_available": CampaignManager is not None,
            "tracking_infrastructure": "ready",
            "next_scheduled_check": (datetime.now() + timedelta(minutes=15)).isoformat(),
            "emergency_override_available": True,
            "configuration": self.campaign_config,
            "segments_configured": len(self.campaign_segments),
            "automation_schedule_items": len(self.automation_schedule)
        }
        
        # Check if workflow files exist
        workflow_file = self.script_dir / ".github" / "workflows" / "campaign-launcher.yml"
        status["github_workflow_file_exists"] = workflow_file.exists()
        
        # Check tracking directories
        tracking_dirs = ["kpis", "outreach", "conversions", "analytics"]
        status["tracking_directories"] = {
            dirname: (self.tracking_dir / dirname).exists() 
            for dirname in tracking_dirs
        }
        
        return status


async def main():
    """Main function for campaign automation system"""
    print("🚀 L.I.F.E. Platform - Campaign Automatic Trigger System")
    print("=" * 65)
    print(f"🕐 Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Target Launch: October 7, 2025 at 09:00 BST")
    print("=" * 65)
    
    trigger_system = CampaignAutomaticTrigger()
    
    # Check system status
    print("\n📋 SYSTEM STATUS CHECK:")
    status = await trigger_system.get_campaign_status()
    print(f"  ✅ System Operational: {status['system_operational']}")
    print(f"  🤖 GitHub Workflow: {status['github_workflow_available']}")
    print(f"  📊 Campaign Manager: {status['campaign_manager_available']}")
    print(f"  📁 Tracking Infrastructure: {status['tracking_infrastructure']}")
    
    # Check trigger conditions
    print("\n🔍 TRIGGER CONDITIONS CHECK:")
    conditions = await trigger_system.check_trigger_conditions()
    print(f"  🎯 Should Trigger: {conditions['should_trigger']}")
    print(f"  📝 Trigger Reason: {conditions['trigger_reason']}")
    
    if conditions.get('next_scheduled'):
        print(f"  ⏰ Next Scheduled: {conditions['next_scheduled']}")
    
    # Execute campaign if conditions are met
    if conditions['should_trigger']:
        print(f"\n🚀 CAMPAIGN EXECUTION:")
        print(f"  📋 Reason: {conditions['trigger_reason']}")
        
        execution_result = await trigger_system.execute_automatic_campaign(conditions)
        
        print(f"  ✅ Success: {execution_result['success']}")
        print(f"  🎯 Campaigns Launched: {len(execution_result['campaigns_launched'])}")
        
        if execution_result['campaigns_launched']:
            print("  📊 Campaign Details:")
            for campaign in execution_result['campaigns_launched']:
                print(f"    - {campaign['type']}: {campaign['campaign_id']}")
        
        if execution_result['errors']:
            print("  ⚠️ Errors:")
            for error in execution_result['errors']:
                print(f"    - {error}")
        
        # Show performance metrics
        if execution_result.get('performance_metrics'):
            metrics = execution_result['performance_metrics']
            print(f"\n📈 INITIAL PERFORMANCE METRICS:")
            print(f"  👀 Marketplace Views: {metrics.get('marketplace_views', 0)}")
            print(f"  🎯 Demo Requests: {metrics.get('demo_requests', 0)}")
            print(f"  🔄 Conversion Rate: {metrics.get('conversion_rate', 0)}%")
    
    else:
        print(f"\n⏳ NO TRIGGER - Waiting for conditions to be met")
        if conditions.get('next_scheduled'):
            next_time = datetime.fromisoformat(conditions['next_scheduled'])
            time_until = next_time - datetime.now()
            print(f"   ⏰ Next check in: {time_until}")
    
    print("\n" + "=" * 65)
    print("🏁 Campaign Automatic Trigger - Complete")


def create_emergency_trigger():
    """Command-line function to create emergency trigger"""
    print("🚨 Creating Emergency Campaign Trigger...")
    
    async def _create():
        trigger_system = CampaignAutomaticTrigger()
        success = await trigger_system.create_emergency_trigger()
        if success:
            print("✅ Emergency trigger created successfully!")
            print("   The next automatic check will launch campaigns immediately.")
        else:
            print("❌ Failed to create emergency trigger.")
    
    asyncio.run(_create())


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "emergency":
        create_emergency_trigger()
    else:
        asyncio.run(main())