#!/usr/bin/env python3
"""
L.I.F.E THEORY CODE 3 VENTURY SYSTEM - Copyright Remediation Engine
Venturi Gate System for Copyright Compliance and Protection

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID:
9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


class CopyrightRemediationEngine:
    """L.I.F.E 3-Venturi Copyright Remediation System"""

    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.copyright_holder = "Sergio Paya Borrull"
        self.copyright_year = "2025"
        self.marketplace_id = "9a600d96-fe1e-420b-902a-a0c42c561adb"

        # Define file extensions to check
        self.source_extensions = {
            ".py",
            ".md",
            ".json",
            ".bicep",
            ".yml",
            ".yaml",
            ".sh",
            ".ps1",
            ".js",
            ".ts",
            ".html",
            ".css",
        }

        # Files to exclude from copyright checks
        self.exclude_patterns = {
            "__pycache__",
            ".git",
            ".mypy_cache",
            "node_modules",
            ".vscode",
            "logs",
            "results",
            "temp",
            "build",
        }

        # Standard copyright templates
        self.copyright_templates = {
            "python": f'''"""
[MODULE_DESCRIPTION]

Copyright {self.copyright_year} - {self.copyright_holder}
L.I.F.E. Platform - Azure Marketplace Offer ID: {self.marketplace_id}
"""''',
            "markdown": f"""---
Copyright {self.copyright_year} - {self.copyright_holder}
L.I.F.E. Platform - Azure Marketplace Offer ID: {self.marketplace_id}
---""",
            "config": f"""# Copyright {self.copyright_year} - {self.copyright_holder}
