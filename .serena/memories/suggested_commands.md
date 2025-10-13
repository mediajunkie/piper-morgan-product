# Piper Morgan - Essential Commands

## Development Setup
```bash
# Initial setup
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add your API keys

# Start services
docker-compose up -d
python main.py
```

## Testing Commands (Updated - pytest.ini handles PYTHONPATH automatically)
```bash
# All tests (pytest.ini configures pythonpath=. automatically)
python -m pytest tests/ -v

# Test categories
python -m pytest tests/unit/ -v          # Unit tests
python -m pytest tests/integration/ -v   # Integration tests
python -m pytest tests/plugins/ -v       # Plugin tests

# Performance and benchmarks
python -m pytest tests/performance/ -v
PYTHONPATH=. python scripts/benchmark_performance.py  # Scripts still need PYTHONPATH

# Coverage reporting
python -m pytest tests/ --cov=services --cov-report=term-missing
```

## Web Application
```bash
# Start web server
PYTHONPATH=. python web/app.py
# or
PYTHONPATH=. python -m uvicorn web.app:app --host 127.0.0.1 --port 8001

# Access points
# Web UI: http://localhost:8001/standup
# API docs: http://localhost:8001/docs
# Health check: http://localhost:8001/health
```

## Code Quality
```bash
# Format code
black services/ tests/ scripts/
isort services/ tests/ scripts/

# Run linting
flake8 services/ tests/

# Pre-commit hooks
pre-commit run --all-files
```

## Plugin Development
```bash
# Test plugin system (pytest.ini handles PYTHONPATH)
pytest tests/plugins/ -v

# Test specific integration
pytest services/integrations/[name]/tests/ -v
```

## Database & Migrations
```bash
# Run migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "Description"
```

## Validation & Schema (Scripts still need PYTHONPATH)
```bash
# Validate configuration
PYTHONPATH=. python tools/schema_validator.py

# Check domain/database consistency
PYTHONPATH=. python tools/check_domain_db_consistency.py
```