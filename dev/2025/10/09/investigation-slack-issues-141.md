# Phase -1 Investigation: Slack Integration Issues

**Issue**: #141 - INFR-DATA-BUG
**Agent**: Cursor Agent
**Task Type**: Investigation (No modifications)
**Date**: October 9, 2025, 9:47 AM

---

## Mission

Determine which Slack integration issues actually exist and how they interact before implementing fixes.

---

## Background

Two potential issues identified:

### Issue A: Asyncio Event Loop (from #141)
```
RuntimeError: There is no current event loop in thread 'MainThread'.
Location: main.py:157 → SlackWebhookRouter() → SlackSpatialAdapter.__init__()
Cause: asyncio.Lock() created at import time
```

### Issue B: Signature Mismatch (from Phase 0 testing)
```
TypeError: __init__() got an unexpected keyword argument 'spatial_adapter'
Location: tests/integration/test_slack_e2e_pipeline.py line 165
Cause: Test fixture passing argument that router doesn't accept
```

**Questions:**
1. Does Issue A still exist?
2. Does Issue B exist independently or is it caused by Issue A?
3. Do both exist and interact?
4. Is there a third issue we haven't discovered?

---

## Investigation Steps

### Step 1: Check Current Import Behavior
```bash
# Can we import the Slack integration without errors?
python3 -c "from services.integrations.slack.spatial_adapter import SlackSpatialAdapter"
# Document: Does this work? Any errors?
```

### Step 2: Examine SlackSpatialAdapter
**File**: `services/integrations/slack/spatial_adapter.py`

Find and document:
1. The `__init__` method - does it create asyncio resources?
2. Line number where asyncio.Lock() or similar is called
3. Any other asyncio resources created at init time
4. Current state vs Issue #141 description

### Step 3: Examine SlackWebhookRouter
**File**: Check where SlackWebhookRouter is defined (likely in services/integrations/slack/)

Find and document:
1. The `__init__` signature - what parameters does it accept?
2. Does it accept `spatial_adapter` parameter?
3. What parameters DOES it accept?
4. Line numbers for reference

### Step 4: Examine Test Fixture
**File**: `tests/integration/test_slack_e2e_pipeline.py`

Look at line 165 (the failing fixture):
1. What parameters is it passing to SlackWebhookRouter?
2. Show the exact fixture code
3. What was the intended purpose of `spatial_adapter` parameter?
4. Is this a test bug or an API change?

### Step 5: Check Git History
```bash
# When was SlackWebhookRouter signature last changed?
git log -p --all -S "spatial_adapter" -- "services/integrations/slack/"

# When was the test fixture created/modified?
git log -p -- tests/integration/test_slack_e2e_pipeline.py
```

Document:
- Was `spatial_adapter` removed from router signature?
- Was test fixture created before or after signature change?
- Any relevant commit messages

### Step 6: Run Test Collection
```bash
# Does pytest collection fail?
PYTHONPATH=. python -m pytest tests/integration/test_slack_e2e_pipeline.py --collect-only
```

Document:
- Does collection succeed or fail?
- If fails, exact error and line number
- Is it the asyncio error or signature error?

### Step 7: Attempt Test Run
```bash
# Try to run the failing test
PYTHONPATH=. python -m pytest tests/integration/test_slack_e2e_pipeline.py::TestSlackE2EPipeline::test_complete_pipeline_flow_with_observability -v
```

Document:
- At what point does it fail (collection, setup, execution)?
- Exact error message
- Stack trace

---

## Deliverable: Investigation Report

Provide a clear report with:

### Section 1: Issue A Status (Asyncio Event Loop)
- **Exists**: Yes/No
- **Evidence**: Code snippets and line numbers
- **Severity**: Blocks import / Blocks tests / Not present

### Section 2: Issue B Status (Signature Mismatch)
- **Exists**: Yes/No
- **Evidence**: Code snippets showing signature vs usage
- **Root Cause**: Parameter removed / Test bug / Other
- **Severity**: Blocks tests / Minor / Not present

### Section 3: Interaction Analysis
- Do issues interact or are they independent?
- Which should be fixed first?
- Will fixing one reveal/hide the other?

### Section 4: Recommended Fix Order
Based on findings, recommend:
1. Fix A first, then B
2. Fix B first, then A
3. Fix both simultaneously
4. Only one needs fixing

Include reasoning for recommendation.

### Section 5: Additional Findings
- Any other Slack integration issues discovered
- Related code that might need attention
- Potential complications in fixes

---

## STOP Conditions

None - this is pure investigation. Document everything found, even if unclear.

---

## Output Format

Provide:
1. Clear answers to each investigation step
2. Code snippets with file paths and line numbers
3. Error messages (full text, not summarized)
4. Specific recommendations for fix approach

---

**Ready for Cursor Agent investigation.**
