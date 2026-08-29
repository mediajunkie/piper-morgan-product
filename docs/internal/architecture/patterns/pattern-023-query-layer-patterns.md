# Pattern-023: Query Layer Patterns

## Status

**Proven**

## Context

High-performance applications require optimized read-only operations with graceful degradation, performance monitoring, and intelligent routing. Traditional architectures often mix read and write operations, leading to performance bottlenecks, cascade failures, and poor user experience during service outages. The Query Layer Patterns address:

- What challenges does this solve? Provides optimized read-only operations with graceful degradation, performance monitoring, and intelligent routing for system resilience
- When should this pattern be considered? When building CQRS architectures that need high-performance read operations with circuit breaker protection
- What are the typical scenarios where this applies? Query routing, federated search, A/B testing of classification methods, specialized domain queries

## Pattern Description

The Query Layer Patterns provide a comprehensive set of patterns for implementing optimized read-only operations with clean separation of concerns, effective error handling, and maintainable architecture. These patterns demonstrate how to build resilient query systems with circuit breaker protection, graceful degradation, and performance monitoring.

Core concepts:

- CQRS Query Router for intelligent intent routing
- Graceful degradation with circuit breaker protection
- A/B testing framework for classification methods
- Specialized query services for domain-specific operations

## Implementation

### 23.1 CQRS Query Router Pattern

```python
from typing import Any, Optional, Dict
from enum import Enum
import asyncio
import time

class IntentCategory(Enum):
    QUERY = "query"
    IDENTITY = "identity"
    TEMPORAL = "temporal"
    STATUS = "status"

class QueryRouter:
    """Routes QUERY intents to appropriate query services with LLM enhancement"""

    def __init__(
        self,
        project_query_service,
        conversation_query_service,
        file_query_service,
        degradation_config: Optional[Dict] = None,
    ):
        self.project_queries = project_query_service
        self.conversation_queries = conversation_query_service
        self.file_queries = file_query_service
        self.degradation_handler = QueryDegradationHandler(degradation_config)

        # Service mapping for targeted error handling
        self.service_mapping = {
            "list_projects": self.project_queries,
            "search_files": self.file_queries,
            "search_conversations": self.conversation_queries,
            "get_project_status": self.project_queries,
            "analyze_file_content": self.file_queries
        }

    async def route_query(self, intent: Intent) -> Any:
        """Route an intent to the appropriate query service with graceful degradation"""
        if intent.category not in [
            IntentCategory.QUERY, IntentCategory.IDENTITY,
            IntentCategory.TEMPORAL, IntentCategory.STATUS
        ]:
            raise ValueError(f"QueryRouter cannot handle intent category: {intent.category}")

        try:
            return await self._route_query_with_protection(intent)
        except Exception as e:
            service = self._get_service_for_action(intent.action)
            return await self.degradation_handler.handle_service_failure(service, intent.action, e)

    async def _route_query_with_protection(self, intent: Intent) -> Any:
        """Route query with circuit breaker protection"""
        action = intent.action

        # Project-related queries
        if action in ["list_projects", "get_project_status", "find_project"]:
            return await self._execute_with_circuit_breaker(
                lambda: self.project_queries.handle_query(intent),
                "project_queries", action
            )

        # File-related queries
        elif action in ["search_files", "analyze_file_content", "list_recent_files"]:
            return await self._execute_with_circuit_breaker(
                lambda: self.file_queries.handle_query(intent),
                "file_queries", action
            )

        # Conversation-related queries
        elif action in ["search_conversations", "get_conversation_history", "find_mentions"]:
            return await self._execute_with_circuit_breaker(
                lambda: self.conversation_queries.handle_query(intent),
                "conversation_queries", action
            )

        else:
            raise ValueError(f"Unknown query action: {action}")

    async def _execute_with_circuit_breaker(self, func, service: str, action: str) -> Any:
        """Execute function with circuit breaker protection"""
        if self.degradation_handler.enabled and await self.degradation_handler.should_degrade(service):
            return await self.degradation_handler.handle_service_failure(
                service, action, Exception("Circuit breaker open")
            )
        return await self.degradation_handler.circuit_breaker.call(func)

    def _get_service_for_action(self, action: str) -> str:
        """Map action to service name for error handling"""
        if action in ["list_projects", "get_project_status", "find_project"]:
            return "project_queries"
        elif action in ["search_files", "analyze_file_content", "list_recent_files"]:
            return "file_queries"
        elif action in ["search_conversations", "get_conversation_history", "find_mentions"]:
            return "conversation_queries"
        else:
            return "unknown_service"

    async def federated_search(self, query: str) -> Dict[str, Any]:
        """Perform federated search across all query services"""
        search_tasks = [
            self._search_files(query),
            self._search_conversations(query),
            self._search_projects(query)
        ]

        results = await asyncio.gather(*search_tasks, return_exceptions=True)

        combined_results = {
            "query": query,
            "sources": [],
            "results": {}
        }

        # Process file search results
        if not isinstance(results[0], Exception) and results[0]:
            combined_results["results"]["files"] = results[0]
            combined_results["sources"].append("files")

        # Process conversation search results
        if not isinstance(results[1], Exception) and results[1]:
            combined_results["results"]["conversations"] = results[1]
            combined_results["sources"].append("conversations")

        # Process project search results
        if not isinstance(results[2], Exception) and results[2]:
            combined_results["results"]["projects"] = results[2]
            combined_results["sources"].append("projects")

        return combined_results

    async def _search_files(self, query: str) -> Optional[Dict]:
        """Search files with error handling"""
        try:
            return await self.file_queries.search_files(query)
        except Exception as e:
            logger.error(f"File search failed: {e}")
            return None

    async def _search_conversations(self, query: str) -> Optional[Dict]:
        """Search conversations with error handling"""
        try:
            return await self.conversation_queries.search_conversations(query)
        except Exception as e:
            logger.error(f"Conversation search failed: {e}")
            return None

    async def _search_projects(self, query: str) -> Optional[Dict]:
        """Search projects with error handling"""
        try:
            return await self.project_queries.search_projects(query)
        except Exception as e:
            logger.error(f"Project search failed: {e}")
            return None
```

