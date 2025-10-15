#!/bin/bash
# L.I.F.E Platform Cloud Backup & Storage Manager
# Saves files to cloud storage to free up local disk space

echo "☁️  L.I.F.E PLATFORM CLOUD BACKUP UTILITY"
echo "=========================================="
echo ""
echo "💾 Disk Space Saver & Cloud Storage Manager"
echo "📅 October 15, 2025"
echo ""

# Create cloud-accessible versions
create_cloud_backup() {
    local source_dir="$1"
    local backup_name="LIFE_Platform_Cloud_Backup_$(date +%Y%m%d_%H%M%S)"
    
    echo "📦 Creating cloud backup: $backup_name"
    
    # Create backup directory structure
    mkdir -p "$backup_name"/{platform,docs,scripts,results}
    
    # Copy essential files
    if [ -f "$source_dir/L.I.F.E_PLATFORM_COMPLETE_WITH_TABS.html" ]; then
        cp "$source_dir/L.I.F.E_PLATFORM_COMPLETE_WITH_TABS.html" "$backup_name/platform/"
        echo "✅ Platform HTML copied"
    fi
    
    if [ -f "$source_dir/SOTA_BENCHMARK_RESULTS_OCT14_2025.txt" ]; then
        cp "$source_dir/SOTA_BENCHMARK_RESULTS_OCT14_2025.txt" "$backup_name/docs/"
        echo "✅ SOTA Benchmarks copied"
    fi
    
    # Copy all HTML files
    cp "$source_dir"/*.html "$backup_name/platform/" 2>/dev/null && echo "✅ All HTML platforms copied"
    
    # Copy Python scripts
    cp "$source_dir"/*.py "$backup_name/scripts/" 2>/dev/null && echo "✅ Python scripts copied"
    
    # Copy PowerShell and batch files
    cp "$source_dir"/*.ps1 "$backup_name/scripts/" 2>/dev/null && echo "✅ PowerShell scripts copied"
    cp "$source_dir"/*.bat "$backup_name/scripts/" 2>/dev/null && echo "✅ Batch files copied"
    
    # Copy documentation
    cp "$source_dir"/*.md "$backup_name/docs/" 2>/dev/null && echo "✅ Documentation copied"
    cp "$source_dir"/*.txt "$backup_name/docs/" 2>/dev/null && echo "✅ Text files copied"
    
    # Create archive for easy transfer
    if command -v tar >/dev/null 2>&1; then
        tar -czf "${backup_name}.tar.gz" "$backup_name"
        echo "📦 Created compressed archive: ${backup_name}.tar.gz"
        
        # Calculate size savings
        original_size=$(du -sh "$source_dir" 2>/dev/null | cut -f1 || echo "Unknown")
        backup_size=$(du -sh "${backup_name}.tar.gz" 2>/dev/null | cut -f1 || echo "Unknown")
        
        echo ""
        echo "💾 DISK SPACE ANALYSIS:"
        echo "   Original size: $original_size"
        echo "   Backup size: $backup_size"
        echo "   Ready for cloud upload!"
    fi
    
    return 0
}

# Check current directory for L.I.F.E files
if [ -f "L.I.F.E_PLATFORM_COMPLETE_WITH_TABS.html" ]; then
    echo "✅ L.I.F.E Platform found in current directory"
    create_cloud_backup "."
elif [ -f "../L.I.F.E_PLATFORM_COMPLETE_WITH_TABS.html" ]; then
    echo "✅ L.I.F.E Platform found in parent directory"  
    create_cloud_backup ".."
else
    echo "🔍 Searching for L.I.F.E Platform files..."
    
    # Search common locations
    found=false
    search_paths=(
        "/mnt/c/Users/*/OneDrive/Documents/GitHub*/*SergiLIFE*"
        "~/OneDrive/Documents/GitHub*/*SergiLIFE*"
        "/mnt/c/Users/*/Documents/GitHub*/*SergiLIFE*"
        "."
    )
    
    for path in "${search_paths[@]}"; do
        if [ -f "$path/L.I.F.E_PLATFORM_COMPLETE_WITH_TABS.html" ]; then
            echo "✅ Found L.I.F.E Platform at: $path"
            create_cloud_backup "$path"
            found=true
            break
        fi
    done
    
    if [ "$found" = false ]; then
        echo "❌ L.I.F.E Platform files not found!"
        echo "📂 Please run this script from the L.I.F.E Platform directory"
        echo ""
        echo "🔍 Current directory contents:"
        ls -la
    fi
fi

echo ""
echo "☁️  CLOUD STORAGE OPTIONS:"
echo "=========================="
echo "1. 📁 OneDrive: Files are already in OneDrive folder"
echo "2. 🌐 Azure Blob Storage: Enterprise cloud storage"
echo "3. 📦 GitHub: Version control + cloud backup"
echo "4. 💾 Local Archive: Compressed for easy transfer"
echo ""
echo "🎯 RECOMMENDATION FOR YOUR DISK SPACE:"
echo "   • Keep only the compressed .tar.gz file locally"
echo "   • Upload to Azure Blob Storage for production"
echo "   • Use OneDrive for automatic sync"
echo ""
echo "✅ Cloud backup preparation complete!"
echo "🚀 Ready for October 15th Strategic Partnership Demo!"
echo ""