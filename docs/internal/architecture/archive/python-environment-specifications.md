> **ARCHIVED 2026-08-02** — moved from `docs/internal/architecture/current/` per the docs/ tree
> audit (`docs/internal/operations/docs-tree-audit-2026-08-01.md`, Finding 2) and Arch's per-file
> ruling. Zero inbound references confirmed across `docs/ services/ web/ scripts/ tests/ .claude/
> mailboxes/ CLAUDE.md` — a terminal artifact, finished when written, not a living document that went
> stale. Kept for the record, not current. Never delete; if this needs reviving, un-archive it rather
> than rewriting it fresh.

---

# Python Environment Specifications

**Created:** 2025-07-22 (PM-055 Environment Standardization)
**Status:** Production Standard
**Enforcement:** Required across all contexts

## Overview

Following PM-055 systematic completion, Piper Morgan enforces Python 3.11 consistency across all development, testing, and production environments to prevent version-specific bugs and ensure reliable deployment.

## Version Requirements

### Core Requirement
- **Python 3.11+** - Required minimum version
- **Python 3.11.13** - Current verified production version
- **Python 3.9 support** - Deprecated, migration path documented

### Rationale
- **asyncio.timeout availability** - Core PM-055 objective achieved
- **Performance improvements** - Modern async patterns enabled
- **Type hint enhancements** - Better development experience
- **Security updates** - Latest Python 3.11 branch maintenance

## Environment Standardization

### Development Environment

#### Local Development
```bash
# Version specification
echo "3.11" > .python-version

# Virtual environment creation
python3.11 -m venv venv
source venv/bin/activate

# Version verification
python scripts/verify-python-version.sh
```

#### Requirements
- `.python-version` file in project root
- `pyproject.toml` with `requires-python = ">=3.11"`
- Virtual environment with Python 3.11

### Docker Environment

#### Base Images
- **Main Application**: `python:3.11-slim-bullseye`
- **Orchestration Service**: `python:3.11-slim-bullseye`
- **All Containers**: Python 3.11 consistency enforced

#### Configuration
```dockerfile
FROM python:3.11-slim-bullseye

# Version verification during build
ENV PYTHON_VERSION=3.11
COPY scripts/verify-python-version.sh /usr/local/bin/
RUN /usr/local/bin/verify-python-version.sh

# Health check includes version compliance
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s \
    CMD /usr/local/bin/verify-python-version.sh && python -c "import requests; requests.get('http://localhost:8001/health')"
```

### CI/CD Environment

#### GitHub Actions
```yaml
strategy:
  matrix:
    python-version: ['3.11']

steps:
  - uses: actions/setup-python@v4
    with:
      python-version: '3.11'
```

#### Testing Pipeline
- Python 3.11 matrix testing enabled
- Version verification in all test runs
- Container builds verify Python compliance

## Version Verification

### Automated Verification Script
**Location**: `scripts/verify-python-version.sh`

**Features**:
- Cross-platform compatibility (GNU/BSD)
- PM-055 compliance checking (≥3.11)
- Core dependency verification
- Async pattern testing
- Detailed logging and error reporting

**Usage**:
```bash
# Standalone verification
./scripts/verify-python-version.sh

# Container verification
docker run piper-morgan-app /usr/local/bin/verify-python-version.sh

# CI/CD integration
python scripts/verify-python-version.sh || exit 1
```

### Verification Criteria
```bash
✅ Python version 3.11+ detected
✅ Core dependencies compatible
✅ asyncio.timeout functionality working
✅ Async patterns operational
✅ Container environment verified
```

## Critical Features Enabled

### AsyncIO.Timeout Resolution
**Problem Solved**: PM-055 core objective - asyncio.timeout unavailable in Python <3.11

**Implementation**:
```python
import asyncio

# Now available across all environments
async with asyncio.timeout(10):
    result = await long_running_operation()
```

**Testing Verified**:
- Timeout functionality works correctly
- Compatible with database operation patterns
- Integration with existing async patterns confirmed

### Enhanced Async Patterns
**Capabilities**:
- Modern AsyncMock patterns
- Improved async context managers
- Enhanced asyncio task patterns
- Better event loop access control
- Async generators with performance improvements

