#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EMERGENCY EMOJI CLEANER - L.I.F.E Platform
Removes all emojis from specific files that still have them
"""

import os
import re


def clean_emojis_from_text(text):
    """Remove all emojis and clean up the text."""
    # Remove common emojis
    text = re.sub(r'[🧠🤖⚡✅🔧💰📊🎯🔬🌟💡🎬📋🏆🎓🏢🏥📞🤝🔐🔍🔗🧪🌐📱🚨⚙️🛠️☁️🏗️🌀🧩🛡️👥🔑🎆💳📈🌍📚🧬⭐🎪🎨🔮🎸🎭🎲🎊🎈🎁🍾🥳🤯😎🔥✨💎🏅🥇📸📹📺📻🎙️🎧🎵🎶🎼🎹🥁🎺🎷🎻🪕🪗🪘🪙🚀]', '', text)
    
    # Remove all emojis using Unicode ranges
    emoji_pattern = re.compile("["
                              u"\U0001F600-\U0001F64F"  # emoticons
                              u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                              u"\U0001F680-\U0001F6FF"  # transport & map symbols
                              u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                              u"\U00002702-\U000027B0"  # dingbats
                              u"\U000024C2-\U0001F251"
                              "]+", flags=re.UNICODE)
    
    text = emoji_pattern.sub('', text)
    
    # Clean up extra spaces
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r' +\n', '\n', text)
    
    return text

def main():
    print("EMERGENCY EMOJI CLEANER FOR L.I.F.E PLATFORM")
    print("=" * 50)
    
    files_to_clean = [
        "README.md",
        "README_PROFESSIONAL.md",
        "README_INTEGRATION.md"
    ]
    
    for filename in files_to_clean:
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                cleaned_content = clean_emojis_from_text(content)
                
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(cleaned_content)
                
                print(f"✅ CLEANED: {filename}")
                
            except Exception as e:
                print(f"❌ ERROR cleaning {filename}: {e}")
        else:
            print(f"⚠️  NOT FOUND: {filename}")
    
    print("=" * 50)
    print("EMERGENCY CLEANING COMPLETE!")
    print("All visible emojis should now be removed.")

if __name__ == '__main__':
    main()    main()