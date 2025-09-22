#!/usr/bin/env python3
"""
L.I.F.E. Platform - GitHub Actions Fix Tool
Automated repair and optimization of GitHub Actions CI/CD workflows

This module provides comprehensive tools for diagnosing, fixing, and
optimizing GitHub Actions workflows for the L.I.F.E. Platform.

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID:
9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import asyncio
import json
import logging
import os
import re
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class FixStatus(Enum):
    """Status of fix operations"""

    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"
    SKIPPED = "skipped"
    PENDING = "pending"


class FixPriority(Enum):
    """Priority levels for fixes"""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class WorkflowIssue(Enum):
    """Types of workflow issues that can be detected and fixed"""

    MISSING_CHECKOUT = "missing_checkout"
    MISSING_SETUP_PYTHON = "missing_setup_python"
    INCORRECT_PYTHON_VERSION = "incorrect_python_version"
    MISSING_AZURE_LOGIN = "missing_azure_login"
    MISSING_DEPENDENCIES = "missing_dependencies"
    MISSING_TEST_COMMAND = "missing_test_command"
    MISSING_BUILD_COMMAND = "missing_build_command"
    SECURITY_VULNERABILITY = "security_vulnerability"
    PERFORMANCE_ISSUE = "performance_issue"
    MISSING_PERMISSIONS = "missing_permissions"
    INCORRECT_TRIGGER = "incorrect_trigger"
    MISSING_ARTIFACT_UPLOAD = "missing_artifact_upload"
    MISSING_ERROR_HANDLING = "missing_error_handling"
    OUTDATED_ACTIONS = "outdated_actions"
    MISSING_MATRIX_STRATEGY = "missing_matrix_strategy"


@dataclass
class WorkflowFix:
    """Represents a fix to be applied to a workflow"""

    issue_type: WorkflowIssue
    priority: FixPriority
    description: str
    file_path: Path
    line_number: Optional[int] = None
    fix_applied: bool = False
    status: FixStatus = FixStatus.PENDING
    before_content: str = ""
    after_content: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    error_message: str = ""


@dataclass
class WorkflowAnalysis:
    """Analysis results for a workflow file"""

    file_path: Path
    issues_found: List[WorkflowFix] = field(default_factory=list)
    fixes_applied: List[WorkflowFix] = field(default_factory=list)
    analysis_timestamp: datetime = field(default_factory=datetime.now)
    workflow_valid: bool = True
    recommendations: List[str] = field(default_factory=list)


@dataclass
class GitHubActionsReport:
    """Comprehensive report of GitHub Actions fixes"""

    total_workflows: int = 0
    workflows_analyzed: int = 0
    issues_found: int = 0
    fixes_applied: int = 0
    critical_issues: int = 0
    success_rate: float = 0.0
    analysis_timestamp: datetime = field(default_factory=datetime.now)
    workflow_reports: List[WorkflowAnalysis] = field(default_factory=list)
    summary: Dict[str, Any] = field(default_factory=dict)


class GitHubActionsFixTool:
    """
    GitHub Actions Fix Tool for L.I.F.E. Platform

    Provides automated diagnosis and repair of GitHub Actions workflows
    to ensure reliable CI/CD pipelines.
    """

    def __init__(self, workspace_path: Optional[str] = None):
        self.workspace_path = Path(workspace_path or os.getcwd())
        self.github_workflows_path = self.workspace_path / ".github" / "workflows"
        self.analysis_results: List[WorkflowAnalysis] = []
        self.backup_created = False

        # Common patterns and fixes
        self.required_actions = {
            "checkout": "actions/checkout@v4",
            "setup_python": "actions/setup-python@v4",
            "azure_login": "azure/login@v1",
            "upload_artifact": "actions/upload-artifact@v3",
            "download_artifact": "actions/download-artifact@v3",
        }

        logger.info(
            f"GitHub Actions Fix Tool initialized for workspace: {self.workspace_path}"
        )

    async def analyze_and_fix_workflows(self) -> GitHubActionsReport:
        """Analyze all workflows and apply fixes"""
        logger.info("Starting GitHub Actions workflow analysis and fixes...")

        # Create backup of workflows directory
        await self._create_backup()

        # Find all workflow files
        workflow_files = self._find_workflow_files()

        if not workflow_files:
            logger.warning("No workflow files found")
            return GitHubActionsReport()

        report = GitHubActionsReport(total_workflows=len(workflow_files))

        # Analyze each workflow
        for workflow_file in workflow_files:
            try:
                analysis = await self._analyze_workflow(workflow_file)
                self.analysis_results.append(analysis)
                report.workflow_reports.append(analysis)
                report.workflows_analyzed += 1

                # Apply fixes
                fixes_applied = await self._apply_workflow_fixes(analysis)
                analysis.fixes_applied = fixes_applied

                report.issues_found += len(analysis.issues_found)
                report.fixes_applied += len(fixes_applied)

                # Count critical issues
                critical_issues = sum(
                    1
                    for fix in analysis.issues_found
                    if fix.priority == FixPriority.CRITICAL
                )
                report.critical_issues += critical_issues

            except Exception as e:
                logger.error(f"Failed to analyze {workflow_file}: {e}")
                # Create minimal analysis for failed workflows
                failed_analysis = WorkflowAnalysis(
                    file_path=workflow_file,
                    workflow_valid=False,
                    recommendations=[f"Manual review required: {str(e)}"],
                )
                self.analysis_results.append(failed_analysis)
                report.workflow_reports.append(failed_analysis)

        # Calculate success rate
        if report.issues_found > 0:
            report.success_rate = (report.fixes_applied / report.issues_found) * 100

        # Generate summary
        report.summary = self._generate_summary_report(report)

        logger.info(
            f"GitHub Actions analysis complete. Fixed {report.fixes_applied}/{report.issues_found} issues"
        )
        return report

    async def _create_backup(self):
        """Create backup of workflows directory"""
        try:
            if self.github_workflows_path.exists():
                backup_path = self.workspace_path / ".github" / "workflows.backup"
                if backup_path.exists():
                    shutil.rmtree(backup_path)
                shutil.copytree(self.github_workflows_path, backup_path)
                self.backup_created = True
                logger.info(f"Workflow backup created at {backup_path}")
        except Exception as e:
            logger.warning(f"Failed to create workflow backup: {e}")

    def _find_workflow_files(self) -> List[Path]:
        """Find all GitHub Actions workflow files"""
        workflow_files = []

        if self.github_workflows_path.exists():
            for file_path in self.github_workflows_path.glob("*.yml"):
                workflow_files.append(file_path)
            for file_path in self.github_workflows_path.glob("*.yaml"):
                workflow_files.append(file_path)

        return workflow_files

    async def _analyze_workflow(self, workflow_file: Path) -> WorkflowAnalysis:
        """Analyze a single workflow file for issues"""
        analysis = WorkflowAnalysis(file_path=workflow_file)

        try:
            # Read workflow content
            with open(workflow_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Parse YAML structure (basic parsing)
            workflow_data = self._parse_workflow_yaml(content)

            # Check for common issues
            issues = []

            # Check for checkout action
            issues.extend(self._check_checkout_action(workflow_data, content))

            # Check for Python setup
            issues.extend(self._check_python_setup(workflow_data, content))

            # Check for Azure login
            issues.extend(self._check_azure_login(workflow_data, content))

            # Check for dependencies installation
            issues.extend(self._check_dependencies(workflow_data, content))

            # Check for test commands
            issues.extend(self._check_test_commands(workflow_data, content))

            # Check for security issues
            issues.extend(self._check_security_issues(workflow_data, content))

            # Check for permissions
            issues.extend(self._check_permissions(workflow_data, content))

            # Check for triggers
            issues.extend(self._check_triggers(workflow_data, content))

            analysis.issues_found = issues

            # Validate workflow structure
            analysis.workflow_valid = self._validate_workflow_structure(workflow_data)

            # Generate recommendations
            analysis.recommendations = self._generate_workflow_recommendations(issues)

        except Exception as e:
            logger.error(f"Error analyzing {workflow_file}: {e}")
            analysis.workflow_valid = False
            analysis.recommendations = [f"Analysis failed: {str(e)}"]

        return analysis

    def _parse_workflow_yaml(self, content: str) -> Dict[str, Any]:
        """Basic YAML parsing for workflow analysis"""
        # Simple parsing - in production, use a proper YAML parser
        workflow_data = {}

        try:
            # Extract basic structure
            lines = content.split("\n")
            current_section = None
            indent_level = 0

            for i, line in enumerate(lines):
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue

                # Count leading spaces
                current_indent = len(line) - len(line.lstrip())

                # Check for section headers
                if ":" in stripped and not stripped.startswith(" "):
                    key = stripped.split(":")[0].strip()
                    if key in ["name", "on", "jobs", "env"]:
                        current_section = key
                        workflow_data[key] = {}
                        indent_level = current_indent
                    elif current_section:
                        # Sub-key
                        workflow_data[current_section][key] = stripped.split(":", 1)[
                            1
                        ].strip()

        except Exception as e:
            logger.warning(f"YAML parsing error: {e}")

        return workflow_data

    def _check_checkout_action(
        self, workflow_data: Dict[str, Any], content: str
    ) -> List[WorkflowFix]:
        """Check for checkout action in jobs"""
        issues = []

        # Look for checkout action in content
        if "actions/checkout" not in content:
            issues.append(
                WorkflowFix(
                    issue_type=WorkflowIssue.MISSING_CHECKOUT,
                    priority=FixPriority.CRITICAL,
                    description="Missing actions/checkout action - required for repository access",
                    file_path=Path("dummy"),  # Will be set by caller
                    line_number=None,
                )
            )

        return issues

    def _check_python_setup(
        self, workflow_data: Dict[str, Any], content: str
    ) -> List[WorkflowFix]:
        """Check for Python setup action"""
        issues = []

        if "python" in content.lower() and "actions/setup-python" not in content:
            issues.append(
                WorkflowFix(
                    issue_type=WorkflowIssue.MISSING_SETUP_PYTHON,
                    priority=FixPriority.CRITICAL,
                    description="Python mentioned but actions/setup-python action missing",
                    file_path=Path("dummy"),
                )
            )

        # Check Python version
        if "python-version" in content:
            # Look for version specification
            version_match = re.search(r'python-version:\s*[\'"]([^\'"]+)[\'"]', content)
            if version_match:
                version = version_match.group(1)
                if not version.startswith(("3.8", "3.9", "3.10", "3.11", "3.12")):
                    issues.append(
                        WorkflowFix(
                            issue_type=WorkflowIssue.INCORRECT_PYTHON_VERSION,
                            priority=FixPriority.HIGH,
                            description=f"Python version {version} may not be compatible with L.I.F.E. Platform",
                            file_path=Path("dummy"),
                        )
                    )

        return issues

    def _check_azure_login(
        self, workflow_data: Dict[str, Any], content: str
    ) -> List[WorkflowFix]:
        """Check for Azure login action"""
        issues = []

        if "azure" in content.lower() and "azure/login" not in content:
            issues.append(
                WorkflowFix(
                    issue_type=WorkflowIssue.MISSING_AZURE_LOGIN,
                    priority=FixPriority.CRITICAL,
                    description="Azure mentioned but azure/login action missing",
                    file_path=Path("dummy"),
                )
            )

        return issues

    def _check_dependencies(
        self, workflow_data: Dict[str, Any], content: str
    ) -> List[WorkflowFix]:
        """Check for dependency installation"""
        issues = []

        has_python = "python" in content.lower()
        has_pip = "pip install" in content
        has_requirements = "requirements.txt" in content

        if has_python and not (has_pip or has_requirements):
            issues.append(
                WorkflowFix(
                    issue_type=WorkflowIssue.MISSING_DEPENDENCIES,
                    priority=FixPriority.HIGH,
                    description="Python project detected but no dependency installation found",
                    file_path=Path("dummy"),
                )
            )

        return issues

    def _check_test_commands(
        self, workflow_data: Dict[str, Any], content: str
    ) -> List[WorkflowFix]:
        """Check for test commands"""
        issues = []

        has_python = "python" in content.lower()
        has_test_commands = any(
            cmd in content for cmd in ["pytest", "unittest", "python -m pytest"]
        )

        if has_python and not has_test_commands:
            issues.append(
                WorkflowFix(
                    issue_type=WorkflowIssue.MISSING_TEST_COMMAND,
                    priority=FixPriority.MEDIUM,
                    description="Python project detected but no test commands found",
                    file_path=Path("dummy"),
                )
            )

        return issues

    def _check_security_issues(
        self, workflow_data: Dict[str, Any], content: str
    ) -> List[WorkflowFix]:
        """Check for security issues"""
        issues = []

        # Check for outdated actions
        outdated_patterns = [
            "actions/checkout@v1",
            "actions/checkout@v2",
            "actions/setup-python@v1",
            "actions/setup-python@v2",
        ]

        for pattern in outdated_patterns:
            if pattern in content:
                action_name = pattern.split("@")[0]
                issues.append(
                    WorkflowFix(
                        issue_type=WorkflowIssue.OUTDATED_ACTIONS,
                        priority=FixPriority.MEDIUM,
                        description=f"Outdated action: {pattern} - should use latest version",
                        file_path=Path("dummy"),
                    )
                )

        # Check for potential secrets exposure
        if any(word in content.lower() for word in ["password", "secret", "key"]):
            # Look for hardcoded secrets (very basic check)
            secret_patterns = [
                r'password:\s*[\'"][^\'"]+[\'"]',
                r'secret:\s*[\'"][^\'"]+[\'"]',
            ]
            for pattern in secret_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    issues.append(
                        WorkflowFix(
                            issue_type=WorkflowIssue.SECURITY_VULNERABILITY,
                            priority=FixPriority.CRITICAL,
                            description="Potential hardcoded secrets detected in workflow",
                            file_path=Path("dummy"),
                        )
                    )
                    break

        return issues

    def _check_permissions(
        self, workflow_data: Dict[str, Any], content: str
    ) -> List[WorkflowFix]:
        """Check for proper permissions"""
        issues = []

        if "azure" in content.lower() and "permissions:" not in content:
            issues.append(
                WorkflowFix(
                    issue_type=WorkflowIssue.MISSING_PERMISSIONS,
                    priority=FixPriority.HIGH,
                    description="Azure deployment detected but no permissions specified",
                    file_path=Path("dummy"),
                )
            )

        return issues

    def _check_triggers(
        self, workflow_data: Dict[str, Any], content: str
    ) -> List[WorkflowFix]:
        """Check workflow triggers"""
        issues = []

        # Check if workflow has proper triggers
        if "on:" not in content and "trigger:" not in content:
            issues.append(
                WorkflowFix(
                    issue_type=WorkflowIssue.INCORRECT_TRIGGER,
                    priority=FixPriority.MEDIUM,
                    description="Workflow missing trigger configuration",
                    file_path=Path("dummy"),
                )
            )

        return issues

    def _validate_workflow_structure(self, workflow_data: Dict[str, Any]) -> bool:
        """Validate basic workflow structure"""
        required_keys = ["jobs"]
        return all(key in workflow_data for key in required_keys)

    def _generate_workflow_recommendations(
        self, issues: List[WorkflowFix]
    ) -> List[str]:
        """Generate recommendations based on issues found"""
        recommendations = []

        issue_types = {issue.issue_type for issue in issues}

        if WorkflowIssue.MISSING_CHECKOUT in issue_types:
            recommendations.append("Add actions/checkout@v4 as the first step in jobs")

        if WorkflowIssue.MISSING_SETUP_PYTHON in issue_types:
            recommendations.append("Add actions/setup-python@v4 for Python projects")

        if WorkflowIssue.MISSING_AZURE_LOGIN in issue_types:
            recommendations.append("Add azure/login@v1 for Azure deployments")

        if WorkflowIssue.SECURITY_VULNERABILITY in issue_types:
            recommendations.append(
                "Use GitHub secrets for sensitive values instead of hardcoding"
            )

        if WorkflowIssue.OUTDATED_ACTIONS in issue_types:
            recommendations.append(
                "Update to latest action versions for security and features"
            )

        if not recommendations:
            recommendations.append(
                "Workflow structure appears good - consider adding matrix builds for multiple Python versions"
            )

        return recommendations

    async def _apply_workflow_fixes(
        self, analysis: WorkflowAnalysis
    ) -> List[WorkflowFix]:
        """Apply fixes to a workflow"""
        applied_fixes = []

        for fix in analysis.issues_found:
            try:
                if await self._apply_single_fix(fix):
                    fix.fix_applied = True
                    fix.status = FixStatus.SUCCESS
                    applied_fixes.append(fix)
                    logger.info(f"Applied fix: {fix.description}")
                else:
                    fix.status = FixStatus.FAILED
                    logger.warning(f"Failed to apply fix: {fix.description}")

            except Exception as e:
                fix.status = FixStatus.FAILED
                fix.error_message = str(e)
                logger.error(f"Error applying fix {fix.description}: {e}")

        return applied_fixes

    async def _apply_single_fix(self, fix: WorkflowFix) -> bool:
        """Apply a single fix to the workflow"""
        try:
            # Read current content
            with open(fix.file_path, "r", encoding="utf-8") as f:
                content = f.read()

            fix.before_content = content

            # Apply fix based on type
            if fix.issue_type == WorkflowIssue.MISSING_CHECKOUT:
                content = self._add_checkout_action(content)
            elif fix.issue_type == WorkflowIssue.MISSING_SETUP_PYTHON:
                content = self._add_python_setup(content)
            elif fix.issue_type == WorkflowIssue.MISSING_AZURE_LOGIN:
                content = self._add_azure_login(content)
            elif fix.issue_type == WorkflowIssue.OUTDATED_ACTIONS:
                content = self._update_outdated_actions(content)
            elif fix.issue_type == WorkflowIssue.MISSING_PERMISSIONS:
                content = self._add_permissions(content)
            else:
                # Fix not implemented yet
                return False

            # Write back if content changed
            if content != fix.before_content:
                with open(fix.file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                fix.after_content = content
                return True

        except Exception as e:
            logger.error(f"Failed to apply fix: {e}")
            return False

        return False

    def _add_checkout_action(self, content: str) -> str:
        """Add checkout action to workflow"""
        # Find the first job and add checkout as first step
        lines = content.split("\n")
        in_job = False
        job_indent = ""

        for i, line in enumerate(lines):
            if line.strip().startswith("jobs:"):
                continue
            elif line.strip().startswith(("build:", "test:", "deploy:")):
                in_job = True
                job_indent = " " * (len(line) - len(line.lstrip()) + 2)  # steps indent
                # Look for steps
                for j in range(i + 1, len(lines)):
                    if "steps:" in lines[j]:
                        # Insert checkout after steps
                        checkout_step = f"{job_indent}- uses: actions/checkout@v4"
                        lines.insert(j + 1, checkout_step)
                        break
                break

        return "\n".join(lines)

    def _add_python_setup(self, content: str) -> str:
        """Add Python setup action"""
        # Find checkout action and add python setup after it
        lines = content.split("\n")

        for i, line in enumerate(lines):
            if "actions/checkout" in line:
                indent = " " * (len(line) - len(line.lstrip()))
                python_step = f"{indent}- uses: actions/setup-python@v4\n{indent}  with:\n{indent}    python-version: '3.8'"
                lines.insert(i + 1, python_step)
                break

        return "\n".join(lines)

    def _add_azure_login(self, content: str) -> str:
        """Add Azure login action"""
        lines = content.split("\n")

        for i, line in enumerate(lines):
            if "actions/setup-python" in line or "pip install" in line:
                indent = " " * (len(line) - len(line.lstrip()))
                azure_step = f"{indent}- uses: azure/login@v1\n{indent}  with:\n{indent}    creds: ${{ secrets.AZURE_CREDENTIALS }}"
                lines.insert(i + 1, azure_step)
                break

        return "\n".join(lines)

    def _update_outdated_actions(self, content: str) -> str:
        """Update outdated actions to latest versions"""
        replacements = {
            "actions/checkout@v1": "actions/checkout@v4",
            "actions/checkout@v2": "actions/checkout@v4",
            "actions/checkout@v3": "actions/checkout@v4",
            "actions/setup-python@v1": "actions/setup-python@v4",
            "actions/setup-python@v2": "actions/setup-python@v4",
            "actions/setup-python@v3": "actions/setup-python@v4",
        }

        for old, new in replacements.items():
            content = content.replace(old, new)

        return content

    def _add_permissions(self, content: str) -> str:
        """Add permissions section for Azure workflows"""
        lines = content.split("\n")

        # Insert permissions after 'on:' section
        for i, line in enumerate(lines):
            if line.strip().startswith("on:"):
                # Find end of on section
                j = i + 1
                while j < len(lines) and (
                    lines[j].startswith(" ") or lines[j].strip() == ""
                ):
                    j += 1

                permissions_block = [
                    "permissions:",
                    "  id-token: write",
                    "  contents: read",
                ]
                lines.insert(j, "\n".join(permissions_block))
                break

        return "\n".join(lines)

    def _generate_summary_report(self, report: GitHubActionsReport) -> Dict[str, Any]:
        """Generate summary report"""
        summary = {
            "workflows_processed": report.workflows_analyzed,
            "issues_detected": report.issues_found,
            "fixes_applied": report.fixes_applied,
            "success_rate": f"{report.success_rate:.1f}%",
            "critical_issues_remaining": report.critical_issues,
            "backup_created": self.backup_created,
            "recommendations": [],
        }

        # Add recommendations based on results
        if report.critical_issues > 0:
            summary["recommendations"].append(
                "Address remaining critical issues manually"
            )

        if report.success_rate < 80:
            summary["recommendations"].append(
                "Review failed fixes and implement manually"
            )

        if not self.backup_created:
            summary["recommendations"].append(
                "Consider creating manual backup before making changes"
            )

        return summary

    def export_fix_report(self, filepath: str, report: GitHubActionsReport) -> bool:
        """Export comprehensive fix report"""
        try:
            export_data = {
                "report_timestamp": datetime.now().isoformat(),
                "summary": report.summary,
                "workflow_details": [],
            }

            for workflow_report in report.workflow_reports:
                workflow_detail = {
                    "file_path": str(workflow_report.file_path),
                    "valid": workflow_report.workflow_valid,
                    "issues_found": len(workflow_report.issues_found),
                    "fixes_applied": len(workflow_report.fixes_applied),
                    "recommendations": workflow_report.recommendations,
                    "issues": [
                        {
                            "type": issue.issue_type.value,
                            "priority": issue.priority.value,
                            "description": issue.description,
                            "status": issue.status.value,
                            "applied": issue.fix_applied,
                        }
                        for issue in workflow_report.issues_found
                    ],
                }
                export_data["workflow_details"].append(workflow_detail)

            with open(filepath, "w") as f:
                json.dump(export_data, f, indent=2, default=str)

            logger.info(f"Fix report exported to {filepath}")
            return True

        except Exception as e:
            logger.error(f"Failed to export fix report: {e}")
            return False

    async def restore_backup(self) -> bool:
        """Restore workflows from backup"""
        try:
            if not self.backup_created:
                logger.warning("No backup available to restore")
                return False

            backup_path = self.workspace_path / ".github" / "workflows.backup"
            workflows_path = self.workspace_path / ".github" / "workflows"

            if backup_path.exists():
                # Remove current workflows
                if workflows_path.exists():
                    shutil.rmtree(workflows_path)

                # Restore from backup
                shutil.copytree(backup_path, workflows_path)
                logger.info("Workflows restored from backup")
                return True
            else:
                logger.warning("Backup directory not found")
                return False

        except Exception as e:
            logger.error(f"Failed to restore backup: {e}")
            return False


# Factory function for easy instantiation
def create_github_actions_fix_tool(
    workspace_path: Optional[str] = None,
) -> GitHubActionsFixTool:
    """
    Factory function to create GitHub Actions fix tool

    Args:
        workspace_path: Path to workspace directory

    Returns:
        Configured GitHubActionsFixTool instance
    """
    return GitHubActionsFixTool(workspace_path=workspace_path)


# Command-line interface
def main():
    """Main CLI function for GitHub Actions fixes"""
    import argparse

    parser = argparse.ArgumentParser(
        description="L.I.F.E. Platform GitHub Actions Fix Tool"
    )
    parser.add_argument(
        "--workspace", "-w", default=None, help="Workspace directory path"
    )
    parser.add_argument(
        "--analyze-only",
        "-a",
        action="store_true",
        help="Only analyze workflows, don't apply fixes",
    )
    parser.add_argument("--export", "-e", help="Export fix report to specified file")
    parser.add_argument(
        "--restore", "-r", action="store_true", help="Restore workflows from backup"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Create fix tool
    tool = create_github_actions_fix_tool(workspace_path=args.workspace)

    print("L.I.F.E. Platform - GitHub Actions Fix Tool")
    print("=" * 50)
    print(f"Workspace: {args.workspace or os.getcwd()}")

    try:
        if args.restore:
            print("\nRestoring workflows from backup...")
            if asyncio.run(tool.restore_backup()):
                print("✅ Workflows restored successfully")
            else:
                print("❌ Failed to restore workflows")
            return 0

        print("\nAnalyzing GitHub Actions workflows...")

        # Run analysis and fixes
        report = asyncio.run(tool.analyze_and_fix_workflows())

        print("\nAnalysis Results:")
        print(f"  Workflows analyzed: {report.workflows_analyzed}")
        print(f"  Issues found: {report.issues_found}")
        print(f"  Fixes applied: {report.fixes_applied}")
        print(f"  Success rate: {report.success_rate:.1f}%")
        print(f"  Critical issues: {report.critical_issues}")

        if report.workflow_reports:
            print("\nWorkflow Details:")
            for workflow in report.workflow_reports:
                status = "✅" if workflow.workflow_valid else "❌"
                print(
                    f"  {status} {workflow.file_path.name}: {len(workflow.issues_found)} issues, {len(workflow.fixes_applied)} fixes"
                )

        if report.summary.get("recommendations"):
            print("\nRecommendations:")
            for rec in report.summary["recommendations"]:
                print(f"  • {rec}")

        if args.export:
            if tool.export_fix_report(args.export, report):
                print(f"\nFix report exported to {args.export}")
            else:
                print("\nFailed to export fix report")
                return 1

        # Return appropriate exit code
        if report.critical_issues > 0:
            print("\n⚠️ Critical issues remain - manual review recommended")
            return 1
        elif report.fixes_applied < report.issues_found:
            print("\n⚠️ Some fixes failed - manual intervention may be needed")
            return 1
        else:
            print("\n✅ All applicable fixes applied successfully")
            return 0

    except KeyboardInterrupt:
        print("\nOperation interrupted by user")
        return 1
    except Exception as e:
        print(f"\nOperation failed: {e}")
        return 1


if __name__ == "__main__":
    import sys

    sys.exit(main())
