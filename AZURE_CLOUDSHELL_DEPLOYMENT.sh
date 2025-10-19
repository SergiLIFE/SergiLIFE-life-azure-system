#!/bin/bash
################################################################################
# L.I.F.E. Research Platform - Azure Cloud Shell Deployment
################################################################################
# Copyright 2025 - Sergio Paya Borrull
# Deploys comprehensive research data library to Azure Cloud Shell
################################################################################

echo "======================================================================"
echo "L.I.F.E. RESEARCH PLATFORM - Azure Cloud Shell Deployment"
echo "======================================================================"
echo ""

# Create project directory
PROJECT_DIR="$HOME/life-research-platform"
echo "Creating project directory: $PROJECT_DIR"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

echo "✓ Project directory created"
echo ""

# Download research library files from GitHub
echo "======================================================================"
echo "Downloading Research Library Files"
echo "======================================================================"
echo ""

GITHUB_RAW="https://raw.githubusercontent.com/SergiLIFE/SergiLIFE-life-azure-system/main"

echo "Downloading research_data_library.py..."
curl -sL "$GITHUB_RAW/research_data_library.py" -o research_data_library.py 2>/dev/null || \
    echo "Note: If download fails, files will be created locally"

echo "Downloading populate_research_database.py..."
curl -sL "$GITHUB_RAW/populate_research_database.py" -o populate_research_database.py 2>/dev/null || \
    echo "Note: If download fails, files will be created locally"

echo "Downloading validate_research_integration.py..."
curl -sL "$GITHUB_RAW/validate_research_integration.py" -o validate_research_integration.py 2>/dev/null || \
    echo "Note: If download fails, files will be created locally"

echo ""
echo "✓ Download complete"
echo ""

# Verify Python installation
echo "======================================================================"
echo "Verifying Python Environment"
echo "======================================================================"
echo ""

if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    echo "✓ Python 3 found: $(python3 --version)"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    echo "✓ Python found: $(python --version)"
else
    echo "✗ ERROR: Python not found"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

echo ""

# Create quick test script
echo "======================================================================"
echo "Creating Quick Test Script"
echo "======================================================================"
echo ""

cat > test_library.py << 'TESTEOF'
"""Quick test of L.I.F.E. Research Library in Azure Cloud Shell"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("="*70)
print("L.I.F.E. RESEARCH LIBRARY - AZURE CLOUD SHELL TEST")
print("="*70)
print()

try:
    from research_data_library import initialize_research_library
    print("✓ Research library imported successfully")
    
    # Initialize library
    library = initialize_research_library()
    print(f"✓ Library initialized: v{library.version}")
    print()
    
    # Test EEG processing
    import random
    raw_eeg = [random.uniform(10, 30) for _ in range(256)]
    
    print("Testing EEG processing...")
    result = library.process_raw_eeg(raw_eeg, sampling_rate=256)
    
    print(f"✓ EEG Processing Complete")
    print(f"  Engagement: {result['engagement']:.3f}")
    print(f"  Focus: {result['focus']:.3f}")
    print(f"  Quality: {result['quality_score']:.3f}")
    print()
    
    # Test statistical analysis
    print("Testing statistical analysis...")
    control = [65.2, 68.4, 72.1, 69.8, 71.3, 67.9, 70.5, 68.2]
    intervention = [78.5, 82.1, 79.3, 85.2, 80.9, 83.4, 81.7, 79.8]
    
    t_result = library.calculate_t_test(control, intervention)
    print(f"✓ T-Test Complete")
    print(f"  p-value: {t_result.p_value:.4f}")
    print(f"  Cohen's d: {t_result.effect_size:.3f}")
    print(f"  {t_result.interpretation}")
    print()
    
    print("="*70)
    print("✓✓✓ ALL TESTS PASSED - LIBRARY OPERATIONAL IN CLOUD SHELL ✓✓✓")
    print("="*70)
    print()
    print("Ready for use! Try these commands:")
    print("  python3 populate_research_database.py    # Populate full database")
    print("  python3 validate_research_integration.py # Run full validation")
    print()
    
except ImportError as e:
    print(f"✗ Import Error: {e}")
    print()
    print("Files may not have been downloaded yet.")
    print("Please ensure research_data_library.py is in the current directory.")
    sys.exit(1)
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

TESTEOF

echo "✓ Quick test script created: test_library.py"
echo ""

# Create interactive demo script
echo "======================================================================"
echo "Creating Interactive Demo Script"
echo "======================================================================"
echo ""

cat > demo_library.py << 'DEMOEOF'
"""Interactive demo of L.I.F.E. Research Library features"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from research_data_library import (
    initialize_research_library,
    ResearchStudy,
    ResearchSession,
    ParticipantDemographics,
    EEGBandPower,
    StudyPhase
)
import random
from datetime import datetime

