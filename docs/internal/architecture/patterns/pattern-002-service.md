# Pattern-002: Service Pattern

## Status

**Proven**

## Context

Business logic scattered throughout controllers, repositories, or domain models creates maintenance challenges and violates single responsibility principle. The Service Pattern addresses:

- What challenges does this solve? Encapsulates business logic in dedicated service classes with clear boundaries
- When should this pattern be considered? When you have complex business operations that involve multiple repositories or external services
- What are the typical scenarios where this applies? Intent processing, workflow orchestration, authentication, complex business rules

## Pattern Description

The Service Pattern encapsulates business logic in dedicated service classes, providing a clear separation between controllers/handlers and data access layers.

Core concept:
- Services contain business logic and orchestrate operations
- Each service has a single, well-defined responsibility
- Services coordinate between repositories, external APIs, and other services
- Clean interface for complex business operations

## Implementation

### Structure

```python
class IntentService:
    """Service for intent processing business logic"""

    def __init__(self, project_repo: ProjectRepository, workflow_service: WorkflowService):
        self.project_repo = project_repo
        self.workflow_service = workflow_service

    async def process_intent(self, intent: Intent) -> WorkflowResult:
        """Business logic for intent processing"""
        # Validate intent
        if not self._is_valid_intent(intent):
            raise InvalidIntentError("Intent validation failed")

        # Load project context
        project = await self.project_repo.get_by_id(intent.project_id)
        if not project:
            raise ProjectNotFoundError("Project not found")

        # Orchestrate workflow
        workflow = await self.workflow_service.create_workflow(intent, project)
        return await self.workflow_service.execute(workflow)

    def _is_valid_intent(self, intent: Intent) -> bool:
        """Private business logic helper"""
        return intent.message and intent.project_id
```

### Service Dependency Injection

```python
class ServiceContainer:
    """Dependency injection for services"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self._services = {}

    def get_intent_service(self) -> IntentService:
        if 'intent' not in self._services:
            project_repo = ProjectRepository(self.session)
            workflow_service = self.get_workflow_service()
            self._services['intent'] = IntentService(project_repo, workflow_service)
        return self._services['intent']

    def get_workflow_service(self) -> WorkflowService:
        if 'workflow' not in self._services:
            self._services['workflow'] = WorkflowService(self.session)
        return self._services['workflow']
```

### Service Usage in Handlers

```python
async def handle_intent_request(request: IntentRequest) -> IntentResponse:
    """Handler delegates business logic to service"""
    async with AsyncSessionFactory.session_scope() as session:
        container = ServiceContainer(session)
        intent_service = container.get_intent_service()

        try:
            result = await intent_service.process_intent(request.intent)
            return IntentResponse(success=True, result=result)
        except (InvalidIntentError, ProjectNotFoundError) as e:
            return IntentResponse(success=False, error=str(e))
```

## Usage Guidelines

- One service per business domain or use case
- Services should not directly access the database (use repositories)
- Keep services focused on business logic, not data access or presentation
- Use dependency injection for service dependencies
- Services can call other services but avoid circular dependencies

## Benefits

- Clear separation of business logic
- Testable business operations
- Reusable business logic across different interfaces
- Single responsibility principle adherence
- Easy to mock for testing

## Trade-offs

- Additional abstraction layer
- Potential over-engineering for simple CRUD operations
- Service coordination complexity for large operations
- Dependency management overhead

## Related Patterns

- [Pattern-001: Repository Pattern](pattern-001-repository.md) - Data access layer used by services
- [Pattern-003: Factory Pattern](pattern-003-factory.md) - Object creation for service dependencies
- [Pattern-004: CQRS-lite Pattern](pattern-004-cqrs-lite.md) - Command/query separation in services

## References

- **Implementation**: `services/*/service.py`
- **Usage Examples**: IntentService, WorkflowService, AuthService
- **Related ADR**: None (core architectural principle)

## Migration Notes

*Consolidated from:*
- `archive/PATTERN-INDEX-legacy.md#service-pattern` - Status, location, and usage examples
- Common service pattern practices - Implementation structure and guidelines
