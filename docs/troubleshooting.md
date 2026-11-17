# Troubleshooting Guide

## Setup Wizard Issues (Issue #218)

### "Docker is not installed"

**Error**: Setup wizard reports Docker is not installed.

**Solution**: Install Docker Desktop:
- **macOS**: https://docs.docker.com/desktop/mac/install/
- **Windows**: https://docs.docker.com/desktop/windows/install/
- **Linux**: https://docs.docker.com/engine/install/

Verify with: `docker --version`

### "Port 8001 is not available"

**Error**: Setup wizard reports port 8001 is already in use.

**Solution**:
```bash
# Find what's using port 8001
lsof -i :8001

# Stop existing Piper Morgan instance
# Only for a computer that runs a single copy of Piper. This stops the stack, and a volume flag deletes its database. Never run it on a shared stack.
docker compose down
```

### "Database is not accessible"

**Error**: Setup wizard cannot connect to database.

**Solution**:
```bash
# Start database
docker compose up -d db

# Wait 10 seconds
sleep 10

# Try setup again
python main.py setup
```

### "OpenAI API key is invalid"

**Error**: Setup wizard rejects OpenAI API key.

**Causes**:
1. Typo in key (should start with `sk-`)
2. Key revoked or expired
3. Network connectivity issues
4. Rate limit exceeded

**Solution**:
1. Double-check key from https://platform.openai.com/api-keys
2. Test key:
   ```bash
   curl https://api.openai.com/v1/models \
     -H "Authorization: Bearer YOUR_KEY"
   ```
3. Wait a few minutes if rate limited

### "Anthropic API key is invalid"

**Error**: Setup wizard rejects Anthropic API key.

**Solution**:
1. Verify key from https://platform.claude.com/settings/keys
2. Ensure key starts with `sk-ant-`
3. Verify key has Claude API access

---

## Python Version Issues

### AsyncIO.timeout AttributeError

**Error**: `AttributeError: module 'asyncio' has no attribute 'timeout'`

**Cause**: Python version < 3.11

**Solution**:

```bash
# Check Python version
python --version

# If < 3.11, install Python 3.11+
pyenv install 3.11.9
pyenv local 3.11.9

# Verify fix
python -c "import asyncio; asyncio.timeout(1.0); print('✅ Fixed')"
```

### Docker Python Version Mismatch

**Error**: Container tests fail with version errors

**Solution**:

```bash
# Rebuild with Python 3.11 base
docker compose build --no-cache
docker compose run app python --version  # Verify 3.11+
```

### CI/CD Python Version Failures

**Error**: GitHub Actions fail with Python compatibility

**Solution**: Workflows updated to use Python 3.11 - clear cache and retry

```bash
# Check workflow configuration
cat .github/workflows/test.yml | grep "python-version"
# Should show: python-version: '3.11'
```

## Environment Setup Issues

### Virtual Environment Wrong Python Version

**Problem**: Virtual environment created with wrong Python version

**Solution**:

```bash
# Remove old virtual environment
rm -rf venv

# Create new with Python 3.11
python3.11 -m venv venv
source venv/bin/activate

# Verify version
python --version  # Should show 3.11.x
```

### Dependency Installation Failures

**Problem**: Package installation fails with version conflicts

**Solution**:

```bash
# Deactivate and reactivate virtual environment
deactivate
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### IDE Python Interpreter Issues

**Problem**: IDE not recognizing Python 3.11

**Solution**:

**VS Code**:

1. `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Windows/Linux)
2. "Python: Select Interpreter"
3. Choose Python 3.11 from virtual environment

**PyCharm**:

1. File → Settings → Project → Python Interpreter
2. Add interpreter → Existing environment
3. Select `./venv/bin/python`

## Testing Issues

### Test Failures with Python Version Errors

**Problem**: Tests fail with Python compatibility warnings

**Solution**:

```bash
# Run with Python 3.11 specific checks
python -W error::DeprecationWarning -m pytest tests/

# Check for version-specific issues
python -c "import sys; print(f'Python {sys.version}')"
```

### Async Test Failures

