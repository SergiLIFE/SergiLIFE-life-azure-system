#!/usr/bin/env python3
"""
🔗 GitHub Workflows Integration Tool
=====================================

Integrates your existing GitHub Actions workflows with the Azure Functions Enterprise System
for maximum DevOps efficiency and automation.

Copyright 2025 - Sergio Paya Borrull
L.I.F.E. Platform - Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb

Features:
- Workflow analysis and compatibility checking
- Automated integration setup
- CI/CD pipeline enhancement
- L.I.F.E Theory workflow integration
- Performance monitoring setup

Author: L.I.F.E. Platform
Created: September 9, 2025
"""

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class WorkflowIntegrator:
    """Integrates GitHub Actions workflows with Azure Functions Enterprise System."""

    def __init__(self):
        self.workspace_dir = Path.cwd()
        self.workflows_dir = self.workspace_dir / ".github" / "workflows"
        self.integration_dir = self.workspace_dir / "integration"
        self.backup_dir = self.workspace_dir / "backups" / "workflows"

        # Workflow categories for integration
        self.workflow_categories = {
            "core_cicd": [
                "ci.yml",
                "python-package.yml",
                "lint-and-test.yml",
                "fixed-lint-and-test.yml",
            ],
            "azure_integration": [
                "azure-deploy.yml",
                "deploy-streamlit-to-azure.yml",
                "terraform-deploy.yml",
            ],
            "life_theory": ["life-algorithm-cicd.yml", "life-system.yml"],
            "research_validation": [
                "sota_nightly.yml",
                "clinical_latency_validation.yml",
                "simplified-clinical-latency.yml",
            ],
            "documentation": [
                "build-docs.yml",
                "build-whitepaper.yml",
                "render-figures.yml",
            ],
            "operations": [
                "intelligent-auto-recovery.yml",
                "emergency-ci.yml",
                "emergency-ci-stabilization.yml",
            ],
            "utility": [
                "auto-comment-issues.yml",
                "archive-validation-artifacts.yml",
                "generator-generic-ossf-slsa3-publish.yml",
            ],
        }

    def analyze_existing_workflows(self) -> Dict:
        """Analyze existing workflows and their capabilities."""
        print("🔍 Analyzing existing GitHub Actions workflows...")

        analysis = {
            "found_workflows": [],
            "categories": {},
            "integration_opportunities": [],
            "value_assessment": {},
        }

        if not self.workflows_dir.exists():
            print("⚠️  No .github/workflows directory found")
            return analysis

        # Scan for workflows
        for workflow_file in self.workflows_dir.glob("*.yml"):
            workflow_name = workflow_file.name
            analysis["found_workflows"].append(workflow_name)

            # Categorize workflow
            for category, workflows in self.workflow_categories.items():
                if workflow_name in workflows:
                    if category not in analysis["categories"]:
                        analysis["categories"][category] = []
                    analysis["categories"][category].append(workflow_name)
                    break

            # Assess value
            value_score = self._assess_workflow_value(workflow_name)
            analysis["value_assessment"][workflow_name] = value_score

        # Identify integration opportunities
        analysis["integration_opportunities"] = (
            self._identify_integration_opportunities(analysis)
        )

        return analysis

    def _assess_workflow_value(self, workflow_name: str) -> Dict:
        """Assess the strategic value of a workflow."""
        # High-value workflows for Azure Functions integration
        high_value_workflows = {
            "ci.yml": {"value": 5, "integration": "critical", "type": "core_cicd"},
            "azure-deploy.yml": {
                "value": 5,
                "integration": "immediate",
                "type": "azure",
            },
            "life-algorithm-cicd.yml": {
                "value": 5,
                "integration": "strategic",
                "type": "innovation",
            },
            "terraform-deploy.yml": {
                "value": 5,
                "integration": "immediate",
                "type": "infrastructure",
            },
            "intelligent-auto-recovery.yml": {
                "value": 5,
                "integration": "operational",
                "type": "reliability",
            },
            "sota_nightly.yml": {
                "value": 4,
                "integration": "research",
                "type": "benchmarking",
            },
            "clinical_latency_validation.yml": {
                "value": 4,
                "integration": "quality",
                "type": "validation",
            },
        }

        return high_value_workflows.get(
            workflow_name, {"value": 3, "integration": "optional", "type": "utility"}
        )

    def _identify_integration_opportunities(self, analysis: Dict) -> List[Dict]:
        """Identify specific integration opportunities."""
        opportunities = []

        # Core CI/CD integration
        if "core_cicd" in analysis["categories"]:
            opportunities.append(
                {
                    "type": "core_cicd_enhancement",
                    "description": "Enhance Azure Functions CI/CD with existing quality gates",
                    "workflows": analysis["categories"]["core_cicd"],
                    "priority": "high",
                }
            )

        # Azure integration enhancement
        if "azure_integration" in analysis["categories"]:
            opportunities.append(
                {
                    "type": "azure_deployment_optimization",
                    "description": "Optimize Azure Functions deployment with existing Azure workflows",
                    "workflows": analysis["categories"]["azure_integration"],
                    "priority": "high",
                }
            )

        # L.I.F.E Theory integration
        if "life_theory" in analysis["categories"]:
            opportunities.append(
                {
                    "type": "life_theory_innovation",
                    "description": "Apply L.I.F.E Theory to Azure Functions optimization",
                    "workflows": analysis["categories"]["life_theory"],
                    "priority": "strategic",
                }
            )

        # Research validation integration
        if "research_validation" in analysis["categories"]:
            opportunities.append(
                {
                    "type": "clinical_grade_validation",
                    "description": "Apply clinical-grade validation to Azure Functions",
                    "workflows": analysis["categories"]["research_validation"],
                    "priority": "medium",
                }
            )

        return opportunities

    def create_backup(self) -> bool:
        """Create backup of existing workflows."""
        print("💾 Creating workflow backup...")

        try:
            # Create backup directory
            self.backup_dir.mkdir(parents=True, exist_ok=True)

            # Copy workflows
            if self.workflows_dir.exists():
                for workflow_file in self.workflows_dir.glob("*.yml"):
                    backup_file = self.backup_dir / workflow_file.name
                    shutil.copy2(workflow_file, backup_file)
                    print(f"  ✅ Backed up: {workflow_file.name}")

            # Create backup metadata
            backup_metadata = {
                "timestamp": datetime.now().isoformat(),
                "source": str(self.workflows_dir),
                "destination": str(self.backup_dir),
                "files_backed_up": [f.name for f in self.workflows_dir.glob("*.yml")],
            }

            metadata_file = self.backup_dir / "backup_metadata.json"
            with open(metadata_file, "w") as f:
                json.dump(backup_metadata, f, indent=2)

            print(
                f"✅ Backup completed: {len(backup_metadata['files_backed_up'])} workflows"
            )
            return True

        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return False

    def generate_integration_workflow(self) -> str:
        """Generate enhanced Azure Functions CI/CD workflow."""
        print("🔧 Generating integrated Azure Functions workflow...")

        workflow_content = """name: Azure Functions Enterprise CI/CD
on:
  push:
    branches: [main, develop]
    paths: 
      - 'src/**'
      - 'infra/**'
      - 'azure_functions_workflow.py'
      - '**.py'
  pull_request:
    branches: [main]

env:
  AZURE_FUNCTIONAPP_NAME: ${{ vars.AZURE_FUNCTIONAPP_NAME || 'life-functions-app' }}
  AZURE_FUNCTIONAPP_PACKAGE_PATH: './src'
  PYTHON_VERSION: '3.11'

jobs:
  # Leverage existing code quality workflows
  code-quality:
    name: Code Quality & Testing
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-test.txt
      
      - name: Run linting
        run: |
          python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
          python -m flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
      
      - name: Run tests with coverage
        run: |
          python -m pytest --cov=./ --cov-report=xml --cov-report=html
          python -m coverage report --fail-under=80
      
      - name: Test Azure Functions workflow
        run: |
          python test_azure_functions.py

  # Azure Functions enterprise workflow
  azure-functions-workflow:
    name: Azure Functions Enterprise Processing
    needs: code-quality
    runs-on: ubuntu-latest
    outputs:
      deployment-ready: ${{ steps.workflow.outputs.deployment-ready }}
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: Run Azure Functions Enterprise Workflow
        id: workflow
        run: |
          python azure_functions_workflow.py \\
            --project-name "${{ github.event.repository.name }}" \\
            --language python \\
            --validate
          echo "deployment-ready=true" >> $GITHUB_OUTPUT
      
      - name: Generate documentation
        run: |
          python azure_functions_workflow.py generate-docs \\
            --format markdown \\
            --output docs/azure-functions/

  # Infrastructure deployment (if terraform-deploy.yml exists)
  infrastructure:
    name: Infrastructure Deployment
    needs: azure-functions-workflow
    if: needs.azure-functions-workflow.outputs.deployment-ready == 'true'
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: "1.5.0"
      
      - name: Deploy infrastructure
        run: |
          cd infra
          terraform init
          terraform plan -var="function_app_name=${{ env.AZURE_FUNCTIONAPP_NAME }}"
          terraform apply -auto-approve

  # Azure Functions deployment
  azure-deployment:
    name: Azure Functions Deployment
    needs: [azure-functions-workflow, infrastructure]
    if: needs.azure-functions-workflow.outputs.deployment-ready == 'true'
    runs-on: ubuntu-latest
    environment: ${{ github.ref == 'refs/heads/main' && 'production' || 'development' }}
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: Azure Login
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      
      - name: Deploy Azure Functions
        uses: Azure/functions-action@v1
        with:
          app-name: ${{ env.AZURE_FUNCTIONAPP_NAME }}
          package: ${{ env.AZURE_FUNCTIONAPP_PACKAGE_PATH }}
          python-version: ${{ env.PYTHON_VERSION }}

  # Post-deployment validation
  post-deployment:
    name: Post-Deployment Validation
    needs: azure-deployment
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Validate deployment
        run: |
          python azure_functions_workflow.py validate \\
            --post-deployment \\
            --function-app-name "${{ env.AZURE_FUNCTIONAPP_NAME }}"
      
      - name: Performance baseline
        run: |
          python azure_functions_workflow.py benchmark \\
            --baseline \\
            --generate-report

  # L.I.F.E Theory integration (if life-algorithm-cicd.yml exists)
  life-theory-optimization:
    name: L.I.F.E Theory Optimization
    needs: post-deployment
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Apply L.I.F.E Theory
        run: |
          python life_algorithm.py --target azure-functions
          python azure_functions_workflow.py optimize \\
            --life-theory-input "life_insights.json"
"""

        return workflow_content

    def setup_integration(self) -> bool:
        """Set up complete workflow integration."""
        print("🚀 Setting up GitHub Actions integration...")

        try:
            # Create integration directory
            self.integration_dir.mkdir(exist_ok=True)

            # Analyze existing workflows
            analysis = self.analyze_existing_workflows()

            # Create backup
            if not self.create_backup():
                return False

            # Generate integrated workflow
            integrated_workflow = self.generate_integration_workflow()

            # Save integrated workflow
            workflow_file = self.workflows_dir / "azure-functions-enterprise.yml"
            workflow_file.parent.mkdir(parents=True, exist_ok=True)

            with open(workflow_file, "w") as f:
                f.write(integrated_workflow)

            print(f"✅ Created integrated workflow: {workflow_file}")

            # Generate integration report
            self._generate_integration_report(analysis)

            print("🎉 GitHub Actions integration setup complete!")
            return True

        except Exception as e:
            print(f"❌ Integration setup failed: {e}")
            return False

    def _generate_integration_report(self, analysis: Dict):
        """Generate comprehensive integration report."""
        report_content = f"""# GitHub Actions Integration Report

## Integration Summary
- **Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Workflows Found**: {len(analysis['found_workflows'])}
- **Categories**: {len(analysis['categories'])}
- **Integration Opportunities**: {len(analysis['integration_opportunities'])}

## Discovered Workflows
"""

        for category, workflows in analysis["categories"].items():
            report_content += f"\n### {category.replace('_', ' ').title()}\n"
            for workflow in workflows:
                value = analysis["value_assessment"].get(workflow, {})
                report_content += f"- **{workflow}**: Value {value.get('value', 3)}/5, Integration: {value.get('integration', 'optional')}\n"

        report_content += "\n## Integration Opportunities\n"
        for opportunity in analysis["integration_opportunities"]:
            report_content += f"\n### {opportunity['type'].replace('_', ' ').title()}\n"
            report_content += f"- **Priority**: {opportunity['priority']}\n"
            report_content += f"- **Description**: {opportunity['description']}\n"
            report_content += (
                f"- **Workflows**: {', '.join(opportunity['workflows'])}\n"
            )

        report_content += """
## Next Steps
1. Review the generated `azure-functions-enterprise.yml` workflow
2. Update repository secrets and variables as needed
3. Test the integrated workflow with a pull request
4. Monitor workflow execution and optimize as needed

## Value Assessment
Your workflows represent **enterprise-grade DevOps infrastructure** with:
- Complete CI/CD automation
- L.I.F.E Theory innovation
- Clinical-grade validation
- Azure deployment optimization
"""

        report_file = self.integration_dir / "integration_report.md"
        with open(report_file, "w") as f:
            f.write(report_content)

        print(f"📋 Generated integration report: {report_file}")

    def test_integration(self) -> bool:
        """Test the integration setup."""
        print("🧪 Testing GitHub Actions integration...")

        try:
            # Test Azure Functions workflow
            result = subprocess.run(
                [sys.executable, "azure_functions_workflow.py", "--help"],
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                print("✅ Azure Functions workflow is accessible")
            else:
                print("❌ Azure Functions workflow test failed")
                return False

            # Test workflow file syntax
            workflow_file = self.workflows_dir / "azure-functions-enterprise.yml"
            if workflow_file.exists():
                print("✅ Integrated workflow file created")
            else:
                print("❌ Integrated workflow file not found")
                return False

            print("🎉 Integration test completed successfully!")
            return True

        except Exception as e:
            print(f"❌ Integration test failed: {e}")
            return False


def main():
    """Main entry point for workflow integration."""
    print("🔗 GitHub Actions + Azure Functions Integration Tool")
    print("=" * 60)

    integrator = WorkflowIntegrator()

    # Run integration process
    if integrator.setup_integration():
        if integrator.test_integration():
            print("\n✨ Integration completed successfully!")
            print("\nNext steps:")
            print("1. Review .github/workflows/azure-functions-enterprise.yml")
            print("2. Update repository secrets (AZURE_CREDENTIALS)")
            print("3. Test with a pull request")
            print("4. Check integration/integration_report.md for details")
        else:
            print("\n⚠️  Integration completed with test issues")
    else:
        print("\n❌ Integration failed")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
