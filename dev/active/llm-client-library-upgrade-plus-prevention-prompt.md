# LLM Client Library Upgrade + Prevention System

**Date**: October 12, 2025, 10:50 AM  
**Agent**: Code Agent  
**Epic**: CORE-CRAFT-GAP-2  
**Task**: Upgrade LLM libraries AND add prevention system

---

## Mission

**Primary**: Upgrade LLM client libraries to fix 49 failing tests

**Secondary**: Add prevention system so we never fall 2 years behind again

**PM Quote**: "Future us will thank now us!"

---

## Part 1: Library Upgrade (30 min)

### Step 1: Upgrade Libraries (5 min)

```bash
# Upgrade both libraries to latest
pip install --upgrade anthropic openai

# Verify versions
pip list | grep -E "anthropic|openai"
```

### Step 2: Update Requirements (5 min)

**Files to Update**:
- `requirements.txt`
- `pyproject.toml` (if exists)

**Update to**:
```txt
anthropic>=0.34.0
openai>=1.50.0
```

### Step 3: Test the Fix (20 min)

```bash
# Direct Interface tests (should go 6/14 → 14/14)
pytest tests/intent/test_direct_interface.py -v

# Contract tests (should go 29/70 → 70/70)
pytest tests/intent/contracts/ -v

# Full suite (should be 143/143)
pytest tests/intent/ -v
```

---

## Part 2: Prevention System (45 min)

### Task 1: Version Enforcement Test (20 min)

**Create**: `tests/integration/test_library_versions.py`

```python
"""
Test to ensure critical dependencies stay reasonably current.

This test will FAIL if libraries fall too far behind, forcing updates
during development rather than discovering stale dependencies months later.

Philosophy: "Future us will thank now us!" - PM, October 12, 2025
"""
import pytest


def test_anthropic_version_current():
    """Ensure Anthropic SDK is reasonably current.
    
    Anthropic releases major versions ~quarterly. This test ensures
    we're not more than 2 major versions behind.
    
    Update MIN_VERSION when new major versions release.
    """
    import anthropic
    
    current_version = tuple(map(int, anthropic.__version__.split('.')[:2]))
    MIN_VERSION = (0, 30)  # Update quarterly as needed
    
    assert current_version >= MIN_VERSION, (
        f"Anthropic {anthropic.__version__} is too old. "
        f"Minimum version: {MIN_VERSION[0]}.{MIN_VERSION[1]}.0. "
        f"Run: pip install --upgrade anthropic"
    )


def test_openai_version_current():
    """Ensure OpenAI SDK is reasonably current.
    
    OpenAI releases major versions ~quarterly. This test ensures
    we're not more than 2 minor versions behind.
    
    Update MIN_VERSION when new major versions release.
    """
    import openai
    
    current_version = tuple(map(int, openai.__version__.split('.')[:2]))
    MIN_VERSION = (1, 40)  # Update quarterly as needed
    
    assert current_version >= MIN_VERSION, (
        f"OpenAI {openai.__version__} is too old. "
        f"Minimum version: {MIN_VERSION[0]}.{MIN_VERSION[1]}.0. "
        f"Run: pip install --upgrade openai"
    )


def test_fastapi_version_current():
    """Ensure FastAPI is reasonably current.
    
    FastAPI is our web framework. Keep it current for security and features.
    """
    import fastapi
    
    current_version = tuple(map(int, fastapi.__version__.split('.')[:2]))
    MIN_VERSION = (0, 100)  # Update when major versions release
    
    assert current_version >= MIN_VERSION, (
        f"FastAPI {fastapi.__version__} is too old. "
        f"Minimum version: {MIN_VERSION[0]}.{MIN_VERSION[1]}.0. "
        f"Run: pip install --upgrade fastapi"
    )


def test_pydantic_version_current():
    """Ensure Pydantic v2 is being used.
    
    Pydantic v2 has major performance improvements and is required
    for modern FastAPI.
    """
    import pydantic
    
    major_version = int(pydantic.__version__.split('.')[0])
    
    assert major_version >= 2, (
        f"Pydantic {pydantic.__version__} is too old. "
        f"Must use Pydantic v2+. "
        f"Run: pip install --upgrade 'pydantic>=2.0'"
    )


@pytest.mark.parametrize("library,min_version", [
    ("anthropic", (0, 30)),
    ("openai", (1, 40)),
    ("fastapi", (0, 100)),
])
def test_critical_dependencies_current(library, min_version):
    """Unified test for all critical dependencies.
    
    This test fails fast if any critical dependency is too old,
    preventing the 2-year staleness that caused GAP-2 LLM issues.
    """
    try:
        module = __import__(library)
        current_version = tuple(map(int, module.__version__.split('.')[:2]))
        
        assert current_version >= min_version, (
            f"{library} {module.__version__} is too old (min: {min_version})"
        )
    except (ImportError, AttributeError) as e:
        pytest.fail(f"Could not check {library} version: {e}")


# Maintenance reminder test
def test_dependency_health_maintenance_reminder():
    """Reminder to review dependency health monthly.
    
    This test always passes but serves as a reminder in test output
    to check dependency health monthly.
    
    See: docs/process/dependency-health-checklist.md
    """
    import datetime
    current_month = datetime.datetime.now().strftime("%B %Y")
    
    # This test always passes, it's just a reminder
    assert True, f"Monthly reminder ({current_month}): Review dependency health!"
```

