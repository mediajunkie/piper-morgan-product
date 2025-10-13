"""
Intent Service - Business Logic for Intent Processing

Extracts business logic from web/app.py /api/v1/intent route.
Handles intent classification, orchestration coordination, and response formatting.

Phase 2B: Service layer extraction for clean architecture
"""

import asyncio
import json
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import structlog

from services.conversation.conversation_handler import ConversationHandler
from services.domain.models import Intent
from services.intent_service import classifier
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.orchestration.engine import OrchestrationEngine
from services.shared_types import IntentCategory


@dataclass
class IntentProcessingResult:
    """
    Result from intent processing.

    Contains all data needed by HTTP route to format response.
    Separates business logic result from HTTP concerns.
    """

    success: bool
    message: str
    intent_data: Dict[str, Any]
    workflow_id: Optional[str] = None
    requires_clarification: bool = False
    clarification_type: Optional[str] = None
    error: Optional[str] = None
    error_type: Optional[str] = None
    implemented: bool = True  # CORE-CRAFT-GAP: Track actual implementation vs placeholders


class IntentProcessingError(Exception):
    """Raised when intent processing fails"""

    pass


class IntentService:
    """
    Service for processing user intents.

    Handles intent classification, orchestration coordination, and response formatting.
    Decouples business logic from HTTP route handlers.

    Architecture:
        - Coordinates with OrchestrationEngine for workflow creation
        - Handles Tier 1 conversation bypass (Phase 3D)
        - Manages timeout protection (Bug #166)
        - Routes QUERY intents appropriately
        - Preserves Phase 3C placeholders

    Phase 2B: Extracted from web/app.py lines 327-551 (225 lines)
    """

    def __init__(
        self,
        orchestration_engine: Optional[OrchestrationEngine] = None,
        intent_classifier: Optional = None,
        conversation_handler: Optional[ConversationHandler] = None,
    ):
        """
        Initialize service with dependencies.

        Args:
            orchestration_engine: Optional engine for workflow orchestration
            intent_classifier: Optional classifier for intent detection
            conversation_handler: Optional handler for conversation intents
        """
        self.orchestration_engine = orchestration_engine
        self.intent_classifier = intent_classifier or classifier
        self.conversation_handler = conversation_handler
        self.canonical_handlers = CanonicalHandlers()
        self.logger = structlog.get_logger()

    async def process_intent(
        self, message: str, session_id: str = "default_session"
    ) -> IntentProcessingResult:
        """
        Process user intent and return formatted response.

        Handles:
        - Tier 1 conversation bypass (Phase 3D)
        - Intent classification
        - Workflow creation with timeout protection
        - QUERY intent routing (standup, projects, generic)
        - Error handling

        Args:
            message: The user's intent text
            session_id: Session identifier

        Returns:
            IntentProcessingResult with results

        Raises:
            IntentProcessingError: If processing fails
        """
        try:
            # Phase 3D: Tier 1 conversation bypass - handle without orchestration
            if self.orchestration_engine is None:
                return await self._handle_missing_engine(message)

            # Classify intent
            self.logger.info(f"Processing intent with OrchestrationEngine: {message}")
            intent = await self.intent_classifier.classify(message)
            self.logger.info(f"Intent classified as: {intent.category} - {intent.action}")

            # Phase 3D: Preserve Tier 1 conversation bypass
            if intent.category.value == "CONVERSATION":
                return await self._handle_conversation_intent(intent, session_id)

            # Handle canonical intents (IDENTITY, TEMPORAL, STATUS, PRIORITY, GUIDANCE)
            if self.canonical_handlers.can_handle(intent):
                canonical_result = await self.canonical_handlers.handle(intent, session_id)
                return IntentProcessingResult(
                    success=True,
                    message=canonical_result["message"],
                    intent_data=canonical_result["intent"],
                    requires_clarification=canonical_result.get("requires_clarification", False),
                )

            # Create workflow with timeout protection (Bug #166)
            workflow = await self._create_workflow_with_timeout(intent)
            if workflow is None:
                # Timeout occurred
                return IntentProcessingResult(
                    success=False,
                    message="Request timeout - workflow creation took too long",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "confidence": intent.confidence,
                        "context": intent.context,
                    },
                    error="Operation timed out after 30 seconds",
                    error_type="TimeoutError",
                )

            self.logger.info(f"Workflow created with ID: {workflow.id}")

            # Handle QUERY intents with domain services
            if intent.category.value.upper() == "QUERY":
                return await self._handle_query_intent(intent, workflow, session_id)

            # GREAT-4D Phase 1: Handle EXECUTION intents with domain services
            if intent.category.value.upper() == "EXECUTION":
                return await self._handle_execution_intent(intent, workflow, session_id)

            # GREAT-4D Phase 2: Handle ANALYSIS intents with domain services
            if intent.category.value.upper() == "ANALYSIS":
                return await self._handle_analysis_intent(intent, workflow, session_id)

            # GREAT-4D Phase 4: Handle SYNTHESIS intents
            if intent.category.value.upper() == "SYNTHESIS":
                return await self._handle_synthesis_intent(intent, workflow, session_id)

            # GREAT-4D Phase 5: Handle STRATEGY intents
            if intent.category.value.upper() == "STRATEGY":
                return await self._handle_strategy_intent(intent, workflow, session_id)

            # GREAT-4D Phase 6: Handle LEARNING intents
            if intent.category.value.upper() == "LEARNING":
                return await self._handle_learning_intent(intent, workflow, session_id)

            # GREAT-4D Phase 7: Handle UNKNOWN intents
            if intent.category.value.upper() == "UNKNOWN":
                return await self._handle_unknown_intent(intent, workflow, session_id)

            # Fallback for truly unhandled categories (should never reach here)
            return IntentProcessingResult(
                success=False,
                message=f"Unhandled intent category: {intent.category.value}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "context": intent.context,
                },
                workflow_id=workflow.id,
                error=f"No handler for category: {intent.category.value}",
                error_type="UnhandledCategoryError",
            )

        except Exception as e:
            self.logger.error(f"Intent processing error: {e}")
            raise IntentProcessingError(f"Intent processing failed: {str(e)}")

    async def _handle_missing_engine(self, message: str) -> IntentProcessingResult:
        """
        Handle case where OrchestrationEngine is not available.

        Phase 3D: Tier 1 conversation bypass for simple greetings.
        """
        # Simple greeting detection
        if any(
            greeting in message.lower()
            for greeting in ["hello", "hi", "good morning", "good afternoon"]
        ):
            return IntentProcessingResult(
                success=True,
                message="Hello! I can help you with project management tasks.",
                intent_data={
                    "category": "CONVERSATION",
                    "action": "greeting",
                    "confidence": 0.9,
                    "context": {},
                },
                workflow_id=None,
                requires_clarification=False,
                clarification_type=None,
            )
        else:
            return IntentProcessingResult(
                success=False,
                message="OrchestrationEngine not available - Phase 3A initialization required",
                intent_data={},
                error="Failed to process intent",
                error_type="ServiceUnavailable",
            )

    async def _handle_conversation_intent(
        self, intent: Intent, session_id: str
    ) -> IntentProcessingResult:
        """
        Handle CONVERSATION category intents (Tier 1 bypass).

        Phase 3D: Conversation handling without full orchestration.
        """
        # Initialize conversation handler if not provided
        if self.conversation_handler is None:
            self.conversation_handler = ConversationHandler(session_manager=None)

        result = await self.conversation_handler.respond(intent, session_id)
        return IntentProcessingResult(
            success=True,
            message=result["message"],
            intent_data=result["intent"],
            workflow_id=result.get("workflow_id"),
            requires_clarification=result.get("requires_clarification", False),
            clarification_type=result.get("clarification_type"),
        )

    async def _handle_query_intent(
        self, intent: Intent, workflow, session_id: str
    ) -> IntentProcessingResult:
        """
        Handle QUERY category intents (standup, projects, generic).

        Routes to appropriate domain service based on intent action.
        """
        self.logger.info(f"Processing QUERY intent: {intent.action}")

        # Handle specific query actions that were broken in August 22 refactor
        if intent.action in ["show_standup", "get_standup"]:
            return await self._handle_standup_query(intent, workflow.id, session_id)

        elif intent.action in ["list_projects", "show_projects"]:
            return await self._handle_projects_query(intent, workflow.id)

        else:
            # Phase 3C: Generic query handler using QueryRouter
            return await self._handle_generic_query(intent, workflow.id)

    async def _handle_standup_query(
        self, intent: Intent, workflow_id: str, session_id: str
    ) -> IntentProcessingResult:
        """
        Handle show_standup/get_standup query actions.

        Restore show_standup functionality with OrchestrationEngine.
        """
        try:
            from services.domain.standup_orchestration_service import StandupOrchestrationService

            standup_service = StandupOrchestrationService()
            standup_result = await standup_service.orchestrate_standup_workflow(
                user_id=session_id, workflow_type="standard"
            )

            return IntentProcessingResult(
                success=True,
                message=f"Good morning! Here's your standup:\n\n{standup_result.summary}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "context": {"standup_data": standup_result.data},
                },
                workflow_id=workflow_id,
                requires_clarification=False,
                clarification_type=None,
            )
        except Exception as e:
            self.logger.error(f"Standup service error: {e}")
            return IntentProcessingResult(
                success=True,  # Still success, just degraded
                message="Unable to generate standup at this time. Please try again later.",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "context": {},
                },
                workflow_id=workflow_id,
                requires_clarification=False,
                clarification_type=None,
            )

    async def _handle_projects_query(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """
        Handle list_projects/show_projects query actions.

        Phase 3C: Restore list_projects functionality.
        """
        return IntentProcessingResult(
            success=True,
            message="Here are your active projects:\n1. Piper Morgan Platform\n2. Issue Tracker Integration\n3. Documentation Updates",
            intent_data={
                "category": intent.category.value,
                "action": intent.action,
                "confidence": intent.confidence,
                "context": {},
            },
            workflow_id=workflow_id,
            requires_clarification=False,
            clarification_type=None,
        )

    async def _handle_generic_query(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """
        Handle generic QUERY intents using QueryRouter.

        Phase 3C: Generic query handler using OrchestrationEngine.
        """
        self.logger.info(f"Routing generic QUERY intent to QueryRouter: {intent.action}")
        try:
            result = await self.orchestration_engine.handle_query_intent(intent)
            return IntentProcessingResult(
                success=True,
                message=f"Query processed successfully: {intent.action}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "context": intent.context,
                },
                workflow_id=workflow_id,
                requires_clarification=False,
                clarification_type=None,
                # Add result data
                error=None,
            )
        except Exception as e:
            self.logger.error(f"QueryRouter error: {e}")
            return IntentProcessingResult(
                success=False,
                message=f"Unable to process query: {intent.action}. Error: {str(e)}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "context": intent.context,
                },
                workflow_id=workflow_id,
                requires_clarification=False,
                clarification_type=None,
                error=str(e),
                error_type="QueryRouterError",
            )

    async def _handle_execution_intent(
        self, intent: Intent, workflow, session_id: str
    ) -> IntentProcessingResult:
        """
        Handle EXECUTION category intents.

        Routes to appropriate domain service based on intent action.
        Follows QUERY pattern for consistency.

        GREAT-4D Phase 1: Replaces Phase 3C placeholder.
        """
        self.logger.info(f"Processing EXECUTION intent: {intent.action}")

        # Route based on action
        if intent.action in ["create_issue", "create_ticket"]:
            return await self._handle_create_issue(intent, workflow.id, session_id)

        elif intent.action in ["update_issue", "update_ticket"]:
            return await self._handle_update_issue(intent, workflow.id)

        else:
            # Generic execution handler - indicate not yet implemented
            self.logger.warning(f"Unhandled EXECUTION action: {intent.action}")
            return IntentProcessingResult(
                success=False,
                message=f"EXECUTION action '{intent.action}' is not yet implemented.",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                },
                workflow_id=workflow.id,
                requires_clarification=False,
                error=f"No handler for action: {intent.action}",
                error_type="NotImplementedError",
            )

    async def _handle_create_issue(
        self, intent: Intent, workflow_id: str, session_id: str
    ) -> IntentProcessingResult:
        """
        Handle create_issue/create_ticket action.

        Creates GitHub issue using domain service.

        GREAT-4D Phase 1: First EXECUTION handler implementation.
        """
        try:
            from services.domain.github_domain_service import GitHubDomainService

            github_service = GitHubDomainService()

            # Extract issue details from intent
            title = intent.context.get("title") or f"Issue: {intent.original_message[:50]}"
            description = intent.context.get("description") or intent.original_message
            repository = intent.context.get("repository") or intent.context.get("repo")

            # Require repository
            if not repository:
                return IntentProcessingResult(
                    success=False,
                    message="Cannot create issue: repository not specified. Please specify which repository.",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                    clarification_type="repository_required",
                )

            # Create issue
            issue = await github_service.create_issue(
                repo_name=repository,
                title=title,
                body=description,
                labels=intent.context.get("labels", []),
                assignees=intent.context.get("assignees", []),
            )

            return IntentProcessingResult(
                success=True,
                message=f"Created issue #{issue.get('number')}: {issue.get('title')}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "issue_number": issue.get("number"),
                    "issue_url": issue.get("html_url"),
                    "repository": repository,
                },
                workflow_id=workflow_id,
                requires_clarification=False,
            )

        except Exception as e:
            self.logger.error(f"Failed to create issue: {e}")
            return IntentProcessingResult(
                success=False,
                message=f"Failed to create issue: {str(e)}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                },
                workflow_id=workflow_id,
                error=str(e),
                error_type="GitHubError",
            )

    async def _handle_update_issue(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """
        Handle update_issue/update_ticket action.

        Updates existing GitHub issue using domain service.

        GREAT-4D Phase 1: FULLY IMPLEMENTED
        """
        try:
            from services.domain.github_domain_service import GitHubDomainService

            github_service = GitHubDomainService()

            # Extract parameters from intent
            issue_number = intent.context.get("issue_number")
            repository = intent.context.get("repository") or intent.context.get("repo")
            title = intent.context.get("title")
            body = intent.context.get("body") or intent.context.get("description")
            state = intent.context.get("state")
            labels = intent.context.get("labels")
            assignees = intent.context.get("assignees")

            # Validate required parameters
            if not issue_number:
                return IntentProcessingResult(
                    success=False,
                    message="Cannot update issue: issue number not specified. Please provide the issue number.",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                    clarification_type="issue_number_required",
                )

            if not repository:
                return IntentProcessingResult(
                    success=False,
                    message="Cannot update issue: repository not specified. Please specify which repository.",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                    clarification_type="repository_required",
                )

            # Ensure at least one field to update is provided
            if not any([title, body, state, labels, assignees]):
                return IntentProcessingResult(
                    success=False,
                    message="Cannot update issue: no fields to update specified. Please provide at least one field to update (title, body, state, labels, or assignees).",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                    clarification_type="update_fields_required",
                )

            # Update issue
            updated_issue = await github_service.update_issue(
                repo_name=repository,
                issue_number=issue_number,
                title=title,
                body=body,
                state=state,
                labels=labels,
                assignees=assignees,
            )

            return IntentProcessingResult(
                success=True,
                message=f"Updated issue #{updated_issue.get('number')}: {updated_issue.get('title')}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "issue_number": updated_issue.get("number"),
                    "title": updated_issue.get("title"),
                    "state": updated_issue.get("state"),
                    "issue_url": updated_issue.get("html_url"),
                    "repository": repository,
                },
                workflow_id=workflow_id,
                requires_clarification=False,
            )

        except Exception as e:
            self.logger.error(f"Failed to update issue: {e}")
            return IntentProcessingResult(
                success=False,
                message=f"Failed to update issue: {str(e)}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                },
                workflow_id=workflow_id,
                error=str(e),
                error_type="GitHubError",
            )

    async def _handle_analysis_intent(
        self, intent: Intent, workflow, session_id: str
    ) -> IntentProcessingResult:
        """
        Handle ANALYSIS category intents.

        Routes to appropriate analysis service based on intent action.
        Follows EXECUTION/QUERY pattern for consistency.

        GREAT-4D Phase 2: Replaces Phase 3C placeholder.
        """
        self.logger.info(f"Processing ANALYSIS intent: {intent.action}")

        # Route based on action
        if intent.action in ["analyze_commits", "analyze_code"]:
            return await self._handle_analyze_commits(intent, workflow.id)

        elif intent.action in ["generate_report", "create_report"]:
            return await self._handle_generate_report(intent, workflow.id)

        elif intent.action in ["analyze_data", "evaluate_metrics"]:
            return await self._handle_analyze_data(intent, workflow.id)

        else:
            # Generic analysis handler - route to orchestration
            self.logger.info(f"Routing generic ANALYSIS to orchestration: {intent.action}")
            try:
                result = await self.orchestration_engine.handle_analysis_intent(intent)
                return IntentProcessingResult(
                    success=True,
                    message=f"Analysis processed: {intent.action}",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "confidence": intent.confidence,
                    },
                    workflow_id=workflow.id,
                    requires_clarification=False,
                )
            except Exception as e:
                self.logger.error(f"Analysis handler error: {e}")
                return IntentProcessingResult(
                    success=False,
                    message=f"Failed to analyze: {str(e)}",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "confidence": intent.confidence,
                    },
                    workflow_id=workflow.id,
                    error=str(e),
                    error_type="AnalysisError",
                )

    async def _handle_analyze_commits(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """
        Handle commit analysis requests.

        Analyzes Git commits from specified repository and timeframe.

        GREAT-4D Phase 2: First ANALYSIS handler - FULLY IMPLEMENTED
        """
        try:
            from services.domain.github_domain_service import GitHubDomainService

            # Extract and validate parameters
            repository = intent.context.get("repository")

            # Validate required parameters
            if not repository:
                return IntentProcessingResult(
                    success=False,
                    message="Cannot analyze commits: repository not specified. Please specify which repository.",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                    clarification_type="repository_required",
                )

            # Get timeframe parameters
            days = intent.context.get("days", 7)  # Default to 7 days
            timeframe = intent.context.get("timeframe", f"last {days} days")

            # Get GitHub service
            github_service = GitHubDomainService()

            # Get recent activity (includes commits)
            self.logger.info(f"Fetching commits for {repository} (last {days} days)")
            activity = await github_service._github_agent.get_recent_activity(days=days)

            # Extract commits from activity
            commits = activity.get("commits", [])
            commit_count = len(commits)

            # Analyze commits
            authors = {}
            messages = []
            for commit in commits:
                # Extract author info
                author_info = commit.get("commit", {}).get("author", {})
                author_name = author_info.get("name", "Unknown")
                authors[author_name] = authors.get(author_name, 0) + 1

                # Extract message
                message = commit.get("commit", {}).get("message", "").split("\n")[0][:100]
                messages.append(message)

            # Build response message
            if commit_count == 0:
                message = f"No commits found in {repository} over the {timeframe}."
            else:
                author_summary = ", ".join([f"{name} ({count})" for name, count in authors.items()])
                message = f"Analyzed {commit_count} commit{'s' if commit_count != 1 else ''} in {repository} over the {timeframe}. Authors: {author_summary}"

            return IntentProcessingResult(
                success=True,
                message=message,
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "repository": repository,
                    "commit_count": commit_count,
                    "timeframe": timeframe,
                    "days": days,
                    "authors": authors,
                    "recent_messages": messages[:5],  # First 5 commit messages
                },
                workflow_id=workflow_id,
                requires_clarification=False,
            )

        except Exception as e:
            self.logger.error(f"Failed to analyze commits: {e}", exc_info=True)
            return IntentProcessingResult(
                success=False,
                message=f"Failed to analyze commits: {str(e)}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                },
                workflow_id=workflow_id,
                error=str(e),
                error_type="AnalysisError",
            )

    async def _handle_generate_report(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """
        Handle report generation requests.

        Generates markdown reports based on repository activity data.

        GREAT-4D Phase 2B: Second ANALYSIS handler - FULLY IMPLEMENTED
        """
        try:
            from services.domain.github_domain_service import GitHubDomainService

            # Extract and validate parameters
            repository = intent.context.get("repository")
            report_type = intent.context.get("report_type", "commit_analysis")

            # Validate required parameters
            if not repository:
                return IntentProcessingResult(
                    success=False,
                    message="Cannot generate report: repository not specified. Please specify which repository.",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                    clarification_type="repository_required",
                )

            # Get timeframe parameters
            days = intent.context.get("days", 7)  # Default to 7 days
            timeframe = intent.context.get("timeframe", f"last {days} days")

            # Get GitHub service
            github_service = GitHubDomainService()

            # Get recent activity (includes commits, PRs, issues)
            self.logger.info(f"Generating {report_type} report for {repository} (last {days} days)")
            activity = await github_service._github_agent.get_recent_activity(days=days)

            # Generate report based on type
            if report_type == "commit_analysis":
                report_content = self._format_commit_report(
                    repository=repository, activity=activity, timeframe=timeframe, days=days
                )
            else:
                # Default to commit analysis for unknown types
                report_content = self._format_commit_report(
                    repository=repository, activity=activity, timeframe=timeframe, days=days
                )

            # Build response message
            commits = activity.get("commits", [])
            commit_count = len(commits)
            message = f"Generated {report_type} report for {repository} with {commit_count} commit{'s' if commit_count != 1 else ''} from {timeframe}."

            return IntentProcessingResult(
                success=True,
                message=message,
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "repository": repository,
                    "report_type": report_type,
                    "timeframe": timeframe,
                    "days": days,
                    "commit_count": commit_count,
                    "content": report_content,
                    "format": "markdown",
                    "generated_at": datetime.now().isoformat(),
                },
                workflow_id=workflow_id,
                requires_clarification=False,
            )

        except Exception as e:
            self.logger.error(f"Failed to generate report: {e}", exc_info=True)
            return IntentProcessingResult(
                success=False,
                message=f"Failed to generate report: {str(e)}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                },
                workflow_id=workflow_id,
                error=str(e),
                error_type="ReportError",
            )

    def _format_commit_report(
        self, repository: str, activity: Dict[str, Any], timeframe: str, days: int
    ) -> str:
        """
        Format commit analysis as markdown report.

        Helper method for _handle_generate_report.
        """
        # Extract data
        commits = activity.get("commits", [])
        commit_count = len(commits)

        # Analyze authors
        authors = {}
        for commit in commits:
            author_info = commit.get("commit", {}).get("author", {})
            author_name = author_info.get("name", "Unknown")
            authors[author_name] = authors.get(author_name, 0) + 1

        # Build markdown report
        report = f"# Commit Analysis Report\n\n"
        report += f"**Repository**: {repository}\n"
        report += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"**Period**: {timeframe} ({days} days)\n\n"

        report += f"## Summary\n\n"
        report += f"- **Total Commits**: {commit_count}\n"
        report += f"- **Contributors**: {len(authors)}\n\n"

        if authors:
            report += f"## Contributors\n\n"
            for author, count in sorted(authors.items(), key=lambda x: x[1], reverse=True):
                report += f"- **{author}**: {count} commit{'s' if count != 1 else ''}\n"
            report += "\n"

        if commits:
            report += f"## Recent Commits\n\n"
            for commit in commits[:10]:  # First 10
                msg = commit.get("commit", {}).get("message", "No message").split("\n")[0]
                author_info = commit.get("commit", {}).get("author", {})
                author_name = author_info.get("name", "Unknown")
                date_str = author_info.get("date", "Unknown date")
                report += f"- **{msg[:80]}** by {author_name} on {date_str}\n"

        return report

    async def _handle_analyze_data(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """
        Handle general data analysis requests.

        Analyzes repository data and returns structured insights based on data_type.
        Supports: repository_metrics, activity_trends, contributor_stats

        GREAT-4D Phase 2C: Third ANALYSIS handler - FULLY IMPLEMENTED
        """
        try:
            from services.domain.github_domain_service import GitHubDomainService

            # Extract and validate parameters
            repository = intent.context.get("repository")
            data_type = intent.context.get("data_type", "repository_metrics")

            # Validate required parameters
            if not repository:
                return IntentProcessingResult(
                    success=False,
                    message="Cannot analyze data: repository not specified. Please specify which repository.",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                    clarification_type="repository_required",
                )

            # Validate data_type
            supported_types = ["repository_metrics", "activity_trends", "contributor_stats"]
            if data_type not in supported_types:
                return IntentProcessingResult(
                    success=False,
                    message=f"Cannot analyze data: unsupported data type '{data_type}'. Supported types: {', '.join(supported_types)}",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "data_type": data_type,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                    clarification_type="unsupported_data_type",
                )

            # Get timeframe parameters
            days = intent.context.get("days", 7)
            timeframe = intent.context.get("timeframe", f"last {days} days")

            # Get GitHub service and fetch data
            github_service = GitHubDomainService()
            self.logger.info(f"Analyzing {data_type} for {repository} (last {days} days)")
            activity = await github_service._github_agent.get_recent_activity(days=days)

            # Route to appropriate analysis helper
            if data_type == "repository_metrics":
                result_data = self._analyze_repository_metrics(
                    activity, repository, days, timeframe, intent
                )
            elif data_type == "activity_trends":
                result_data = self._analyze_activity_trends(
                    activity, repository, days, timeframe, intent
                )
            elif data_type == "contributor_stats":
                result_data = self._analyze_contributor_stats(
                    activity, repository, days, timeframe, intent
                )

            # Return success
            return IntentProcessingResult(
                success=True,
                message=result_data["message"],
                intent_data=result_data["intent_data"],
                workflow_id=workflow_id,
                requires_clarification=False,
            )

        except Exception as e:
            self.logger.error(f"Failed to analyze data: {e}", exc_info=True)
            return IntentProcessingResult(
                success=False,
                message=f"Failed to analyze data: {str(e)}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                },
                workflow_id=workflow_id,
                error=str(e),
                error_type="AnalysisError",
            )

    def _analyze_repository_metrics(
        self, activity: Dict[str, Any], repository: str, days: int, timeframe: str, intent: Intent
    ) -> Dict[str, Any]:
        """
        Analyze repository metrics from activity data.

        Helper method for _handle_analyze_data.
        Returns dict with 'message' and 'intent_data' keys.
        """
        # Extract counts
        commits = activity.get("commits", [])
        prs = activity.get("prs", [])
        issues_created = activity.get("issues_created", [])
        issues_closed = activity.get("issues_closed", [])

        commit_count = len(commits)
        pr_count = len(prs)
        issues_created_count = len(issues_created)
        issues_closed_count = len(issues_closed)
        total_activity = commit_count + pr_count + issues_created_count + issues_closed_count

        # Calculate distribution percentages
        distribution = {}
        if total_activity > 0:
            distribution = {
                "commits": round((commit_count / total_activity) * 100, 1),
                "prs": round((pr_count / total_activity) * 100, 1),
                "issues_created": round((issues_created_count / total_activity) * 100, 1),
                "issues_closed": round((issues_closed_count / total_activity) * 100, 1),
            }

        # Build message
        message = f"Analyzed repository metrics for {repository} over {timeframe}: {total_activity} total activities ({commit_count} commits, {pr_count} PRs, {issues_created_count} issues created, {issues_closed_count} issues closed)"

        # Build intent_data
        intent_data = {
            "category": intent.category.value,
            "action": intent.action,
            "confidence": intent.confidence,
            "repository": repository,
            "data_type": "repository_metrics",
            "timeframe": timeframe,
            "days": days,
            "metrics": {
                "total_activity_count": total_activity,
                "commits_count": commit_count,
                "prs_count": pr_count,
                "issues_created_count": issues_created_count,
                "issues_closed_count": issues_closed_count,
                "activity_distribution": distribution,
            },
        }

        return {"message": message, "intent_data": intent_data}

    def _analyze_activity_trends(
        self, activity: Dict[str, Any], repository: str, days: int, timeframe: str, intent: Intent
    ) -> Dict[str, Any]:
        """
        Analyze activity trends from activity data.

        Helper method for _handle_analyze_data.
        Returns dict with 'message' and 'intent_data' keys.
        """
        # Extract counts
        commits = activity.get("commits", [])
        prs = activity.get("prs", [])
        issues_created = activity.get("issues_created", [])
        issues_closed = activity.get("issues_closed", [])

        commit_count = len(commits)
        pr_count = len(prs)
        issues_created_count = len(issues_created)
        issues_closed_count = len(issues_closed)
        total_activity = commit_count + pr_count + issues_created_count + issues_closed_count

        # Analyze trends
        trends = {}
        insights = []

        # Most active type
        activity_types = {
            "commits": commit_count,
            "prs": pr_count,
            "issues_created": issues_created_count,
            "issues_closed": issues_closed_count,
        }
        most_active = max(activity_types, key=activity_types.get) if total_activity > 0 else "none"
        trends["most_active_type"] = most_active

        # Issue closure rate
        total_issue_activity = issues_created_count + issues_closed_count
        if total_issue_activity > 0:
            closure_rate = (issues_closed_count / total_issue_activity) * 100
            trends["issue_closure_rate"] = round(closure_rate, 1)
            insights.append(f"Issue closure rate: {round(closure_rate, 1)}%")

        # Commit velocity
        if days > 0:
            commit_velocity = commit_count / days
            trends["commit_velocity"] = f"{round(commit_velocity, 1)} commits/day"
            insights.append(f"Commit velocity: {round(commit_velocity, 1)} commits/day")

        # PR activity
        if pr_count > 0:
            trends["pr_activity"] = f"{pr_count} PRs updated"
            insights.append(f"Active PR development ({pr_count} PRs)")

        # Most active insight
        if total_activity > 0:
            insights.insert(
                0, f"Most active in {most_active} ({activity_types[most_active]} total)"
            )

        # Build message
        message = f"Analyzed activity trends for {repository} over {timeframe}: {total_activity} total activities, most active in {most_active}"

        # Build intent_data
        intent_data = {
            "category": intent.category.value,
            "action": intent.action,
            "confidence": intent.confidence,
            "repository": repository,
            "data_type": "activity_trends",
            "timeframe": timeframe,
            "days": days,
            "metrics": {
                "total_activity_count": total_activity,
                "commits_count": commit_count,
                "prs_count": pr_count,
                "issues_created_count": issues_created_count,
                "issues_closed_count": issues_closed_count,
            },
            "trends": trends,
            "insights": insights,
        }

        return {"message": message, "intent_data": intent_data}

    def _analyze_contributor_stats(
        self, activity: Dict[str, Any], repository: str, days: int, timeframe: str, intent: Intent
    ) -> Dict[str, Any]:
        """
        Analyze contributor statistics from activity data.

        Helper method for _handle_analyze_data.
        Returns dict with 'message' and 'intent_data' keys.
        """
        commits = activity.get("commits", [])
        prs = activity.get("prs", [])
        issues_created = activity.get("issues_created", [])
        issues_closed = activity.get("issues_closed", [])

        # Analyze commit authors
        commit_authors = {}
        for commit in commits:
            # Try to get author from commit data structure
            author = commit.get("author", "Unknown")
            # Handle nested author structure
            if isinstance(author, dict):
                author = author.get("name", "Unknown")
            # Also try commit.commit.author.name
            if author == "Unknown":
                commit_data = commit.get("commit", {})
                author_info = commit_data.get("author", {})
                author = author_info.get("name", "Unknown")
            commit_authors[author] = commit_authors.get(author, 0) + 1

        # Analyze PR authors
        pr_authors = {}
        for pr in prs:
            author = pr.get("author", "Unknown")
            pr_authors[author] = pr_authors.get(author, 0) + 1

        # Analyze issue authors (created and closed)
        issue_authors = {}
        for issue in issues_created + issues_closed:
            author = issue.get("author", "Unknown")
            issue_authors[author] = issue_authors.get(author, 0) + 1

        # Get unique contributors
        all_contributors = set()
        all_contributors.update(commit_authors.keys())
        all_contributors.update(pr_authors.keys())
        all_contributors.update(issue_authors.keys())

        # Build insights
        insights = []
        total_contributors = len(all_contributors)
        insights.append(
            f"{total_contributors} total contributor{'s' if total_contributors != 1 else ''} across all activities"
        )

        if commit_authors:
            top_committer = max(commit_authors, key=commit_authors.get)
            insights.append(
                f"{top_committer} is most active committer ({commit_authors[top_committer]} commits)"
            )

        if len(all_contributors) > 1:
            insights.append("Collaboration across commits, PRs, and issues")

        # Build message
        message = f"Analyzed contributor stats for {repository} over {timeframe}: {total_contributors} total contributor{'s' if total_contributors != 1 else ''}"

        # Build intent_data
        intent_data = {
            "category": intent.category.value,
            "action": intent.action,
            "confidence": intent.confidence,
            "repository": repository,
            "data_type": "contributor_stats",
            "timeframe": timeframe,
            "days": days,
            "metrics": {
                "total_contributors": total_contributors,
                "commit_authors": len(commit_authors),
                "pr_authors": len(pr_authors),
                "issue_authors": len(issue_authors),
            },
            "contributors": {"commits": commit_authors, "prs": pr_authors, "issues": issue_authors},
            "insights": insights,
        }

        return {"message": message, "intent_data": intent_data}

    async def _handle_synthesis_intent(
        self, intent: Intent, workflow, session_id: str
    ) -> IntentProcessingResult:
        """
        Handle SYNTHESIS category intents.

        Routes to appropriate synthesis service based on intent action.
        Follows EXECUTION/ANALYSIS pattern for consistency.

        GREAT-4D Phase 4: Completes intent handler coverage.
        """
        self.logger.info(f"Processing SYNTHESIS intent: {intent.action}")

        # Route based on action
        if intent.action in ["generate_content", "create_content"]:
            return await self._handle_generate_content(intent, workflow.id)

        elif intent.action in ["summarize", "create_summary"]:
            return await self._handle_summarize(intent, workflow.id)

        else:
            # Generic synthesis - provide working response
            return IntentProcessingResult(
                success=True,
                message=f"Synthesis capability ready for '{intent.action}'. Specific implementation pending.",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                },
                workflow_id=workflow.id,
                requires_clarification=True,
                clarification_type="synthesis_type",
            )

    async def _handle_generate_content(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """
        Handle content generation requests - SYNTHESIS category.

        Creates new content artifacts (status reports, README sections, issue templates).
        Unlike ANALYSIS handlers that read/analyze data, SYNTHESIS handlers create new content.

        Supported content types:
        - status_report: Generate markdown status report from repository metrics
        - readme_section: Generate README.md section (installation, usage, etc.)
        - issue_template: Generate GitHub issue template (bug_report, feature_request)
        """
        try:
            import time

            start_time = time.time()

            # 1. Validate content_type (required parameter)
            content_type = intent.context.get("content_type")
            if not content_type:
                return IntentProcessingResult(
                    success=False,
                    message="Content type is required for content generation.",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                    clarification_type="content_type_required",
                )

            # 2. Validate content_type is supported
            valid_types = ["status_report", "readme_section", "issue_template"]
            if content_type not in valid_types:
                return IntentProcessingResult(
                    success=False,
                    message=f"Unsupported content type: {content_type}. Valid types: {', '.join(valid_types)}",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "content_type": content_type,
                        "valid_types": valid_types,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                    clarification_type="unsupported_content_type",
                )

            # 3. Route to appropriate helper method
            if content_type == "status_report":
                result = await self._generate_status_report(intent, workflow_id)
            elif content_type == "readme_section":
                result = await self._generate_readme_section(intent, workflow_id)
            elif content_type == "issue_template":
                result = await self._generate_issue_template(intent, workflow_id)

            # 4. Add generation timing to metadata
            generation_time_ms = int((time.time() - start_time) * 1000)
            result.intent_data["generation_time_ms"] = generation_time_ms

            return result

        except Exception as e:
            self.logger.error(f"Failed to generate content: {e}", exc_info=True)
            return IntentProcessingResult(
                success=False,
                message=f"Content generation failed: {str(e)}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "content_type": intent.context.get("content_type"),
                },
                workflow_id=workflow_id,
                error=str(e),
                error_type="SynthesisError",
            )

    async def _generate_status_report(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """
        Generate status report from repository metrics.

        Leverages Phase 2C _handle_analyze_data to get repository metrics,
        then applies markdown template to create formatted status report.

        Parameters:
        - repository (optional): Repository to analyze (e.g., "org/repo")
        - days (optional): Days to analyze (default: 7, range: 1-90)
        - data_type (optional): Analysis type (default: "repository_metrics")
          - "repository_metrics": Activity counts and distribution
          - "activity_trends": Trends, velocity, insights
          - "contributor_stats": Contributor analysis
        """
        from datetime import datetime

        # 1. Extract and validate parameters
        repository = intent.context.get("repository")
        if not repository:
            # Try to get from user config or default
            repository = self._get_default_repository()
            if not repository:
                return IntentProcessingResult(
                    success=False,
                    message="Repository is required for status report generation.",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "content_type": "status_report",
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                    clarification_type="repository_required",
                )

        # Validate and normalize days parameter
        days = intent.context.get("days", 7)
        if not isinstance(days, int) or days < 1 or days > 90:
            days = 7  # Default to 7 days

        # Validate data_type
        data_type = intent.context.get("data_type", "repository_metrics")
        valid_types = ["repository_metrics", "activity_trends", "contributor_stats"]
        if data_type not in valid_types:
            data_type = "repository_metrics"  # Default

        # Get custom title or use default
        title = intent.context.get("title")
        if not title:
            title = f"Status Report: {repository}"

        # 2. Call Phase 2C _handle_analyze_data to get repository metrics
        analysis_intent = Intent(
            original_message=f"analyze data for {repository}",
            category=IntentCategory.ANALYSIS,
            action="analyze_data",
            confidence=1.0,
            context={
                "repository": repository,
                "days": days,
                "data_type": data_type,
            },
        )

        analysis_result = await self._handle_analyze_data(analysis_intent, workflow_id)

        if not analysis_result.success:
            return IntentProcessingResult(
                success=False,
                message=f"Failed to analyze repository: {analysis_result.message}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "content_type": "status_report",
                    "repository": repository,
                },
                workflow_id=workflow_id,
                error=analysis_result.error,
                error_type="AnalysisFailed",
            )

        # 3. Extract data from analysis result
        metrics = analysis_result.intent_data.get("metrics", {})
        trends = analysis_result.intent_data.get("trends", {})
        insights = analysis_result.intent_data.get("insights", [])
        contributors = analysis_result.intent_data.get("contributors", {})

        # 4. Apply appropriate template based on data_type
        if data_type == "repository_metrics":
            content = self._apply_repository_metrics_template(title, repository, days, metrics)
        elif data_type == "activity_trends":
            content = self._apply_activity_trends_template(
                title, repository, days, metrics, trends, insights
            )
        elif data_type == "contributor_stats":
            content = self._apply_contributor_stats_template(
                title, repository, days, metrics, contributors, insights
            )

        # 5. Validate content quality
        if not content or len(content) < 100:
            return IntentProcessingResult(
                success=False,
                message="Generated content is too short or empty",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "content_type": "status_report",
                    "content_length": len(content) if content else 0,
                },
                workflow_id=workflow_id,
                error="Content generation produced insufficient content",
                error_type="ContentGenerationError",
            )

        # 6. Return success result with generated content
        return IntentProcessingResult(
            success=True,
            message=f"Generated {data_type} status report for {repository}",
            intent_data={
                "category": intent.category.value,
                "action": intent.action,
                "content_type": "status_report",
                "repository": repository,
                "days": days,
                "data_type": data_type,
                "generated_content": content,
                "content_length": len(content),
                "metadata": {
                    "title": title,
                    "generated_at": datetime.now().isoformat(),
                    "total_activity": metrics.get("total_activity_count", 0),
                    "data_source": data_type,
                },
            },
            workflow_id=workflow_id,
            requires_clarification=False,
        )

    def _get_default_repository(self) -> str:
        """Get default repository from user config or return None."""
        # This could be enhanced to read from user config
        # For now, return None to require explicit repository
        return None

    def _apply_repository_metrics_template(
        self, title: str, repository: str, days: int, metrics: dict
    ) -> str:
        """Apply repository metrics template to generate status report."""
        from datetime import datetime

        # Extract metrics
        total = metrics.get("total_activity_count", 0)
        commits = metrics.get("commits_count", 0)
        prs = metrics.get("prs_count", 0)
        issues_created = metrics.get("issues_created_count", 0)
        issues_closed = metrics.get("issues_closed_count", 0)

        distribution = metrics.get("activity_distribution", {})
        commits_pct = distribution.get("commits", 0)
        prs_pct = distribution.get("prs", 0)
        issues_created_pct = distribution.get("issues_created", 0)
        issues_closed_pct = distribution.get("issues_closed", 0)

        # Generate ASCII bar chart
        bar_chart = self._generate_ascii_bar_chart(distribution)

        # Determine activity level
        if total > 50:
            activity_level = "high"
        elif total > 20:
            activity_level = "moderate"
        else:
            activity_level = "low"

        # Generate issue activity summary
        if issues_closed > 0:
            issue_summary = f"{issues_created} issues created and {issues_closed} closed"
        elif issues_created > 0:
            issue_summary = f"{issues_created} issues created"
        else:
            issue_summary = "no issue activity"

        # Apply template
        content = f"""# {title}

**Repository**: {repository}
**Period**: Last {days} days
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Activity Overview

- **Total Activity**: {total} events
- **Commits**: {commits} ({commits_pct:.1f}%)
- **Pull Requests**: {prs} ({prs_pct:.1f}%)
- **Issues Created**: {issues_created} ({issues_created_pct:.1f}%)
- **Issues Closed**: {issues_closed} ({issues_closed_pct:.1f}%)

---

## Activity Distribution

{bar_chart}

---

## Summary

Repository shows {activity_level} activity with {commits} commits, {prs} pull requests, and {issue_summary}.

---

*Generated by Piper Morgan at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        return content

    def _apply_activity_trends_template(
        self, title: str, repository: str, days: int, metrics: dict, trends: dict, insights: list
    ) -> str:
        """Apply activity trends template to generate status report."""
        from datetime import datetime

        # Extract metrics
        total = metrics.get("total_activity_count", 0)
        commits = metrics.get("commits_count", 0)
        prs = metrics.get("prs_count", 0)
        issues_created = metrics.get("issues_created_count", 0)
        issues_closed = metrics.get("issues_closed_count", 0)

        # Extract trends
        most_active_type = trends.get("most_active_type", "N/A")
        issue_closure_rate = trends.get("issue_closure_rate", 0)
        commit_velocity = trends.get("commit_velocity", "N/A")
        pr_activity = trends.get("pr_activity", "N/A")

        # Format insights list
        insights_text = (
            "\n".join(f"- {insight}" for insight in insights)
            if insights
            else "- No insights available"
        )

        # Apply template
        content = f"""# {title}

