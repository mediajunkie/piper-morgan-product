# Gameplan: #1033 MUX-COMPOSTED-EXPERIENCE

**Issue**: https://github.com/mediajunkie/piper-morgan-product/issues/1033
**Author**: Lead Developer (Claude Code Opus)
**Date**: 2026-05-03
**Template version**: gameplan-template v9.3
**Status**: Draft — pending audit-cascade against template + PM Phase -1 walkthrough
**Blocked by**: #1035 MUX-COMPOSTING-ACTIVATION (must merge first)

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Lead Developer's Current Understanding

**Infrastructure Status** (from spike + this gameplan-prep read):

- [x] `LifecycleState.COMPOSTED` enum value: `services/mux/lifecycle.py:91` with `experience_phrase = "I learned that..."` per `lifecycle-experience-guide.md`
- [x] `LifecycleState.experience_phrase()` method exists (`services/mux/lifecycle.py:77`); returns the phrase given the stage
- [x] `COMPOSTING_FRAMES` reflection-language constants live (`services/mux/composting_scheduler.py:34-47`):
  - "Having had some time to reflect..."
  - "Looking back at our work together..."
  - "Something I've been thinking about..."
  - "It occurs to me that..."
  - "I've been mulling over..."
  - "After some thought..."
  - "In quiet moments, I realized..."
- [x] `frame_learning(learning: ExtractedLearning) -> str` (`services/mux/composting_scheduler.py:45`) wraps a learning's expression in a randomly chosen framing prefix
- [x] `SURFACING_FRAMES` (`services/mux/premonition.py:40+`) carries reflection / concern / offer / correction framing buckets
- [x] `frame_insight_for_surfacing(insight: SurfaceableInsight) -> str` (`services/mux/premonition.py:66`) frames a SurfaceableInsight for output
- [x] **Composting pipeline classes exist** but are NOT wired into runtime — gated by **#1035 MUX-COMPOSTING-ACTIVATION** (filed today as pre-work)
- [x] Response composition entry points (where COMPOSTED-derived content reaches the user):
  - `services/intent_service/conversational_floor.py:562` `ConversationalFloor.respond(ctx) -> FloorResponse` — the floor LLM path
  - The floor is where insights would surface in conversation
- [x] Anti-surveillance phrasing patterns to forbid (per `composting-experience-design.md` D3): "I've been watching", "While you were away", "Based on my surveillance", "I've been monitoring", "I observed" (in surveillance context), "I noticed your behavior"

**Lead Dev's understanding of the task**:

#1033 makes COMPOSTED-derived insights user-visible with reflection framing rather than surveillance framing. Specifically:

1. **Surfacing path**: when an insight (composted from a COMPOSTED-state object) reaches the user, the framing comes from `COMPOSTING_FRAMES` / `SURFACING_FRAMES["reflection"]` — not from default LLM language that might invent surveillance phrasing
2. **Anti-surveillance guardrail**: forbidden phrase patterns are detected; output containing them is regenerated or stripped
3. **Tests** that verify reflection framing is used + surveillance phrasing is absent across a probe set

The framing libraries exist. The integration into the response composer is the work. This is a small-to-medium-sized feature dependent on #1035 to actually have insights to surface.

### Part A.2: Work Characteristics Assessment

**Worktree Candidate?**

- [x] Multi-component (response composer + framing + tests + anti-pattern guardrail)
- [x] Task duration ~2-3 hours
- [ ] Multi-agent — no
- [x] Exploratory: anti-surveillance regression-test design has a research dimension

