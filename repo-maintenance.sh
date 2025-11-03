#!/bin/bash
# Repository Maintenance Script
# Implements the guidelines from REPOSITORY_GUIDELINES.md

echo "=========================================="
echo "REPOSITORY MAINTENANCE SCRIPT"
echo "=========================================="
echo ""

# Check for problematic file patterns
echo "1. CHECKING FOR PROBLEMATIC FILE PATTERNS..."
echo "------------------------------------------"
echo "Files with problematic prefixes:"
find . -name "*EMERGENCY*" -o -name "*QUICK*" -o -name "*IMMEDIATE*" -o -name "*COMPREHENSIVE*" -o -name "*FINAL*" | head -10
echo ""

# Check repository health
echo "2. REPOSITORY HEALTH CHECK..."
echo "------------------------------------------"
echo "Repository size:"
du -sh .git/ 2>/dev/null || echo "Not a git repository or .git not accessible"
echo ""
echo "File count by type:"
echo "  Markdown files: $(find . -name "*.md" | wc -l)"
echo "  Python files: $(find . -name "*.py" | wc -l)"
echo "  Batch files: $(find . -name "*.bat" | wc -l)"
echo "  HTML files: $(find . -name "*.html" | wc -l)"
echo ""

# Check for large files
echo "3. LARGE FILE ANALYSIS..."
echo "------------------------------------------"
echo "Files larger than 1MB:"
find . -type f -size +1M -exec ls -lh {} \; | head -5
echo ""

# Cleanup recommendations
echo "4. CLEANUP RECOMMENDATIONS..."
echo "------------------------------------------"
echo "Suggested actions:"
if [ -d ".cleanup" ]; then
    echo "✅ Cleanup system already in place"
else
    echo "❗ Consider setting up .cleanup directory structure"
fi

if [ -f ".gitignore" ]; then
    echo "✅ .gitignore file exists"
else
    echo "❗ Create .gitignore to prevent future issues"
fi

echo ""
echo "=========================================="
echo "MAINTENANCE SCRIPT COMPLETE"
echo "Run this script weekly as per guidelines"
echo "=========================================="