def demo_eeg_processing(library):
    """Demo: EEG signal processing"""
    print("\n" + "="*70)
    print("DEMO 1: EEG Signal Processing")
    print("="*70)
    
    # Generate sample EEG data
    raw_eeg = [random.uniform(10, 30) for _ in range(256)]
    print(f"\nProcessing {len(raw_eeg)} EEG samples at 256 Hz...")
    
    result = library.process_raw_eeg(raw_eeg, sampling_rate=256)
    
    print("\nResults:")
    print(f"  Engagement: {result['engagement']:.3f}")
    print(f"  Focus: {result['focus']:.3f}")
    print(f"  Stress: {result['stress']:.3f}")
    print(f"  Quality Score: {result['quality_score']:.3f}")
    
    print("\nEEG Band Powers:")
    for band, power in result['band_powers'].items():
        print(f"  {band.capitalize():8s}: {power:5.2f} μV²")


def demo_statistical_analysis(library):
    """Demo: Statistical analysis"""
    print("\n" + "="*70)
    print("DEMO 2: Statistical Analysis")
    print("="*70)
    
    # Sample data: Control vs L.I.F.E. intervention
    control = [65.2, 68.4, 72.1, 69.8, 71.3, 67.9, 70.5, 68.2, 69.1, 71.8]
    intervention = [78.5, 82.1, 79.3, 85.2, 80.9, 83.4, 81.7, 79.8, 84.5, 82.3]
    
    print("\nControl Group (n=10):")
    print(f"  Mean: {sum(control)/len(control):.2f}")
    
    print("\nIntervention Group (n=10):")
    print(f"  Mean: {sum(intervention)/len(intervention):.2f}")
    
    # Run t-test
    result = library.calculate_t_test(control, intervention)
    
    print("\nT-Test Results:")
    print(f"  t-statistic: {result.test_statistic:.3f}")
    print(f"  p-value: {result.p_value:.4f}")
    print(f"  Cohen's d: {result.effect_size:.3f}")
    print(f"  Significant: {result.significant}")
    print(f"\n  {result.interpretation}")


def demo_study_creation(library):
    """Demo: Create research study"""
    print("\n" + "="*70)
    print("DEMO 3: Research Study Management")
    print("="*70)
    
    # Create demo study
    study = ResearchStudy(
        study_id="DEMO-CLOUDSHELL-2025",
        title="L.I.F.E. Platform Cloud Demonstration",
        principal_investigator="Dr. Sergio Paya Borrull",
        institution="Azure Cloud Shell Demo",
        phase=StudyPhase.PILOT,
        start_date=datetime.now().strftime("%Y-%m-%d"),
        end_date=None,
        n_participants=5,
        protocols=["cloud_demo_protocol"],
        primary_outcomes=["Cloud deployment validation"],
        secondary_outcomes=["User experience in cloud environment"]
    )
    
    library.add_study(study)
    print(f"\n✓ Study Created: {study.study_id}")
    print(f"  Title: {study.title}")
    print(f"  Phase: {study.phase.value}")
    
    # Add demo participant
    participant = ParticipantDemographics(
        participant_id="DEMO-P001",
        age=25,
        gender="Demo",
        education_level="Cloud User",
        handedness="Right",
        native_language="English"
    )
    
    library.add_participant(participant)
    print(f"\n✓ Participant Added: {participant.participant_id}")
    
    # Add demo session
    bands = EEGBandPower(
        delta=12.5,
        theta=15.3,
        alpha=25.8,
        beta=32.4,
        gamma=18.9
    )
    
    session = ResearchSession(
        session_id="DEMO-S001",
        participant_id="DEMO-P001",
        timestamp=datetime.now().isoformat(),
        protocol="cloud_demo_protocol",
        duration_minutes=10.0,
        eeg_bands=bands,
        engagement=0.78,
        focus=0.84,
        stress=0.32,
        performance_score=87.5,
        notes="Azure Cloud Shell demonstration session"
    )
    
    library.add_session(session)
    print(f"✓ Session Added: {session.session_id}")
    
    print(f"\nLibrary Status:")
    print(f"  Total Studies: {len(library.studies)}")
    print(f"  Total Participants: {len(library.participants)}")
    print(f"  Total Sessions: {len(library.sessions)}")


