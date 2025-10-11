#!/usr/bin/env python3
"""
Azure Subscription Switch Guide - L.I.F.E. Platform Access
Copyright 2025 - Sergio Paya Borrull
Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb

ISSUE: Logged into wrong Azure subscription (Azure for Startups)
NEED: Access to L.I.F.E. Platform subscription 5c88cef6-f243-497d-98af-6c6086d575ca

IMMEDIATE SOLUTION REQUIRED
"""

import os
import logging
from datetime import datetime
from typing import Dict, List

# Setup logging
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(SCRIPT_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOGS_DIR, "azure_subscription_switch.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

class AzureSubscriptionSwitcher:
    """
    Guide user to switch to correct Azure subscription for L.I.F.E. Platform
    """
    
    def __init__(self):
        self.current_tenant = "lifecoach121.com"
        self.target_subscription = "5c88cef6-f243-497d-98af-6c6086d575ca"
        self.marketplace_offer_id = "9a600d96-fe1e-420b-902a-a0c42c561adb"
        self.current_view = "Azure for Startups"
        self.demo_date = "October 15, 2025"
        
        logging.info("Azure Subscription Switch Guide initialized")
        logging.info(f"Current view: {self.current_view}")
        logging.info(f"Target subscription: {self.target_subscription}")
    
    def diagnose_subscription_issue(self) -> Dict[str, str]:
        """
        Diagnose why user is in wrong subscription
        """
        logging.info("Diagnosing subscription access issue")
        
        diagnosis = {
            "current_status": "Logged into Azure for Startups program",
            "current_tenant": "lifecoach121.com tenant",
            "issue": "Not accessing L.I.F.E. Platform production subscription",
            "cause": "Multiple subscriptions - landed in startup program instead of main subscription",
            "solution_needed": "Switch to production subscription with L.I.F.E. resources"
        }
        
        logging.info(f"Issue identified: {diagnosis['issue']}")
        return diagnosis
    
    def get_subscription_switch_steps(self) -> List[Dict[str, str]]:
        """
        Provide step-by-step guide to switch subscriptions
        """
        logging.info("Generating subscription switch steps")
        
        steps = [
            {
                "step": "1",
                "action": "Click on Subscriptions in left menu",
                "location": "Left sidebar - look for 'Subscriptions' icon",
                "expected": "Will show all available subscriptions",
                "critical": "This reveals all subscriptions you have access to"
            },
            {
                "step": "2", 
                "action": "Look for subscription ID: 5c88cef6-f243-497d-98af-6c6086d575ca",
                "location": "In the subscriptions list",
                "expected": "Should see L.I.F.E. Platform production subscription",
                "critical": "This is your main Azure subscription with resources"
            },
            {
                "step": "3",
                "action": "Click on the correct subscription",
                "location": "Click the subscription name or ID",
                "expected": "Will switch context to that subscription",
                "critical": "This activates the correct subscription context"
            },
            {
                "step": "4",
                "action": "Verify subscription name and resources", 
                "location": "Top of portal should show correct subscription",
                "expected": "Should see L.I.F.E. Platform resources and services",
                "critical": "Confirms you're in the right subscription"
            },
            {
                "step": "5",
                "action": "Navigate to Resource Groups",
                "location": "Left sidebar - 'Resource groups'",
                "expected": "Should see life-platform-rg or similar L.I.F.E. resources",
                "critical": "Validates access to your L.I.F.E. Platform infrastructure"
            }
        ]
        
        for step in steps:
            logging.info(f"Step {step['step']}: {step['action']}")
        
        return steps
    
    def get_alternative_access_methods(self) -> List[Dict[str, str]]:
        """
        Alternative methods if subscription switching doesn't work
        """
        logging.info("Preparing alternative access methods")
        
        alternatives = [
            {
                "method": "Direct Subscription URL",
                "url": f"https://portal.azure.com/#@/resource/subscriptions/{self.target_subscription}/overview",
                "description": "Direct link to your L.I.F.E. Platform subscription",
                "when_to_use": "If you can't find subscription in the list"
            },
            {
                "method": "Resource Groups Direct",
                "url": "https://portal.azure.com/#view/HubsExtension/BrowseResourceGroups",
                "description": "View all resource groups across subscriptions",
                "when_to_use": "To find L.I.F.E. resources regardless of subscription view"
            },
            {
                "method": "All Resources View",
                "url": "https://portal.azure.com/#view/HubsExtension/BrowseAll",
                "description": "See all resources you have access to",
                "when_to_use": "If resources are scattered or hard to locate"
            },
            {
                "method": "Search for L.I.F.E. Resources",
                "url": "Use search box: 'life' or 'stlifeplatformprod'",
                "description": "Search for specific L.I.F.E. Platform resources",
                "when_to_use": "Quick way to find resources by name"
            },
            {
                "method": "Account Sign-Out and Re-Sign",
                "url": "Sign out completely and use different Microsoft account",
                "description": "Try with sergio.payaborrull@outlook.com or other account",
                "when_to_use": "If current account doesn't have access to main subscription"
            }
        ]
        
        for alt in alternatives:
            logging.info(f"Alternative: {alt['method']} - {alt['description']}")
        
        return alternatives
    
    def check_account_permissions(self) -> Dict[str, str]:
        """
        Guide to check what permissions current account has
        """
        logging.info("Checking account permissions guidance")
        
        permission_check = {
            "current_account_indicator": "lifecoach121.com shown in top right",
            "subscription_access_check": "Go to Subscriptions to see what you can access",
            "expected_subscriptions": [
                "Azure for Startups (current - visible)",
                f"L.I.F.E. Platform Prod ({self.target_subscription}) - NEEDED"
            ],
            "marketplace_access_check": f"Look for marketplace offer {self.marketplace_offer_id}",
            "resource_access_validation": "Check if you can see Storage Accounts, Function Apps, etc."
        }
        
        logging.info("Permission check guidance prepared")
        return permission_check
    
    def generate_demo_impact_assessment(self) -> Dict[str, str]:
        """
        Assess impact on October 15 demo
        """
        logging.info("Assessing demo preparation impact")
        
        impact = {
            "demo_date": self.demo_date,
            "days_remaining": "5 days",
            "participants": "23 confirmed",
            "current_blocker": "Wrong Azure subscription - can't access L.I.F.E. resources",
            "critical_need": "Access to production L.I.F.E. Platform infrastructure",
            "fallback_plan": "Local development environment if Azure access not restored",
            "urgency_level": "HIGH - Must resolve within 24 hours for demo prep"
        }
        
        logging.info(f"Demo impact: {impact['urgency_level']}")
        return impact
    
    def run_complete_subscription_guide(self) -> None:
        """
        Run complete subscription switching guide
        """
        logging.info("=" * 80)
        logging.info("AZURE SUBSCRIPTION SWITCHING GUIDE")
        logging.info("=" * 80)
        
        # Diagnosis
        diagnosis = self.diagnose_subscription_issue()
        logging.info(f"\nDIAGNOSIS: {diagnosis['current_status']}")
        
        # Switch steps
        steps = self.get_subscription_switch_steps()
        logging.info(f"\nSWITCH STEPS: {len(steps)} actions required")
        
        # Alternatives
        alternatives = self.get_alternative_access_methods()
        logging.info(f"\nALTERNATIVE METHODS: {len(alternatives)} options available")
        
        # Permissions
        permissions = self.check_account_permissions()
        logging.info(f"\nPERMISSION CHECK: {permissions['current_account_indicator']}")
        
        # Demo impact
        impact = self.generate_demo_impact_assessment()
        logging.info(f"\nDEMO IMPACT: {impact['urgency_level']}")
        
        logging.info("\n" + "=" * 80)
        logging.info("SUBSCRIPTION GUIDE COMPLETE")
        logging.info("=" * 80)

def main():
    """
    Main function to guide subscription switching
    """
    print("🔄 AZURE SUBSCRIPTION SWITCHING REQUIRED")
    print("=" * 60)
    
    switcher = AzureSubscriptionSwitcher()
    switcher.run_complete_subscription_guide()
    
    print("\n🎯 IMMEDIATE ACTION REQUIRED:")
    print("1. Click 'Subscriptions' in the left sidebar")
    print("2. Look for subscription ID: 5c88cef6-f243-497d-98af-6c6086d575ca")
    print("3. Click on that subscription to switch context")
    print("4. Verify you can see L.I.F.E. Platform resources")
    
    print("\n🚨 IF SUBSCRIPTION NOT VISIBLE:")
    print("Try this direct URL:")
    print("https://portal.azure.com/#@/resource/subscriptions/5c88cef6-f243-497d-98af-6c6086d575ca/overview")
    
    print("\n⚡ DEMO CRITICAL:")
    print("- October 15, 2025 demo in 5 days")
    print("- 23 participants confirmed")
    print("- MUST access L.I.F.E. Platform resources!")
    
    print("\n🔍 ALTERNATIVE: Search for 'life' in Azure search box")
    print("=" * 60)

if __name__ == "__main__":
    main()