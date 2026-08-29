# Pattern-001: Repository Pattern

## Status

**Proven**

## Context

Data access logic scattered throughout the codebase creates maintenance challenges and tight coupling between domain models and database implementation. The Repository Pattern addresses:

- What challenges does this solve? Encapsulates data access logic and provides clean separation between domain and data layers
- When should this pattern be considered? When you need consistent database operations across multiple entities
- What are the typical scenarios where this applies? CRUD operations, domain model persistence, transaction management

## Pattern Description

The Repository Pattern encapsulates data access logic and provides a clean interface between domain models and database implementation, with automatic resource management and consistent transaction handling.

Core concept:
- BaseRepository provides common CRUD operations
- Domain-specific repositories extend base functionality
- Automatic transaction handling via context managers
- Clean separation between domain and database concerns

## Implementation

### Structure

```python
class BaseRepository:
    """Base repository with common CRUD operations"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, **kwargs) -> Any:
        # Use transaction context for automatic commit/rollback
        async with self.session.begin():
            instance = self.model(**kwargs)
            self.session.add(instance)
            # Automatic commit via context manager
        return instance

    async def get_by_id(self, id: str) -> Optional[Any]:
        result = await self.session.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()
```

### Domain-Specific Implementation

```python
class ProjectRepository(BaseRepository):
    """Domain-specific repository"""

    model = ProjectDB

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def list_active_projects(self) -> List[Project]:
        result = await self.session.execute(
            select(ProjectDB).where(ProjectDB.is_archived == False)
        )
        db_projects = result.scalars().all()
        return [db_project.to_domain() for db_project in db_projects]
```

### Usage with Session Management

```python
from contextlib import asynccontextmanager
from services.database.session_factory import AsyncSessionFactory

async def service_example():
    """Example service using context manager for automatic resource management"""
    async with AsyncSessionFactory.session_scope() as session:
        repo = ProjectRepository(session)
        return await repo.list_active_projects()
```

## Usage Guidelines

- Extend BaseRepository for domain-specific operations
- Use async context managers for automatic transaction handling
- Keep repository focused on data access, not business logic
- Define clear interfaces between domain and data layers

## Benefits

- Clean separation of concerns
- Consistent data access patterns
- Automatic resource management
- Easy testing with repository mocking
- Transaction handling abstraction

## Trade-offs

- Additional abstraction layer
- Potential over-engineering for simple CRUD
- Learning curve for transaction management patterns

## Related Patterns

- [Pattern-002: Service Pattern](pattern-002-service.md) - Business logic layer using repositories
- [Pattern-005: Transaction Management](pattern-005-transaction-management.md) - Session and transaction handling

## References

- **Implementation**: `services/repositories/`, `services/database/repositories.py`
- **Related ADR**: ADR-005 (repository pattern consistency)
- **Usage Examples**: BaseRepository, ProjectRepository, WorkflowRepository

## Migration Notes

*Consolidated from:*
- `pattern-catalog.md#1-repository-pattern` - Implementation details and code examples
- `archive/PATTERN-INDEX-legacy.md#repository-pattern` - Status and location information
