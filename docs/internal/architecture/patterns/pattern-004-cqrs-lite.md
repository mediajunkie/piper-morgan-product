# Pattern-004: CQRS-lite Pattern

## Status

**Proven**

## Context

Mixing read and write operations in the same service classes creates performance bottlenecks and complexity. When query operations have different optimization requirements than command operations, a unified approach becomes inefficient. The CQRS-lite Pattern addresses:

- What challenges does this solve? Separates read operations (queries) from write operations (commands) for optimized performance
- When should this pattern be considered? When read and write patterns differ significantly in complexity or performance requirements
- What are the typical scenarios where this applies? Data retrieval optimizations, complex reporting, simple CRUD separation

## Pattern Description

CQRS-lite Pattern separates read operations from write operations, providing optimized paths for simple data retrieval without the full complexity of CQRS event sourcing.

Core concept:
- Separate query services for read operations
- Workflow engine handles write operations (commands)
- Query router directs read requests to appropriate services
- Lightweight separation without event sourcing complexity

## Implementation

### Query Side Structure

```python
class QueryRouter:
    """Routes query intents to appropriate services"""

    def __init__(self, project_repository: ProjectRepository):
        self.project_queries = ProjectQueryService(project_repository)

    async def route_query(self, intent: Intent) -> QueryResult:
        if intent.action == "list_projects":
            projects = await self.project_queries.list_active_projects()
            return QueryResult(
                success=True,
                data={"projects": [p.to_dict() for p in projects]}
            )
        elif intent.action == "get_project":
            project = await self.project_queries.get_project(intent.project_id)
            return QueryResult(
                success=True,
                data={"project": project.to_dict() if project else None}
            )
        # Route other queries...

class ProjectQueryService:
    """Handles project-related queries"""

    def __init__(self, repository: ProjectRepository):
        self.repo = repository

    async def list_active_projects(self) -> List[Project]:
        """Optimized read-only project listing"""
        return await self.repo.list_active_projects()

    async def get_project(self, project_id: str) -> Optional[Project]:
        """Simple project retrieval"""
        return await self.repo.get_by_id(project_id)
```

### Command Side Structure

```python
class WorkflowEngine:
    """Handles write operations (commands)"""

    def __init__(self, project_repo: ProjectRepository, workflow_factory: WorkflowFactory):
        self.project_repo = project_repo
        self.workflow_factory = workflow_factory

    async def execute_command(self, intent: Intent) -> WorkflowResult:
        """Process write operations through workflows"""
        workflow = await self.workflow_factory.create_from_intent(intent)
        if workflow:
            return await workflow.execute()
        else:
            raise UnsupportedCommandError("No workflow found for command")
```

### Integration Pattern

```python
class IntentProcessor:
    """Main processor that routes to query or command side"""

    def __init__(self, query_router: QueryRouter, workflow_engine: WorkflowEngine):
        self.query_router = query_router
        self.workflow_engine = workflow_engine

    async def process_intent(self, intent: Intent) -> Union[QueryResult, WorkflowResult]:
        """Route intent to appropriate side"""
        if self._is_query(intent):
            return await self.query_router.route_query(intent)
        else:
            return await self.workflow_engine.execute_command(intent)

    def _is_query(self, intent: Intent) -> bool:
        """Determine if intent is a query or command"""
        query_actions = ["list_projects", "get_project", "search", "status"]
        return intent.action in query_actions
```

## Usage Guidelines

- Use query services for read-only operations that need optimization
- Route write operations through workflow engine for complex business logic
- Keep query services simple and focused on data retrieval
- Use intent action to determine query vs command routing
- Optimize query services for performance, commands for consistency

## Benefits

- Optimized read paths for better performance
- Clear separation between read and write concerns
- Simplified query services without complex business logic
- Scalable architecture for different access patterns
- Easy to optimize queries independently

## Trade-offs

- Additional routing complexity
- Potential code duplication between sides
- Need to determine query vs command classification
- May be overkill for simple CRUD applications

## Related Patterns

- [Pattern-001: Repository Pattern](pattern-001-repository.md) - Data access for both query and command sides
- [Pattern-002: Service Pattern](pattern-002-service.md) - Query services implement service pattern
- [Pattern-003: Factory Pattern](pattern-003-factory.md) - Workflow factory for command side

## References

- **Implementation**: `services/queries/`, `services/orchestration/`
- **Usage Example**: QueryRouter for reads, WorkflowEngine for writes
- **Related ADR**: None (core architectural principle)

## Migration Notes

*Consolidated from:*
- `pattern-catalog.md#7-query-service-pattern-cqrs-lite` - Full implementation details and routing logic
- `archive/PATTERN-INDEX-legacy.md#cqrs-lite-pattern` - Status and location information
