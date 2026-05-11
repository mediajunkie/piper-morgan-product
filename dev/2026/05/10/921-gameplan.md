# Gameplan: #921 — FastAPI/Starlette/httpx upgrade (conservative)

**Issue**: UPGRADE: FastAPI/Starlette/httpx to current versions
**PM Disposition (2026-05-10 11:40)**: Sunday calm-sprint slot; "#921 ahoy!" — proceed.
**Conservative target**: pin to `fastapi==0.115.x` (the original issue's target when it was filed) rather than latest `0.136`. Smaller blast radius; can file separate issue for further upgrade later if needed.
**Auditor**: Lead Developer
**Date**: 2026-05-10 ~11:45
**Phase**: 2 of 3 (Gameplan) — Phase 0 complete (`dev/2026/05/09/921-issue-audit.md`)
**Branch / worktree**: `claude/921-fastapi-upgrade` at `../piper-morgan-product-921`

---

## Phase -1: Infrastructure verification

**Work characteristics**: Dependency upgrade with mechanical migrations + test sweep + server smoke. Pre-release dev env. Phase 0.5/0.6/0.7/0.8 N/A (no UI design / data flow / conversation / completion side effects, same N/A pattern PM already approved for M2f Group A).

**Pre-flight**:
- ✅ Phase 0 audit complete
- ✅ #1072 already shipped (`regex=` → `pattern=` independent fix)
- ✅ Worktree-isolated; branch synced with main
- ✅ PM go-ahead 11:40 today

---

## Phase 1: Pin versions + resolve dependencies (~30 min)

### 1a. Update `requirements.txt`

```
# OLD
fastapi==0.104.1
starlette==0.27.0
httpx>=0.27.0,<0.28  # Pinned: ... See #921.

# NEW
fastapi==0.115.14   # Last of 0.115 series; conservative target per #921 disposition 2026-05-10
starlette==0.41.3   # Pinned by fastapi 0.115.x; lock to known-good version
httpx>=0.28.1       # Unpin; #921 closes #920's stopgap
```

(Will adjust pins after `pip install --dry-run` confirms exact compatible versions.)

### 1b. `pip install --dry-run` to verify resolution

If clean, proceed. If dependency conflicts surface, adjust pins. Document any forced upgrades for transitives.

### 1c. `pip install` actual

Once dry-run is clean.

---

## Phase 2: Mechanical migrations (~30 min)

### 2a. Migrate 6 `AsyncClient(app=)` calls to `ASGITransport(app=)` pattern

```python
# OLD
async with httpx.AsyncClient(app=app, base_url="http://test") as client:
    ...

# NEW
async with httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
    ...
```

Sites (per Phase 0 audit):
- `tests/unit/services/database/test_conversation_lifecycle.py:511, 535, 549, 563`
- `tests/auth/test_auth_endpoints.py:504`
- (1 additional surfaced by full grep)

Add `from httpx import ASGITransport` import where needed.

### 2b. `class Config` → `model_config = ConfigDict(...)` (3 sites; cosmetic; defer if mechanical migrations are clean)

Skip for v1 if not needed; file as cleanup follow-up.

---

## Phase 3: Smoke + test sweep (~1-2 hr)

### 3a. Server smoke

```bash
POSTGRES_PORT=5433 ./venv/bin/python main.py
# Hit /health and /api/v1/auth/login
```

Verify clean startup (no DeprecationWarnings from FastAPI; lifespan phases initialize).

### 3b. Auth + API + security suites

```bash
POSTGRES_PORT=5433 ./venv/bin/pytest --maxfail=100 \
  tests/auth/ tests/security/ tests/integration/test_intent_wiring_integration.py \
  tests/unit/services/database/test_conversation_lifecycle.py
```

Compare to pre-#921 baseline (yesterday's: 16 fails + 4 errors all pre-existing DB-fixture issues).

### 3c. Iterate on breakage

Fix anything new that's clearly attributable to the upgrade (deprecation, signature change, etc.). Document anything that requires deeper investigation as STOP-and-surface.

---

## Phase Z: Verification + handoff (~30 min)

- Run full test suite to characterize regression delta vs main pre-#921
- Update issue evidence comment
- Cross-reference #1072 (already shipped) and #920 (httpx pin removed)
- Sign-off check before close

---

## STOP Conditions

- **Architect-strategy question surfaces** (e.g., "should we go to 0.136 instead of 0.115?") → STOP, surface to PM, file findings
- **>10 NEW test failures** beyond pre-existing baseline → STOP, surface, decide whether to push or revert
- **Server fails to start cleanly** after dependency install → STOP, investigate, surface if not quickly resolvable
- **Starlette breaking change** that requires substantive code changes (middleware semantics, lifespan signature, etc.) → STOP, surface, may require Architect input

---

## Effort Estimate

**Total: ~3-4 hours conservative target**, with bounded escalation:
- Phase 1: 30 min
- Phase 2: 30 min
- Phase 3: 1-2 hr
- Phase Z: 30 min

If at the 4-hour mark we're not converging on green tests, that's a STOP signal.

---

## Audit-cascade self-check

Phase 0 audit done. Phase 0.5/0.6/0.7/0.8 N/A (PM precedent). Phase 1-3 + Z above. Effort + STOP conditions explicit.

Lead Dev solo work; no subagent for Phase 1+2 (mechanical migrations are tightly coupled to dep state). Possible subagent for Phase 3 test sweep if iteration becomes long.

— Lead Developer, 2026-05-10 ~11:45
