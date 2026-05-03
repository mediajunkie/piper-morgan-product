# Gameplan: #714 MUX-LISTS-STALENESS-UI

**Issue**: https://github.com/mediajunkie/piper-morgan-product/issues/714
**Author**: Lead Developer (Claude Code Opus)
**Date**: 2026-05-03
**Template version**: gameplan-template v9.3
**Status**: Draft — pending audit-cascade against template + PM Phase -1 walkthrough
**Surfaces a Phase -1 STOP**: `/api/v1/lists` GET endpoint is a stub; see Phase -1 Q1.

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Lead Developer's Current Understanding

**Infrastructure Status** (from spike + this gameplan-prep read):

- [x] Web framework: **FastAPI**
- [x] Lists UI route: `GET /lists` returns `templates/lists.html` (`web/api/routes/ui.py:423`)
- [x] Lists template: `templates/lists.html` (~28KB; renders via JS calling `/api/v1/lists`)
- [x] **Lists API GET endpoint is a STUB** — `services/api/todo_management.py:644-678` returns mock `TodoListListResponse(lists=[], total_count=0, ...)` with three TODO comments:
  - "Implement list listing with UniversalListService"
  - "List universal Lists with item_type='todo'"
  - "Integrate with PM-040 Knowledge Graph"
- [x] `UniversalListService` resolves to `ItemService` (`services/api/todo_management.py:189-191`)
- [x] **Domain model `List`** (`services/domain/models.py:1250-1335`) carries `created_at` + `updated_at` already — staleness can compute from `updated_at` directly without schema changes
- [x] **`ListItem`** (`services/domain/models.py:1338-1369`) has `added_at` (membership creation) only, NOT `updated_at` — per-item-modification staleness is NOT trivially available; would require joining underlying Todo/Feature `updated_at`
- [x] DB model `ListItemDB` exists (`services/database/models.py:1494`)

**Lead Dev's understanding of the task** (with the Phase -1 STOP caveat):

#714 is scoped to "design staleness, then implement on Lists view." But the Lists view is currently rendering empty state always because the API is stubbed. Two options:

