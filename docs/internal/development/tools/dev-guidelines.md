# Piper Morgan 1.0 - Development Guidelines

## Overview

This document establishes development standards, practices, and guidelines for contributing to Piper Morgan. Following these guidelines ensures code quality, maintainability, and architectural consistency.

## Development Philosophy

### Domain-First Design

- Business concepts drive technical implementation
- PM terminology and workflows guide architecture
- Database schema follows domain models
- External tools are plugins, not core

### Test-First Development

- Write tests before implementation
- Tests define expected behavior
- Use tests to catch architectural drift
- Maintain high test coverage (>80%)

### Incremental Delivery

- Each PR should provide working functionality
- Avoid large, complex changes
- Use feature flags for partial implementations
- Maintain backward compatibility

## Code Standards

### Pre-commit Hooks

This project uses pre-commit hooks to enforce code quality standards automatically. The hooks run before each commit and will:

- **black**: Format Python code consistently
- **flake8**: Check for code quality and style issues
- **isort**: Sort and organize imports
- **trailing-whitespace**: Remove trailing whitespace
- **end-of-file-fixer**: Ensure files end with newline
- **check-yaml**: Validate YAML files
- **check-added-large-files**: Prevent committing large files

#### Setup (already done)

```bash
# Install pre-commit
pip install pre-commit

# Install the hooks
python -m pre_commit install
```

#### Usage

```bash
# Run hooks on all files
python -m pre_commit run --all-files

# Run hooks on staged files only
python -m pre_commit run

# Skip hooks for a commit (use sparingly)
git commit --no-verify -m "Emergency fix"
```

#### Updating Hooks

```bash
# Update to latest versions
python -m pre_commit autoupdate

# Update specific hook
python -m pre_commit update black
```

### Python Style Guide

Follow PEP 8 with these specific conventions:

```python
# Imports grouped and ordered
import os
import sys
from datetime import datetime
from typing import List, Optional, Dict, Any

from fastapi import FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from services.domain.models import Project, Intent
from services.orchestration.engine import OrchestrationEngine
from shared_types import WorkflowType, IntentCategory

# Class naming
class ProjectRepository:  # PascalCase for classes
    """Repository for project operations"""  # Docstring required

    async def list_active_projects(self) -> List[Project]:  # Type hints required
        """Get all active projects"""
        # Implementation

# Function naming
async def process_intent(intent: Intent) -> WorkflowResult:  # snake_case
    """Process user intent and return result"""
    # Implementation

# Constants
DEFAULT_TIMEOUT = 30  # UPPER_CASE for constants
MAX_RETRIES = 3

# Private methods/variables
def _internal_helper(self) -> None:  # Leading underscore
    self._private_var = "internal"
```

### Type Hints

Always use type hints for:

- Function parameters
- Return values
- Class attributes
- Complex data structures

```python
from typing import List, Optional, Dict, Tuple, Union, Any

async def resolve_project(
    self,
    intent: Intent,
    session_id: str,
    confirmed: bool = False
) -> Tuple[Project, bool]:
    """Resolve project with confirmation flag"""
    # Implementation
```

### Async/Await Patterns

```python
# Correct async patterns
async def get_projects(self) -> List[Project]:
    async with self.factory.get_repository(ProjectRepository) as repo:
        return await repo.list_active_projects()

# Avoid blocking operations
# ❌ Wrong
time.sleep(5)  # Blocks event loop

# ✅ Correct
await asyncio.sleep(5)  # Non-blocking

# Concurrent operations
projects, users = await asyncio.gather(
    repo.get_projects(),
    repo.get_users()
)
```

### Error Handling

```python
# Domain-specific exceptions
class ProjectNotFoundError(Exception):
    """Raised when project doesn't exist"""
    def __init__(self, project_id: str):
        self.project_id = project_id
        super().__init__(f"Project not found: {project_id}")

# Proper error handling
async def get_project(self, project_id: str) -> Project:
    try:
        project = await self.repo.get_by_id(project_id)
        if not project:
            raise ProjectNotFoundError(project_id)
        return project
    except DatabaseError as e:
        logger.error(f"Database error getting project: {e}")
        raise ServiceUnavailableError("Unable to access projects")
```

## Architecture Guidelines

### Layer Separation

```
┌─────────────────────────┐
│   API Layer (FastAPI)   │ ← HTTP concerns only
├─────────────────────────┤
│  Application Services   │ ← Business orchestration
├─────────────────────────┤
│    Domain Models       │ ← Pure business logic
├─────────────────────────┤
│    Repositories        │ ← Data access only
├─────────────────────────┤
│  Database (PostgreSQL) │ ← Persistence
└─────────────────────────┘
```

Rules:

