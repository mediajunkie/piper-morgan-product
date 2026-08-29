# Pattern-005: Transaction Management Pattern

## Status

**Proven**

## Context

Manual transaction handling creates inconsistent data states and error-prone code. When operations involve multiple database changes, ensuring atomicity and proper rollback on failure becomes critical. The Transaction Management Pattern addresses:

- What challenges does this solve? Provides consistent transaction handling with automatic commit/rollback across operations
- When should this pattern be considered? When operations involve multiple database changes that must be atomic
- What are the typical scenarios where this applies? Repository operations, complex business transactions, data consistency requirements

## Pattern Description

The Transaction Management Pattern ensures consistent transaction handling with automatic commit/rollback, eliminating manual transaction management and reducing data consistency errors.

Core concept:
- Automatic transaction context management
- Session scope handles transaction lifecycle
- Explicit transaction boundaries for complex operations
- Rollback on exceptions, commit on success

## Implementation

### Session Scope Pattern

```python
from contextlib import asynccontextmanager
from services.database.session_factory import AsyncSessionFactory

@asynccontextmanager
async def transaction_scope():
    """Context manager for automatic transaction handling"""
    async with AsyncSessionFactory.session_scope() as session:
        try:
            async with session.begin():
                yield session
                # Automatic commit on successful exit
        except Exception:
            # Automatic rollback on exception
            raise
```

### Repository Transaction Integration

```python
class BaseRepository:
    """Repository with integrated transaction handling"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, **kwargs) -> Any:
        """Create with automatic transaction handling"""
        async with self.session.begin():
            instance = self.model(**kwargs)
            self.session.add(instance)
            # Automatic commit via context manager
        return instance

    async def update(self, id: str, **kwargs) -> Optional[Any]:
        """Update with transaction safety"""
        async with self.session.begin():
            result = await self.session.execute(
                select(self.model).where(self.model.id == id)
            )
            instance = result.scalar_one_or_none()
            if instance:
                for key, value in kwargs.items():
                    setattr(instance, key, value)
                # Automatic commit via context manager
            return instance
```

### Service-Level Transaction Management

```python
class ProjectService:
    """Service with transaction management for complex operations"""

    def __init__(self, project_repo: ProjectRepository, workflow_repo: WorkflowRepository):
        self.project_repo = project_repo
        self.workflow_repo = workflow_repo

    async def create_project_with_workflows(self, project_data: dict, workflows: List[dict]) -> Project:
        """Complex operation requiring transaction coordination"""
        async with AsyncSessionFactory.session_scope() as session:
            async with session.begin():
                # Create project
                project = await self.project_repo.create(**project_data)

                # Create associated workflows
                for workflow_data in workflows:
                    workflow_data['project_id'] = project.id
                    await self.workflow_repo.create(**workflow_data)

                # All operations commit together or rollback together
                return project
```

### Error Handling with Transactions

```python
async def safe_operation_with_transaction():
    """Example of proper transaction error handling"""
    try:
        async with AsyncSessionFactory.session_scope() as session:
            async with session.begin():
                # Perform operations
                project = await project_repo.create(name="Test Project")
                await workflow_repo.create(project_id=project.id, name="Test Workflow")

                # Operations committed automatically on success
                return project

    except IntegrityError as e:
        logger.error(f"Database integrity violation: {e}")
        raise ProjectCreationError("Project creation failed due to data constraints")
    except Exception as e:
        logger.error(f"Unexpected error in transaction: {e}")
        raise ProjectCreationError("Project creation failed")
```

## Usage Guidelines

- Use `AsyncSessionFactory.session_scope()` for session management
- Wrap multi-operation transactions in `session.begin()` context
- Let context managers handle commit/rollback automatically
- Never call `session.commit()` or `session.rollback()` manually
- Keep transaction scope as small as possible for performance

## Benefits

- Automatic transaction lifecycle management
- Consistent rollback behavior on errors
- Eliminates manual transaction handling mistakes
- Clean separation of business logic from transaction concerns
- Improved data consistency and reliability

## Trade-offs

- Context manager overhead for simple operations
- Learning curve for developers used to manual transactions
- Debugging can be more complex with automatic handling
- May mask transaction boundary issues in complex workflows

## Anti-patterns to Avoid

- ❌ Manual `session.commit()` calls
- ❌ Sharing sessions across operation boundaries
- ❌ Missing session cleanup in exception handlers
- ❌ Long-running transactions holding locks

## Related Patterns

- [Pattern-001: Repository Pattern](pattern-001-repository.md) - Repositories implement transaction pattern
- [Pattern-002: Service Pattern](pattern-002-service.md) - Services coordinate multi-repository transactions
- [Pattern-007: Async Error Handling](pattern-007-async-error-handling.md) - Error propagation in transactions

## References

- **Implementation**: `services/database/repositories.py`
- **Usage Example**: Repository create/update operations
- **Related ADR**: ADR-005 (repository pattern consistency)

## Migration Notes

*Consolidated from:*
- `archive/PATTERN-INDEX-legacy.md#transaction-management-pattern` - Status and location information
- Repository pattern implementation - Transaction context usage examples