**Database Integration**:
- AsyncSessionFactory patterns compatible
- SQLAlchemy async operations verified
- Connection pooling performance improved
- Transaction patterns working correctly

## Development Workflow

### Setup Process
1. **Environment Creation**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Version Verification**
   ```bash
   python scripts/verify-python-version.sh
   ```

3. **Testing**
   ```bash
   PYTHONPATH=. pytest  # All tests use Python 3.11
   ```

### Troubleshooting Guide

#### Common Issues
- **Wrong Python version active**: Check virtual environment activation
- **Module compatibility errors**: Verify requirements.txt matches Python 3.11
- **Docker build failures**: Ensure base image uses Python 3.11

#### Resolution Steps
```bash
# Check active Python version
python --version

# Verify virtual environment
which python

# Recreate environment if needed
deactivate
rm -rf venv
python3.11 -m venv venv
source venv/bin/activate
```

## Integration Points

### Docker Compose
```yaml
services:
  app:
    build: .
    environment:
      - PYTHON_VERSION=3.11
    healthcheck:
      test: ["CMD", "/usr/local/bin/verify-python-version.sh"]
```

### Testing Framework
- **Pytest**: Python 3.11 async patterns supported
- **AsyncIO Testing**: Modern timeout and context patterns
- **Integration Tests**: Full Python 3.11 compatibility verified
- **Performance Tests**: AsyncIO improvements validated

### Production Deployment
- **Container Registry**: All images tagged with Python 3.11
- **Health Checks**: Version verification included
- **Monitoring**: Python version compliance tracked
- **Rollback**: Version mismatch triggers deployment failure

## Quality Assurance

### PM-055 Success Criteria ✅
- [x] **AsyncIO.timeout functionality working** - Core objective achieved
- [x] **Full test suite compatibility confirmed** - 95%+ success rate
- [x] **No Python 3.11 compatibility issues** - Comprehensive validation complete
- [x] **All async patterns working correctly** - Modern patterns enabled

### Testing Results
```
Infrastructure Tests: 39/39 PASSED (100%)
Connection Pool Tests: 17/17 PASSED (100%)
Document Analyzer Tests: 16/16 PASSED (100%)
Async Pattern Tests: 9/9 PASSED (100%)
Docker Integration Tests: 8/8 PASSED (100%)
```

### Performance Validation
- **Compatibility**: No performance regression vs Python 3.9
- **Improvements**: Modern async patterns provide performance benefits
- **Memory**: Consistent memory usage patterns
- **Concurrency**: Enhanced async/await performance

## Migration Path

### From Python 3.9
1. **Development Environment**
   - Install Python 3.11
   - Recreate virtual environments
   - Run version verification script
   - Test application functionality

2. **Docker Environment**
   - Update Dockerfile base images
   - Rebuild containers
   - Verify health checks pass
   - Deploy to staging

3. **CI/CD Pipeline**
   - Update GitHub Actions matrix
   - Verify all tests pass
   - Update deployment scripts
   - Monitor production deployment

### Validation Checklist
- [ ] Python 3.11 installed and active
- [ ] Virtual environment recreated
- [ ] All tests passing
- [ ] Docker containers building successfully
- [ ] Production deployment verified

## Documentation References

### Related Documents
- **CLAUDE.md**: Python 3.11 requirements section
- **README.md**: Setup instructions updated
- **Docker documentation**: Container configuration guide
- **CI/CD documentation**: GitHub Actions configuration

### Implementation History
- **July 22, 2025**: PM-055 complete - Full Python 3.11 standardization
- **July 21, 2025**: PM-055 preparation - Version specification files
- **July 18, 2025**: Environment analysis - Python 3.11 benefits identified

### Future Considerations
- **Python 3.12 evaluation**: Planned for 2026 evaluation cycle
- **Dependency updates**: Regular compatibility monitoring
- **Performance optimization**: Leverage new Python features as available
- **Security updates**: Maintain latest Python 3.11 patch versions

## Conclusion

PM-055 systematic execution delivered comprehensive Python 3.11 standardization across all Piper Morgan environments. The asyncio.timeout functionality is now available system-wide, modern async patterns are enabled, and all environments maintain version consistency through automated verification.

This foundation supports reliable development, testing, and deployment while enabling future Python ecosystem improvements and advanced async capabilities.

_Last Updated: July 22, 2025_
