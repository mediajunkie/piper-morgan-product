#!/usr/bin/env python3
"""
User Journey Testing Script

Tests real user journeys end-to-end to identify polish opportunities and UX friction points.
Focuses on actual user paths through the system.

Usage:
    python scripts/test_user_journeys.py
"""

import asyncio
import json
import os
import sys
import time
from dataclasses import dataclass
from typing import Any, Dict, List

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.conversation.conversation_handler import ConversationHandler
from services.domain.models import Intent, IntentCategory
from services.orchestration.engine import OrchestrationEngine
from services.orchestration.workflow_factory import WorkflowFactory
from services.shared_types import TaskType, WorkflowType


@dataclass
class UserJourneyResult:
    """Result of a user journey test"""

    journey_name: str
    success: bool
    duration_ms: float
    friction_points: List[str]
    polish_opportunities: List[str]
    response_time_ms: float
    error_message: str = None
    workflow_id: str = None


class UserJourneyTester:
    """Test real user journeys end-to-end"""

    def __init__(self):
        self.engine = OrchestrationEngine()
        self.factory = WorkflowFactory()
        # #1759: ConversationHandler's session_manager parameter was deleted
        # with the dead clarify-carrier machinery.
        self.conversation_handler = ConversationHandler()
        self.results = []

    async def test_journey_create_github_issue(self) -> UserJourneyResult:
        """Test: 'Create a GitHub issue for login bug'"""
        print("🧪 Testing: Create GitHub Issue Journey")
        start_time = time.time()
        friction_points = []
        polish_opportunities = []

        try:
            # Step 1: User sends message
            user_message = "Create a GitHub issue for login bug"
            print(f"   📝 User: {user_message}")

            # Step 2: Intent classification
            intent_start = time.time()
            intent = Intent(
                category=IntentCategory.EXECUTION,
                action="create_github_issue",
                confidence=1.0,
                context={"original_message": user_message},
            )
            intent_time = (time.time() - intent_start) * 1000
            print(f"   ⚡ Intent classification: {intent_time:.1f}ms")

            if intent_time > 1000:
                friction_points.append(f"Intent classification slow: {intent_time:.1f}ms")
                polish_opportunities.append("Optimize intent classification for faster response")

            # Step 3: Workflow creation
            workflow_start = time.time()
            workflow = await self.factory.create_from_intent(intent)
            workflow_time = (time.time() - workflow_start) * 1000
            print(f"   ⚡ Workflow creation: {workflow_time:.1f}ms")

            if not workflow:
                return UserJourneyResult(
                    journey_name="Create GitHub Issue",
                    success=False,
                    duration_ms=(time.time() - start_time) * 1000,
                    friction_points=["Workflow creation failed"],
                    polish_opportunities=["Improve workflow factory error handling"],
                    response_time_ms=0,
                    error_message="Failed to create workflow",
                )

            if workflow_time > 500:
                friction_points.append(f"Workflow creation slow: {workflow_time:.1f}ms")
                polish_opportunities.append("Cache workflow templates for faster creation")

            # Step 4: Workflow execution
            execution_start = time.time()
            try:
                # Store workflow in engine registry
                self.engine.workflows[workflow.id] = workflow

                # Execute workflow
                result = await asyncio.wait_for(
                    self.engine.execute_workflow(workflow.id), timeout=30.0
                )
                execution_time = (time.time() - execution_start) * 1000
                print(f"   ⚡ Workflow execution: {execution_time:.1f}ms")

                if execution_time > 10000:
                    friction_points.append(f"Workflow execution very slow: {execution_time:.1f}ms")
                    polish_opportunities.append(
                        "Implement progress indicators for long-running workflows"
                    )

                # Step 5: Response analysis
                if result.get("status") == "completed":
                    print("   ✅ Journey completed successfully")
                    polish_opportunities.append("Add success confirmation with next steps")
                else:
                    friction_points.append(
                        f"Workflow completed with status: {result.get('status')}"
                    )
                    polish_opportunities.append("Improve workflow status reporting")

            except asyncio.TimeoutError:
                friction_points.append("Workflow execution timed out")
                polish_opportunities.append("Implement timeout handling with user feedback")
                return UserJourneyResult(
                    journey_name="Create GitHub Issue",
                    success=False,
                    duration_ms=(time.time() - start_time) * 1000,
                    friction_points=friction_points,
                    polish_opportunities=polish_opportunities,
                    response_time_ms=0,
                    error_message="Workflow execution timed out",
                    workflow_id=workflow.id,
                )

            total_time = (time.time() - start_time) * 1000

            # Analyze response times
            if total_time > 15000:
                friction_points.append(f"Total journey time too long: {total_time:.1f}ms")
                polish_opportunities.append("Implement async processing with immediate feedback")

            return UserJourneyResult(
                journey_name="Create GitHub Issue",
                success=True,
                duration_ms=total_time,
                friction_points=friction_points,
                polish_opportunities=polish_opportunities,
                response_time_ms=total_time,
                workflow_id=workflow.id,
            )

        except Exception as e:
            return UserJourneyResult(
                journey_name="Create GitHub Issue",
                success=False,
                duration_ms=(time.time() - start_time) * 1000,
                friction_points=[f"Unexpected error: {str(e)}"],
                polish_opportunities=["Improve error handling and user feedback"],
                response_time_ms=0,
                error_message=str(e),
            )

    async def test_journey_list_projects(self) -> UserJourneyResult:
        """Test: 'List all my projects'"""
        print("🧪 Testing: List Projects Journey")
        start_time = time.time()
        friction_points = []
        polish_opportunities = []

        try:
            # Step 1: User sends message
            user_message = "List all my projects"
            print(f"   📝 User: {user_message}")

            # Step 2: Intent classification
            intent_start = time.time()
            intent = Intent(
                category=IntentCategory.QUERY,
                action="list_projects",
                confidence=1.0,
                context={"original_message": user_message},
            )
            intent_time = (time.time() - intent_start) * 1000
            print(f"   ⚡ Intent classification: {intent_time:.1f}ms")

            # Step 3: Workflow creation
            workflow_start = time.time()
            workflow = await self.factory.create_from_intent(intent)
            workflow_time = (time.time() - workflow_start) * 1000
            print(f"   ⚡ Workflow creation: {workflow_time:.1f}ms")

            if not workflow:
                return UserJourneyResult(
                    journey_name="List Projects",
                    success=False,
                    duration_ms=(time.time() - start_time) * 1000,
                    friction_points=["Workflow creation failed"],
                    polish_opportunities=["Improve workflow factory error handling"],
                    response_time_ms=0,
                    error_message="Failed to create workflow",
                )

            # Step 4: Execute list projects task directly
            execution_start = time.time()
            try:
                task = workflow.tasks[0]
                handler = self.engine.task_handlers.get(task.type)

                if not handler:
                    friction_points.append(f"No handler for task type: {task.type.value}")
                    polish_opportunities.append(f"Implement handler for {task.type.value}")
                    return UserJourneyResult(
                        journey_name="List Projects",
                        success=False,
                        duration_ms=(time.time() - start_time) * 1000,
                        friction_points=friction_points,
                        polish_opportunities=polish_opportunities,
                        response_time_ms=0,
                        error_message=f"No handler for {task.type.value}",
                    )

                result = await handler(workflow, task)
                execution_time = (time.time() - execution_start) * 1000
                print(f"   ⚡ Task execution: {execution_time:.1f}ms")

                if result.success:
                    print("   ✅ Projects listed successfully")
                    # Check response formatting
                    if result.output_data and "projects" in result.output_data:
                        projects = result.output_data["projects"]
                        if len(projects) == 0:
                            polish_opportunities.append(
                                "Provide helpful message when no projects found"
                            )
                        else:
                            polish_opportunities.append(
                                "Format project list with better visual hierarchy"
                            )
                    else:
                        friction_points.append("No projects data in response")
                        polish_opportunities.append("Improve response data structure")
                else:
                    friction_points.append(f"Task execution failed: {result.error}")
                    polish_opportunities.append("Improve error messages for database queries")

            except Exception as e:
                friction_points.append(f"Task execution error: {str(e)}")
                polish_opportunities.append("Add better error handling for database operations")

            total_time = (time.time() - start_time) * 1000

            return UserJourneyResult(
                journey_name="List Projects",
                success=True,
                duration_ms=total_time,
                friction_points=friction_points,
                polish_opportunities=polish_opportunities,
                response_time_ms=total_time,
                workflow_id=workflow.id,
            )

        except Exception as e:
            return UserJourneyResult(
                journey_name="List Projects",
                success=False,
                duration_ms=(time.time() - start_time) * 1000,
                friction_points=[f"Unexpected error: {str(e)}"],
                polish_opportunities=["Improve error handling and user feedback"],
                response_time_ms=0,
                error_message=str(e),
            )

    async def test_journey_generate_report(self) -> UserJourneyResult:
        """Test: 'Generate a status report'"""
        print("🧪 Testing: Generate Report Journey")
        start_time = time.time()
        friction_points = []
        polish_opportunities = []

        try:
            # Step 1: User sends message
            user_message = "Generate a status report"
            print(f"   📝 User: {user_message}")

            # Step 2: Intent classification
            intent_start = time.time()
            intent = Intent(
                category=IntentCategory.EXECUTION,
                action="generate_report",
                confidence=1.0,
                context={"original_message": user_message},
            )
            intent_time = (time.time() - intent_start) * 1000
            print(f"   ⚡ Intent classification: {intent_time:.1f}ms")

            # Step 3: Workflow creation
            workflow_start = time.time()
            workflow = await self.factory.create_from_intent(intent)
            workflow_time = (time.time() - workflow_start) * 1000
            print(f"   ⚡ Workflow creation: {workflow_time:.1f}ms")

            if not workflow:
                return UserJourneyResult(
                    journey_name="Generate Report",
                    success=False,
                    duration_ms=(time.time() - start_time) * 1000,
                    friction_points=["Workflow creation failed"],
                    polish_opportunities=["Improve workflow factory error handling"],
                    response_time_ms=0,
                    error_message="Failed to create workflow",
                )

            # Step 4: Execute report generation task
            execution_start = time.time()
            try:
                task = workflow.tasks[0]
                handler = self.engine.task_handlers.get(task.type)

                if not handler:
                    friction_points.append(f"No handler for task type: {task.type.value}")
                    polish_opportunities.append(f"Implement handler for {task.type.value}")
                    return UserJourneyResult(
                        journey_name="Generate Report",
                        success=False,
                        duration_ms=(time.time() - start_time) * 1000,
                        friction_points=friction_points,
                        polish_opportunities=polish_opportunities,
                        response_time_ms=0,
                        error_message=f"No handler for {task.type.value}",
                    )

                result = await handler(workflow, task)
                execution_time = (time.time() - execution_start) * 1000
                print(f"   ⚡ Report generation: {execution_time:.1f}ms")

                if result.success:
                    print("   ✅ Report generated successfully")
                    # Check report quality
                    if result.output_data and "content" in result.output_data:
                        content = result.output_data["content"]
                        if len(content) < 100:
                            polish_opportunities.append("Generate more detailed reports")
                        else:
                            polish_opportunities.append(
                                "Add report formatting options (PDF, markdown)"
                            )
                    else:
                        friction_points.append("No report content in response")
                        polish_opportunities.append("Improve report generation response structure")
                else:
                    friction_points.append(f"Report generation failed: {result.error}")
                    polish_opportunities.append(
                        "Provide better error messages for report generation"
                    )

            except Exception as e:
                friction_points.append(f"Report generation error: {str(e)}")
                polish_opportunities.append("Add better error handling for report generation")

            total_time = (time.time() - start_time) * 1000

            return UserJourneyResult(
                journey_name="Generate Report",
                success=True,
                duration_ms=total_time,
                friction_points=friction_points,
                polish_opportunities=polish_opportunities,
                response_time_ms=total_time,
                workflow_id=workflow.id,
            )

        except Exception as e:
            return UserJourneyResult(
                journey_name="Generate Report",
                success=False,
                duration_ms=(time.time() - start_time) * 1000,
                friction_points=[f"Unexpected error: {str(e)}"],
                polish_opportunities=["Improve error handling and user feedback"],
                response_time_ms=0,
                error_message=str(e),
            )

    async def run_all_journeys(self):
        """Run all user journey tests"""
        print("🚀 Starting User Journey Tests")
        print("=" * 60)

        # Test all user journeys
        journeys = [
            self.test_journey_create_github_issue(),
            self.test_journey_list_projects(),
            self.test_journey_generate_report(),
        ]

        for journey in journeys:
            result = await journey
            self.results.append(result)
            print()

        # Print summary
        self.print_summary()

    def print_summary(self):
        """Print comprehensive test summary"""
        print("=" * 60)
        print("📊 USER JOURNEY TEST SUMMARY")
        print("=" * 60)

        total = len(self.results)
        successful = sum(1 for r in self.results if r.success)
        failed = total - successful

        print(f"Total Journeys: {total}")
        print(f"✅ Successful: {successful}")
        print(f"❌ Failed: {failed}")
        print(f"Success Rate: {(successful/total)*100:.1f}%")

        # Performance analysis
        avg_response_time = sum(r.response_time_ms for r in self.results) / total
        print(f"Average Response Time: {avg_response_time:.1f}ms")

        # Collect all friction points and polish opportunities
        all_friction_points = []
        all_polish_opportunities = []

        for result in self.results:
            all_friction_points.extend(result.friction_points)
            all_polish_opportunities.extend(result.polish_opportunities)

        print(f"\n🔍 Friction Points Found: {len(all_friction_points)}")
        for i, point in enumerate(all_friction_points, 1):
            print(f"   {i}. {point}")

        print(f"\n✨ Polish Opportunities Identified: {len(all_polish_opportunities)}")
        for i, opportunity in enumerate(all_polish_opportunities, 1):
            print(f"   {i}. {opportunity}")

        # Priority recommendations
        print(f"\n🎯 PRIORITY RECOMMENDATIONS:")

        # Performance issues
        performance_issues = [r for r in self.results if r.response_time_ms > 5000]
        if performance_issues:
            print("   🚨 CRITICAL: Performance issues detected")
            for issue in performance_issues:
                print(f"      - {issue.journey_name}: {issue.response_time_ms:.1f}ms")

        # Error handling issues
        error_issues = [r for r in self.results if not r.success]
        if error_issues:
            print("   🚨 CRITICAL: Error handling issues detected")
            for issue in error_issues:
                print(f"      - {issue.journey_name}: {issue.error_message}")

        # UX improvements
        if all_polish_opportunities:
            print("   💡 HIGH: UX improvements recommended")
            for opportunity in all_polish_opportunities[:5]:  # Top 5
                print(f"      - {opportunity}")


async def main():
    """Main test runner"""
    tester = UserJourneyTester()
    await tester.run_all_journeys()


if __name__ == "__main__":
    asyncio.run(main())