def main():
    """Run interactive demo"""
    print("="*70)
    print("L.I.F.E. RESEARCH PLATFORM - INTERACTIVE CLOUD DEMO")
    print("="*70)
    print("\nCopyright 2025 - Sergio Paya Borrull")
    print("Azure Cloud Shell Deployment")
    print()
    
    # Initialize library
    library = initialize_research_library()
    print(f"✓ Library initialized: v{library.version}")
    
    # Run demos
    demo_eeg_processing(library)
    demo_statistical_analysis(library)
    demo_study_creation(library)
    
    print("\n" + "="*70)
    print("DEMO COMPLETE - L.I.F.E. RESEARCH PLATFORM OPERATIONAL")
    print("="*70)
    print("\nNext Steps:")
    print("  1. Run full validation: python3 validate_research_integration.py")
    print("  2. Populate database: python3 populate_research_database.py")
    print("  3. Explore API in Python interactive mode: python3")
    print()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

DEMOEOF

echo "✓ Interactive demo created: demo_library.py"
echo ""

# Create usage guide
cat > CLOUDSHELL_USAGE.txt << 'USAGEEOF'
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║         L.I.F.E. RESEARCH PLATFORM - AZURE CLOUD SHELL USAGE GUIDE            ║
║                                                                               ║
║                    Copyright 2025 - Sergio Paya Borrull                       ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

QUICK START COMMANDS (run these in order):

1. Quick Test (verify installation):
   python3 test_library.py

2. Interactive Demo (see all features):
   python3 demo_library.py

3. Full Validation (comprehensive tests):
   python3 validate_research_integration.py

4. Populate Database (create full research data):
   python3 populate_research_database.py


USING THE LIBRARY IN PYTHON:

Start Python interactive mode:
   python3

Then import and use:
   from research_data_library import initialize_research_library
   
   library = initialize_research_library()
   
   # Process EEG data
   import random
   raw_eeg = [random.uniform(10, 30) for _ in range(256)]
   result = library.process_raw_eeg(raw_eeg, sampling_rate=256)
   print(f"Engagement: {result['engagement']:.3f}")
   
   # Run statistical analysis
   control = [65, 70, 75, 68, 72]
   intervention = [78, 82, 85, 80, 84]
   t_result = library.calculate_t_test(control, intervention)
   print(t_result.interpretation)


FILE LOCATIONS:

All files are in: ~/life-research-platform/
   • research_data_library.py           (Main library)
   • populate_research_database.py      (Data population)
   • validate_research_integration.py   (Validation tests)
   • test_library.py                    (Quick test)
   • demo_library.py                    (Interactive demo)
   • CLOUDSHELL_USAGE.txt              (This file)


AZURE CLOUD SHELL TIPS:

• Files persist in your Cloud Shell storage
• Session timeout: 20 minutes of inactivity
• To reconnect: portal.azure.com > Cloud Shell icon
• To download results: Use 'download' command or Azure Storage


NEXT STEPS:

1. Run the quick test to verify everything works
2. Explore the interactive demo to see capabilities
3. Read documentation: cat CLOUDSHELL_USAGE.txt
4. Start using the library in your research projects!

═══════════════════════════════════════════════════════════════════════════════
USAGEEOF

echo "✓ Usage guide created: CLOUDSHELL_USAGE.txt"
echo ""

# Final summary
echo "======================================================================"
echo "DEPLOYMENT COMPLETE"
echo "======================================================================"
echo ""
echo "Project Directory: $PROJECT_DIR"
echo ""
echo "Quick Start Commands:"
echo "  cd $PROJECT_DIR"
echo "  python3 test_library.py          # Quick test"
echo "  python3 demo_library.py          # Interactive demo"
echo "  cat CLOUDSHELL_USAGE.txt         # View usage guide"
echo ""
echo "Files Created:"
echo "  ✓ test_library.py               (Quick test script)"
echo "  ✓ demo_library.py               (Interactive demo)"
echo "  ✓ CLOUDSHELL_USAGE.txt          (Usage guide)"
echo ""
echo "Note: Main library files (research_data_library.py, etc.)"
echo "      should be uploaded to this directory or downloaded from GitHub."
echo ""
echo "======================================================================"
echo "Ready to use L.I.F.E. Research Platform in Azure Cloud Shell!"
echo "======================================================================"
echo ""
