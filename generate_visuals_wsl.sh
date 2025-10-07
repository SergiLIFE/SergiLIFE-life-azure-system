#!/bin/bash
# L.I.F.E Platform Visual Generator - WSL/Linux Compatible
# Run this in your bash terminal

echo "============================================================"
echo "L.I.F.E PLATFORM - VISUAL GENERATOR (WSL/Linux)"
echo "============================================================"
echo ""

# Convert Windows path to WSL path
WSL_PATH="/mnt/c/Users/Sergio Paya Borrull/OneDrive/Documents/GitHub/.vscode/New folder/SergiLIFE-life-azure-system/SergiLIFE-life-azure-system"

echo "Navigating to project directory..."
cd "$WSL_PATH" || {
    echo "❌ Error: Cannot find project directory"
    echo ""
    echo "Current directory: $(pwd)"
    echo "Expected: $WSL_PATH"
    echo ""
    echo "ALTERNATIVE: Just double-click DOUBLE_CLICK_ME.bat in File Explorer!"
    exit 1
}

echo "✅ Found project directory"
echo ""

# Check if Python script exists
if [ ! -f "generate_visuals_standalone.py" ]; then
    echo "❌ Error: generate_visuals_standalone.py not found"
    echo ""
    echo "ALTERNATIVE: Double-click DOUBLE_CLICK_ME.bat in File Explorer!"
    exit 1
fi

echo "Running visual generator..."
echo ""

# Try python3 first (Linux standard), then python
if command -v python3 &> /dev/null; then
    python3 generate_visuals_standalone.py
elif command -v python &> /dev/null; then
    python generate_visuals_standalone.py
else
    echo "❌ Error: Python not found in WSL"
    echo ""
    echo "Install Python in WSL:"
    echo "  sudo apt update"
    echo "  sudo apt install python3 python3-pip"
    echo ""
    echo "OR EASIER: Just double-click DOUBLE_CLICK_ME.bat in Windows File Explorer!"
    exit 1
fi

echo ""
echo "============================================================"
echo "Done! Check marketplace_assets folder in File Explorer"
echo "============================================================"
