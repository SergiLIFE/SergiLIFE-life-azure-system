#!/usr/bin/env python3
"""
L.I.F.E THEORY CODE 3 VENTURY SYSTEM - Copyright Remediation Engine
Venturi Gate System for Copyright Compliance and Protection

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID:
9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import os
from pathlib import Path


def check_copyright_compliance():
    """Basic copyright compliance check"""
    print("🚪 L.I.F.E 3-VENTURI COPYRIGHT ANALYSIS")
    print("=" * 50)

    root_path = Path(".")
    copyright_holder = "Sergio Paya Borrull"
    copyright_year = "2025"

    # File extensions to check
    extensions = [".py", ".md", ".json", ".yml", ".yaml"]

    missing_copyright = []
    inconsistent_copyright = []

    for ext in extensions:
        for file_path in root_path.rglob(f"**/*{ext}"):
            # Skip certain directories
            skip_dirs = ["__pycache__", ".git", "logs"]
            if any(skip in str(file_path) for skip in skip_dirs):
                continue

            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                has_copyright = (
                    "Copyright" in content
                    and copyright_holder in content
                    and copyright_year in content
                )

                if not has_copyright:
                    missing_copyright.append(str(file_path))
                else:
                    # Check for inconsistent formats
                    copyright_lines = [
                        line
                        for line in content.split("\n")
                        if "Copyright" in line and copyright_holder in line
                    ]
                    if len(copyright_lines) > 1:
                        inconsistent_copyright.append(str(file_path))

            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    print(f"📊 Analysis Results:")
    print(f"   Missing copyright: {len(missing_copyright)}")
    print(f"   Inconsistent copyright: {len(inconsistent_copyright)}")

    if missing_copyright:
        print("\nFiles missing copyright:")
        for file in missing_copyright[:10]:  # Show first 10
            print(f"   - {file}")
        if len(missing_copyright) > 10:
            print(f"   ... and {len(missing_copyright) - 10} more")

    if inconsistent_copyright:
        print("\nFiles with inconsistent copyright:")
        for file in inconsistent_copyright[:5]:  # Show first 5
            print(f"   - {file}")

    # Generate basic report
    report = f"""# Copyright Compliance Report
Generated: {os.environ.get('DATE', 'Unknown')}

## Summary
- Files missing copyright: {len(missing_copyright)}
- Files with inconsistent copyright: {len(inconsistent_copyright)}
- Overall compliance: {'❌ Needs Review' if missing_copyright or inconsistent_copyright else '✅ Compliant'}

## Copyright Standard
Copyright {copyright_year} - {copyright_holder}
L.I.F.E. Platform - Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
"""

    with open("COPYRIGHT_COMPLIANCE_REPORT.md", "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n📄 Report saved to: COPYRIGHT_COMPLIANCE_REPORT.md")

    return len(missing_copyright) == 0 and len(inconsistent_copyright) == 0


if __name__ == "__main__":
    compliant = check_copyright_compliance()
    exit(0 if compliant else 1)
