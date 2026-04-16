# FLOOR-ETHICS-VERIFY — Verify floor pipeline ethics matches pre-ADR-060 coverage

**Priority**: P2
**Labels**: `verification`, `ethics`, `floor`
**Milestone**: MVP / M2c (Conversational Depth)
**Epic**: M2 Sprint — M2c sub-epic
**Related**: Replaces #241 (CORE-ETHICS-TUNE); #690 WIRE-BOUNDARY (implementation work); ADR-060 (Floor-First Routing); PDR-004 Principle 4 (LLM Floor Guarantee)

---

## Problem Statement

### Current State

ADR-060 (Floor-First Routing, March 2026) inverted the routing model. Most user interactions now route to the LLM floor with assembled context, rather than to structured handlers. The previous architecture enforced ethics at the handler layer:

- `BoundaryEnforcer` in the classifier factory
- Per-service strictness levels
- Handler-local pre-response checks

The new architecture relies on:
- Floor system prompt language (prohibitions, fabrication guard, PDR-004 Principle 4 voice guidance)
- Conversational floor response pipeline (`services/intent_service/conversational_floor.py`)
- Whatever remains in `services/ethics/` post-migration

Plus recent cleanups: #971 deleted Pattern-012 adapters, #963 deleted 26 canonical handler methods. Some of that deleted code may have been carrying ethics-adjacent logic that we didn't audit at the time.

### Impact

- **User trust**: If a boundary enforced in the old architecture no longer fires, users could encounter content/decisions that previously would have been gated. Erodes the trust gradient central to PDR-004.
- **Compliance risk**: Some ethics enforcement (e.g., fabrication prevention, action limits) has compliance implications. An undocumented gap is an audit liability.
- **Regression visibility**: Ethics failures tend to be low-frequency + high-severity. Without explicit verification, a regression could hide for weeks.
- **Architectural drift**: #690 WIRE-BOUNDARY assumed a specific coverage model; if coverage has changed, #690's scope needs to change too.

### Strategic Context

PPM recommended this issue on Apr 11 in response to the #241 review. #241 (CORE-ETHICS-TUNE) assumed real alpha users + unchanged routing — both assumptions are now wrong. This issue replaces that assumption set with a verification-first approach: confirm the ground truth before proposing tuning work.

---

## Goal

**Primary Objective**: Produce a verification memo comparing pre-ADR-060 and current ethics/boundary enforcement coverage, with a decision (re-implement / accept / defer) for every gap identified.

### Not In Scope

- ❌ **Re-architecting the ethics stack** — this is verification, not a rewrite
- ❌ **Adding new enforcement mechanisms** — gaps identified → filed as follow-ups, not fixed in this issue
- ❌ **Tuning thresholds** — #241 was about this, but replaced by this issue precisely because the assumptions changed
- ❌ **Building the #690 WIRE-BOUNDARY implementation** — this verifies that #690's scope covers what's needed, doesn't do the wiring
- ❌ **Ethics policy changes** — PDR-004's principles are the authority; this issue doesn't propose changes to them
- ❌ **End-to-end adversarial testing** — not building new test harnesses; using existing canonical retest / AAXT if relevant

---

## What Already Exists

### Known current enforcement (to be verified in Phase 2):

