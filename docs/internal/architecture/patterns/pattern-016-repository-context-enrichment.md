# Pattern-016: Repository Context Enrichment Pattern

## Status

**Proven**

## Context

Workflow systems that integrate with external services like GitHub require repository context for operations like ticket creation, but requiring users to explicitly provide repository information every time creates friction and reduces usability. Without automatic context enrichment, workflows either fail due to missing information or force users to repeatedly provide the same contextual data. The Repository Context Enrichment Pattern addresses:

- Reducing user friction by automatically providing required context
- Enabling seamless integration workflows without explicit repository specification
- Supporting multiple integration types through extensible enrichment logic
- Maintaining workflow reliability when context enrichment fails
- Centralizing context management for consistency across workflows
- Enabling downstream handlers to access necessary repository information

## Pattern Description

The Repository Context Enrichment Pattern automatically enriches workflow context with repository information and other required contextual data, enabling seamless integration workflows. The pattern intercepts workflow creation, identifies workflows that require specific context (like repository information), attempts to enrich the context from available sources, and gracefully handles enrichment failures to maintain workflow reliability.

## Implementation

### Structure

```python
# Repository context enrichment framework
class ContextEnrichmentEngine:
    def __init__(self, project_context: ProjectContext):
        self.project_context = project_context
        self.enrichers = []

    def register_enricher(self, enricher: ContextEnricher):
        """Register context enricher for specific workflow types"""
        self.enrichers.append(enricher)

    async def enrich_workflow_context(self, intent: Intent) -> Dict[str, Any]:
        """Apply context enrichment based on workflow type"""
        pass

    def get_repository_context(self) -> Optional[RepositoryInfo]:
        """Extract repository context from project"""
        pass
```

### Example (GitHub Repository Enrichment)

```python
from typing import Dict, Any, Optional
import structlog

logger = structlog.get_logger()

class GitHubRepositoryEnricher:
    """Enriches workflow context with GitHub repository information"""

    def __init__(self, project_context: ProjectContext):
        self.project_context = project_context

    def can_enrich(self, intent: Intent) -> bool:
        """Check if this enricher applies to the given intent"""
        return intent.type in [
            WorkflowType.CREATE_TICKET,
            WorkflowType.CREATE_ISSUE,
            WorkflowType.ANALYZE_REPOSITORY
        ]

    async def enrich_context(self, intent: Intent) -> Dict[str, Any]:
        """Enrich context with repository information"""
        context = dict(intent.context)

        if not self.can_enrich(intent):
            return context

        try:
            # Attempt to get repository from project context
            repo = await self.project_context.get_github_repository()
            if repo:
                context["repository"] = {
                    "owner": repo.owner,
                    "name": repo.name,
                    "full_name": repo.full_name,
                    "url": repo.url
                }
                logger.info(
                    "Repository context enriched",
                    workflow_type=intent.type,
                    repository=repo.full_name
                )
            else:
                logger.warning(
                    "No GitHub repository found for project",
                    project_id=self.project_context.id,
                    workflow_type=intent.type
                )
        except Exception as e:
            logger.error(
                "Failed to enrich context with repository",
                error=str(e),
                workflow_type=intent.type,
                project_id=self.project_context.id
            )
            # Don't fail the workflow - proceed without enrichment

        return context

def create_workflow_from_intent(intent: Intent, project_context: ProjectContext):
    """
    Create workflow with enriched context for seamless integrations.
    This pattern ensures downstream handlers have necessary context.
    """
    # Initialize enrichment engine
    enricher = GitHubRepositoryEnricher(project_context)

    # Enrich context based on workflow type
    enriched_context = await enricher.enrich_context(intent)

    # Create workflow with enriched context
    workflow = Workflow(
        type=intent.type,
        context=enriched_context,
        metadata={
            "enrichment_applied": True,
            "enrichment_timestamp": datetime.utcnow().isoformat()
        }
    )

    logger.info(
        "Workflow created with context enrichment",
        workflow_type=intent.type,
        context_keys=list(enriched_context.keys())
    )

    return workflow
```

### Example (Multi-Integration Enrichment)

```python
class MultiIntegrationEnricher:
    """Supports multiple integration types through extensible enrichment"""

    def __init__(self, project_context: ProjectContext):
        self.project_context = project_context
        self.enrichers = {
            'github': GitHubRepositoryEnricher(project_context),
            'notion': NotionWorkspaceEnricher(project_context),
            'slack': SlackChannelEnricher(project_context)
        }

    async def enrich_workflow_context(self, intent: Intent) -> Dict[str, Any]:
        """Apply all applicable enrichers to workflow context"""
        context = dict(intent.context)

        for enricher_name, enricher in self.enrichers.items():
            try:
                if enricher.can_enrich(intent):
                    enriched = await enricher.enrich_context(intent)
                    context.update(enriched)
                    logger.debug(
                        "Applied context enricher",
                        enricher=enricher_name,
                        workflow_type=intent.type
                    )
            except Exception as e:
                logger.error(
                    "Context enricher failed",
                    enricher=enricher_name,
                    error=str(e),
                    workflow_type=intent.type
                )
                # Continue with other enrichers

        return context

# Centralized workflow factory with enrichment
class EnrichedWorkflowFactory:
    def __init__(self, project_context: ProjectContext):
        self.enricher = MultiIntegrationEnricher(project_context)

    async def create_workflow(self, intent: Intent) -> Workflow:
        """Create workflow with automatic context enrichment"""
        enriched_context = await self.enricher.enrich_workflow_context(intent)

        return Workflow(
            type=intent.type,
            context=enriched_context,
            created_at=datetime.utcnow()
        )
```