- Dependencies flow downward only
- Domain models have no dependencies
- Repositories return domain models
- Services orchestrate but don't contain business logic

### When to Use Workflows vs Queries

**Use Workflows for:**

- Multi-step processes
- State changes
- External system updates
- Background processing
- Complex orchestration

**Use Queries for:**

- Data retrieval
- Listings and searches
- Read-only operations
- Simple aggregations
- Synchronous responses

### Managing Dependencies

```python
# Good: Explicit dependencies
class ProjectService:
    def __init__(
        self,
        project_repo: ProjectRepository,
        github_client: GitHubClient,
        event_bus: EventBus
    ):
        self.project_repo = project_repo
        self.github_client = github_client
        self.event_bus = event_bus

# Bad: Hidden dependencies
class ProjectService:
    def __init__(self):
        self.project_repo = ProjectRepository()  # Creates own dependencies
        self.github_client = GitHubClient.get_instance()  # Singleton
```

## Testing Patterns

### Test Structure

```python
# tests/test_project_service.py
import pytest
from unittest.mock import Mock, AsyncMock

class TestProjectService:
    """Test project service operations"""

    @pytest.fixture
    def mock_repo(self):
        """Provides mock repository"""
        repo = Mock(spec=ProjectRepository)
        repo.get_by_id = AsyncMock()
        return repo

    @pytest.fixture
    def service(self, mock_repo):
        """Provides service with mocked dependencies"""
        return ProjectService(mock_repo)

    @pytest.mark.asyncio
    async def test_get_project_success(self, service, mock_repo):
        """Should return project when found"""
        # Arrange
        expected = Project(id="123", name="Test")
        mock_repo.get_by_id.return_value = expected

        # Act
        result = await service.get_project("123")

        # Assert
        assert result == expected
        mock_repo.get_by_id.assert_called_once_with("123")
```

### Testing Layers

1. **Unit Tests** - Test individual components with mocks
2. **Integration Tests** - Test component interactions
3. **End-to-End Tests** - Test full workflows with real services

### Test Data Management

```python
# tests/factories.py
from datetime import datetime
from services.domain.models import Project, ProjectIntegration

class ProjectFactory:
    """Creates test projects"""

    @staticmethod
    def create(**kwargs):
        defaults = {
            "id": "test-123",
            "name": "Test Project",
            "description": "Test description",
            "created_at": datetime.now()
        }
        defaults.update(kwargs)
        return Project(**defaults)

    @staticmethod
    def create_with_github(**kwargs):
        project = ProjectFactory.create(**kwargs)
        project.integrations.append(
            ProjectIntegration(
                type=IntegrationType.GITHUB,
                config={"repository": "org/repo"}
            )
        )
        return project
```

### Test Contract Evolution (July 2025)

When architectural patterns evolve, tests must be updated to match new contracts:

#### **Async Test Configuration**
```python
# pytest.ini or pyproject.toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
markers = [
    "asyncio: mark test as requiring async event loop",
]
```

#### **Context Handling Patterns**
```python
# Current pattern: context propagation includes template fields
def test_workflow_context():
    intent = Intent(category=IntentCategory.EXECUTION, action="create_ticket")
    workflow = await factory.create_from_intent(intent)

    # New context fields added for template system
    assert workflow.context["intent_category"] == "execution"
    assert workflow.context["intent_action"] == "create_ticket"
    # Original context still preserved
    assert workflow.context["original_message"] == intent.context["original_message"]
```

#### **Pre-Classifier Test Expectations**
```python
# Simple greetings: should be pre-classified
def test_simple_greeting():
    intent = PreClassifier.pre_classify("hello")
    assert intent is not None
    assert intent.action == "greeting"

# Compound messages: should NOT be pre-classified
def test_compound_greeting():
    intent = PreClassifier.pre_classify("hello there how are you")
    assert intent is None  # Let LLM handle complex patterns
```

#### **Type Safety at Boundaries**
```python
# Repository interfaces expect specific types
def test_file_repository():
    file_id = "uuid-string"  # Not integer
    result = await repo.get_file_by_id(file_id)
    # Test should verify string input, not assume integer conversion
```

#### **JSON-Mode LLM Testing Patterns**
```python
# LLM services using JSON structured output (TextAnalyzer, etc.)
def test_llm_json_mode():
    mock_llm_client = Mock()
    mock_llm_client.complete = AsyncMock(
        return_value='{"title": "Test Doc", "key_findings": ["Finding 1"], "sections": [{"heading": "Section", "points": ["Point 1"]}]}'
    )

    analyzer = TextAnalyzer(llm_client=mock_llm_client)
    result = await analyzer.analyze("file.txt")

    # Verify JSON prompt and response format
    call = mock_llm_client.complete.call_args_list[0]
    assert "JSON format" in call[1]["prompt"]
    assert call[1]["response_format"] == {"type": "json_object"}

    # Verify domain model conversion
    assert result.key_findings == ["Finding 1"]
    assert "Test Doc" in result.summary  # Generated markdown
```

