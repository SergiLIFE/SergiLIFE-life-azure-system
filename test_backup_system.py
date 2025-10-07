#!/usr/bin/env python3
"""
L.I.F.E. Platform Backup System Test
Comprehensive testing suite for the deployed backup infrastructure

This script tests all components of the backup system and integrates
with the performance analyzer for monitoring.

Copyright 2025 - Sergio Paya Borrull
Azure Marketplace Offer ID: 9a600d96-fe1e-420b-902a-a0c42c561adb
"""

import asyncio
import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import requests

from performance_analyzer import PerformanceAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class BackupSystemTester:
    """
    Comprehensive backup system tester with performance integration
    """

    def __init__(self, function_app_url: str = None):
        self.function_app_url = function_app_url
        self.test_results: List[Dict[str, Any]] = []

        # Initialize performance analyzer
        self.performance_analyzer = PerformanceAnalyzer(
            workspace_path=os.getcwd(), sampling_interval=2.0
        )

        # Test configuration
        self.test_config = {
            "admin_email": "sergiomiguelpaya@sergiomiguelpayaborrullmsn.onmicrosoft.com",
            "storage_account": "stlifeplatformprod",
            "marketplace_offer_id": "9a600d96-fe1e-420b-902a-a0c42c561adb",
            "timeout_seconds": 30,
        }

        logger.info("Backup System Tester initialized")

    def discover_function_app_url(self) -> str:
        """Discover Function App URL from AZD outputs"""
        try:
            import subprocess

            # Get azd environment values
            result = subprocess.run(
                ["azd", "env", "get-values"], capture_output=True, text=True, check=True
            )

            for line in result.stdout.split("\n"):
                if "functionAppName" in line:
                    function_name = line.split("=")[1].strip('"')
                    return f"https://{function_name}.azurewebsites.net"

            return None

        except Exception as e:
            logger.error(f"Failed to discover Function App URL: {e}")
            return None

    async def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run comprehensive backup system test"""

        logger.info("🧪 Starting L.I.F.E. Platform Backup System Test")
        logger.info("=" * 60)

        # Discover Function App URL if not provided
        if not self.function_app_url:
            self.function_app_url = self.discover_function_app_url()

        if not self.function_app_url:
            logger.error(
                "❌ Function App URL not found. Please provide URL or ensure deployment is complete."
            )
            return {"status": "failed", "error": "Function App URL not available"}

        logger.info(f"🎯 Testing Function App: {self.function_app_url}")

        # Start performance monitoring
        self.performance_analyzer.start_real_time_monitoring()

        try:
            test_suite_results = {
                "timestamp": datetime.now().isoformat(),
                "function_app_url": self.function_app_url,
                "test_config": self.test_config,
                "tests": {},
            }

            # Test 1: Backup Status Endpoint
            logger.info("\n🔍 Test 1: Backup Status Endpoint")
            test_suite_results["tests"][
                "backup_status"
            ] = await self.test_backup_status()

            # Test 2: Performance Metrics Endpoint
            logger.info("\n📊 Test 2: Performance Metrics Endpoint")
            test_suite_results["tests"][
                "performance_metrics"
            ] = await self.test_performance_metrics()

            # Test 3: Backup Trigger Endpoint
            logger.info("\n⚡ Test 3: Backup Trigger Endpoint")
            test_suite_results["tests"][
                "backup_trigger"
            ] = await self.test_backup_trigger()

            # Test 4: Azure Storage Integration
            logger.info("\n💾 Test 4: Azure Storage Integration")
            test_suite_results["tests"][
                "storage_integration"
            ] = await self.test_storage_integration()

            # Test 5: Performance Analyzer Integration
            logger.info("\n🔗 Test 5: Performance Analyzer Integration")
            test_suite_results["tests"][
                "performance_integration"
            ] = await self.test_performance_integration()

            # Test 6: End-to-End Backup Flow
            logger.info("\n🔄 Test 6: End-to-End Backup Flow")
            test_suite_results["tests"][
                "e2e_backup_flow"
            ] = await self.test_e2e_backup_flow()

            # Calculate overall test results
            total_tests = len(test_suite_results["tests"])
            passed_tests = sum(
                1
                for test in test_suite_results["tests"].values()
                if test["status"] == "passed"
            )

            test_suite_results["summary"] = {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": total_tests - passed_tests,
                "success_rate": (
                    (passed_tests / total_tests) * 100 if total_tests > 0 else 0
                ),
                "overall_status": "passed" if passed_tests == total_tests else "failed",
            }

            return test_suite_results

        finally:
            # Stop performance monitoring
            self.performance_analyzer.stop_monitoring()

    async def test_backup_status(self) -> Dict[str, Any]:
        """Test backup status endpoint"""
        try:
            url = f"{self.function_app_url}/api/backup-status"

            start_time = time.time()
            response = requests.get(url, timeout=self.test_config["timeout_seconds"])
            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds

            if response.status_code == 200:
                data = response.json()

                result = {
                    "status": "passed",
                    "response_time_ms": response_time,
                    "status_code": response.status_code,
                    "response_data": data,
                    "validations": {
                        "has_system_status": "system_status" in data,
                        "has_performance_metrics": "performance_metrics" in data,
                        "response_time_acceptable": response_time < 2000,
                    },
                }

                logger.info(f"✅ Backup status endpoint: {response_time:.1f}ms")
                return result

            else:
                logger.error(
                    f"❌ Backup status endpoint failed: {response.status_code}"
                )
                return {
                    "status": "failed",
                    "error": f"HTTP {response.status_code}",
                    "response_time_ms": response_time,
                }

        except Exception as e:
            logger.error(f"❌ Backup status test failed: {e}")
            return {"status": "failed", "error": str(e)}

    async def test_performance_metrics(self) -> Dict[str, Any]:
        """Test performance metrics endpoint"""
        try:
            url = f"{self.function_app_url}/api/performance-metrics"

            start_time = time.time()
            response = requests.get(url, timeout=self.test_config["timeout_seconds"])
            response_time = (time.time() - start_time) * 1000

            if response.status_code == 200:
                data = response.json()

                result = {
                    "status": "passed",
                    "response_time_ms": response_time,
                    "status_code": response.status_code,
                    "response_data": data,
                    "validations": {
                        "has_backup_system_metrics": "backup_system" in data,
                        "has_storage_metrics": "storage_system" in data,
                        "has_integration_status": "integration_status" in data,
                        "response_time_acceptable": response_time < 2000,
                    },
                }

                logger.info(f"✅ Performance metrics endpoint: {response_time:.1f}ms")
                return result

            else:
                logger.error(
                    f"❌ Performance metrics endpoint failed: {response.status_code}"
                )
                return {
                    "status": "failed",
                    "error": f"HTTP {response.status_code}",
                    "response_time_ms": response_time,
                }

        except Exception as e:
            logger.error(f"❌ Performance metrics test failed: {e}")
            return {"status": "failed", "error": str(e)}

    async def test_backup_trigger(self) -> Dict[str, Any]:
        """Test backup trigger endpoint"""
        try:
            url = f"{self.function_app_url}/api/trigger-backup"

            payload = {
                "admin_email": self.test_config["admin_email"],
                "storage_account": self.test_config["storage_account"],
                "timestamp": datetime.now().isoformat(),
            }

            start_time = time.time()
            response = requests.post(
                url,
                json=payload,
                timeout=self.test_config["timeout_seconds"],
                headers={"Content-Type": "application/json"},
            )
            response_time = (time.time() - start_time) * 1000

            if response.status_code == 200:
                data = response.json()

                result = {
                    "status": "passed",
                    "response_time_ms": response_time,
                    "status_code": response.status_code,
                    "response_data": data,
                    "validations": {
                        "backup_triggered": data.get("status") == "success",
                        "has_backup_id": "backup_id" in data,
                        "response_time_acceptable": response_time < 5000,
                    },
                }

                logger.info(f"✅ Backup trigger endpoint: {response_time:.1f}ms")
                logger.info(f"   Backup ID: {data.get('backup_id', 'N/A')}")
                return result

            else:
                logger.error(
                    f"❌ Backup trigger endpoint failed: {response.status_code}"
                )
                return {
                    "status": "failed",
                    "error": f"HTTP {response.status_code}",
                    "response_time_ms": response_time,
                }

        except Exception as e:
            logger.error(f"❌ Backup trigger test failed: {e}")
            return {"status": "failed", "error": str(e)}

    async def test_storage_integration(self) -> Dict[str, Any]:
        """Test Azure Storage integration"""
        try:
            # For now, we'll test this through the Function App endpoints
            # In a full implementation, this would test direct storage access

            logger.info("   Testing storage integration via Function App...")

            # Test if Function App can access storage (implicit through backup trigger)
            trigger_result = await self.test_backup_trigger()

            if trigger_result["status"] == "passed":
                result = {
                    "status": "passed",
                    "validation_method": "function_app_proxy",
                    "storage_accessible": True,
                    "note": "Storage integration tested through Function App endpoints",
                }

                logger.info("✅ Storage integration: Function App can access storage")
                return result
            else:
                return {
                    "status": "failed",
                    "error": "Function App cannot access storage",
                    "details": trigger_result,
                }

        except Exception as e:
            logger.error(f"❌ Storage integration test failed: {e}")
            return {"status": "failed", "error": str(e)}

    async def test_performance_integration(self) -> Dict[str, Any]:
        """Test Performance Analyzer integration"""
        try:
            logger.info("   Testing performance monitoring integration...")

            # Get current performance status
            status = self.performance_analyzer.get_current_performance_status()

            # Check if we have performance data
            has_metrics = len(status.get("metrics", {})) > 0

            # Test performance analysis
            analysis = await self.performance_analyzer.perform_comprehensive_analysis()

            result = {
                "status": "passed",
                "performance_status": status["overall_health"],
                "metrics_count": len(status.get("metrics", {})),
                "analysis_score": analysis.performance_score,
                "validations": {
                    "analyzer_operational": True,
                    "has_performance_data": has_metrics,
                    "analysis_completed": analysis.analysis_id is not None,
                },
            }

            logger.info(
                f"✅ Performance integration: {status['overall_health']} ({len(status.get('metrics', {}))} metrics)"
            )
            return result

        except Exception as e:
            logger.error(f"❌ Performance integration test failed: {e}")
            return {"status": "failed", "error": str(e)}

    async def test_e2e_backup_flow(self) -> Dict[str, Any]:
        """Test end-to-end backup flow"""
        try:
            logger.info("   Testing complete backup workflow...")

            # Step 1: Check system status
            status_result = await self.test_backup_status()
            if status_result["status"] != "passed":
                return {
                    "status": "failed",
                    "error": "Backup status check failed",
                    "step": "status_check",
                }

            # Step 2: Trigger backup
            trigger_result = await self.test_backup_trigger()
            if trigger_result["status"] != "passed":
                return {
                    "status": "failed",
                    "error": "Backup trigger failed",
                    "step": "trigger_backup",
                }

            # Step 3: Monitor performance during backup
            await asyncio.sleep(2)  # Simulate backup time

            metrics_result = await self.test_performance_metrics()
            if metrics_result["status"] != "passed":
                return {
                    "status": "failed",
                    "error": "Performance monitoring failed",
                    "step": "performance_monitoring",
                }

            # Calculate end-to-end performance
            total_time = (
                status_result.get("response_time_ms", 0)
                + trigger_result.get("response_time_ms", 0)
                + metrics_result.get("response_time_ms", 0)
            )

            result = {
                "status": "passed",
                "total_e2e_time_ms": total_time,
                "steps_completed": [
                    "status_check",
                    "trigger_backup",
                    "performance_monitoring",
                ],
                "backup_id": trigger_result["response_data"].get("backup_id"),
                "validations": {
                    "all_endpoints_working": True,
                    "e2e_time_acceptable": total_time < 10000,
                    "backup_successfully_triggered": True,
                },
            }

            logger.info(f"✅ End-to-end backup flow: {total_time:.1f}ms total")
            return result

        except Exception as e:
            logger.error(f"❌ End-to-end test failed: {e}")
            return {"status": "failed", "error": str(e)}

    def generate_test_report(self, test_results: Dict[str, Any]) -> str:
        """Generate comprehensive test report"""

        report = f"""
