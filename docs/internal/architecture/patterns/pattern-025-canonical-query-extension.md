# Pattern-025: Canonical Query Extension Pattern

## Status

**Proven**

## Context

Existing canonical query systems often need additional intelligence and capabilities, but replacing them entirely risks breaking backward compatibility and losing proven functionality. Traditional approaches either create entirely new systems (losing compatibility) or modify existing systems directly (risking stability). The Canonical Query Extension Pattern addresses:

- What challenges does this solve? Extends existing canonical query systems with additional intelligence while preserving original functionality and maintaining backward compatibility
- When should this pattern be considered? When enhancing proven systems with new capabilities without disrupting existing functionality
- What are the typical scenarios where this applies? GitHub issue intelligence integration, external service enhancement, progressive feature rollout, legacy system modernization

## Pattern Description

The Canonical Query Extension Pattern extends existing canonical query systems with additional intelligence while preserving original functionality and maintaining backward compatibility. The pattern uses delegation to preserve existing behavior while adding enhancements through composition, ensuring graceful degradation and additive functionality.

Core concept:

- Delegation-first approach preserving original functionality
- Additive enhancements that never break existing behavior
- Graceful degradation when external services are unavailable
- Performance isolation between original and enhanced features

## Implementation

### Core Extension Framework

```python
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime
import asyncio
import logging

@dataclass
class IssueIntelligenceResult:
    """Enhanced result preserving original response"""
    original_response: Dict[str, Any]      # From CanonicalHandlers
    enhanced_message: str                  # With additional context
    issue_intelligence: Dict[str, Any]     # Enhancement data
    context_source: str = "github_integration"
    enhancement_time_ms: Optional[int] = None
    fallback_used: bool = False

class CanonicalQueryExtensionEngine:
    """Base class for extending canonical query systems"""

    def __init__(self, original_handlers, enhancement_services: Dict[str, Any]):
        self.original_handlers = original_handlers  # Delegation target
        self.enhancement_services = enhancement_services
        self.performance_monitor = PerformanceMonitor()
        self.circuit_breaker = CircuitBreaker()
        self.logger = logging.getLogger(__name__)

    async def handle_extended_query(self, intent, session_id, enhancement_config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Handle query with optional enhancements while preserving original behavior"""
        # Step 1: Always get original response first (delegation)
        start_time = datetime.utcnow()

        try:
            original_response = await self.original_handlers.handle(intent, session_id)
        except Exception as e:
            self.logger.error(f"Original handler failed: {e}")
            return {"error": "Original query handler failed", "details": str(e)}

        original_time = (datetime.utcnow() - start_time).total_seconds() * 1000

        # Step 2: Determine if enhancements are requested and available
        should_enhance = self._should_apply_enhancements(intent, enhancement_config)

        if not should_enhance:
            return {
                "response": original_response,
                "enhanced": False,
                "original_time_ms": original_time
            }

        # Step 3: Apply enhancements with circuit breaker protection
        enhancement_start = datetime.utcnow()
        enhancement_result = await self._apply_enhancements(
            original_response, intent, session_id
        )
        enhancement_time = (datetime.utcnow() - enhancement_start).total_seconds() * 1000

        # Step 4: Merge results preserving original structure
        return {
            "response": enhancement_result.original_response,  # Preserved exactly
            "enhanced_message": enhancement_result.enhanced_message,
            "enhancements": enhancement_result.issue_intelligence,
            "enhanced": True,
            "original_time_ms": original_time,
            "enhancement_time_ms": enhancement_time,
            "fallback_used": enhancement_result.fallback_used
        }

    async def _apply_enhancements(self, original_response: Dict[str, Any], intent, session_id) -> IssueIntelligenceResult:
        """Apply enhancements with graceful degradation"""
        try:
            # Attempt to gather enhancement intelligence
            enhancement_data = await self.circuit_breaker.call(
                self._gather_enhancement_intelligence,
                intent, session_id
            )

            # Enhance the original message
            enhanced_message = await self._enhance_message(
                original_response.get("message", ""),
                enhancement_data,
                intent
            )

            return IssueIntelligenceResult(
                original_response=original_response,
                enhanced_message=enhanced_message,
                issue_intelligence=enhancement_data,
                enhancement_time_ms=None,  # Calculated by caller
                fallback_used=False
            )

        except Exception as e:
            self.logger.warning(f"Enhancement failed, using fallback: {e}")

            # Graceful degradation - return original with minimal enhancement
            return IssueIntelligenceResult(
                original_response=original_response,
                enhanced_message=original_response.get("message", ""),
                issue_intelligence={"error": "Enhancement unavailable", "reason": str(e)},
                fallback_used=True
            )

    def _should_apply_enhancements(self, intent, config: Dict[str, Any] = None) -> bool:
        """Determine if enhancements should be applied"""
        if not config:
            config = {}

        # Check if enhancements are explicitly disabled
        if config.get("disable_enhancements", False):
            return False

        # Check if enhancement services are available
        if not self.enhancement_services:
            return False

        # Check circuit breaker state
        if self.circuit_breaker.is_open():
            return False

        # Check intent type compatibility
        compatible_actions = config.get("compatible_actions", ["list_issues", "search_issues", "get_project_status"])
        if intent.action not in compatible_actions:
            return False

        return True

    async def _gather_enhancement_intelligence(self, intent, session_id) -> Dict[str, Any]:
        """Gather enhancement intelligence from external services"""
        intelligence = {}

        # GitHub integration enhancement
        if "github" in self.enhancement_services:
            github_service = self.enhancement_services["github"]
            try:
                github_data = await github_service.get_related_issues(intent)
                intelligence["github_issues"] = github_data
            except Exception as e:
                self.logger.warning(f"GitHub enhancement failed: {e}")
                intelligence["github_issues"] = {"error": str(e)}

        # Spatial intelligence enhancement
        if "spatial" in self.enhancement_services:
            spatial_service = self.enhancement_services["spatial"]
            try:
                spatial_context = await spatial_service.analyze_spatial_context(intent)
                intelligence["spatial_context"] = spatial_context
            except Exception as e:
                self.logger.warning(f"Spatial enhancement failed: {e}")
                intelligence["spatial_context"] = {"error": str(e)}

        # Learning system enhancement
        if "learning" in self.enhancement_services:
            learning_service = self.enhancement_services["learning"]
            try:
                learned_patterns = await learning_service.get_relevant_patterns(intent)
                intelligence["learned_patterns"] = learned_patterns
            except Exception as e:
                self.logger.warning(f"Learning enhancement failed: {e}")
                intelligence["learned_patterns"] = {"error": str(e)}

        return intelligence

    async def _enhance_message(self, original_message: str, intelligence: Dict[str, Any], intent) -> str:
        """Enhance original message with additional context"""
        enhanced_parts = [original_message]

        # Add GitHub issues context if available
        github_issues = intelligence.get("github_issues", {})
        if github_issues and not github_issues.get("error"):
            issue_count = len(github_issues.get("issues", []))
            if issue_count > 0:
                enhanced_parts.append(f"\n\n🔗 Related: Found {issue_count} related GitHub issues")

                # Add top 3 most relevant issues
                for issue in github_issues.get("issues", [])[:3]:
                    enhanced_parts.append(f"  • #{issue.get('number')}: {issue.get('title', 'Untitled')}")

        # Add spatial context if available
        spatial_context = intelligence.get("spatial_context", {})
        if spatial_context and not spatial_context.get("error"):
            attention_level = spatial_context.get("attention_level", 0)
            if attention_level > 0.7:
                enhanced_parts.append(f"\n⚡ High priority context detected (attention: {attention_level:.1f})")

        # Add learned patterns if available
        learned_patterns = intelligence.get("learned_patterns", {})
        if learned_patterns and not learned_patterns.get("error"):
            pattern_count = len(learned_patterns.get("patterns", []))
            if pattern_count > 0:
                enhanced_parts.append(f"\n🧠 {pattern_count} learned patterns may apply to this context")

        return "".join(enhanced_parts)

class IssueIntelligenceCanonicalQueryEngine(CanonicalQueryExtensionEngine):
    """Canonical query engine with GitHub issue intelligence"""

    def __init__(self, canonical_handlers, github_integration, session_manager):
        enhancement_services = {
            "github": github_integration,
            "session": session_manager
        }
        super().__init__(canonical_handlers, enhancement_services)

    async def enhance_canonical_query(self, intent, session_id) -> IssueIntelligenceResult:
        """Enhanced query with GitHub issue intelligence"""
        # Step 1: Get original response (delegation)
        original_response = await self.original_handlers.handle(intent, session_id)

        # Step 2: Gather GitHub issue intelligence
        issue_intelligence = await self._gather_issue_intelligence(intent)

        # Step 3: Enhance message with additional context
        enhanced_message = await self._enhance_message_with_issues(
            original_response["message"], issue_intelligence, intent
        )

        # Step 4: Return enhanced result preserving original
        return IssueIntelligenceResult(
            original_response=original_response,      # Preserved
            enhanced_message=enhanced_message,        # Enhanced
            issue_intelligence=issue_intelligence     # Additional data
        )

    async def _gather_issue_intelligence(self, intent) -> Dict[str, Any]:
        """Gather GitHub issue intelligence for enhancement"""
        intelligence = {}

        try:
            github_service = self.enhancement_services["github"]

            # Search for related issues based on intent
            if intent.action in ["list_issues", "search_issues"]:
                query_terms = self._extract_search_terms(intent)
                related_issues = await github_service.search_issues(query_terms)
                intelligence["related_issues"] = related_issues

            # Get project-specific issue metrics
            if hasattr(intent, 'project_id') and intent.project_id:
                project_metrics = await github_service.get_project_metrics(intent.project_id)
                intelligence["project_metrics"] = project_metrics

            # Get user-specific issue context
            if hasattr(intent, 'user_context') and intent.user_context:
                user_issues = await github_service.get_user_issues(intent.user_context)
                intelligence["user_issues"] = user_issues

        except Exception as e:
            self.logger.error(f"Failed to gather issue intelligence: {e}")
            intelligence["error"] = str(e)

        return intelligence

    async def _enhance_message_with_issues(self, original_message: str, intelligence: Dict[str, Any], intent) -> str:
        """Enhance message with GitHub issue context"""
        if intelligence.get("error"):
            return original_message  # No enhancement on error

        enhanced_parts = [original_message]

        # Add related issues
        related_issues = intelligence.get("related_issues", [])
        if related_issues:
            enhanced_parts.append(f"\n\n📋 Found {len(related_issues)} related issues:")
            for issue in related_issues[:5]:  # Top 5 issues
                status_emoji = "✅" if issue.get("state") == "closed" else "🔴"
                enhanced_parts.append(f"  {status_emoji} #{issue.get('number')}: {issue.get('title')}")

        # Add project metrics
        project_metrics = intelligence.get("project_metrics", {})
        if project_metrics:
            open_count = project_metrics.get("open_issues", 0)
            closed_count = project_metrics.get("closed_issues", 0)
            if open_count > 0 or closed_count > 0:
                enhanced_parts.append(f"\n\n📊 Project status: {open_count} open, {closed_count} closed issues")

        # Add user context
        user_issues = intelligence.get("user_issues", [])
        if user_issues:
            assigned_count = len([i for i in user_issues if i.get("assigned_to_user")])
            if assigned_count > 0:
                enhanced_parts.append(f"\n\n👤 You have {assigned_count} assigned issues")

        return "".join(enhanced_parts)

    def _extract_search_terms(self, intent) -> List[str]:
        """Extract search terms from intent for issue search"""
        terms = []

        if hasattr(intent, 'message') and intent.message:
            # Extract keywords from message
            words = intent.message.lower().split()
            # Filter out common words and keep meaningful terms
            meaningful_words = [w for w in words if len(w) > 3 and w not in ["this", "that", "with", "have", "will"]]
            terms.extend(meaningful_words[:5])  # Top 5 terms

        if hasattr(intent, 'action') and intent.action:
            terms.append(intent.action)

        return terms
```

