#!/usr/bin/env python3
"""
Emoji Sanitization and Prevention System
Removes emojis from files and implements prevention measures
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class EmojiSanitizer:
    def __init__(self):
        # Comprehensive emoji patterns
        self.emoji_patterns = [
            # Unicode emoji ranges
            r"[\U0001F600-\U0001F64F]",  # emoticons
            r"[\U0001F300-\U0001F5FF]",  # symbols & pictographs
            r"[\U0001F680-\U0001F6FF]",  # transport & map symbols
            r"[\U0001F1E0-\U0001F1FF]",  # flags (iOS)
            r"[\U00002702-\U000027B0]",  # dingbats
            r"[\U000024C2-\U0001F251]",  # enclosed characters
            r"[\U0001F900-\U0001F9FF]",  # supplemental symbols
            r"[\U0001FA70-\U0001FAFF]",  # symbols and pictographs extended-A
            # Common text emojis
            r":\)|:\(|:D|:P|:o|:O|;\)|<3|</3|:/",
            # Specific emoji characters commonly used
            r"[🧠🤖⚡🎉📦📁✅❌⚠️🔍🔧🛡️🚀📋📊💾☁️🌤️🆘📍🔄📂🔒📖🎯📘🧪🏆⭐🌟💡🔥⚙️]",
        ]

        self.compiled_patterns = [
            re.compile(pattern, re.UNICODE) for pattern in self.emoji_patterns
        ]

        # File extensions to process
        self.processable_extensions = {
            ".md",
            ".txt",
            ".py",
            ".js",
            ".html",
            ".css",
            ".json",
            ".yml",
            ".yaml",
            ".bat",
            ".sh",
            ".ps1",
        }

        # Files to exclude from processing
        self.excluded_files = {
            "emoji_sanitizer.py",
            "node_modules",
            ".git",
            "__pycache__",
            ".venv",
        }

    def has_emojis(self, text: str) -> bool:
        """Check if text contains emojis"""
        for pattern in self.compiled_patterns:
            if pattern.search(text):
                return True
        return False

    def remove_emojis(self, text: str) -> str:
        """Remove all emojis from text"""
        for pattern in self.compiled_patterns:
            text = pattern.sub("", text)
        return text

    def sanitize_file(self, file_path: Path) -> Tuple[bool, str]:
        """
        Sanitize a single file by removing emojis
        Returns (changed, message)
        """
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                original_content = f.read()

            if not self.has_emojis(original_content):
                return False, "No emojis found"

            sanitized_content = self.remove_emojis(original_content)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(sanitized_content)

            return True, "Emojis removed successfully"

        except Exception as e:
            return False, f"Error processing file: {e}"

    def should_process_file(self, file_path: Path) -> bool:
        """Determine if file should be processed"""
        # Check extension
        if file_path.suffix not in self.processable_extensions:
            return False

        # Check excluded files/directories
        for excluded in self.excluded_files:
            if excluded in str(file_path):
                return False

        # Check if file is too large (>10MB)
        try:
            if file_path.stat().st_size > 10 * 1024 * 1024:
                return False
        except:
            return False

        return True

    def scan_directory(self, directory: Path) -> List[Path]:
        """Scan directory for files containing emojis"""
        files_with_emojis = []

        for file_path in directory.rglob("*"):
            if not file_path.is_file():
                continue

            if not self.should_process_file(file_path):
                continue

            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    if self.has_emojis(content):
                        files_with_emojis.append(file_path)
            except:
                continue

        return files_with_emojis

    def sanitize_directory(self, directory: Path) -> Dict[str, any]:
        """Sanitize all files in directory"""
        results = {"processed": 0, "changed": 0, "errors": 0, "files": []}

        files_to_process = self.scan_directory(directory)

        for file_path in files_to_process:
            changed, message = self.sanitize_file(file_path)

            results["processed"] += 1
            if changed:
                results["changed"] += 1
            if "Error" in message:
                results["errors"] += 1

            results["files"].append(
                {
                    "file": str(file_path.relative_to(directory)),
                    "changed": changed,
                    "message": message,
                }
            )

        return results

    def create_gitignore_emoji_rules(self, directory: Path):
        """Add emoji prevention rules to .gitignore"""
        gitignore_path = directory / ".gitignore"

        emoji_rules = """
# Emoji Prevention Rules
# Block files with emojis in names
*[🧠🤖⚡🎉📦📁✅❌⚠️🔍🔧🛡️🚀📋📊💾☁️🌤️🆘📍🔄📂🔒📖🎯📘🧪🏆⭐🌟💡🔥⚙️]*

# Block common emoji file patterns
*emoji*
*Emoji*
*EMOJI*
"""

        if gitignore_path.exists():
            with open(gitignore_path, "r", encoding="utf-8") as f:
                content = f.read()

            if "Emoji Prevention Rules" not in content:
                with open(gitignore_path, "a", encoding="utf-8") as f:
                    f.write(emoji_rules)
        else:
            with open(gitignore_path, "w", encoding="utf-8") as f:
                f.write(emoji_rules.strip())


def main():
    if len(sys.argv) > 1:
        target_directory = Path(sys.argv[1])
    else:
        target_directory = Path.cwd()

    if not target_directory.exists() or not target_directory.is_dir():
        print(f"Error: {target_directory} is not a valid directory")
        sys.exit(1)

    print("L.I.F.E Platform - Emoji Sanitization System")
    print("=" * 50)
    print(f"Target directory: {target_directory}")
    print()

    sanitizer = EmojiSanitizer()

    # Scan for files with emojis
    print("Scanning for files with emojis...")
    files_with_emojis = sanitizer.scan_directory(target_directory)

    if not files_with_emojis:
        print("No files with emojis found.")
        sanitizer.create_gitignore_emoji_rules(target_directory)
        print("Added emoji prevention rules to .gitignore")
        return

    print(f"Found {len(files_with_emojis)} files containing emojis:")
    for file_path in files_with_emojis:
        print(f"  - {file_path.relative_to(target_directory)}")

    print()
    response = input("Remove emojis from these files? (y/N): ")

    if response.lower() != "y":
        print("Operation cancelled.")
        return

    # Sanitize directory
    print("\nSanitizing files...")
    results = sanitizer.sanitize_directory(target_directory)

    print(f"\nSanitization complete:")
    print(f"  Files processed: {results['processed']}")
    print(f"  Files changed: {results['changed']}")
    print(f"  Errors: {results['errors']}")

    if results["errors"] > 0:
        print("\nFiles with errors:")
        for file_info in results["files"]:
            if "Error" in file_info["message"]:
                print(f"  - {file_info['file']}: {file_info['message']}")

    # Create emoji prevention rules
    sanitizer.create_gitignore_emoji_rules(target_directory)
    print("\nAdded emoji prevention rules to .gitignore")

    # Save results to file
    results_file = target_directory / "emoji_sanitization_results.json"
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"Detailed results saved to: {results_file}")
    print("\nEmoji sanitization complete!")


if __name__ == "__main__":
    main()