#### **Contract Documentation Requirements**
1. **Document interface changes** alongside implementation
2. **Update test expectations** when architectural patterns evolve
3. **Verify test compatibility** before merging architectural improvements
4. **Maintain backward compatibility** in test fixtures when possible
5. **JSON-mode tests** should mock structured responses and verify conversion to domain models

## Common Patterns

### Repository Pattern

```python
class ProjectRepository(BaseRepository):
    """Follow repository pattern consistently"""

    def __init__(self, session: AsyncSession):
        super().__init__(session, ProjectDB)

    async def find_by_name(self, name: str) -> List[Project]:
        # Repository method returns domain models
        result = await self.session.execute(
            select(ProjectDB).where(ProjectDB.name.ilike(f"%{name}%"))
        )
        db_projects = result.scalars().all()
        return [self._to_domain(p) for p in db_projects]

    def _to_domain(self, db_model: ProjectDB) -> Project:
        # Convert database model to domain model
        return Project(
            id=db_model.id,
            name=db_model.name,
            # ... map all fields
        )
```

### Service Pattern

```python
class ProjectService:
    """Services orchestrate but don't contain business logic"""

    async def create_project_with_github(
        self,
        name: str,
        description: str,
        github_repo: str
    ) -> Project:
        # Orchestrate multiple operations
        project = Project(name=name, description=description)

        # Add GitHub integration
        project.add_integration(
            IntegrationType.GITHUB,
            {"repository": github_repo}
        )

        # Persist
        async with self.repo_factory.get_repository(ProjectRepository) as repo:
            saved = await repo.create(project)

        # Publish event
        await self.event_bus.publish(
            ProjectCreatedEvent(project_id=saved.id)
        )

        return saved
```

## Anti-patterns to Avoid

### ❌ Business Logic in Wrong Layer

```python
# Wrong: Business logic in repository
class ProjectRepository:
    async def create_with_validation(self, project: Project):
        if len(project.name) < 3:  # Business rule in repository!
            raise ValueError("Name too short")
        # ...

# Correct: Business logic in domain
class Project:
    def validate(self):
        if len(self.name) < 3:
            raise ValidationError("Name too short")
```

### ❌ Direct Database Access

```python
# Wrong: Service accessing database directly
class ProjectService:
    async def get_project(self, id: str):
        result = await self.db.execute(  # Direct DB access!
            "SELECT * FROM projects WHERE id = ?"
        )

# Correct: Service uses repository
class ProjectService:
    async def get_project(self, id: str):
        async with self.repo_factory.get_repository(ProjectRepository) as repo:
            return await repo.get_by_id(id)
```

### ❌ God Objects

```python
# Wrong: Class doing too much
class ProjectManager:
    def create_project(self): ...
    def send_notifications(self): ...
    def generate_reports(self): ...
    def sync_with_github(self): ...
    def calculate_metrics(self): ...

# Correct: Separate concerns
class ProjectService: ...
class NotificationService: ...
class ReportGenerator: ...
class GitHubSyncService: ...
class MetricsCalculator: ...
```

## Configuration Management

### Environment Variables

```python
# config.py
import os
from typing import Optional
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Application settings from environment"""

    # Required settings
    database_url: str
    anthropic_api_key: str
    github_token: str

    # Optional with defaults
    log_level: str = "INFO"
    max_retries: int = 3
    timeout_seconds: int = 30

    # Computed settings
    @property
    def redis_url(self) -> str:
        return os.getenv("REDIS_URL", "redis://localhost:6379")

    class Config:
        env_file = ".env"
        case_sensitive = False

# Singleton instance
settings = Settings()
```

### Feature Flags

```python
# feature_flags.py
class FeatureFlags:
    """Manage feature toggles"""

    ENABLE_CLARIFYING_QUESTIONS = os.getenv("FF_CLARIFYING_QUESTIONS", "false").lower() == "true"
    ENABLE_MULTI_REPO = os.getenv("FF_MULTI_REPO", "false").lower() == "true"
    ENABLE_LEARNING = os.getenv("FF_LEARNING", "false").lower() == "true"

# Usage
if FeatureFlags.ENABLE_CLARIFYING_QUESTIONS:
    response = await self.ask_clarification(intent)
else:
    response = await self.process_directly(intent)
```

## Documentation Standards

### Code Documentation

