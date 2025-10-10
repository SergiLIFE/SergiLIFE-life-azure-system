#!/usr/bin/env python3
"""
🎮 L.I.F.E. Platform - Self-Guided Tutorial System
Enhanced Tab Navigation with Back/Forward Controls and Step Completion

Copyright 2025 - Sergio Paya Borrull
Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
Production-Ready Tutorial System with Advanced Navigation
"""

import os
import sys
import json
import time
import keyboard
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List, Optional, Callable
import asyncio

# Setup directories
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TUTORIAL_DATA_DIR = os.path.join(SCRIPT_DIR, "tutorial_data")
PROGRESS_DIR = os.path.join(TUTORIAL_DATA_DIR, "progress")
os.makedirs(TUTORIAL_DATA_DIR, exist_ok=True)
os.makedirs(PROGRESS_DIR, exist_ok=True)

class StepStatus(Enum):
    """Tutorial step completion status"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress" 
    COMPLETED = "completed"
    MASTERED = "mastered"
    REVIEW = "review"

class NavigationAction(Enum):
    """Available navigation actions"""
    NEXT = "next"
    PREVIOUS = "previous"
    JUMP_TO = "jump_to"
    COMPLETE = "complete"
    REVIEW = "review"
    SAVE = "save"
    EXIT = "exit"
    RESTART = "restart"

@dataclass
class TutorialStep:
    """Individual tutorial step definition"""
    step_id: int
    title: str
    description: str
    tab_elements: List[str]
    completion_criteria: List[str]
    status: StepStatus = StepStatus.NOT_STARTED
    time_spent: float = 0.0
    attempts: int = 0
    last_accessed: Optional[str] = None
    notes: str = ""

@dataclass
class TutorialProgress:
    """Tutorial progress tracking"""
    user_id: str
    session_id: str
    current_step: int
    total_steps: int
    completed_steps: List[int]
    mastered_steps: List[int]
    total_time: float
    start_time: str
    last_update: str
    completion_percentage: float

class SelfGuidedTutorial:
    """
    🎯 Enhanced Self-Guided Tutorial System
    
    Features:
    - Tab navigation through every step
    - Back/Forward controls
    - Step completion tracking
    - Progress persistence
    - Non-linear navigation
    - Visual progress indicators
    """
    
    def __init__(self, user_id: str = "default_user"):
        self.user_id = user_id
        self.session_id = f"session_{int(time.time())}"
        self.current_step = 0
        self.steps: List[TutorialStep] = []
        self.progress_file = os.path.join(PROGRESS_DIR, f"{user_id}_progress.json")
        
        # Initialize tutorial steps
        self._initialize_tutorial_steps()
        
        # Load existing progress if available
        self._load_progress()
        
        print("🎮 L.I.F.E. Platform - Self-Guided Tutorial System Initialized")
        print("=" * 70)
    
    def _initialize_tutorial_steps(self):
        """Initialize the 10-step tutorial with tab navigation"""
        
        tutorial_data = [
            {
                "step_id": 1,
                "title": "🛒 Discovery - Azure Marketplace Introduction",
                "description": "Learn about L.I.F.E. Platform features and pricing",
                "tab_elements": [
                    "Pricing Tiers (Basic $15, Professional $30, Enterprise $50)",
                    "Core Features (Real-time EEG, Neural Processing, Analytics)",
                    "Benefits (97.95% Accuracy, 0.38ms Latency, 99.95% Uptime)",
                    "Purchase Button (Azure Marketplace Integration)",
                    "Trial Options (14-day free trial available)"
                ],
                "completion_criteria": [
                    "Review all pricing tiers",
                    "Understand core features",
                    "Navigate to purchase flow"
                ]
            },
            {
                "step_id": 2,
                "title": "🔐 Onboarding - Account Setup and Configuration",
                "description": "Complete initial account setup and preferences",
                "tab_elements": [
                    "Azure SSO Login (Single Sign-On authentication)",
                    "Permission Setup (Role-based access control)",
                    "Initial Configuration (Learning parameters, thresholds)",
                    "User Preferences (Interface theme, notifications)",
                    "Organization Setup (Multi-tenant configuration)"
                ],
                "completion_criteria": [
                    "Complete Azure authentication",
                    "Configure initial settings",
                    "Set user preferences"
                ]
            },
            {
                "step_id": 3,
                "title": "📊 Dashboard - Main Interface Familiarization",
                "description": "Explore the main dashboard and navigation",
                "tab_elements": [
                    "Navigation Menu (Home, Sessions, Analytics, Settings)",
                    "Widget Configuration (KPI displays, charts, metrics)",
                    "Quick Actions Panel (Start session, reports, system check)",
                    "System Status Indicators (Health, performance, alerts)",
                    "Help & Support Access (Documentation, chat, tutorials)"
                ],
                "completion_criteria": [
                    "Navigate through all menu items",
                    "Configure at least 2 widgets",
                    "Access help system"
                ]
            },
            {
                "step_id": 4,
                "title": "🧠 EEG Setup - Hardware Connection Guide",
                "description": "Connect and configure EEG hardware",
                "tab_elements": [
                    "Device Selection (Emotiv, Muse, OpenBCI, NeuroSky, etc.)",
                    "Connection Steps (USB, Bluetooth, wireless setup)",
                    "Signal Testing (Quality check, artifact detection)",
                    "Calibration Process (Baseline recording, sensitivity)",
                    "Troubleshooting (Common issues, solutions)"
                ],
                "completion_criteria": [
                    "Select EEG device type",
                    "Complete connection process",
                    "Validate signal quality"
                ]
            },
            {
                "step_id": 5,
                "title": "🎯 Learning Session - Live Neural Processing Demo",
                "description": "Experience real-time neural processing",
                "tab_elements": [
                    "Session Parameters (Learning rate, difficulty, duration)",
                    "Start Session Button (Initialize neural processing)",
                    "Real-time Metrics (Alpha/beta waves, attention, coherence)",
                    "Adaptive Controls (Difficulty adjustment, pause/resume)",
                    "Results Dashboard (Performance summary, analytics)"
                ],
                "completion_criteria": [
                    "Configure session parameters",
                    "Run complete learning session",
                    "Review performance results"
                ]
            },
            {
                "step_id": 6,
                "title": "📈 Analytics - Performance Metrics Overview",
                "description": "Analyze learning performance and trends",
                "tab_elements": [
                    "Performance Reports (Accuracy, latency, throughput)",
                    "Trend Analysis (Historical data, progress tracking)",
                    "Custom Filters (Date range, metrics, comparisons)",
                    "Export Options (PDF, Excel, CSV formats)",
                    "Benchmark Comparisons (Industry standards, goals)"
                ],
                "completion_criteria": [
                    "Generate performance report",
                    "Apply custom filters",
                    "Export data successfully"
                ]
            },
            {
                "step_id": 7,
                "title": "👥 Administration - User Management Features",
                "description": "Manage users, roles, and permissions",
                "tab_elements": [
                    "User Management (Add, edit, deactivate users)",
                    "Role Assignment (Admin, instructor, student roles)",
                    "Permission Groups (Access control, feature restrictions)",
                    "Audit Logs (User activity, system changes)",
                    "Security Settings (Password policy, MFA, compliance)"
                ],
                "completion_criteria": [
                    "Create test user account",
                    "Assign user role",
                    "Review audit logs"
                ]
            },
            {
                "step_id": 8,
                "title": "🔗 Integrations - Third-Party System Connections",
                "description": "Connect external systems and services",
                "tab_elements": [
                    "Available Integrations (LMS, EHR, CRM systems)",
                    "Setup Wizard (Step-by-step configuration)",
                    "API Configuration (Keys, endpoints, authentication)",
                    "Testing Tools (Connection validation, data sync)",
                    "Webhook Management (Event notifications, callbacks)"
                ],
                "completion_criteria": [
                    "Review integration options",
                    "Configure test integration",
                    "Validate connection"
                ]
            },
            {
                "step_id": 9,
                "title": "🛠️ API Access - Developer Tools and Customization",
                "description": "Explore API capabilities and customization",
                "tab_elements": [
                    "API Documentation (RESTful endpoints, parameters)",
                    "Code Examples (Python, JavaScript, .NET samples)",
                    "Testing Interface (Interactive API explorer)",
                    "SDK Downloads (Client libraries, documentation)",
                    "Custom Integration (Webhook setup, custom endpoints)"
                ],
                "completion_criteria": [
                    "Review API documentation",
                    "Test API endpoint",
                    "Download SDK"
                ]
            },
            {
                "step_id": 10,
                "title": "🎓 Support & Next Steps - Help Resources and Training",
                "description": "Access support and continue learning",
                "tab_elements": [
                    "Help Center (FAQs, troubleshooting, guides)",
                    "Training Materials (Video tutorials, webinars)",
                    "Support Channels (Chat, email, phone support)",
                    "Community Forum (User discussions, best practices)",
                    "Certification Program (Professional certification path)"
                ],
                "completion_criteria": [
                    "Access help center",
                    "Join community forum",
                    "Explore certification options"
                ]
            }
        ]
        
        # Create TutorialStep objects
        for step_data in tutorial_data:
            step = TutorialStep(
                step_id=step_data["step_id"],
                title=step_data["title"],
                description=step_data["description"],
                tab_elements=step_data["tab_elements"],
                completion_criteria=step_data["completion_criteria"]
            )
            self.steps.append(step)
    
    def _load_progress(self):
        """Load existing tutorial progress"""
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, 'r') as f:
                    progress_data = json.load(f)
                    
                # Restore current step
                self.current_step = progress_data.get('current_step', 0)
                
                # Restore step statuses
                for step in self.steps:
                    step_progress = progress_data.get('steps', {}).get(str(step.step_id), {})
                    if step_progress:
                        step.status = StepStatus(step_progress.get('status', 'not_started'))
                        step.time_spent = step_progress.get('time_spent', 0.0)
                        step.attempts = step_progress.get('attempts', 0)
                        step.last_accessed = step_progress.get('last_accessed')
                        step.notes = step_progress.get('notes', '')
                
                print(f"✅ Progress loaded from previous session")
            except Exception as e:
                print(f"⚠️ Could not load previous progress: {e}")
    
    def _save_progress(self):
        """Save current tutorial progress"""
        try:
            completed_steps = [s.step_id for s in self.steps if s.status == StepStatus.COMPLETED]
            mastered_steps = [s.step_id for s in self.steps if s.status == StepStatus.MASTERED]
            total_time = sum(s.time_spent for s in self.steps)
            
            progress_data = {
                'user_id': self.user_id,
                'session_id': self.session_id,
                'current_step': self.current_step,
                'total_steps': len(self.steps),
                'completed_steps': completed_steps,
                'mastered_steps': mastered_steps,
                'total_time': total_time,
                'start_time': datetime.now().isoformat(),
                'last_update': datetime.now().isoformat(),
                'completion_percentage': (len(completed_steps) / len(self.steps)) * 100,
                'steps': {
                    str(step.step_id): {
                        'status': step.status.value,
                        'time_spent': step.time_spent,
                        'attempts': step.attempts,
                        'last_accessed': step.last_accessed,
                        'notes': step.notes
                    } for step in self.steps
                }
            }
            
            with open(self.progress_file, 'w') as f:
                json.dump(progress_data, f, indent=2)
                
            print(f"💾 Progress saved successfully")
        except Exception as e:
            print(f"⚠️ Could not save progress: {e}")
    
    def display_progress_bar(self):
        """Display visual progress bar"""
        completed = len([s for s in self.steps if s.status in [StepStatus.COMPLETED, StepStatus.MASTERED]])
        total = len(self.steps)
        percentage = (completed / total) * 100
        
        bar_length = 50
        filled_length = int(bar_length * completed // total)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        
        print(f"\n📊 Tutorial Progress: [{bar}] {percentage:.1f}% ({completed}/{total} steps)")
        print(f"⏱️  Time spent: {sum(s.time_spent for s in self.steps):.1f} minutes")
    
    def display_current_step(self):
        """Display current step with tab navigation"""
        if 0 <= self.current_step < len(self.steps):
            step = self.steps[self.current_step]
            
            # Update step access info
            step.last_accessed = datetime.now().isoformat()
            step.attempts += 1
            if step.status == StepStatus.NOT_STARTED:
                step.status = StepStatus.IN_PROGRESS
            
            print("\n" + "="*70)
            print(f"📚 Step {step.step_id}/10: {step.title}")
            print("="*70)
            print(f"📝 {step.description}")
            print("\n🎯 Tab Through These Elements:")
            
            for i, element in enumerate(step.tab_elements, 1):
                status_icon = "▶️" if i == 1 else "⭐"
                print(f"  {status_icon} Tab {i}: {element}")
            
            print("\n✅ Completion Criteria:")
            for criterion in step.completion_criteria:
                print(f"  • {criterion}")
            
            print(f"\n📊 Status: {step.status.value.replace('_', ' ').title()}")
            if step.time_spent > 0:
                print(f"⏱️  Time spent: {step.time_spent:.1f} minutes")
            
            self.display_navigation_controls()
        else:
            print("❌ Invalid step number")
    
    def display_navigation_controls(self):
        """Display available navigation controls"""
        print("\n🎮 Navigation Controls:")
        print("┌─────────────────────────────────────────────────────────────┐")
        print("│ TAB          - Next element    │ SHIFT+TAB    - Previous     │")
        print("│ ENTER        - Complete step   │ SPACE        - Mark reviewed│")
        print("│ ◀️ B          - Back step      │ ▶️ N          - Next step   │")
        print("│ 🔄 R          - Restart        │ 💾 S          - Save        │")
        print("│ 📋 M          - Menu/Jump      │ ESC          - Exit         │")
        print("└─────────────────────────────────────────────────────────────┘")
    
    def navigate_to_step(self, step_number: int):
        """Navigate to specific step"""
        if 1 <= step_number <= len(self.steps):
            self.current_step = step_number - 1
            self.display_current_step()
            self._save_progress()
        else:
            print(f"❌ Invalid step number. Please choose 1-{len(self.steps)}")
    
    def next_step(self):
        """Move to next step"""
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.display_current_step()
            self._save_progress()
        else:
            print("🎉 Congratulations! You've reached the end of the tutorial!")
            self.display_completion_summary()
    
    def previous_step(self):
        """Move to previous step"""
        if self.current_step > 0:
            self.current_step -= 1
            self.display_current_step()
            self._save_progress()
        else:
            print("📝 You're already at the first step")
    
    def complete_current_step(self):
        """Mark current step as completed"""
        if 0 <= self.current_step < len(self.steps):
            step = self.steps[self.current_step]
            step.status = StepStatus.COMPLETED
            
            print(f"✅ Step {step.step_id} marked as completed!")
            print("🎯 Great job! Ready to move to the next step?")
            
            self._save_progress()
            self.display_progress_bar()
    
    def mark_step_for_review(self):
        """Mark current step for review"""
        if 0 <= self.current_step < len(self.steps):
            step = self.steps[self.current_step]
            step.status = StepStatus.REVIEW
            
            print(f"🔄 Step {step.step_id} marked for review")
            self._save_progress()
    
    def display_step_menu(self):
        """Display step selection menu"""
        print("\n📋 Tutorial Step Menu:")
        print("="*50)
        
        for step in self.steps:
            status_icon = {
                StepStatus.NOT_STARTED: "🔲",
                StepStatus.IN_PROGRESS: "🟡", 
                StepStatus.COMPLETED: "✅",
                StepStatus.MASTERED: "⭐",
                StepStatus.REVIEW: "🔄"
            }.get(step.status, "🔲")
            
            current_marker = "👈" if step.step_id - 1 == self.current_step else "  "
            print(f"{status_icon} {step.step_id:2d}. {step.title} {current_marker}")
        
        print("\n💡 Enter step number (1-10) or 0 to return:")
    
    def display_completion_summary(self):
        """Display tutorial completion summary"""
        completed = [s for s in self.steps if s.status == StepStatus.COMPLETED]
        mastered = [s for s in self.steps if s.status == StepStatus.MASTERED]
        total_time = sum(s.time_spent for s in self.steps)
        
        print("\n🎉 Tutorial Completion Summary")
        print("="*50)
        print(f"✅ Completed Steps: {len(completed)}/{len(self.steps)}")
        print(f"⭐ Mastered Steps: {len(mastered)}/{len(self.steps)}")
        print(f"⏱️  Total Time: {total_time:.1f} minutes")
        print(f"🏆 Completion Rate: {(len(completed)/len(self.steps))*100:.1f}%")
        
        if len(completed) == len(self.steps):
            print("\n🥇 CONGRATULATIONS! Tutorial Complete!")
            print("🚀 You're ready to use the L.I.F.E. Platform!")
        else:
            remaining = len(self.steps) - len(completed)
            print(f"\n📝 {remaining} steps remaining to complete")
    
    def restart_tutorial(self):
        """Restart tutorial from beginning"""
        print("🔄 Restarting tutorial...")
        self.current_step = 0
        
        # Reset all steps
        for step in self.steps:
            step.status = StepStatus.NOT_STARTED
            step.time_spent = 0.0
            step.attempts = 0
            step.last_accessed = None
            step.notes = ""
        
        self._save_progress()
        print("✅ Tutorial reset successfully!")
    
    async def run_interactive_tutorial(self):
        """Main interactive tutorial loop"""
        print("🎮 Welcome to the L.I.F.E. Platform Self-Guided Tutorial!")
        print("🎯 Use Tab navigation to explore each step thoroughly")
        self.display_progress_bar()
        self.display_current_step()
        
        while True:
            try:
                print("\n💬 Enter command (or 'help' for options): ", end="")
                user_input = input().strip().lower()
                
                if user_input in ['exit', 'quit', 'esc']:
                    print("💾 Saving progress and exiting...")
                    self._save_progress()
                    break
                
                elif user_input in ['next', 'n', '>']:
                    self.next_step()
                
                elif user_input in ['back', 'previous', 'b', '<']:
                    self.previous_step()
                
                elif user_input in ['complete', 'done', 'c']:
                    self.complete_current_step()
                
                elif user_input in ['review', 'r']:
                    self.mark_step_for_review()
                
                elif user_input in ['menu', 'm']:
                    self.display_step_menu()
                    try:
                        choice = int(input())
                        if choice == 0:
                            continue
                        elif 1 <= choice <= len(self.steps):
                            self.navigate_to_step(choice)
                    except ValueError:
                        print("❌ Invalid input. Please enter a number.")
                
                elif user_input in ['save', 's']:
                    self._save_progress()
                
                elif user_input in ['restart']:
                    confirm = input("🔄 Restart tutorial? All progress will be lost (y/N): ")
                    if confirm.lower() in ['y', 'yes']:
                        self.restart_tutorial()
                
                elif user_input in ['progress', 'p']:
                    self.display_progress_bar()
                
                elif user_input in ['summary']:
                    self.display_completion_summary()
                
                elif user_input in ['help', 'h', '?']:
                    self.display_help()
                
                elif user_input.isdigit():
                    step_num = int(user_input)
                    self.navigate_to_step(step_num)
                
                else:
                    print("❌ Unknown command. Type 'help' for available options.")
            
            except KeyboardInterrupt:
                print("\n\n💾 Saving progress and exiting...")
                self._save_progress()
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def display_help(self):
        """Display help information"""
        print("\n📚 Tutorial Help & Commands:")
        print("="*50)
        print("Navigation:")
        print("  next, n, >     - Move to next step")
        print("  back, b, <     - Move to previous step")
        print("  1-10           - Jump to specific step")
        print("  menu, m        - Show step selection menu")
        print("")
        print("Actions:")
        print("  complete, c    - Mark current step as completed")
        print("  review, r      - Mark step for review")
        print("  save, s        - Save current progress")
        print("  restart        - Restart entire tutorial")
        print("")
        print("Information:")
        print("  progress, p    - Show progress bar")
        print("  summary        - Show completion summary")
        print("  help, h, ?     - Show this help")
        print("  exit, quit     - Save and exit tutorial")

def main():
    """
    🚀 L.I.F.E. Platform Self-Guided Tutorial System
    Enhanced with Tab Navigation and Progress Tracking
    """
    
    print("🎮 L.I.F.E. Platform - Self-Guided Tutorial System")
    print("=" * 70)
    print("🎯 Enhanced Tab Navigation with Back/Forward Controls")
    print("📊 Complete Step Tracking and Progress Persistence")
    print("🔄 Non-Linear Navigation with Jump-to-Step Capability")
    print("=" * 70)
    
    # Get user ID
    user_id = input("👤 Enter your user ID (or press Enter for default): ").strip()
    if not user_id:
        user_id = "default_user"
    
    # Initialize tutorial system
    tutorial = SelfGuidedTutorial(user_id=user_id)
    
    # Run interactive tutorial
    try:
        asyncio.run(tutorial.run_interactive_tutorial())
    except Exception as e:
        print(f"❌ Tutorial system error: {e}")
        tutorial._save_progress()
    
    print("\n🎉 Thank you for using the L.I.F.E. Platform Tutorial System!")
    print("🚀 Ready to start your neural learning journey!")

if __name__ == "__main__":
    main()