# Pattern-013: Database Session Management Pattern

## Status

**Proven**

## Context

> **⚠️ Disambiguation Note**: This pattern covers database and user application sessions for data consistency and state management. For development workflow session logging, see [Pattern-021: Development Session Management Pattern](pattern-021-development-session-management.md).

Applications need to manage database sessions for data consistency and user sessions for state continuity. Without systematic session management, applications suffer from resource leaks, data inconsistency, and lost user context. The Database Session Management Pattern addresses:

- What challenges does this solve? Provides consistent lifecycle management for database and user application sessions
- When should this pattern be considered? When applications need reliable session state management and resource cleanup
- What are the typical scenarios where this applies? Database operations, user interactions, web applications, multi-step transactions

## Pattern Description

The Database Session Management Pattern manages session lifecycle consistently for database and user application sessions with proper cleanup, transaction handling, and state management.

Core concept:
- Context managers for automatic resource management
- Clear session ownership and boundaries
- Proper cleanup in all execution paths
- Transaction handling at appropriate levels

## Implementation

### Database Session Management

```python
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from typing import Type, TypeVar

T = TypeVar('T', bound='BaseRepository')

class AsyncSessionFactory:
    """Factory for managing database sessions"""

    def __init__(self, database_url: str):
        self.engine = create_async_engine(
            database_url,
            echo=False,
            pool_pre_ping=True,
            pool_recycle=3600
        )
        self.async_session = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    @asynccontextmanager
    async def session_scope(self):
        """Provide a transactional scope around a series of operations"""
        session = self.async_session()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    @asynccontextmanager
    async def get_repository(self, repo_class: Type[T]) -> T:
        """Provide repository with managed session"""
        async with self.session_scope() as session:
            yield repo_class(session)

    async def close(self):
        """Clean shutdown of engine"""
        await self.engine.dispose()

# Global factory instance
session_factory = AsyncSessionFactory(DATABASE_URL)
```

### Repository Integration

```python
class BaseRepository:
    """Base repository with session management"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, **kwargs) -> Any:
        """Create with automatic transaction handling"""
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.flush()  # Get ID without committing
        return instance

    async def get_by_id(self, id: str) -> Optional[Any]:
        """Get by ID with session management"""
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

# Usage example
async def service_operation():
    async with session_factory.session_scope() as session:
        project_repo = ProjectRepository(session)
        workflow_repo = WorkflowRepository(session)

        # Multiple operations in same transaction
        project = await project_repo.create(name="New Project")
        workflow = await workflow_repo.create(
            project_id=project.id,
            name="Initial Workflow"
        )

        # Both committed together when context exits
        return project, workflow
```

### User Session Management

```python
from datetime import datetime, timedelta
import uuid
from typing import Dict, Any, Optional

class UserSessionManager:
    """Manages user session state and lifecycle"""

    def __init__(self, default_timeout: int = 3600):
        self._sessions: Dict[str, Dict[str, Any]] = {}
        self.default_timeout = default_timeout

    def create_session(self, user_id: str, **initial_data) -> str:
        """Create new user session"""
        session_id = str(uuid.uuid4())
        session_data = {
            "user_id": user_id,
            "created_at": datetime.utcnow(),
            "last_accessed": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(seconds=self.default_timeout),
            "data": initial_data
        }
        self._sessions[session_id] = session_data
        return session_id

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data if valid"""
        if session_id not in self._sessions:
            return None

        session = self._sessions[session_id]

        # Check expiration
        if datetime.utcnow() > session["expires_at"]:
            self.destroy_session(session_id)
            return None

        # Update last accessed
        session["last_accessed"] = datetime.utcnow()
        return session

    def update_session(self, session_id: str, **updates):
        """Update session data"""
        if session_id in self._sessions:
            self._sessions[session_id]["data"].update(updates)
            self._sessions[session_id]["last_accessed"] = datetime.utcnow()

    def destroy_session(self, session_id: str):
        """Destroy session"""
        self._sessions.pop(session_id, None)

    def cleanup_expired_sessions(self):
        """Remove expired sessions"""
        now = datetime.utcnow()
        expired = [
            sid for sid, session in self._sessions.items()
            if now > session["expires_at"]
        ]
        for session_id in expired:
            self.destroy_session(session_id)
```


## Usage Guidelines

### Database Session Management
- Use `session_scope()` for transaction boundaries
- Keep session scope as small as possible
- Let context managers handle commit/rollback
- Never share sessions across async boundaries

### User Session Management
- Set appropriate session timeouts
- Clean up expired sessions regularly
- Store only necessary data in sessions
- Use secure session IDs


## Benefits

- Automatic resource cleanup prevents leaks
- Consistent transaction handling across application
- Clear session boundaries and ownership
- User state persistence and management
- Error recovery through proper rollback

## Trade-offs

- Context manager overhead for simple operations
- Memory usage for session storage
- Additional complexity for session lifecycle
- Need for cleanup processes for expired sessions

## Anti-patterns to Avoid

- ❌ Manual session creation without cleanup
- ❌ Sharing database sessions across operation boundaries
- ❌ Long-lived sessions without timeout
- ❌ Session state without clear ownership

## Related Patterns

- [Pattern-005: Transaction Management](pattern-005-transaction-management.md) - Transaction handling within sessions
- [Pattern-001: Repository Pattern](pattern-001-repository.md) - Repositories use managed sessions
- [Pattern-011: Context Resolution Pattern](pattern-011-context-resolution.md) - Context resolution using session state

## References

- **Database Sessions**: Repository factory and session management
- **User Sessions**: Web application session handling
- **Related ADR**: Database session management, user session handling

## Migration Notes

*Split from original Pattern-013 Session Management Pattern to focus specifically on database and user application sessions. Development workflow session logging moved to Pattern-021: Development Session Management Pattern.*

*Original consolidation from:*
- `pattern-catalog.md#13-session-management-pattern` - Database session management with repositories
- Codebase analysis - User session management patterns