### Performance Monitoring and Circuit Breaker

```python
class EnhancementPerformanceMonitor:
    """Monitor performance of canonical query extensions"""

    def __init__(self):
        self.metrics = {
            "total_queries": 0,
            "enhanced_queries": 0,
            "enhancement_failures": 0,
            "average_original_time_ms": 0.0,
            "average_enhancement_time_ms": 0.0,
            "circuit_breaker_trips": 0
        }
        self.recent_performance = []
        self.max_history = 100

    def record_query_performance(self, original_time_ms: float, enhancement_time_ms: float = None,
                                enhanced: bool = False, failed: bool = False):
        """Record performance metrics for monitoring"""
        self.metrics["total_queries"] += 1

        # Update average original time
        total_original_time = self.metrics["average_original_time_ms"] * (self.metrics["total_queries"] - 1)
        self.metrics["average_original_time_ms"] = (total_original_time + original_time_ms) / self.metrics["total_queries"]

        if enhanced:
            self.metrics["enhanced_queries"] += 1

            if enhancement_time_ms:
                # Update average enhancement time
                enhanced_count = self.metrics["enhanced_queries"]
                total_enhancement_time = self.metrics["average_enhancement_time_ms"] * (enhanced_count - 1)
                self.metrics["average_enhancement_time_ms"] = (total_enhancement_time + enhancement_time_ms) / enhanced_count

        if failed:
            self.metrics["enhancement_failures"] += 1

        # Keep recent performance history
        self.recent_performance.append({
            "timestamp": datetime.utcnow(),
            "original_time_ms": original_time_ms,
            "enhancement_time_ms": enhancement_time_ms,
            "enhanced": enhanced,
            "failed": failed
        })

        # Trim history if too long
        if len(self.recent_performance) > self.max_history:
            self.recent_performance = self.recent_performance[-self.max_history:]

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary"""
        enhancement_rate = (
            self.metrics["enhanced_queries"] / max(self.metrics["total_queries"], 1)
        )

        failure_rate = (
            self.metrics["enhancement_failures"] / max(self.metrics["enhanced_queries"], 1)
        )

        return {
            "total_queries": self.metrics["total_queries"],
            "enhancement_rate": enhancement_rate,
            "failure_rate": failure_rate,
            "average_times": {
                "original_ms": self.metrics["average_original_time_ms"],
                "enhancement_ms": self.metrics["average_enhancement_time_ms"],
                "total_ms": self.metrics["average_original_time_ms"] + self.metrics["average_enhancement_time_ms"]
            },
            "circuit_breaker_trips": self.metrics["circuit_breaker_trips"],
            "health_status": self._calculate_health_status()
        }

    def _calculate_health_status(self) -> str:
        """Calculate overall health status"""
        failure_rate = (
            self.metrics["enhancement_failures"] / max(self.metrics["enhanced_queries"], 1)
        )

        if failure_rate > 0.5:
            return "unhealthy"
        elif failure_rate > 0.2:
            return "degraded"
        else:
            return "healthy"

class CanonicalQueryCircuitBreaker:
    """Circuit breaker for canonical query enhancements"""

    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open

    async def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        if self.state == "open":
            if self.last_failure_time and \
               (datetime.utcnow() - self.last_failure_time).seconds > self.recovery_timeout:
                self.state = "half-open"
            else:
                raise Exception("Circuit breaker is open - enhancement unavailable")

        try:
            result = await func(*args, **kwargs)

            # Success resets failure count
            if self.state == "half-open":
                self.state = "closed"
                self.failure_count = 0

            return result

        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.utcnow()

            if self.failure_count >= self.failure_threshold:
                self.state = "open"

            raise

    def is_open(self) -> bool:
        """Check if circuit breaker is open"""
        return self.state == "open"

    def get_state(self) -> Dict[str, Any]:
        """Get current circuit breaker state"""
        return {
            "state": self.state,
            "failure_count": self.failure_count,
            "failure_threshold": self.failure_threshold,
            "last_failure": self.last_failure_time.isoformat() if self.last_failure_time else None,
            "recovery_timeout": self.recovery_timeout
        }
```