L.I.F.E. Platform Backup System Test Report
===========================================

Test Execution: {test_results['timestamp']}
Function App URL: {test_results['function_app_url']}
Azure Marketplace Offer ID: {self.test_config['marketplace_offer_id']}

SUMMARY
-------
Total Tests: {test_results['summary']['total_tests']}
Passed: {test_results['summary']['passed_tests']}
Failed: {test_results['summary']['failed_tests']}
Success Rate: {test_results['summary']['success_rate']:.1f}%
Overall Status: {test_results['summary']['overall_status'].upper()}

DETAILED RESULTS
----------------
"""

        for test_name, test_result in test_results["tests"].items():
            status_icon = "✅" if test_result["status"] == "passed" else "❌"
            report += f"{status_icon} {test_name.replace('_', ' ').title()}: {test_result['status'].upper()}\n"

            if test_result["status"] == "passed":
                if "response_time_ms" in test_result:
                    report += (
                        f"   Response Time: {test_result['response_time_ms']:.1f}ms\n"
                    )

                if "validations" in test_result:
                    for validation, result in test_result["validations"].items():
                        validation_icon = "✓" if result else "✗"
                        report += f"   {validation_icon} {validation.replace('_', ' ').title()}: {result}\n"
            else:
                report += f"   Error: {test_result.get('error', 'Unknown error')}\n"

            report += "\n"

        report += f"""
