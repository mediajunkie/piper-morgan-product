# Pattern-007: Async Error Handling Pattern

## Status

**Proven**

## Context

Asynchronous operations in modern applications introduce complex error handling challenges where failures can occur at multiple points in the execution pipeline. Traditional synchronous error handling patterns don't adequately address async contexts where errors may be deferred, propagated across async boundaries, or lost in concurrent operations. The Async Error Handling Pattern addresses:

- Proper error propagation in async/await contexts
- Graceful degradation when async operations fail
- User-friendly error reporting for async failures
- Recovery guidance for failed async operations
- Structured exception handling across async boundaries

## Pattern Description

The Async Error Handling Pattern provides systematic error management for asynchronous operations through structured exception hierarchies, graceful degradation mechanisms, and user-friendly error reporting.

**Core Principle**: "Errors should be user-friendly, actionable, and provide clear recovery guidance, even in async contexts."

**Error Handling Model**:
```
Async Request → Processing → Error Detection → Classification → User Response → Recovery Guidance
```

**Key Components**:
- Structured exception hierarchy for async operations
- User-friendly error messages with context
- Recovery guidance for failed operations
- API contract compliance across async endpoints
- Graceful degradation for non-critical failures

## Implementation

### Structure

```python
# Base error hierarchy for async operations
class APIError(Exception):
    """Base class for all application-specific API errors."""

    def __init__(self, status_code: int, error_code: str, details: Dict[str, Any] = None):
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        super().__init__(f"API Error [{error_code}]")

class AsyncOperationError(APIError):
    """Base class for async operation failures."""

    def __init__(self, operation: str, details: Dict[str, Any] = None):
        super().__init__(500, f"ASYNC_{operation.upper()}_FAILED", details)
        self.operation = operation

class IntentClassificationFailedError(AsyncOperationError):
    """Raised when async intent classification fails."""

    def __init__(self, query: str, details: Dict[str, Any] = None):
        super().__init__("INTENT_CLASSIFICATION", {
            "query": query,
            "suggestion": "Try rephrasing your request more clearly",
            **(details or {})
        })
```

### Code Example

```python
import asyncio
import logging
from typing import Optional, Dict, Any

class AsyncErrorHandler:
    """Centralized async error handling with graceful degradation."""

    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)

    async def handle_async_operation(
        self,
        operation: Callable,
        fallback: Optional[Callable] = None,
        context: Dict[str, Any] = None
    ) -> Any:
        """Execute async operation with error handling and optional fallback."""

        try:
            result = await operation()
            self.logger.info(f"Async operation succeeded: {context}")
            return result

        except APIError as e:
            # Known API errors - provide structured response
            self.logger.error(f"API error in async operation: {e.error_code}",
                            extra={"context": context, "details": e.details})

            if fallback:
                try:
                    fallback_result = await fallback()
                    self.logger.info("Fallback operation succeeded")
                    return fallback_result
                except Exception as fallback_error:
                    self.logger.error(f"Fallback also failed: {fallback_error}")

            raise e

        except asyncio.TimeoutError:
            # Timeout handling with recovery guidance
            timeout_error = AsyncOperationError("TIMEOUT", {
                "context": context,
                "suggestion": "Try again in a few moments or check system status"
            })
            self.logger.error("Async operation timed out", extra={"context": context})
            raise timeout_error

        except Exception as e:
            # Unexpected errors - wrap in structured format
            unexpected_error = AsyncOperationError("UNEXPECTED", {
                "original_error": str(e),
                "context": context,
                "suggestion": "Please report this issue to support"
            })
            self.logger.error(f"Unexpected error in async operation: {e}",
                            extra={"context": context}, exc_info=True)
            raise unexpected_error

# Usage example
async def process_user_request_with_error_handling(request: Dict[str, Any]) -> Dict[str, Any]:
    """Process user request with comprehensive async error handling."""

    error_handler = AsyncErrorHandler()

    async def main_operation():
        # Main async processing logic
        intent = await classify_intent(request["query"])
        response = await generate_response(intent, request)
        return {"status": "success", "response": response}

    async def fallback_operation():
        # Fallback when main operation fails
        return {
            "status": "degraded",
            "response": "I'm having trouble processing your request. Please try again.",
            "recovery_actions": ["Rephrase your request", "Check system status", "Contact support"]
        }

    return await error_handler.handle_async_operation(
        operation=main_operation,
        fallback=fallback_operation,
        context={"request_id": request.get("id"), "user": request.get("user")}
    )
```