**Problem**: Async tests fail with timeout or context errors

**Solution**:

```bash
# Verify asyncio.timeout availability
python -c "import asyncio; asyncio.timeout(1.0); print('✅ asyncio.timeout available')"

# Run async tests with proper event loop
pytest tests/ -v --asyncio-mode=auto
```

## Docker Issues

### Container Build Failures

**Problem**: Docker build fails with Python version errors

**Solution**:

```bash
# Check Dockerfile Python version
grep "FROM python" services/orchestration/Dockerfile
# Should show: FROM python:3.11-slim-buster

# Rebuild with no cache
docker-compose build --no-cache
```

### Container Runtime Issues

**Problem**: Container fails to start or crashes

**Solution**:

```bash
# Check container logs
docker-compose logs app

# Verify container Python version
docker-compose exec app python --version

# Check container dependencies
docker-compose exec app python -c "import fastapi, sqlalchemy; print('✅ Dependencies OK')"
```

## CI/CD Issues

### GitHub Actions Failures

**Problem**: CI/CD workflows fail with Python version errors

**Solution**:

```bash
# Check workflow configuration
cat .github/workflows/test.yml | grep -A 5 -B 5 "python-version"

# Verify workflow syntax
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/test.yml'))"
```

### Cache Issues

**Problem**: CI/CD cache causing version conflicts

**Solution**: Clear GitHub Actions cache or update cache keys

```yaml
# Check cache configuration in workflows
- name: Cache Python dependencies
  uses: actions/cache@v3
  with:
    key: ${{ runner.os }}-pip-3.11-${{ hashFiles('**/requirements.txt') }}
```

## Performance Issues

### Slow Async Operations

**Problem**: Async operations are slower than expected

**Solution**:

```bash
# Verify Python 3.11 performance features
python -c "
import asyncio
import time

async def test_performance():
    start = time.time()
    async with asyncio.timeout(1.0):
        await asyncio.sleep(0.1)
    print(f'Async operation took: {time.time() - start:.3f}s')

asyncio.run(test_performance())
"
```

### Memory Usage Issues

**Problem**: High memory usage in async operations

**Solution**: Check for proper resource cleanup

```python
# Ensure proper async context management
async def proper_resource_usage():
    async with asyncio.timeout(5.0):
        async with some_resource() as resource:
            result = await resource.operation()
    return result
```

## Common Error Messages and Solutions

### "Module 'asyncio' has no attribute 'timeout'"

- **Cause**: Python < 3.11
- **Solution**: Upgrade to Python 3.11+

### "Python version 3.11 is required"

- **Cause**: Version constraint in pyproject.toml
- **Solution**: Ensure Python 3.11+ is active

### "Docker build failed: unsupported Python version"

- **Cause**: Dockerfile specifies Python 3.11
- **Solution**: Rebuild with Python 3.11 base image

### "CI/CD workflow failed: Python version mismatch"

- **Cause**: Workflow expects Python 3.11
- **Solution**: Check workflow configuration and cache

## Getting Help

### Self-Diagnosis Steps

1. **Check Python version**: `python --version`
2. **Verify asyncio.timeout**: `python -c "import asyncio; asyncio.timeout(1.0)"`
3. **Check virtual environment**: `echo $VIRTUAL_ENV`
4. **Verify dependencies**: `pip list | grep -E "(fastapi|sqlalchemy|pytest)"`
5. **Check Docker version**: `docker-compose exec app python --version`

### Resources

