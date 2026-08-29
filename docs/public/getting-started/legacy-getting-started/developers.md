# Developer Quick Start

Complete development environment setup for Piper Morgan. This guide will get you from zero to a fully functional development environment.

## Prerequisites

- **Python 3.11** (required - exactly 3.11, not 3.12+)
  - Docker with Python 3.11 base images
  - Git
- **Docker & Docker Compose**
- **PostgreSQL 14+**
- **Redis 7+**
- **Node.js 18+** (for frontend development)
- **GitHub CLI** (recommended)

### Python 3.11 Requirement

Piper Morgan specifically requires Python 3.11 for `asyncio.timeout` support and other 3.11-specific features. Using Python 3.12+ will cause compatibility issues.

## Environment Setup

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product

# Verify .python-version file
cat .python-version  # Should show 3.11
```

### 2. Python Environment Setup

```bash
# Verify Python version (must be 3.11 exactly)
python --version  # Should show Python 3.11.x

# Set up Python virtual environment with Python 3.11
python3.11 -m venv venv  # Explicitly use Python 3.11
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Verify Python version in virtual environment
python --version  # Should show Python 3.11.x

# Install dependencies
pip install -r requirements.txt

# Verify asyncio.timeout availability (requires Python 3.11)
python -c "import asyncio; asyncio.timeout(1.0); print('✅ Python 3.11 verified')"
```

### 3. Environment Variables

Copy the example environment file and configure:

```bash
# Copy environment template
cp .env.example .env
# Edit .env with your API keys and configuration
```

**Required Environment Variables:**

```bash
# AI Integration
ANTHROPIC_API_KEY=required
OPENAI_API_KEY=required

# GitHub Integration
GITHUB_TOKEN=for_gh_commands

# Database Configuration
DATABASE_URL=postgresql://piper:dev_changeme_in_production@localhost:5433/piper_morgan

# Redis Configuration
REDIS_URL=redis://localhost:6379
```

**Configuration Notes:**
- All API keys are required for full functionality
- Database runs on port 5433 (not default 5432) to avoid conflicts
- Redis uses default port 6379

### 4. Infrastructure Services Setup

```bash
# Start infrastructure services
docker-compose up -d postgres redis

# Initialize the database
python scripts/init_db.py

# Verify database connection
docker exec -it piper-postgres psql -U piper -d piper_morgan
```

### 5. Docker Setup (Alternative)

```bash
# Docker containers now use Python 3.11
docker-compose build
docker-compose up

# Verify container Python version
docker-compose exec app python --version  # Should show Python 3.11.x
```

### 6. Verification & Startup

```bash
# Start the development server
python main.py  # API runs on port 8001

# Start the web interface (separate terminal)
cd web && python -m uvicorn app:app --reload --port 8081

# Run comprehensive tests
PYTHONPATH=. python -m pytest tests/unit/ -v

# Verify asyncio.timeout functionality
python -c "import asyncio; asyncio.timeout(1.0); print('✅ Python 3.11 asyncio support verified')"
```

## Development Workflow

### Testing

**CRITICAL**: Always use the full PYTHONPATH prefix. Never use bare `pytest`.

```bash
# Run all tests
PYTHONPATH=. pytest

# Run API query integration tests
PYTHONPATH=. pytest tests/test_api_query_integration.py

# Unit tests
PYTHONPATH=. python -m pytest tests/unit/ -v

# Integration tests
PYTHONPATH=. python -m pytest tests/integration/ -v

# Run with coverage reporting
PYTHONPATH=. python -m pytest tests/ --cov=services --cov-report=term-missing

# Fast failure mode for development
PYTHONPATH=. python -m pytest tests/ -x -v

# Database-free testing (Excellence Flywheel infrastructure)
python tests/orchestration/run_standalone_tests.py

# Specific test
PYTHONPATH=. python -m pytest tests/integration/test_file.py::TestClass::test_method -v
```

**Testing Notes:**
- Some asyncpg/SQLAlchemy warnings may appear during test teardown; these are benign
- Database integration tests use port 5433
- Always verify existing patterns before writing new tests
- Use `async_transaction` fixture for database tests

### Database Operations

```bash
# Access PostgreSQL
docker exec -it piper-postgres psql -U piper -d piper_morgan

# View logs
docker-compose logs postgres
docker-compose logs redis
```

### Code Quality

Follow the project's architectural patterns:
- Domain models in `services/domain/models.py` drive everything
- Use `AsyncSessionFactory.session_scope()` for all DB operations
- Repositories handle data access only
- Services contain business logic
- All enums go in `services/shared_types.py`

## Project Structure

```
services/
├── domain/models.py           # Source of truth - check first
├── shared_types.py            # All enums here
├── orchestration/             # Workflows, multi-agent coordination
├── queries/                   # Read operations (CQRS)
├── repositories/              # Data access only
└── integrations/              # GitHub, Slack, external