## Usage Guidelines

### When to Use Repository Context Enrichment

- **Integration Workflows**: Workflows that interact with external services requiring repository context
- **User Experience Optimization**: Reducing friction by eliminating repetitive context input
- **Multi-Project Environments**: When projects have associated repositories that should be automatically resolved
- **Workflow Automation**: Enabling seamless automation without manual context specification
- **Cross-Service Operations**: When workflows span multiple services requiring consistent context

### Enrichment Strategy Best Practices

- **Workflow Type Mapping**: Clearly define which workflow types require which context enrichment
- **Graceful Degradation**: Never fail workflows due to enrichment failures - log and proceed
- **Centralized Logic**: Keep enrichment logic centralized in workflow factories or orchestration engines
- **Extensible Design**: Support multiple integration types through pluggable enrichers
- **Context Documentation**: Document expected context flow for maintainers and integrators

### Error Handling Best Practices

- **Non-Blocking Failures**: Enrichment failures should not prevent workflow execution
- **Comprehensive Logging**: Log enrichment attempts, successes, and failures with context
- **Fallback Mechanisms**: Provide fallback strategies when primary enrichment fails
- **User Feedback**: Inform users when context enrichment affects workflow behavior
- **Monitoring**: Track enrichment success rates for system health monitoring

### Anti-Patterns to Avoid

- **Forced User Input**: Requiring users to specify repository information every time
- **Hardcoded Context**: Embedding repository or integration context directly in workflow logic
- **Blocking Failures**: Failing entire workflows when context enrichment encounters errors
- **Scattered Logic**: Distributing enrichment logic across multiple modules without coordination
- **Silent Failures**: Failing to log or report context enrichment issues
- **Over-Enrichment**: Adding unnecessary context that increases complexity without benefit

## Benefits

- Reduces user friction by eliminating repetitive context input
- Enables seamless integration workflows without manual repository specification
- Supports multiple integration types through extensible enrichment logic
- Maintains workflow reliability through graceful degradation
- Centralizes context management for consistency across workflows
- Improves automation capabilities for cross-service operations

## Trade-offs

- Additional complexity in workflow creation and management
- Potential for incorrect context enrichment leading to wrong operations
- Performance overhead from enrichment logic execution
- Dependency on reliable project context and repository mapping
- Debugging complexity when enrichment fails silently
- Need for comprehensive testing of enrichment scenarios

## Related Patterns

- [Pattern-002: Service Pattern](pattern-002-service.md) - Service integration architecture
- [Pattern-003: Factory Pattern](pattern-003-factory.md) - Workflow creation with enrichment
- [Pattern-008: DDD Service Layer](pattern-008-ddd-service-layer.md) - Domain service context management
- [Pattern-007: Async Error Handling](pattern-007-async-error-handling.md) - Enrichment error handling

## Migration Notes (for consolidation from legacy systems)

- **From `pattern-catalog.md`**: Section 16 "Repository Context Enrichment Pattern" - comprehensive implementation and usage guidelines
- **From `PATTERN-INDEX.md`**: No direct equivalent found - this is a workflow-specific pattern
- **From codebase**: Implementation examples in workflow orchestration and GitHub integration services
- **Consolidation Strategy**: Expanded pattern-catalog.md content with additional error handling, multi-integration support, and comprehensive usage guidelines

## Quality Assurance Checklist

- [x] Pattern description is clear and concise
- [x] Context explains problem and applicability
- [x] Implementation examples are provided and correct
- [x] Usage guidelines are comprehensive
- [x] Related patterns are linked
- [x] All information from source catalog is preserved
- [x] Follows ADR-style numbering and naming conventions

## Agent Coordination Notes

- **Agent A (Code)**: Responsible for workflow orchestration and integration service implementation
- **Agent B (Cursor)**: Responsible for pattern documentation and usage guideline validation
- **Integration Points**: Workflow factories, context enrichment engines, and integration services

## References

- Original catalog: `docs/architecture/pattern-catalog.md#16-repository-context-enrichment-pattern`
- Workflow orchestration: `services/orchestration/`
- GitHub integration: `services/integrations/github/`
- Project context: `services/project/context.py`

_Last updated: September 15, 2025_