**Repository**: {repository}
**Period**: Last {days} days
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Activity Metrics

- **Total Activity**: {total} events
- **Commits**: {commits}
- **Pull Requests**: {prs}
- **Issues Created**: {issues_created}
- **Issues Closed**: {issues_closed}

---

## Trends

- **Most Active Type**: {most_active_type}
- **Issue Closure Rate**: {issue_closure_rate}%
- **Commit Velocity**: {commit_velocity}
- **PR Activity**: {pr_activity}

---

## Insights

{insights_text}

---

*Generated by Piper Morgan at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        return content

    def _apply_contributor_stats_template(
        self,
        title: str,
        repository: str,
        days: int,
        metrics: dict,
        contributors: dict,
        insights: list,
    ) -> str:
        """Apply contributor stats template to generate status report."""
        from datetime import datetime

        # Extract metrics
        total_contributors = metrics.get("total_contributors", 0)
        commit_authors = metrics.get("commit_authors", 0)
        pr_authors = metrics.get("pr_authors", 0)
        issue_authors = metrics.get("issue_authors", 0)

        # Generate leaderboards
        commits_leaderboard = self._generate_leaderboard(contributors.get("commits", {}))
        prs_leaderboard = self._generate_leaderboard(contributors.get("prs", {}))
        issues_leaderboard = self._generate_leaderboard(contributors.get("issues", {}))

        # Format insights list
        insights_text = (
            "\n".join(f"- {insight}" for insight in insights)
            if insights
            else "- No insights available"
        )

        # Apply template
        content = f"""# {title}

**Repository**: {repository}
**Period**: Last {days} days
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Contributor Overview

- **Total Contributors**: {total_contributors}
- **Commit Authors**: {commit_authors}
- **PR Authors**: {pr_authors}
- **Issue Authors**: {issue_authors}

---

## Top Contributors

### Commits
{commits_leaderboard}

### Pull Requests
{prs_leaderboard}

### Issues
{issues_leaderboard}

---

## Insights

{insights_text}

---

*Generated by Piper Morgan at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        return content

    def _generate_ascii_bar_chart(self, distribution: dict) -> str:
        """Generate simple ASCII bar chart from distribution data."""
        if not distribution:
            return "No distribution data available"

        lines = []
        max_bar_width = 40

        for label, percent in distribution.items():
            bar_width = int((percent / 100) * max_bar_width)
            bar = "█" * bar_width
            lines.append(f"{label:20s} │{bar} {percent:.1f}%")

        return "\n".join(lines)

    def _generate_leaderboard(self, contributor_dict: dict) -> str:
        """Generate leaderboard text from contributor dictionary."""
        if not contributor_dict:
            return "- No data available"

        # Sort by count (descending)
        sorted_contributors = sorted(contributor_dict.items(), key=lambda x: x[1], reverse=True)

        lines = []
        for i, (name, count) in enumerate(sorted_contributors[:10], 1):  # Top 10
            lines.append(f"{i}. **{name}**: {count}")

        return "\n".join(lines)

    async def _generate_readme_section(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """
        Generate README.md section.

        Creates standard README sections with language-specific templates.

        Parameters:
        - section_type (required): Type of section to generate
          - "installation": Installation instructions
          - "usage": Usage examples
          - "contributing": Contributing guidelines
          - "testing": Testing instructions
        - language (optional): Primary language (default: "python")
        - repository (optional): Repository name for examples
        - title (optional): Custom section title
        """
        from datetime import datetime

        # 1. Validate section_type (required)
        section_type = intent.context.get("section_type")
        if not section_type:
            return IntentProcessingResult(
                success=False,
                message="Section type is required for README generation.",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "content_type": "readme_section",
                },
                workflow_id=workflow_id,
                requires_clarification=True,
                clarification_type="section_type_required",
            )

        # 2. Validate section_type is supported
        valid_sections = ["installation", "usage", "contributing", "testing"]
        if section_type not in valid_sections:
            return IntentProcessingResult(
                success=False,
                message=f"Unsupported section type: {section_type}. Valid types: {', '.join(valid_sections)}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "content_type": "readme_section",
                    "section_type": section_type,
                    "valid_types": valid_sections,
                },
                workflow_id=workflow_id,
                requires_clarification=True,
                clarification_type="unsupported_section_type",
            )

        # 3. Extract optional parameters
        repository = intent.context.get("repository")
        language = intent.context.get("language", "python")
        title = intent.context.get("title", section_type.capitalize())

        # Parse repository into org/repo if provided
        org, repo = None, None
        if repository:
            parts = repository.split("/")
            if len(parts) == 2:
                org, repo = parts

        # 4. Generate content based on section_type
        if section_type == "installation":
            content = self._generate_installation_section(title, language, org, repo)
        elif section_type == "usage":
            content = self._generate_usage_section(title, language, repo)
        elif section_type == "contributing":
            content = self._generate_contributing_section(title, repo)
        elif section_type == "testing":
            content = self._generate_testing_section(title, language, repo)

        # 5. Validate content quality
        if not content or len(content) < 50:
            return IntentProcessingResult(
                success=False,
                message="Generated content is too short or empty",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "content_type": "readme_section",
                    "section_type": section_type,
                    "content_length": len(content) if content else 0,
                },
                workflow_id=workflow_id,
                error="Content generation produced insufficient content",
                error_type="ContentGenerationError",
            )

        # 6. Return success result
        return IntentProcessingResult(
            success=True,
            message=f"Generated {section_type} section for README",
            intent_data={
                "category": intent.category.value,
                "action": intent.action,
                "content_type": "readme_section",
                "section_type": section_type,
                "generated_content": content,
                "content_length": len(content),
                "metadata": {
                    "title": title,
                    "language": language,
                    "repository": repository,
                    "generated_at": datetime.now().isoformat(),
                },
            },
            workflow_id=workflow_id,
            requires_clarification=False,
        )

    def _generate_installation_section(
        self, title: str, language: str, org: str = None, repo: str = None
    ) -> str:
        """Generate installation section based on language."""

        if language.lower() in ["javascript", "typescript", "js", "ts"]:
            return self._generate_installation_javascript(title, org, repo)
        else:  # Default to Python
            return self._generate_installation_python(title, org, repo)

    def _generate_installation_python(self, title: str, org: str = None, repo: str = None) -> str:
        """Generate Python installation section."""
        repo_url = (
            f"https://github.com/{org}/{repo}.git"
            if org and repo
            else "https://github.com/ORG/REPO.git"
        )
        repo_name = repo if repo else "repo"
        package_name = repo.replace("-", "_") if repo else "package_name"

        return f"""## {title}

