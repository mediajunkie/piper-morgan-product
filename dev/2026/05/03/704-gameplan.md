# Gameplan: #704 MUX-LIFECYCLE-UI-A (Morning Standup integration)

**Issue**: https://github.com/mediajunkie/piper-morgan-product/issues/704
**Author**: Lead Developer (Claude Code Opus)
**Date**: 2026-05-03
**Template version**: gameplan-template v9.3
**Status**: Draft — pending audit-cascade against template + PM Phase -1 walkthrough
**Blocked by**: #1034 STANDUP-STRUCTURED-WORKITEMS (must merge first)

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Lead Developer's Current Understanding

**Infrastructure Status** (from spike + this gameplan-prep read):

- [x] Web framework: **FastAPI** (`web/api/routes/standup.py` + `web/api/routes/ui.py:282` for the standup UI route)
- [x] Standup UI route: `GET /standup` returns `templates/standup.html` (`web/api/routes/ui.py:282-287`)
- [x] Standup API: `POST /api/v1/standup/generate` returns standup payload (`web/api/routes/standup.py:520`)
- [x] Lifecycle indicator components ready (`templates/components/lifecycle_indicator.html` + `lifecycle_detail.html` + `lifecycle_notification.html`)
- [x] `LifecycleIndicator.create(stage: string, compact: bool = false) → HTMLElement` JS API live (`templates/components/lifecycle_indicator.html:227-256`)
- [x] Stage values per `services/mux/lifecycle.py`: `emergent | derived | noticed | proposed | ratified | deprecated | archived | composted`
- [x] Experience phrases live in JS (e.g., `RATIFIED: "We're doing..."`) and match `lifecycle-experience-guide.md`
- [x] **Pre-work #1034**: structured per-item dicts must reach the template (currently `List[str]`); blocked until #1034 merges

**Lead Dev's understanding of the task**:

After #1034 lands, the standup API response carries per-item dicts with `lifecycle_state`. This issue:
1. Includes the lifecycle indicator component template + JS in `standup.html`
2. Updates the template's render loop to call `LifecycleIndicator.create(item.lifecycle_state, true)` per item that has lifecycle_state, appending the dot indicator
3. Items without lifecycle_state render unchanged (graceful degradation)
4. Adds template tests verifying indicator rendering

This is the small, well-scoped "wire indicator into template" issue the body originally promised. Today it's not deliverable; after #1034, it is.

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**

- [ ] Multi-agent — no
- [x] Task duration ~30 min - 1 hr — small
- [ ] Multi-component — no, frontend-only
- [ ] Exploratory/risky — no, well-scoped
- [ ] Coordination queue — no

**Assessment**: **SKIP WORKTREE** — single agent, ~45 min, frontend-only, on top of #1034 branch. Stage on the #1034 worktree (`piper-morgan-product-1034-standup`) once #1034 lands, OR on a fresh worktree off main once #1034 merges.

Rationale: worktree overhead exceeds benefit for a 45-min single-agent template change.

### Part B: PM Verification Required

Questions for PM:

