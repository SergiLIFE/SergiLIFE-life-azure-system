# L.I.F.E. Research Platform - PowerShell Deployment for Azure Cloud Shell
# Copyright 2025 - Sergio Paya Borrull
# PowerShell script for deploying research library in Azure Cloud Shell

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "L.I.F.E. RESEARCH PLATFORM - Azure Cloud Shell Deployment (PowerShell)" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Create project directory
$projectDir = "$HOME/life-research-platform"
Write-Host "Creating project directory: $projectDir" -ForegroundColor Yellow

if (-not (Test-Path $projectDir)) {
    New-Item -ItemType Directory -Path $projectDir -Force | Out-Null
    Write-Host "✓ Project directory created" -ForegroundColor Green
} else {
    Write-Host "✓ Project directory already exists" -ForegroundColor Green
}

Set-Location $projectDir
Write-Host ""

# Create Python test script
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Creating Quick Test Script" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

$testScript = @'
"""L.I.F.E. Research Library - Quick Test for Azure Cloud Shell"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("="*70)
print("L.I.F.E. RESEARCH LIBRARY - QUICK TEST")
print("="*70)
print()

try:
    from research_data_library import initialize_research_library
    print("✓ Successfully imported research_data_library")
    
    import random
    
    # Initialize library
    library = initialize_research_library()
    print(f"✓ Library v{library.version} initialized")
    print()
    
    # Test EEG processing
    print("Testing EEG processing...")
    raw_eeg = [random.uniform(10, 30) for _ in range(256)]
    result = library.process_raw_eeg(raw_eeg, sampling_rate=256)
    
    print(f"✓ Engagement: {result['engagement']:.3f}")
    print(f"✓ Focus: {result['focus']:.3f}")
    print(f"✓ Quality: {result['quality_score']:.3f}")
    print()
    
    # Test statistical analysis
    print("Testing statistical analysis...")
    control = [65, 68, 72, 70, 71]
    intervention = [78, 82, 79, 85, 81]
    
    t_result = library.calculate_t_test(control, intervention)
    print(f"✓ p-value: {t_result.p_value:.4f}")
    print(f"✓ Cohen's d: {t_result.effect_size:.3f}")
    print()
    
    print("="*70)
    print("✓✓✓ ALL TESTS PASSED - LIBRARY OPERATIONAL ✓✓✓")
    print("="*70)
    
except ImportError as e:
    print(f"✗ Import Error: {e}")
    print()
    print("The research library files are not in this directory.")
    print("Please upload these files using the Cloud Shell upload button:")
    print("  1. research_data_library.py")
    print("  2. populate_research_database.py")
    print("  3. validate_research_integration.py")
    print()
    print(f"Upload them to: {os.getcwd()}")
    sys.exit(1)
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
'@

Set-Content -Path "test_library.py" -Value $testScript
Write-Host "✓ Created: test_library.py" -ForegroundColor Green
Write-Host ""

# Create interactive demo script
$demoScript = @'
"""L.I.F.E. Research Library - Interactive Demo"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from research_data_library import initialize_research_library
import random

def demo():
    print("="*70)
    print("L.I.F.E. RESEARCH PLATFORM - INTERACTIVE DEMO")
    print("="*70)
    print()
    
    # Initialize
    library = initialize_research_library()
    print(f"Library Version: {library.version}")
    print()
    
    # Demo 1: EEG Processing
    print("DEMO 1: EEG Signal Processing")
    print("-"*70)
    for i in range(3):
        raw_eeg = [random.uniform(10, 30) for _ in range(256)]
        result = library.process_raw_eeg(raw_eeg, sampling_rate=256)
        print(f"Sample {i+1}: Engagement={result['engagement']:.3f}, Focus={result['focus']:.3f}")
    print()
    
    # Demo 2: Statistical Analysis
    print("DEMO 2: Statistical Comparison")
    print("-"*70)
    control = [65, 68, 72, 70, 71, 69, 73, 67]
    intervention = [78, 82, 79, 85, 81, 83, 80, 84]
    
    t_result = library.calculate_t_test(control, intervention)
    print(f"Control Mean: {sum(control)/len(control):.2f}")
    print(f"Intervention Mean: {sum(intervention)/len(intervention):.2f}")
    print(f"Result: {t_result.interpretation}")
    print()
    
    print("="*70)
    print("DEMO COMPLETE")
    print("="*70)

if __name__ == "__main__":
    try:
        demo()
    except ImportError:
        print("ERROR: research_data_library.py not found in this directory")
        print("Please upload the library files first")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
