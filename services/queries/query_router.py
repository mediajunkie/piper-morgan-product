"""
Query Router - Routes QUERY intents to appropriate query services
"""

import logging
import random
import time
from typing import Any, Dict, List, Optional

from services.domain.models import Intent
from services.intent_service.llm_classifier import LLMIntentClassifier
from services.knowledge.knowledge_graph_service import KnowledgeGraphService
from services.knowledge.semantic_indexing_service import SemanticIndexingService
from services.queries.conversation_queries import ConversationQueryService
from services.queries.degradation import QueryDegradationHandler
from services.queries.file_queries import FileQueryService
from services.queries.project_queries import ProjectQueryService
from services.shared_types import IntentCategory

# GitHub integration with deprecation support (PM-033b-deprecation)
try:
    from services.integrations.github.github_integration_router import GitHubIntegrationRouter

    GITHUB_ROUTER_AVAILABLE = True
except ImportError:
    GITHUB_ROUTER_AVAILABLE = False

# MCP Consumer integration
try:
    from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter

    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False

logger = logging.getLogger(__name__)


class QueryRouter:
    """Routes QUERY intents to appropriate query services with LLM enhancement"""

    def __init__(
        self,
        project_query_service: ProjectQueryService,
        conversation_query_service: ConversationQueryService,
        file_query_service: FileQueryService,
        test_mode: bool = False,
        degradation_config: Optional[Dict] = None,
        # PM-034 Phase 2B: LLM Intent Classification Integration
        llm_classifier: Optional[LLMIntentClassifier] = None,
        knowledge_graph_service: Optional[KnowledgeGraphService] = None,
        semantic_indexing_service: Optional[SemanticIndexingService] = None,
        enable_llm_classification: bool = False,
        llm_rollout_percentage: float = 0.0,  # 0.0 = 0%, 1.0 = 100%
        performance_targets: Optional[Dict[str, float]] = None,
        # MCP Consumer integration
        github_adapter: Optional["GitHubMCPSpatialAdapter"] = None,
        enable_mcp_federation: bool = True,
        # GitHub integration with deprecation support (PM-033b-deprecation)
        github_router: Optional["GitHubIntegrationRouter"] = None,
    ):
        self.project_queries = project_query_service
        self.conversation_queries = conversation_query_service
        self.file_queries = file_query_service
        self.test_mode = test_mode  # PM-063: Backward compatibility with existing test_mode
        self.degradation_handler = QueryDegradationHandler(
            degradation_config
        )  # PM-063: Comprehensive degradation framework

        # PM-034 Phase 2B: LLM Intent Classification Integration
        self.llm_classifier = llm_classifier
        self.knowledge_graph_service = knowledge_graph_service
        self.semantic_indexing_service = semantic_indexing_service
        self.enable_llm_classification = enable_llm_classification
        self.llm_rollout_percentage = llm_rollout_percentage

        # Performance targets (in milliseconds)
        self.performance_targets = performance_targets or {
            "rule_based": 50.0,  # <50ms for rule-based classification
            "llm_classification": 200.0,  # <200ms for LLM classification
        }

        # Performance monitoring
        self.performance_metrics = {
            "total_requests": 0,
            "llm_classifications": 0,
            "rule_based_classifications": 0,
            "llm_success_rate": 0.0,
            "rule_based_success_rate": 0.0,
            "average_llm_latency_ms": 0.0,
            "average_rule_based_latency_ms": 0.0,
            "target_violations": 0,
        }

        # MCP Consumer integration
        self.github_adapter = None
        self.enable_mcp_federation = enable_mcp_federation and MCP_AVAILABLE

        # GitHub integration with deprecation support (PM-033b-deprecation)
        self.github_router = None
        if GITHUB_ROUTER_AVAILABLE:
            self.github_router = github_router or GitHubIntegrationRouter()
            logger.info("GitHub integration router enabled with deprecation support")

        if self.enable_mcp_federation and MCP_AVAILABLE:
            self.github_adapter = github_adapter or GitHubMCPSpatialAdapter()
            logger.info("MCP federation enabled in QueryRouter")

    async def route_query(self, intent: Intent) -> Any:
        """Route an intent to the appropriate query service with graceful degradation"""
        # Support all intent categories for canonical queries (UX Quick Win - Phase 3)
        if intent.category not in [
            IntentCategory.QUERY,
            IntentCategory.IDENTITY,
            IntentCategory.TEMPORAL,
            IntentCategory.STATUS,
            IntentCategory.PRIORITY,
            IntentCategory.GUIDANCE,
        ]:
            raise ValueError(f"QueryRouter cannot handle intent category: {intent.category}")

        # PM-063: Comprehensive degradation handling
        try:
            return await self._route_query_with_protection(intent)
        except (ValueError, ImportError) as e:
            # Re-raise ValueError and ImportError - these should not be degraded
            raise
        except Exception as e:
            logger.error(f"Query routing failed for action {intent.action}: {e}")
            # Determine service and apply appropriate degradation
            service = self._get_service_for_action(intent.action)
            return await self.degradation_handler.handle_service_failure(service, intent.action, e)

    async def classify_and_route(
        self,
        message: str,
        user_context: Optional[Dict[str, Any]] = None,
        session_id: Optional[str] = None,
        conversation_manager=None,  # PM-034 Phase 3: ConversationManager integration
    ) -> Any:
        """
        PM-034 Phase 2B/3: Classify message and route to appropriate service with conversation context

        This method provides the enhanced classification and routing pipeline
        with A/B testing, performance monitoring, and anaphoric reference resolution.
        """
        start_time = time.time()
        self.performance_metrics["total_requests"] += 1

        try:
            # PM-034 Phase 3: Resolve anaphoric references if ConversationManager available
            resolved_message = message
            resolved_references = []

            if conversation_manager and session_id:
                try:
                    (
                        resolved_message,
                        resolved_references,
                    ) = await conversation_manager.resolve_references_in_message(
                        message, session_id
                    )
                    if resolved_references:
                        logger.info(
                            "References resolved in query",
                            session_id=session_id,
                            original=message,
                            resolved=resolved_message,
                            reference_count=len(resolved_references),
                        )
                except Exception as e:
                    logger.warning(f"Reference resolution failed, using original message: {e}")
                    resolved_message = message  # Graceful degradation

            # Determine classification method based on rollout percentage
            use_llm = self._should_use_llm_classification(session_id)

            if use_llm and self.enable_llm_classification and self.llm_classifier:
                # Use LLM classification with resolved message
                result = await self._classify_and_route_with_llm(
                    resolved_message, user_context, session_id, start_time
                )
            else:
                # Use rule-based classification (fast path) with resolved message
                result = await self._classify_and_route_rule_based(
                    resolved_message, user_context, session_id, start_time
                )

            # PM-034 Phase 3: Enhance result with conversation context if references were resolved
            if resolved_references:
                conversation_context = {
                    "original_message": message,
                    "resolved_message": resolved_message,
                    "resolved_references": [
                        {
                            "original": ref.original_text,
                            "resolved": ref.resolved_entity,
                            "type": ref.entity_type,
                            "confidence": ref.confidence,
                        }
                        for ref in resolved_references
                    ],
                }

                # Wrap result with conversation context
                if isinstance(result, dict):
                    result["conversation_context"] = conversation_context
                else:
                    # Wrap non-dict results to include conversation context
                    result = {"query_result": result, "conversation_context": conversation_context}

            return result

        except Exception as e:
            logger.error(f"Classification and routing failed: {e}")
            # Fallback to rule-based classification with original message if resolution failed
            fallback_message = resolved_message if "resolved_message" in locals() else message
            return await self._classify_and_route_rule_based(
                fallback_message, user_context, session_id, start_time
            )

    def _should_use_llm_classification(self, session_id: Optional[str] = None) -> bool:
        """
        PM-034 Phase 2B: A/B Testing Logic

        Determines whether to use LLM classification based on rollout percentage
        and session-based consistency.
        """
        if not self.enable_llm_classification or self.llm_rollout_percentage <= 0.0:
            return False

        if self.llm_rollout_percentage >= 1.0:
            return True

        # Use session_id for consistent A/B testing per session
        if session_id:
            # Hash session_id to get consistent assignment
            hash_value = hash(session_id) % 100
            return hash_value < (self.llm_rollout_percentage * 100)
        else:
            # Random assignment for sessions without ID
            return random.random() < self.llm_rollout_percentage

    async def _classify_and_route_with_llm(
        self,
        message: str,
        user_context: Optional[Dict[str, Any]],
        session_id: Optional[str],
        start_time: float,
    ) -> Any:
        """Classify and route using LLM with performance monitoring"""
        try:
            # LLM Classification
            intent = await self.llm_classifier.classify(message, user_context, session_id)

            # Calculate latency
            latency_ms = (time.time() - start_time) * 1000

            # Update metrics
            self.performance_metrics["llm_classifications"] += 1
            self._update_llm_metrics(latency_ms, True)

            # Check performance target
            if latency_ms > self.performance_targets["llm_classification"]:
                self.performance_metrics["target_violations"] += 1
                logger.warning(
                    f"LLM classification exceeded target: {latency_ms:.1f}ms > {self.performance_targets['llm_classification']}ms"
                )

            # Route the classified intent
            return await self.route_query(intent)

        except Exception as e:
            # Update metrics for failure
            latency_ms = (time.time() - start_time) * 1000
            self._update_llm_metrics(latency_ms, False)
            logger.error(f"LLM classification failed: {e}")
            raise

    async def _classify_and_route_rule_based(
        self,
        message: str,
        user_context: Optional[Dict[str, Any]],
        session_id: Optional[str],
        start_time: float,
    ) -> Any:
        """Classify and route using rule-based patterns (fast path)"""
        try:
            # Rule-based classification (simplified for now)
            intent = self._rule_based_classification(message, user_context, session_id)

            # Calculate latency
            latency_ms = (time.time() - start_time) * 1000

            # Update metrics
            self.performance_metrics["rule_based_classifications"] += 1
            self._update_rule_based_metrics(latency_ms, True)

            # Check performance target
            if latency_ms > self.performance_targets["rule_based"]:
                self.performance_metrics["target_violations"] += 1
                logger.warning(
                    f"Rule-based classification exceeded target: {latency_ms:.1f}ms > {self.performance_targets['rule_based']}ms"
                )

            # Route the classified intent
            return await self.route_query(intent)

        except Exception as e:
            # Update metrics for failure
            latency_ms = (time.time() - start_time) * 1000
            self._update_rule_based_metrics(latency_ms, False)
            logger.error(f"Rule-based classification failed: {e}")
            raise

    def _rule_based_classification(
        self, message: str, user_context: Optional[Dict[str, Any]], session_id: Optional[str]
    ) -> Intent:
        """
        PM-034 Phase 2B: Fast rule-based classification

        Provides fast path classification for common patterns
        while preserving existing functionality.
        """
        message_lower = message.lower().strip()

        # Canonical Query Patterns (UX Quick Win - Phase 3)
        # Identity queries
        if any(
            phrase in message_lower
            for phrase in [
                "what's your name",
                "what is your name",
                "who are you",
                "your name",
                "your role",
            ]
        ):
            return Intent(
                category=IntentCategory.IDENTITY,
                action="get_identity",
                confidence=0.95,
                original_message=message,
                context={
                    "rule_based": True,
                    "canonical_query": "identity",
                    "session_id": session_id,
                },
            )

        # Calendar queries (Issue #589: Must be BEFORE temporal to prevent misrouting)
        # These route to QUERY/meeting_time to use timezone-aware calendar adapter (#586)
        elif any(
            phrase in message_lower
            for phrase in [
                "what's on my calendar",
                "what is on my calendar",
                "whats on my calendar",
                "my calendar today",
                "calendar today",
                "meetings today",
                "do i have any meetings",
                "do i have meetings",
                "what meetings do i have",
                "what meetings",
                "my schedule today",
                "today's schedule",
                "todays schedule",
                "schedule for today",
            ]
        ):
            return Intent(
                category=IntentCategory.QUERY,
                action="meeting_time",
                confidence=0.95,
                original_message=message,
                context={
                    "rule_based": True,
                    "calendar_query": True,
                    "session_id": session_id,
                },
            )

        # Temporal queries (pure time/date questions, NOT calendar)
        elif any(
            phrase in message_lower
            for phrase in [
                "what day is it",
                "what time is it",
                "current date",
                "current time",
                "today's date",
            ]
        ):
            return Intent(
                category=IntentCategory.TEMPORAL,
                action="get_temporal_context",
                confidence=0.95,
                original_message=message,
                context={
                    "rule_based": True,
                    "canonical_query": "temporal",
                    "session_id": session_id,
                },
            )

        # Status queries
        elif any(
            phrase in message_lower
            for phrase in [
                "what am i working on",
                "what am i doing",
                "current work",
                "my work",
                "work status",
            ]
        ):
            return Intent(
                category=IntentCategory.STATUS,
                action="get_project_status",
                confidence=0.95,
                original_message=message,
                context={"rule_based": True, "canonical_query": "status", "session_id": session_id},
            )

        # Priority queries
        elif any(
            phrase in message_lower
            for phrase in [
                "what's my top priority",
                "what is my priority",
                "my priority",
                "top priority",
                "highest priority",
            ]
        ):
            return Intent(
                category=IntentCategory.PRIORITY,
                action="get_priorities",
                confidence=0.95,
                original_message=message,
                context={
                    "rule_based": True,
                    "canonical_query": "priority",
                    "session_id": session_id,
                },
            )

        # Guidance queries
        elif any(
            phrase in message_lower
            for phrase in [
                "what should i focus on",
                "what should i do",
                "focus today",
                "guidance",
                "recommendation",
            ]
        ):
            return Intent(
                category=IntentCategory.GUIDANCE,
                action="get_guidance",
                confidence=0.95,
                original_message=message,
                context={
                    "rule_based": True,
                    "canonical_query": "guidance",
                    "session_id": session_id,
                },
            )

        # Project-related queries
        elif any(word in message_lower for word in ["list", "show", "get", "find"]) and any(
            word in message_lower for word in ["project", "projects"]
        ):
            if "list" in message_lower or "show" in message_lower:
                return Intent(
                    category=IntentCategory.QUERY,
                    action="list_projects",
                    confidence=0.9,
                    original_message=message,
                    context={"rule_based": True, "session_id": session_id},
                )
            elif "find" in message_lower:
                # Extract project name if possible
                return Intent(
                    category=IntentCategory.QUERY,
                    action="find_project",
                    confidence=0.8,
                    original_message=message,
                    context={"rule_based": True, "session_id": session_id},
                )

        # File-related queries
        elif any(word in message_lower for word in ["file", "document", "content"]) and any(
            word in message_lower for word in ["search", "find", "read"]
        ):
            if "search" in message_lower:
                return Intent(
                    category=IntentCategory.QUERY,
                    action="search_files",
                    confidence=0.85,
                    original_message=message,
                    context={"rule_based": True, "search_query": message, "session_id": session_id},
                )
            elif "read" in message_lower:
                return Intent(
                    category=IntentCategory.QUERY,
                    action="read_file_contents",
                    confidence=0.8,
                    original_message=message,
                    context={"rule_based": True, "session_id": session_id},
                )

        # Conversation queries
        elif any(word in message_lower for word in ["hello", "hi", "greeting"]):
            return Intent(
                category=IntentCategory.QUERY,
                action="get_greeting",
                confidence=0.95,
                original_message=message,
                context={"rule_based": True, "session_id": session_id},
            )
        elif any(word in message_lower for word in ["help", "support", "assist"]):
            return Intent(
                category=IntentCategory.QUERY,
                action="get_help",
                confidence=0.9,
                original_message=message,
                context={"rule_based": True, "session_id": session_id},
            )

        # Default fallback
        else:
            return Intent(
                category=IntentCategory.QUERY,
                action="get_help",  # Safe fallback
                confidence=0.5,
                original_message=message,
                context={"rule_based": True, "fallback": True, "session_id": session_id},
            )

    def _update_llm_metrics(self, latency_ms: float, success: bool):
        """Update LLM classification metrics"""
        total = self.performance_metrics["llm_classifications"]
        avg = self.performance_metrics["average_llm_latency_ms"]

        # Update average latency
        self.performance_metrics["average_llm_latency_ms"] = (
            (avg * (total - 1) + latency_ms) / total if total > 0 else latency_ms
        )

        # Update success rate
        if total > 0:
            successful = sum(1 for i in range(total) if success)  # Simplified for now
            self.performance_metrics["llm_success_rate"] = successful / total

    def _update_rule_based_metrics(self, latency_ms: float, success: bool):
        """Update rule-based classification metrics"""
        total = self.performance_metrics["rule_based_classifications"]
        avg = self.performance_metrics["average_rule_based_latency_ms"]

        # Update average latency
        self.performance_metrics["average_rule_based_latency_ms"] = (
            (avg * (total - 1) + latency_ms) / total if total > 0 else latency_ms
        )

        # Update success rate
        if total > 0:
            successful = sum(1 for i in range(total) if success)  # Simplified for now
            self.performance_metrics["rule_based_success_rate"] = successful / total

    async def _route_query_with_protection(self, intent: Intent) -> Any:
        """Internal routing with circuit breaker protection"""

        if intent.action == "list_projects":
            if self.test_mode:
                # PM-063: Backward compatibility with test_mode
                return await self.degradation_handler.handle_database_failure(intent.action)
            return await self._execute_with_circuit_breaker(
                self.project_queries.list_active_projects, "project_queries", intent.action
            )
        elif intent.action == "get_project":
            if self.test_mode:
                return await self.degradation_handler.handle_database_failure(intent.action)
            project_id = intent.context.get("project_id")
            if not project_id:
                raise ValueError("get_project query requires project_id in context")
            return await self._execute_with_circuit_breaker(
                lambda: self.project_queries.get_project_by_id(project_id),
                "project_queries",
                intent.action,
            )
        elif intent.action == "get_default_project":
            if self.test_mode:
                return await self.degradation_handler.handle_database_failure(intent.action)
            # #1421: owner-scoped; absent principal fails closed to None (never
            # another tenant's default).
            _owner_id = intent.context.get("user_id")
            return await self._execute_with_circuit_breaker(
                lambda: self.project_queries.get_default_project(_owner_id),
                "project_queries",
                intent.action,
            )
        elif intent.action == "find_project":
            if self.test_mode:
                return await self.degradation_handler.handle_database_failure(intent.action)
            name = intent.context.get("name")
            if not name:
                raise ValueError("find_project query requires name in context")
            return await self._execute_with_circuit_breaker(
                lambda: self.project_queries.find_project_by_name(name),
                "project_queries",
                intent.action,
            )
        elif intent.action == "count_projects":
            if self.test_mode:
                return await self.degradation_handler.handle_database_failure(intent.action)
            return await self._execute_with_circuit_breaker(
                self.project_queries.count_active_projects, "project_queries", intent.action
            )
        elif intent.action == "get_project_details":
            if self.test_mode:
                return await self.degradation_handler.handle_database_failure(intent.action)
            project_id = intent.context.get("project_id")
            if not project_id:
                raise ValueError("get_project_details query requires project_id in context")
            return await self._execute_with_circuit_breaker(
                lambda: self.project_queries.get_project_details(project_id),
                "project_queries",
                intent.action,
            )
        elif intent.action == "get_greeting":
            if self.test_mode:
                return await self.degradation_handler.handle_database_failure(intent.action)
            return await self._execute_with_circuit_breaker(
                self.conversation_queries.get_greeting, "conversation_queries", intent.action
            )
        elif intent.action == "get_help":
            if self.test_mode:
                return await self.degradation_handler.handle_database_failure(intent.action)
            return await self._execute_with_circuit_breaker(
                self.conversation_queries.get_help, "conversation_queries", intent.action
            )
        elif intent.action == "get_status":
            if self.test_mode:
                return await self.degradation_handler.handle_database_failure(intent.action)
            return await self._execute_with_circuit_breaker(
                self.conversation_queries.get_status, "conversation_queries", intent.action
            )
        elif intent.action == "get_initial_contact":
            if self.test_mode:
                return await self.degradation_handler.handle_database_failure(intent.action)
            return await self._execute_with_circuit_breaker(
                self.conversation_queries.get_initial_contact, "conversation_queries", intent.action
            )
        # Canonical Query Actions (UX Quick Win - Phase 3)
        elif intent.action == "get_identity":
            if self.test_mode:
                return await self.degradation_handler.handle_database_failure(intent.action)
            return await self._execute_with_circuit_breaker(
                self.conversation_queries.get_identity, "conversation_queries", intent.action
            )
        elif intent.action == "get_temporal_context":
            if self.test_mode:
                return await self.degradation_handler.handle_database_failure(intent.action)
            return await self._execute_with_circuit_breaker(
                self.conversation_queries.get_temporal_context,
                "conversation_queries",
                intent.action,
            )
        elif intent.action == "get_project_status":
            if self.test_mode:
                return await self.degradation_handler.handle_database_failure(intent.action)
            return await self._execute_with_circuit_breaker(
                self.conversation_queries.get_project_status, "conversation_queries", intent.action
            )
        elif intent.action == "get_priorities":
            if self.test_mode:
                return await self.degradation_handler.handle_database_failure(intent.action)
            return await self._execute_with_circuit_breaker(
                self.conversation_queries.get_priorities, "conversation_queries", intent.action
            )
        elif intent.action == "get_guidance":
            if self.test_mode:
                return await self.degradation_handler.handle_database_failure(intent.action)
            return await self._execute_with_circuit_breaker(
                self.conversation_queries.get_guidance, "conversation_queries", intent.action
            )
        elif intent.action == "read_file_contents":
            file_id = intent.context.get("resolved_file_id")
            if not file_id:
                raise ValueError("read_file_contents query requires resolved_file_id in context")
            if self.test_mode:
                return await self.degradation_handler.handle_database_failure(intent.action)
            print(f"DEBUG: QueryRouter - file_id from context: {file_id}")
            print(f"DEBUG: QueryRouter - full context: {intent.context}")
            return await self._execute_with_circuit_breaker(
                lambda: self.file_queries.read_file_contents(file_id), "file_queries", intent.action
            )
        elif intent.action == "summarize_file":
            file_id = intent.context.get("resolved_file_id")
            if not file_id:
                raise ValueError("summarize_file query requires resolved_file_id in context")
            if self.test_mode:
                return await self.degradation_handler.handle_database_failure(intent.action)
            print(f"DEBUG: QueryRouter - summarize file_id: {file_id}")
            return await self._execute_with_circuit_breaker(
                lambda: self.file_queries.summarize_file(file_id), "file_queries", intent.action
            )
        elif intent.action == "search_files":
            search_query = intent.context.get("search_query")
            session_id = intent.context.get("session_id")
            if not search_query:
                raise ValueError("search_files query requires search_query in context")
            if self.test_mode:
                return await self.degradation_handler.handle_database_failure(intent.action)
            print(f"DEBUG: QueryRouter - searching files for: {search_query}")
            return await self._execute_with_circuit_breaker(
                lambda: self.file_queries.search_files_by_query(search_query, session_id),
                "file_queries",
                intent.action,
            )
        elif intent.action == "find_documents":
            search_query = intent.context.get("search_query")
            session_id = intent.context.get("session_id")
            if not search_query:
                raise ValueError("find_documents query requires search_query in context")
            if self.test_mode:
                return await self.degradation_handler.handle_database_failure(intent.action)
            print(f"DEBUG: QueryRouter - finding documents about: {search_query}")
            return await self._execute_with_circuit_breaker(
                lambda: self.file_queries.find_documents_about_topic(search_query, session_id),
                "file_queries",
                intent.action,
            )
        elif intent.action == "search_content":
            search_query = intent.context.get("search_query")
            session_id = intent.context.get("session_id")
            if not search_query:
                raise ValueError("search_content query requires search_query in context")
            if self.test_mode:
                return await self.degradation_handler.handle_database_failure(intent.action)
            print(f"DEBUG: QueryRouter - searching content for: {search_query}")
            return await self._execute_with_circuit_breaker(
                lambda: self.file_queries.search_content_by_query(search_query, session_id),
                "file_queries",
                intent.action,
            )
        elif intent.action == "search_documents":
            # Handle LLM-generated search_documents action (maps to find_documents)
            search_query = intent.context.get("search_query") or intent.context.get(
                "original_message", ""
            )
            session_id = intent.context.get("session_id")
            if self.test_mode:
                return await self.degradation_handler.handle_database_failure(intent.action)
            print(f"DEBUG: QueryRouter - searching documents for: {search_query}")
            return await self._execute_with_circuit_breaker(
                lambda: self.file_queries.find_documents_about_topic(search_query, session_id),
                "file_queries",
                intent.action,
            )
        else:
            raise ValueError(f"Unknown query action: {intent.action}")

    async def _execute_with_circuit_breaker(self, func, service: str, action: str) -> Any:
        """Execute function with circuit breaker protection and degradation handling"""
        try:
            if self.degradation_handler.enabled and await self.degradation_handler.should_degrade(
                service
            ):
                logger.info(f"Applying degradation for {service}.{action}")
                return await self.degradation_handler.handle_service_failure(
                    service, action, Exception("Circuit breaker open")
                )

            # Execute with circuit breaker protection
            return await self.degradation_handler.circuit_breaker.call(func)

        except (ValueError, ImportError) as e:
            # Re-raise these exceptions - they should not be degraded
            raise
        except Exception as e:
            logger.error(f"Circuit breaker execution failed for {service}.{action}: {e}")
            return await self.degradation_handler.handle_service_failure(service, action, e)

    def _get_service_for_action(self, action: str) -> str:
        """Map query action to service name for degradation handling"""
        project_actions = {
            "list_projects",
            "get_project",
            "get_default_project",
            "find_project",
            "count_projects",
            "get_project_details",
        }
        file_actions = {
            "read_file_contents",
            "summarize_file",
            "search_files",
            "find_documents",
            "search_content",
            "search_documents",
        }
        conversation_actions = {"get_greeting", "get_help", "get_status", "get_initial_contact"}

        if action in project_actions:
            return "project_queries"
        elif action in file_actions:
            return "file_queries"
        elif action in conversation_actions:
            return "conversation_queries"
        else:
            return "unknown_service"

    def get_supported_queries(self) -> List[str]:
        """Get list of supported query actions"""
        return [
            "list_projects",
            "get_project",
            "get_project_details",
            "get_default_project",
            "find_project",
            "count_projects",
            "get_greeting",
            "get_help",
            "get_status",
            "get_initial_contact",
            "read_file_contents",
            "summarize_file",
            "search_files",
            "find_documents",
            "search_content",
            "search_documents",  # LLM-generated action
        ]

    def get_degradation_status(self) -> Dict[str, Any]:
        """Get current degradation handler status for monitoring and debugging"""
        return {
            "test_mode": self.test_mode,
            "degradation_handler": self.degradation_handler.get_circuit_breaker_status(),
            "supported_queries": len(self.get_supported_queries()),
            "services": {
                "project_queries": "available",
                "file_queries": "available",
                "conversation_queries": "available",
            },
        }

    def get_performance_metrics(self) -> Dict[str, Any]:
        """PM-034 Phase 2B: Get performance metrics for monitoring and A/B testing"""
        metrics = self.performance_metrics.copy()

        # Add rollout information
        metrics.update(
            {
                "llm_rollout_percentage": self.llm_rollout_percentage,
                "enable_llm_classification": self.enable_llm_classification,
                "performance_targets": self.performance_targets,
                "llm_classifier_available": self.llm_classifier is not None,
            }
        )

        return metrics

    def update_rollout_percentage(self, percentage: float) -> None:
        """PM-034 Phase 2B: Update LLM rollout percentage for gradual deployment"""
        if not 0.0 <= percentage <= 1.0:
            raise ValueError("Rollout percentage must be between 0.0 and 1.0")

        self.llm_rollout_percentage = percentage
        logger.info(f"Updated LLM rollout percentage to {percentage:.1%}")

    def set_llm_classification_enabled(self, enable: bool = True) -> None:
        """PM-034 Phase 2B: Enable or disable LLM classification"""
        self.enable_llm_classification = enable
        logger.info(f"LLM classification {'enabled' if enable else 'disabled'}")