### Usage Examples

```python
# Setup canonical query extension
canonical_handlers = ExistingCanonicalHandlers()
github_integration = GitHubIntegrationService()
session_manager = SessionManager()

# Create extended engine
extended_engine = IssueIntelligenceCanonicalQueryEngine(
    canonical_handlers=canonical_handlers,
    github_integration=github_integration,
    session_manager=session_manager
)

# Handle query with enhancement
async def handle_enhanced_query(intent, session_id):
    result = await extended_engine.handle_extended_query(
        intent=intent,
        session_id=session_id,
        enhancement_config={
            "compatible_actions": ["list_issues", "search_issues", "get_project_status"],
            "disable_enhancements": False
        }
    )

    if result["enhanced"]:
        print(f"Original response: {result['response']}")
        print(f"Enhanced message: {result['enhanced_message']}")
        print(f"Performance: {result['original_time_ms']}ms original, {result['enhancement_time_ms']}ms enhancement")
    else:
        print(f"Original response only: {result['response']}")
        print(f"Performance: {result['original_time_ms']}ms")

    return result

# Monitor performance
performance_monitor = EnhancementPerformanceMonitor()

async def monitored_query_handler(intent, session_id):
    start_time = datetime.utcnow()

    try:
        result = await extended_engine.handle_extended_query(intent, session_id)

        # Record performance
        performance_monitor.record_query_performance(
            original_time_ms=result.get("original_time_ms", 0),
            enhancement_time_ms=result.get("enhancement_time_ms", 0),
            enhanced=result.get("enhanced", False),
            failed=False
        )

        return result

    except Exception as e:
        total_time = (datetime.utcnow() - start_time).total_seconds() * 1000
        performance_monitor.record_query_performance(
            original_time_ms=total_time,
            enhanced=False,
            failed=True
        )
        raise
```