### 23.2 Graceful Degradation Handler Pattern

```python
import asyncio
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class QueryDegradationHandler:
    """Graceful degradation handler for QueryRouter operations"""

    def __init__(self, circuit_breaker_config: Optional[Dict] = None):
        config = circuit_breaker_config or {}
        self.circuit_breaker = QueryCircuitBreaker(
            failure_threshold=config.get("failure_threshold", 5),
            recovery_timeout=config.get("recovery_timeout", 60),
        )
        self.enabled = FeatureFlags.is_circuit_breaker_enabled()
        self.service_failure_counts = {}
        self.last_failure_times = {}

    async def handle_service_failure(self, service: str, action: str, error: Exception) -> Any:
        """Handle service-specific failures with appropriate fallbacks"""
        logger.error(f"Service failure - Service: {service}, Action: {action}, Error: {error}")

        # Track failure metrics
        self._track_failure(service, error)

        if service == "file_queries":
            return await self._handle_file_service_failure(action, error)
        elif service == "project_queries":
            return await self._handle_project_service_failure(action, error)
        elif service == "conversation_queries":
            return await self._handle_conversation_service_failure(action, error)
        else:
            return await self._handle_unknown_service_failure(action, error)

    async def _handle_file_service_failure(self, action: str, error: Exception) -> Dict[str, Any]:
        """Handle file service failures with structured fallback responses"""
        fallback_responses = {
            "search_files": {
                "success": False,
                "error": "Unable to search files. Search service temporarily unavailable.",
                "suggestion": "File search is temporarily unavailable. Please try again shortly.",
                "results": [],
                "fallback": True
            },
            "analyze_file_content": {
                "success": False,
                "error": "Unable to analyze file content. Analysis service temporarily unavailable.",
                "suggestion": "File analysis is temporarily unavailable. Please try again shortly.",
                "analysis": None,
                "fallback": True
            },
            "list_recent_files": {
                "success": False,
                "error": "Unable to list recent files. File service temporarily unavailable.",
                "suggestion": "Recent files listing is temporarily unavailable. Please try again shortly.",
                "files": [],
                "fallback": True
            }
        }

        return fallback_responses.get(action, {
            "success": False,
            "error": "File service temporarily unavailable.",
            "suggestion": "Please try again shortly.",
            "fallback": True
        })

    async def _handle_project_service_failure(self, action: str, error: Exception) -> Dict[str, Any]:
        """Handle project service failures with structured fallback responses"""
        fallback_responses = {
            "list_projects": {
                "success": False,
                "error": "Unable to list projects. Project service temporarily unavailable.",
                "suggestion": "Project listing is temporarily unavailable. Please try again shortly.",
                "projects": [],
                "fallback": True
            },
            "get_project_status": {
                "success": False,
                "error": "Unable to get project status. Project service temporarily unavailable.",
                "suggestion": "Project status is temporarily unavailable. Please try again shortly.",
                "status": "unknown",
                "fallback": True
            },
            "find_project": {
                "success": False,
                "error": "Unable to find project. Project service temporarily unavailable.",
                "suggestion": "Project search is temporarily unavailable. Please try again shortly.",
                "project": None,
                "fallback": True
            }
        }

        return fallback_responses.get(action, {
            "success": False,
            "error": "Project service temporarily unavailable.",
            "suggestion": "Please try again shortly.",
            "fallback": True
        })

    async def _handle_conversation_service_failure(self, action: str, error: Exception) -> Dict[str, Any]:
        """Handle conversation service failures with structured fallback responses"""
        fallback_responses = {
            "search_conversations": {
                "success": False,
                "error": "Unable to search conversations. Conversation service temporarily unavailable.",
                "suggestion": "Conversation search is temporarily unavailable. Please try again shortly.",
                "conversations": [],
                "fallback": True
            },
            "get_conversation_history": {
                "success": False,
                "error": "Unable to get conversation history. Conversation service temporarily unavailable.",
                "suggestion": "Conversation history is temporarily unavailable. Please try again shortly.",
                "history": [],
                "fallback": True
            }
        }

        return fallback_responses.get(action, {
            "success": False,
            "error": "Conversation service temporarily unavailable.",
            "suggestion": "Please try again shortly.",
            "fallback": True
        })

    async def _handle_unknown_service_failure(self, action: str, error: Exception) -> Dict[str, Any]:
        """Handle unknown service failures with generic fallback"""
        return {
            "success": False,
            "error": "Service temporarily unavailable.",
            "suggestion": "The requested operation is temporarily unavailable. Please try again shortly.",
            "fallback": True,
            "action": action
        }

    async def should_degrade(self, service: str) -> bool:
        """Check if service should be degraded based on failure history"""
        if not self.enabled:
            return False

        failure_count = self.service_failure_counts.get(service, 0)
        return failure_count >= self.circuit_breaker.failure_threshold

    def _track_failure(self, service: str, error: Exception):
        """Track service failure for circuit breaker logic"""
        current_time = time.time()
        self.service_failure_counts[service] = self.service_failure_counts.get(service, 0) + 1
        self.last_failure_times[service] = current_time

        # Reset failure count if last failure was long ago
        if service in self.last_failure_times:
            time_since_last_failure = current_time - self.last_failure_times[service]
            if time_since_last_failure > self.circuit_breaker.recovery_timeout:
                self.service_failure_counts[service] = 1

class QueryCircuitBreaker:
    """Circuit breaker for query operations"""

    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = 0
        self.state = "closed"  # closed, open, half-open

    async def call(self, func):
        """Execute function with circuit breaker protection"""
        if self.state == "open":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "half-open"
            else:
                raise Exception("Circuit breaker is open")

        try:
            result = await func()
            if self.state == "half-open":
                self.state = "closed"
                self.failure_count = 0
            return result
        except Exception as e:
            self.last_failure_time = time.time()
            self.failure_count += 1
            if self.failure_count >= self.failure_threshold:
                self.state = "open"
            raise
```

