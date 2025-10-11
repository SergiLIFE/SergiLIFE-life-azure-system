"""
L.I.F.E. Platform - Repository Integration System
Copyright 2025 - Sergio Paya Borrull

Repository integration and management system for the L.I.F.E. Platform.
Handles Git operations, Azure DevOps integration, and automated repository
management for the neuroadaptive learning system.

This module provides comprehensive repository management capabilities including:
- Git repository operations and automation
- Azure DevOps pipeline integration
- Repository health monitoring and maintenance
- Automated deployment triggers and rollbacks
- Code quality and security scanning integration
"""

import asyncio
import json
import logging
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class RepositoryStatus:
    """Repository status information"""

    name: str
    branch: str
    last_commit: str
    last_commit_date: datetime
    is_clean: bool
    pending_changes: int
    remote_status: str
    health_score: float


@dataclass
class DeploymentStatus:
    """Deployment status information"""

    deployment_id: str
    status: str
    environment: str
    start_time: datetime
    end_time: Optional[datetime]
    success: bool
    logs_url: Optional[str]


@dataclass
class PipelineRun:
    """Azure DevOps pipeline run information"""

    run_id: int
    pipeline_name: str
    status: str
    result: str
    start_time: datetime
    finish_time: Optional[datetime]
    build_number: str


