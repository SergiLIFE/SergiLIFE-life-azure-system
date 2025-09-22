#!/usr/bin/env python3
"""
L.I.F.E. Platform - CI/CD Pipeline Fix Tool
Automated repair and optimization of CI/CD pipelines

This module provides comprehensive tools for diagnosing, fixing, and
optimizing CI/CD pipelines across different platforms (GitHub Actions,
Azure DevOps, Jenkins, etc.).

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
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class PipelineType(Enum):
    """Types of CI/CD pipelines"""

    GITHUB_ACTIONS = "github_actions"
    AZURE_DEVOPS = "azure_devops"
    JENKINS = "jenkins"
    GITLAB_CI = "gitlab_ci"
    CIRCLE_CI = "circle_ci"
    UNKNOWN = "unknown"


class PipelineIssue(Enum):
    """Types of pipeline issues that can be detected and fixed"""

    MISSING_STAGES = "missing_stages"
    INCORRECT_ORDER = "incorrect_order"
    MISSING_VALIDATION = "missing_validation"
    SECURITY_RISKS = "security_risks"
    PERFORMANCE_BOTTLENECKS = "performance_bottlenecks"
    MISSING_ERROR_HANDLING = "missing_error_handling"
    OUTDATED_TOOLS = "outdated_tools"
    CONFIGURATION_ERRORS = "configuration_errors"
    MISSING_ARTIFACTS = "missing_artifacts"
    DEPLOYMENT_ISSUES = "deployment_issues"


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


@dataclass
class PipelineFix:
    """Represents a fix to be applied to a pipeline"""

    issue_type: PipelineIssue
    priority: FixPriority
    description: str
    file_path: Path
    pipeline_type: PipelineType
    line_number: Optional[int] = None
    fix_applied: bool = False
    status: FixStatus = FixStatus.PENDING
    before_content: str = ""
    after_content: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    error_message: str = ""
    recommendations: List[str] = field(default_factory=list)


@dataclass
class PipelineAnalysis:
    """Analysis results for a pipeline file"""

    file_path: Path
    pipeline_type: PipelineType
    issues_found: List[PipelineFix] = field(default_factory=list)
    fixes_applied: List[PipelineFix] = field(default_factory=list)
    analysis_timestamp: datetime = field(default_factory=datetime.now)
    pipeline_valid: bool = True
    recommendations: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CICDPipelineReport:
    """Comprehensive CI/CD pipeline fix report"""

    total_pipelines: int = 0
    pipelines_analyzed: int = 0
    issues_found: int = 0
    fixes_applied: int = 0
    critical_issues: int = 0
    success_rate: float = 0.0
    analysis_timestamp: datetime = field(default_factory=datetime.now)
    pipeline_reports: List[PipelineAnalysis] = field(default_factory=list)
    summary: Dict[str, Any] = field(default_factory=dict)


class CICDPipelineFixTool:
    """
    CI/CD Pipeline Fix Tool for L.I.F.E. Platform

    Provides automated diagnosis and repair of CI/CD pipelines
    across multiple platforms to ensure reliable deployments.
    """

    def __init__(self, workspace_path: Optional[str] = None):
        self.workspace_path = Path(workspace_path or os.getcwd())
        self.analysis_results: List[PipelineAnalysis] = []
        self.backup_created = False

        # Pipeline file patterns
        self.pipeline_patterns = {
            PipelineType.GITHUB_ACTIONS: [
                ".github/workflows/*.yml",
                ".github/workflows/*.yaml",
            ],
            PipelineType.AZURE_DEVOPS: [
                "azure-pipelines.yml",
                ".azure-pipelines/*.yml",
            ],
            PipelineType.JENKINS: ["Jenkinsfile", "jenkins/*.groovy"],
            PipelineType.GITLAB_CI: [".gitlab-ci.yml"],
            PipelineType.CIRCLE_CI: [".circleci/config.yml"],
        }

        logger.info(
            f"CI/CD Pipeline Fix Tool initialized for workspace: {self.workspace_path}"
        )

    async def analyze_and_fix_pipelines(self) -> CICDPipelineReport:
        """Analyze all pipelines and apply fixes"""
        logger.info("Starting CI/CD pipeline analysis and fixes...")

        # Create backup of pipeline files
        await self._create_backup()

        # Find all pipeline files
        pipeline_files = self._find_pipeline_files()

        if not pipeline_files:
            logger.warning("No pipeline files found")
            return CICDPipelineReport()

        report = CICDPipelineReport(total_pipelines=len(pipeline_files))

        # Analyze each pipeline
        for pipeline_file in pipeline_files:
            try:
                analysis = await self._analyze_pipeline(pipeline_file)
                self.analysis_results.append(analysis)
                report.pipeline_reports.append(analysis)
                report.pipelines_analyzed += 1

                # Apply fixes
                fixes_applied = await self._apply_pipeline_fixes(analysis)
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
                logger.error(f"Failed to analyze {pipeline_file}: {e}")
                # Create minimal analysis for failed pipelines
                failed_analysis = PipelineAnalysis(
                    file_path=pipeline_file,
                    pipeline_type=PipelineType.UNKNOWN,
                    pipeline_valid=False,
                    recommendations=[f"Manual review required: {str(e)}"],
                )
                self.analysis_results.append(failed_analysis)
                report.pipeline_reports.append(failed_analysis)

        # Calculate success rate
        if report.issues_found > 0:
            report.success_rate = (report.fixes_applied / report.issues_found) * 100

        # Generate summary
        report.summary = self._generate_summary_report(report)

        logger.info(
            f"CI/CD pipeline analysis complete. Fixed {report.fixes_applied}/{report.issues_found} issues"
        )
        return report

    async def _create_backup(self):
        """Create backup of pipeline directories"""
        try:
            backup_dirs = [".github", ".azure-pipelines", ".gitlab-ci", ".circleci"]
            jenkins_dirs = ["jenkins"]

            for backup_dir in backup_dirs + jenkins_dirs:
                source_path = self.workspace_path / backup_dir
                if source_path.exists():
                    backup_path = self.workspace_path / f"{backup_dir}.backup"
                    if backup_path.exists():
                        shutil.rmtree(backup_path)
                    shutil.copytree(source_path, backup_path)
                    self.backup_created = True
                    logger.info(f"Pipeline backup created at {backup_path}")

            # Backup root-level pipeline files
            root_files = ["azure-pipelines.yml", "Jenkinsfile", ".gitlab-ci.yml"]
            for file_name in root_files:
                file_path = self.workspace_path / file_name
                if file_path.exists():
                    backup_path = self.workspace_path / f"{file_name}.backup"
                    shutil.copy2(file_path, backup_path)
                    self.backup_created = True
                    logger.info(f"Pipeline file backup created at {backup_path}")

        except Exception as e:
            logger.warning(f"Failed to create pipeline backup: {e}")

    def _find_pipeline_files(self) -> List[Path]:
        """Find all CI/CD pipeline files"""
        pipeline_files = []

        # Check for each pipeline type
        for pipeline_type, patterns in self.pipeline_patterns.items():
            for pattern in patterns:
                try:
                    # Handle glob patterns
                    if "*" in pattern:
                        base_path = self.workspace_path
                        glob_pattern = pattern
                        matches = list(base_path.glob(glob_pattern))
                        pipeline_files.extend(matches)
                    else:
                        # Direct file check
                        file_path = self.workspace_path / pattern
                        if file_path.exists():
                            pipeline_files.append(file_path)
                except Exception as e:
                    logger.warning(f"Error checking pattern {pattern}: {e}")

        # Remove duplicates
        seen = set()
        unique_files = []
        for file_path in pipeline_files:
            if file_path not in seen:
                seen.add(file_path)
                unique_files.append(file_path)

        return unique_files

    def _detect_pipeline_type(self, file_path: Path) -> PipelineType:
        """Detect the type of CI/CD pipeline from file path and content"""
        file_name = file_path.name
        parent_dirs = [p.name for p in file_path.parents if p != self.workspace_path]

        # Check file path patterns
        if ".github" in parent_dirs and "workflows" in parent_dirs:
            return PipelineType.GITHUB_ACTIONS
        elif file_name == "azure-pipelines.yml" or ".azure-pipelines" in parent_dirs:
            return PipelineType.AZURE_DEVOPS
        elif file_name == "Jenkinsfile" or "jenkins" in parent_dirs:
            return PipelineType.JENKINS
        elif file_name == ".gitlab-ci.yml":
            return PipelineType.GITLAB_CI
        elif ".circleci" in parent_dirs and file_name == "config.yml":
            return PipelineType.CIRCLE_CI

        # Check file content for detection
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read(1000)  # Read first 1000 chars

            if "jobs:" in content and "runs-on:" in content:
                return PipelineType.GITHUB_ACTIONS
            elif "stages:" in content and ("pool:" in content or "vmImage:" in content):
                return PipelineType.AZURE_DEVOPS
            elif "pipeline" in content and ("agent" in content or "docker" in content):
                return PipelineType.JENKINS
            elif "stages:" in content and "script:" in content:
                return PipelineType.GITLAB_CI
            elif "version:" in content and "workflows:" in content:
                return PipelineType.CIRCLE_CI

        except Exception:
            pass

        return PipelineType.UNKNOWN

    async def _analyze_pipeline(self, pipeline_file: Path) -> PipelineAnalysis:
        """Analyze a single pipeline file for issues"""
        pipeline_type = self._detect_pipeline_type(pipeline_file)

        analysis = PipelineAnalysis(
            file_path=pipeline_file, pipeline_type=pipeline_type
        )

        try:
            # Read pipeline content
            with open(pipeline_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Analyze based on pipeline type
            if pipeline_type == PipelineType.GITHUB_ACTIONS:
                issues = self._analyze_github_actions(content)
            elif pipeline_type == PipelineType.AZURE_DEVOPS:
                issues = self._analyze_azure_devops(content)
            elif pipeline_type == PipelineType.JENKINS:
                issues = self._analyze_jenkins(content)
            elif pipeline_type == PipelineType.GITLAB_CI:
                issues = self._analyze_gitlab_ci(content)
            elif pipeline_type == PipelineType.CIRCLE_CI:
                issues = self._analyze_circle_ci(content)
            else:
                issues = [
                    PipelineFix(
                        issue_type=PipelineIssue.CONFIGURATION_ERRORS,
                        priority=FixPriority.MEDIUM,
                        description="Unknown pipeline type - manual review required",
                        file_path=pipeline_file,
                        pipeline_type=pipeline_type,
                    )
                ]

            # Set file path for all issues
            for issue in issues:
                issue.file_path = pipeline_file

            analysis.issues_found = issues

            # Validate pipeline structure
            analysis.pipeline_valid = self._validate_pipeline_structure(
                content, pipeline_type
            )

            # Generate recommendations
            analysis.recommendations = self._generate_pipeline_recommendations(
                issues, pipeline_type
            )

            # Extract metadata
            analysis.metadata = self._extract_pipeline_metadata(content, pipeline_type)

        except Exception as e:
            logger.error(f"Error analyzing {pipeline_file}: {e}")
            analysis.pipeline_valid = False
            analysis.recommendations = [f"Analysis failed: {str(e)}"]

        return analysis

    def _analyze_github_actions(self, content: str) -> List[PipelineFix]:
        """Analyze GitHub Actions workflow"""
        issues = []

        # Check for required elements
        if "on:" not in content:
            issues.append(
                PipelineFix(
                    issue_type=PipelineIssue.MISSING_STAGES,
                    priority=FixPriority.CRITICAL,
                    description="Missing trigger configuration (on: section)",
                    file_path=Path("dummy"),
                    pipeline_type=PipelineType.GITHUB_ACTIONS,
                )
            )

        if "jobs:" not in content:
            issues.append(
                PipelineFix(
                    issue_type=PipelineIssue.MISSING_STAGES,
                    priority=FixPriority.CRITICAL,
                    description="Missing jobs configuration",
                    file_path=Path("dummy"),
                    pipeline_type=PipelineType.GITHUB_ACTIONS,
                )
            )

        # Check for checkout action
        if "actions/checkout" not in content:
            issues.append(
                PipelineFix(
                    issue_type=PipelineIssue.MISSING_VALIDATION,
                    priority=FixPriority.HIGH,
                    description="Missing repository checkout action",
                    file_path=Path("dummy"),
                    pipeline_type=PipelineType.GITHUB_ACTIONS,
                )
            )

        # Check for security issues
        if "permissions:" not in content and "azure" in content.lower():
            issues.append(
                PipelineFix(
                    issue_type=PipelineIssue.SECURITY_RISKS,
                    priority=FixPriority.HIGH,
                    description="Missing permissions for Azure operations",
                    file_path=Path("dummy"),
                    pipeline_type=PipelineType.GITHUB_ACTIONS,
                )
            )

        # Check for outdated actions
        outdated_patterns = [
            "actions/checkout@v1",
            "actions/checkout@v2",
            "actions/setup-python@v1",
            "actions/setup-python@v2",
        ]

        for pattern in outdated_patterns:
            if pattern in content:
                issues.append(
                    PipelineFix(
                        issue_type=PipelineIssue.OUTDATED_TOOLS,
                        priority=FixPriority.MEDIUM,
                        description=f"Outdated action: {pattern}",
                        file_path=Path("dummy"),
                        pipeline_type=PipelineType.GITHUB_ACTIONS,
                    )
                )

        return issues

    def _analyze_azure_devops(self, content: str) -> List[PipelineFix]:
        """Analyze Azure DevOps pipeline"""
        issues = []

        # Check for required elements
        if "trigger:" not in content and "pr:" not in content:
            issues.append(
                PipelineFix(
                    issue_type=PipelineIssue.MISSING_STAGES,
                    priority=FixPriority.CRITICAL,
                    description="Missing trigger or PR configuration",
                    file_path=Path("dummy"),
                    pipeline_type=PipelineType.AZURE_DEVOPS,
                )
            )

        if "stages:" not in content and "jobs:" not in content:
            issues.append(
                PipelineFix(
                    issue_type=PipelineIssue.MISSING_STAGES,
                    priority=FixPriority.CRITICAL,
                    description="Missing stages or jobs configuration",
                    file_path=Path("dummy"),
                    pipeline_type=PipelineType.AZURE_DEVOPS,
                )
            )

        # Check for checkout task
        if "checkout:" not in content and "task: Checkout@" not in content:
            issues.append(
                PipelineFix(
                    issue_type=PipelineIssue.MISSING_VALIDATION,
                    priority=FixPriority.HIGH,
                    description="Missing repository checkout task",
                    file_path=Path("dummy"),
                    pipeline_type=PipelineType.AZURE_DEVOPS,
                )
            )

        return issues

    def _analyze_jenkins(self, content: str) -> List[PipelineFix]:
        """Analyze Jenkins pipeline"""
        issues = []

        # Basic checks for Jenkinsfile
        if "pipeline" not in content:
            issues.append(
                PipelineFix(
                    issue_type=PipelineIssue.MISSING_STAGES,
                    priority=FixPriority.CRITICAL,
                    description="Missing pipeline block",
                    file_path=Path("dummy"),
                    pipeline_type=PipelineType.JENKINS,
                )
            )

        if "agent" not in content:
            issues.append(
                PipelineFix(
                    issue_type=PipelineIssue.MISSING_STAGES,
                    priority=FixPriority.HIGH,
                    description="Missing agent configuration",
                    file_path=Path("dummy"),
                    pipeline_type=PipelineType.JENKINS,
                )
            )

        return issues

    def _analyze_gitlab_ci(self, content: str) -> List[PipelineFix]:
        """Analyze GitLab CI pipeline"""
        issues = []

        # Check for basic structure
        if "stages:" not in content:
            issues.append(
                PipelineFix(
                    issue_type=PipelineIssue.MISSING_STAGES,
                    priority=FixPriority.CRITICAL,
                    description="Missing stages configuration",
                    file_path=Path("dummy"),
                    pipeline_type=PipelineType.GITLAB_CI,
                )
            )

        return issues

    def _analyze_circle_ci(self, content: str) -> List[PipelineFix]:
        """Analyze CircleCI pipeline"""
        issues = []

        # Check for basic structure
        if "workflows:" not in content:
            issues.append(
                PipelineFix(
                    issue_type=PipelineIssue.MISSING_STAGES,
                    priority=FixPriority.CRITICAL,
                    description="Missing workflows configuration",
                    file_path=Path("dummy"),
                    pipeline_type=PipelineType.CIRCLE_CI,
                )
            )

        return issues

    def _validate_pipeline_structure(
        self, content: str, pipeline_type: PipelineType
    ) -> bool:
        """Validate basic pipeline structure"""
        try:
            if pipeline_type == PipelineType.GITHUB_ACTIONS:
                return "jobs:" in content and (
                    "on:" in content or "workflow_dispatch:" in content
                )
            elif pipeline_type == PipelineType.AZURE_DEVOPS:
                return ("stages:" in content or "jobs:" in content) and (
                    "trigger:" in content or "pr:" in content
                )
            elif pipeline_type == PipelineType.JENKINS:
                return "pipeline" in content and "agent" in content
            elif pipeline_type == PipelineType.GITLAB_CI:
                return "stages:" in content
            elif pipeline_type == PipelineType.CIRCLE_CI:
                return "workflows:" in content and "version:" in content
            else:
                return False
        except Exception:
            return False

    def _generate_pipeline_recommendations(
        self, issues: List[PipelineFix], pipeline_type: PipelineType
    ) -> List[str]:
        """Generate recommendations based on issues found"""
        recommendations = []

        issue_types = {issue.issue_type for issue in issues}

        if PipelineIssue.MISSING_STAGES in issue_types:
            recommendations.append("Add missing pipeline stages/jobs configuration")

        if PipelineIssue.SECURITY_RISKS in issue_types:
            recommendations.append("Review and fix security configurations")

        if PipelineIssue.OUTDATED_TOOLS in issue_types:
            recommendations.append("Update to latest tool versions")

        if PipelineIssue.MISSING_VALIDATION in issue_types:
            recommendations.append("Add proper validation and error handling")

        if not recommendations:
            recommendations.append(
                "Pipeline structure appears good - consider adding monitoring and notifications"
            )

        return recommendations

    def _extract_pipeline_metadata(
        self, content: str, pipeline_type: PipelineType
    ) -> Dict[str, Any]:
        """Extract metadata from pipeline content"""
        metadata = {
            "pipeline_type": pipeline_type.value,
            "estimated_stages": 0,
            "estimated_jobs": 0,
            "has_artifacts": False,
            "has_testing": False,
            "has_deployment": False,
        }

        try:
            if pipeline_type == PipelineType.GITHUB_ACTIONS:
                metadata["estimated_jobs"] = content.count("jobs:")
                metadata["has_artifacts"] = "actions/upload-artifact" in content
                metadata["has_testing"] = "pytest" in content or "unittest" in content
                metadata["has_deployment"] = "azure" in content.lower()

            elif pipeline_type == PipelineType.AZURE_DEVOPS:
                metadata["estimated_stages"] = content.count("stages:")
                metadata["estimated_jobs"] = content.count("jobs:")
                metadata["has_artifacts"] = (
                    "PublishBuildArtifacts" in content
                    or "PublishPipelineArtifact" in content
                )
                metadata["has_testing"] = (
                    "VSTest" in content or "DotNetCoreCLI" in content
                )
                metadata["has_deployment"] = (
                    "AzureRmWebAppDeployment" in content
                    or "AzureResourceManagerTemplateDeployment" in content
                )

        except Exception as e:
            logger.warning(f"Failed to extract metadata: {e}")

        return metadata

    async def _apply_pipeline_fixes(
        self, analysis: PipelineAnalysis
    ) -> List[PipelineFix]:
        """Apply fixes to a pipeline"""
        applied_fixes = []

        for fix in analysis.issues_found:
            try:
                if await self._apply_single_pipeline_fix(fix):
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

    async def _apply_single_pipeline_fix(self, fix: PipelineFix) -> bool:
        """Apply a single fix to the pipeline"""
        try:
            # Read current content
            with open(fix.file_path, "r", encoding="utf-8") as f:
                content = f.read()

            fix.before_content = content

            # Apply fix based on type and pipeline type
            success = False

            if fix.pipeline_type == PipelineType.GITHUB_ACTIONS:
                success = self._apply_github_actions_fix(fix, content)
            elif fix.pipeline_type == PipelineType.AZURE_DEVOPS:
                success = self._apply_azure_devops_fix(fix, content)
            # Add other pipeline types as needed

            # Write back if content changed
            if success and content != fix.before_content:
                with open(fix.file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                fix.after_content = content
                return True

        except Exception as e:
            logger.error(f"Failed to apply fix: {e}")
            return False

        return False

    def _apply_github_actions_fix(self, fix: PipelineFix, content: str) -> bool:
        """Apply fix to GitHub Actions workflow"""
        lines = content.split("\n")
        modified = False

        if fix.issue_type == PipelineIssue.OUTDATED_TOOLS:
            # Update outdated actions
            replacements = {
                "actions/checkout@v1": "actions/checkout@v4",
                "actions/checkout@v2": "actions/checkout@v4",
                "actions/checkout@v3": "actions/checkout@v4",
                "actions/setup-python@v1": "actions/setup-python@v4",
                "actions/setup-python@v2": "actions/setup-python@v4",
                "actions/setup-python@v3": "actions/setup-python@v4",
            }

            for old, new in replacements.items():
                if old in content:
                    content = content.replace(old, new)
                    modified = True
                    break

        elif fix.issue_type == PipelineIssue.SECURITY_RISKS:
            # Add permissions for Azure
            if "permissions:" not in content:
                # Find position after 'on:' section
                insert_pos = -1
                for i, line in enumerate(lines):
                    if line.strip().startswith("on:"):
                        # Find end of on section
                        j = i + 1
                        while j < len(lines) and (
                            lines[j].startswith(" ") or lines[j].strip() == ""
                        ):
                            j += 1
                        insert_pos = j
                        break

                if insert_pos >= 0:
                    permissions_block = [
                        "permissions:",
                        "  id-token: write",
                        "  contents: read",
                        "",
                    ]
                    lines[insert_pos:insert_pos] = permissions_block
                    modified = True

        if modified:
            content = "\n".join(lines)

        return modified

    def _apply_azure_devops_fix(self, fix: PipelineFix, content: str) -> bool:
        """Apply fix to Azure DevOps pipeline"""
        # Placeholder for Azure DevOps fixes
        return False

    def _generate_summary_report(self, report: CICDPipelineReport) -> Dict[str, Any]:
        """Generate summary report"""
        summary = {
            "pipelines_processed": report.pipelines_analyzed,
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

    def export_pipeline_report(self, filepath: str, report: CICDPipelineReport) -> bool:
        """Export comprehensive pipeline fix report"""
        try:
            export_data = {
                "report_timestamp": datetime.now().isoformat(),
                "summary": report.summary,
                "pipeline_details": [],
            }

            for pipeline_report in report.pipeline_reports:
                pipeline_detail = {
                    "file_path": str(pipeline_report.file_path),
                    "pipeline_type": pipeline_report.pipeline_type.value,
                    "valid": pipeline_report.pipeline_valid,
                    "issues_found": len(pipeline_report.issues_found),
                    "fixes_applied": len(pipeline_report.fixes_applied),
                    "recommendations": pipeline_report.recommendations,
                    "metadata": pipeline_report.metadata,
                    "issues": [
                        {
                            "type": issue.issue_type.value,
                            "priority": issue.priority.value,
                            "description": issue.description,
                            "status": issue.status.value,
                            "applied": issue.fix_applied,
                        }
                        for issue in pipeline_report.issues_found
                    ],
                }
                export_data["pipeline_details"].append(pipeline_detail)

            with open(filepath, "w") as f:
                json.dump(export_data, f, indent=2, default=str)

            logger.info(f"Pipeline report exported to {filepath}")
            return True

        except Exception as e:
            logger.error(f"Failed to export pipeline report: {e}")
            return False

    async def restore_backup(self) -> bool:
        """Restore pipelines from backup"""
        try:
            if not self.backup_created:
                logger.warning("No backup available to restore")
                return False

            # Restore backed up directories
            backup_dirs = [
                ".github",
                ".azure-pipelines",
                ".gitlab-ci",
                ".circleci",
                "jenkins",
            ]

            for backup_dir in backup_dirs:
                backup_path = self.workspace_path / f"{backup_dir}.backup"
                original_path = self.workspace_path / backup_dir

                if backup_path.exists():
                    if original_path.exists():
                        shutil.rmtree(original_path)
                    shutil.copytree(backup_path, original_path)
                    logger.info(f"Restored {backup_dir} from backup")

            # Restore root-level files
            root_files = ["azure-pipelines.yml", "Jenkinsfile", ".gitlab-ci.yml"]
            for file_name in root_files:
                backup_path = self.workspace_path / f"{file_name}.backup"
                original_path = self.workspace_path / file_name

                if backup_path.exists():
                    shutil.copy2(backup_path, original_path)
                    logger.info(f"Restored {file_name} from backup")

            return True

        except Exception as e:
            logger.error(f"Failed to restore backup: {e}")
            return False


# Factory function for easy instantiation
def create_cicd_pipeline_fix_tool(
    workspace_path: Optional[str] = None,
) -> CICDPipelineFixTool:
    """
    Factory function to create CI/CD pipeline fix tool

    Args:
        workspace_path: Path to workspace directory

    Returns:
        Configured CICDPipelineFixTool instance
    """
    return CICDPipelineFixTool(workspace_path=workspace_path)


# Command-line interface
def main():
    """Main CLI function for CI/CD pipeline fixes"""
    import argparse

    parser = argparse.ArgumentParser(
        description="L.I.F.E. Platform CI/CD Pipeline Fix Tool"
    )
    parser.add_argument(
        "--workspace", "-w", default=None, help="Workspace directory path"
    )
    parser.add_argument(
        "--analyze-only",
        "-a",
        action="store_true",
        help="Only analyze pipelines, don't apply fixes",
    )
    parser.add_argument(
        "--export", "-e", help="Export pipeline report to specified file"
    )
    parser.add_argument(
        "--restore", "-r", action="store_true", help="Restore pipelines from backup"
    )
    parser.add_argument(
        "--pipeline-type",
        "-t",
        choices=["github", "azure", "jenkins", "gitlab", "circle"],
        help="Focus on specific pipeline type",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Create pipeline fix tool
    tool = create_cicd_pipeline_fix_tool(workspace_path=args.workspace)

    print("L.I.F.E. Platform - CI/CD Pipeline Fix Tool")
    print("=" * 50)
    print(f"Workspace: {args.workspace or os.getcwd()}")

    try:
        if args.restore:
            print("\nRestoring pipelines from backup...")
            if asyncio.run(tool.restore_backup()):
                print("✅ Pipelines restored successfully")
            else:
                print("❌ Failed to restore pipelines")
            return 0

        print("\nAnalyzing CI/CD pipelines...")

        # Run analysis and fixes
        report = asyncio.run(tool.analyze_and_fix_pipelines())

        print("\nAnalysis Results:")
        print(f"  Pipelines analyzed: {report.pipelines_analyzed}")
        print(f"  Issues found: {report.issues_found}")
        print(f"  Fixes applied: {report.fixes_applied}")
        print(f"  Success rate: {report.success_rate:.1f}%")
        print(f"  Critical issues: {report.critical_issues}")

        if report.pipeline_reports:
            print("\nPipeline Details:")
            for pipeline in report.pipeline_reports:
                status = "✅" if pipeline.pipeline_valid else "❌"
                print(
                    f"  {status} {pipeline.file_path.name} ({pipeline.pipeline_type.value}): {len(pipeline.issues_found)} issues, {len(pipeline.fixes_applied)} fixes"
                )

        if report.summary.get("recommendations"):
            print("\nRecommendations:")
            for rec in report.summary["recommendations"]:
                print(f"  • {rec}")

        if args.export:
            if tool.export_pipeline_report(args.export, report):
                print(f"\nPipeline report exported to {args.export}")
            else:
                print("\nFailed to export pipeline report")
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