1. **Layout decision**: where on each item line does the dot go? Inline before the icon (`[● ✅ commit msg]`)? Inline after the icon (`[✅ ● commit msg]`)? After the text (`[✅ commit msg ●]`)? **My lean**: inline after the icon (`✅ ● commit msg`) — lifecycle is a "second-order signal"; primary content stays first.
2. **Hover behavior**: spec says "hovering shows experience phrase tooltip." `LifecycleIndicator.create(stage, compact=true)` already handles this via the tooltip element baked into the template. Confirm: the existing tooltip behavior is sufficient (no custom hover work needed).
3. **Accessibility scope**: spec says "Accessible (keyboard focusable)." Indicators are inline visual elements; making each one a focus stop in a list of 10+ items may be noisy. Confirm: aria-label on the indicator (already done in `createIndicator` line 247) is sufficient; we don't need each indicator to be a tab-stop.
4. **Items that get indicators**: only `source: "work"` items carry `lifecycle_state` (per #1034 spec — commits, repos, system blockers don't have lifecycle). Confirm scope is "show indicator on items where `lifecycle_state` is present, else nothing" — graceful, no special-casing per source type.

### Part C: Proceed/Revise Decision

- [ ] **PROCEED** (after #1034 merges) — pending PM confirmation on Q1-Q4
- [ ] **REVISE** — only if Q1 layout decision triggers re-design
- [ ] **CLARIFY** — if accessibility scope expands

---

## Phase 0: Initial Bookending - GitHub Investigation

### Required Actions

1. **GitHub Issue Verification**:
   ```bash
   gh issue view 704
   ```

2. **Verify #1034 has merged**:
   ```bash
   gh issue view 1034 | grep -i state
   git log main --grep "#1034" --oneline | head -3
   ```
   STOP if #1034 has not merged.

3. **Codebase Investigation**:
   ```bash
   # Verify standup.html structure is what spike found
   grep -n "yesterday_accomplishments\|today_priorities\|blockers" templates/standup.html

   # Verify lifecycle indicator API still as documented
   grep -n "createIndicator\|window.LifecycleIndicator" templates/components/lifecycle_indicator.html

   # Verify post-#1034 API response shape (curl, server up)
   curl -s -X POST http://localhost:8001/api/v1/standup/generate -H "Content-Type: application/json" -d '{...}' | jq '.standup.yesterday_accomplishments[0]'
   ```

4. **Update GitHub Issue**:
   ```
   ## Status: Investigation Started
   - [ ] #1034 merged
   - [ ] Lifecycle indicator API surface confirmed
   - [ ] Post-#1034 API response shape verified live
   ```

### STOP Conditions

- #1034 not yet merged → wait
- Lifecycle indicator API has changed unexpectedly → re-scope
- Post-#1034 API response doesn't carry `lifecycle_state` per item → coordinate with #1034 closure

---

## Phase 0.5: Frontend-Backend Contract Verification (MANDATORY for UI work)

### Applicability assessment

**Applies** — this issue connects the frontend (`standup.html`) to the API contract that #1034 establishes.

### Required Actions

1. **Document the verified API response shape** (post-#1034 — should match):
   ```json
   {
     "standup": {
       "yesterday_accomplishments": [
         {"display": "...", "source": "work", "lifecycle_state": "ratified", "icon": "📋"},
         {"display": "...", "source": "commit", "lifecycle_state": null, "icon": "✅"}
       ],
       ...
     }
   }
   ```

2. **Path verification** (server running):
   ```bash
   curl -sX POST http://localhost:8001/api/v1/standup/generate -H "Content-Type: application/json" -d '{"user_id":"alpha","mode":"standard"}' | jq '.standup.yesterday_accomplishments'
   # Must NOT 404
   # Must contain the structured dict shape
   ```

3. **Static-file verification**: `templates/components/lifecycle_indicator.html` is included via Jinja `{% include %}`; no static-file path changes.

### STOP Conditions

- API path returns 404 → coordinate with #1034 / #1018 lifespan ordering
- Shape doesn't match expectation → coordinate with #1034 closure

---

## Phase 0.6: Data Flow & Integration Verification

### Applicability assessment

**Marginal**: this is a frontend-only issue — there's no NEW data flow being introduced. The data flow change happened in #1034. This issue consumes #1034's contract.

For audit-cascade rigor, the verification step here is: **confirm the data shape #1034 ships matches what this gameplan assumes.**

### Part A: Data Flow Requirements

| Layer | Responsibility | Verification |
|-------|----------------|--------------|
| API response | Carries per-item dicts with `lifecycle_state` (post-#1034) | curl + jq verify |
| Template (`standup.html`) | Reads `item.lifecycle_state` and `item.display`; calls `LifecycleIndicator.create()` if present | new code in this issue |
| Lifecycle indicator JS | Renders dot + tooltip (existing) | confirmed in component |

### Part B: Integration Points Checklist

| Caller | Callee | Verified? |
|--------|--------|-----------|
| `standup.html` JS render loop | `LifecycleIndicator.create(stage, true)` | After Phase 1 |
| `LifecycleIndicator.create` | template `#lifecycle-indicator-template` | Already wired via `{% include %}` we'll add |

### Part C: Pattern Adaptation Notes

This is the **reference implementation** for the lifecycle-indicator pattern across MUX-conscious surfaces. Future surfaces (todos, projects, lists) will copy the pattern from here. So while this issue isn't *adopting* a pattern, it's *establishing* one.

**Documentation deliverable**: a brief comment block in `standup.html` explaining the integration pattern.

### STOP Conditions

- If #1034's contract diverges from the gameplan assumption → STOP and align

---

## Phase 0.7: Conversation Design

### Applicability assessment

**Not applicable** — visual UI change, no conversation flow.

### Per audit-cascade skill: PM approval needed

**Question for PM**: confirm Phase 0.7 inapplicability.

---

## Phase 0.8: Post-Completion Integration

### Applicability assessment

**Not applicable** — read-only template change, no user state changes, no DB writes.

### Per audit-cascade skill: PM approval needed

**Question for PM**: confirm Phase 0.8 inapplicability.

---

## Phases 1-N: Development Work

### Phase 1: Template integration

**Work**:

- [ ] Add `{% include "components/lifecycle_indicator.html" %}` to `standup.html` head (loads the component template, CSS, and JS API)
- [ ] Update the JS render loop to render structured items:
  ```js
  ${(standup.yesterday_accomplishments || []).map((item) => {
    const indicatorEl = item.lifecycle_state
      ? `<span class="lifecycle-inline" data-stage="${item.lifecycle_state}"></span>`
      : '';
    return `<li>${item.icon} ${indicatorEl} ${item.display}</li>`;
  }).join("")}
  ```
- [ ] After innerHTML update, walk the rendered DOM and replace `.lifecycle-inline` placeholder with `LifecycleIndicator.create(stage, true)`:
  ```js
  document.querySelectorAll('.lifecycle-inline').forEach(el => {
    const stage = el.dataset.stage;
    const indicator = window.LifecycleIndicator?.create(stage, true);
    if (indicator) el.replaceWith(indicator);
  });
  ```
  (This indirection is needed because the lifecycle indicator's HTML template is rendered via `template.content.cloneNode()` rather than as a string.)
- [ ] Apply same pattern to `today_priorities` and `blockers`
- [ ] Apply same pattern to any list rendering structured items

**Bookend**: comment on #704 with "Phase 1 complete: standup.html renders inline lifecycle indicators per item with lifecycle_state."

### Phase 2: Tests

**Work**:

- [ ] Template tests in `tests/unit/templates/test_standup_lifecycle.py`:
  - `test_indicator_renders_when_lifecycle_present`: response with `lifecycle_state="ratified"` → rendered HTML contains `data-lifecycle-stage="ratified"`
  - `test_indicator_not_rendered_when_no_lifecycle`: response with `lifecycle_state=null` → no `lifecycle-indicator` element
  - `test_compact_mode`: verify `data-compact="true"` on rendered indicators
  - `test_experience_phrase_in_aria_label`: rendered indicator has `aria-label="Lifecycle: We're doing..."` (or matching phrase)
  - `test_no_technical_labels_visible`: rendered HTML does NOT contain "RATIFIED" / "PROPOSED" / etc. as visible text (only as data attributes)

**Bookend**: Phase 2 complete with test output.

### Phase 2a: Routing integration tests

**Not applicable**.

### Phase 2b: Wiring integration tests

Marginal: the API contract change happened in #1034. For this issue, a targeted **end-to-end smoke** is sufficient (not a full wiring test).

- [ ] Smoke test: server up, hit `/api/v1/standup/generate`, render `/standup` HTML, verify a lifecycle indicator element exists for items with `lifecycle_state`

### Phase 3: Manual verification

**Scenarios to verify in browser** (server up):
1. **Lifecycle visibility**: standup contains an item with `lifecycle_state` → indicator dot visible inline
2. **Graceful degradation**: standup contains an item without `lifecycle_state` → no indicator, no console error
3. **Tooltip on hover**: hovering over indicator shows experience phrase ("We're doing...", "I learned that...", etc.)
4. **No technical labels visible**: nothing on screen reads "RATIFIED" or "PROPOSED" — only experience phrases
5. **Color**: indicator dot color matches the stage (per legend at top of `lifecycle_indicator.html`)
6. **No regressions**: standup loads, generates, displays summary as before; no console errors

---

## Phase Z: Final Bookending & Handoff

### Required Actions

1. **GitHub Final Update**:
   ```
   ## Status: Complete - Awaiting PM Approval
   - Lifecycle indicators render in standup view per #1034 contract
   - Tests passing (paste output)
   - No technical labels visible in user-facing output
   - Experience phrases in tooltips + aria-labels
   - Graceful degradation verified for items without lifecycle_state
   - Reference pattern documented in standup.html comment block
   ```

2. **Documentation**:
   - [ ] Comment block in `standup.html` documenting the inline-indicator render pattern
   - [ ] Cross-reference to spike doc + #1034 + #423 (UI components)
   - [ ] Update #703 tracking issue: `[x] #704 MUX-LIFECYCLE-UI-A` complete

3. **Evidence Compilation**:
   - [ ] Test output (Phase 2)
   - [ ] Browser screenshot or curl+jq output of an indicator-bearing item
   - [ ] Files modified list

4. **Handoff**:
   - [ ] Document on #703 that #704 is reference implementation for the pattern; future surfaces (todos, projects) can copy this pattern
   - [ ] Update #703 success criteria checkbox

5. **Session log** complete

6. **PM Approval Request**:
   ```
   @PM - #704 complete:
   - Indicator wiring landed; reference implementation
   - Tests + manual scenarios pass
   - #703 tracking issue updated
   ```

---

## Multi-Agent Coordination Plan

Single agent (Lead Dev). Frontend-only single-file change.

### Verification Gates

- [ ] Phase 1: Template renders without errors
- [ ] Phase 2: Template tests pass
- [ ] Phase 3: Manual browser scenarios pass
- [ ] Phase Z: #703 tracking issue updated; PM approval request

---

## STOP Conditions

- #1034 not merged → wait
- Existing standup tests fail → investigate
- Performance: render lag visible (>50ms for 10 items) → optimize before ship
- Console errors → block

---

## Evidence Requirements

- [ ] Test output for Phase 2
- [ ] Browser screenshot showing indicator + tooltip on hover
- [ ] git diff of `templates/standup.html` + new test file

---

## Effort Estimate

**Overall Size**: Small (~45 min - 1 hr)

| Phase | Estimate |
|-------|----------|
| Phase -1 PM walk | 10 min |
| Phase 0 verify-#1034-landed | 5 min |
| Phase 0.5 contract verify | 5 min |
| Phase 1 template change | 20 min |
| Phase 2 tests | 15 min |
| Phase 3 manual | 10 min |
| Phase Z bookend | 10 min |

---

## Dependencies

- [ ] **#1034 STANDUP-STRUCTURED-WORKITEMS** must merge first (blocking)
- [x] Lifecycle indicator components already built (#423 closed)
- [x] WorkItem.lifecycle_state already exists in domain model

## Blocks

None directly — but #704 is a tracking-issue child of #703, so #703's M2d-gate-completion criteria depends on this.

---

# Audit-Cascade: Gameplan vs gameplan-template v9.3

## Audit Matrix

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| Phase -1: Infrastructure Verification | ✅ | Filled with spike findings; four PM Qs queued |
| Phase -1: Worktree Assessment | ✅ | SKIP WORKTREE — small frontend change |
| Phase -1: PM Verification placeholder | ⚠️ | Four explicit Qs need PM walkthrough |
| Phase 0: GitHub Issue Verification | ✅ | `gh issue view 704` step; verify-#1034-merged step added |
| Phase 0: Codebase Investigation | ✅ | grep + curl-shape steps |
| Phase 0: STOP Conditions | ✅ | Three named (incl. dependency on #1034 contract) |
| Phase 0.5: Applicability | ✅ | Applies — frontend consumes API contract |
| Phase 0.5: API path documentation | ✅ | curl example included |
| Phase 0.5: Static-file verification | ✅ | No new static files; `{% include %}` documented |
| Phase 0.5: STOP Conditions | ✅ | Two named |
| Phase 0.6: Applicability | ⚠️ | Marked **marginal** — no NEW data flow added; relies on #1034 contract; **PM approval requested** for marginal-applicability framing |
| Phase 0.6: Data Flow Requirements | ✅ | 3-row layer table |
| Phase 0.6: Integration Points | ✅ | 2-row caller→callee |
| Phase 0.6: Pattern Adaptation Notes | ✅ | This is the reference impl establishing the pattern |
| Phase 0.7: Conversation Design | ⚠️ | Marked inapplicable; **PM approval requested** |
| Phase 0.8: Post-Completion Integration | ⚠️ | Marked inapplicable (read-only template); **PM approval requested** |
| Phases 1-N: Development with progressive bookending | ✅ | Phase 1, 2, 2a, 2b, 3 defined; bookend examples |
| Phase 2a: Routing integration tests | ⚠️ | Marked N/A — not intent/classifier work; **PM approval requested** |
| Phase 2b: Wiring integration tests | ⚠️ | Marked **marginal** — full wiring done in #1034; smoke test sufficient here; **PM approval requested** |
| Phase Z: GitHub Final Update | ✅ | Template included |
| Phase Z: Documentation Updates | ✅ | Reference-pattern comment block documented |
| Phase Z: Evidence Compilation | ✅ | Listed |
| Phase Z: Handoff Preparation | ✅ | #703 tracker update + future-surface handoff documented |
| Phase Z: Session Completion | ✅ | Listed |
| Phase Z: PM Approval Request | ✅ | Template included |
| Multi-Agent Coordination Plan | ✅ | Single agent — small change |
| Verification Gates | ✅ | Listed |
| STOP Conditions (throughout) | ✅ | Section included |
| Evidence Requirements | ✅ | Listed |
| Effort Estimate | ✅ | Per-phase; ~45 min - 1 hr |
| Dependencies + Blocks | ✅ | #1034 dependency explicit |
| Test Scope | ✅ | Unit (template tests), smoke (manual + curl) |

## Action Required Before Proceeding

1. **Phase -1 Qs 1-4** (layout, hover, a11y scope, item-source scope)
2. **Phase 0.6 marginal-applicability** confirmation
3. **Phase 0.7 + 0.8 + 2a inapplicability + 2b marginal-applicability** confirmations per audit-cascade skill
4. **#1034 must merge** before this gameplan executes (gating dependency, not an audit item)

## Status

**Audit cascade gate: NOT YET PASSED.** Six ⚠️ items pending PM input. No ❌ items.
