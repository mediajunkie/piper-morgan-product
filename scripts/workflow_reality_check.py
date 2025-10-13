#!/usr/bin/env python3
"""
PM-062 Workflow Reality Check Script

Systematically tests every workflow type to identify completion vs. hanging issues.
Tests both factory creation and API execution paths.

Usage:
    python scripts/workflow_reality_check.py
"""

import asyncio
import json
import os

# Import project modules
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Tuple

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.database.repositories import ProjectRepository
from services.domain.models import Intent, IntentCategory

# llm_client import removed - OrchestrationEngine uses ServiceRegistry
from services.orchestration.engine import OrchestrationEngine
from services.orchestration.workflow_factory import WorkflowFactory
from services.project_context.project_context import ProjectContext
from services.shared_types import WorkflowStatus, WorkflowType


class TestResult(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    TIMEOUT = "TIMEOUT"
    ERROR = "ERROR"
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"


@dataclass
class WorkflowTestResult:
    workflow_type: WorkflowType
    test_name: str
    result: TestResult
    duration_ms: float
    error_message: Optional[str] = None
    workflow_id: Optional[str] = None
    context_size: Optional[int] = None
    enrichment_impact: Optional[bool] = None


class WorkflowRealityChecker:
    """Systematic workflow testing and analysis"""

    def __init__(self):
        self.factory = WorkflowFactory()
        self.engine = OrchestrationEngine()
        # Skip ProjectContext for now - focus on core workflow testing
        self.results: List[WorkflowTestResult] = []
        self.timeout_seconds = 30

    async def test_workflow_factory_creation(
        self, workflow_type: WorkflowType, context: Dict
    ) -> WorkflowTestResult:
        """Test workflow creation through factory"""
        start_time = time.time()

        try:
            # Create intent for workflow type
            intent = Intent(
                category=IntentCategory.EXECUTION,
                action=workflow_type.value,
                confidence=1.0,
                context=context,
            )

            # Test factory creation
            workflow = await self.factory.create_from_intent(intent)

            duration_ms = (time.time() - start_time) * 1000

            return WorkflowTestResult(
                workflow_type=workflow_type,
                test_name=f"Factory Creation - {workflow_type.value}",
                result=TestResult.PASS,
                duration_ms=duration_ms,
                workflow_id=workflow.id,
                context_size=len(context),
            )

        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            import traceback

            error_details = f"{str(e)}\n{traceback.format_exc()}"
            return WorkflowTestResult(
                workflow_type=workflow_type,
                test_name=f"Factory Creation - {workflow_type.value}",
                result=TestResult.ERROR,
                duration_ms=duration_ms,
                error_message=error_details,
            )

    async def test_workflow_execution(
        self, workflow_type: WorkflowType, context: Dict
    ) -> WorkflowTestResult:
        """Test workflow execution through orchestration engine"""
        start_time = time.time()

        try:
            # Create intent
            intent = Intent(
                category=IntentCategory.EXECUTION,
                action=workflow_type.value,
                confidence=1.0,
                context=context,
            )

            # Create workflow through engine (which stores it in registry)
            workflow = await self.engine.create_workflow_from_intent(intent)

            if not workflow:
                return WorkflowTestResult(
                    workflow_type=workflow_type,
                    test_name=f"Execution - {workflow_type.value}",
                    result=TestResult.ERROR,
                    duration_ms=(time.time() - start_time) * 1000,
                    error_message="Failed to create workflow through engine",
                )

            # Execute workflow with timeout
            try:
                result = await asyncio.wait_for(
                    self.engine.execute_workflow(workflow.id), timeout=self.timeout_seconds
                )

                duration_ms = (time.time() - start_time) * 1000

                # Check if workflow completed successfully
                if result.get("status") == "completed":
                    return WorkflowTestResult(
                        workflow_type=workflow_type,
                        test_name=f"Execution - {workflow_type.value}",
                        result=TestResult.PASS,
                        duration_ms=duration_ms,
                        workflow_id=workflow.id,
                        context_size=len(context),
                    )
                else:
                    return WorkflowTestResult(
                        workflow_type=workflow_type,
                        test_name=f"Execution - {workflow_type.value}",
                        result=TestResult.FAIL,
                        duration_ms=duration_ms,
                        workflow_id=workflow.id,
                        error_message=f"Workflow status: {result.get('status')}",
                    )

            except asyncio.TimeoutError:
                duration_ms = (time.time() - start_time) * 1000
                return WorkflowTestResult(
                    workflow_type=workflow_type,
                    test_name=f"Execution - {workflow_type.value}",
                    result=TestResult.TIMEOUT,
                    duration_ms=duration_ms,
                    workflow_id=workflow.id,
                    error_message=f"Timeout after {self.timeout_seconds}s",
                )

        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            import traceback

            error_details = f"{str(e)}\n{traceback.format_exc()}"
            return WorkflowTestResult(
                workflow_type=workflow_type,
                test_name=f"Execution - {workflow_type.value}",
                result=TestResult.ERROR,
                duration_ms=duration_ms,
                error_message=error_details,
            )

    async def test_enrichment_impact(self, workflow_type: WorkflowType) -> WorkflowTestResult:
        """Test if context enrichment affects workflow behavior"""
        start_time = time.time()

        try:
            # Test with minimal context
            minimal_context = {"original_message": f"test {workflow_type.value}"}

            # Test with enriched context
            enriched_context = {
                "original_message": f"test {workflow_type.value}",
                "project_id": "test-project",
                "user_id": "test-user",
                "session_id": "test-session",
                "timestamp": datetime.now().isoformat(),
            }

            # Compare execution times
            minimal_result = await self.test_workflow_execution(workflow_type, minimal_context)
            enriched_result = await self.test_workflow_execution(workflow_type, enriched_context)

            duration_ms = (time.time() - start_time) * 1000

            enrichment_impact = (
                abs(minimal_result.duration_ms - enriched_result.duration_ms) > 1000
            )  # 1s threshold

            return WorkflowTestResult(
                workflow_type=workflow_type,
                test_name=f"Enrichment Impact - {workflow_type.value}",
                result=(
                    TestResult.PASS
                    if minimal_result.result == TestResult.PASS
                    and enriched_result.result == TestResult.PASS
                    else TestResult.FAIL
                ),
                duration_ms=duration_ms,
                enrichment_impact=enrichment_impact,
                error_message=f"Minimal: {minimal_result.result.value}, Enriched: {enriched_result.result.value}",
            )

        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            return WorkflowTestResult(
                workflow_type=workflow_type,
                test_name=f"Enrichment Impact - {workflow_type.value}",
                result=TestResult.ERROR,
                duration_ms=duration_ms,
                error_message=str(e),
            )

    def get_test_contexts(self) -> Dict[WorkflowType, Dict]:
        """Get appropriate test contexts for each workflow type"""
        return {
            WorkflowType.CREATE_TICKET: {
                "original_message": "create a ticket for bug fix",
                "project_id": "test-project",
            },
            WorkflowType.LIST_PROJECTS: {"original_message": "list all projects"},
            WorkflowType.ANALYZE_FILE: {
                "original_message": "analyze the uploaded file",
                "file_id": "test-file-123",
            },
            WorkflowType.GENERATE_REPORT: {"original_message": "generate a performance report"},
            WorkflowType.REVIEW_ITEM: {
                "original_message": "review this GitHub issue",
                "github_url": "https://github.com/test/repo/issues/1",
            },
            WorkflowType.PLAN_STRATEGY: {"original_message": "plan strategy for Q4"},
            WorkflowType.CREATE_FEATURE: {"original_message": "create a new feature"},
            WorkflowType.ANALYZE_METRICS: {"original_message": "analyze performance metrics"},
            WorkflowType.CREATE_TASK: {"original_message": "create a new task"},
            WorkflowType.LEARN_PATTERN: {"original_message": "learn from this pattern"},
            WorkflowType.ANALYZE_FEEDBACK: {"original_message": "analyze user feedback"},
            WorkflowType.CONFIRM_PROJECT: {"original_message": "confirm project selection"},
            WorkflowType.SELECT_PROJECT: {"original_message": "select a project"},
        }

    async def run_comprehensive_tests(self) -> List[WorkflowTestResult]:
        """Run all workflow tests systematically"""
        print("🚀 Starting PM-062 Workflow Reality Check...")
        print(f"Testing {len(WorkflowType)} workflow types")
        print("=" * 60)

        test_contexts = self.get_test_contexts()

        for workflow_type in WorkflowType:
            print(f"\n📋 Testing {workflow_type.value}...")

            context = test_contexts.get(
                workflow_type, {"original_message": f"test {workflow_type.value}"}
            )

            # Test 1: Factory Creation
            factory_result = await self.test_workflow_factory_creation(workflow_type, context)
            self.results.append(factory_result)
            print(f"  Factory: {factory_result.result.value} ({factory_result.duration_ms:.1f}ms)")

            # Test 2: Workflow Execution
            execution_result = await self.test_workflow_execution(workflow_type, context)
            self.results.append(execution_result)
            print(
                f"  Execution: {execution_result.result.value} ({execution_result.duration_ms:.1f}ms)"
            )

            # Test 3: Enrichment Impact
            enrichment_result = await self.test_enrichment_impact(workflow_type)
            self.results.append(enrichment_result)
            print(
                f"  Enrichment: {enrichment_result.result.value} ({enrichment_result.duration_ms:.1f}ms)"
            )

            if execution_result.result == TestResult.TIMEOUT:
                print(f"  ⚠️  TIMEOUT detected for {workflow_type.value}")
            elif execution_result.result == TestResult.ERROR:
                print(
                    f"  ❌ ERROR detected for {workflow_type.value}: {execution_result.error_message}"
                )

        return self.results

    def generate_report(self) -> Dict:
        """Generate comprehensive test report"""
        total_tests = len(self.results)
        pass_count = sum(1 for r in self.results if r.result == TestResult.PASS)
        fail_count = sum(1 for r in self.results if r.result == TestResult.FAIL)
        timeout_count = sum(1 for r in self.results if r.result == TestResult.TIMEOUT)
        error_count = sum(1 for r in self.results if r.result == TestResult.ERROR)

        # Group by workflow type
        workflow_results = {}
        for result in self.results:
            if result.workflow_type not in workflow_results:
                workflow_results[result.workflow_type] = []
            workflow_results[result.workflow_type].append(result)

        # Identify problematic workflows
        problematic_workflows = []
        for workflow_type, results in workflow_results.items():
            execution_results = [r for r in results if "Execution" in r.test_name]
            if any(
                r.result in [TestResult.FAIL, TestResult.TIMEOUT, TestResult.ERROR]
                for r in execution_results
            ):
                problematic_workflows.append(
                    {
                        "workflow_type": workflow_type.value,
                        "issues": [
                            r.result.value for r in execution_results if r.result != TestResult.PASS
                        ],
                        "errors": [r.error_message for r in execution_results if r.error_message],
                    }
                )

        # Performance analysis
        execution_times = [
            r.duration_ms
            for r in self.results
            if "Execution" in r.test_name and r.result == TestResult.PASS
        ]
        avg_execution_time = sum(execution_times) / len(execution_times) if execution_times else 0

        return {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tests": total_tests,
                "pass_count": pass_count,
                "fail_count": fail_count,
                "timeout_count": timeout_count,
                "error_count": error_count,
                "success_rate": (pass_count / total_tests * 100) if total_tests > 0 else 0,
                "avg_execution_time_ms": avg_execution_time,
            },
            "problematic_workflows": problematic_workflows,
            "detailed_results": [
                {
                    "workflow_type": r.workflow_type.value,
                    "test_name": r.test_name,
                    "result": r.result.value,
                    "duration_ms": r.duration_ms,
                    "error_message": r.error_message,
                    "workflow_id": r.workflow_id,
                }
                for r in self.results
            ],
            "recommendations": self._generate_recommendations(
                problematic_workflows, avg_execution_time
            ),
        }

    def _generate_recommendations(
        self, problematic_workflows: List, avg_execution_time: float
    ) -> List[str]:
        """Generate actionable recommendations based on test results"""
        recommendations = []

        if problematic_workflows:
            recommendations.append("🔧 CRITICAL: Fix hanging/timeout workflows immediately")
            for workflow in problematic_workflows:
                recommendations.append(
                    f"  - {workflow['workflow_type']}: {', '.join(workflow['issues'])}"
                )

        if avg_execution_time > 10000:  # 10 seconds
            recommendations.append("⚡ PERFORMANCE: Optimize workflow execution times")

        timeout_workflows = [w for w in problematic_workflows if "TIMEOUT" in w["issues"]]
        if timeout_workflows:
            recommendations.append("⏱️ TIMEOUT: Implement proper async completion handling")

        error_workflows = [w for w in problematic_workflows if "ERROR" in w["issues"]]
        if error_workflows:
            recommendations.append("🐛 ERROR HANDLING: Fix error swallowing in workflow execution")

        return recommendations

    def print_report(self, report: Dict):
        """Print formatted test report"""
        print("\n" + "=" * 60)
        print("📊 PM-062 WORKFLOW REALITY CHECK REPORT")
        print("=" * 60)

        summary = report["summary"]
        print(f"\n📈 SUMMARY:")
        print(f"  Total Tests: {summary['total_tests']}")
        print(f"  Pass: {summary['pass_count']} ✅")
        print(f"  Fail: {summary['fail_count']} ❌")
        print(f"  Timeout: {summary['timeout_count']} ⏱️")
        print(f"  Error: {summary['error_count']} 🐛")
        print(f"  Success Rate: {summary['success_rate']:.1f}%")
        print(f"  Avg Execution Time: {summary['avg_execution_time_ms']:.1f}ms")

        if report["problematic_workflows"]:
            print(f"\n🚨 PROBLEMATIC WORKFLOWS:")
            for workflow in report["problematic_workflows"]:
                print(f"  {workflow['workflow_type']}: {', '.join(workflow['issues'])}")
                for error in workflow["errors"]:
                    print(f"    Error: {error}")

        if report["recommendations"]:
            print(f"\n💡 RECOMMENDATIONS:")
            for rec in report["recommendations"]:
                print(f"  {rec}")

        print(f"\n📄 Detailed results saved to: workflow_reality_check_report.json")


async def main():
    """Main execution function"""
    checker = WorkflowRealityChecker()

    try:
        # Run comprehensive tests
        results = await checker.run_comprehensive_tests()

        # Generate and print report
        report = checker.generate_report()
        checker.print_report(report)

        # Save detailed report
        with open("workflow_reality_check_report.json", "w") as f:
            json.dump(report, f, indent=2, default=str)

        # Exit with error code if critical issues found
        if report["summary"]["timeout_count"] > 0 or report["summary"]["error_count"] > 0:
            print("\n❌ CRITICAL ISSUES DETECTED - Workflow system needs immediate attention!")
            return 1
        else:
            print("\n✅ All workflows passing - System is healthy!")
            return 0

    except Exception as e:
        print(f"\n💥 CRITICAL ERROR: {e}")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