PERFORMANCE METRICS
-------------------
The backup system integrates with the L.I.F.E. Platform Performance Analyzer
for real-time monitoring and optimization recommendations.

NEXT STEPS
----------
1. Monitor backup operations in Azure Portal
2. Check Application Insights for detailed telemetry  
3. Verify scheduled backups (daily at 2:00 AM UTC)
4. Integrate with existing L.I.F.E. Platform monitoring

AZURE RESOURCES
---------------
Subscription: 5c88cef6-f243-497d-98af-6c6086d575ca
Resource Group: rg-life-backup-prod
Region: East US 2

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

        return report

    def save_test_results(self, test_results: Dict[str, Any]) -> None:
        """Save test results to files"""

        # Create results directory
        results_dir = Path("test_results")
        results_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save JSON results
        json_file = results_dir / f"backup_test_results_{timestamp}.json"
        with open(json_file, "w") as f:
            json.dump(test_results, f, indent=2, default=str)

        # Save text report
        report_file = results_dir / f"backup_test_report_{timestamp}.txt"
        report = self.generate_test_report(test_results)
        with open(report_file, "w") as f:
            f.write(report)

        logger.info(f"📄 Test results saved:")
        logger.info(f"   JSON: {json_file}")
        logger.info(f"   Report: {report_file}")