```python
class ProjectContext:
    """
    Resolves project context from various sources.

    This class implements a sophisticated resolution hierarchy:
    1. Explicit project_id in the intent
    2. Last used project in the session
    3. Inferred from message content
    4. Default project fallback

    Example:
        context = ProjectContext(repo, llm)
        project, needs_confirm = await context.resolve_project(
            intent, session_id="abc123"
        )
    """

    async def resolve_project(
        self,
        intent: Intent,
        session_id: str,
        confirmed: bool = False
    ) -> Tuple[Project, bool]:
        """
        Resolve project from intent and context.

        Args:
            intent: The classified intent with context
            session_id: Current session identifier
            confirmed: Whether user confirmed project selection

        Returns:
            Tuple of (resolved_project, needs_confirmation)

        Raises:
            ProjectNotFoundError: If explicit project_id doesn't exist
            AmbiguousProjectError: If project cannot be determined
        """
```

### API Documentation

- Use docstrings for all public methods
- Include parameter descriptions
- Document return types and exceptions
- Provide usage examples for complex APIs

## Git Workflow

### Branch Naming

- `feature/pm-XXX-description` - New features
- `fix/pm-XXX-description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring

### Commit Messages

```
PM-009: Add query service for project listing

- Implement ProjectQueryService with list_active_projects
- Add integration tests for query flow
- Update API to route QUERY intents appropriately

Fixes #21
```

### Pull Request Guidelines

1. Link to GitHub issue
2. Describe what changed and why
3. Include test results
4. Update documentation if needed
5. Request review from team

## Performance Guidelines

### Database Queries

```python
# Avoid N+1 queries
# Wrong
projects = await repo.get_all_projects()
for project in projects:
    project.integrations = await repo.get_integrations(project.id)

# Correct - Eager loading
result = await session.execute(
    select(ProjectDB).options(selectinload(ProjectDB.integrations))
)
```

### Caching Strategy

```python
# Cache frequently accessed data
@cached(ttl=300)  # 5 minutes
async def get_default_project(self) -> Optional[Project]:
    return await self.repo.get_default_project()
```

### Async Best Practices

```python
# Process concurrently when possible
results = await asyncio.gather(
    self.process_intent(intent1),
    self.process_intent(intent2),
    self.process_intent(intent3)
)
```

## Security Guidelines

### API Key Management

- Never commit API keys
- Use environment variables
- Rotate keys regularly
- Use separate keys for dev/prod

### Input Validation

```python
# Always validate user input
from pydantic import BaseModel, validator

class IntentRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

    @validator('message')
    def message_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Message cannot be empty")
        return v
```

### SQL Injection Prevention

```python
# Never build SQL strings
# Wrong
query = f"SELECT * FROM projects WHERE name = '{name}'"

# Correct - Use parameterized queries
result = await session.execute(
    select(ProjectDB).where(ProjectDB.name == name)
)
```

## Monitoring and Logging

### Structured Logging

```python
import structlog

logger = structlog.get_logger()

# Include context in logs
logger.info(
    "processing_intent",
    intent_id=intent.id,
    category=intent.category.value,
    confidence=intent.confidence
)
```

### Metrics Collection

```python
# Track key metrics
from prometheus_client import Counter, Histogram

intent_counter = Counter(
    'intents_processed_total',
    'Total intents processed',
    ['category', 'status']
)

response_time = Histogram(
    'intent_processing_duration_seconds',
    'Time to process intent'
)

# Usage
with response_time.time():
    result = await process_intent(intent)
    intent_counter.labels(
        category=intent.category.value,
        status='success'
    ).inc()
```

## Troubleshooting Guide

### Common Issues

1. **Import Errors**

   - Check `__init__.py` files exist
   - Verify PYTHONPATH includes project root
   - Ensure consistent module naming

2. **Async Context Errors**

   - Remember to await async functions
   - Use `pytest.mark.asyncio` for async tests
   - Check event loop configuration

3. **Database Connection Issues**

   - Verify DATABASE_URL is set
   - Check Docker containers are running
   - Ensure migrations are applied

4. **Type Checking Errors**
   - Run `mypy services/` to check types
   - Add type ignores sparingly with explanations
   - Update type stubs if needed

## Resources

- [Python Style Guide (PEP 8)](https://pep8.org/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Async Guide](https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html)
- [Structlog Documentation](https://www.structlog.org/)
- [Pytest Async](https://pytest-asyncio.readthedocs.io/)

---

_Last Updated: June 27, 2025_

## Revision Log

- **June 27, 2025**: Post-PM-011 consolidation: Updated deployment/user guides for web interface, fixed PostgreSQL port, added monitoring/security/config documentation
- **June 27, 2025**: Added systematic documentation dating and revision tracking
