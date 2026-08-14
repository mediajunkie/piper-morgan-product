# Technical Reference Guide - For Developers

**Audience**: Developers, architects, and technical contributors
**Last Updated**: November 17, 2025
**Status**: Active technical documentation

---

## Quick Navigation

- **For Local Setup**: See [Getting Started Guide](#getting-started-with-piper-morgan)
- **For Architecture**: See [System Architecture](#system-architecture)
- **For Integration**: See [Integration Patterns](#integration-patterns)
- **For Debugging**: See [Common Issues & Solutions](#common-issues--solutions)

---

## Getting Started with Piper Morgan

### System Requirements

- **Python**: 3.11 or higher
- **Docker**: Latest version (for PostgreSQL, Redis, other services)
- **Port Requirements**: 8001 (web), 5433 (PostgreSQL), 6379 (Redis)
- **Disk Space**: ~2GB for dependencies and database

### Initial Setup

```bash
# Clone repository
git clone https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start services (Docker)
docker compose up -d

# Initialize database
python scripts/init-db.py

# Start application
python main.py
```

**Access Points**:
- Web UI: http://localhost:8001
- API Docs: http://localhost:8001/docs
- Standup Interface: http://localhost:8001/standup

---

## System Architecture

### Core Components

#### 1. **Entry Point** (`main.py`)
- Application bootstrap
- Service initialization
- Dependency injection setup
- NOT uvicorn directly

#### 2. **Web Server** (`web/app.py`)
- FastAPI application (~678 lines)
- Route definitions
- Middleware stack
- Template rendering

#### 3. **Services** (`services/`)
- **Domain Models**: `domain/models.py` (source of truth)
- **Intent Classification**: `intent/intent_service.py`
- **User Context**: `user_context/user_context_service.py`
- **Plugin System**: `integrations/` (7+ plugins)
- **Handlers**: Canonical and workflow handlers

#### 4. **Data Layer** (`services/`)
- PostgreSQL (port 5433)
- Redis caching (port 6379)
- ORM/Query layer

#### 5. **Templates** (`templates/`)
- Jinja2 templates for web pages
- Component modules (skip-link, modals, toasts, etc.)
- Base layout and page templates

#### 6. **Frontend Assets** (`web/static/`)
- CSS stylesheets
- JavaScript modules
- Images and icons

### Critical File Locations

```
main.py                           # Application entry point
web/app.py                        # FastAPI application
services/domain/models.py         # Domain models (source of truth)
services/shared_types.py          # Shared types and enums
services/config.py                # Configuration settings
services/intent/intent_service.py # Intent classification
services/user_context/            # User context service
services/integrations/            # Plugin integrations
templates/                        # Jinja2 templates
web/static/                       # Static assets
config/PIPER.user.md             # User configuration
```

### Key Architectural Patterns

1. **Hub-and-Spoke Model**: 39 domain models orchestrated from Intent Service
2. **Plugin Architecture**: Standardized integration points with versioning
3. **Intent Classification**: 13 intent categories routed to handlers
4. **Canonical Handlers**: Fast (~1ms) responses for common queries
5. **Workflow Handlers**: Complex (2-3s) operations for synthesis/analysis
6. **User Context Service**: Multi-user configuration and context isolation

---

## Development Workflow

### Setting Up Your Development Environment

```bash
# Check system health
python main.py status

# Run tests
python -m pytest tests/unit/ -v
python -m pytest tests/integration/ -v

# Start with debugging
python main.py --debug
```

### Common Development Tasks

#### Adding a New Intent Handler

1. Read existing handler: `services/intent/handlers/`
2. Understand the pattern from similar handlers
3. Create `_handle_your_intent` method in `IntentService`
4. Add intent classification in classifier
5. Test with manual script in `tests/manual/`
6. Update documentation

#### Creating a New Plugin

1. Read demo plugin: `services/integrations/demo/`
2. Implement required methods: `get_config()`, `validate()`, `execute()`
3. Create plugin directory: `services/integrations/your_plugin/`
4. Add versioning and metadata
5. Register in plugin registry
6. Test with integration tests
7. Document in [Plugin Development Guide](guides/plugin-development-guide.md)

#### Working with Database

```bash
# Connect to PostgreSQL (port 5433)
docker exec -it piper-postgres psql -U piper -d piper_morgan

# View migrations
python scripts/show-migrations.py

# Run migrations
python scripts/run-migrations.py

# Reset database (development only!)
python scripts/reset-db.py
```

#### Frontend Development

1. Edit templates in `templates/`
2. Edit CSS in `web/static/css/`
3. Edit JavaScript in `web/static/js/`
4. Changes reload automatically with debugger enabled
5. Check browser console for errors

---

## Integration Patterns

### Available Integrations

| Integration | Type | Status | Purpose |
|-------------|------|--------|---------|
| GitHub | API | Active | Issue tracking, PR analysis |
| Slack | Webhook | Active | Notifications, messaging |
| Calendar | API | Active | Schedule, availability |
| Notion | API | Active | Document management |
| Demo | Example | Reference | Template for new plugins |
| MCP | Protocol | Active | Model context protocol |
| Spatial | Custom | Active | Specialized features |

### Plugin Interface

All plugins implement `BaseIntegration`:

```python
class YourPlugin(BaseIntegration):
    """Plugin description"""

    @property
    def name(self) -> str:
        return "your_plugin"

    @property
    def version(self) -> str:
        return "1.0.0"

    async def get_config(self) -> Dict:
        """Return configuration schema"""
        pass

    async def validate(self) -> ValidationResult:
        """Validate integration setup"""
        pass

    async def execute(self, command: str, **kwargs) -> ExecutionResult:
        """Execute integration command"""
        pass
```

### Intent Routing

Intent → Classification → Handler Selection → Plugin Execution

1. User sends natural language intent
2. Classifier determines intent type (Identity, Temporal, Status, Priority, etc.)
3. Canonical handlers: Direct, fast response (~1ms)
4. Workflow handlers: Complex orchestration, plugin execution (2-3s)
5. Response returned to user

---

## Data Models

### Core Domain Models

- **User**: User identity and configuration
- **Issue**: GitHub issue representation
- **Task**: Internal task management
- **Document**: File and document references
- **Event**: Calendar and activity tracking
- **Conversation**: Multi-turn context
- **Plugin**: Integration metadata
- **Configuration**: User/team settings

### Model File Location

**Source of Truth**: `services/domain/models.py`

All models are defined here. Don't scatter definitions across services.

### Shared Types

**Location**: `services/shared_types.py`

```python
# All enums defined here
class IntentCategory(Enum):
    IDENTITY = "identity"
    TEMPORAL = "temporal"
    STATUS = "status"
    # ... etc
```

---

## Configuration Management

### User Configuration

**File**: `config/PIPER.user.md` (not YAML)

```markdown
# PIPER User Configuration

## GitHub
- repository: mediajunkie/piper-morgan-product
- token: ${GITHUB_TOKEN}

## Slack
- workspace_token: ${SLACK_TOKEN}
- user_id: U12345

## Calendar
- provider: google
- credentials: ${CALENDAR_CREDS}
```

### Environment Variables

```bash
# Required
OPENAI_API_KEY=sk-...
GITHUB_TOKEN=ghp_...

# Optional
ANTHROPIC_API_KEY=sk-ant-...
SLACK_BOT_TOKEN=xoxb-...
CALENDAR_CREDENTIALS=...

# Internal
DATABASE_URL=postgresql://piper:password@localhost:5433/piper_morgan
REDIS_URL=redis://localhost:6379
```

### Settings File

**Location**: `services/config.py`

```python
class Settings:
    """Application settings from environment"""
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    # ... other settings
```

---

## Testing Strategy

### Test Organization

```
tests/
├── unit/              # Fast, isolated tests
├── integration/       # Service integration tests
└── manual/           # Interactive debugging scripts
```

### Running Tests

```bash
# All unit tests
python -m pytest tests/unit/ -v

# Specific test file
python -m pytest tests/unit/test_intent_service.py -v

# With coverage
python -m pytest tests/unit/ --cov=services

# Integration tests (slower, require services)
python -m pytest tests/integration/ -v

# Manual debugging
python tests/manual/manual_notion_test.py
```

### Test Naming Convention

- **Automated**: `test_*.py` or `*_test.py` in `tests/unit/` or `tests/integration/`
- **Manual**: `manual_*.py` in `tests/manual/` (can use hardcoded IDs, `load_dotenv()`)

---

## Common Issues & Solutions

### Issue: Database Connection Refused

```
Error: could not connect to server: Connection refused
```

**Solution**:
```bash
# Check if Docker containers are running
docker ps | grep postgres

# Start services
docker compose up -d

# Verify port 5433 (not 5432)
netstat -an | grep 5433
```

### Issue: Static Files Return 404

```
GET /static/css/style.css → HTTP 404
```

**Solution**:
1. Check if files exist in `web/static/`
2. Verify mount in `web/app.py`: `app.mount("/static", StaticFiles(...))`
3. Ensure mounts are AFTER all route handlers
4. Clear browser cache (Cmd+Shift+R)

### Issue: Template Not Found

```
TemplateNotFound: skip-link.html
```

**Solution**:
1. Verify template exists: `ls templates/skip-link.html`
2. Check Jinja2 path points to `templates/` (parent of `web/`)
3. Verify absolute path in `web/app.py`:
   ```python
   templates = Jinja2Templates(
       directory=os.path.join(os.path.dirname(__file__), "..", "templates")
   )
   ```

### Issue: Intent Classification Returns Wrong Category

**Solution**:
1. Check test cases in `tests/unit/test_intent_classifier.py`
2. Review training data for that category
3. Add more examples to improve accuracy
4. Check recent code changes for regressions

### Issue: Plugin Not Loading

```
PluginNotFoundError: your_plugin
```

**Solution**:
1. Verify plugin class inherits `BaseIntegration`
2. Check plugin registered in registry
3. Verify required methods implemented
4. Check for import errors: `python -c "from services.integrations.your_plugin import YourPlugin"`

---

## Debugging Techniques

### Using Print Debugging

```python
from services.logger import logger

# In your code
logger.debug(f"Value: {variable}")
logger.info(f"Operation: {description}")
logger.error(f"Error: {error_message}")
```

### Using Interactive Debugger

```python
import pdb
pdb.set_trace()  # Execution pauses here
```

### Checking System State

```bash
# Database state
docker exec -it piper-postgres psql -U piper -d piper_morgan -c "SELECT * FROM users LIMIT 5;"

# Redis cache
docker exec -it piper-redis redis-cli

# API responses
curl -H "Content-Type: application/json" \
  -d '{"message":"what is my status?"}' \
  http://localhost:8001/api/v1/intent
```

### Performance Profiling

```bash
# Benchmark intent processing
python scripts/benchmark-intent.py

# Profile database queries
python -m pytest tests/unit/test_intent_service.py -v --durations=10
```

---

## Performance Guidelines

### Response Time Targets

- **Canonical Handlers**: <1ms (cached, deterministic)
- **Web Requests**: <150ms (from request to response)
- **Workflow Handlers**: 2-3 seconds (complex processing)
- **Full Standup**: 4.6-5.1 seconds (multiple integrations)

### Caching Strategy

- **Cache Hit Rate Target**: 84%+ (currently achieved)
- **Speedup Ratio**: 7-8x with cache vs without
- **Cache Keys**: User-scoped to prevent leaks

### Database Optimization

- Use indexes for frequently queried fields
- Batch operations when possible
- Use connection pooling (configured in `services/config.py`)
- Monitor slow queries in PostgreSQL

---

## Security Considerations

### API Key Management

- Never commit `.env` or `PIPER.user.md`
- Use environment variables for secrets
- Rotate tokens regularly
- Log successful authentications only

### User Data Protection

- All queries scoped to authenticated user
- User context service enforces isolation
- Audit logging for sensitive operations

### Input Validation

```python
from pydantic import BaseModel, validator

class IntentRequest(BaseModel):
    message: str

    @validator('message')
    def message_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Message cannot be empty')
        return v
```

---

## Deployment

### Production Build

```bash
# Install production dependencies
pip install -r requirements.txt --no-dev

# Build Docker images
docker build -t piper-morgan:latest .

# Run migrations
python scripts/run-migrations.py

# Start application
python main.py
```

### Monitoring

- Check `/api/health` endpoint for system status
- Monitor database connections
- Track error rates and response times
- Review logs for warnings and errors

---

## Additional Resources

- **[Plugin Development Guide](guides/plugin-development-guide.md)** - Detailed plugin creation tutorial
- **[Intent Classification Guide](guides/intent-classification-guide.md)** - Intent system deep dive
- **[Architecture Decisions](https://github.com/mediajunkie/piper-morgan-product/tree/main/docs/internal/architecture/current/adrs)** - Design rationale
- **[Domain Models Reference](https://github.com/mediajunkie/piper-morgan-product/tree/main/docs/internal/architecture/current/models)** - Complete model documentation
- **[CLAUDE.md](../CLAUDE.md)** - Agent development guidelines

---

**Need Help?** Check the [main README](README.md) for support options or consult the [NAVIGATION guide](NAVIGATION.md) to find relevant documentation.