**Add to test suite**:
```bash
# Verify test works
pytest tests/integration/test_library_versions.py -v

# Should see 5-7 tests pass
```

---

### Task 2: Dependabot Configuration (10 min)

**Create**: `.github/dependabot.yml`

```yaml
# Dependabot configuration for automated dependency updates
# Enabled: October 12, 2025 (GAP-2)
# Purpose: Prevent 2-year library staleness (anthropic 0.7.0 → 0.34+)

version: 2
updates:
  # Python dependencies
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "09:00"
    open-pull-requests-limit: 10
    reviewers:
      - "xianminx"  # Adjust to your GitHub username
    assignees:
      - "xianminx"
    commit-message:
      prefix: "deps"
      include: "scope"
    labels:
      - "dependencies"
      - "automated"
    
    # Group minor/patch updates
    groups:
      production-dependencies:
        patterns:
          - "anthropic"
          - "openai"
          - "fastapi"
          - "pydantic"
        update-types:
          - "minor"
          - "patch"
      
      development-dependencies:
        patterns:
          - "pytest*"
          - "black"
          - "ruff"
          - "mypy"
        update-types:
          - "minor"
          - "patch"
    
    # Security updates get individual PRs
    allow:
      - dependency-type: "direct"
      - dependency-type: "indirect"
    
    # Ignore specific updates if needed
    ignore:
      # Example: Pin specific versions if needed
      # - dependency-name: "library-name"
      #   versions: ["x.x.x"]
```

**Verify configuration**:
```bash
# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('.github/dependabot.yml'))"

# Commit
git add .github/dependabot.yml
git commit -m "ci: Add Dependabot for automated dependency updates

- Weekly dependency scanning (Mondays, 9 AM)
- Grouped updates for related dependencies
- Auto-assign to maintainer
- Prevents 2-year staleness (GAP-2 lesson)
"
```

---

### Task 3: Monthly Health Check Script (15 min)

**Create**: `scripts/check_dependency_health.py`