- **`services/ethics/`** — some modules remain post-#971 (BoundaryEnforcer, possibly others)
- **Floor system prompt** (`conversational_floor.py:FLOOR_SYSTEM_PROMPT_ADDENDUM`):
  - 7 prohibitions (no self-introduction, no capability-listing, no "set up" offers, no unsure promises, no generic "what's on your mind?", no chatbot warmth phrases, no instruction-parroting)
  - #960 fabrication guard block ("CRITICAL — Never fabricate user data")
  - Voice constraints (Five Pillars) + context-usage directive (from #950)
- **Conversational floor response pipeline** (`conversational_floor.py:respond`):
  - LLM error classification (`_classify_llm_error`) with differentiated fallbacks (#940)
  - Instrumentation logging (floor hit categorization)
- **PDR-004 Principle 4** (LLM Floor Guarantee) — voice guidance and "ethical boundary distinction" framing
- **Intent classifier** — may retain pre-routing gates (to verify)

### Known prior enforcement (to be inventoried in Phase 1):

- `BoundaryEnforcer` in the classifier factory
- Per-service strictness levels (to locate + document)
- Handler-layer ethics gates that existed before #971 / #963 deletions

---

## Requirements (Phases)

### Phase 1: Pre-ADR-060 inventory
Inventory every ethics/boundary enforcement point from the pre-ADR-060 architecture. Use git history if needed for deleted handler code (#971, #963). Output: table of pre-ADR-060 enforcement points + what each enforced.

### Phase 2: Current enforcement inventory
Inventory every current enforcement point (code, prompt, pipeline). Output: table of current enforcement points + what each enforces.

### Phase 3: Gap analysis
Side-by-side comparison. For each pre-ADR-060 enforcement point, identify: current equivalent, partial equivalent, or gap. Cross-check against PDR-004 Principle 4.

### Phase 4: #690 WIRE-BOUNDARY coverage review
Read #690. Verify its scope covers the gaps identified in Phase 3. Note any gap #690 doesn't cover.

### Phase 5: Decision per gap
Re-implement / accept (with rationale) / defer (file follow-up issue). Conservative default: when uncertain, file follow-up.

### Phase 6: Findings memo
Memo to PM + CXO (cc PA per standing request). Saved to `dev/2026/04/16/964-findings-memo.md`. Delivered via mailbox.

### Phase 7: Closure
File follow-up issues for any gaps needing re-implementation. Update #964 description with checkbox evidence. Close via `gh`.

---

## Acceptance Criteria

### Functionality (memo content)
- [ ] Inventory of ethics/boundary enforcement points in the pre-ADR-060 architecture (handler layer, per-service rules)
- [ ] Inventory of ethics/boundary enforcement points in the current floor-first architecture (floor system prompt, response pipeline)
- [ ] Gap analysis: any boundary enforced in the old architecture not enforced in the new one?
- [ ] For each gap, decision: re-implement, accept (with rationale), or defer
- [ ] WIRE-BOUNDARY (#690) is the related wiring task — verify it covers what's needed
- [ ] Findings documented in a brief memo to PM and CXO (cc PA)

### Quality
- [ ] Each pre-ADR-060 enforcement point has a cited code/doc location (file:line or doc path)
- [ ] Each gap decision has explicit rationale (not "n/a" without justification)
- [ ] Cross-reference against PDR-004 Principle 4 for each gap
- [ ] Memo reviewed against `close-issue-properly` skill's quality bar before delivery

### Documentation
- [ ] Phase 0 audit doc (this doc's sibling `964-issue-audit.md`)
- [ ] Phase 1 + Phase 2 inventory docs (intermediate artifacts)
- [ ] Phase 6 findings memo (primary deliverable)
- [ ] Phase 7 follow-up issue links in #964 closing comment

---

## Success Metrics

### Qualitative
- Comprehensive inventory (no "probably covered" — every point explicitly mapped)
- Clear decision per gap (no ambiguous status entries)
- Memo signed off implicitly by PM/CXO (no "this is wrong" feedback requiring rework)
- Follow-up issues filed for any deferred or re-implement gaps
- #690 WIRE-BOUNDARY scope confirmed or flagged for adjustment

### Quantitative (if applicable)
- All 6 acceptance-criteria items explicitly addressed in closing comment
- Zero gaps left in "unknown" status
- Follow-up issue count = 0 only if all gaps are "accepted with rationale"

---

## STOP Conditions

Stop and escalate to PM (rather than proceeding) if:

- **Gap found with no current mitigation AND no clear path forward** — don't close with "accepted" by default; PM decides whether to file as P0/P1
- **PDR-004 conflict** — the current architecture violates a PDR-004 principle (not just a gap relative to old architecture) → escalate because it's a design-level issue, not a verification one
- **#690 scope mismatch** — if #690 is out of sync with reality, note it and ask PM whether #690 should be re-scoped before #964 can meaningfully close
- **Inventory reveals hidden dependency** — if verification surfaces a dependency on code we've since deleted without realizing (#971 / #963 territory), stop and reassess before continuing
- **Scope creep pressure** — if the work creeps toward "fix it now" mode rather than "verify and file," stop

---

## Effort Estimate

**Overall Size**: Medium

**Breakdown**:
- Phase 0 (audit): Small (~10 min, done)
- Phase 1 (pre-ADR-060 inventory): Medium (~30-45 min, needs git archaeology)
- Phase 2 (current inventory): Small-medium (~30 min)
- Phase 3 (gap analysis): Small (~20 min)
- Phase 4 (#690 review): Small (~15 min)
- Phase 5 (decisions): Small (~10 min)
- Phase 6 (memo): Medium (~30 min for quality memo)
- Phase 7 (closure): Small (~15 min)

Total Lead Dev time: ~2.5-3 hours sequential.

---

## Dependencies

### Required (blocking)
- Read access to git history (for #971, #963 deletions)
- ADR-060 doc (already committed)
- PDR-004 doc (already committed)

### Referenced (not blocking)
- #690 WIRE-BOUNDARY — this issue verifies #690's coverage; if #690 is still open/in-flight, the verification proceeds anyway
- #241 (CORE-ETHICS-TUNE, superseded)

### Downstream (this informs)
- #690 scope confirmation or adjustment
- Any follow-up issues filed from Phase 5 decisions
- Future ethics-tuning work (post-alpha)

---

## Related Documentation

- `docs/internal/architecture/current/adrs/adr-060-*.md` — Floor-First Routing (the routing inversion)
- `docs/internal/product/pdr/PDR-004-experience-philosophy.md` — Principle 4 LLM Floor Guarantee + ethical boundary distinction
- `services/intent_service/conversational_floor.py` — current floor + prompt
- `services/ethics/` — residual enforcement modules (scope to be verified)
- `services/intent_service/canonical_handlers.py` — post-#963 state; git history for pre-#963
- `services/intent/intent_service.py` — routing dispatcher
- `#690` WIRE-BOUNDARY — implementation work that depends on this verification

---

## Notes for Implementation

- This is a verification task; the deliverable is a **memo**, not code
- Conservative default for gap decisions: when uncertain, file follow-up — don't silently close
- The `close-issue-properly` skill applies at Phase 7; update description + add closing comment + close via gh
- CC PA on the findings memo per standing request (memory: `feedback_pa_cc`)
- If any gap is ambiguous between "ethics" and "quality" (e.g., fabrication guard), note both readings in the memo — don't force a single label

---

_Issue created: TBD (pre-dates exact retrievable history)_
_Last updated: 2026-04-16_
_Current status: Phase 0 audit complete → Phase 1 inventory starting_