- **Option A**: file pre-work for "wire `/api/v1/lists` to actual ItemService" (parallel to #1034 carve-out for #704), then #714 stays scoped to "add staleness on top of working list listing"
- **Option B**: expand #714 to include both the Lists API wiring AND staleness — bigger issue, but they're conceptually paired (no point in staleness if lists don't list)
- **Option C**: discover that #714 work was always implicitly going to wire the listing (the issue body says "Lists view shows lists + list items" as current state, which the spike disproved)

**Recommended**: surface to PM. **My lean**: Option A (file pre-work) — parallels the #1034/#704 split + keeps #714's audit-passable scope (staleness design + implementation) intact.

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**

- [x] Multi-component (backend staleness logic + API change + frontend visual treatment)
- [x] Task duration >30 min — yes, ~3-4 hours estimated
- [ ] Multi-agent — no
- [ ] Exploratory/risky — moderate (depends on Phase 0 staleness-spec design pass)

**Assessment**: **USE WORKTREE** — multi-component change with rollback value. Branch: `claude/714-lists-staleness`.

### Part B: PM Verification Required

Questions for PM:

1. **STOP-flagged**: `/api/v1/lists` GET is a stub. How to handle?
   - **Option A** (lead): file pre-work issue "Wire /api/v1/lists to ItemService" first; #714 sits on top of working listing
   - **Option B**: expand #714 to cover both
   - **Option C**: confirm wiring is in flight elsewhere already and I missed it
   What does PM want?
2. **Staleness definition (Phase 0 design pass core question)**: simple "no updates in N days" using `List.updated_at`, OR richer signal incorporating ListItem activity (would require joining underlying item types — Todo/Feature/Bug — for their updated_at)? **My lean**: simple `List.updated_at` for MVP. Per-item activity is a Post-MVP enrichment.
3. **Threshold value of N**: 30 days? 90 days? Differ by `list_type` (personal vs shared vs project)? **My lean**: single default of 60 days for MVP; revisit after user observation. Specific thresholds are easy to tune later.
4. **Visual treatment**: subtle muted color? "Stale" badge? Icon? Combo? **My lean**: subtle muted card background + small "Last updated: 73 days ago" hint for stale lists. NOT a hard "STALE!" badge — that's punitive. The signal should be informational.
5. **Conceptual integrity language sweep**: per #714 issue's conceptual-integrity AC, no user-facing text uses "archived" / lifecycle phrasing. Confirm scope: this means the *staleness label* and *tooltip* never mention "archived"; "stale" / "old" / "untouched" / "last updated" are the OK vocabulary.

### Part C: Proceed/Revise Decision

- [ ] **PROCEED** — only after PM Q1 disposition (Option A, B, or C)
- [ ] **REVISE** — if PM picks Option B (expand scope), gameplan needs material restructure
- [ ] **CLARIFY** — Q1 is the STOP gate; rest are tunable

---

## Phase 0: Initial Bookending - GitHub Investigation

### Required Actions

1. **GitHub Issue Verification**: `gh issue view 714`

2. **Confirm Q1 disposition path**:
   - If Option A: verify pre-work issue exists + wait for it to merge
   - If Option B: integrate listing-wiring work into Phase 1
   - If Option C: locate the in-flight work

3. **Codebase Investigation** (for staleness design):
   ```bash
   # Inventory of List + ListItem updated_at usage
   grep -rn "List.updated_at\|list.updated_at" services/ | head

   # Verify ItemService has the listing query
   grep -n "def list\|def get_lists\|def find_lists" services/item_service.py

   # Verify lists.html JS render hooks for adding staleness
   grep -n "renderLists\|list.created_at\|list.updated_at" templates/lists.html

   # Decide where to compute staleness: backend (in API response) or frontend (from updated_at)?
   # Lean: backend, so server has authority on the threshold and policy
   ```

4. **Phase 0 staleness design pass deliverable**:
   - Working doc at `dev/2026/05/03/714-staleness-design-v0.md` capturing:
     - Definition: "stale = `now() - List.updated_at > THRESHOLD_DAYS`"
     - Threshold: 60 days (default; tunable)
     - Granularity: per-list only for MVP (per-item is Post-MVP)
     - Visual: muted card background + "Last updated N days ago" hint
     - Conceptual-integrity language sweep: vocabulary uses "stale" / "old" / "untouched" / "last updated"; never "archived" / lifecycle terms
   - Informal review by PM (and CXO if PM thinks signal warrants)

5. **Update GitHub Issue**:
   ```
   ## Status: Investigation Started
   - [ ] Phase -1 Q1 STOP resolved (lists API path)
   - [ ] Staleness design v0 documented
   - [ ] (optionally) CXO review on visual treatment
   ```

### STOP Conditions

- Phase -1 Q1 not resolved → block until resolved
- ItemService has no list-listing method (Q1 Option A reveals listing isn't viable yet) → escalate
- Staleness threshold disagreement at PM/CXO review → revise design before Phase 1

---

## Phase 0.5: Frontend-Backend Contract Verification

### Applicability assessment

**Applies** — adding a `staleness` field to the API response that the template consumes.

### Required Actions

1. **Document target API response shape**:
   ```json
   {
     "lists": [
       {
         "id": "...",
         "name": "Books to Read",
         "updated_at": "2025-12-15T10:00:00Z",
         "staleness": {
           "is_stale": true,
           "days_since_update": 138,
           "last_updated_human": "138 days ago"
         },
         ...
       }
     ]
   }
   ```

2. **Path verification** (server up, post-Q1-resolution):
   ```bash
   curl -s http://localhost:8001/api/v1/lists | jq '.lists[0] | keys'
   # Must include "staleness"
   ```

3. **Static-file verification**: no new static files; styling lives in `templates/lists.html` <style> block.

### STOP Conditions

- API path returns 404 or wrong shape → resolve before frontend work
- `staleness` not surfaced in response → backend bug

---

## Phase 0.6: Data Flow & Integration Verification

### Applicability assessment

**Applies** — multi-layer: ItemService → API endpoint → response → frontend render.

### Part A: Data Flow Requirements

| Layer | Needs change? | What changes |
|-------|---------------|--------------|
| Domain `List` model | No change | `updated_at` already exists |
| `ItemService.list_lists` (or equivalent — TBD Phase 0) | Maybe (per Q1) | Either already returns Lists with `updated_at`; OR pre-work issue addresses |
| Staleness computation | NEW | Pure function `compute_staleness(list, threshold_days=60) -> StalenessSignal`; or service-layer method |
| API endpoint `GET /api/v1/lists` | ✅ | Either (a) staleness computed in service + returned via response model, or (b) computed in route handler. Lean (a). |
| Pydantic response model | ✅ | `TodoListListResponse` carries `staleness` per item |
| `lists.html` render | ✅ | Reads `list.staleness`; applies class/CSS for muted treatment + "N days ago" hint |

### Part B: Integration Points Checklist

| Caller | Callee | Verification |
|--------|--------|--------------|
| `/api/v1/lists` route | `ItemService.list_lists` (TBD name) | Verify method exists + returns `List` objects with `updated_at` |
| `ItemService` | Staleness computation | New helper function or service method |
| Response builder | `staleness` payload | Pydantic model field |
| `lists.html` | `staleness` from response | Renders muted/badge per design |

### Part C: Pattern Adaptation Notes

This isn't following an existing pattern — staleness is a new concept. The visual-treatment pattern (muted card, "last updated N days ago" hint) might be reusable across other list-shaped surfaces (todos, projects) post-MVP.

**Potential pitfalls**:
1. **Threshold tuning rebuilds**: changing the threshold post-deploy is a config change, not a migration — but if we hardcode the threshold, swapping requires redeploy. Phase 1 should expose threshold via config (env var or config file).
2. **TimeZone**: `List.updated_at` may be naive datetime in some code paths. Verify TIMESTAMPTZ at the DB level (it should be per the Apr 16 fix to similar shape problems); compute staleness with timezone-aware datetime arithmetic.
3. **Caching**: if list listing is heavily called, recomputing staleness on every request is fine but should be considered for perf.

### STOP Conditions

- `List.updated_at` is naive datetime → fix timezone path before computing
- Threshold not configurable → don't ship hardcoded magic number; expose to config

---

## Phase 0.7: Conversation Design

### Applicability assessment

**Not applicable** — read-only display feature; no conversation flow.

### Per audit-cascade skill: PM approval needed

**Question for PM**: confirm Phase 0.7 inapplicability.

---

## Phase 0.8: Post-Completion Integration

### Applicability assessment

**Not applicable** — read-only feature; no user state changes; no DB writes.

### Per audit-cascade skill: PM approval needed

**Question for PM**: confirm Phase 0.8 inapplicability.

---

## Phases 1-N: Development Work

### Phase 1: Staleness backend (per Q2 simple definition + Q3 default 60 days)

**Work**:

- [ ] Helper function in `services/mux/` (or equivalent — TBD Phase 0): `compute_staleness(list_obj, threshold_days=60) -> StalenessSignal` returning `{is_stale: bool, days_since_update: int, last_updated_human: str}`
- [ ] Threshold sourced from config / env (`PIPER_LIST_STALENESS_DAYS`, default 60)
- [ ] Unit tests:
  - List updated yesterday → not stale, days_since_update=1, last_updated_human="yesterday"
  - List updated 100 days ago, threshold 60 → stale, days_since_update=100
  - List updated today → not stale, days_since_update=0, last_updated_human="today"
  - Edge: List with `updated_at` in the future (clock skew) → not stale, days_since_update=0

### Phase 2: API endpoint integration (per Q1 disposition)

**Work**:

- [ ] If Q1 Option A: confirm pre-work merged; thin wrap of staleness in the now-working endpoint
- [ ] If Q1 Option B: implement listing AND staleness here
- [ ] Update `TodoListListResponse` Pydantic model to include `staleness: StalenessResponse` per item
- [ ] Endpoint computes staleness for each list and returns

**Tests**:

- [ ] Endpoint integration test: GET returns `staleness` field
- [ ] Conceptual-integrity test: response field names use "stale" not "archived"

### Phase 3: Frontend integration

**Work**:

- [ ] Update `lists.html` `renderLists` (line 265) to read `list.staleness`
- [ ] Apply CSS class to stale list cards (`.resource-item.is-stale { background: var(--color-background-tertiary); opacity: 0.85; }` — TBD final treatment per Q4 design)
- [ ] Add `<div class="staleness-hint">Last updated ${list.staleness.last_updated_human}</div>` inside the card
- [ ] Conceptual-integrity sweep: no user-facing text uses "archived" / lifecycle terms (per Q5)

**Tests**:

- [ ] Template tests:
  - `test_stale_list_renders_muted`
  - `test_fresh_list_renders_normal`
  - `test_no_lifecycle_phrasing_in_user_facing_text` — assert "archived", "RATIFIED", etc. NOT in rendered HTML

### Phase 4: Manual verification

**Scenarios** (server up; need a real stale + fresh list — may require seeding test data):
1. **Stale list visible as muted**: list `updated_at = now() - 90 days` → muted background + "90 days ago" hint
2. **Fresh list normal**: list updated today → normal styling, no staleness hint OR "today" hint
3. **Threshold tuning**: change `PIPER_LIST_STALENESS_DAYS=30`; restart; verify the same 90-day list now shows AND a 45-day list also shows
4. **No regressions**: list editing/sharing/permissions still work as before
5. **Conceptual integrity**: no on-screen "archived" / "RATIFIED" / lifecycle-flavored text appears

### Phase 2a: Routing integration tests

**Not applicable** — no intent/classifier changes. **Question for PM**: confirm 2a inapplicability.

### Phase 2b: Wiring integration tests

**Applies** — multi-layer feature.

- [ ] Wiring test: ItemService.list_lists (or equiv) → endpoint → response carries `staleness` correctly per list
- [ ] Wiring test: real list with controlled `updated_at` (test fixture) flows through to frontend render via the API

---

## Phase Z: Final Bookending & Handoff

### Required Actions

1. **GitHub Final Update**:
   ```
   ## Status: Complete - Awaiting PM Approval
   - Staleness design v0 captured + reviewed (link)
   - Backend staleness computation
   - API exposes staleness per list
   - Lists view shows muted treatment + "last updated" hint for stale lists
   - Conceptual-integrity sweep complete: no lifecycle vocabulary in user-facing strings
   - Tests + manual scenarios pass
   ```

2. **Documentation**:
   - [ ] Phase-0 staleness design v0 cross-referenced from #714
   - [ ] Code comment in `lists.html` documenting muted-treatment rule + threshold-config-source

3. **Evidence Compilation**:
   - [ ] Test output (Phases 1-3 unit + integration)
   - [ ] Browser screenshots: stale list + fresh list
   - [ ] Files modified list

4. **Handoff**:
   - [ ] If staleness design is reusable for other surfaces, document the pattern for future issues

5. **Session log** complete

6. **PM Approval Request** standard

---

## Multi-Agent Coordination Plan

Single agent (Lead Dev). Multi-component but tightly coupled.

### Verification Gates

- [ ] Phase 1: backend computation tests pass
- [ ] Phase 2: endpoint tests pass
- [ ] Phase 3: template tests pass
- [ ] Phase 2b: wiring tests pass
- [ ] Phase 4: manual scenarios pass

---

## STOP Conditions

- Phase -1 Q1 unresolved
- `List.updated_at` timezone issues
- Threshold hardcoded (must be config-driven)
- Conceptual-integrity AC fails (any "archived" / lifecycle text in user-facing output)

---

## Evidence Requirements

- Test output
- Screenshots (stale + fresh)
- git diff
- Phase-0 design doc

---

## Effort Estimate

**Overall Size**: Medium (~3-4 hours, contingent on Q1 disposition)

| Phase | Estimate (Q1 Option A) | Estimate (Q1 Option B) |
|-------|------------------------|------------------------|
| Phase -1 PM walk | 20 min | 20 min |
| Phase 0 design pass | 45 min | 45 min |
| Phase 1 backend computation | 45 min | 45 min |
| Phase 2 API integration | 30 min | 1.5 hr (if includes listing wiring) |
| Phase 3 frontend | 45 min | 45 min |
| Phase 2b wiring | 30 min | 30 min |
| Phase 4 manual + 5 tests | 30 min | 30 min |
| Phase Z bookend | 15 min | 15 min |
| **Total** | **~3.5 hr** | **~5 hr** |

---

## Dependencies

- [x] Phase -1 spike completed
- [ ] PM Phase -1 walkthrough complete (esp. Q1 STOP-flagged item)
- [ ] (Q1 Option A only) Pre-work issue "Wire /api/v1/lists to ItemService" merged

## Blocks

- M2d gate completeness depends on this issue closing

---

# Audit-Cascade: Gameplan vs gameplan-template v9.3

## Audit Matrix

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| Phase -1: Infrastructure Verification | ✅ | Spike findings + extended; STOP surfaced (Q1 stub-endpoint finding) |
| Phase -1: Worktree Assessment | ✅ | USE WORKTREE — multi-component |
| Phase -1: PM Verification placeholder | ⚠️ | Five Qs queued; Q1 is STOP-gating |
| Phase 0: GitHub Issue Verification | ✅ | Step included |
| Phase 0: Codebase Investigation | ✅ | grep + verification commands |
| Phase 0: Staleness design pass deliverable | ✅ | Working doc + path included |
| Phase 0: Update GitHub Issue | ✅ | Status template |
| Phase 0: STOP Conditions | ✅ | Three named (Q1 + ItemService + threshold disagreement) |
| Phase 0.5: Applicability | ✅ | Applies (response shape change consumed by template) |
| Phase 0.5: API path documentation | ✅ | curl example included |
| Phase 0.5: Static-file verification | ✅ | No new static files documented |
| Phase 0.5: STOP Conditions | ✅ | Two named |
| Phase 0.6: Applicability | ✅ | Applies (multi-layer feature) |
| Phase 0.6: Data Flow Requirements | ✅ | Six-row layer table |
| Phase 0.6: Integration Points | ✅ | Caller→callee table |
| Phase 0.6: Pattern Adaptation Notes | ✅ | This is not following a pattern; pitfalls listed (timezone, threshold config, perf) |
| Phase 0.6: STOP Conditions | ✅ | Two named |
| Phase 0.7: Conversation Design | ⚠️ | Marked inapplicable; **PM approval requested** |
| Phase 0.8: Post-Completion Integration | ⚠️ | Marked inapplicable; **PM approval requested** |
| Phases 1-N: Development with progressive bookending | ✅ | Phases 1-4 + 2a + 2b defined |
| Phase 2a: Routing integration tests | ⚠️ | Marked N/A — not intent/classifier work; **PM approval requested** |
| Phase 2b: Wiring integration tests | ✅ | Two wiring tests specified |
| Phase Z: GitHub Final Update | ✅ | Template included |
| Phase Z: Documentation Updates | ✅ | Design doc + code comment |
| Phase Z: Evidence Compilation | ✅ | Tests + screenshots + diff + design doc |
| Phase Z: Handoff Preparation | ✅ | Reusable-pattern note |
| Phase Z: Session Completion | ✅ | Listed |
| Phase Z: PM Approval Request | ✅ | Template included |
| Multi-Agent Coordination Plan | ✅ | Single-agent justification |
| Verification Gates | ✅ | Listed per Phase |
| STOP Conditions (throughout) | ✅ | Section included |
| Evidence Requirements | ✅ | Listed |
| Effort Estimate | ✅ | Per-phase + Q1-disposition variants |
| Dependencies + Blocks | ✅ | Q1 disposition + spike + M2d-gate dependency |
| Test Scope | ✅ | Unit + integration + wiring + manual |

## Action Required Before Proceeding

1. **Phase -1 Q1 STOP-gated** (lists API path: file pre-work, expand scope, or PM redirects)
2. **Phase -1 Qs 2-5** (staleness definition, threshold, visual treatment, conceptual-integrity language)
3. **Phase 0.7 + 0.8 + 2a inapplicability confirmations** per audit-cascade skill

## Status

**Audit cascade gate: NOT YET PASSED.** Four ⚠️ items pending PM input + one STOP-gated item (Q1). No ❌ items.
