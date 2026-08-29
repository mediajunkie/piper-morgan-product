# Pattern-008: DDD Service Layer Pattern

## Status

**Proven**

## Context

Direct access to integration layers from application code creates tight coupling, makes testing difficult, and violates Domain-Driven Design principles. When application layers directly call external services, databases, or APIs, the domain becomes polluted with infrastructure concerns and loses its focus on business logic. The DDD Service Layer Pattern addresses:

- Mediating between application layer and integration layer
- Maintaining clean domain boundaries and separation of concerns
- Providing domain-specific interfaces for external system access
- Translating integration exceptions to domain exceptions
- Enabling dependency injection and testability
- Following DDD principles for layered architecture

## Pattern Description

The DDD Service Layer Pattern creates domain services that mediate all external system access, providing clean domain interfaces while encapsulating integration complexity. Domain services act as gatekeepers that:

**Core Principle**: "Domain services mediate external system access while maintaining clean domain boundaries."

**Layer Architecture**:
```
Application Layer → Domain Service → Integration Layer → External System
```

**Key Responsibilities**:
- **Mediation**: Translate between domain concepts and integration specifics
- **Error Translation**: Convert integration exceptions to domain exceptions
- **Interface Abstraction**: Provide domain-focused method signatures
- **Lifecycle Management**: Handle integration agent initialization and configuration
- **Logging & Monitoring**: Domain-aware logging for operations

## Implementation

### Structure

```python
from typing import Any, Dict, List, Optional
import structlog
from services.api.errors import DomainServiceError
from services.integrations.external.external_agent import ExternalAgent

logger = structlog.get_logger()

class ExternalDomainService:
    """
    Domain service for external system operations mediation

    Encapsulates external integration access following DDD principles:
    - Mediates between application layer and integration layer
    - Provides clean domain interface for external operations
    - Handles integration-specific error translation to domain exceptions
    - Manages external agent lifecycle and configuration
    """

    def __init__(self, external_agent: Optional[ExternalAgent] = None):
        """Initialize with optional agent injection for testability"""
        try:
            self._external_agent = external_agent or ExternalAgent()
            logger.info(
                "External domain service initialized",
                agent_type=type(self._external_agent).__name__
            )
        except Exception as e:
            logger.error("Failed to initialize external domain service", error=str(e))
            raise DomainServiceInitializationError(f"External service initialization failed: {e}")

    async def domain_operation(self, domain_param: str) -> Dict[str, Any]:
        """Domain-focused operation that mediates external system access"""
        try:
            # Translate domain parameters to integration parameters
            integration_params = self._translate_to_integration(domain_param)

            # Call integration layer
            result = await self._external_agent.integration_operation(integration_params)

            # Translate integration result to domain result
            return self._translate_to_domain(result)

        except IntegrationSpecificError as e:
            logger.error("Integration operation failed", domain_param=domain_param, error=str(e))
            raise DomainOperationFailedError(f"Domain operation failed: {e}")
        except Exception as e:
            logger.error("Unexpected error in domain service", error=str(e))
            raise
```

### Code Example

```python
# Real example: GitHub Domain Service
class GitHubDomainService:
    """Domain service for GitHub operations mediation"""

    def __init__(self, github_agent: Optional[GitHubAgent] = None):
        """Initialize with optional GitHub agent injection"""
        try:
            self._github_agent = github_agent or GitHubAgent()
            logger.info(
                "GitHub domain service initialized",
                agent_type=type(self._github_agent).__name__
            )
        except Exception as e:
            logger.error("Failed to initialize GitHub domain service", error=str(e))
            raise

    async def get_recent_issues(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent GitHub issues for domain consumption"""
        try:
            return await self._github_agent.get_recent_issues(limit)
        except GitHubAuthFailedError:
            logger.error("GitHub authentication failed for recent issues")
            raise
        except GitHubRateLimitError:
            logger.warning("GitHub rate limit exceeded for recent issues")
            raise
        except Exception as e:
            logger.error("GitHub recent issues retrieval failed", error=str(e))
            raise

    async def create_issue(self, title: str, description: str, labels: List[str] = None) -> Dict[str, Any]:
        """Create GitHub issue with domain-focused interface"""
        try:
            # Domain-to-integration translation
            issue_data = {
                "title": title,
                "body": description,
                "labels": labels or []
            }

            result = await self._github_agent.create_issue(issue_data)
            logger.info("GitHub issue created successfully", issue_id=result.get("id"))
            return result

        except GitHubAuthFailedError:
            logger.error("GitHub authentication failed for issue creation")
            raise
        except Exception as e:
            logger.error("GitHub issue creation failed", error=str(e))
            raise

# Usage in application layer
class StandupOrchestrationService:
    """Application service using domain services"""

    def __init__(self, github_service: Optional[GitHubDomainService] = None):
        self.github_service = github_service or GitHubDomainService()

    async def get_github_activity(self) -> Dict[str, Any]:
        """Get GitHub activity through domain service mediation"""
        try:
            # Application layer calls domain service, not integration directly
            recent_issues = await self.github_service.get_recent_issues(limit=5)
            return {"github_activity": recent_issues}
        except GitHubAuthFailedError:
            return {"github_activity": "Authentication required"}
        except Exception as e:
            logger.error("Failed to get GitHub activity", error=str(e))
            return {"github_activity": "Error retrieving activity"}
```