'@

Set-Content -Path "demo_library.py" -Value $demoScript
Write-Host "✓ Created: demo_library.py" -ForegroundColor Green
Write-Host ""

# Create usage instructions
$usageInstructions = @"
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║      L.I.F.E. RESEARCH PLATFORM - AZURE CLOUD SHELL USAGE (PowerShell)        ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

IMPORTANT: You are in PowerShell, not Bash!

CURRENT LOCATION: $projectDir

FILES NEEDED (MUST UPLOAD):
  1. research_data_library.py
  2. populate_research_database.py  
  3. validate_research_integration.py

HOW TO UPLOAD FILES:
  1. Click the Upload/Download button (📤) in Cloud Shell toolbar
  2. Select "Upload"
  3. Choose each of the 3 files above from your local machine
  4. They will upload to your home directory

AFTER UPLOADING, MOVE FILES HERE:
  Move-Item ~/research_data_library.py .
  Move-Item ~/populate_research_database.py .
  Move-Item ~/validate_research_integration.py .

VERIFY FILES ARE HERE:
  Get-ChildItem *.py

RUN QUICK TEST:
  python3 test_library.py

RUN INTERACTIVE DEMO:
  python3 demo_library.py

RUN FULL VALIDATION:
  python3 validate_research_integration.py

POPULATE FULL DATABASE:
  python3 populate_research_database.py

SWITCH TO BASH (if you prefer):
  bash
  # Then you can use Linux commands

═══════════════════════════════════════════════════════════════════════════════

COMMON POWERSHELL COMMANDS:

List files:              Get-ChildItem  (or 'ls')
Change directory:        Set-Location   (or 'cd')
Show current path:       Get-Location   (or 'pwd')
Create directory:        New-Item -ItemType Directory -Path <path>
Move file:               Move-Item <source> <destination>
Copy file:               Copy-Item <source> <destination>
View file:               Get-Content <file>  (or 'cat')
Run Python:              python3 <script.py>

═══════════════════════════════════════════════════════════════════════════════
"@

Set-Content -Path "POWERSHELL_USAGE.txt" -Value $usageInstructions
Write-Host "✓ Created: POWERSHELL_USAGE.txt" -ForegroundColor Green
Write-Host ""

# Summary
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "SETUP COMPLETE" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Current Directory: " -NoNewline -ForegroundColor Yellow
Write-Host $projectDir -ForegroundColor White
Write-Host ""

Write-Host "Files Created:" -ForegroundColor Yellow
Write-Host "  ✓ test_library.py         (Quick test script)" -ForegroundColor Green
Write-Host "  ✓ demo_library.py         (Interactive demo)" -ForegroundColor Green
Write-Host "  ✓ POWERSHELL_USAGE.txt    (Usage guide)" -ForegroundColor Green
Write-Host ""

Write-Host "NEXT STEPS:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. UPLOAD THE 3 PYTHON LIBRARY FILES:" -ForegroundColor Cyan
Write-Host "   - Click Upload button (📤) in Cloud Shell toolbar" -ForegroundColor White
Write-Host "   - Upload these files from your computer:" -ForegroundColor White
Write-Host "     • research_data_library.py" -ForegroundColor White
Write-Host "     • populate_research_database.py" -ForegroundColor White
Write-Host "     • validate_research_integration.py" -ForegroundColor White
Write-Host ""

Write-Host "2. MOVE FILES TO THIS DIRECTORY:" -ForegroundColor Cyan
Write-Host "   Move-Item ~/research_data_library.py ." -ForegroundColor White
Write-Host "   Move-Item ~/populate_research_database.py ." -ForegroundColor White
Write-Host "   Move-Item ~/validate_research_integration.py ." -ForegroundColor White
Write-Host ""

Write-Host "3. VERIFY FILES:" -ForegroundColor Cyan
Write-Host "   Get-ChildItem *.py" -ForegroundColor White
Write-Host ""

Write-Host "4. RUN QUICK TEST:" -ForegroundColor Cyan
Write-Host "   python3 test_library.py" -ForegroundColor White
Write-Host ""

Write-Host "OR SWITCH TO BASH:" -ForegroundColor Yellow
Write-Host "   bash" -ForegroundColor White
Write-Host ""

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "View usage guide: " -NoNewline -ForegroundColor Yellow
Write-Host "Get-Content POWERSHELL_USAGE.txt" -ForegroundColor White
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""
