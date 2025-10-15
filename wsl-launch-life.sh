#!/bin/bash
# L.I.F.E Platform WSL/Linux Launcher & Cloud Uploader
# Handles path conversion and cloud storage

echo ""
echo "🧠 ========================================"
echo "   L.I.F.E PLATFORM WSL CLOUD LAUNCHER"
echo "========================================"
echo ""
echo "🔍 Detecting environment and paths..."

# Check if we're in WSL
if grep -qi microsoft /proc/version 2>/dev/null; then
    echo "✅ WSL Environment Detected"
    WSL_MODE=true
    # Convert Windows path to WSL path
    WIN_PATH="/mnt/c/Users/Sergio Paya Borrull/OneDrive/Documents/GitHub/.vscode/New folder/SergiLIFE-life-azure-system/SergiLIFE-life-azure-system"
else
    echo "✅ Linux Environment Detected"
    WSL_MODE=false
    WIN_PATH="."
fi

echo "📂 Looking for L.I.F.E Platform files..."

# Check multiple possible locations
POSSIBLE_PATHS=(
    "$WIN_PATH"
    "/mnt/c/Users/Sergio*/OneDrive/Documents/GitHub*/*SergiLIFE*"
    "~/OneDrive/Documents/GitHub*/*SergiLIFE*"
    "."
    "../"
)

FOUND_PATH=""
for path in "${POSSIBLE_PATHS[@]}"; do
    if [ -d "$path" ] && [ -f "$path/L.I.F.E_PLATFORM_COMPLETE_WITH_TABS.html" ]; then
        FOUND_PATH="$path"
        break
    fi
done

if [ -n "$FOUND_PATH" ]; then
    echo "✅ L.I.F.E Platform found at: $FOUND_PATH"
    cd "$FOUND_PATH"
    
    echo ""
    echo "📁 Available platform files:"
    ls -la *.html 2>/dev/null || echo "   No HTML files found"
    
    echo ""
    echo "🌐 Opening L.I.F.E Platform Complete Edition..."
    
    # Try different browser opening methods
    PLATFORM_FILE="$FOUND_PATH/L.I.F.E_PLATFORM_COMPLETE_WITH_TABS.html"
    
    if command -v wslview >/dev/null 2>&1; then
        wslview "$PLATFORM_FILE"
        echo "✅ Opened with wslview (WSL)"
    elif command -v xdg-open >/dev/null 2>&1; then
        xdg-open "$PLATFORM_FILE"
        echo "✅ Opened with xdg-open (Linux)"
    elif command -v open >/dev/null 2>&1; then
        open "$PLATFORM_FILE"
        echo "✅ Opened with open (macOS)"
    else
        echo "🌐 Manual browser opening required:"
        echo "   File location: $PLATFORM_FILE"
        echo "   Copy this path to your browser or file manager"
    fi
    
else
    echo "❌ L.I.F.E Platform files not found!"
    echo "🔍 Current directory contents:"
    ls -la
    echo ""
    echo "📂 Please navigate to the correct directory or check these locations:"
    for path in "${POSSIBLE_PATHS[@]}"; do
        echo "   • $path"
    done
fi

echo ""
echo "☁️  CLOUD STORAGE SETUP"
echo "========================"
echo "💾 To save space on your computer, consider:"
echo "   1. Azure Blob Storage (free tier available)"
echo "   2. OneDrive sync (already in OneDrive folder)"
echo "   3. GitHub repository (version control)"
echo ""
echo "🚀 L.I.F.E Platform Ready!"
echo "📅 October 15, 2025 - Strategic Partnership Demo"
echo ""