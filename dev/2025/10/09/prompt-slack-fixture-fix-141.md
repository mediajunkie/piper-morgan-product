# Implementation Prompt: Fix Slack Test Fixture Signature

**Issue**: #141 - INFR-DATA-BUG
**Agent**: Cursor Agent
**Estimated Time**: 15 minutes
**Date**: October 9, 2025, 10:30 AM

---

## Context from Phase -1 Investigation

**Finding**: The asyncio event loop issue described in #141 was already resolved (likely during Great Refactor). Only a simple test fixture signature mismatch remains.

**Current Error**:
```
TypeError: __init__() got an unexpected keyword argument 'spatial_adapter'
Location: tests/integration/test_slack_e2e_pipeline.py line 165
```

---

## Root Cause

Test fixture passes `spatial_adapter` parameter that doesn't exist in SlackWebhookRouter signature.

**SlackWebhookRouter Signature** (actual):
```python
def __init__(
    self,
    config_service: Optional[SlackConfigService] = None,
    oauth_handler: Optional[SlackOAuthHandler] = None,
    spatial_mapper: Optional[SlackSpatialMapper] = None,
    integration_router: Optional[SlackIntegrationRouter] = None,
    response_handler: Optional[SlackResponseHandler] = None,
):
```

**Test Fixture** (line 165 - incorrect):
```python
router = SlackWebhookRouter(
    config_service=config_service,
    oauth_handler=MagicMock(spec=SlackOAuthHandler),
    spatial_mapper=MagicMock(spec=SlackSpatialMapper),
    spatial_adapter=mock_spatial_adapter,  # ❌ This parameter doesn't exist
)
```

---

## Task

Fix the test fixture to match actual SlackWebhookRouter signature.

### Change Required

**File**: `tests/integration/test_slack_e2e_pipeline.py`
**Line**: 165

**Remove this line**:
```python
    spatial_adapter=mock_spatial_adapter,  # Delete this entire line
```

**Result should be**:
```python
router = SlackWebhookRouter(
    config_service=config_service,
    oauth_handler=MagicMock(spec=SlackOAuthHandler),
    spatial_mapper=MagicMock(spec=SlackSpatialMapper),
)
```

---

## Validation Steps

### Step 1: Test Collection
```bash
PYTHONPATH=. python -m pytest tests/integration/test_slack_e2e_pipeline.py --collect-only
# Expected: All tests collected successfully (no TypeError)
```

### Step 2: Run the Specific Test
```bash
PYTHONPATH=. python -m pytest tests/integration/test_slack_e2e_pipeline.py::TestSlackE2EPipeline::test_complete_pipeline_flow_with_observability -v
# Expected: Test runs (may fail for other reasons, but not signature error)
```

### Step 3: Run All Slack Tests
```bash
PYTHONPATH=. python -m pytest tests/integration/test_slack_* -v
# Expected: Tests run without signature errors
```

---

## Acceptance Criteria

- [ ] `spatial_adapter` parameter removed from test fixture
- [ ] Test collection succeeds (no TypeError)
- [ ] Slack tests can execute (may have other failures, but not signature errors)
- [ ] No other references to `spatial_adapter` parameter in Slack tests

---

## Additional Work

### Update Issue #141

Add comment to issue:
```
Investigation found that the asyncio event loop issue described in this issue
was already resolved (likely during Great Refactor).

The remaining issue was a simple test fixture signature mismatch where the
test was passing a `spatial_adapter` parameter that never existed in the
SlackWebhookRouter signature.

Fixed by removing the invalid parameter from the test fixture.

Time: 15 minutes (investigation + fix)
Status: Resolved
```

Close issue with label: `resolved-during-refactor`

---

## STOP Conditions

- If removing parameter causes test failures that suggest it was needed
- If there are other uses of `spatial_adapter` that need addressing
- If router signature is actually wrong and test is correct

---

## Success Validation

After implementation:
```bash
# All Slack tests should at least run (collection and setup should work)
PYTHONPATH=. python -m pytest tests/integration/test_slack_* -v --tb=short

# Specific test should not have TypeError
PYTHONPATH=. python -m pytest tests/integration/test_slack_e2e_pipeline.py::TestSlackE2EPipeline::test_complete_pipeline_flow_with_observability -v
```

---

**This is a simple one-line deletion. Should take ~15 minutes including validation.**
