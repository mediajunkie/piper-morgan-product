# Gameplan: #1031 MUX-INSIGHT-PASSIVE

**Issue**: https://github.com/mediajunkie/piper-morgan-product/issues/1031
**Author**: Lead Developer (Claude Code Opus)
**Date**: 2026-05-03
**Template version**: gameplan-template v9.3
**Status**: Draft — pending audit-cascade against template + PM Phase -1 walkthrough
**Blocked by**: #1035 MUX-COMPOSTING-ACTIVATION
**Scope-trim note**: Prior-art read on `templates/insights.html` (#424, closed Jan) showed page is **structurally complete**. This issue's work is "wire the existing page to a working backend" — substantially smaller than the issue body suggested.

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Lead Developer's Current Understanding

**Infrastructure Status — what's already done** (`templates/insights.html` 748 lines, structurally complete from #424):

- [x] UI route `GET /insights` renders `templates/insights.html` (`web/api/routes/ui.py:349`)
- [x] Topic filter tabs (5 categories: Work Patterns / Projects / Preferences / Relationships / Scheduling + All)
- [x] Insights grid with `<template id="insight-card-template">` carrying topic + confidence + expression + sources + date
- [x] All four spec affordances (Correct / Confirm / Why? / Delete) wired as buttons + custom-event dispatchers (`insight-correct`, `insight-confirm`, `insight-why`, `insight-delete`)
- [x] Reset-all (D2-compliant — requires typing "RESET")
- [x] Trust-gating mechanism via `data-min-stage="1"` + reads `window.trustStage` (defaults 1)
- [x] Empty + loading states
- [x] Confidence binning matches D3: ≥0.8 high, 0.6-0.8 medium, <0.6 "something to consider"
- [x] Date formatting (Today / Yesterday / N days ago)
- [x] Toast feedback strings match D2 ("That's gone." / "Starting fresh." / "Thanks for confirming!")

**Infrastructure Status — what's missing** (the actual work for #1031):

- [ ] Real backend insights API at `/api/v1/insights*` (currently the page has TODO comments at `templates/insights.html:455-457`):
  - `GET /api/v1/insights` — list user's insights with metadata
  - `POST /api/v1/insights/{id}/correct` — record correction
  - `POST /api/v1/insights/{id}/confirm` — record confirmation
  - `POST /api/v1/insights/{id}/why` — return source-inquiry response
  - `DELETE /api/v1/insights/{id}` — soft delete (or hard, per design)
  - `DELETE /api/v1/insights` — reset-all (per-user)
- [ ] Frontend wiring to replace the TODO with real `fetch()` calls
- [ ] Custom-event listeners in JS that wire `insight-correct` → POST endpoint, etc.
- [ ] `window.trustStage` plumbing — pass actual user trust stage from server-rendered context (currently defaults to 1)

**Lead Dev's understanding of the task** (post scope-trim):

This is a **wiring** issue. After #1035 lands (insight persistence), the work is:
1. Backend: 5-6 endpoints under `/api/v1/insights*` that delegate to `InsightRepository`
2. Frontend: replace the `TODO` and wire event handlers to fetch
3. Trust-stage plumbing
4. Minor design decisions (hard vs soft delete; correction flow shape)

The original issue body listed "Build the page; topic filter; affordances; trust gating" — all of which are already done. The remaining work is meaningful but smaller than originally scoped.

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**

- [x] Multi-component (5-6 endpoints + frontend wiring + trust-stage plumbing)
- [x] Task duration ~3-4 hours
- [ ] Multi-agent — no
- [ ] Exploratory — moderate; existing UI's expectations are clear contracts to honor

**Assessment**: **USE WORKTREE** — branch `claude/1031-insight-passive` based on #1035.

### Part B: PM Verification Required

Questions for PM:

1. **Delete semantics**: hard delete or soft delete? `templates/insights.html:679-685` removes the card from DOM with toast "Got it, that's gone." — implies hard. But for an audit/reflection-style system, soft (mark as user-deleted, hidden from view but preserved) may be safer. **My lean**: **soft delete** for MVP — adds an `is_deleted` field on `InsightDB`; `GET /api/v1/insights` excludes them; reset-all is a soft delete for all. Justification: insights are reflections, not user data per se; reversibility is gentle.
2. **Correction shape**: when user clicks "Correct," what's the input flow?
   - **Option A**: simple text input — user types their correction text; stored alongside insight as `user_correction`
   - **Option B**: structured "Wrong / partly wrong / context missing" — typed correction taxonomy
   - **Option C**: just mark `user_response = "corrected"` with no detail (the existing InsightJournal API)
   **My lean**: **Option A** for MVP — simplest user flow + most preservation of intent.
3. **"Why?" response**: when user clicks "Why?" on an insight, the response should cite source(s). `SurfaceableInsight` has `object_id` (the COMPOSTED object that produced it) and `learning.applies_to_entities` / `topic_tags`. What's the "Why?" endpoint return?
   - **Option A**: text response: "I noticed this from N observations across [object names if available]"
   - **Option B**: structured: `{source_count, source_objects: [...], confidence_basis: "..."}`
   **My lean**: **Option A** for chat consistency; structured-payload is unnecessary for a reflection surface.
4. **Trust-stage plumbing**: how does `window.trustStage` get set? Currently page defaults to 1.
   - **Option A**: server-rendered template variable: `<script>window.trustStage = {{ trust_stage }};</script>`
   - **Option B**: `/api/v1/me` or `/api/v1/trust/stage` endpoint that frontend fetches early
   **My lean**: **Option A** — simpler, no extra round-trip, works on initial render.
5. **Empty state**: page already shows "No insights yet — We'll learn together as we work. Check back after a few sessions." This is good. Confirm.
6. **Topic mapping**: spec lists 5 categories (Work Patterns / Projects / Preferences / Relationships / Scheduling). `SurfaceableInsight.context_tags` and `learning.topic_tags` are free-form. How does an insight get assigned a topic for the UI tabs?
   - **Option A**: `SurfaceableInsight` carries explicit `topic` field; CompostingExtractor decides
   - **Option B**: API derives topic from `learning.topic_tags` via mapping rules
   - **Option C**: leave topic-mapping out for MVP; show all insights in "All" tab; topic tabs visually present but functional in Post-MVP
   **My lean**: **Option C** for #1031 MVP — topic infrastructure isn't in `SurfaceableInsight` today; adding it is a separate concern. Tabs work cosmetically; "All" is the operational tab.

### Part C: Proceed/Revise Decision

- [ ] **PROCEED** — pending PM Q1-Q6 + #1035 merge
- [ ] **REVISE** — Q6 disposition (topic mapping) is the most likely scope-shaper
- [ ] **CLARIFY** — Q2 correction shape

---

## Phase 0: Initial Bookending - GitHub Investigation

### Required Actions

1. **GitHub Issue Verification**: `gh issue view 1031`

2. **Verify #1035 has merged**:
   ```bash
   gh issue view 1035 | grep -i state
   git log main --grep "#1035" --oneline | head -3
   ```

3. **Read `templates/insights.html`** end-to-end (already done in prior-art read, but Phase 0 confirms nothing changed):
   - Verify event-dispatch contract is what we assumed
   - Verify confidence binning still matches what `respond_to_pull` / framing layer produces

4. **Update issue body** to reflect scope-trim:
   ```
   ## Status: Scope-trimmed 2026-05-03

   Original issue assumed page needed building. Per Lead Dev prior-art
   read, templates/insights.html (748 lines, from #424 closed Jan 2026)
   is structurally complete. This issue's work is "wire to backend":
   - 5-6 endpoints under /api/v1/insights*
   - Replace TODO at templates/insights.html:455 with real fetch
   - Wire custom-event handlers to API calls
   - Trust-stage plumbing
   ```

### STOP Conditions

- #1035 not merged
- Page structure changed since prior-art read → re-read

---

## Phase 0.5: Frontend-Backend Contract Verification (MANDATORY for UI work)

### Applicability assessment

**Applies** — adding 5-6 new endpoints that the existing template will consume.

### Required Actions

1. **Document target endpoint shape**:
   ```
   GET /api/v1/insights?topic=all|work-patterns|projects|preferences|relationships|scheduling
   → { "insights": [{id, expression, confidence, topic, source_count, created_at, ...}], "trust_stage": int }

   POST /api/v1/insights/{id}/correct  body: {correction_text: string}
   → { "ok": true, "insight": {...} }

   POST /api/v1/insights/{id}/confirm
   → { "ok": true }

   POST /api/v1/insights/{id}/why
   → { "explanation": "I noticed this from N observations..." }

   DELETE /api/v1/insights/{id}
   → 204

   DELETE /api/v1/insights  (reset-all)
   → 204
   ```

2. **Path verification** (server up, post-Phase-2):
   ```bash
   curl -s http://localhost:8001/api/v1/insights | jq
   # Must return non-empty insights from #1035-persisted journal
   ```

3. **Static-file verification**: no new static files; routes mount on existing FastAPI app.

### STOP Conditions

- 404 from any endpoint after wiring → coordinate with mount-prefix verification
- Response schema mismatch with what `templates/insights.html` expects (see lines 482-498 + 542-573 for the JS reading the response) → resolve

---

## Phase 0.6: Data Flow & Integration Verification

### Applicability assessment

**Applies** — multi-layer: route → InsightRepository (#1035) → DB.

### Part A: Data Flow Requirements

| Layer | Needs change? |
|-------|---------------|
| `web/api/routes/insights.py` (NEW) | ✅ NEW — routes for the 5-6 endpoints |
| Or extend existing route file | (consult Phase 0) |
| `InsightRepository` | No change (built in #1035) |
| `InsightDB` | ✅ add `is_deleted: bool = False` (per Q1 lean: soft delete) + `user_correction: Optional[str]` (per Q2 Option A) |
| Migration | ✅ tiny migration adding the two columns |
| Auth: `get_current_user` dependency | ✅ all endpoints user-scoped |

### Part B: Integration Points Checklist

| Caller | Callee | Verification |
|--------|--------|--------------|
| `GET /api/v1/insights` | `InsightRepository.list_for_user(user_id, exclude_deleted=True)` | NEW repository method |
| `POST .../correct` | `InsightRepository.update_user_correction(insight_id, text)` | NEW repository method |
| `POST .../confirm` | `InsightRepository.mark_surfaced(insight_id, "engaged")` (existing) | Reuse |
| `POST .../why` | `InsightRepository.get(insight_id)` + format explanation | Read-only |
| `DELETE .../{id}` | `InsightRepository.soft_delete(insight_id, user_id)` | NEW (or `update is_deleted=True`) |
| `DELETE .../` | `InsightRepository.soft_delete_all(user_id)` | NEW |

### Part C: Pattern Adaptation Notes

The mount-prefix + auth + repository wrapping pattern is identical to other CRUD-style endpoints (e.g., todos under `/api/v1/todos`).

**Pitfalls**:
1. **Auth**: every endpoint must be user-scoped; mistakenly returning another user's insights is a privacy violation. Use `Depends(get_current_user)` consistently.
2. **Schema migration**: adding `is_deleted` + `user_correction` to `InsightDB` requires a tiny migration. Coordinate with #1035's migration head.
3. **Backwards compatibility**: existing `InsightRepository.add` callers must not break when new fields are added (default values handle this).
4. **Topic mapping (Q6 Option C lean)**: tabs are cosmetic for MVP; "All" is operational. Make sure the UI degrades gracefully — the page already has count badges that will show 0 for the per-topic tabs and N for "All".

### STOP Conditions

- Schema migration coordination conflict with #1035 → align
- Auth guard missed on any endpoint → block

---

## Phase 0.7: Conversation Design

### Applicability assessment

**Not applicable** — UI page browse experience, not conversation flow.

**Question for PM**: confirm Phase 0.7 inapplicability.

---

## Phase 0.8: Post-Completion Integration

### Applicability assessment

**Applies** — feature changes user state via correction/deletion writes.

### Completion Side-Effects Checklist

| Side Effect | Table/Field | Verified? |
|---|---|---|
| Correction recorded | `insights.user_correction` | ✅ test |
| Confirmation recorded | `insights.user_response = "engaged"` | ✅ test |
| Soft delete | `insights.is_deleted = true` | ✅ test |
| Reset-all | `insights.is_deleted = true` for all user's insights | ✅ test |
| Surfaced count incremented | `insights.surfaced_count` | only via Pull / Push, not Passive (browse doesn't count as surface) — confirm with PM |

### Downstream Behavior

| Feature | Before | After |
|---|---|---|
| Pull mode (#1030) | Sees all insights | Excludes user-deleted (`is_deleted=True`) |
| Push mode (#1032) | Sees all insights | Excludes user-deleted |
| Passive (this issue) | Empty | Shows non-deleted insights |

**Question for PM**: confirm whether "browsed via Passive" counts as a surfacing event (incrementing `surfaced_count`). My lean: NO — Passive is browse-on-demand, not surfacing.

---

## Phases 1-N: Development Work

### Phase 1: Schema migration (small)

**Work**:

- [ ] Migration `aXXXX_insight_user_correction_and_soft_delete.py`:
  - `ALTER TABLE insights ADD COLUMN is_deleted BOOLEAN NOT NULL DEFAULT FALSE`
  - `ALTER TABLE insights ADD COLUMN user_correction TEXT`
- [ ] Update `InsightDB` model + `from_domain` / `to_domain`
- [ ] Update `SurfaceableInsight` dataclass to add the two fields (with defaults)

**Tests**:
- [ ] Migration apply/revert round-trip
- [ ] `from_domain`/`to_domain` preserves new fields

### Phase 2: Repository extensions

**Work**:

- [ ] `InsightRepository.list_for_user(user_id, topic=None, exclude_deleted=True, limit=None)`
- [ ] `InsightRepository.update_user_correction(insight_id, text)`
- [ ] `InsightRepository.soft_delete(insight_id, user_id)` (verifies user owns)
- [ ] `InsightRepository.soft_delete_all(user_id)`
- [ ] `mark_surfaced` already exists (confirm with #1035)

**Tests**: each method round-trip with aiosqlite.importorskip pattern.

### Phase 3: Routes

**Work**:

- [ ] New file `services/api/insights.py` (or extension):
  ```python
  router = APIRouter(prefix="/api/v1/insights", tags=["insights"])

  @router.get("")
  async def list_insights(user=Depends(get_current_user), topic: Optional[str] = None):
      ...

  @router.post("/{insight_id}/correct")
  async def correct(insight_id: str, body: CorrectRequest, user=Depends(get_current_user)):
      ...

  @router.post("/{insight_id}/confirm")
  async def confirm(insight_id: str, user=Depends(get_current_user)):
      ...

  @router.post("/{insight_id}/why")
  async def why(insight_id: str, user=Depends(get_current_user)):
      ...

  @router.delete("/{insight_id}")
  async def delete_insight(insight_id: str, user=Depends(get_current_user)):
      ...

  @router.delete("")
  async def reset_all(user=Depends(get_current_user)):
      ...
  ```
- [ ] Mount router in `web/router_initializer.py` or `web/app.py`
- [ ] Pydantic request/response models

**Tests**:
- [ ] Endpoint integration tests with TestClient
- [ ] Auth: cross-user request returns 404 / 403, never another user's insight

### Phase 4: Frontend wiring

**Work**:

- [ ] In `templates/insights.html`, replace lines 455-457 TODO with real `fetch('/api/v1/insights', {credentials: 'include'})`
- [ ] Wire event listeners in the same script (or new script) for the dispatched custom events:
  ```js
  window.addEventListener('insight-correct', (e) => {
    const text = prompt('What should I have noticed instead?');
    if (text) {
      fetch(`/api/v1/insights/${e.detail.insight.id}/correct`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        credentials: 'include',
        body: JSON.stringify({correction_text: text})
      }).then(...)
    }
  });
  // similarly for insight-confirm, insight-why, insight-delete, insights-reset
  ```
- [ ] Add server-rendered `<script>window.trustStage = {{ trust_stage }};</script>` per Q4 Option A
- [ ] Update `insights_ui` route handler in `web/api/routes/ui.py` to pass `trust_stage` to the template (after fetching from `TrustComputationService`)

**Tests**:
- [ ] Template integration test: rendered HTML contains the trust-stage script
- [ ] Manual: page loads, fetches insights, displays them; clicking actions triggers API calls

### Phase 5: "Why?" response composition

**Work**:

- [ ] `POST /api/v1/insights/{id}/why` returns explanation text
- [ ] Format: "I noticed this from {source_count} observation(s) [optional: across {object names}]"
- [ ] Optional: frontend displays the explanation in a toast or modal (currently the event handler is a no-op `dispatchEvent`)

**Tests**:
- [ ] Unit tests for explanation formatting

### Phase 2a: Routing integration tests

**Not applicable** — these are CRUD endpoints, not intent-classifier routing. **PM approval requested**.

### Phase 2b: Wiring integration tests (REQUIRED)

- [ ] Wiring test: `GET /api/v1/insights` after #1035 + an insight added via `InsightJournal.add` → endpoint returns the insight
- [ ] Wiring test: `DELETE /api/v1/insights/{id}` → next `GET` excludes it
- [ ] Wiring test: `POST .../correct` → DB carries `user_correction` text

### Phase 6: Manual verification

- [ ] Browser scenarios: load page → see insights → click each affordance → verify behavior
- [ ] Cross-user: log in as different user → only that user's insights visible

---

## Phase Z: Final Bookending & Handoff

### Required Actions

1. **GitHub Final Update**:
   ```
   ## Status: Complete - Awaiting PM Approval
   - Backend insights API (5-6 endpoints) wired
   - Frontend TODO replaced with real fetch + custom-event handlers
   - Trust-stage server-rendered to template
   - Soft delete (Q1) + correction text (Q2 Option A) + topic-tabs-cosmetic-for-MVP (Q6 Option C)
   - Tests + manual scenarios pass
   - #1030 Pull and #1032 Push see consistent insight set (excludes deleted)
   ```

2. **Documentation**:
   - [ ] Update #1031 issue with scope-trim note (already did Phase 0 update)
   - [ ] Cross-reference D2 + D4 spec in code comments

3. **Evidence Compilation**:
   - [ ] Test output (Phases 1-5)
   - [ ] Browser screenshots
   - [ ] curl examples

4. **Handoff**:
   - [ ] Update #707 tracker: `[x] #1031 MUX-INSIGHT-PASSIVE`
   - [ ] Note for #1030/#1032: deleted insights are excluded by default

5. **Session log** complete

6. **PM Approval Request** standard

---

## Multi-Agent Coordination Plan

Single agent (Lead Dev). Multi-component but tightly coupled.

### Verification Gates

- [ ] Phase 1: schema migration round-trip
- [ ] Phase 2: repository unit tests pass
- [ ] Phase 3: endpoint integration tests pass (incl. cross-user auth check)
- [ ] Phase 4: frontend manual smoke
- [ ] Phase 2b: wiring tests pass
- [ ] Phase 6: cross-user verification

---

## STOP Conditions

- #1035 not merged
- Auth guard missing on any endpoint
- Page structure changed unexpectedly
- Topic-mapping disagreement (Q6) → re-scope

---

## Evidence Requirements

- Test output for Phases 1-5
- Browser screenshots
- Cross-user auth test output
- git diff of frontend wiring changes

---

## Effort Estimate

**Overall Size**: Medium (~3-4 hours)

| Phase | Estimate |
|-------|----------|
| Phase -1 PM walk | 25 min |
| Phase 0 verify-#1035 + prior-art recheck | 15 min |
| Phase 1 schema | 30 min |
| Phase 2 repository | 45 min |
| Phase 3 routes | 1 hr |
| Phase 4 frontend wiring | 45 min |
| Phase 5 why-response | 15 min |
| Phase 2b wiring | 30 min |
| Phase 6 manual | 20 min |
| Phase Z bookend | 15 min |

---

## Dependencies

- [ ] #1035 must merge
- [x] Insight Journal page structurally complete from #424
- [x] InsightRepository pattern established by #1035

## Blocks

- M2d gate completeness; #707 tracker

---

# Audit-Cascade: Gameplan vs gameplan-template v9.3

## Audit Matrix

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| Phase -1: Infrastructure Verification | ✅ | Detailed inventory of what's done vs what's needed; six PM Qs |
| Phase -1: Worktree Assessment | ✅ | USE WORKTREE based on #1035 |
| Phase -1: PM Verification placeholder | ⚠️ | Six Qs queued |
| Phase 0: GitHub Issue Verification | ✅ | Step + scope-trim update |
| Phase 0: Codebase Investigation | ✅ | Re-verify prior-art unchanged |
| Phase 0: Update GitHub Issue with scope-trim | ✅ | Status template includes scope-trim language |
| Phase 0: STOP Conditions | ✅ | Two named |
| Phase 0.5: Applicability | ✅ | Applies (5-6 new endpoints + frontend) |
| Phase 0.5: Endpoint shape documented | ✅ | All 6 endpoints with request/response |
| Phase 0.5: Path verification (curl) | ✅ | Listed for Phase-2 |
| Phase 0.5: Static-file verification | ✅ | No new static files |
| Phase 0.5: STOP Conditions | ✅ | Two named |
| Phase 0.6: Applicability | ✅ | Applies (multi-layer route → repo → DB) |
| Phase 0.6: Data Flow Requirements | ✅ | 6-row layer table |
| Phase 0.6: Integration Points | ✅ | Caller→callee; auth-scoped guidance |
| Phase 0.6: Pattern Adaptation Notes | ✅ | Identical to existing CRUD pattern; four pitfalls |
| Phase 0.6: STOP Conditions | ✅ | Two named |
| Phase 0.7: Conversation Design | ⚠️ | Marked inapplicable (UI browse, not conversation); **PM approval requested** |
| Phase 0.8: Post-Completion Integration | ✅ | Applies; side-effects table + downstream behavior table |
| Phases 1-N: Development with progressive bookending | ✅ | Phases 1-6 + 2a + 2b defined |
| Phase 2a: Routing integration tests | ⚠️ | Marked N/A — CRUD not classifier; **PM approval requested** |
| Phase 2b: Wiring integration tests | ✅ | Three end-to-end tests |
| Phase Z: GitHub Final Update | ✅ | Template included |
| Phase Z: Documentation Updates | ✅ | Spec cross-references + scope-trim note |
| Phase Z: Evidence Compilation | ✅ | Listed |
| Phase Z: Handoff Preparation | ✅ | #707 tracker + #1030/#1032 deleted-exclusion note |
| Phase Z: Session Completion | ✅ | Listed |
| Phase Z: PM Approval Request | ✅ | Template included |
| Multi-Agent Coordination Plan | ✅ | Single-agent justification |
| Verification Gates | ✅ | Listed per Phase + cross-user auth check |
| STOP Conditions (throughout) | ✅ | Section included |
| Evidence Requirements | ✅ | Listed |
| Effort Estimate | ✅ | Per-phase ~3-4 hr |
| Dependencies + Blocks | ✅ | #1035 + #424 prior art |
| Test Scope | ✅ | Unit + integration + wiring + cross-user |

## Action Required Before Proceeding

1. **Phase -1 Qs 1-6** (delete semantics, correction shape, why-response shape, trust-stage plumbing, empty-state, topic mapping)
2. **Phase 0.7 + 2a inapplicability** confirmations per audit-cascade skill
3. **#1035 must merge**
4. **Side-effect Q on `surfaced_count` semantic** (does Passive browse increment?) per Phase 0.8

## Status

**Audit cascade gate: NOT YET PASSED.** Two ⚠️ items pending PM input. No ❌ items.
