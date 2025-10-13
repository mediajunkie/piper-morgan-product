# Implementation Prompt: Fix Slack Asyncio Initialization Bug

**Issue**: #141 - INFR-DATA-BUG
**Agent**: Cursor Agent
**Estimated Time**: 1 hour
**Date**: October 9, 2025

---

## Context

Test suite fails during collection with asyncio event loop error. The Slack integration creates asyncio locks at import time rather than runtime, causing the error:

```
RuntimeError: There is no current event loop in thread 'MainThread'.
```

**Error Location**:
- `main.py:157` → `SlackWebhookRouter()`
- `SlackSpatialAdapter.__init__()` → `asyncio.Lock()`

---

## Root Cause

From issue description:
```python
# services/integrations/slack/spatial_adapter.py:35
def __init__(self):
    super().__init__("slack")
    self._lock = asyncio.Lock()  # ❌ Requires active event loop
```

---

## Task

Fix asyncio resource initialization by moving to lazy initialization pattern.

### Primary Change

**File**: `services/integrations/slack/spatial_adapter.py`

**Current Code** (around line 35):
```python
def __init__(self):
    super().__init__("slack")
    self._lock = asyncio.Lock()  # Create at init
```

**New Code**:
```python
def __init__(self):
    super().__init__("slack")
    self._lock = None  # Initialize as None

@property
def lock(self):
    """Lazy-initialize asyncio lock when first accessed."""
    if self._lock is None:
        self._lock = asyncio.Lock()
    return self._lock
```

### Additional Changes

1. **Update all references** to `self._lock` → `self.lock` (property access)
2. **Check for other asyncio resources** created at import time:
   - Look for other `asyncio.Lock()`, `asyncio.Queue()`, `asyncio.Event()` in `__init__`
   - Apply same lazy initialization pattern if found
3. **Search entire codebase** for similar patterns:
   - Other integrations that might have same issue
   - Other adapters creating asyncio resources at init

---

## Validation Steps

### Step 1: Test Collection
```bash
# Should no longer fail on import
PYTHONPATH=. python -m pytest --collect-only
# Expected: All tests collected successfully
```

### Step 2: Run Slack Tests
```bash
# Run Slack integration tests
PYTHONPATH=. python -m pytest tests/integration/test_slack_* -v
# Expected: Tests run (may have other failures, but not import errors)
```

### Step 3: Verify Functionality
```bash
# Start server and verify Slack integration loads
PYTHONPATH=. python main.py
# Expected: Server starts, Slack integration initializes without errors
```

---

## Acceptance Criteria

- [ ] Test suite runs without asyncio import errors
- [ ] All `self._lock` references updated to `self.lock`
- [ ] Slack integration maintains full functionality
- [ ] Pattern applied to any other asyncio resources in the file
- [ ] Similar patterns fixed elsewhere in codebase (if found)
- [ ] Tests pass collection phase
- [ ] CI/CD pipeline can execute tests successfully

---

## STOP Conditions

- If lazy initialization breaks Slack functionality
- If there are architectural reasons asyncio resources must be created at init
- If similar patterns exist but require different solutions
- If fixing this reveals deeper integration issues

---

## Notes

- **Priority**: HIGH - This blocks testing and development workflow
- **Production Impact**: Unknown if this affects production (needs verification)
- **Pattern**: This is a common asyncio antipattern - good to fix systematically
- **Documentation**: Consider adding guidelines about asyncio resource initialization

---

## Success Validation

After implementation:
```bash
# Full test suite should collect and run
PYTHONPATH=. python -m pytest tests/ -v --tb=short

# Specifically verify Slack tests
PYTHONPATH=. python -m pytest tests/integration/test_slack_* -v

# Check for any remaining asyncio warnings
PYTHONPATH=. python -m pytest tests/ -v 2>&1 | grep -i "event loop"
```

---

**Ready for Cursor Agent implementation.**
