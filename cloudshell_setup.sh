#!/bin/bash
# Azure Cloud Shell Setup Script for L.I.F.E Platform Screenshot Generation
# Run this in Cloud Shell to set up Python environment and generate screenshots

echo "=================================================="
echo "L.I.F.E Platform - Azure Cloud Shell Setup"
echo "=================================================="
echo ""

# Check Python version
echo "Checking Python installation..."
python3 --version

# Install Pillow in Cloud Shell (user space)
echo ""
echo "Installing Pillow library..."
pip install --user Pillow

# Create output directory
echo ""
echo "Creating output directory..."
mkdir -p marketplace_assets
mkdir -p logs

# Check if installation was successful
echo ""
echo "Verifying Pillow installation..."
python3 -c "from PIL import Image; print('✅ Pillow installed successfully!')" || echo "❌ Pillow installation failed"

echo ""
echo "=================================================="
echo "Setup complete! Now you can run:"
echo "  python3 cloudshell_screenshot_generator.py"
echo "=================================================="