### Configuration

```yaml
# DDD Service Layer Configuration
domain_services:
  github:
    enabled: true
    agent_type: "GitHubAgent"
    retry_attempts: 3
    timeout_seconds: 30

  slack:
    enabled: true
    agent_type: "SlackAgent"
    fallback_enabled: true

  notion:
    enabled: false
    agent_type: "NotionAgent"

logging:
  domain_operations: true
  integration_calls: true
  error_translation: true
```

## Usage Guidelines

### When to Use

- **External System Access**: Any interaction with external APIs, databases, services
- **DDD Architecture**: When implementing Domain-Driven Design layered architecture
- **Integration Abstraction**: Need to abstract complex integration logic from application
- **Testing Requirements**: When domain logic needs to be testable without external dependencies
- **Error Boundary Management**: Need consistent error handling across external operations

### When NOT to Use

- **Simple Internal Operations**: Pure domain logic that doesn't involve external systems
- **Direct Database Access**: Use Repository pattern for data access instead
- **Utility Functions**: Simple helper functions that don't mediate external access
- **Performance-Critical Paths**: Where additional abstraction layer impacts performance significantly

### Best Practices

- **Single Responsibility**: Each domain service should mediate one external system
- **Dependency Injection**: Accept integration agents as optional parameters for testability
- **Error Translation**: Convert integration-specific errors to domain exceptions
- **Domain-Focused Interface**: Method signatures should reflect domain concepts, not integration details
- **Comprehensive Logging**: Log domain operations with business context
- **Clean Boundaries**: Never expose integration-specific types in domain service interfaces

## Examples in Codebase

### Primary Usage

- `services/domain/github_domain_service.py` - GitHub operations mediation
- `services/domain/slack_domain_service.py` - Slack integration mediation
- `services/domain/notion_domain_service.py` - Notion database operations
- `services/domain/standup_orchestration_service.py` - Multi-service orchestration

### Test Examples

- `tests/domain/test_github_domain_service.py` - Domain service unit tests
- `tests/integration/test_domain_service_integration.py` - Integration testing

## Related Patterns

### Complements

- [Pattern-001: Repository Pattern](pattern-001-repository.md) - Data access mediation
- [Pattern-002: Service Pattern](pattern-002-service.md) - Business logic organization
- [Pattern-007: Async Error Handling](pattern-007-async-error-handling.md) - Error management in async operations

### Alternatives

- **Direct Integration Access**: Calling integration layers directly (violates DDD)
- **Facade Pattern**: Similar abstraction but without domain focus

### Dependencies

- **Integration Layer**: Requires well-defined integration agents/clients
- **Error Handling Framework**: Needs structured exception hierarchy
- **Logging Infrastructure**: Required for domain operation tracking

## Migration Notes

*Consolidated from codebase analysis and DDD implementation*

### From services/domain/ implementation

- **Creation Context**: Created 2025-09-12 during DDD refactoring to address architectural violations
- **Problem Addressed**: Direct GitHub integration access from CLI/features/main layers
- **Implementation Pattern**: All domain services follow consistent mediation pattern
- **Error Handling**: Structured exception translation from integration to domain errors

### From architectural refactoring

- **DDD Compliance**: Part of broader DDD architecture implementation
- **Layer Separation**: Enforces clean boundaries between application and integration layers
- **Testability**: Enables dependency injection for testing without external dependencies

## References

### Documentation

- **Implementation**: `services/domain/*.py` - All domain service implementations
- **Related ADRs**: DDD architecture decisions, layer separation principles
- **Architecture**: Domain-driven design layered architecture documentation

### Usage Analysis

- **Current usage**: Core pattern for all external system access
- **Implementation count**: 6+ domain services (GitHub, Slack, Notion, Standup, User Preferences, PM Number)
- **Status**: Production proven, actively maintained
- **Last updated**: September 15, 2025

---

*Pattern extracted and consolidated: September 15, 2025*
*Agent B (Cursor) - Pattern Catalog Consolidation Project*
