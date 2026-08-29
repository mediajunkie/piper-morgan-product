# CORE-UX-STATUS-USER: Status Checker Should Detect Current User

⚠️ **The Alpha fix is already shipped.** Flagged 2026-08-11 during weekly-docs-audit
#1583/#1585 — verified directly against `scripts/status_checker.py:79`, which already reads
`SELECT id, username FROM users ORDER BY created_at DESC LIMIT 1`, exactly the "Alpha Solution
(Quick Fix)" proposed below. The unchecked Acceptance Criteria checkboxes are stale, not
reflecting real state — this doc's Alpha scope is done; only the Beta scope (JWT detection,
`--user` flag) remains genuinely open, if still wanted.

**Sprint**: A7
**Priority**: Medium
**Effort**: 3 hours
**Impact**: Medium (confusing for new users)

## Problem

Status checker currently shows API key status for first user in database, not the user who just completed setup.

**Example** (from Issue #218 testing):
```
API Keys:
  ○ openai: Not configured
  ○ anthropic: Not configured
  ○ github: Not configured
```

But user "xian-alpha" just configured OpenAI and GitHub keys in setup wizard!

**Root cause**: Status checker queries `SELECT id, username FROM users LIMIT 1` which returns oldest user (warmth_user_0.3 from development), not the most recent user (xian-alpha from setup).

## Proposed Solution

**For Alpha** (single user assumption):
Show status for most recently created user (the one who just ran setup).

**For Beta** (multi-user):
- Detect current user from JWT token or environment
- Allow `--user` flag to specify user
- Show current user's username in output

## Implementation

### Alpha Solution (Quick Fix)

**File**: `scripts/status_checker.py`

Change query from:
```python
user_result = await session.execute(
    text("SELECT id, username FROM users LIMIT 1")
)
```

To:
```python
user_result = await session.execute(
    text("SELECT id, username FROM users ORDER BY created_at DESC LIMIT 1")
)
```

### Beta Solution (Full Implementation)

**Add user detection**:
```python
async def detect_current_user() -> Optional[str]:
    """
    Detect current user from:
    1. JWT token (if logged in)
    2. Environment variable USER_ID
    3. Most recent user (fallback)
    """
    # Check for JWT token
    # Check for USER_ID env var
    # Fallback to most recent
```

**Add --user flag**:
```python
if len(sys.argv) > 2 and sys.argv[1] == "status":
    if sys.argv[2].startswith("--user="):
        user_id = sys.argv[2].split("=")[1]
```

**Show username in output**:
```
==================================================
Piper Morgan System Status
User: xian-alpha
==================================================
```

## Acceptance Criteria

**Alpha** (Sprint A7):
- [ ] Status checker shows most recent user's API keys
- [ ] Setup wizard + status checker show consistent information
- [ ] Username displayed in status output

**Beta** (Future):
- [ ] Status checker detects JWT-authenticated user
- [ ] `--user=<username>` flag works
- [ ] Multiple users can check their own status

## User Impact

**Current behavior**: Confusing for new users who just configured keys
**Expected behavior**: Status reflects what user just configured

## Testing Plan

1. Run `python main.py setup` and configure OpenAI key
2. Run `python main.py status`
3. Verify status shows OpenAI as "Valid" (not "Not configured")
4. Verify username matches setup wizard username

## Related Issues

- #228 CORE-USERS-API (multi-user infrastructure)
- #218 CORE-USERS-ONBOARD (setup wizard)