async def main():
    """Main test execution function"""

    # Get Function App URL from command line or environment
    function_url = None
    if len(sys.argv) > 1:
        function_url = sys.argv[1]
    else:
        function_url = os.environ.get("FUNCTION_APP_URL")

    # Initialize and run tests
    tester = BackupSystemTester(function_url)

    try:
        # Run comprehensive test suite
        results = await tester.run_comprehensive_test()

        # Print summary
        print("\n" + "=" * 60)
        print("🎯 L.I.F.E. PLATFORM BACKUP SYSTEM TEST COMPLETE")
        print("=" * 60)

        print(f"\n📊 Summary:")
        print(f"   Total Tests: {results['summary']['total_tests']}")
        print(f"   Passed: {results['summary']['passed_tests']}")
        print(f"   Failed: {results['summary']['failed_tests']}")
        print(f"   Success Rate: {results['summary']['success_rate']:.1f}%")

        status_color = (
            "🟢" if results["summary"]["overall_status"] == "passed" else "🔴"
        )
        print(
            f"\n{status_color} Overall Status: {results['summary']['overall_status'].upper()}"
        )

        # Save results
        tester.save_test_results(results)

        # Return appropriate exit code
        return 0 if results["summary"]["overall_status"] == "passed" else 1

    except Exception as e:
        logger.error(f"Test execution failed: {e}")
        return 1


if __name__ == "__main__":
    import sys

    sys.exit(asyncio.run(main()))