## Usage Guidelines

### Extension Design Principles

- **Always Delegate First**: Get original response from existing handlers before attempting enhancements
- **Preserve Original Structure**: Never modify the original response structure or data
- **Additive Enhancements**: Make enhancements additive, never subtractive or destructive
- **Graceful Degradation**: Implement fallback behavior when external services are unavailable
- **Performance Isolation**: Track enhancement performance separately from original functionality

### Integration Best Practices

- **Extend, Don't Replace**: Extend existing functionality rather than replacing it entirely
- **Maintain Compatibility**: Ensure existing consumers continue to work without modification
- **Use Dependency Injection**: Enable testability and flexibility through dependency injection
- **Circuit Breaker Protection**: Implement circuit breaker patterns for external service calls
- **Performance Monitoring**: Track enhancement performance and failure rates

### Configuration Management

- **Feature Flags**: Use configuration to enable/disable enhancements per environment
- **Selective Enhancement**: Allow enhancement configuration per intent type or action
- **Performance Thresholds**: Set and monitor performance thresholds for enhancement operations
- **Fallback Configuration**: Define clear fallback behavior for different failure scenarios

## Benefits

- Preserves existing functionality while adding new capabilities
- Maintains backward compatibility with existing consumers
- Enables gradual rollout of enhancements through configuration
- Provides graceful degradation when external services are unavailable
- Allows performance optimization of original and enhanced features separately
- Reduces risk compared to complete system replacement