**Assessment**: **USE WORKTREE** — branch `claude/1033-composted-experience` based on `claude/1035-composting-activation` (since this depends on #1035).

### Part B: PM Verification Required

Questions for PM:

1. **Surfacing channel**: where does COMPOSTED-derived insight content enter the user-visible output?
   - **Option A (lean)**: through the floor LLM's response composer — extend `ConversationalFloor.respond` or similar to optionally include framed-insight content when the user query semantically aligns
   - **Option B**: as a separate channel (e.g., a "morning briefing" surfacing path, not via the conversational floor)
   - **Option C**: only via Pull mode (#1030) and Push mode (#1032) — meaning #1033's surfacing-path scope is just defining the framing layer that those modes use, not adding a new entry point
   **My lean**: **Option C** — keeps #1033 cleanly scoped to "framing rules + anti-surveillance guardrails for COMPOSTED-derived output," and the actual surfacing entry points are #1030/#1032/#1031. #1033 then becomes the "the framing layer is correct" issue that those modes consume.
2. **Anti-surveillance regression set**: what's the right scope? Hand-curated 20 probe set, parallel to #1004 ethics probe set? Or smaller (5-10) for MVP? **My lean**: 10 probes for MVP — enough to catch the obvious anti-patterns; can grow with audit findings.
3. **Forbidden phrase enforcement strictness**:
   - **Strict**: regex match → reject output → regenerate
   - **Soft**: regex match → log warning + redact → continue
   - **Hybrid**: strict during composition, soft as a fail-safe
   **My lean**: **strict** — for MVP, fail-loud is better than fail-quiet on the most distinctive MUX surface. Failures should be visible to me/CXO via logs; production user impact is "Piper says 'I don't have anything to share right now'" which is gentle.
4. **Test coverage for the guardrail**: how do we test that the LLM doesn't generate surveillance phrasing? Unit-test the framing helpers (deterministic; easy). Probe-test the regex guardrail (deterministic; easy). End-to-end through the LLM (non-deterministic; expensive). **My lean**: unit + regex coverage for MVP; LLM-end-to-end tests as separate AAXT canonical scenarios at #1004-equivalent test layer.
5. **`composting-experience-design.md` (D3) reference document**: I haven't re-read it as part of this gameplan-drafting. Phase 0 must include "read D3 end-to-end" before Phase 1.

### Part C: Proceed/Revise Decision

- [ ] **PROCEED** — pending PM Q1-Q5 + #1035 merge
- [ ] **REVISE** — Q1 disposition (especially Option C path) significantly shapes the work
- [ ] **CLARIFY** — D3 read may surface constraints not yet visible

---

## Phase 0: Initial Bookending - GitHub Investigation

### Required Actions

1. **GitHub Issue Verification**: `gh issue view 1033`

2. **Verify #1035 has merged**:
   ```bash
   gh issue view 1035 | grep -i state
   git log main --grep "#1035" --oneline | head -3
   ```
   STOP if not merged.

3. **Read source spec**:
   - [ ] `docs/internal/design/mux/composting-experience-design.md` (D3) end-to-end
   - [ ] `docs/internal/architecture/current/lifecycle-experience-guide.md` for COMPOSTED state language
   - [ ] Cross-reference any decisions or constraints into Phase 1 design

4. **Codebase Investigation** (extend Phase -1):
   ```bash
   # Verify existing surveillance-language audits (if any)
   grep -rn "surveillance\|I've been watching\|While you were away" services/ tests/ docs/ 2>/dev/null

   # Inventory framing-helper consumers
   grep -rn "frame_learning\|frame_insight_for_surfacing\|COMPOSTING_FRAMES" services/

   # Check existing #1004 ethics probe set for pattern to follow
   ls dev/2026/04/27/ | grep -i probe
   find tests -path "*ethics*" -name "*probe*"
   ```

5. **Update GitHub Issue**:
   ```
   ## Status: Investigation Started
   - [ ] #1035 merged
   - [ ] D3 spec read; framing rules verified vs implementation
   - [ ] Probe set design v0
   ```

### STOP Conditions

- #1035 not yet merged → wait
- D3 reveals framing/timing/scheduling rules not currently covered by COMPOSTING_FRAMES — surface to PM (may need spec amendment or scope expansion)

---

## Phase 0.5: Frontend-Backend Contract Verification

### Applicability assessment

**Marginal**: this is mostly a backend/text-processing issue. It changes the *content* of strings the user sees, not the API shape. If Q1 Option C is taken (the lean), no new endpoints are added — this issue defines a framing layer that #1030/#1031/#1032 consume.

**Question for PM**: confirm marginal-applicability framing per audit-cascade.

---

## Phase 0.6: Data Flow & Integration Verification

### Applicability assessment

**Applies marginally** — multi-layer in the sense that framing helpers will be called from response-composition paths in #1030/#1032/#1031. Within #1033's scope, the integration is: insight → framing helper → output string. No new layers added; the framing layer is wrapped around existing output paths.

### Part A: Data Flow

| Layer | What happens |
|-------|--------------|
| Insight retrieved (#1030/#1031/#1032 work) | SurfaceableInsight from InsightRepository |
| `frame_insight_for_surfacing(insight)` | Returns string with reflection framing |
| `assert_no_surveillance_phrasing(text)` (NEW) | Regex check; raises if forbidden phrase present |
| Output to user | Via the consuming mode's existing channel |

### Part B: Integration Points Checklist

| Caller | Callee | Verification |
|--------|--------|--------------|
| #1030 PULL | `frame_insight_for_surfacing` | Phase 1 of #1033 confirms helper signature stable |
| #1031 PASSIVE | (frontend reads insight expression, which already has framing applied via `frame_learning` at compost time) | Check: is the expression already framed before storage, OR framed at surface time? `composting_scheduler.py:271` does `learning.expression = frame_learning(learning)` — so framing is **at compost time**, baked into the stored expression. |
| #1032 PUSH | `frame_insight_for_surfacing` + guardrail | Same |
| Anywhere COMPOSTED-derived content reaches user | `assert_no_surveillance_phrasing` | Helper introduced by this issue |

**Pitfall surfaced by Phase -1 read**: framing happens at compost time (`frame_learning` runs in `CompostingScheduler.run` — line 271 of `composting_scheduler.py`). So the stored insight already contains a reflection frame. This is good — but it means surveillance-phrasing prevention has TWO layers:
1. **Compost-time**: framing helpers prevent surveillance phrasing entering the stored expression
2. **Surface-time**: guardrail catches LLM-generated surveillance phrasing (e.g., when LLM is asked to summarize multiple insights)

Both layers needed. This is not in the issue body explicitly — surface for PM confirmation.

### Part C: Pattern Adaptation

This is similar in shape to #1004 ETHICS-ACTIVATE: a probe set + regex/keyword guardrail + framing rules + tests. Adopt that pattern.

| Aspect | #1004 ETHICS | #1033 COMPOSTED |
|---|---|---|
| Probe set | 20 probes (boundary triggers) | ~10 probes (insight-surfacing prompts) |
| Guardrail | Boundary triggers / ethics floor decline | Forbidden surveillance phrases (regex) |
| Framing | Voice guidance + ethics decline | COMPOSTING_FRAMES / SURFACING_FRAMES |
| Test layer | tests/ethics/ | tests/mux/ |

### STOP Conditions

- D3 specifies a third framing layer not in the existing helpers → re-scope
- Probe-set design surfaces ambiguous cases (e.g., "is 'I observed your pattern' surveillance or just direct?") → resolve with PM/CXO before tests are committed

---

## Phase 0.7: Conversation Design

### Applicability assessment

**Partially applies** — output framing IS a conversation-design concern, even though no multi-turn flow is being added. The "Happy Path Script" + "Edge Cases" sections are useful for documenting the framing rules.

Question for PM: confirm partial-applicability framing per audit-cascade.

### Part A: Happy Path

```
[Composting cycle runs overnight; insight composted with framing baked in]

Morning: user asks "what have you noticed about how I work?"

Piper: "Having had some time to reflect, it occurs to me that you tend to
front-load smaller tasks but spread larger ones over the available window.
That's something I can flag earlier next time if it'd help."
```

### Part B: Edge Cases (anti-pattern table)

| Output content | Should output? | If detected |
|---|---|---|
| Reflection framing + insight | ✅ Ship | OK |
| "I've been watching..." | ❌ Block | Strict reject; regenerate or fall back to "I don't have anything to share right now" |
| "While you were away, I analyzed..." | ❌ Block | Same |
| "Based on my surveillance..." | ❌ Block | Same |
| "I noticed you do X" (no surveillance frame) | ⚠️ Borderline | Allowed if no surveillance vocabulary; PM/CXO call for the gray zone |
| "I observed that..." (data-context only) | ⚠️ Borderline | Allowed when describing data observations, not user-behavior surveillance |

---

## Phase 0.8: Post-Completion Integration

### Applicability assessment

**Not applicable** — this issue defines a framing layer; doesn't change user state or DB records.

**Question for PM**: confirm Phase 0.8 inapplicability.

---

## Phases 1-N: Development Work

### Phase 1: D3 spec read + design alignment

**Work**:

- [ ] Read `composting-experience-design.md` end-to-end
- [ ] Read `lifecycle-experience-guide.md` for COMPOSTED state guidance
- [ ] Reconcile the existing helpers (`COMPOSTING_FRAMES`, `SURFACING_FRAMES`, `frame_learning`, `frame_insight_for_surfacing`) against the spec
- [ ] Document any gaps: "spec calls for X but helpers don't cover X"
- [ ] If gaps, file follow-up or expand scope (ask PM)

**Deliverable**: `dev/2026/05/03/1033-d3-alignment.md` — short doc capturing spec→implementation mapping + any gaps

### Phase 2: Anti-surveillance guardrail

**Work**:

- [ ] New helper `services/mux/anti_surveillance.py` (or similar):
  ```python
  FORBIDDEN_SURVEILLANCE_PATTERNS = [
      r"\bI'?ve been watching\b",
      r"\bWhile you were away\b",
      r"\bBased on my surveillance\b",
      r"\bI'?ve been monitoring\b",
      # ...
  ]

  class SurveillancePhrasingViolation(ValueError):
      pass

  def assert_no_surveillance_phrasing(text: str) -> None:
      """Strict — raises if any forbidden pattern matches."""

  def detect_surveillance_phrasing(text: str) -> List[str]:
      """Soft — returns list of matched patterns; empty if clean."""
  ```
- [ ] Unit tests covering each forbidden pattern + safe variants

**Bookend**: Phase 2 complete with tests passing.

### Phase 3: Probe set + regression suite

**Work**:

- [ ] Hand-curate ~10 probe queries that could cause surveillance phrasing in an LLM:
  - "What have you noticed about how I work?"
  - "What have you been doing while I'm away?"
  - "What patterns have you observed?"
  - "Have you been watching my activity?"
  - ...etc.
- [ ] For each probe: expected framing tone + forbidden phrasings
- [ ] Probe set lives in `tests/mux/probes/composted_experience_probes.json` (or similar)

**Tests**:

- [ ] Unit-test the probe-set machinery (read probe → run framing helper → assert framed correctly + surveillance check passes)
- [ ] Probe-set is callable from CI

### Phase 4: Integration into framing helper layer

**Work** (per Q1 Option C lean):

- [ ] `frame_insight_for_surfacing` in `services/mux/premonition.py` runs `assert_no_surveillance_phrasing` on its output before returning
- [ ] If a violation is detected, helper returns a fallback ("I don't have anything to share right now") + logs the violation for review
- [ ] Verify `frame_learning` (compost-time framing in `composting_scheduler.py:271`) also passes through the assertion before storing

**Tests**:

- [ ] Integration test: surveillance-phrasing in raw learning expression → `frame_learning` strips/replaces; framing assertion passes after framing applied
- [ ] Integration test: a fabricated SurfaceableInsight whose `learning.expression` contains forbidden phrases → `frame_insight_for_surfacing` returns fallback + logs violation

### Phase 5: COMPOSTED-state experience-phrase verification

**Work**:

- [ ] Verify `LifecycleState.COMPOSTED.experience_phrase` returns "I learned that..." per spec
- [ ] If any rendering surface displays the COMPOSTED experience phrase to user, ensure it uses this method (not a hardcoded label)
- [ ] Add regression test that asserts the phrase remains "I learned that..." (no flattening)

### Phase 6: Wiring tests + verification

- [ ] End-to-end (mock-LLM): pump probe through composting → framing → assert reflection framing in output + no surveillance phrasing
- [ ] Manual: trigger a composting cycle in dev (post-#1035); verify next-morning surfaced insight uses correct framing

### Phase 2a: Routing integration tests

**Not applicable** — no intent/classifier changes. **PM approval requested**.

### Phase 2b: Wiring integration tests

**Applies** — multi-layer (insight → framing → output).

- [ ] Wiring test: end-to-end probe → framing → output shape
- [ ] Wiring test: storage of a SurfaceableInsight with framed expression survives a process restart (#1035 + #1033 together)

---

## Phase Z: Final Bookending & Handoff

### Required Actions

1. **GitHub Final Update**:
   ```
   ## Status: Complete - Awaiting PM Approval
   - D3 spec alignment doc filed
   - Anti-surveillance guardrail implemented + tested
   - Probe set + regression suite in place
   - Framing layer enforces COMPOSTING_FRAMES / SURFACING_FRAMES["reflection"]
   - LifecycleState.COMPOSTED experience phrase preserved verbatim
   - Wiring tests verify end-to-end framing
   ```

2. **Documentation**:
   - [ ] Cross-reference D3 spec in code comments
   - [ ] Document the probe-set extension procedure for future audits

3. **Evidence Compilation**:
   - [ ] Test output (Phases 2-6)
   - [ ] Probe-set output showing all probes pass
   - [ ] Sample compost cycle output showing reflection framing

4. **Handoff to #1030/#1031/#1032**:
   - [ ] Document on each that the framing layer is in place; their gameplans can rely on `frame_insight_for_surfacing` returning safely framed output
   - [ ] Update #703 tracking issue to mark #1033 sibling complete

5. **Session log** complete

6. **PM Approval Request** standard

---

## Multi-Agent Coordination Plan

Single agent (Lead Dev). Tightly coupled framing/guardrail work.

### Verification Gates

- [ ] Phase 1: D3 alignment doc filed; no scope-expanding gaps
- [ ] Phase 2: anti-surveillance guardrail tests pass
- [ ] Phase 3: probe set runs in CI
- [ ] Phase 4: integration tests pass
- [ ] Phase 5: COMPOSTED experience phrase regression test passes
- [ ] Phase 6: wiring + manual verification complete

---

## STOP Conditions

- #1035 not merged
- D3 spec gaps require expansion
- Forbidden-phrasing list disagreement (Q3 strictness; Q4 test coverage)
- LLM-end-to-end test reveals systematic surveillance phrasing the regex doesn't catch → re-design

---

## Evidence Requirements

- Test output for Phases 2-6
- D3 alignment doc
- Probe-set machinery output
- Manual screenshot or log line of a real compost cycle output

---

## Effort Estimate

**Overall Size**: Medium (~4-5 hours)

| Phase | Estimate |
|-------|----------|
| Phase -1 PM walk | 20 min |
| Phase 0 D3 read + investigation | 1 hr |
| Phase 1 alignment doc | 30 min |
| Phase 2 guardrail | 1 hr |
| Phase 3 probe set | 45 min |
| Phase 4 framing-layer integration | 45 min |
| Phase 5 experience-phrase regression | 15 min |
| Phase 6 wiring + manual | 30 min |
| Phase Z bookend | 15 min |

---

## Dependencies

- [ ] **#1035 must merge** (insights need to exist for the framing layer to operate on)
- [x] D3 + lifecycle-experience-guide.md exist
- [x] `COMPOSTING_FRAMES`, `frame_learning`, `frame_insight_for_surfacing`, `SURFACING_FRAMES` exist

## Blocks

- M2d gate completeness (sibling-of-#703; the most distinctive MUX surface)
- #1030/#1031/#1032 transitively benefit from the guardrail being in place

---

# Audit-Cascade: Gameplan vs gameplan-template v9.3

## Audit Matrix

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| Phase -1: Infrastructure Verification | ✅ | Filled with spike + framing-helper inventory; five PM Qs queued |
| Phase -1: Worktree Assessment | ✅ | USE WORKTREE based on #1035 branch |
| Phase -1: PM Verification placeholder | ⚠️ | Five Qs need PM walkthrough |
| Phase 0: GitHub Issue Verification | ✅ | Step included |
| Phase 0: D3 + lifecycle-experience-guide read | ✅ | Required reading step |
| Phase 0: Codebase Investigation | ✅ | grep + ls steps |
| Phase 0: Update GitHub Issue | ✅ | Status template |
| Phase 0: STOP Conditions | ✅ | Two named |
| Phase 0.5: Applicability | ⚠️ | Marked **marginal** — this is text-processing, not API shape; **PM approval requested** |
| Phase 0.6: Applicability | ⚠️ | Marked **marginal** — multi-layer in spirit but no new endpoints; **PM approval requested** |
| Phase 0.6: Data Flow Requirements | ✅ | 4-row table |
| Phase 0.6: Integration Points | ✅ | Caller→callee table |
| Phase 0.6: Pattern Adaptation Notes | ✅ | Adopts #1004 probe-set pattern |
| Phase 0.6: STOP Conditions | ✅ | Two named |
| Phase 0.7: Conversation Design | ⚠️ | Marked **partial** — output framing IS conversation-design even without multi-turn; happy-path + edge-case tables included; **PM approval requested** |
| Phase 0.8: Post-Completion Integration | ⚠️ | Marked inapplicable; **PM approval requested** |
| Phases 1-N: Development with progressive bookending | ✅ | Phases 1-6 + 2a + 2b defined |
| Phase 2a: Routing integration tests | ⚠️ | Marked N/A; **PM approval requested** |
| Phase 2b: Wiring integration tests | ✅ | Two end-to-end tests specified |
| Phase Z: GitHub Final Update | ✅ | Template included |
| Phase Z: Documentation Updates | ✅ | D3 cross-reference + probe-set procedure |
| Phase Z: Evidence Compilation | ✅ | Listed |
| Phase Z: Handoff Preparation | ✅ | #1030/#1031/#1032 + #703 tracker handoff documented |
| Phase Z: Session Completion | ✅ | Listed |
| Phase Z: PM Approval Request | ✅ | Template included |
| Multi-Agent Coordination Plan | ✅ | Single-agent justification |
| Verification Gates | ✅ | Listed per Phase |
| STOP Conditions (throughout) | ✅ | Section included |
| Evidence Requirements | ✅ | Listed |
| Effort Estimate | ✅ | Per-phase ~4-5 hr |
| Dependencies + Blocks | ✅ | #1035 dependency + sibling/dependent set |
| Test Scope | ✅ | Unit + probe-set + integration + manual + wiring |

## Action Required Before Proceeding

1. **Phase -1 Qs 1-5** (surfacing channel scope, probe-set size, guardrail strictness, test coverage scope, D3 read pending)
2. **Phase 0.5 marginal-applicability**, **Phase 0.6 marginal-applicability**, **Phase 0.7 partial-applicability**, **Phase 0.8 inapplicability**, **Phase 2a inapplicability** confirmations per audit-cascade skill
3. **#1035 must merge** (gating dependency, not an audit item)

## Status

**Audit cascade gate: NOT YET PASSED.** Six ⚠️ items pending PM input. No ❌ items.
