#!/bin/bash

# Function to identify and remove duplicates
remove_duplicates() {
    declare -A seen_content
    
    for file in $(find . -type f -name "*CORRECTED*" -o -name "*FIXED*"); do
        # Calculate file hash
        hash=$(md5sum "$file" | awk '{print $1}')
        
        if [[ -v seen_content[$hash] ]]; then
            # Duplicate found
            mv "$file" ".cleanup/quarantine/duplicates/"
            echo "Removed duplicate: $file"
        else
            seen_content[$hash]="$file"
        fi
    done
}

remove_duplicates