### 23.3 A/B Testing Query Classification Pattern

```python
import hashlib
from typing import Dict, Any, Optional
import time

class ABTestingQueryClassification:
    """Enable gradual rollout of LLM-based classification with performance monitoring"""

    def __init__(self,
                 rule_based_classifier,
                 llm_classifier,
                 llm_percentage: float = 50.0,
                 performance_target_ms: float = 200.0):
        self.rule_based_classifier = rule_based_classifier
        self.llm_classifier = llm_classifier
        self.llm_percentage = llm_percentage
        self.performance_target_ms = performance_target_ms

        # Performance monitoring
        self.llm_metrics = {
            "total_calls": 0,
            "success_count": 0,
            "total_latency_ms": 0.0,
            "target_violations": 0
        }

        self.rule_metrics = {
            "total_calls": 0,
            "success_count": 0,
            "total_latency_ms": 0.0
        }

    def should_use_llm_classification(self, session_id: str) -> bool:
        """Determine if session should use LLM classification based on consistent hashing"""
        # Use session-based hashing for consistent A/B assignment
        session_hash = hashlib.md5(session_id.encode()).hexdigest()
        hash_value = int(session_hash[:8], 16)  # Use first 8 hex chars
        percentage = (hash_value % 100)

        return percentage < self.llm_percentage

    async def classify_intent(self, message: str, session_id: str) -> Intent:
        """Classify intent using A/B testing between rule-based and LLM methods"""
        use_llm = self.should_use_llm_classification(session_id)

        if use_llm:
            return await self._classify_with_llm(message, session_id)
        else:
            return await self._classify_with_rules(message, session_id)

    async def _classify_with_llm(self, message: str, session_id: str) -> Intent:
        """Classify using LLM with performance monitoring"""
        start_time = time.time()

        try:
            intent = await self.llm_classifier.classify(message)
            latency_ms = (time.time() - start_time) * 1000

            self._update_llm_metrics(latency_ms, True)

            # Check performance target
            if latency_ms > self.performance_target_ms:
                logger.warning(f"LLM classification exceeded target: {latency_ms:.2f}ms > {self.performance_target_ms}ms")
                self.llm_metrics["target_violations"] += 1

            return intent

        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            self._update_llm_metrics(latency_ms, False)

            # Fallback to rule-based classification
            logger.error(f"LLM classification failed, falling back to rules: {e}")
            return await self._classify_with_rules(message, session_id)

    async def _classify_with_rules(self, message: str, session_id: str) -> Intent:
        """Classify using rule-based method with performance monitoring"""
        start_time = time.time()

        try:
            intent = await self.rule_based_classifier.classify(message)
            latency_ms = (time.time() - start_time) * 1000

            self._update_rule_metrics(latency_ms, True)
            return intent

        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            self._update_rule_metrics(latency_ms, False)
            raise

    def _update_llm_metrics(self, latency_ms: float, success: bool):
        """Update LLM performance metrics"""
        self.llm_metrics["total_calls"] += 1
        self.llm_metrics["total_latency_ms"] += latency_ms
        if success:
            self.llm_metrics["success_count"] += 1

    def _update_rule_metrics(self, latency_ms: float, success: bool):
        """Update rule-based performance metrics"""
        self.rule_metrics["total_calls"] += 1
        self.rule_metrics["total_latency_ms"] += latency_ms
        if success:
            self.rule_metrics["success_count"] += 1

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get comprehensive performance metrics for both classification methods"""
        llm_avg_latency = (
            self.llm_metrics["total_latency_ms"] / max(self.llm_metrics["total_calls"], 1)
        )
        rule_avg_latency = (
            self.rule_metrics["total_latency_ms"] / max(self.rule_metrics["total_calls"], 1)
        )

        llm_success_rate = (
            self.llm_metrics["success_count"] / max(self.llm_metrics["total_calls"], 1)
        )
        rule_success_rate = (
            self.rule_metrics["success_count"] / max(self.rule_metrics["total_calls"], 1)
        )

        return {
            "llm_classification": {
                "total_calls": self.llm_metrics["total_calls"],
                "success_rate": llm_success_rate,
                "average_latency_ms": llm_avg_latency,
                "target_violations": self.llm_metrics["target_violations"],
                "performance_target_ms": self.performance_target_ms
            },
            "rule_classification": {
                "total_calls": self.rule_metrics["total_calls"],
                "success_rate": rule_success_rate,
                "average_latency_ms": rule_avg_latency
            },
            "ab_testing": {
                "llm_percentage": self.llm_percentage,
                "total_sessions": self.llm_metrics["total_calls"] + self.rule_metrics["total_calls"]
            }
        }

class IntentClassificationRouter:
    """Router that uses A/B testing for intent classification"""

    def __init__(self, ab_testing_classifier, query_router):
        self.ab_testing_classifier = ab_testing_classifier
        self.query_router = query_router

    async def process_message(self, message: str, session_id: str) -> Any:
        """Process message with A/B tested classification and routing"""
        # Classify intent using A/B testing
        start_time = time.time()

        try:
            intent = await self.ab_testing_classifier.classify_intent(message, session_id)
            classification_ms = (time.time() - start_time) * 1000

            # Route to appropriate handler
            return await self.query_router.route_query(intent)
        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            self._update_llm_metrics(latency_ms, False)
            raise
```