### Configuration

```yaml
# Async Error Handling Configuration
error_handling:
  async:
    timeout_seconds: 30
    max_retries: 3
    retry_delay_seconds: 1

  graceful_degradation:
    enabled: true
    fallback_timeout_seconds: 10

  logging:
    log_all_errors: true
    include_stack_traces: true
    log_recovery_attempts: true

  user_messages:
    include_recovery_guidance: true
    technical_details: false
    contact_support_threshold: 3
```

## Usage Guidelines

### When to Use

- **Async Operations**: All asynchronous function calls and operations
- **External API Calls**: HTTP requests, database operations, file I/O
- **User-Facing Async Features**: Real-time updates, background processing
- **Multi-Step Async Workflows**: Complex operations with multiple async steps
- **Timeout-Sensitive Operations**: Operations with time constraints

### When NOT to Use

- **Synchronous Operations**: Use standard exception handling for sync code
- **Simple Internal Functions**: Basic utility functions without external dependencies
- **Performance-Critical Paths**: Where error handling overhead is prohibitive
- **Fire-and-Forget Operations**: Background tasks where failures are acceptable

### Best Practices

- **Structured Exception Hierarchy**: Use specific error types for different failure modes
- **Context Preservation**: Include relevant context in error details
- **User-Friendly Messages**: Provide actionable error messages for end users
- **Graceful Degradation**: Implement fallback mechanisms where possible
- **Comprehensive Logging**: Log errors with sufficient detail for debugging
- **Recovery Guidance**: Always provide clear next steps for users

## Examples in Codebase

### Primary Usage

- `services/api/error_handlers.py` - Central async error handling
- `services/integrations/*/client.py` - External API error handling
- `services/orchestration/workflow_engine.py` - Workflow error management

### Test Examples

- `tests/patterns/test_async_error_handling.py` - Pattern implementation tests
- `tests/integration/test_error_recovery.py` - End-to-end error recovery testing

## Related Patterns

### Complements

- [Pattern-006: Verification-First](pattern-006-verification-first.md) - Prevents errors through verification
- [Pattern-008: DDD Service Layer](pattern-008-ddd-service-layer.md) - Domain-specific error handling

### Alternatives

- **Fail-Fast Pattern**: Immediate failure without recovery attempts
- **Circuit Breaker Pattern**: Prevents cascading failures in distributed systems

### Dependencies

- **Logging Infrastructure**: Required for error tracking and debugging
- **Configuration Management**: Needed for error handling parameters

## Migration Notes

*Consolidated from multiple sources*

### From PATTERN-INDEX.md

- **Status**: ✅ Proven pattern in production use
- **Location**: `services/` directory with domain exceptions
- **Usage**: HTTP status codes, domain-specific exceptions
- **Related ADR**: Error handling framework architectural decision

### From error-handling-framework.md

- **Pattern Strength**: 14/16 (High Strength) - indicates reliable production use
- **Core Components**: Structured exception hierarchy, user-friendly messages, recovery guidance
- **Framework Model**: Complete error lifecycle from detection to recovery
- **Production Status**: Proven effective across multiple system components

## References

### Documentation

- **Original source**: `docs/patterns/archive/PATTERN-INDEX-legacy.md#error-handling-pattern`
- **Framework source**: `docs/internal/archive/piper-education-2025/frameworks/emergent/error-handling-framework.md` (archived Feb 2026)
- **Related patterns**: Verification-First Pattern, Configuration Management Framework

### Usage Analysis

- **Current usage**: Core pattern across API endpoints, external integrations, workflow processing
- **Pattern strength**: 14/16 high strength rating
- **Status**: Production proven, actively maintained
- **Last updated**: September 15, 2025

---

*Pattern extracted and consolidated: September 15, 2025*
*Agent B (Cursor) - Pattern Catalog Consolidation Project*