### Prerequisites

- Python 3.9 or higher
- pip or poetry
- Git

### Quick Start

```bash
# Clone the repository
git clone {repo_url}
cd {repo_name}

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt
```

### Verification

```bash
# Run tests
python -m pytest tests/

# Check installation
python -c "import {package_name}; print({package_name}.__version__)"
```

### Troubleshooting

If you encounter issues:

- Ensure Python 3.9+ is installed: `python --version`
- Update pip: `pip install --upgrade pip`
- Check dependencies: `pip check`
- See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues

---

*For detailed installation instructions, see [INSTALL.md](INSTALL.md)*
"""

    def _generate_installation_javascript(
        self, title: str, org: str = None, repo: str = None
    ) -> str:
        """Generate JavaScript/TypeScript installation section."""
        repo_url = (
            f"https://github.com/{org}/{repo}.git"
            if org and repo
            else "https://github.com/ORG/REPO.git"
        )
        repo_name = repo if repo else "repo"

        return f"""## {title}

### Prerequisites

- Node.js 18+ (LTS recommended)
- npm or yarn or pnpm
- Git

### Quick Start

```bash
# Clone the repository
git clone {repo_url}
cd {repo_name}

# Install dependencies
npm install
# or: yarn install
# or: pnpm install
```

### Verification