tests/
├── unit/                      # Fast, mocked tests
├── integration/               # Real DB tests (port 5433)
└── conftest.py               # Fixtures: async_session, async_transaction
```

## Common Tasks

### Adding a New Feature

**Excellence Flywheel Methodology**: Verify first → Implement second → Evidence-based progress

1. **Verification Phase**:
   ```bash
   grep -r "pattern" services/ --include="*.py" -A 3 -B 3  # Find existing patterns
   cat services/domain/models.py | grep "class"            # Check domain models
   find . -name "*.py" -exec grep -l "ADR-" {} \;         # Find architectural decisions
   ```

2. **Implementation Phase**:
   - Update domain models first (`services/domain/models.py`)
   - Add any new enums to `services/shared_types.py`
   - Create repository layer for data access
   - Implement service layer for business logic
   - Add comprehensive tests
   - Update API endpoints if needed

3. **Evidence Phase**:
   ```bash
   PYTHONPATH=. python -m pytest [test] -v                 # Run actual tests
   # See "X passed" before claiming success
   ```

### Database Schema Changes

1. Modify domain models in `services/domain/models.py` (source of truth)
2. Generate Alembic migration: `alembic revision --autogenerate -m "description"`
3. Test migration locally: `alembic upgrade head`
4. Update integration tests
5. Verify with `AsyncSessionFactory.session_scope()` pattern

### Session Protocol

1. Create session log: `development/session-logs/YYYY-MM-DD-log.md`
2. Check handoffs: `docs/development/prompts/*-handoff-*.md`
3. Complex tasks: Use TodoWrite tool
4. End session: Update GitHub issues with evidence

## Debugging

### Common Issues

- **Import Errors**: Ensure `PYTHONPATH=.` is used (never bare pytest)
- **Python Version Issues**: Must use Python 3.11 exactly (asyncio.timeout requirement)
- **Database Connection**: Check Docker services are running on port 5433
- **Test Failures**: Use `async_transaction` fixture for database tests
- **API Errors**: Check logs in `python main.py` output
- **AsyncPG Warnings**: Benign asyncpg/SQLAlchemy warnings during test teardown (safe to ignore)
- **MCP Integration Issues**: Verify API keys are properly configured
- **Performance Issues**: Check connection pooling is enabled (642x improvement available)

### Useful Commands

```bash
# View all Docker services
docker-compose ps

# Restart a specific service
docker-compose restart postgres

# View application logs
docker-compose logs -f api

# View database and Redis logs
docker-compose logs postgres
docker-compose logs redis

# CLI Standup (Production Feature)
python main.py standup  # <2 second execution, beautiful formatting

# Pre-commit Hook Strategy
# Check what pre-commit will do without changing files
pre-commit run --all-files --show-diff-on-failure

# Let pre-commit fix formatting issues
pre-commit run --all-files

# Skip specific hooks if needed (emergency use only)
SKIP=end-of-file-fixer,trailing-whitespace git commit -m "Your message"
```

## Advanced Development Topics

### Staging Environment (Production-Grade)

For testing MCP integration and production readiness:

```bash
# One-command staging deployment
./scripts/deploy_staging.sh

# Verify staging deployment (14 comprehensive tests)
./scripts/verify_staging_deployment.sh

# Access staging services
# API: http://localhost:8001
# Web UI: http://localhost:8081
# Grafana: http://localhost:3001
# Prometheus: http://localhost:9090
```

**Staging Features:**
- MCP Integration with 642x performance improvement
- Production monitoring with Prometheus + Grafana dashboards
- Health checks and comprehensive component monitoring
- Automated rollback procedures
- Performance validation: <500ms search target (achieving ~60ms)

### Architecture Patterns

**Domain-Driven Design**:
- Domain models in `services/domain/models.py` drive everything - DB follows models
- `AsyncSessionFactory.session_scope()` for all DB operations
- Repositories for data access only - no business logic
- Services for business logic - no direct DB access
- All enums in `services/shared_types.py` only

**MCP + Spatial Intelligence**:
- 8-dimensional spatial analysis: HIERARCHY, TEMPORAL, PRIORITY, COLLABORATIVE, FLOW, QUANTITATIVE, CAUSAL, CONTEXTUAL
- Sub-1ms federated search (150x better than industry standards)
- Connection pooling for 642x performance improvement

## Next Steps

- Read the [Architecture Documentation](../architecture/)
- Review the [Excellence Flywheel Methodology](../development/methodology-core/)
- Check out [Multi-Agent Coordinator Guide](../../../internal/architecture/current/multi-agent-coordinator-pm-guide.md)
- Explore [Architecture Patterns](../../../internal/architecture/patterns/README.md) - 27 consolidated patterns
- Study [MCP Integration Patterns](../architecture/mcp-integration-patterns.md)
- Review [API Reference](../../../internal/architecture/current/api-reference.md)

---

## Documentation Architecture

Piper Morgan uses a **three-tier documentation structure**:

1. **Getting Started** (this tier): Quick setup and basic usage
2. **Architecture & Development**: Deep technical guidance and patterns
3. **Operations & Deployment**: Production deployment and maintenance

## Key Development Resources

- **[Staging Deployment Guide](../../../internal/operations/legacy-operations/staging-deployment-guide.md)** - Production-grade local staging
- **[Excellence Flywheel Methodology](../development/methodology-core/)** - Core development philosophy
- **[Test Infrastructure Guide](../../../internal/development/active/pending-review/TEST-GUIDE.md)** - Smart test execution (599+ tests)
- **[Multi-Agent Integration](../../../internal/development/methodology-core/MULTI_AGENT_INTEGRATION_GUIDE.md)** - AI coordination patterns
- **[Morning Standup MVP](../../../internal/development/tools/MORNING_STANDUP_MVP_GUIDE.md)** - CLI interface usage

*For production deployment, see the [Production Guide](production.md). For API integration, see [API Integration](api-integration.md).*
