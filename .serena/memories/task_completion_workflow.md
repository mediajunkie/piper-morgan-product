# Piper Morgan - Task Completion Workflow

## Before Starting Any Task
1. **Verify Infrastructure**: Check that expected files/directories exist
2. **Read Briefing Documents**: Check knowledge/ directory for context
3. **Activate Virtual Environment**: `source venv/bin/activate`
4. **Set PYTHONPATH**: Always use `PYTHONPATH=.` for Python commands

## Development Workflow
1. **Create Working Branch**: Follow git flow practices
2. **Write Tests First**: TDD approach preferred
3. **Implement Changes**: Follow established patterns
4. **Run Quality Checks**: Format, lint, test
5. **Update Documentation**: Keep docs in sync

## Quality Assurance Checklist
```bash
# 1. Format code
black services/ tests/ scripts/
isort services/ tests/ scripts/

# 2. Run linting
flake8 services/ tests/

# 3. Run tests with coverage
PYTHONPATH=. python -m pytest tests/ -v --cov=services --cov-report=term-missing

# 4. Run performance benchmarks (if applicable)
PYTHONPATH=. python scripts/benchmark_performance.py

# 5. Validate architecture compliance
PYTHONPATH=. python -m pytest tests/test_architecture_enforcement.py -v
```

## Pre-commit Requirements
- **Code formatting**: Black and isort must pass
- **Linting**: flake8 must pass clean
- **Architecture enforcement**: No direct adapter imports
- **Documentation**: Update relevant docs
- **GitHub sync**: Update backlog.md if planning docs change

## Testing Requirements
- **Unit tests**: Fast tests (<30 seconds total)
- **Integration tests**: May take up to 2 minutes
- **Performance tests**: Benchmark critical paths
- **Plugin tests**: Contract compliance for integrations

## Deployment Checklist
1. **All tests passing**: Full test suite green
2. **Performance gates**: No regressions detected
3. **Security checks**: No vulnerabilities introduced
4. **Documentation updated**: READMEs and guides current
5. **Configuration validated**: All services properly configured

## Post-completion
1. **Update session logs**: Document work completed
2. **Create deliverables**: Summarize changes and impact
3. **Update GitHub issues**: Mark tasks complete with evidence
4. **Push changes**: Ensure remote repository is updated