#!/bin/bash
# ========================================
# Azure Cloud Shell Recovery Tool
# Interactive recovery from cloud backups
# ========================================

BACKUP_DIR="$HOME/life_repository_backups"
REPO_URL="https://github.com/SergiLIFE/SergiLIFE-life-azure-system.git"

echo "===== L.I.F.E. Repository Azure Cloud Recovery ====="
echo ""

# Check if backup directory exists
if [ ! -d "$BACKUP_DIR" ]; then
    echo "❌ No backups found in Cloud Shell"
    echo "💡 Run azure_cloud_backup.sh first to create backups"
    exit 1
fi

echo "📍 Cloud Shell backup location: $BACKUP_DIR"
echo ""

# Show available bundles
echo "📦 Available git bundles:"
if ls "$BACKUP_DIR/bundles/"*.bundle 1> /dev/null 2>&1; then
    ls -la "$BACKUP_DIR/bundles/"*.bundle | awk '{print "   " $9 " (" $5 " bytes) " $6 " " $7 " " $8}'
else
    echo "   No bundles found"
fi

echo ""

# Show available snapshots
echo "📁 Available snapshots:"
if ls "$BACKUP_DIR/snapshots/"*.tar.gz 1> /dev/null 2>&1; then
    ls -la "$BACKUP_DIR/snapshots/"*.tar.gz | awk '{print "   " $9 " (" $5 " bytes) " $6 " " $7 " " $8}'
else
    echo "   No snapshots found"
fi

echo ""
echo "===== Recovery Options ====="
echo "1. Clone from latest bundle"
echo "2. Extract latest snapshot"
echo "3. Clone fresh from GitHub"
echo "4. Show backup details"
echo "5. Upload backup to Azure Storage"
echo "6. Create new backup"
echo "0. Exit"
echo ""

read -p "Select option (0-6): " choice

case $choice in
    1)
        echo ""
        echo "🔄 Cloning from latest bundle..."
        LATEST_BUNDLE=$(ls -t "$BACKUP_DIR/bundles/"*.bundle 2>/dev/null | head -1)
        if [ -n "$LATEST_BUNDLE" ]; then
            echo "Latest bundle: $(basename "$LATEST_BUNDLE")"
            read -p "Enter directory name for recovered repository: " target_dir
            target_dir=${target_dir:-"recovered_from_bundle"}
            
            git clone "$LATEST_BUNDLE" "$target_dir"
            if [ $? -eq 0 ]; then
                echo "✅ Repository recovered to: $target_dir"
                cd "$target_dir"
                echo "🔍 Verifying recovery..."
                git log --oneline -3
                git fsck --full
            else
                echo "❌ Recovery failed"
            fi
        else
            echo "❌ No bundles available"
        fi
        ;;
    
    2)
        echo ""
        echo "📂 Extracting latest snapshot..."
        LATEST_SNAPSHOT=$(ls -t "$BACKUP_DIR/snapshots/"*.tar.gz 2>/dev/null | head -1)
        if [ -n "$LATEST_SNAPSHOT" ]; then
            echo "Latest snapshot: $(basename "$LATEST_SNAPSHOT")"
            read -p "Enter directory name for extracted files: " target_dir
            target_dir=${target_dir:-"recovered_from_snapshot"}
            
            mkdir -p "$target_dir"
            tar -xzf "$LATEST_SNAPSHOT" -C "$target_dir"
            if [ $? -eq 0 ]; then
                echo "✅ Files extracted to: $target_dir"
                echo "📋 Contents:"
                ls -la "$target_dir" | head -10
            else
                echo "❌ Extraction failed"
            fi
        else
            echo "❌ No snapshots available"
        fi
        ;;
    
    3)
        echo ""
        echo "📥 Cloning fresh from GitHub..."
        read -p "Enter directory name for fresh clone: " target_dir
        target_dir=${target_dir:-"fresh_from_github"}
        
        git clone $REPO_URL "$target_dir"
        if [ $? -eq 0 ]; then
            echo "✅ Fresh repository cloned to: $target_dir"
            cd "$target_dir"
            git log --oneline -3
        else
            echo "❌ Clone failed"
        fi
        ;;
    
    4)
        echo ""
        echo "📊 Backup details..."
        if [ -f "$BACKUP_DIR/last_backup.txt" ]; then
            cat "$BACKUP_DIR/last_backup.txt"
        else
            echo "No backup summary found"
        fi
        
        echo ""
        echo "💾 Disk usage:"
        du -sh "$BACKUP_DIR"/* 2>/dev/null
        ;;
    
    5)
        echo ""
        echo "☁️  Uploading to Azure Storage..."
        echo "Available storage accounts:"
        az storage account list --query "[].{Name:name, ResourceGroup:resourceGroup}" --output table
        
        read -p "Enter storage account name (or press Enter for stlifeplatformprod): " storage_account
        storage_account=${storage_account:-"stlifeplatformprod"}
        
        read -p "Enter container name (or press Enter for backups): " container_name
        container_name=${container_name:-"backups"}
        
        # Create container if it doesn't exist
        az storage container create --name "$container_name" --account-name "$storage_account" 2>/dev/null
        
        # Upload latest bundle and snapshot
        LATEST_BUNDLE=$(ls -t "$BACKUP_DIR/bundles/"*.bundle 2>/dev/null | head -1)
        LATEST_SNAPSHOT=$(ls -t "$BACKUP_DIR/snapshots/"*.tar.gz 2>/dev/null | head -1)
        
        if [ -n "$LATEST_BUNDLE" ]; then
            echo "Uploading bundle: $(basename "$LATEST_BUNDLE")"
            az storage blob upload --file "$LATEST_BUNDLE" --name "$(basename "$LATEST_BUNDLE")" --container-name "$container_name" --account-name "$storage_account"
        fi
        
        if [ -n "$LATEST_SNAPSHOT" ]; then
            echo "Uploading snapshot: $(basename "$LATEST_SNAPSHOT")"
            az storage blob upload --file "$LATEST_SNAPSHOT" --name "$(basename "$LATEST_SNAPSHOT")" --container-name "$container_name" --account-name "$storage_account"
        fi
        
        echo "✅ Upload complete"
        ;;
    
    6)
        echo ""
        echo "🔄 Creating new backup..."
        bash azure_cloud_backup.sh
        ;;
    
    0)
        echo "Recovery tool closed."
        exit 0
        ;;
    
    *)
        echo "Invalid choice. Please select 0-6."
        ;;
esac

echo ""
read -p "Press Enter to continue..."