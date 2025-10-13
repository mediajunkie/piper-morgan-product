# Piper Morgan - Code Style & Conventions

## Code Formatting
- **Black**: Line length 100 characters, Python 3.9+ target
- **isort**: Black-compatible import sorting
- **flake8**: Linting with standard rules

## File Organization
- **services/**: Core business logic organized by domain
- **web/**: FastAPI application and web interface
- **tests/**: Comprehensive test suite with markers
- **config/**: Configuration management
- **docs/**: Documentation and architecture decisions

## Naming Conventions
- **Files**: snake_case.py
- **Classes**: PascalCase
- **Functions/Variables**: snake_case
- **Constants**: UPPER_SNAKE_CASE
- **Enums**: Defined in services/shared_types.py

## Type Hints & Documentation
- **Type hints**: Required for all public methods
- **Docstrings**: Google-style docstrings for classes and public methods
- **Pydantic models**: For data validation and API schemas

## Testing Conventions
- **Test markers**: smoke, unit, integration, performance, benchmark, contract
- **File naming**: test_*.py pattern
- **Async tests**: Automatic asyncio mode enabled
- **Coverage**: Tiered coverage enforcement in CI/CD

## Architecture Patterns
- **Plugin Interface**: All integrations implement PiperPlugin ABC
- **Router Pattern**: Integration routers for external services
- **Config Services**: Dedicated configuration validation per integration
- **Auto-registration**: Plugins register themselves on import

## Git & CI/CD
- **Pre-commit hooks**: Automated formatting, linting, architecture enforcement
- **Branch protection**: Quality gates prevent direct commits
- **Performance gates**: Automated benchmarking and regression detection