```python
#!/usr/bin/env python3
"""
Check dependency health - run monthly or in CI/CD.

Usage:
    python scripts/check_dependency_health.py
    
Exit codes:
    0 - All dependencies healthy
    1 - Critical dependencies outdated
    2 - Script error
"""
import json
import subprocess
import sys
from datetime import datetime


CRITICAL_DEPS = {
    'anthropic': {'major_lag': 0, 'minor_lag': 5},  # Max 5 minor versions behind
    'openai': {'major_lag': 0, 'minor_lag': 10},    # Max 10 minor versions behind
    'fastapi': {'major_lag': 0, 'minor_lag': 10},
    'pydantic': {'major_lag': 0, 'minor_lag': 5},
}


def get_outdated_packages():
    """Get list of outdated packages from pip."""
    try:
        result = subprocess.run(
            ["pip", "list", "--outdated", "--format=json"],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running pip: {e}")
        sys.exit(2)
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing pip output: {e}")
        sys.exit(2)


def parse_version(version_str):
    """Parse version string to tuple of ints."""
    return tuple(map(int, version_str.split('.')[:3]))


def check_critical_deps(outdated_packages):
    """Check if critical dependencies are too far behind."""
    critical_issues = []
    
    for pkg in outdated_packages:
        if pkg['name'] not in CRITICAL_DEPS:
            continue
        
        current = parse_version(pkg['version'])
        latest = parse_version(pkg['latest_version'])
        limits = CRITICAL_DEPS[pkg['name']]
        
        major_lag = latest[0] - current[0]
        minor_lag = latest[1] - current[1] if latest[0] == current[0] else 999
        
        if major_lag > limits['major_lag']:
            critical_issues.append({
                'name': pkg['name'],
                'current': pkg['version'],
                'latest': pkg['latest_version'],
                'issue': f'{major_lag} major versions behind (max: {limits["major_lag"]})'
            })
        elif minor_lag > limits['minor_lag']:
            critical_issues.append({
                'name': pkg['name'],
                'current': pkg['version'],
                'latest': pkg['latest_version'],
                'issue': f'{minor_lag} minor versions behind (max: {limits["minor_lag"]})'
            })
    
    return critical_issues


def main():
    """Main health check routine."""
    print(f"🔍 Dependency Health Check - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print()
    
    outdated = get_outdated_packages()
    
    if not outdated:
        print("✅ All dependencies up to date!")
        return 0
    
    print(f"📦 Found {len(outdated)} outdated packages")
    print()
    
    critical_issues = check_critical_deps(outdated)
    
    if critical_issues:
        print("❌ CRITICAL: Core dependencies too far behind!")
        print()
        for issue in critical_issues:
            print(f"  {issue['name']}: {issue['current']} → {issue['latest']}")
            print(f"    Issue: {issue['issue']}")
        print()
        print("Run: pip install --upgrade " + " ".join(i['name'] for i in critical_issues))
        return 1
    
    # Show non-critical outdated packages
    non_critical = [p for p in outdated if p['name'] not in CRITICAL_DEPS]
    if non_critical:
        print("ℹ️  Non-critical dependencies outdated:")
        for pkg in non_critical[:10]:  # Show first 10
            print(f"  {pkg['name']}: {pkg['version']} → {pkg['latest_version']}")
        if len(non_critical) > 10:
            print(f"  ... and {len(non_critical) - 10} more")
    
    print()
    print("✅ Critical dependencies healthy")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

**Make executable and test**:
```bash
chmod +x scripts/check_dependency_health.py

# Test it
python scripts/check_dependency_health.py

# Should show: ✅ Critical dependencies healthy
```

---

## Part 3: Final Validation (10 min)

### Complete Test Suite

```bash
# Run ALL tests to verify no regression
pytest tests/ -v --tb=short

# Specifically verify:
# 1. 143/143 intent tests passing
# 2. Library version tests passing
# 3. No new failures introduced
```

### Documentation Update

**Update GAP-2 outline** with prevention system:
- Version enforcement tests added
- Dependabot enabled
- Health check script created

---

## Success Criteria

**Library Upgrade**:
- [ ] anthropic upgraded to 0.34+
- [ ] openai upgraded to 1.50+
- [ ] Requirements files updated
- [ ] 14/14 Direct Interface tests passing
- [ ] 70/70 Contract tests passing
- [ ] 143/143 total tests passing (100%)

**Prevention System**:
- [ ] `tests/integration/test_library_versions.py` created
- [ ] Version tests passing
- [ ] `.github/dependabot.yml` created
- [ ] `scripts/check_dependency_health.py` created
- [ ] Health check script tested
- [ ] All changes committed

---

## Deliverables

**Code Changes**:
1. `requirements.txt` - Updated library versions
2. `tests/integration/test_library_versions.py` - Version enforcement
3. `.github/dependabot.yml` - Automated dependency updates
4. `scripts/check_dependency_health.py` - Monthly health check

**Documentation**:
- `dev/2025/10/12/llm-client-library-upgrade.md` - Full report
- Updated GAP-2 outline with prevention additions

---

## Expected Duration (For PM Planning Only)

**Total**: ~1.5 hours
- Part 1 (Upgrade): 30 min
- Part 2 (Prevention): 45 min
- Part 3 (Validation): 15 min

**Important**: Quality over speed - verify completely

---

## Progress Milestones

**Report to PM after**:
- Part 1 complete (libraries upgraded, tests passing)
- Part 2 complete (prevention system added)
- Part 3 complete (full validation done)

---

## Notes

### Philosophy

**"Future us will thank now us!"** - PM, October 12, 2025

This prevention system ensures we never repeat the 2-year library staleness that caused:
- 49 test failures
- 2 hours of investigation
- Claimed "100% coverage" with 34% reality

### What We're Preventing

**2-year staleness pattern**:
- anthropic 0.7.0 → 0.34+ (2 years behind)
- openai 0.28.0 → 1.50+ (18 months behind)
- Code using modern APIs with ancient libraries
- Tests created but never validated

**Never again!** 🛡️

---

**Updated Prompt Created**: October 12, 2025, 10:50 AM  
**Agent**: Code Agent authorized to proceed  
**Goal**: 143/143 tests + prevention system  
**Next**: GAP-2 Phase 2 (Evidence Collection) after complete