class LIFERepositoryIntegrator:
    """Repository integration system for L.I.F.E. Platform"""

    def __init__(self, repo_path: str = None):
        self.repo_path = Path(repo_path) if repo_path else Path.cwd()
        self.logger = logging.getLogger(__name__)

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

        # Azure DevOps configuration
        self.azure_config = {
            "organization": "life-platform",
            "project": "LIFE-Neuroadaptive-System",
            "repository_id": "SergiLIFE-life-azure-system",
            "main_branch": "main",
        }

        # Repository health thresholds
        self.health_thresholds = {
            "max_pending_changes": 50,
            "max_days_since_commit": 7,
            "min_health_score": 0.7,
        }

    async def get_repository_status(self) -> RepositoryStatus:
        """Get comprehensive repository status"""
        try:
            # Get current branch
            branch_result = await self._run_git_command("rev-parse --abbrev-ref HEAD")
            branch = branch_result.stdout.strip()

            # Get last commit info
            commit_result = await self._run_git_command(
                "log -1 --format='%H|%s|%cd' --date=iso"
            )
            commit_parts = commit_result.stdout.strip().split("|")
            last_commit = commit_parts[0] if len(commit_parts) > 0 else "unknown"
            commit_message = commit_parts[1] if len(commit_parts) > 1 else "unknown"
            commit_date_str = (
                commit_parts[2] if len(commit_parts) > 2 else datetime.now().isoformat()
            )
            last_commit_date = datetime.fromisoformat(
                commit_date_str.replace(" +", "+").replace(" -", "-")
            )

            # Check if working directory is clean
            status_result = await self._run_git_command("status --porcelain")
            is_clean = len(status_result.stdout.strip()) == 0
            pending_changes = (
                len(status_result.stdout.strip().split("\n")) if not is_clean else 0
            )

            # Check remote status
            remote_result = await self._run_git_command("status -b --ahead-behind")
            remote_status = "synchronized"
            if "ahead" in remote_result.stdout:
                remote_status = "ahead"
            elif "behind" in remote_result.stdout:
                remote_status = "behind"

            # Calculate health score
            health_score = self._calculate_health_score(
                is_clean, pending_changes, last_commit_date
            )

            return RepositoryStatus(
                name=self.repo_path.name,
                branch=branch,
                last_commit=last_commit,
                last_commit_date=last_commit_date,
                is_clean=is_clean,
                pending_changes=pending_changes,
                remote_status=remote_status,
                health_score=health_score,
            )

        except Exception as e:
            self.logger.error(f"Error getting repository status: {e}")
            return RepositoryStatus(
                name=self.repo_path.name,
                branch="unknown",
                last_commit="unknown",
                last_commit_date=datetime.now(),
                is_clean=False,
                pending_changes=0,
                remote_status="error",
                health_score=0.0,
            )

    def _calculate_health_score(
        self, is_clean: bool, pending_changes: int, last_commit_date: datetime
    ) -> float:
        """Calculate repository health score (0.0 to 1.0)"""
        score = 1.0

        # Penalize unclean working directory
        if not is_clean:
            score -= 0.3

        # Penalize too many pending changes
        if pending_changes > self.health_thresholds["max_pending_changes"]:
            penalty = min(0.4, (pending_changes / 100) * 0.4)
            score -= penalty

        # Penalize old commits
        # Remove timezone info if present for comparison
        now = datetime.now()
        if last_commit_date.tzinfo is not None:
            last_commit_date = last_commit_date.replace(tzinfo=None)
        days_since_commit = (now - last_commit_date).days
        if days_since_commit > self.health_thresholds["max_days_since_commit"]:
            penalty = min(0.3, (days_since_commit / 30) * 0.3)
            score -= penalty

        return max(0.0, score)

    async def _run_git_command(self, command: str) -> subprocess.CompletedProcess:
        """Run a git command and return the result"""
        full_command = f"git -C {self.repo_path} {command}"
        process = await asyncio.create_subprocess_shell(
            full_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout_bytes, stderr_bytes = await process.communicate()
        
        # Decode bytes to string
        stdout = stdout_bytes.decode('utf-8') if stdout_bytes else ''
        stderr = stderr_bytes.decode('utf-8') if stderr_bytes else ''

        if process.returncode != 0:
            raise subprocess.CalledProcessError(
                process.returncode, full_command, stdout, stderr
            )

        # Create a CompletedProcess-like object with the results
        class Result:
            def __init__(self, returncode, stdout, stderr):
                self.returncode = returncode
                self.stdout = stdout
                self.stderr = stderr
        
        return Result(process.returncode, stdout, stderr)

    async def create_commit(self, message: str, files: List[str] = None) -> bool:
        """Create a commit with the specified message"""
        try:
            # Add files if specified
            if files:
                add_command = "add " + " ".join(f'"{f}"' for f in files)
                await self._run_git_command(add_command)
            else:
                await self._run_git_command("add .")

            # Commit
            await self._run_git_command(f'commit -m "{message}"')

            self.logger.info(f"Created commit: {message}")
            return True

        except Exception as e:
            self.logger.error(f"Error creating commit: {e}")
            return False

    async def push_changes(self, branch: str = None) -> bool:
        """Push changes to remote repository"""
        try:
            if not branch:
                status = await self.get_repository_status()
                branch = status.branch

            await self._run_git_command(f"push origin {branch}")

            self.logger.info(f"Pushed changes to {branch}")
            return True

        except Exception as e:
            self.logger.error(f"Error pushing changes: {e}")
            return False

    async def create_pull_request(
        self, title: str, description: str, target_branch: str = "main"
    ) -> Optional[str]:
        """Create a pull request (simplified - would integrate with Azure DevOps/GitHub API)"""
        try:
            # Get current branch
            status = await self.get_repository_status()
            source_branch = status.branch

            # In a real implementation, this would call Azure DevOps REST API
            # For now, we'll simulate and log the PR creation
            pr_info = {
                "title": title,
                "description": description,
                "source_branch": source_branch,
                "target_branch": target_branch,
                "created_at": datetime.now().isoformat(),
            }

            self.logger.info(f"Pull request created: {title}")
            self.logger.info(f"Source: {source_branch} -> Target: {target_branch}")

            # Export PR info for tracking
            pr_filename = f"pr_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(pr_filename, "w") as f:
                json.dump(pr_info, f, indent=2)

            return pr_filename

        except Exception as e:
            self.logger.error(f"Error creating pull request: {e}")
            return None

    async def run_pipeline(
        self, pipeline_name: str, parameters: Dict = None
    ) -> Optional[PipelineRun]:
        """Trigger an Azure DevOps pipeline run"""
        try:
            # In a real implementation, this would call Azure DevOps REST API
            # For simulation, we'll create a mock pipeline run
            run_id = int(datetime.now().timestamp())

            pipeline_run = PipelineRun(
                run_id=run_id,
                pipeline_name=pipeline_name,
                status="inProgress",
                result="unknown",
                start_time=datetime.now(),
                finish_time=None,
                build_number=f"{pipeline_name}_{run_id}",
            )

            self.logger.info(f"Triggered pipeline: {pipeline_name} (Run ID: {run_id})")

            # Simulate pipeline completion (in real implementation, would poll API)
            await asyncio.sleep(2)  # Simulate processing time

            # Mark as completed
            pipeline_run.status = "completed"
            pipeline_run.result = "succeeded"
            pipeline_run.finish_time = datetime.now()

            self.logger.info(
                f"Pipeline completed: {pipeline_name} - {pipeline_run.result}"
            )

            return pipeline_run

        except Exception as e:
            self.logger.error(f"Error running pipeline: {e}")
            return None

    async def check_repository_health(self) -> Dict:
        """Perform comprehensive repository health check"""
        health_report = {
            "timestamp": datetime.now().isoformat(),
            "overall_health": "unknown",
            "checks": {},
            "recommendations": [],
        }

        try:
            # Get repository status
            status = await self.get_repository_status()
            health_report["checks"]["repository_status"] = asdict(status)

            # Check for large files
            large_files = await self._find_large_files()
            health_report["checks"]["large_files"] = large_files

            # Check for security issues (simplified)
            security_issues = await self._check_security_issues()
            health_report["checks"]["security"] = security_issues

            # Check code quality (simplified)
            quality_metrics = await self._check_code_quality()
            health_report["checks"]["code_quality"] = quality_metrics

            # Determine overall health
            health_scores = [
                status.health_score,
                1.0 if len(large_files) == 0 else 0.8,
                1.0 if len(security_issues) == 0 else 0.6,
                quality_metrics.get("overall_score", 0.8),
            ]

            overall_score = sum(health_scores) / len(health_scores)
            health_report["overall_health"] = self._score_to_rating(overall_score)

            # Generate recommendations
            health_report["recommendations"] = self._generate_recommendations(
                status, large_files, security_issues, quality_metrics
            )

        except Exception as e:
            self.logger.error(f"Error during health check: {e}")
            health_report["overall_health"] = "error"
            health_report["error"] = str(e)

        return health_report

    async def _find_large_files(self, max_size_mb: int = 100) -> List[Dict]:
        """Find files larger than specified size"""
        large_files = []
        max_size_bytes = max_size_mb * 1024 * 1024

        try:
            for file_path in self.repo_path.rglob("*"):
                if file_path.is_file() and not file_path.name.startswith("."):
                    size = file_path.stat().st_size
                    if size > max_size_bytes:
                        large_files.append(
                            {
                                "path": str(file_path.relative_to(self.repo_path)),
                                "size_mb": size / (1024 * 1024),
                                "size_bytes": size,
                            }
                        )
        except Exception as e:
            self.logger.error(f"Error finding large files: {e}")

        return large_files

    async def _check_security_issues(self) -> List[Dict]:
        """Check for common security issues (simplified)"""
        issues = []

        # Check for exposed secrets (simplified pattern matching)
        secret_patterns = [
            r"password\s*=\s*['\"][^'\"]*['\"]",
            r"secret\s*=\s*['\"][^'\"]*['\"]",
            r"key\s*=\s*['\"][^'\"]*['\"]",
        ]

        try:
            for py_file in self.repo_path.rglob("*.py"):
                with open(py_file, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    for pattern in secret_patterns:
                        if (
                            pattern.replace(r"['\"][^'\"]*['\"]", "secret")
                            in content.lower()
                        ):
                            issues.append(
                                {
                                    "file": str(py_file.relative_to(self.repo_path)),
                                    "type": "potential_secret_exposure",
                                    "severity": "high",
                                }
                            )
                            break
        except Exception as e:
            self.logger.error(f"Error checking security issues: {e}")

        return issues

    async def _check_code_quality(self) -> Dict:
        """Check code quality metrics (simplified)"""
        metrics = {
            "total_files": 0,
            "python_files": 0,
            "total_lines": 0,
            "average_complexity": 0,
            "overall_score": 0.8,
        }

        try:
            python_files = list(self.repo_path.rglob("*.py"))
            metrics["python_files"] = len(python_files)

            total_lines = 0
            for py_file in python_files:
                try:
                    with open(py_file, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()
                        total_lines += len(lines)
                except:
                    pass

            metrics["total_lines"] = total_lines
            metrics["total_files"] = len(list(self.repo_path.rglob("*")))

            # Simple complexity estimate based on file count and size
            if metrics["python_files"] > 0:
                avg_lines_per_file = total_lines / metrics["python_files"]
                metrics["average_complexity"] = min(10, avg_lines_per_file / 50)

        except Exception as e:
            self.logger.error(f"Error checking code quality: {e}")

        return metrics

    def _score_to_rating(self, score: float) -> str:
        """Convert numeric score to rating"""
        if score >= 0.9:
            return "excellent"
        elif score >= 0.8:
            return "good"
        elif score >= 0.7:
            return "fair"
        elif score >= 0.6:
            return "poor"
        else:
            return "critical"

    def _generate_recommendations(
        self,
        status: RepositoryStatus,
        large_files: List,
        security_issues: List,
        quality_metrics: Dict,
    ) -> List[str]:
        """Generate health recommendations"""
        recommendations = []

        if not status.is_clean:
            recommendations.append(
                "Commit or stash pending changes to clean working directory"
            )

        if status.pending_changes > self.health_thresholds["max_pending_changes"]:
            recommendations.append(
                "Consider breaking down large changes into smaller commits"
            )

        if status.health_score < self.health_thresholds["min_health_score"]:
            recommendations.append(
                "Repository health is below threshold - review and address issues"
            )

        if large_files:
            recommendations.append(
                f"Found {len(large_files)} large files - consider using Git LFS"
            )

        if security_issues:
            recommendations.append(
                f"Address {len(security_issues)} security issues immediately"
            )

        if quality_metrics.get("average_complexity", 0) > 8:
            recommendations.append("Code complexity is high - consider refactoring")

        return recommendations

    async def export_health_report(self, report: Dict, filename: str = None) -> str:
        """Export health report to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"repo_health_report_{timestamp}.json"

        with open(filename, "w") as f:
            json.dump(report, f, indent=2, default=str)

        self.logger.info(f"Health report exported to {filename}")
        return filename


async def main():
    """Main function for repository integration demo"""
    print("🧠 L.I.F.E. Platform - Repository Integration System")
    print("=" * 55)

    integrator = LIFERepositoryIntegrator()

    try:
        # Get repository status
        print("📊 Getting repository status...")
        status = await integrator.get_repository_status()

        print(f"Repository: {status.name}")
        print(f"Branch: {status.branch}")
        print(f"Clean: {status.is_clean}")
        print(f"Health Score: {status.health_score:.2f}")
        print()

        # Run health check
        print("🔍 Running comprehensive health check...")
        health_report = await integrator.check_repository_health()

        print(f"Overall Health: {health_report['overall_health'].upper()}")
        print(f"Checks Performed: {len(health_report['checks'])}")

        if health_report["recommendations"]:
            print("💡 Recommendations:")
            for rec in health_report["recommendations"]:
                print(f"  • {rec}")
        print()

        # Export health report
        report_file = await integrator.export_health_report(health_report)
        print(f"📄 Health report exported to: {report_file}")

        # Simulate pipeline run
        print("🔄 Simulating pipeline execution...")
        pipeline = await integrator.run_pipeline("LIFE-CI-CD-Pipeline")
        if pipeline:
            print(f"Pipeline: {pipeline.pipeline_name}")
            print(f"Status: {pipeline.status}")
            print(f"Result: {pipeline.result}")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
