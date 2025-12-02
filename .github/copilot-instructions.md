# Copilot Instructions for Piper Morgan

AI Product Management Assistant - Python/FastAPI backend with plugin architecture

## Core Architecture

**Entry Point**: `main.py` → NOT `web/app.py` directly
- Run: `python main.py` (starts server on http://localhost:8001)
- FastAPI app defined in `web/app.py` (~1000 lines)
- Service initialization via `ServiceContainer` (DDD pattern)

**Service Container Pattern**:
```python
from services.container import ServiceContainer
container = ServiceContainer()
await container.initialize()
llm_service = container.get_service('llm')
```

**Hub-and-Spoke Model**: `IntentService` orchestrates 39 domain models from `services/domain/models.py` (source of truth)

## Critical File Locations

- **All Enums**: `services/shared_types.py` (IntentCategory, WorkflowType, TaskType, TodoStatus, etc.)
- **Domain Models**: `services/domain/models.py` (1300+ lines - truth source)
- **Intent Routing**: `services/intent/intent_service.py` (5200+ lines - 13 intent categories)
- **User Config**: `config/PIPER.user.md` (NOT YAML - Markdown-based configuration)
- **Personality**: `config/PIPER.md` (system identity and tone)

## Infrastructure (docker-compose.yml)

**Non-standard ports to avoid conflicts**:
- PostgreSQL: **port 5433** (NOT 5432!)
- Redis: port 6379
- ChromaDB: port 8000
- Temporal: port 7233
- Web: port 8001

Docker project name: `piper-morgan-stable` (survives directory renames)

## Development Commands

```bash
# Start application
python main.py                    # Normal startup
python main.py --verbose          # Detailed logging
python main.py --no-browser       # No auto-launch

# CLI commands
python main.py setup              # Interactive setup
python main.py status             # System health check
python main.py keys add openai    # Add API key

# Tests with pytest markers
pytest tests/unit/ -v             # Unit tests
pytest tests/ -m smoke            # Critical path (<5 sec)
pytest tests/ -m integration      # Integration tests
pytest tests/ -m llm              # Requires LLM keys
pytest tests/ -m contract         # Plugin compliance

# Database migrations
docker-compose up -d              # Start services
alembic upgrade head              # Run migrations
alembic revision --autogenerate -m "desc"

# Pre-commit CRITICAL
./scripts/fix-newlines.sh         # ALWAYS before commit
```

## Project-Specific Patterns

### Intent Handler Convention
Intent handlers follow naming: `_handle_{intent_type}` in `IntentService`:
- Query intents → `_handle_query_intent()`
- Execution → `_handle_execution_intent()`
- Analysis → `_handle_analysis_intent()`
- Synthesis → `_handle_synthesis_intent()`

Action names from classifier may differ from handler names - see `ActionMapper` (Issue #284)

### Plugin Architecture
All plugins extend `PiperPlugin` from `services/plugins/plugin_interface.py`:
- Metadata: name, version, capabilities
- Capabilities: "routes", "webhooks", "spatial", "mcp", "background"
- Contract tests verify plugin compliance (`@pytest.mark.contract`)
- Integrations in `services/integrations/`: slack, github, notion, calendar, mcp

### Two-Tier Response Pattern
- **Canonical Handlers**: Fast (<1ms) for direct queries - no orchestration
- **Workflow Handlers**: Complex (2-3s) synthesis/analysis via `OrchestrationEngine`

### Graceful Degradation (Pattern-007)
Web layer returns structured responses even on service failure:
```python
def _create_degradation_response(message: str, degradation_msg: str) -> dict:
    # Returns 200 OK with user-friendly message
    # Never expose technical details to users
```

## Testing Philosophy

**Marker hierarchy** (pytest.ini):
- `@pytest.mark.smoke` - Critical path, <5 sec total
- `@pytest.mark.unit` - Unit tests, <30 sec
- `@pytest.mark.integration` - Up to 2 minutes
- `@pytest.mark.llm` - Requires API keys (skipped in CI)
- `@pytest.mark.contract` - Plugin interface compliance

**Async configuration**: Session-scoped event loops prevent "Task attached to different loop" errors (Issue #290)

## Common Gotchas

1. **PostgreSQL Port**: Use 5433, not default 5432
2. **Entry Point**: Run `main.py`, not directly uvicorn
3. **Config Format**: User config is Markdown (`PIPER.user.md`), not YAML
4. **Enum Location**: ALL enums go in `services/shared_types.py`
5. **Pre-commit**: Run `./scripts/fix-newlines.sh` before committing to fix EOF newlines
6. **Repository URL**: `https://github.com/mediajunkie/piper-morgan-product` (NOT `Codewarrior1988/piper-morgan`)

## Service Structure

```
services/
├── container/          # ServiceContainer (DDD lifecycle)
├── domain/             # Domain models (models.py is truth)
├── shared_types.py     # ALL enums
├── intent/             # Intent classification & routing
├── intent_service/     # Canonical handlers, todo handlers
├── integrations/       # External plugins (7+ integrations)
├── llm/                # LLM providers & adapters
├── orchestration/      # Temporal workflow engine
├── plugins/            # Plugin interface & registry
├── knowledge/          # Knowledge graph & RAG
└── user_context/       # Multi-user config isolation
```

## Key Design Decisions

- **DDD with ServiceContainer**: Explicit lifecycle management over framework magic
- **Intent-driven routing**: 13 categories (EXECUTION, ANALYSIS, SYNTHESIS, QUERY, etc.)
- **Plugin system**: Standardized interfaces with version tracking
- **Multi-user context**: Service isolates user configuration per session
- **Personality injection**: Markdown config parsed and applied to LLM responses
- **Temporal orchestration**: Complex workflows use Temporal activities (not direct calls)

## Documentation

- Technical: `docs/TECHNICAL-DEVELOPERS.md` (575 lines)
- Architecture: `docs/NAVIGATION.md`
- Testing: `docs/testing/` and `COMPREHENSIVE-TESTING-GUIDE.md`
- Claude conventions: `CLAUDE.md` (792 lines - debugging protocols, anti-completion-bias)
- Public docs: https://pmorgan.tech

## When Adding Features

1. Check `services/shared_types.py` for existing enums
2. Extend domain models in `services/domain/models.py`
3. Add intent handler to `IntentService` if user-facing
4. Create plugin in `services/integrations/` if external integration
5. Add smoke test for critical path (`@pytest.mark.smoke`)
6. Update user docs at https://pmorgan.tech if user-facing

## Anti-Patterns to Avoid

- Don't create new enum files - use `shared_types.py`
- Don't bypass ServiceContainer - use `container.get_service()`
- Don't skip pre-commit newline fixes - causes CI failures
- Don't use port 5432 - PostgreSQL is on 5433
- Don't declare completion without passing tests (see CLAUDE.md anti-completion-bias protocol)
