# #921 Findings — Pause at clean checkpoint

**Date**: 2026-05-10 ~18:00 PT
**Status**: PAUSED at Phase 2 complete; Phase 3 (test sweep) partial; **not merged to main**
**Branch**: `claude/921-fastapi-upgrade` at commit `25312d2d` (pushed)

---

## What's done

### Phase 1 — dependency upgrade ✅ shipped on branch

`requirements.txt` updated. Conservative pin:
- `fastapi==0.115.14` (was 0.104.1; +32 minor versions, same starlette family)
- `starlette==>=0.40,<0.50` (resolves to 0.46.2; was pinned 0.27.0)
- `httpx>=0.28.1` (was pinned <0.28; #920 stopgap removed)
- `sse-starlette>=2.2,<3.0` (resolves to 2.4.1; was pinned 2.1.3)

`pip install -r requirements.txt` clean. Server boots fully (all lifespan phases initialize: auth, attention decay, ethics audit cleanup, composting scheduler). App imports clean.

### Phase 2 — mechanical migrations ✅ shipped on branch

6 `AsyncClient(app=app)` sites migrated to `httpx.AsyncClient(transport=httpx.ASGITransport(app=app), ...)` pattern. `ASGITransport` import added to `tests/integration/conftest.py`. Sites:
- `tests/unit/services/database/test_conversation_lifecycle.py:511,535,549,563`
- `tests/auth/test_auth_endpoints.py:504`
- `tests/integration/conftest.py:134`

### Phase 3 — test sweep partial

**Subset comparison done early** (auth + security + intent_wiring + conversation_lifecycle + unit/security + setup_wizard + fresh_install):
- Main pre-#921: 36 failed + 17 errors + 207 passed = 53 non-passing
- Branch post-#921: 39 failed + 4 errors + 217 passed = 43 non-passing
- **Net: −10 non-passing, +10 PASS on the relevant subset**
- The "+3 failures" were ERROR→FAILED transitions where AsyncClient(app=) sites couldn't even run on main; now they run and reveal pre-existing test fixtures using `json=` instead of `Form()` (8 auth-endpoint tests). Filed as **#1073** — not caused by upgrade.

**Full-suite sweep** (entire test tree):
- Branch post-#921: hit `--maxfail=500` after 37 min. 227 failed + 273 errors + 929 passed reported.
- Main baseline attempted but shell wrapper ate the output; could not capture summary.

## What's NOT done

- Clean full-suite baseline on main pre-#921 (needs ~37 min re-run with proper output capture)
- Diff of branch failures vs main baseline failures
- Identification of which (if any) of the 500 truncated fail+error events are TRUE regressions vs pre-existing
- Merge to main

## Honest read

The subset comparison strongly suggests the upgrade is fundamentally correct:
- Production code unchanged (Phase 1+2 was dep pins + test-fixture mechanical migration only)
- Server starts and imports cleanly
- The targeted test files that the issue body said would need migration are working better post-upgrade
- 8 newly-revealed test failures are pre-existing fixture bugs unrelated to FastAPI/Starlette

The full-suite 500-surface includes a substantial baseline of pre-existing fails on main (yesterday's M2f Group A+B work confirmed ~16-20 pre-existing DB-fixture pattern issues in the security suites alone). The full-suite picture is unclear without a clean diff, but directional evidence says the upgrade isn't broadly regressing.

That said: **cannot responsibly merge without verifying the full-suite diff.**

## Next-session pickup plan

1. Run `pytest --tb=no -v --no-header > /tmp/main-baseline.txt 2>&1` on main (37 min)
2. Run same on `claude/921-fastapi-upgrade` (37 min)
3. Diff with `comm` or similar tool to identify TRUE regressions vs pre-existing
4. If TRUE regressions < 10: fix and merge
5. If TRUE regressions > 10: surface findings + decision (push through or revert + reframe)
6. If clean: merge `claude/921-fastapi-upgrade` to main; close #921

Estimated next-session work: 1.5-2 hours assuming clean comparison + a small number of real regressions.

## STOP rationale for pausing now

Per yesterday's gameplan STOP conditions:
> "If at the 4-hour mark we're not converging on green tests, that's a STOP signal."

Today's reality: started ~11:45, now ~18:00. **6+ hours elapsed**, much of it lost to monitor-pattern-mismatch where I went idle waiting for events that never fired (acknowledged to PM at 17:55). Recovery + clean-baseline-attempt would require another 1.5-2 hours pushing the day past 8pm. Not the right shape.

The pause point IS clean:
- Phase 1+2 committed + pushed (`25312d2d`)
- Phase 0 audit memo (`dev/2026/05/09/921-issue-audit.md`)
- Gameplan (`dev/2026/05/10/921-gameplan.md`)
- This findings-pause memo (this doc)
- #1073 filed for the discovered stale auth tests
- Branch not merged; main unchanged from yesterday's state

No state is at risk. Next session picks up with clear next-steps.

## Honest call-out

The 6-hour spin was a workflow failure on my part:
- Monitor pattern grepping for `passed|failed|...` didn't match pytest's `-q` summary line shape
- After "Standing by" message at ~12:00, I had nothing pulling me back to check output
- Should have polled the output file every 5-10 min or used `run_in_background` on the pytest itself with a `wait`-style follow-up
- PM checked in at ~17:55 noting I was spinning; that was the only thing that broke the loop

Worth a methodology pattern entry? Possibly — "Monitor pattern must match all process exit signals, not just expected output formats." For now, captured here.

— Lead Developer, 2026-05-10 ~18:00 PT