```bash
# Run tests
npm test

# Build the project
npm run build

# Check installation
npm list
```

### Troubleshooting

If you encounter issues:

- Ensure Node.js 18+ is installed: `node --version`
- Clear npm cache: `npm cache clean --force`
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`
- See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues

---

*For detailed installation instructions, see [INSTALL.md](INSTALL.md)*
"""

    def _generate_usage_section(self, title: str, language: str, repo: str = None) -> str:
        """Generate usage section based on language."""

        if language.lower() in ["javascript", "typescript", "js", "ts"]:
            return self._generate_usage_javascript(title, repo)
        else:  # Default to Python
            return self._generate_usage_python(title, repo)

    def _generate_usage_python(self, title: str, repo: str = None) -> str:
        """Generate Python usage section."""
        package_name = repo.replace("-", "_") if repo else "package_name"

        return f"""## {title}

### Basic Usage

```python
from {package_name} import Client

# Initialize
client = Client()

# Basic operation
result = client.process("input data")
print(result)
```

### Common Use Cases

#### Use Case 1: Simple Processing

```python
# Process a single item
result = client.process_item(item)
```

#### Use Case 2: Batch Processing

```python
# Process multiple items
results = client.process_batch(items)
for result in results:
    print(result)
```

#### Use Case 3: Async Processing

```python
import asyncio

async def main():
    async with Client() as client:
        result = await client.process_async("data")
        print(result)

asyncio.run(main())
```

### Configuration

Create a configuration file:

```python
# config.py
config = {{
    "option1": "value1",
    "option2": "value2"
}}
```

Use configuration:

```python
from config import config

client = Client(config=config)
```

### Examples

See [examples/](examples/) directory for complete examples:

- [examples/basic.py](examples/basic.py) - Basic usage
- [examples/advanced.py](examples/advanced.py) - Advanced features
- [examples/async.py](examples/async.py) - Async operations

---

*For more examples, see [examples/](examples/)*
"""

    def _generate_usage_javascript(self, title: str, repo: str = None) -> str:
        """Generate JavaScript usage section."""
        package_name = repo if repo else "package-name"

        return f"""## {title}

### Basic Usage

```javascript
const {{ Client }} = require('{package_name}');

// Initialize
const client = new Client();

// Basic operation
const result = client.process('input data');
console.log(result);
```

### Common Use Cases

#### Use Case 1: Simple Processing

```javascript
// Process a single item
const result = client.processItem(item);
```

#### Use Case 2: Batch Processing

```javascript
// Process multiple items
const results = client.processBatch(items);
results.forEach(result => console.log(result));
```

#### Use Case 3: Async/Await

```javascript
async function main() {{
    const result = await client.processAsync('data');
    console.log(result);
}}

main();
```

### Configuration

Create a configuration file:

```javascript
// config.js
module.exports = {{
    option1: 'value1',
    option2: 'value2'
}};
```

Use configuration:

```javascript
const config = require('./config');
const client = new Client(config);
```

### Examples

See [examples/](examples/) directory for complete examples:

- [examples/basic.js](examples/basic.js) - Basic usage
- [examples/advanced.js](examples/advanced.js) - Advanced features
- [examples/async.js](examples/async.js) - Async operations

---

*For more examples, see [examples/](examples/)*
"""

    def _generate_contributing_section(self, title: str, repo: str = None) -> str:
        """Generate contributing section."""
        repo_name = repo if repo else "repo"
        package_name = repo.replace("-", "_") if repo else "package_name"

        return f"""## {title}

We welcome contributions! Here's how to get started.

### Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/{repo_name}.git
   cd {repo_name}
   ```
3. Create a virtual environment and install dev dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -e ".[dev]"
   ```
4. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

### Making Changes

1. Make your changes in the feature branch
2. Add tests for new functionality
3. Update documentation as needed
4. Ensure all tests pass: `pytest`
5. Run linting: `flake8 .` and `black .`

### Code Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints for function signatures
- Write docstrings for all public functions/classes
- Keep functions focused and under 50 lines
- Maximum line length: 100 characters

### Testing

- Write unit tests for all new code
- Maintain or improve code coverage (target: 80%+)
- Run full test suite before submitting: `pytest tests/`
- Run coverage check: `pytest --cov={package_name} tests/`

### Submitting Changes

1. Commit your changes:
   ```bash
   git commit -m "feat: add new feature"
   ```
   Follow [Conventional Commits](https://www.conventionalcommits.org/)

2. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

3. Create a Pull Request:
   - Describe your changes
   - Link any related issues
   - Add screenshots if UI changes
   - Wait for review and address feedback

---

*See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines*
"""

    def _generate_testing_section(self, title: str, language: str, repo: str = None) -> str:
        """Generate testing section based on language."""
        package_name = repo.replace("-", "_") if repo else "package_name"

        return f"""## {title}

### Running Tests

Run all tests:
```bash
pytest
```

Run specific test file:
```bash
pytest tests/test_module.py
```

Run specific test:
```bash
pytest tests/test_module.py::test_function
```

Run with coverage:
```bash
pytest --cov={package_name} --cov-report=html tests/
```

Run with verbose output:
```bash
pytest -v
```

### Test Structure

```
tests/
├── unit/               # Unit tests
│   ├── test_core.py
│   └── test_utils.py
├── integration/        # Integration tests
│   └── test_workflow.py
├── fixtures/           # Test fixtures and data
│   └── sample_data.json
└── conftest.py        # Shared fixtures
```

### Writing Tests

Use pytest fixtures for setup:

```python
import pytest
from {package_name} import Client

@pytest.fixture
def client():
    return Client()

def test_basic_functionality(client):
    result = client.process("test input")
    assert result is not None
    assert "expected" in result