### 23.4 Specialized Query Service Pattern

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class BaseQueryService(ABC):
    """Base class for specialized query services"""

    def __init__(self, repository, cache_manager=None):
        self.repository = repository
        self.cache = cache_manager
        self.performance_monitor = PerformanceMonitor()

    @abstractmethod
    async def handle_query(self, intent: Intent) -> Any:
        """Handle query intent for this domain"""
        pass

    async def _execute_with_monitoring(self, operation_name: str, func):
        """Execute operation with performance monitoring"""
        start_time = time.time()
        try:
            result = await func()
            latency_ms = (time.time() - start_time) * 1000
            self.performance_monitor.record_success(operation_name, latency_ms)
            return result
        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            self.performance_monitor.record_failure(operation_name, latency_ms)
            raise

class ProjectQueryService(BaseQueryService):
    """Specialized query service for project-related operations"""

    async def handle_query(self, intent: Intent) -> Any:
        """Handle project query intents"""
        action = intent.action

        if action == "list_projects":
            return await self._execute_with_monitoring(
                "list_projects",
                lambda: self._list_projects(intent.parameters)
            )
        elif action == "get_project_status":
            return await self._execute_with_monitoring(
                "get_project_status",
                lambda: self._get_project_status(intent.parameters)
            )
        elif action == "find_project":
            return await self._execute_with_monitoring(
                "find_project",
                lambda: self._find_project(intent.parameters)
            )
        else:
            raise ValueError(f"Unknown project action: {action}")

    async def _list_projects(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """List projects with filtering and pagination"""
        # Check cache first
        cache_key = f"projects:list:{hash(str(parameters))}"
        if self.cache:
            cached_result = await self.cache.get(cache_key)
            if cached_result:
                return cached_result

        # Query repository
        projects = await self.repository.list_projects(
            limit=parameters.get("limit", 50),
            offset=parameters.get("offset", 0),
            filters=parameters.get("filters", {})
        )

        result = {
            "success": True,
            "projects": [self._serialize_project(p) for p in projects],
            "total_count": len(projects),
            "cached": False
        }

        # Cache result
        if self.cache:
            await self.cache.set(cache_key, result, ttl=300)  # 5 minutes

        return result

    async def _get_project_status(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed project status"""
        project_id = parameters.get("project_id")
        if not project_id:
            raise ValueError("project_id required for get_project_status")

        project = await self.repository.get_project_by_id(project_id)
        if not project:
            return {
                "success": False,
                "error": f"Project {project_id} not found",
                "status": "not_found"
            }

        # Get additional status information
        status_info = await self.repository.get_project_status_details(project_id)

        return {
            "success": True,
            "project": self._serialize_project(project),
            "status": status_info.get("status", "unknown"),
            "last_activity": status_info.get("last_activity"),
            "metrics": status_info.get("metrics", {})
        }

    async def _find_project(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Find project by various criteria"""
        query = parameters.get("query", "")
        search_fields = parameters.get("search_fields", ["name", "description"])

        projects = await self.repository.search_projects(
            query=query,
            fields=search_fields,
            limit=parameters.get("limit", 20)
        )

        return {
            "success": True,
            "query": query,
            "projects": [self._serialize_project(p) for p in projects],
            "search_fields": search_fields
        }

    def _serialize_project(self, project) -> Dict[str, Any]:
        """Serialize project for API response"""
        return {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "created_at": project.created_at.isoformat() if project.created_at else None,
            "updated_at": project.updated_at.isoformat() if project.updated_at else None,
            "status": getattr(project, 'status', 'unknown')
        }

class FileQueryService(BaseQueryService):
    """Specialized query service for file-related operations"""

    async def handle_query(self, intent: Intent) -> Any:
        """Handle file query intents"""
        action = intent.action

        if action == "search_files":
            return await self._execute_with_monitoring(
                "search_files",
                lambda: self._search_files(intent.parameters)
            )
        elif action == "analyze_file_content":
            return await self._execute_with_monitoring(
                "analyze_file_content",
                lambda: self._analyze_file_content(intent.parameters)
            )
        elif action == "list_recent_files":
            return await self._execute_with_monitoring(
                "list_recent_files",
                lambda: self._list_recent_files(intent.parameters)
            )
        else:
            raise ValueError(f"Unknown file action: {action}")

    async def _search_files(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Search files by content or metadata"""
        query = parameters.get("query", "")
        file_types = parameters.get("file_types", [])
        limit = parameters.get("limit", 50)

        # Perform search with repository
        files = await self.repository.search_files(
            query=query,
            file_types=file_types,
            limit=limit
        )

        return {
            "success": True,
            "query": query,
            "files": [self._serialize_file(f) for f in files],
            "file_types": file_types,
            "total_results": len(files)
        }

    async def _analyze_file_content(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze file content for patterns or insights"""
        file_path = parameters.get("file_path")
        analysis_type = parameters.get("analysis_type", "basic")

        if not file_path:
            raise ValueError("file_path required for analyze_file_content")

        file_content = await self.repository.get_file_content(file_path)
        if not file_content:
            return {
                "success": False,
                "error": f"File {file_path} not found or cannot be read",
                "analysis": None
            }

        # Perform analysis based on type
        analysis_result = await self._perform_file_analysis(file_content, analysis_type)

        return {
            "success": True,
            "file_path": file_path,
            "analysis_type": analysis_type,
            "analysis": analysis_result
        }

    async def _list_recent_files(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """List recently modified files"""
        limit = parameters.get("limit", 20)
        days_back = parameters.get("days_back", 7)

        files = await self.repository.get_recent_files(
            limit=limit,
            days_back=days_back
        )

        return {
            "success": True,
            "files": [self._serialize_file(f) for f in files],
            "limit": limit,
            "days_back": days_back
        }

    def _serialize_file(self, file) -> Dict[str, Any]:
        """Serialize file for API response"""
        return {
            "path": file.path,
            "name": file.name,
            "size": file.size,
            "modified_at": file.modified_at.isoformat() if file.modified_at else None,
            "file_type": file.file_type,
            "extension": file.extension
        }

    async def _perform_file_analysis(self, content: str, analysis_type: str) -> Dict[str, Any]:
        """Perform different types of file analysis"""
        if analysis_type == "basic":
            return {
                "line_count": content.count('\n') + 1,
                "character_count": len(content),
                "word_count": len(content.split()),
                "analysis_type": "basic"
            }
        elif analysis_type == "code":
            # Basic code analysis
            return {
                "line_count": content.count('\n') + 1,
                "import_count": content.count('import '),
                "function_count": content.count('def '),
                "class_count": content.count('class '),
                "analysis_type": "code"
            }
        else:
            return {
                "error": f"Unknown analysis type: {analysis_type}",
                "analysis_type": analysis_type
            }
```

## Usage Guidelines

### When to Use Query Layer Patterns

- **High-Performance Read Operations**: When building CQRS architectures that need optimized read paths
- **System Resilience Requirements**: When applications need graceful degradation and circuit breaker protection
- **A/B Testing Needs**: When gradually rolling out new classification or processing methods
- **Federated Search**: When searching across multiple data sources with different performance characteristics

### Implementation Best Practices

- **Circuit Breaker Protection**: Apply circuit breaker protection to all external service calls
- **Graceful Degradation**: Provide meaningful fallback responses with actionable user guidance
- **Performance Monitoring**: Track latency and success rates for all query operations
- **Service Specialization**: Create focused query services for specific domains
- **A/B Testing Consistency**: Use session-based hashing for consistent user experience

### Performance Targets

- **Rule-based Classification**: <50ms target, deterministic patterns
- **LLM Classification**: <200ms target, higher accuracy for complex queries
- **Circuit Breaker Recovery**: 60-second timeout with exponential backoff
- **Federated Search**: <500ms combined across all sources
- **Query Service Operations**: <100ms for single repository access

## Benefits

- Optimized read paths without workflow overhead for improved performance
- Circuit breaker protection prevents cascade failures across service boundaries
- Clear separation of concerns between queries and commands
- Centralized routing logic with service specialization for maintainability
- Intelligent fallback strategies for enhanced user experience during outages
- A/B testing framework enables safe deployment of new features

## Trade-offs

- Additional architectural complexity with multiple specialized services
- Performance monitoring overhead and metrics collection requirements
- Circuit breaker configuration and tuning complexity
- Need for comprehensive fallback response design
- A/B testing infrastructure maintenance and session consistency requirements
- Memory overhead for caching and performance metrics storage

## Anti-patterns to Avoid

- ❌ **Mixing Read/Write Operations**: Combining query and command operations in same service
- ❌ **Blocking Operations**: Using synchronous operations in async query methods
- ❌ **Heavy Processing**: Complex business logic in query services
- ❌ **State Mutations**: Changing data in read-only query operations
- ❌ **Missing Degradation**: No fallback strategy for service failures
- ❌ **Poor Performance**: Ignoring latency targets and metrics
- ❌ **Inconsistent Routing**: Different error handling patterns per service

## Related Patterns

- [Pattern-004: CQRS-lite Pattern](pattern-004-cqrs-lite.md) - Foundational CQRS architecture
- [Pattern-014: Error Handling Pattern (API Contract)](pattern-014-error-handling-api-contract.md) - Error handling integration
- [Pattern-017: Background Task Error Handling Pattern](pattern-017-background-task-error-handling.md) - Circuit breaker implementation
- [Pattern-001: Repository Pattern](pattern-001-repository.md) - Data access layer integration

## References

- **Implementation**: QueryRouter with circuit breaker protection and specialized services
- **Performance Evidence**: <50ms rule-based, <200ms LLM classification targets validated
- **Test Coverage**: Comprehensive async testing with performance monitoring
- **Related ADR**: A/B testing framework, graceful degradation strategies

## Migration Notes

_Consolidated from:_

- `pattern-catalog.md#23-query-layer-patterns` - Complete query routing and degradation implementation
- CQRS query router pattern with circuit breaker protection
- A/B testing framework for gradual rollout of LLM-based classification
- Specialized query services for domain-specific operations

_Last updated: September 15, 2025_
