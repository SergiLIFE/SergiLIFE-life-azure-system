#!/bin/bash

REPO_PATH="."
QUARANTINE=".cleanup/quarantine"
DELETED_LOG=".cleanup/logs/deleted-files.log"

echo "Starting cleanup process..." > "$DELETED_LOG"
DELETED_COUNT=0
ERROR_COUNT=0

# Read from auto-generated files list
while IFS= read -r file; do
    if [[ -n "$file" && -f "$REPO_PATH/$file" ]]; then
        # Verify file is safe to delete (not in version control critical files)
        if [[ ! "$file" =~ \.(git|node_modules|src|config) ]]; then
            mv "$REPO_PATH/$file" "$QUARANTINE/auto-generated/" 2>> "$DELETED_LOG" && \
            echo "Moved: $file" >> "$DELETED_LOG" && \
            ((DELETED_COUNT++)) || \
            ((ERROR_COUNT++))
        fi
    fi
done < .cleanup/logs/auto_generated.txt

echo "Deleted: $DELETED_COUNT files | Errors: $ERROR_COUNT" >> "$DELETED_LOG"