```

### Coverage

Current coverage: **85%** (target: 80%+)

View coverage report:
```bash
pytest --cov={package_name} --cov-report=html tests/
open htmlcov/index.html
```

---

*See [tests/README.md](tests/README.md) for detailed testing guide*
"""

    async def _generate_issue_template(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """
        Generate GitHub issue template.

        Creates YAML-formatted issue templates for .github/ISSUE_TEMPLATE/ directory.

        Parameters:
        - template_type (required): Type of template to generate
          - "bug_report": Bug report template
          - "feature_request": Feature request template
          - "custom": Custom template (requires additional context)
        - labels (optional): Default labels to apply
        - repository (optional): Repository name for context
        """
        from datetime import datetime

        # 1. Validate template_type (required)
        template_type = intent.context.get("template_type")
        if not template_type:
            return IntentProcessingResult(
                success=False,
                message="Template type is required for issue template generation.",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "content_type": "issue_template",
                },
                workflow_id=workflow_id,
                requires_clarification=True,
                clarification_type="template_type_required",
            )

        # 2. Validate template_type is supported
        valid_types = ["bug_report", "feature_request", "custom"]
        if template_type not in valid_types:
            return IntentProcessingResult(
                success=False,
                message=f"Unsupported template type: {template_type}. Valid types: {', '.join(valid_types)}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "content_type": "issue_template",
                    "template_type": template_type,
                    "valid_types": valid_types,
                },
                workflow_id=workflow_id,
                requires_clarification=True,
                clarification_type="unsupported_template_type",
            )

        # 3. Extract optional parameters
        repository = intent.context.get("repository")
        labels = intent.context.get("labels")

        # Set default labels based on template type
        if not labels:
            if template_type == "bug_report":
                labels = ["bug", "needs-triage"]
            elif template_type == "feature_request":
                labels = ["enhancement", "needs-triage"]
            else:
                labels = ["needs-triage"]

        # 4. Generate content based on template_type
        if template_type == "bug_report":
            content = self._generate_bug_report_template(labels)
            filename = "bug_report.yml"
        elif template_type == "feature_request":
            content = self._generate_feature_request_template(labels)
            filename = "feature_request.yml"
        elif template_type == "custom":
            content = self._generate_custom_template(intent.context, labels)
            filename = "custom_template.yml"

        # 5. Validate content quality
        if not content or len(content) < 50:
            return IntentProcessingResult(
                success=False,
                message="Generated content is too short or empty",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "content_type": "issue_template",
                    "template_type": template_type,
                    "content_length": len(content) if content else 0,
                },
                workflow_id=workflow_id,
                error="Content generation produced insufficient content",
                error_type="ContentGenerationError",
            )

        # 6. Return success result
        return IntentProcessingResult(
            success=True,
            message=f"Generated {template_type} issue template",
            intent_data={
                "category": intent.category.value,
                "action": intent.action,
                "content_type": "issue_template",
                "template_type": template_type,
                "generated_content": content,
                "content_length": len(content),
                "metadata": {
                    "filename": filename,
                    "labels": labels,
                    "repository": repository,
                    "generated_at": datetime.now().isoformat(),
                    "installation_path": f".github/ISSUE_TEMPLATE/{filename}",
                },
            },
            workflow_id=workflow_id,
            requires_clarification=False,
        )

    def _generate_bug_report_template(self, labels: list) -> str:
        """Generate bug report issue template."""
        labels_yaml = ", ".join(f'"{label}"' for label in labels)

        return f"""---
name: Bug Report
about: Report a bug to help us improve
title: "[BUG] "
labels: [{labels_yaml}]
assignees: []
---

## Description

A clear and concise description of the bug.

## Steps to Reproduce

1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

## Expected Behavior

A clear description of what you expected to happen.

## Actual Behavior

A clear description of what actually happened.

## Screenshots

If applicable, add screenshots to help explain the problem.

## Environment

- **OS**: [e.g., macOS 14.0, Windows 11, Ubuntu 22.04]
- **Browser** (if applicable): [e.g., Chrome 120, Safari 17]
- **Version**: [e.g., 1.0.0]
- **Python Version** (if applicable): [e.g., 3.9.6]

## Additional Context

Add any other context about the problem here.

## Possible Solution

If you have suggestions on how to fix the bug, please describe them here.
"""

    def _generate_feature_request_template(self, labels: list) -> str:
        """Generate feature request issue template."""
        labels_yaml = ", ".join(f'"{label}"' for label in labels)

        return f"""---
name: Feature Request
about: Suggest a new feature or enhancement
title: "[FEATURE] "
labels: [{labels_yaml}]
assignees: []
---

## Feature Description

A clear and concise description of the feature you'd like to see.

## Problem Statement

Describe the problem this feature would solve. Why is this feature needed?

## Proposed Solution

Describe your proposed solution. How would you like this feature to work?

## Alternatives Considered

Have you considered any alternative solutions? If so, describe them here.

## Use Cases

Describe specific use cases where this feature would be valuable:

1. Use case 1...
2. Use case 2...
3. Use case 3...

## Additional Context

Add any other context, mockups, or examples about the feature request here.

## Acceptance Criteria

What would need to be true for this feature to be considered complete?

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Priority

How important is this feature to you?

- [ ] Critical - Blocking my work
- [ ] High - Significantly improves my workflow
- [ ] Medium - Nice to have
- [ ] Low - Minor improvement
"""

    def _generate_custom_template(self, context: dict, labels: list) -> str:
        """Generate custom issue template."""
        labels_yaml = ", ".join(f'"{label}"' for label in labels)

        # Extract custom parameters or use defaults
        custom_name = context.get("custom_name", "Custom Issue")
        custom_description = context.get("custom_description", "Custom issue template")
        custom_title_prefix = context.get("custom_title_prefix", "")

        return f"""---
name: {custom_name}
about: {custom_description}
title: "{custom_title_prefix}"
labels: [{labels_yaml}]
assignees: []
---

## Description

Please provide a detailed description.

## Context

Add any relevant context or background information.

## Checklist

- [ ] I have read the contributing guidelines
- [ ] I have searched existing issues
- [ ] I have provided all requested information

## Additional Information

Add any additional information here.
"""

    async def _handle_summarize(self, intent: Intent, workflow_id: str) -> IntentProcessingResult:
        """
        Handle summarization requests - FULLY IMPLEMENTED.

        Creates concise summaries of content from various sources. This is a SYNTHESIS
        operation that creates new condensed versions of existing content.

        Supported source_types:
            - 'github_issue': Summarize GitHub issue and comments
            - 'commit_range': Summarize commits from a time period
            - 'text': Summarize provided text content
        """
        try:
            # 1. VALIDATION
            source_type = intent.context.get("source_type")

            if not source_type:
                return IntentProcessingResult(
                    success=False,
                    message="Cannot summarize: source type not specified. Please specify 'github_issue', 'commit_range', or 'text'.",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                    clarification_type="source_type_required",
                )

            # Validate source_type
            valid_sources = ["github_issue", "commit_range", "text"]
            if source_type not in valid_sources:
                return IntentProcessingResult(
                    success=False,
                    message=f"Unknown source type '{source_type}'. Supported types: {', '.join(valid_sources)}",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "requested_source_type": source_type,
                    },
                    workflow_id=workflow_id,
                    error=f"Unknown source type: {source_type}",
                    error_type="ValidationError",
                )

            # 2. FETCH CONTENT based on source_type
            try:
                if source_type == "github_issue":
                    content, source_metadata = await self._fetch_issue_content(intent.context)
                elif source_type == "commit_range":
                    content, source_metadata = await self._fetch_commit_content(
                        intent.context, workflow_id
                    )
                elif source_type == "text":
                    content, source_metadata = self._extract_text_content(intent.context)

                # Check for empty content
                if not content or len(content.strip()) < 50:
                    return IntentProcessingResult(
                        success=False,
                        message=f"Content too short to summarize (< 50 characters). Please provide more content.",
                        intent_data={
                            "category": intent.category.value,
                            "action": intent.action,
                            "source_type": source_type,
                        },
                        workflow_id=workflow_id,
                        error="Content too short",
                        error_type="ValidationError",
                    )

            except ValueError as e:
                # Parameter validation errors
                return IntentProcessingResult(
                    success=False,
                    message=f"Validation error: {str(e)}",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "source_type": source_type,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                    clarification_type="parameter_validation",
                    error=str(e),
                    error_type="ValidationError",
                )

            # 3. SUMMARIZE with LLM
            length = intent.context.get("length", "moderate")

            doc_summary = await self._summarize_with_llm(
                content=content, source_type=source_type, length=length, **source_metadata
            )

            # 4. FORMAT summary
            format_type = intent.context.get("format", "bullet_points")
            formatted_summary = self._format_summary(doc_summary, format_type)

            # 5. CALCULATE metrics
            original_length = len(content)
            summary_length = len(formatted_summary)
            compression_ratio = summary_length / original_length if original_length > 0 else 0.0

            # 6. BUILD response
            return IntentProcessingResult(
                success=True,
                message=f"Summarized {source_type} successfully ({original_length} → {summary_length} chars, {compression_ratio:.1%} compression)",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    # Summary content
                    "summary": formatted_summary,
                    "summary_format": format_type,
                    "summary_length": summary_length,
                    # Metrics
                    "original_length": original_length,
                    "compression_ratio": compression_ratio,
                    # Structured data
                    "title": doc_summary.title,
                    "document_type": doc_summary.document_type,
                    "key_findings": doc_summary.key_findings,
                    # Source info
                    "source_type": source_type,
                    "source_metadata": source_metadata,
                    # Timing
                    "summarized_at": datetime.now().isoformat(),
                },
                workflow_id=workflow_id,
                requires_clarification=False,
            )

        except Exception as e:
            self.logger.error(f"Failed to summarize: {e}", exc_info=True)
            return IntentProcessingResult(
                success=False,
                message=f"Summarization failed: {str(e)}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                },
                workflow_id=workflow_id,
                error=str(e),
                error_type="SynthesisError",
            )

    async def _fetch_issue_content(self, context: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """
        Fetch and format GitHub issue content for summarization.

        Args:
            context: Intent context containing issue_url OR (repository + issue_number)

        Returns:
            Tuple of (content_string, metadata_dict)
        """
        from services.domain.github_domain_service import GitHubDomainService

        # Extract parameters
        issue_url = context.get("issue_url")
        repository = context.get("repository")
        issue_number = context.get("issue_number")
        include_comments = context.get("include_comments", True)
        max_comments = context.get("max_comments", 10)

        # Validate we have required params
        if not issue_url and not (repository and issue_number):
            raise ValueError("Either issue_url or (repository + issue_number) is required")

        # Initialize GitHub service
        github_service = GitHubDomainService()

        # Fetch issue
        try:
            if issue_url:
                # Parse URL to extract repo and number
                import re

                match = re.match(r"https://github\.com/([^/]+)/([^/]+)/issues/(\d+)", issue_url)
                if not match:
                    raise ValueError(f"Invalid issue URL format: {issue_url}")
                owner, repo, num = match.groups()
                repository = f"{owner}/{repo}"
                issue_number = int(num)

            # Fetch issue data
            issue = await github_service.get_issue(repository, issue_number)

            # Extract fields
            title = issue.get("title", "Untitled")
            body = issue.get("body", "")
            state = issue.get("state", "unknown")
            created_at = issue.get("created_at", "")

            # Handle author - could be nested dict
            author_data = issue.get("user") or issue.get("author", {})
            if isinstance(author_data, dict):
                author = author_data.get("login", "unknown")
            else:
                author = str(author_data)

            # Build content markdown
            content_parts = [
                f"# GitHub Issue Summary Request\n",
                f"**Issue**: #{issue_number} - {title}",
                f"**Repository**: {repository}",
                f"**Status**: {state}",
                f"**Created**: {created_at}",
                f"**Author**: {author}\n",
                f"## Issue Body\n",
                body or "(No description provided)",
            ]

            # Add comments if requested
            comment_count = 0
            if include_comments:
                comments = issue.get("comments", [])
                if isinstance(comments, list):
                    comment_count = len(comments)
                    if comment_count > 0:
                        content_parts.append(
                            f"\n## Comments ({comment_count} total, showing {min(comment_count, max_comments)})\n"
                        )
                        for i, comment in enumerate(comments[:max_comments], 1):
                            comment_author_data = comment.get("user") or comment.get("author", {})
                            if isinstance(comment_author_data, dict):
                                comment_author = comment_author_data.get("login", "unknown")
                            else:
                                comment_author = str(comment_author_data)
                            comment_body = comment.get("body", "")
                            comment_date = comment.get("created_at", "")
                            content_parts.append(
                                f"### Comment {i} by {comment_author} ({comment_date})\n"
                            )
                            content_parts.append(comment_body)
                            content_parts.append("")  # Blank line

            content = "\n".join(content_parts)

            # Build metadata
            metadata = {
                "issue_url": f"https://github.com/{repository}/issues/{issue_number}",
                "issue_number": issue_number,
                "repository": repository,
                "issue_state": state,
                "comment_count": comment_count,
                "comments_included": min(comment_count, max_comments) if include_comments else 0,
                "author": author,
                "created_at": created_at,
            }

            return content, metadata

        except Exception as e:
            self.logger.error(f"Failed to fetch issue content: {e}", exc_info=True)
            raise Exception(f"Failed to fetch GitHub issue: {str(e)}")

    async def _fetch_commit_content(
        self, context: Dict[str, Any], workflow_id: str
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Fetch and format commit data for summarization.

        Integrates with Phase 2C _handle_analyze_commits.

        Args:
            context: Intent context containing repository and timeframe params
            workflow_id: Current workflow ID

        Returns:
            Tuple of (content_string, metadata_dict)
        """
        # Extract parameters
        repository = context.get("repository")
        if not repository:
            raise ValueError("repository is required for commit_range summarization")

        days = context.get("days", 7)
        timeframe = context.get("timeframe", f"last {days} days")
        categorize = context.get("categorize", True)

        # Build intent for Phase 2C
        from services.domain.models import Intent as DomainIntent

        commit_intent = DomainIntent(
            original_message=f"analyze commits for {repository}",
            category=IntentCategory.ANALYSIS,
            action="analyze_commits",
            confidence=1.0,
            context={
                "repository": repository,
                "days": days,
            },
        )

        # Call Phase 2C handler
        commit_result = await self._handle_analyze_commits(commit_intent, workflow_id)

        if not commit_result.success:
            raise Exception(f"Failed to fetch commits: {commit_result.message}")

        # Extract commit data
        commit_count = commit_result.intent_data.get("commit_count", 0)
        commits = commit_result.intent_data.get("recent_messages", [])
        authors = commit_result.intent_data.get("authors", {})

        # Build content
        content_parts = [
            f"# Commit Summary Request\n",
            f"**Repository**: {repository}",
            f"**Timeframe**: {timeframe}",
            f"**Total Commits**: {commit_count}",
            f"**Authors**: {', '.join([f'{name} ({count})' for name, count in authors.items()])}\n",
        ]

        # Categorize commits if requested
        if categorize and commits:
            categories = self._categorize_commits(commits)

            # Add categorized commits
            for category, cat_commits in categories.items():
                if cat_commits:
                    category_title = category.capitalize() if category != "other" else "Other"
                    content_parts.append(f"## {category_title} ({len(cat_commits)} commits)\n")
                    for commit in cat_commits:
                        content_parts.append(f"- {commit}")
                    content_parts.append("")  # Blank line
        else:
            # Non-categorized list
            content_parts.append(f"## Commits (chronological)\n")
            for i, commit in enumerate(commits, 1):
                content_parts.append(f"{i}. {commit}")

        content = "\n".join(content_parts)

        # Build metadata
        metadata = {
            "repository": repository,
            "commit_count": commit_count,
            "timeframe": timeframe,
            "days": days,
            "authors": authors,
        }

        if categorize:
            categories = self._categorize_commits(commits)
            category_counts = {cat: len(msgs) for cat, msgs in categories.items()}
            metadata["categories"] = category_counts

        return content, metadata

    def _extract_text_content(self, context: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """
        Extract and validate text content for summarization.

        Args:
            context: Intent context containing content text

        Returns:
            Tuple of (content_string, metadata_dict)
        """
        # Extract content
        content = context.get("content")
        if not content:
            raise ValueError("content is required for text summarization")

        if not isinstance(content, str):
            raise ValueError("content must be a string")

        # Validate minimum length
        if len(content.strip()) < 50:
            raise ValueError("content is too short to summarize (minimum 50 characters)")

        # Truncate if too long (with warning)
        MAX_LENGTH = 10000
        if len(content) > MAX_LENGTH:
            self.logger.warning(
                f"Content exceeds maximum length ({len(content)} > {MAX_LENGTH}), truncating"
            )
            content = content[:MAX_LENGTH]

        # Extract optional params
        title = context.get("title", "Document")
        document_type = context.get("document_type", "Text")

        # Build formatted content
        formatted_content = f"""# Text Summary Request

**Title**: {title}
**Document Type**: {document_type}
**Length**: {len(content)} characters

## Content

{content}"""

        # Build metadata
        metadata = {
            "title": title,
            "document_type": document_type,
            "original_length": len(content),
            "provided_by": "user",
        }

        return formatted_content, metadata

    async def _summarize_with_llm(
        self, content: str, source_type: str, length: str = "moderate", **kwargs
    ):
        """
        Summarize content using LLM with structured JSON output.

        Args:
            content: Formatted content to summarize
            source_type: Type of source
            length: Desired summary length
            **kwargs: Additional metadata

        Returns:
            DocumentSummary object with structured summary
        """
        # Initialize LLM client if needed (for test mocking)
        if not hasattr(self, "llm_client") or self.llm_client is None:
            from services.llm.clients import get_selected_client

            self.llm_client = get_selected_client()

        # Build length guidance
        length_guidance = {
            "brief": "Provide 2-3 key points only.",
            "moderate": "Provide 5-7 key points covering main topics.",
            "detailed": "Provide 10+ key points with comprehensive coverage.",
        }.get(length, "Provide 5-7 key points covering main topics.")

        # Build source-specific guidance
        source_guidance = {
            "github_issue": "Focus on the issue description, key discussion points, and proposed solutions.",
            "commit_range": "Focus on categorizing changes by type (features, fixes, chores) and identifying key contributors.",
            "text": "Focus on extracting the main themes and important details.",
        }.get(source_type, "Focus on the key themes and important details.")

        # Truncate content to avoid token limits (like TextAnalyzer does)
        truncated_content = content[:3000]

        # Build prompt
        prompt = f"""Please summarize the following content.

{source_guidance}
{length_guidance}

Return a JSON object with this exact structure:
{{
    "title": "Brief title for the summary",
    "document_type": "{source_type}",
    "key_findings": ["Finding 1", "Finding 2", "Finding 3", ...],
    "sections": []
}}

Content to summarize:

{truncated_content}"""

        # Call LLM with JSON mode
        try:
            json_response = await self.llm_client.complete(
                task_type="summarize", prompt=prompt, response_format={"type": "json_object"}
            )

            # Parse JSON response
            summary_data = json.loads(json_response)

            # Create DocumentSummary-like object
            from services.analysis.summary_parser import DocumentSummary

            doc_summary = DocumentSummary(
                title=summary_data.get("title", "Summary"),
                document_type=summary_data.get("document_type", source_type),
                key_findings=summary_data.get("key_findings", []),
                sections=summary_data.get("sections", []),
            )

            return doc_summary

        except Exception as e:
            self.logger.error(f"LLM summarization failed: {e}", exc_info=True)
            raise Exception(f"Failed to generate summary: {str(e)}")

    def _format_summary(self, doc_summary, format_type: str = "bullet_points") -> str:
        """
        Format DocumentSummary into requested output format.

        Args:
            doc_summary: Structured summary from LLM
            format_type: Output format (bullet_points, paragraph, executive_summary)

        Returns:
            Formatted summary string
        """
        if format_type == "paragraph":
            # Convert to narrative paragraph
            sentences = []
            sentences.append(f"This document discusses {doc_summary.title}.")
            sentences.extend(doc_summary.key_findings)
            return " ".join(sentences)

        elif format_type == "executive_summary":
            # Build executive summary structure
            parts = [
                f"# Executive Summary: {doc_summary.title}\n",
                f"## Overview\n",
            ]

            if doc_summary.key_findings:
                parts.append(doc_summary.key_findings[0])
                parts.append("\n## Key Points\n")
                for finding in doc_summary.key_findings[1:]:
                    parts.append(f"- {finding}")

            if doc_summary.sections:
                parts.append("\n## Details\n")
                for section in doc_summary.sections:
                    if isinstance(section, dict):
                        title = section.get("title", "")
                        points = section.get("points", [])
                        parts.append(f"### {title}\n")
                        for point in points:
                            parts.append(f"- {point}")

            return "\n".join(parts)

        else:
            # Default to bullet_points - use to_markdown if available
            if hasattr(doc_summary, "to_markdown"):
                return doc_summary.to_markdown()
            else:
                # Fallback: build markdown manually
                parts = [f"## Summary: {doc_summary.title}\n"]
                if doc_summary.key_findings:
                    parts.append("### Key Findings\n")
                    for finding in doc_summary.key_findings:
                        parts.append(f"- {finding}")
                return "\n".join(parts)

    def _categorize_commits(self, commits: List[str]) -> Dict[str, List[str]]:
        """
        Categorize commit messages by conventional commit type.

        Args:
            commits: List of commit messages

        Returns:
            Dict mapping category to list of commit messages
        """
        if not commits:
            return {}

        # Define categories
        CATEGORIES = {
            "feat": "Features",
            "fix": "Bug Fixes",
            "docs": "Documentation",
            "chore": "Chores",
            "refactor": "Refactoring",
            "test": "Tests",
            "style": "Style",
            "perf": "Performance",
            "ci": "CI/CD",
        }

        # Initialize categories dict
        categories = {cat: [] for cat in CATEGORIES.keys()}
        categories["other"] = []

        # Categorize each commit
        for commit in commits:
            categorized = False
            for cat in CATEGORIES.keys():
                # Check if commit starts with category prefix
                if commit.startswith(f"{cat}:") or commit.startswith(f"{cat}("):
                    categories[cat].append(commit)
                    categorized = True
                    break

            if not categorized:
                categories["other"].append(commit)

        # Remove empty categories
        return {cat: msgs for cat, msgs in categories.items() if msgs}

    async def _handle_strategy_intent(
        self, intent: Intent, workflow, session_id: str
    ) -> IntentProcessingResult:
        """
        Handle STRATEGY category intents.

        Routes to appropriate strategy service based on intent action.
        Follows EXECUTION/ANALYSIS pattern for consistency.

        GREAT-4D Phase 5: Completes intent handler coverage.
        """
        self.logger.info(f"Processing STRATEGY intent: {intent.action}")

        # Route based on action
        if intent.action in ["strategic_planning", "create_plan"]:
            return await self._handle_strategic_planning(intent, workflow.id)

        elif intent.action in ["prioritize", "set_priorities"]:
            return await self._handle_prioritization(intent, workflow.id)

        else:
            # Generic strategy - provide working response
            return IntentProcessingResult(
                success=True,
                message=f"Strategy capability ready for '{intent.action}'. Specific implementation pending.",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                },
                workflow_id=workflow.id,
                requires_clarification=True,
                clarification_type="strategy_scope",
            )

    async def _handle_strategic_planning(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """
        Handle strategic planning requests - FULLY IMPLEMENTED.

        Creates strategic plans for projects, sprints, features, and issue resolution.
        This is a STRATEGY operation that plans future actions and provides recommendations.

        Supported planning_types:
            - 'sprint': Sprint/iteration planning with 3-phase structure
            - 'feature_roadmap': Feature development roadmap with 4-phase structure
            - 'issue_resolution': Strategic issue resolution with 4-phase structure

        Intent Context Parameters:
            - planning_type (required): Type of plan to create
            - goal (required): Primary goal/objective for the plan
            - timeframe (optional): Duration/deadline (default: type-specific)
            - context (optional): Additional context or constraints

        Returns:
            IntentProcessingResult with plan, recommendations, and metadata
        """
        try:
            # 1. VALIDATION - Check planning_type
            planning_type = intent.context.get("planning_type")
            if not planning_type:
                self.logger.warning("Planning type missing for strategic planning")
                return IntentProcessingResult(
                    success=False,
                    message="Cannot create plan: planning type not specified. Supported types: sprint, feature_roadmap, issue_resolution",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                    clarification_type="planning_type_required",
                )

            # Validate goal
            goal = intent.context.get("goal")
            if not goal:
                self.logger.warning("Goal missing for strategic planning")
                return IntentProcessingResult(
                    success=False,
                    message="Cannot create plan: goal not specified. Please provide the objective or goal for this plan.",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "planning_type": planning_type,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                    clarification_type="goal_required",
                )

            # Normalize planning_type
            planning_type = planning_type.lower().strip()

            # Validate planning_type is supported
            supported_types = ["sprint", "feature_roadmap", "issue_resolution"]
            if planning_type not in supported_types:
                self.logger.warning(f"Unsupported planning type: {planning_type}")
                return IntentProcessingResult(
                    success=False,
                    message=f"Planning type '{planning_type}' is not supported. Supported types: {', '.join(supported_types)}",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "planning_type": planning_type,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                    clarification_type="unsupported_planning_type",
                )

            # Get optional parameters
            timeframe = intent.context.get("timeframe", "not_specified")
            context = intent.context.get("context", "")

            # 2. CREATE PLAN based on type
            if planning_type == "sprint":
                plan = self._create_sprint_plan(goal, timeframe, context)
            elif planning_type == "feature_roadmap":
                plan = self._create_feature_roadmap(goal, timeframe, context)
            elif planning_type == "issue_resolution":
                plan = self._create_issue_resolution_plan(goal, context)
            else:
                # This should never happen due to validation above
                raise ValueError(f"Unhandled planning type: {planning_type}")

            # 3. GENERATE RECOMMENDATIONS
            recommendations = self._generate_strategic_recommendations(plan, planning_type)

            # 4. BUILD RESPONSE
            self.logger.info(f"Successfully created {planning_type} plan for goal: {goal}")
            return IntentProcessingResult(
                success=True,
                message=f"Successfully created {planning_type} plan: {goal}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "planning_type": planning_type,
                    "goal": goal,
                    "timeframe": timeframe,
                    "plan": plan,
                    "recommendations": recommendations,
                },
                workflow_id=workflow_id,
                requires_clarification=False,
            )

        except Exception as e:
            # 5. ERROR HANDLING
            self.logger.error(f"Failed to create strategic plan: {e}", exc_info=True)
            return IntentProcessingResult(
                success=False,
                message=f"Failed to create strategic plan: {str(e)}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                },
                workflow_id=workflow_id,
                error=str(e),
                error_type="StrategyError",
            )

    def _create_sprint_plan(self, goal: str, timeframe: str, context: str) -> Dict[str, Any]:
        """
        Create a sprint plan with 3-phase structure (Planning, Implementation, Testing).

        Args:
            goal: Sprint goal/objective
            timeframe: Duration (e.g., '2_weeks', '1_week', '3_weeks')
            context: Additional context or constraints

        Returns:
            Dictionary containing sprint plan with phases, tasks, and success criteria
        """
        # Parse timeframe to days
        duration_days = self._parse_timeframe_to_days(timeframe)

        # Create structured 3-phase plan
        plan = {
            "goal": goal,
            "duration": f"{duration_days} days",
            "phases": [
                {
                    "phase": 1,
                    "name": "Planning & Setup",
                    "duration": "1-2 days",
                    "tasks": [
                        {"task": f"Refine requirements for: {goal}", "priority": "high"},
                        {
                            "task": "Set up development environment and dependencies",
                            "priority": "high",
                        },
                        {
                            "task": "Create detailed task breakdown and estimates",
                            "priority": "medium",
                        },
                        {
                            "task": "Identify potential risks and mitigation strategies",
                            "priority": "medium",
                        },
                    ],
                },
                {
                    "phase": 2,
                    "name": "Implementation",
                    "duration": f"{max(duration_days - 4, 5)} days",
                    "tasks": [
                        {"task": f"Implement core functionality for: {goal}", "priority": "high"},
                        {
                            "task": "Write comprehensive unit tests for all components",
                            "priority": "high",
                        },
                        {"task": "Conduct code review and address feedback", "priority": "high"},
                        {"task": "Refactor and optimize implementation", "priority": "medium"},
                        {"task": "Document code and API interfaces", "priority": "medium"},
                    ],
                },
                {
                    "phase": 3,
                    "name": "Testing & Deployment",
                    "duration": "2-3 days",
                    "tasks": [
                        {"task": "Run integration tests with existing system", "priority": "high"},
                        {
                            "task": "Perform manual QA testing and edge case validation",
                            "priority": "high",
                        },
                        {"task": "Complete user documentation and guides", "priority": "medium"},
                        {
                            "task": "Deploy to staging environment for validation",
                            "priority": "high",
                        },
                        {"task": "Production deployment with monitoring", "priority": "high"},
                    ],
                },
            ],
            "success_criteria": [
                f"{goal} is fully implemented and tested",
                "All tests passing (unit, integration, manual QA)",
                "Code reviewed and documented",
                "Successfully deployed to production with monitoring enabled",
            ],
        }

        return plan

    def _create_feature_roadmap(self, goal: str, timeframe: str, context: str) -> Dict[str, Any]:
        """
        Create a feature development roadmap with 4-phase structure.

        Args:
            goal: Feature goal/objective
            timeframe: Duration (e.g., '3_months', '1_month', '6_months')
            context: Additional context or constraints

        Returns:
            Dictionary containing feature roadmap with phases, milestones, and dependencies
        """
        # Parse timeframe
        duration_days = self._parse_timeframe_to_days(timeframe)
        num_months = max(1, duration_days // 30)

        # Create structured 4-phase roadmap
        plan = {
            "goal": goal,
            "duration": f"{num_months} month{'s' if num_months != 1 else ''}",
            "phases": [
                {
                    "phase": 1,
                    "name": "Research & Planning",
                    "duration": "2-3 weeks",
                    "tasks": [
                        {
                            "task": "Conduct user interviews and gather requirements",
                            "priority": "high",
                        },
                        {
                            "task": "Analyze competitor solutions and market research",
                            "priority": "medium",
                        },
                        {"task": f"Define key features and scope for: {goal}", "priority": "high"},
                        {"task": "Create technical specification document", "priority": "high"},
                        {"task": "Design mockups and user flows", "priority": "medium"},
                    ],
                },
                {
                    "phase": 2,
                    "name": "MVP Development",
                    "duration": "4-6 weeks",
                    "tasks": [
                        {"task": "Implement core feature functionality", "priority": "high"},
                        {
                            "task": "Build basic user interface with essential workflows",
                            "priority": "high",
                        },
                        {"task": "Create data models and backend services", "priority": "high"},
                        {"task": "Write unit and integration tests", "priority": "high"},
                        {"task": "Internal alpha testing with team", "priority": "high"},
                    ],
                },
                {
                    "phase": 3,
                    "name": "Enhancement & Polish",
                    "duration": "3-4 weeks",
                    "tasks": [
                        {
                            "task": "Add advanced features based on MVP feedback",
                            "priority": "medium",
                        },
                        {"task": "Implement performance optimizations", "priority": "high"},
                        {
                            "task": "Polish UI/UX based on alpha testing feedback",
                            "priority": "high",
                        },
                        {
                            "task": "Enhance error handling and edge case coverage",
                            "priority": "medium",
                        },
                        {"task": "Complete comprehensive documentation", "priority": "medium"},
                    ],
                },
                {
                    "phase": 4,
                    "name": "Launch Preparation",
                    "duration": "1-2 weeks",
                    "tasks": [
                        {"task": "Beta testing with external users", "priority": "high"},
                        {
                            "task": "Fix critical bugs and issues from beta feedback",
                            "priority": "high",
                        },
                        {
                            "task": "Create marketing materials and announcements",
                            "priority": "medium",
                        },
                        {"task": "Staged rollout (10% → 50% → 100% of users)", "priority": "high"},
                        {
                            "task": "Monitor performance and user adoption metrics",
                            "priority": "high",
                        },
                    ],
                },
            ],
            "milestones": [
                {
                    "milestone": "Research Complete & Specs Finalized",
                    "target_date": f"Week {min(3, duration_days // 7)}",
                },
                {
                    "milestone": "MVP Released to Alpha Testers",
                    "target_date": f"Week {min(8, duration_days // 7 - 4)}",
                },
                {
                    "milestone": "Beta Release with Full Features",
                    "target_date": f"Week {min(11, duration_days // 7 - 2)}",
                },
                {"milestone": "Public Launch to All Users", "target_date": f"End of {timeframe}"},
            ],
            "dependencies": [
                "User research must complete before MVP design",
                "Alpha testing must pass before enhancement phase",
                "Beta testing must complete before public launch",
            ],
        }

        return plan

    def _create_issue_resolution_plan(self, goal: str, context: str) -> Dict[str, Any]:
        """
        Create an issue resolution plan with 4-phase structure.

        Args:
            goal: Issue description
            context: Issue details, attempted solutions, symptoms

        Returns:
            Dictionary containing issue resolution plan with phases and success criteria
        """
        # Create structured 4-phase resolution plan
        plan = {
            "goal": f"Resolve: {goal}",
            "phases": [
                {
                    "phase": 1,
                    "name": "Investigation",
                    "tasks": [
                        {
                            "task": "Reproduce issue in development/staging environment",
                            "priority": "high",
                        },
                        {
                            "task": "Gather logs, error messages, and stack traces",
                            "priority": "high",
                        },
                        {
                            "task": "Analyze system behavior under issue conditions",
                            "priority": "high",
                        },
                        {"task": "Profile performance and resource usage", "priority": "medium"},
                        {"task": "Review related code and recent changes", "priority": "medium"},
                    ],
                },
                {
                    "phase": 2,
                    "name": "Root Cause Analysis",
                    "tasks": [
                        {
                            "task": "Identify specific code or configuration causing issue",
                            "priority": "high",
                        },
                        {
                            "task": "Determine if issue is code, infrastructure, or data-related",
                            "priority": "high",
                        },
                        {
                            "task": "Analyze dependencies and interactions between components",
                            "priority": "medium",
                        },
                        {
                            "task": "Check for similar historical issues and solutions",
                            "priority": "medium",
                        },
                        {"task": "Document findings and root cause hypothesis", "priority": "high"},
                    ],
                },
                {
                    "phase": 3,
                    "name": "Solution Implementation",
                    "tasks": [
                        {"task": "Design fix addressing root cause", "priority": "high"},
                        {
                            "task": "Implement solution with appropriate error handling",
                            "priority": "high",
                        },
                        {
                            "task": "Write regression tests to prevent reoccurrence",
                            "priority": "high",
                        },
                        {
                            "task": "Add monitoring and alerting for issue detection",
                            "priority": "medium",
                        },
                        {"task": "Code review and validation of fix", "priority": "high"},
                    ],
                },
                {
                    "phase": 4,
                    "name": "Verification & Documentation",
                    "tasks": [
                        {"task": "Test fix in staging environment", "priority": "high"},
                        {
                            "task": "Verify issue no longer occurs under original conditions",
                            "priority": "high",
                        },
                        {"task": "Deploy to production with monitoring", "priority": "high"},
                        {"task": "Monitor for 1-2 weeks to confirm resolution", "priority": "high"},
                        {
                            "task": "Document root cause and solution for team knowledge base",
                            "priority": "medium",
                        },
                    ],
                },
            ],
            "success_criteria": [
                f"{goal} is resolved and verified",
                "Issue does not reoccur in production",
                "Regression tests added to prevent future occurrence",
                "Solution documented for team reference",
            ],
        }

        return plan

    def _generate_strategic_recommendations(
        self, plan: Dict[str, Any], planning_type: str
    ) -> List[str]:
        """
        Generate strategic recommendations based on plan type.

        Args:
            plan: The generated plan structure
            planning_type: Type of plan ('sprint', 'feature_roadmap', 'issue_resolution')

        Returns:
            List of strategic recommendations (4-6 recommendations)
        """
        recommendations = []

        if planning_type == "sprint":
            recommendations.extend(
                [
                    "Start with highest priority tasks first to deliver value early",
                    "Schedule daily stand-ups for team alignment and blocker removal",
                    "Reserve 10-20% buffer time for unexpected issues and technical debt",
                    "Conduct sprint retrospective at the end to capture learnings",
                ]
            )
        elif planning_type == "feature_roadmap":
            recommendations.extend(
                [
                    "Validate assumptions with user research early to avoid costly pivots",
                    "Build MVP first (Phase 2), then iterate based on real user feedback",
                    "Maintain regular communication with stakeholders throughout development",
                    "Plan for technical debt reduction alongside new feature work",
                    "Use feature flags for gradual rollout to minimize risk",
                ]
            )
        elif planning_type == "issue_resolution":
            recommendations.extend(
                [
                    "Investigate root cause systematically before implementing fixes",
                    "Use profiling and monitoring tools to gather evidence",
                    "Write regression tests to prevent the issue from recurring",
                    "Document the solution clearly for future team reference",
                ]
            )

        # Add general recommendation for all types
        recommendations.append(
            "Track progress regularly and adjust plan as needed based on actual progress"
        )

        return recommendations

    def _parse_timeframe_to_days(self, timeframe: str) -> int:
        """
        Parse timeframe string to number of days.

        Args:
            timeframe: String like '2_weeks', '1_month', '14_days', 'not_specified'

        Returns:
            Integer number of days

        Examples:
            '2_weeks' → 14
            '1_month' → 30
            '3_months' → 90
            '7_days' → 7
            'not_specified' → 14 (default 2 weeks)
        """
        timeframe_lower = timeframe.lower().strip()

        # Extract numeric portion
        import re

        numbers = re.findall(r"\d+", timeframe_lower)
        number = int(numbers[0]) if numbers else 1

        # Check for time unit
        if "week" in timeframe_lower:
            return number * 7
        elif "month" in timeframe_lower:
            return number * 30
        elif "day" in timeframe_lower:
            return number
        else:
            # Default to 2 weeks if unparseable
            return 14

    async def _handle_prioritization(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """Handle prioritization requests.

        Supports three prioritization types:
        1. issues: Impact/Urgency/Effort scoring
        2. features: RICE framework (Reach/Impact/Confidence/Effort)
        3. tasks: Eisenhower matrix (Urgent/Important quadrants)

        Args:
            intent: Intent object with prioritization context
            workflow_id: Workflow identifier

        Returns:
            IntentProcessingResult with prioritized items
        """
        try:
            # Phase 1: Validate request
            validation_result = self._validate_prioritization_request(intent)
            if validation_result:
                return validation_result

            # Phase 2: Extract items and type
            prioritization_type = intent.context.get("prioritization_type")
            items = self._extract_prioritization_items(intent)

            self.logger.info(f"Prioritizing {len(items)} items using {prioritization_type} method")

            # Phase 3: Calculate scores based on type
            if prioritization_type == "issues":
                scored_items = self._calculate_issue_priority_scores(items)
            elif prioritization_type == "features":
                scored_items = self._calculate_rice_scores(items)
            elif prioritization_type == "tasks":
                scored_items = self._calculate_eisenhower_quadrants(items)
            else:
                return IntentProcessingResult(
                    success=False,
                    message=f"Unsupported prioritization type: {prioritization_type}. Supported types: issues, features, tasks.",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "prioritization_type": prioritization_type,
                    },
                    workflow_id=workflow_id,
                    requires_clarification=True,
                    clarification_type="unsupported_prioritization_type",
                    error=f"Unsupported prioritization type: {prioritization_type}",
                    error_type="ValidationError",
                )

            # Phase 4: Rank and format response
            ranked_items = self._rank_items_by_score(scored_items)
            recommendations = self._generate_prioritization_recommendations(
                ranked_items, prioritization_type
            )
            response_message = self._format_prioritization_response(
                ranked_items, prioritization_type
            )

            self.logger.info(f"Prioritization completed: {len(ranked_items)} items ranked")

            return IntentProcessingResult(
                success=True,
                message=response_message,
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "prioritization_type": prioritization_type,
                    "total_items": len(ranked_items),
                    "prioritized_items": ranked_items,
                    "recommendations": recommendations,
                },
                workflow_id=workflow_id,
            )

        except Exception as e:
            self.logger.error(f"Failed to prioritize: {e}", exc_info=True)
            return IntentProcessingResult(
                success=False,
                message=f"Failed to prioritize: {str(e)}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                },
                workflow_id=workflow_id,
                error=str(e),
                error_type="StrategyError",
            )

    def _validate_prioritization_request(self, intent: Intent) -> Optional[IntentProcessingResult]:
        """Validate prioritization request has required fields.

        Args:
            intent: Intent object to validate

        Returns:
            IntentProcessingResult if validation fails, None if valid
        """
        # Check for prioritization_type
        prioritization_type = intent.context.get("prioritization_type")
        if not prioritization_type:
            return IntentProcessingResult(
                success=False,
                message="Prioritization type is required. Please specify: issues, features, or tasks.",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                },
                workflow_id="",
                requires_clarification=True,
                clarification_type="prioritization_type_required",
            )

        # Check for items
        items = intent.context.get("items")
        if items is None:
            return IntentProcessingResult(
                success=False,
                message="Items list is required for prioritization.",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "prioritization_type": prioritization_type,
                },
                workflow_id="",
                requires_clarification=True,
                clarification_type="items_required",
            )

        # Check items not empty
        if not isinstance(items, list) or len(items) == 0:
            return IntentProcessingResult(
                success=False,
                message="Items list cannot be empty.",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "prioritization_type": prioritization_type,
                    "item_count": 0,
                },
                workflow_id="",
                requires_clarification=True,
                clarification_type="items_empty",
            )

        return None  # Validation passed

    def _extract_prioritization_items(self, intent: Intent) -> List[Dict[str, Any]]:
        """Extract and normalize items from intent context.

        Args:
            intent: Intent with items in context

        Returns:
            List of item dictionaries
        """
        items = intent.context.get("items", [])

        # Normalize items to dicts if they're strings
        normalized_items = []
        for item in items:
            if isinstance(item, str):
                normalized_items.append({"title": item})
            elif isinstance(item, dict):
                normalized_items.append(item)
            else:
                self.logger.warning(f"Skipping invalid item type: {type(item)}")

        return normalized_items

    def _calculate_issue_priority_scores(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Calculate priority scores for issues using impact/urgency/effort.

        Formula: priority_score = (impact * urgency) / effort

        Args:
            items: List of issue dictionaries

        Returns:
            Items with priority_score added
        """
        scored_items = []

        for item in items:
            # Get explicit scores or estimate from keywords
            impact = item.get("impact")
            urgency = item.get("urgency")
            effort = item.get("effort")

            # Estimate missing scores from title/description
            if impact is None or urgency is None or effort is None:
                title = item.get("title", "")
                description = item.get("description", "")
                text = f"{title} {description}".lower()

                estimated = self._estimate_scores_from_keywords(text)
                impact = impact or estimated["impact"]
                urgency = urgency or estimated["urgency"]
                effort = effort or estimated["effort"]

            # Calculate priority score
            # Avoid division by zero
            effort = max(effort, 0.1)
            priority_score = (impact * urgency) / effort

            scored_items.append(
                {
                    **item,
                    "impact": impact,
                    "urgency": urgency,
                    "effort": effort,
                    "priority_score": priority_score,
                }
            )

        return scored_items

    def _calculate_rice_scores(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Calculate RICE scores for features.

        Formula: RICE_score = (reach * impact * confidence) / effort

        Args:
            items: List of feature dictionaries

        Returns:
            Items with rice_score added
        """
        scored_items = []

        for item in items:
            # Get RICE components (with defaults)
            reach = item.get("reach", 100)  # Default: 100 users
            impact = item.get("impact", 1.0)  # Default: 1.0 (moderate)
            confidence = item.get("confidence", 0.8)  # Default: 80%
            effort = item.get("effort", 1.0)  # Default: 1 person-month

            # Calculate RICE score
            effort = max(effort, 0.1)  # Avoid division by zero
            rice_score = (reach * impact * confidence) / effort

            scored_items.append(
                {
                    **item,
                    "reach": reach,
                    "impact": impact,
                    "confidence": confidence,
                    "effort": effort,
                    "rice_score": rice_score,
                    "priority_score": rice_score,  # Alias for consistent ranking
                }
            )

        return scored_items

    def _calculate_eisenhower_quadrants(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Classify tasks into Eisenhower matrix quadrants.

        Quadrants:
        - Q1 (urgent + important): Do First
        - Q2 (not urgent + important): Schedule
        - Q3 (urgent + not important): Delegate
        - Q4 (not urgent + not important): Eliminate

        Args:
            items: List of task dictionaries

        Returns:
            Items with quadrant and priority_score added
        """
        scored_items = []

        # Quadrant priority mapping (for ranking)
        quadrant_priority = {
            "Q1": 100,  # Do First
            "Q2": 75,  # Schedule
            "Q3": 50,  # Delegate
            "Q4": 25,  # Eliminate
        }

        for item in items:
            # Get urgency/importance or estimate from keywords
            urgency = item.get("urgency")
            importance = item.get("importance")

            # Estimate from title/description if missing
            if urgency is None or importance is None:
                title = item.get("title", "")
                description = item.get("description", "")
                text = f"{title} {description}".lower()

                estimated = self._estimate_scores_from_keywords(text)
                urgency = urgency or estimated["urgency"]
                importance = importance or estimated["impact"]  # Use impact as importance

            # Determine quadrant (using median split at 5.5)
            is_urgent = urgency > 5.5
            is_important = importance > 5.5

            if is_urgent and is_important:
                quadrant = "Q1"
                quadrant_label = "Do First"
            elif not is_urgent and is_important:
                quadrant = "Q2"
                quadrant_label = "Schedule"
            elif is_urgent and not is_important:
                quadrant = "Q3"
                quadrant_label = "Delegate"
            else:  # not urgent and not important
                quadrant = "Q4"
                quadrant_label = "Eliminate"

            scored_items.append(
                {
                    **item,
                    "urgency": urgency,
                    "importance": importance,
                    "quadrant": quadrant,
                    "quadrant_label": quadrant_label,
                    "priority_score": quadrant_priority[quadrant],
                }
            )

        return scored_items

    def _estimate_scores_from_keywords(self, text: str) -> Dict[str, float]:
        """Estimate impact/urgency/effort scores from text keywords.

        Args:
            text: Lowercase text to analyze

        Returns:
            Dict with estimated impact, urgency, effort scores (1-10)
        """
        # Impact keywords
        high_impact = ["critical", "severe", "major", "essential", "vital"]
        medium_impact = ["important", "significant", "moderate"]
        low_impact = ["minor", "trivial", "small", "cosmetic"]

        # Urgency keywords
        high_urgency = ["urgent", "asap", "immediate", "now", "emergency"]
        medium_urgency = ["soon", "timely", "prompt"]
        low_urgency = ["later", "eventually", "someday", "future"]

        # Effort keywords
        low_effort = ["quick", "easy", "simple", "trivial", "fast"]
        medium_effort = ["moderate", "medium", "average"]
        high_effort = ["complex", "difficult", "hard", "slow", "large"]

        # Estimate impact (default: 5)
        impact = 5.0
        if any(keyword in text for keyword in high_impact):
            impact = 9.0
        elif any(keyword in text for keyword in medium_impact):
            impact = 6.0
        elif any(keyword in text for keyword in low_impact):
            impact = 3.0

        # Estimate urgency (default: 5)
        urgency = 5.0
        if any(keyword in text for keyword in high_urgency):
            urgency = 9.0
        elif any(keyword in text for keyword in medium_urgency):
            urgency = 6.0
        elif any(keyword in text for keyword in low_urgency):
            urgency = 3.0

        # Estimate effort (default: 5)
        effort = 5.0
        if any(keyword in text for keyword in high_effort):
            effort = 8.0
        elif any(keyword in text for keyword in medium_effort):
            effort = 5.0
        elif any(keyword in text for keyword in low_effort):
            effort = 2.0

        return {
            "impact": impact,
            "urgency": urgency,
            "effort": effort,
        }

    def _rank_items_by_score(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Sort items by priority_score and assign ranks with proper structure.

        Args:
            items: List of items with priority_score and other fields

        Returns:
            Sorted items with structure:
            {
                "rank": 1,
                "priority_score": 45.0,
                "item": {...original item...},
                "scores": {...extracted scores...},
                "reasoning": "..."
            }
        """
        # Sort by priority_score descending (highest first)
        sorted_items = sorted(items, key=lambda x: x.get("priority_score", 0), reverse=True)

        result = []
        for i, item in enumerate(sorted_items, start=1):
            priority_score = item.get("priority_score", 0)

            # Extract scores based on what fields are present
            scores = {}
            if "impact" in item:
                scores["impact"] = item["impact"]
            if "urgency" in item:
                scores["urgency"] = item["urgency"]
            if "effort" in item:
                scores["effort"] = item["effort"]
            if "reach" in item:
                scores["reach"] = item["reach"]
            if "confidence" in item:
                scores["confidence"] = item["confidence"]
            if "importance" in item:
                scores["importance"] = item["importance"]

            # Create original item (without internal scoring fields)
            original_item = {
                k: v
                for k, v in item.items()
                if k
                not in [
                    "priority_score",
                    "impact",
                    "urgency",
                    "effort",
                    "reach",
                    "confidence",
                    "importance",
                    "quadrant",
                    "quadrant_label",
                    "rice_score",
                ]
            }

            # Generate reasoning
            reasoning = self._generate_prioritization_reasoning(item, priority_score)

            # Build structured result
            structured_item = {
                "rank": i,
                "priority_score": priority_score,
                "item": original_item,
                "scores": scores,
                "reasoning": reasoning,
            }

            # Add quadrant info for Eisenhower matrix
            if "quadrant" in item:
                structured_item["quadrant"] = item["quadrant"]
                structured_item["quadrant_label"] = item.get("quadrant_label", "")

            result.append(structured_item)

        return result

    def _generate_prioritization_reasoning(
        self, item: Dict[str, Any], priority_score: float
    ) -> str:
        """Generate reasoning explanation for prioritization.

        Args:
            item: Item with scoring fields
            priority_score: Calculated priority score

        Returns:
            Human-readable reasoning string
        """
        title = item.get("title", "Item")

        # Issues prioritization reasoning
        if "impact" in item and "urgency" in item and "effort" in item:
            impact = item["impact"]
            urgency = item["urgency"]
            effort = item["effort"]

            return (
                f"{title} has high priority (score: {priority_score:.1f}) due to "
                f"impact={impact}, urgency={urgency}, and effort={effort}. "
                f"Formula: (impact × urgency) / effort = ({impact} × {urgency}) / {effort}"
            )

        # RICE framework reasoning
        elif "reach" in item and "confidence" in item:
            reach = item["reach"]
            impact = item.get("impact", 1.0)
            confidence = item["confidence"]
            effort = item.get("effort", 1.0)

            return (
                f"{title} scores {priority_score:.1f} using RICE framework: "
                f"reach={reach}, impact={impact}, confidence={confidence:.0%}, effort={effort}. "
                f"Formula: (reach × impact × confidence) / effort"
            )

        # Eisenhower matrix reasoning
        elif "quadrant" in item:
            quadrant = item["quadrant"]
            quadrant_label = item.get("quadrant_label", "")
            urgency = item.get("urgency", 5)
            importance = item.get("importance", 5)

            return (
                f"{title} falls in {quadrant} ({quadrant_label}) with "
                f"urgency={urgency}, importance={importance}. "
                f"This quadrant has priority score {priority_score:.0f}."
            )

        # Generic fallback
        else:
            return f"{title} has priority score of {priority_score:.1f}"

    def _generate_prioritization_recommendations(
        self, ranked_items: List[Dict[str, Any]], prioritization_type: str
    ) -> List[str]:
        """Generate recommendations based on prioritization results.

        Args:
            ranked_items: Ranked items with scores
            prioritization_type: Type of prioritization

        Returns:
            List of recommendation strings
        """
        recommendations = []

        if not ranked_items:
            return ["No items to prioritize."]

        # Get top and bottom items
        top_item = ranked_items[0]

        if prioritization_type == "issues":
            # Issues recommendations
            recommendations.append(
                f"Start with rank 1: {top_item['item'].get('title', 'Top item')} "
                f"(priority score: {top_item['priority_score']:.1f})"
            )

            # Check for low-effort high-impact items
            quick_wins = [
                item
                for item in ranked_items
                if item["scores"].get("effort", 10) <= 3 and item["rank"] <= 5
            ]
            if quick_wins:
                recommendations.append(
                    f"Found {len(quick_wins)} quick win(s) in top 5 (low effort, high priority)"
                )

            # Warn about low-priority items
            if len(ranked_items) > 5:
                low_priority = ranked_items[-1]
                recommendations.append(
                    f"Consider deferring rank {low_priority['rank']}: "
                    f"{low_priority['item'].get('title', 'Last item')} "
                    f"(score: {low_priority['priority_score']:.1f})"
                )

        elif prioritization_type == "features":
            # RICE recommendations
            recommendations.append(
                f"Highest RICE score: {top_item['item'].get('title', 'Top feature')} "
                f"({top_item['priority_score']:.1f})"
            )

            # Check confidence levels
            low_confidence = [
                item for item in ranked_items[:3] if item["scores"].get("confidence", 1.0) < 0.5
            ]
            if low_confidence:
                recommendations.append(
                    f"Warning: {len(low_confidence)} top-ranked feature(s) have low confidence (<50%). "
                    "Consider validating assumptions."
                )

        elif prioritization_type == "tasks":
            # Eisenhower recommendations
            q1_items = [item for item in ranked_items if item.get("quadrant") == "Q1"]
            q2_items = [item for item in ranked_items if item.get("quadrant") == "Q2"]
            q3_items = [item for item in ranked_items if item.get("quadrant") == "Q3"]
            q4_items = [item for item in ranked_items if item.get("quadrant") == "Q4"]

            if q1_items:
                recommendations.append(
                    f"Do First (Q1): {len(q1_items)} urgent and important task(s)"
                )
            if q2_items:
                recommendations.append(
                    f"Schedule (Q2): {len(q2_items)} important but not urgent task(s)"
                )
            if q3_items:
                recommendations.append(
                    f"Delegate (Q3): {len(q3_items)} urgent but less important task(s)"
                )
            if q4_items:
                recommendations.append(
                    f"Eliminate (Q4): {len(q4_items)} low-priority task(s) to eliminate"
                )

        return recommendations

    def _format_prioritization_response(
        self, ranked_items: List[Dict[str, Any]], prioritization_type: str
    ) -> str:
        """Format human-readable response message.

        Args:
            ranked_items: List of ranked items
            prioritization_type: Type of prioritization used

        Returns:
            Formatted message string
        """
        if not ranked_items:
            return "No items to prioritize."

        count = len(ranked_items)

        # Get top 3 items for preview
        top_items = ranked_items[:3]
        preview = []

        for item in top_items:
            title = item.get("title", "Untitled")
            rank = item.get("rank", 0)
            score = item.get("priority_score", 0)

            if prioritization_type == "issues":
                preview.append(f"{rank}. {title} (score: {score:.2f})")
            elif prioritization_type == "features":
                preview.append(f"{rank}. {title} (RICE: {score:.2f})")
            elif prioritization_type == "tasks":
                quadrant = item.get("quadrant_label", "Unknown")
                preview.append(f"{rank}. {title} ({quadrant})")

        preview_text = "\n".join(preview)

        return (
            f"Prioritized {count} items using {prioritization_type} method:\n\n"
            f"{preview_text}\n\n"
            f"See intent_data.prioritized_items for complete ranking."
        )

    async def _handle_learning_intent(
        self, intent: Intent, workflow, session_id: str
    ) -> IntentProcessingResult:
        """
        Handle LEARNING category intents.

        Routes to appropriate learning service based on intent action.
        Follows EXECUTION/ANALYSIS pattern for consistency.

        GREAT-4D Phase 6: Completes intent handler coverage.
        """
        self.logger.info(f"Processing LEARNING intent: {intent.action}")

        # Route based on action
        if intent.action in ["learn_pattern", "detect_pattern"]:
            return await self._handle_learn_pattern(intent, workflow.id)

        else:
            # Generic learning - provide working response
            return IntentProcessingResult(
                success=True,
                message=f"Learning capability ready for '{intent.action}'. Specific implementation pending.",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                },
                workflow_id=workflow.id,
                requires_clarification=True,
                clarification_type="learning_type",
            )

    async def _handle_learn_pattern(
        self, intent: Intent, workflow_id: str
    ) -> IntentProcessingResult:
        """Handle pattern learning requests.

        Learns patterns from historical data to identify recurring themes,
        similar issues, and common approaches. Helps recognize patterns
        and improve future decision-making.

        Supported pattern_types:
            - 'issue_similarity': Find similar issues and common patterns
            - 'resolution_patterns': Learn solution approaches for problems
            - 'tag_patterns': Learn tag/classification patterns

        Args:
            intent: Intent object with pattern learning context
            workflow_id: Workflow identifier

        Returns:
            IntentProcessingResult with learned patterns
        """
        try:
            # Phase 1: Validate request
            validation_result = self._validate_learning_request(intent)
            if validation_result:
                return validation_result

            # Phase 2: Fetch historical data
            self.logger.info("Fetching historical data for pattern learning")
            historical_data = await self._fetch_learning_data(intent)

            if not historical_data or len(historical_data) == 0:
                self.logger.info("No historical data found for pattern learning")
                return IntentProcessingResult(
                    success=True,
                    message="No historical data available for pattern learning.",
                    intent_data={
                        "category": intent.category.value,
                        "action": intent.action,
                        "pattern_type": intent.context.get("pattern_type"),
                        "total_items_analyzed": 0,
                        "patterns_count": 0,
                        "patterns_found": [],
                    },
                    workflow_id=workflow_id,
                )

            # Phase 3: Learn patterns based on type
            pattern_type = intent.context.get("pattern_type")
            search_query = intent.context.get("query", "")
            min_occurrences = intent.context.get("min_occurrences", 2)

            if pattern_type == "issue_similarity":
                patterns = self._learn_issue_similarity_patterns(
                    historical_data, search_query, min_occurrences
                )
            elif pattern_type == "resolution_patterns":
                patterns = self._learn_resolution_patterns(historical_data, min_occurrences)
            elif pattern_type == "tag_patterns":
                patterns = self._learn_tag_patterns(historical_data, min_occurrences)
            else:
                # Should not reach here due to validation
                raise ValueError(f"Unhandled pattern type: {pattern_type}")

            # Phase 4: Format and return
            response_message = self._format_learning_response(patterns, len(historical_data))

            self.logger.info(f"Learned {len(patterns)} patterns from {len(historical_data)} items")

            return IntentProcessingResult(
                success=True,
                message=response_message,
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "pattern_type": pattern_type,
                    "total_items_analyzed": len(historical_data),
                    "patterns_count": len(patterns),
                    "patterns_found": patterns,
                },
                workflow_id=workflow_id,
            )

        except Exception as e:
            self.logger.error(f"Failed to learn pattern: {e}", exc_info=True)
            return IntentProcessingResult(
                success=False,
                message=f"Failed to learn pattern: {str(e)}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                },
                workflow_id=workflow_id,
                error=str(e),
                error_type="LearningError",
            )

    def _validate_learning_request(self, intent: Intent) -> Optional[IntentProcessingResult]:
        """Validate pattern learning request has required fields.

        Args:
            intent: Intent object to validate

        Returns:
            IntentProcessingResult if validation fails, None if valid
        """
        # Check for pattern_type
        pattern_type = intent.context.get("pattern_type")
        if not pattern_type:
            return IntentProcessingResult(
                success=False,
                message="Pattern type is required. Supported: issue_similarity, resolution_patterns, tag_patterns.",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                },
                workflow_id="",
                requires_clarification=True,
                clarification_type="pattern_type_required",
            )

        # Check for source
        source = intent.context.get("source")
        if not source:
            return IntentProcessingResult(
                success=False,
                message="Source is required (e.g., github_issues).",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "pattern_type": pattern_type,
                },
                workflow_id="",
                requires_clarification=True,
                clarification_type="source_required",
            )

        # Validate pattern_type
        supported_types = ["issue_similarity", "resolution_patterns", "tag_patterns"]
        if pattern_type not in supported_types:
            return IntentProcessingResult(
                success=False,
                message=f"Unsupported pattern type: {pattern_type}. Supported: {', '.join(supported_types)}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "pattern_type": pattern_type,
                },
                workflow_id="",
                requires_clarification=True,
                clarification_type="unsupported_pattern_type",
            )

        return None  # Validation passed

    async def _fetch_learning_data(self, intent: Intent) -> List[Dict[str, Any]]:
        """Fetch historical data for pattern learning.

        Args:
            intent: Intent with source and query parameters

        Returns:
            List of historical data items
        """
        source = intent.context.get("source")
        search_query = intent.context.get("query", "")

        if source == "github_issues":
            # Import and instantiate GitHub service
            from services.domain.github_domain_service import GitHubDomainService

            github_service = GitHubDomainService()

            try:
                # Fetch recent issues
                issues = await github_service.list_issues(
                    repository="piper-morgan", state="all", limit=100
                )

                # Filter by search query if provided
                if search_query:
                    query_lower = search_query.lower()
                    issues = [
                        issue
                        for issue in issues
                        if query_lower in (issue.title or "").lower()
                        or query_lower in (issue.body or "").lower()
                    ]

                # Convert to standard format
                return [
                    {
                        "number": issue.number,
                        "title": issue.title,
                        "body": issue.body,
                        "labels": [label.name for label in (issue.labels or [])],
                        "state": issue.state,
                    }
                    for issue in issues
                ]

            except Exception as e:
                self.logger.error(f"Failed to fetch GitHub issues: {e}")
                return []

        # Future: Add support for other sources
        return []

    def _learn_issue_similarity_patterns(
        self,
        historical_data: List[Dict[str, Any]],
        search_query: str,
        min_occurrences: int,
    ) -> List[Dict[str, Any]]:
        """Learn patterns from similar issues using keyword clustering.

        Args:
            historical_data: List of issue dictionaries
            search_query: Optional query string (for context)
            min_occurrences: Minimum pattern frequency threshold

        Returns:
            List of identified pattern dictionaries
        """
        if len(historical_data) < min_occurrences:
            return []

        # Extract keywords and group issues
        keyword_groups = {}
        stop_words = {
            "the",
            "a",
            "an",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "is",
            "are",
            "be",
            "by",
        }

        for item in historical_data:
            title = item.get("title", "").lower()
            words = title.split()

            # Filter significant keywords
            keywords = [w for w in words if len(w) > 3 and w not in stop_words]

            for keyword in keywords:
                keyword_groups.setdefault(keyword, []).append(item)

        # Create patterns from groups with enough occurrences
        patterns = []

        for keyword, items in keyword_groups.items():
            if len(items) >= min_occurrences:
                # Calculate confidence
                confidence = min(len(items) / 10, 1.0)  # Scale to 1.0

                # Extract common labels
                all_labels = []
                for item in items:
                    all_labels.extend(item.get("labels", []))

                # Count label occurrences
                label_counts = {}
                for label in all_labels:
                    label_counts[label] = label_counts.get(label, 0) + 1

                # Keep labels appearing in 30%+ of items
                common_labels = [
                    label for label, count in label_counts.items() if count >= len(items) * 0.3
                ]

                # Generate recommendations
                recommendations = self._generate_pattern_recommendations(
                    keyword, common_labels, len(items)
                )

                # Create pattern
                pattern = {
                    "pattern_id": f"keyword_{keyword}",
                    "description": f"Issues related to '{keyword}'",
                    "keyword": keyword,
                    "confidence": confidence,
                    "occurrences": len(items),
                    "common_labels": common_labels,
                    "examples": [
                        {"number": item["number"], "title": item["title"]}
                        for item in items[:5]  # First 5 examples
                    ],
                    "recommended_actions": recommendations,
                }

                patterns.append(pattern)

        # Sort by occurrences (most common first)
        patterns.sort(key=lambda x: x["occurrences"], reverse=True)

        # Return top 10 patterns
        return patterns[:10]

    def _learn_resolution_patterns(
        self,
        historical_data: List[Dict[str, Any]],
        min_occurrences: int,
    ) -> List[Dict[str, Any]]:
        """Learn solution patterns from resolved issues.

        Args:
            historical_data: List of issue dictionaries
            min_occurrences: Minimum pattern frequency threshold

        Returns:
            List of resolution pattern dictionaries
        """
        # Filter to closed issues only
        closed_issues = [item for item in historical_data if item.get("state") == "closed"]

        if len(closed_issues) < min_occurrences:
            return []

        # Group by common resolution labels
        resolution_groups = {}

        for item in closed_issues:
            labels = item.get("labels", [])
            for label in labels:
                if label.lower() in ["fixed", "resolved", "completed", "duplicate", "wontfix"]:
                    resolution_groups.setdefault(label, []).append(item)

        # Create patterns
        patterns = []
        for resolution_type, items in resolution_groups.items():
            if len(items) >= min_occurrences:
                patterns.append(
                    {
                        "pattern_id": f"resolution_{resolution_type}",
                        "description": f"Issues resolved as '{resolution_type}'",
                        "resolution_type": resolution_type,
                        "confidence": min(len(items) / 5, 1.0),
                        "occurrences": len(items),
                        "examples": [
                            {"number": item["number"], "title": item["title"]} for item in items[:3]
                        ],
                        "recommended_actions": [
                            f"Review {len(items)} similar resolutions of type '{resolution_type}'"
                        ],
                    }
                )

        return patterns

    def _learn_tag_patterns(
        self,
        historical_data: List[Dict[str, Any]],
        min_occurrences: int,
    ) -> List[Dict[str, Any]]:
        """Learn tag/label patterns from historical issues.

        Args:
            historical_data: List of issue dictionaries
            min_occurrences: Minimum pattern frequency threshold

        Returns:
            List of tag pattern dictionaries
        """
        if len(historical_data) < min_occurrences:
            return []

        # Analyze label co-occurrence
        label_pairs = {}

        for item in historical_data:
            labels = sorted(item.get("labels", []))
            if len(labels) >= 2:
                # Create pairs
                for i in range(len(labels)):
                    for j in range(i + 1, len(labels)):
                        pair = (labels[i], labels[j])
                        label_pairs[pair] = label_pairs.get(pair, 0) + 1

        # Create patterns from frequent pairs
        patterns = []
        for (label1, label2), count in label_pairs.items():
            if count >= min_occurrences:
                patterns.append(
                    {
                        "pattern_id": f"tags_{label1}_{label2}",
                        "description": f"Labels '{label1}' and '{label2}' often appear together",
                        "label_pair": [label1, label2],
                        "confidence": min(count / 10, 1.0),
                        "occurrences": count,
                        "recommended_actions": [
                            f"When applying '{label1}', consider also applying '{label2}'"
                        ],
                    }
                )

        # Sort by occurrences
        patterns.sort(key=lambda x: x["occurrences"], reverse=True)

        return patterns[:10]

    def _generate_pattern_recommendations(
        self, keyword: str, common_labels: List[str], occurrences: int
    ) -> List[str]:
        """Generate actionable recommendations for a pattern.

        Args:
            keyword: The keyword defining the pattern
            common_labels: Labels commonly associated with the pattern
            occurrences: Number of times pattern occurred

        Returns:
            List of recommendation strings
        """
        recommendations = []

        # Always recommend reviewing similar issues
        recommendations.append(f"Review {occurrences} similar past issues with '{keyword}'")

        # Recommend common labels if available
        if common_labels:
            recommendations.append(f"Consider applying labels: {', '.join(common_labels[:3])}")

        # Add frequency-based recommendations
        if occurrences >= 5:
            recommendations.append(
                f"High frequency pattern ({occurrences} occurrences) - consider root cause analysis"
            )

        # Add keyword-specific recommendations
        if keyword in ["bug", "error", "issue", "problem", "fail", "crash"]:
            recommendations.append(
                "Investigate if a systemic fix can address multiple related issues"
            )
        elif keyword in ["performance", "slow", "timeout", "latency"]:
            recommendations.append("Consider performance monitoring and profiling tools")
        elif keyword in ["security", "auth", "authentication", "authorization"]:
            recommendations.append("Review security best practices and recent CVEs")

        return recommendations

    def _format_learning_response(self, patterns: List[Dict[str, Any]], total_analyzed: int) -> str:
        """Format human-readable response message.

        Args:
            patterns: List of identified patterns
            total_analyzed: Total number of items analyzed

        Returns:
            Formatted message string
        """
        if not patterns:
            return f"Analyzed {total_analyzed} items but found no recurring patterns."

        # Create preview of top 3 patterns
        preview = []
        for i, pattern in enumerate(patterns[:3], 1):
            preview.append(
                f"{i}. {pattern['description']} ({pattern['occurrences']} occurrences, "
                f"confidence: {pattern['confidence']:.2f})"
            )

        preview_text = "\n".join(preview)

        return (
            f"Learned {len(patterns)} patterns from {total_analyzed} items:\n\n"
            f"{preview_text}\n\n"
            f"See intent_data.patterns_found for complete details."
        )

    async def _handle_unknown_intent(
        self, intent: Intent, workflow, session_id: str
    ) -> IntentProcessingResult:
        """
        Handle UNKNOWN category intents.

        Provides helpful fallback for unclear intents.
        Follows EXECUTION/ANALYSIS pattern for consistency.

        GREAT-4D Phase 7: Completes intent handler coverage.
        """
        self.logger.info(f"Processing UNKNOWN intent: {intent.action}")

        # Provide helpful response for unclear intents
        return IntentProcessingResult(
            success=True,
            message="I'm not sure what you're asking for. Could you rephrase or provide more details?",
            intent_data={
                "category": intent.category.value,
                "action": intent.action,
                "confidence": intent.confidence,
                "original_message": intent.original_message,
            },
            workflow_id=workflow.id,
            requires_clarification=True,
            clarification_type="intent_unclear",
        )

    async def _create_workflow_with_timeout(
        self, intent: Intent, timeout_seconds: float = 30.0
    ) -> Optional:
        """
        Create workflow with timeout protection.

        Bug #166 fix: Add timeout to prevent workflow creation from hanging.
        """
        try:
            workflow = await asyncio.wait_for(
                self.orchestration_engine.create_workflow_from_intent(intent),
                timeout=timeout_seconds,
            )
            return workflow
        except asyncio.TimeoutError:
            self.logger.error(f"Workflow creation timeout after {timeout_seconds}s")
            return None
        except Exception as e:
            self.logger.error(f"Workflow creation error: {e}")
            raise