# L.I.F.E. Platform - Azure Marketplace Offer ID: {self.marketplace_id}""",
            "script": f"""#!/bin/bash
# Copyright {self.copyright_year} - {self.copyright_holder}
# L.I.F.E. Platform - Azure Marketplace Offer ID: {self.marketplace_id}""",
        }

    def venturi_gate_1_analysis(self) -> Dict[str, List[str]]:
        """Venturi Gate 1: Comprehensive Copyright Analysis"""
        print("🚪 VENTURI GATE 1: Copyright Analysis Initiating...")

        analysis_results = {
            "missing_copyright": [],
            "inconsistent_copyright": [],
            "external_references": [],
            "license_issues": [],
        }

        # Scan all source files
        for file_path in self._get_source_files():
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")

                if not self._has_valid_copyright(content):
                    analysis_results["missing_copyright"].append(str(file_path))

                # Check for inconsistent copyright
                if self._has_inconsistent_copyright(content):
                    analysis_results["inconsistent_copyright"].append(str(file_path))

                # Check for external references that might indicate copied code
                if self._has_external_references(content):
                    analysis_results["external_references"].append(str(file_path))

            except (IOError, OSError) as e:
                print(f"⚠️  Error analyzing {file_path}: {e}")

        print(
            f"📊 Analysis Complete: "
            f"{len(analysis_results['missing_copyright'])} missing, "
            f"{len(analysis_results['inconsistent_copyright'])} inconsistent, "
            f"{len(analysis_results['external_references'])} external references"
        )

        return analysis_results

    def venturi_gate_2_remediation(
        self, analysis_results: Dict[str, List[str]]
    ) -> Dict[str, int]:
        """Venturi Gate 2: Copyright Remediation and Correction"""
        print("🚪 VENTURI GATE 2: Copyright Remediation Initiating...")

        remediation_stats = {
            "copyrights_added": 0,
            "copyrights_updated": 0,
            "files_processed": 0,
            "errors": 0,
        }

        # Process missing copyrights
        for file_path in analysis_results["missing_copyright"]:
            try:
                self._add_copyright_header(file_path)
                remediation_stats["copyrights_added"] += 1
            except (IOError, OSError) as e:
                print(f"❌ Error adding copyright to {file_path}: {e}")
                remediation_stats["errors"] += 1

        # Process inconsistent copyrights
        for file_path in analysis_results["inconsistent_copyright"]:
            try:
                self._standardize_copyright(file_path)
                remediation_stats["copyrights_updated"] += 1
            except (IOError, OSError) as e:
                print(f"❌ Error updating copyright in {file_path}: {e}")
                remediation_stats["errors"] += 1

        remediation_stats["files_processed"] = (
            remediation_stats["copyrights_added"]
            + remediation_stats["copyrights_updated"]
        )

        print(
            f"✅ Remediation Complete: {remediation_stats['copyrights_added']} added, "
            f"{remediation_stats['copyrights_updated']} updated, "
            f"{remediation_stats['errors']} errors"
        )

        return remediation_stats

    def venturi_gate_3_validation(self) -> Dict[str, bool]:
        """Venturi Gate 3: Validation and Enforcement"""
        print("🚪 VENTURI GATE 3: Copyright Validation Initiating...")

        validation_results = {
            "all_files_compliant": True,
            "license_file_present": False,
            "consistent_copyright_holder": True,
            "marketplace_id_present": True,
            "no_external_copyrights": True,
        }

        # Check license file
        license_path = self.root_path / "LICENSE"
        if license_path.exists():
            validation_results["license_file_present"] = True
            license_content = license_path.read_text()
            if "Sergio Paya Borrull" not in license_content:
                validation_results["license_file_present"] = False

        # Validate all source files
        for file_path in self._get_source_files():
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")

                if not self._has_valid_copyright(content):
                    validation_results["all_files_compliant"] = False
                    break

                if not self._has_consistent_holder(content):
                    validation_results["consistent_copyright_holder"] = False

                if not self._has_marketplace_id(content):
                    validation_results["marketplace_id_present"] = False

                if self._has_external_copyrights(content):
                    validation_results["no_external_copyrights"] = False

            except (IOError, OSError) as e:
                print(f"⚠️  Validation error for {file_path}: {e}")
                validation_results["all_files_compliant"] = False

        # Generate compliance report
        self._generate_compliance_report(validation_results)

        compliance_status = (
            "✅ COMPLIANT"
            if validation_results["all_files_compliant"]
            else "❌ NON-COMPLIANT"
        )
        print(f"🎯 Validation Complete: {compliance_status}")

        return validation_results

    def _get_source_files(self) -> List[Path]:
        """Get all source files to analyze"""
        source_files = []

        for ext in self.source_extensions:
            pattern = f"**/*{ext}"
            for file_path in self.root_path.glob(pattern):
                # Skip excluded directories
                if any(excl in str(file_path) for excl in self.exclude_patterns):
                    continue
                source_files.append(file_path)

        return source_files

    def _has_valid_copyright(self, content: str) -> bool:
        """Check if file has valid copyright notice"""
        return (
            "Copyright" in content
            and self.copyright_holder in content
            and self.copyright_year in content
        )

    def _has_inconsistent_copyright(self, content: str) -> bool:
        """Check for inconsistent copyright formatting"""
        if not self._has_valid_copyright(content):
            return False

        # Check for multiple different copyright formats
        copyright_lines = [line for line in content.split("\n") if "Copyright" in line]
        if len(copyright_lines) > 1:
            # Check if they have different formats
            formats = set()
            for line in copyright_lines:
                # Normalize format
                normalized = re.sub(r"\d{4}", "YEAR", line)
                normalized = re.sub(
                    r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
                    "UUID",
                    normalized,
                )
                formats.add(normalized.strip())
            return len(formats) > 1

        return False

    def _has_external_references(self, content: str) -> bool:
        """Check for external references that might indicate copied code"""
        external_indicators = [
            "stackoverflow.com",
            "github.com",
            "medium.com",
            "reddit.com",
            "quora.com",
            "copied from",
            "adapted from",
            "based on",
            "source:",
            "reference:",
        ]

        content_lower = content.lower()
        return any(indicator in content_lower for indicator in external_indicators)

    def _has_external_copyrights(self, content: str) -> bool:
        """Check for external copyright notices"""
        # Look for copyright notices that aren't ours
        copyright_pattern = r"Copyright.*\d{4}.*"
        copyright_notices = re.findall(copyright_pattern, content, re.IGNORECASE)

        for notice in copyright_notices:
            if self.copyright_holder not in notice:
                return True

        return False

    def _has_consistent_holder(self, content: str) -> bool:
        """Check for consistent copyright holder"""
        return self.copyright_holder in content

    def _has_marketplace_id(self, content: str) -> bool:
        """Check for marketplace ID presence"""
        return self.marketplace_id in content

    def _add_copyright_header(self, file_path: str):
        """Add copyright header to file"""
        path = Path(file_path)
        content = path.read_text(encoding="utf-8", errors="ignore")

        # Determine file type and get appropriate template
        suffix = path.suffix.lower()
        if suffix == ".py":
            template = self.copyright_templates["python"]
            # Replace module description placeholder
            module_name = path.stem.replace("_", " ").replace("-", " ").title()
            template = template.replace("[MODULE_DESCRIPTION]", f"{module_name} Module")
        elif suffix == ".md":
            template = self.copyright_templates["markdown"]
        elif suffix in [".json", ".bicep", ".yml", ".yaml"]:
            template = self.copyright_templates["config"]
        elif suffix == ".sh":
            template = self.copyright_templates["script"]
        else:
            template = self.copyright_templates["config"]

        # Add header
        new_content = template + "\n\n" + content

        # Write back
        path.write_text(new_content, encoding="utf-8")

    def _standardize_copyright(self, file_path: str):
        """Standardize copyright notice in file"""
        path = Path(file_path)
        content = path.read_text(encoding="utf-8", errors="ignore")

        # Remove existing copyright lines
        lines = content.split("\n")
        filtered_lines = []
        in_copyright_block = False

        for line in lines:
            if "Copyright" in line and self.copyright_holder in line:
                in_copyright_block = True
                continue
            elif in_copyright_block and (
                line.strip() == "" or line.startswith("#") or line.startswith('"""')
            ):
                continue
            else:
                in_copyright_block = False
                filtered_lines.append(line)

        # Add standardized copyright
        suffix = path.suffix.lower()
        if suffix == ".py":
            copyright_header = f'''"""
{path.stem.replace('_', ' ').replace('-', ' ').title()} Module

Copyright {self.copyright_year} - {self.copyright_holder}
L.I.F.E. Platform - Azure Marketplace Offer ID: {self.marketplace_id}
"""'''
        else:
            copyright_header = f"""# Copyright {self.copyright_year} - {self.copyright_holder}
# L.I.F.E. Platform - Azure Marketplace Offer ID: {self.marketplace_id}"""

        new_content = copyright_header + "\n\n" + "\n".join(filtered_lines)

        # Write back
        path.write_text(new_content, encoding="utf-8")

    def _generate_compliance_report(self, validation_results: Dict[str, bool]):
        """Generate copyright compliance report"""
        report_path = self.root_path / "COPYRIGHT_COMPLIANCE_REPORT.md"

        report_content = f"""# Copyright Compliance Report
Generated: {datetime.now().isoformat()}

## L.I.F.E Platform Copyright Compliance Status

### Overall Compliance: {'✅ COMPLIANT' if validation_results['all_files_compliant'] else '❌ NON-COMPLIANT'}

### Validation Results:
- **All Files Compliant**: {validation_results['all_files_compliant']}
- **License File Present**: {validation_results['license_file_present']}
- **Consistent Copyright Holder**: {validation_results['consistent_copyright_holder']}
- **Marketplace ID Present**: {validation_results['marketplace_id_present']}
- **No External Copyrights**: {validation_results['no_external_copyrights']}

### Copyright Standards:
- **Copyright Holder**: {self.copyright_holder}
- **Copyright Year**: {self.copyright_year}
- **Azure Marketplace Offer ID**: {self.marketplace_id}
- **License**: MIT License with Commercial Terms

### Remediation Actions Taken:
This report was generated by the L.I.F.E 3-Venturi Copyright Remediation System.

---
Copyright {self.copyright_year} - {self.copyright_holder}
L.I.F.E. Platform - Azure Marketplace Offer ID: {self.marketplace_id}
"""

        report_path.write_text(report_content, encoding="utf-8")
        print(f"📄 Compliance report generated: {report_path}")

    def execute_full_remediation(self) -> Dict[str, Any]:
        """Execute complete 3-Venturi remediation process"""
        print("🔄 L.I.F.E 3-VENTURI COPYRIGHT REMEDIATION SYSTEM ACTIVATED")
        print("=" * 60)

        # Gate 1: Analysis
        analysis_results = self.venturi_gate_1_analysis()

        # Gate 2: Remediation
        remediation_stats = self.venturi_gate_2_remediation(analysis_results)

        # Gate 3: Validation
        validation_results = self.venturi_gate_3_validation()

        # Final report
        final_status = {
            "analysis": analysis_results,
            "remediation": remediation_stats,
            "validation": validation_results,
            "overall_compliant": validation_results["all_files_compliant"],
        }

        print("=" * 60)
        if final_status["overall_compliant"]:
            print("🎉 COPYRIGHT REMEDIATION COMPLETE - ALL SYSTEMS COMPLIANT")
        else:
            print("⚠️  COPYRIGHT REMEDIATION COMPLETE - REVIEW REQUIRED")

        return final_status


def main():
    """Main execution function"""
    # Get the repository root (assuming script is in the repo)
    script_dir = Path(__file__).parent
    repo_root = script_dir

    # Initialize remediation engine
    engine = CopyrightRemediationEngine(str(repo_root))

    # Execute full remediation
    results = engine.execute_full_remediation()

    # Exit with appropriate code
    exit(0 if results["overall_compliant"] else 1)


if __name__ == "__main__":
    main()