## Trade-offs

- Additional architectural complexity with delegation and enhancement layers
- Performance overhead from enhancement processing and external service calls
- Dependency management complexity with multiple service integrations
- Need for comprehensive monitoring of both original and enhanced functionality
- Circuit breaker configuration and tuning requirements
- Testing complexity covering both original and enhanced code paths

## Anti-patterns to Avoid

- ❌ **Replacing Original Handlers**: Replacing existing handlers instead of delegating to them
- ❌ **Breaking Original Structure**: Modifying or breaking the original response structure
- ❌ **Failing on Enhancement Errors**: Failing entire queries when enhancements are unavailable
- ❌ **Tight External Coupling**: Creating tight coupling to external enhancement services
- ❌ **Missing Performance Monitoring**: Not tracking performance impact of enhancements
- ❌ **No Graceful Degradation**: Missing fallback behavior for enhancement failures

## Related Patterns

- [Pattern-004: CQRS-lite Pattern](pattern-004-cqrs-lite.md) - Query routing foundation for canonical handlers
- [Pattern-017: Background Task Error Handling Pattern](pattern-017-background-task-error-handling.md) - Circuit breaker implementation
- [Pattern-022: MCP+Spatial Intelligence Integration Pattern](pattern-022-mcp-spatial-intelligence-integration.md) - External service integration
- [Pattern-023: Query Layer Patterns](pattern-023-query-layer-patterns.md) - Query system architecture

## References

- **Implementation**: IssueIntelligenceCanonicalQueryEngine with GitHub integration
- **Usage Evidence**: Canonical query extension with issue intelligence enhancement
- **Performance Monitoring**: EnhancementPerformanceMonitor and circuit breaker protection
- **Related ADR**: External service integration patterns and graceful degradation strategies

## Migration Notes

_Consolidated from:_

- `pattern-catalog.md#25-canonical-query-extension-pattern` - Complete extension framework with GitHub issue intelligence
- Delegation-first approach preserving existing canonical handler functionality
- Performance monitoring and circuit breaker protection for external service integration
- Graceful degradation patterns for enhanced query systems

_Last updated: September 15, 2025_
