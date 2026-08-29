# Pattern-003: Factory Pattern

## Status

**Proven**

## Context

Complex object creation logic scattered throughout the codebase creates maintenance challenges and makes testing difficult. When objects require intricate setup or context-specific configuration, direct instantiation becomes unwieldy. The Factory Pattern addresses:

- What challenges does this solve? Encapsulates object creation logic and provides stateless, thread-safe object creation
- When should this pattern be considered? When object creation involves complex logic, multiple dependencies, or context-specific setup
- What are the typical scenarios where this applies? Workflow creation, service instantiation, complex domain object construction

## Pattern Description

The Factory Pattern creates complex objects without exposing construction logic, maintaining stateless design for concurrency safety.

Core concept:
- Stateless factory classes with no instance state
- All context passed as method parameters per call
- Supports concurrent creation safely
- Makes object dependencies explicit

## Implementation

### Structure

```python
class WorkflowFactory:
    """Stateless factory - all context passed per-call"""

    def __init__(self):
        self.workflow_registry = {}
        self._register_default_workflows()

    async def create_from_intent(
        self,
        intent: Intent,
        session_id: str,
        project_context: Optional[ProjectContext] = None
    ) -> Optional[Workflow]:
        """Create workflow with per-call context injection"""
        # No instance state used - all data from parameters

        if project_context:
            project, needs_confirm = await project_context.resolve_project(
                intent, session_id
            )
            intent.context.update({
                "project_id": project.id,
                "project_name": project.name
            })

        workflow_class = self._match_workflow(intent)
        return workflow_class(context=intent.context) if workflow_class else None

    def _match_workflow(self, intent: Intent) -> Optional[Type[Workflow]]:
        """Private helper for workflow selection"""
        for pattern, workflow_class in self.workflow_registry.items():
            if pattern.matches(intent):
                return workflow_class
        return None

    def _register_default_workflows(self):
        """Register available workflow types"""
        self.workflow_registry = {
            CreateIssuePattern(): CreateIssueWorkflow,
            QueryKnowledgePattern(): QueryKnowledgeWorkflow,
            ReviewIssuePattern(): ReviewIssueWorkflow,
        }
```

### Factory with Dependency Injection

```python
class ServiceFactory:
    """Factory for service objects with dependency injection"""

    def __init__(self, session: AsyncSession):
        self.session = session

    def create_intent_service(self) -> IntentService:
        """Create IntentService with all dependencies"""
        project_repo = ProjectRepository(self.session)
        workflow_service = self.create_workflow_service()
        return IntentService(project_repo, workflow_service)

    def create_workflow_service(self) -> WorkflowService:
        """Create WorkflowService with dependencies"""
        workflow_repo = WorkflowRepository(self.session)
        return WorkflowService(workflow_repo)
```

### Usage Example

```python
async def workflow_handler(intent: Intent, session_id: str):
    """Handler using factory for object creation"""
    async with AsyncSessionFactory.session_scope() as session:
        # Factory creates complex object with proper setup
        workflow_factory = WorkflowFactory()
        project_context = ProjectContext(session)

        workflow = await workflow_factory.create_from_intent(
            intent, session_id, project_context
        )

        if workflow:
            return await workflow.execute()
        else:
            raise UnsupportedIntentError("No workflow found for intent")
```

## Usage Guidelines

- Pass all context as method parameters (no instance state for request data)
- No instance variables for request-specific data
- Support concurrent creation safely
- Make dependencies explicit in factory methods
- Keep creation logic encapsulated and testable

## Benefits

- Encapsulated object creation logic
- Thread-safe and stateless design
- Makes complex construction simple for clients
- Easy to test and mock
- Supports different object configurations

## Trade-offs

- Additional abstraction layer
- Can become complex with many object types
- May be overkill for simple object creation
- Requires careful design to avoid hidden dependencies

## Anti-patterns to Avoid

- ❌ Storing request context in factory instance
- ❌ Stateful factories that require reset between uses
- ❌ Hidden dependencies through instance state
- ❌ Thread-unsafe shared state

## Related Patterns

- [Pattern-002: Service Pattern](pattern-002-service.md) - Services often created by factories
- [Pattern-001: Repository Pattern](pattern-001-repository.md) - Repositories may be factory-created
- [Pattern-004: CQRS-lite Pattern](pattern-004-cqrs-lite.md) - Command/query handlers may use factories

## References

- **Implementation**: `services/orchestration/workflow_factory.py`
- **Usage Example**: WorkflowFactory.create_from_intent()
- **Related ADR**: None (core architectural principle)

## Migration Notes

*Consolidated from:*
- `pattern-catalog.md#2-factory-pattern-stateless` - Implementation details and anti-patterns
- `archive/PATTERN-INDEX-legacy.md#factory-pattern` - Status and location information