- [Contributing Guidelines](../CONTRIBUTING.md)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Async Guide](https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html)
- [Docker Compose Troubleshooting](https://docs.docker.com/compose/troubleshooting/)

### Support Channels

- **GitHub Issues**: For bug reports and feature requests
- **Team Chat**: For quick questions and troubleshooting
- **Code Review**: For specific implementation issues

## Prevention

### Best Practices

1. **Always verify Python version** before starting development
2. **Use virtual environments** with Python 3.11
3. **Run tests regularly** to catch version issues early
4. **Keep dependencies updated** for Python 3.11 compatibility
5. **Use pre-commit hooks** to catch issues before commit

### Validation Scripts

```bash
#!/bin/bash
# validation.sh - Quick environment validation

echo "=== Environment Validation ==="
echo "Python version: $(python --version)"
echo "Virtual environment: $VIRTUAL_ENV"
python -c "import asyncio; asyncio.timeout(1.0); print('✅ asyncio.timeout available')"
python -c "import fastapi, sqlalchemy, pytest; print('✅ Key dependencies available')"
echo "=== Validation Complete ==="
```

Run this script regularly to ensure your environment is properly configured.


# Additional Troubleshooting (from development guide)

# Piper Morgan 1.0 - Troubleshooting Guide

## Overview

This guide addresses common issues encountered during Piper Morgan development and deployment. Issues are organized by category with step-by-step resolution procedures.

## Environment Setup Issues

### Docker Services Won't Start

**Symptoms:**
- `docker-compose up -d` fails
- Port conflicts (5432, 6379, 8000)
- Service health checks failing

**Resolution:**
```bash
# Check for port conflicts
lsof -i :5432  # PostgreSQL
lsof -i :6379  # Redis
lsof -i :8000  # ChromaDB

# Stop conflicting services
brew services stop postgresql  # If Homebrew PostgreSQL running
sudo systemctl stop redis     # If system Redis running

# Clean up Docker state
# Only for a computer that runs a single copy of Piper. This stops the stack, and a volume flag deletes its database. Never run it on a shared stack.
docker-compose down --volumes
docker system prune -f
docker-compose up -d

# Verify services
docker-compose ps
```

**Common Causes:**
- Homebrew PostgreSQL claiming port 5432
- Previous Docker containers not cleaned up
- Insufficient Docker resources allocated

### Python Environment Issues

**Symptoms:**
- Import errors despite installed packages
- `ModuleNotFoundError` for local services
- Type checking failures

**Resolution:**
```bash
# Ensure virtual environment activated
source venv/bin/activate

# Verify Python path includes project root
python -c "import sys; print('\n'.join(sys.path))"

# Reinstall dependencies
pip install -r requirements.txt

# Add project root to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Verify imports work
python -c "from services.domain.models import Project; print('OK')"
```

### Environment Variables Not Loading

**Symptoms:**
- `None` values for API keys
- Services failing with authentication errors
- "API key not found" messages

**Resolution:**
```bash
# Check .env file exists and is readable
ls -la .env
cat .env | grep -v "^#" | head -5  # Don't expose keys

# Verify load_dotenv() calls
grep -r "load_dotenv" services/

# Test environment loading
python -c "
from dotenv import load_dotenv
import os
load_dotenv()
print('ANTHROPIC_API_KEY set:', bool(os.getenv('ANTHROPIC_API_KEY')))
"
```

**Critical Fix Pattern:**
```python
# Always add at top of modules using os.getenv()
from dotenv import load_dotenv
load_dotenv()  # BEFORE any os.getenv() calls

import os
api_key = os.getenv('ANTHROPIC_API_KEY')
```

## Runtime Issues

### Intent Classification Failures

**Symptoms:**
- Low confidence scores (<0.5)
- Incorrect intent categories
- "UNKNOWN" classifications for valid requests

**Diagnosis:**
```bash
# Check LLM service status
curl -X POST http://localhost:8001/api/v1/intent \
  -H "Content-Type: application/json" \
  -d '{"message": "test classification"}'

# Enable debug logging
export LOG_LEVEL=DEBUG
```

**Resolution:**
- **Knowledge Base Issues**: Upload more relevant PM documents
- **Prompt Problems**: Check intent classification prompts for clarity
- **API Failures**: Verify Claude/OpenAI API keys and quotas
- **Context Missing**: Ensure knowledge search returns relevant results

### Database Connection Errors

**Symptoms:**
- `sqlalchemy.exc.OperationalError`
- "Connection refused" to PostgreSQL
- Workflow state not persisting

**Resolution:**
```bash
# Check PostgreSQL container
docker logs piper-postgres

# Test database connection
python -c "
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

async def test():
    engine = create_async_engine('postgresql+asyncpg://piper:dev_changeme@localhost/piper_morgan')
    async with engine.begin() as conn:
        result = await conn.execute('SELECT 1')
        print('DB connection OK:', result.scalar())
    await engine.dispose()

asyncio.run(test())
"

# Initialize database schema
python -c "
import asyncio
from services.database.session import init_database
asyncio.run(init_database())
"
```

### Knowledge Base Search Issues

**Symptoms:**
- Poor search relevance
- Empty search results
- ChromaDB connection errors

**Diagnosis:**
```bash
# Check ChromaDB status
curl http://localhost:8000/api/v1/version

# Verify document ingestion
python -c "
import chromadb
client = chromadb.HttpClient(host='localhost', port=8000)
collection = client.get_collection('pm_knowledge')
print('Document count:', collection.count())
"
```

**Resolution:**
- **Empty Collection**: Re-run document ingestion
- **Poor Relevance**: Tune chunking strategy and embedding parameters
- **Connection Issues**: Restart ChromaDB container

## API Issues

### 404 Not Found Errors

**Symptoms:**
- API endpoints return 404
- FastAPI not starting correctly
- Route registration failures

**Diagnosis:**
```bash
# Check FastAPI startup logs
docker logs piper-api  # If containerized
# OR
python main.py  # Direct startup

# Verify routes registered
curl http://localhost:8001/docs  # OpenAPI docs
```

**Common Causes:**
- Missing route registration in main.py
- Import errors in route modules
- Port conflicts or service not starting

### 422 Validation Errors

**Symptoms:**
- Request validation failures
- Pydantic model errors
- Missing required fields

**Resolution:**
```bash
# Test with valid request format
curl -X POST http://localhost:8001/api/v1/intent \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Create a ticket for login bug",
    "session_id": "test-123"
  }'

# Check API documentation
open http://localhost:8001/docs
```

### 500 Internal Server Errors

**Symptoms:**
- Unhandled exceptions
- Service crashes
- Database transaction failures

**Diagnosis:**
```bash
# Check application logs
tail -f logs/app.log

# Enable detailed error tracking
export LOG_LEVEL=DEBUG
export SHOW_ERROR_DETAILS=true
```

**Common Causes:**
- Uninitialized database schemas
- Missing environment variables
- Service dependency failures

## Testing Issues

### Async Test Failures

**Symptoms:**
- `RuntimeError: This event loop is already running`
- Test timeouts
- Fixture dependency errors

**Resolution:**
```python
# Ensure proper async test setup
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result is not None

# Configure pytest.ini
[tool.pytest.ini_options]
asyncio_mode = "auto"
```

### Test Database Issues

**Symptoms:**
- Tests interfering with each other
- Database state not cleaned
- Connection pool exhaustion

**Resolution:**
```python
# Use isolated test database
@pytest.fixture
async def test_db():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()
```

### Mock Configuration Problems

**Symptoms:**
- Mocks not applying correctly
- Real API calls during tests
- Inconsistent test results

**Resolution:**
```python
# Proper mock setup
from unittest.mock import Mock, AsyncMock

@pytest.fixture
def mock_llm_client():
    client = Mock()
    client.complete = AsyncMock(return_value="test response")
    return client

# Verify mock calls
def test_with_mock(mock_llm_client):
    # ... test code ...
    mock_llm_client.complete.assert_called_once()
```

## Performance Issues

### Slow Response Times

**Symptoms:**
- API responses >5 seconds
- Knowledge search timeouts
- Workflow execution delays

**Diagnosis:**
```bash
# Profile API performance
time curl -X POST http://localhost:8001/api/v1/intent \
  -H "Content-Type: application/json" \
  -d '{"message": "list projects"}'

# Check database query performance
export LOG_LEVEL=DEBUG  # Shows SQL queries
```

**Optimization Steps:**
1. **Database**: Add indexes, optimize queries
2. **Knowledge Search**: Reduce search scope, tune parameters
3. **Caching**: Implement Redis caching for frequent queries
4. **Concurrency**: Use async operations properly

### Memory Usage Issues

**Symptoms:**
- Increasing memory consumption
- Out of memory errors
- Container restarts

**Monitoring:**
```bash
# Monitor container memory
docker stats

# Python memory profiling
pip install memory-profiler
python -m memory_profiler your_script.py
```

## Development Workflow Issues

### Git Workflow Problems

**Symptoms:**
- Merge conflicts in generated files
- Branch synchronization issues
- Lost work due to force pushes

**Best Practices:**
```bash
# Create feature branch
git checkout -b feature/pm-XXX-description

# Regular commits with clear messages
git commit -m "PM-009: Add project context resolution

- Implement ProjectContext class
- Add session memory for project tracking
- Update workflow factory integration"

# Sync with main regularly
git fetch origin
git rebase origin/main
```

### Code Review Issues

**Symptoms:**
- Architectural drift
- Pattern violations
- Missing tests

**Prevention:**
```bash
# Pre-commit checks
grep -r "create.*workflow" services/  # Check patterns
mypy services/  # Type checking
pytest  # All tests pass
```

## Debugging Techniques

### Structured Logging

```python
import structlog

logger = structlog.get_logger()

# Add context to all log entries
logger.info(
    "processing_intent",
    intent_id=intent.id,
    category=intent.category.value,
    confidence=intent.confidence,
    user_id=session_id
)
```

### Interactive Debugging

```python
# Drop into debugger on errors
import pdb; pdb.set_trace()

# Or use ipdb for better interface
import ipdb; ipdb.set_trace()

# VS Code debugging
# Set breakpoints in IDE and run with debugger
```

### Health Check Endpoints

```bash
# System health
curl http://localhost:8001/api/v1/health

# Individual service checks
curl http://localhost:8000/api/v1/version  # ChromaDB
curl http://localhost:8088/  # Temporal UI
```

## Emergency Procedures

### Complete System Reset

```bash
# Nuclear option - reset everything
# Only for a computer that runs a single copy of Piper. This stops the stack, and a volume flag deletes its database. Never run it on a shared stack.
docker-compose down --volumes
docker system prune -a -f
rm -rf data/  # Clears all persistent data
docker-compose up -d

# Reinitialize
python -c "
import asyncio
from services.database.session import init_database
asyncio.run(init_database())
"

# Re-upload knowledge base
python scripts/upload_docs.py  # If exists
```

### Data Recovery

```bash
# Backup before major changes
docker exec piper-postgres pg_dump -U piper piper_morgan > backup.sql

# Restore from backup
docker exec -i piper-postgres psql -U piper piper_morgan < backup.sql
```

## Getting Help

### Log Analysis

**Check these locations:**
- Application logs: `logs/app.log`
- Docker logs: `docker-compose logs [service]`
- System logs: `/var/log/` (production)

### Useful Commands

```bash
# Service status overview
docker-compose ps

# Resource usage
docker stats --no-stream

# Network connectivity
docker-compose exec api ping postgres

# Database inspection
docker-compose exec postgres psql -U piper -d piper_morgan -c "\dt"
```

### External Resources

- **FastAPI Issues**: [FastAPI GitHub Issues](https://github.com/tiangolo/fastapi/issues)
- **SQLAlchemy Async**: [Official Async Guide](https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html)
- **Docker Compose**: [Compose Troubleshooting](https://docs.docker.com/compose/troubleshooting/)
- **ChromaDB**: [ChromaDB Documentation](https://docs.trychroma.com/)

## Prevention Strategies

### Regular Maintenance

```bash
# Weekly cleanup
docker system prune -f
docker-compose pull  # Update images

# Monthly tasks
pip list --outdated  # Check for updates
brew update && brew upgrade  # Update system tools
```

### Monitoring Setup

```python
# Add health checks to critical services
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "services": {
            "database": await check_database(),
            "chromadb": await check_chromadb(),
            "redis": await check_redis()
        }
    }
```

---
*Last Updated: June 21, 2025*

## Revision Log
- **June 21, 2025**: Initial troubleshooting guide creation with common Piper Morgan issues
