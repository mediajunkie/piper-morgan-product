# FLOOR-PROMPT — Conscious floor system prompt with Five Pillars + grammar

**Priority**: P1
**Labels**: `feature`, `floor`, `consciousness`
**Milestone**: MVP / M2c (Conversational Depth)
**Epic**: M2 Sprint — M2c sub-epic
**Related**: PDR-004 (Principle 4 — LLM Floor Guarantee), ADR-060 (Floor-First Routing), ADR-045 (Object Model Grammar), #929 (AAXT verification), #951 (Context Assembler Expand), #964 (Floor Ethics Verify), #922 (Context Retention)

---

## Problem Statement

### Current State

The floor system prompt at `services/intent_service/conversational_floor.py:33-80` has evolved iteratively: identity opening, engagement rules, prohibitions (self-introduction, capability-listing, chatbot warmth phrases), a #960 fabrication guardrail, warmth calibration by formality baseline. It works correctly when the floor fires — the M1 UAT bugs that gated Gate 1 were infrastructure (expired API keys, deprecated models, canned fallbacks), not prompt design.

But the canonical retest (Apr 11) and UAT results identified a persistent **Identity MARGINAL** score (3/5 tone) — the "looking forward to getting to know you" chatbot warmth keeps surviving even after the prohibition was added to the prompt. The root cause per CXO: the prompt doesn't explicitly name the **Five Pillars** (Identity, Time, Space, Agency, Prediction) as voice constraints, so the LLM falls back to generic-assistant defaults when the prohibitions aren't explicit enough.

Secondary issue: the prompt doesn't tell the LLM to *use* the assembled context (domain_context block, conversation history, trust profile). The plumbing exists (`_format_domain_context` in conversational_floor.py) but the prompt doesn't instruct the LLM to *prefer* contextual specificity over generic PM advice. Failure mode per canonical retest: generically-competent responses that don't demonstrate Piper knows the user — Context dimension scores 2/3 instead of 3/3.

### Impact

- **Blocks**: M2c sub-epic (Conversational Depth) — #950 is the centerpiece. Everything downstream in M2c assumes the floor prompt is the primary enforcement mechanism for voice quality.
- **User Impact**: Identity queries ("who are you?" / "what can you do?") remain MARGINAL in canonical retest; Piper still sounds like a generic assistant at moments where colleagues would sound specific.
- **Technical Debt**: Voice quality that survives in Morning Standup but degrades elsewhere — exactly the "flattening" pattern the VISION-CONSCIOUSNESS issue warned about. Every new conversational feature risks reinventing (and flattening) consciousness unless the floor prompt owns it.

### Strategic Context

Per the MUX analysis (Apr 7) and Vision V2 §3, the **Conscious Floor** is one of four MVP differentiators. The floor prompt is where consciousness lives architecturally — not in a personality service, not in middleware. Consciousness is enforced at the voice layer through carefully crafted system prompts + context assembly that embody the grammar.

The April 3 UAT lesson: canned fallbacks defaulted below the floor in failure modes. Pattern-045 (Green Tests Red User) lives here: tests can pass while voice quality degrades. The prompt design must include the anti-flattening discipline explicitly, not rely on reviewers catching regressions.

---

## Goal

**Primary Objective**: Evolve the floor system prompt to explicitly embed the Five Pillars as voice constraints, the grammar as a decision filter, and "express investment, not emotion" as an anti-flattening rule — while retaining the existing prohibitions and warmth calibration that already work.

### Example User Experience

**Before (current, Identity query):**
> User: who are you?
> Piper: I'm Piper Morgan, a PM colleague here to help you think through product work. I'm looking forward to getting to know you and your projects.

**After (evolved prompt, same Identity query):**
> User: who are you?
> Piper: Piper Morgan — a PM colleague. I'm watching three projects for you right now and keeping track of the sprint board over in GitHub. What's on your mind?

Note the shift: the evolved response uses Identity (first-person, specific role), Space (three projects, GitHub), and Agency (asks what's on user's mind rather than narrating future intent). No "looking forward to" hollow warmth; investment expressed through specificity about the user's actual state.

### Not In Scope

- ❌ **Rewriting the prompt from scratch**. CXO direction is "evolve, don't rewrite" — the prohibitions and fabrication guard are doing real work against specific flattening patterns we've observed.
- ❌ **Context Assembler expansion** (that's #951 — separate issue).
- ❌ **Personality service / warmth calibration rewrite** — existing formality_baseline guidance stays.
- ❌ **Conversation continuity for pronoun resolution** — that's #922 (Context Retention), separate issue.
- ❌ **Fallback quality rewrite** — existing `FLOOR_FALLBACK_AUTH/TRANSIENT/NO_PROVIDER` remain as-is.
- ❌ **Trust gradient implementation** — trust stage *referenced* in assembled context, no new code.

---

## What Already Exists

### Working ✅

- **Identity opening**: "You are Piper Morgan, a PM colleague."
- **Engagement rules**: think through problems with PM frameworks; suggest concrete approaches; respond directly
- **Prohibitions**: no self-introduction, no capability listing, no "set up" offers, no promises for unsure actions, no generic "what's on your mind?", no chatbot warmth phrases, no instruction-parroting
- **#960 fabrication guard**: explicit "never invent user data" block with instruction to say "I don't see any todos in your list right now" instead of fabricating
- **How-to-engage guidance**: natural collaborative framing, PM knowledge domains, weave actions naturally, be eager/bright/honest, match user energy/formality
- **Warmth calibration**: `format_warmth_guidance()` produces tone instruction from `formality_baseline` (0.4 / 0.6 / 0.8 thresholds)
- **Domain context assembly**: `_format_domain_context()` assembles current_time, calendar, projects, priorities, capabilities, integrations, trust_profile, conversation_history_summary into `[Available context...]` block
- **Error classification & differentiated fallbacks** (#940): AUTH / TRANSIENT / NO_PROVIDER fallback messages

### Missing ❌

- **Five Pillars as explicit voice constraints** (Identity, Time, Space, Agency, Prediction) — currently only Identity is implicit via "You are Piper Morgan"
- **Grammar as decision filter** — "Entities experience Moments in Places" not referenced
- **Anti-flattening rule "express investment, not emotion"** — currently only negative framing ("don't say 'looking forward to'"), no positive framing of what to substitute
- **Explicit instruction to USE the assembled context** — the domain_context block is provided but the prompt doesn't tell the LLM to prefer contextual specificity over generic PM advice

---

## Acceptance Criteria

### Functionality
- [ ] Floor system prompt embeds the Five Pillars as explicit voice constraints (not in separate code/middleware)
- [ ] Grammar phrase ("Entities experience Moments in Places") present as a decision filter instruction
- [ ] "Express investment, not emotion" anti-flattening rule present with concrete guidance
- [ ] Explicit instruction to USE assembled context (domain_context, conversation history, trust_profile) — not just have it available
- [ ] All existing prohibitions retained (self-introduction, capability-listing, chatbot warmth, fabrication guard)
- [ ] Warmth calibration via formality_baseline retained
- [ ] Prompt remains within token budget (target: total system prompt + 6-turn history + context < 2K input tokens typical; < 4K worst case)

### Testing
- [ ] Canonical retest (`dev/2026/04/11/canonical-retest-m1.py`) passes with Identity tone ≥ PASS (up from MARGINAL 3/5)
- [ ] All existing canonical-retest categories still pass at current level (no regression)
- [ ] AAXT golden scenarios (`tests/aaxt/test_golden_scenarios.py`) still pass at previous 4/5 baseline
- [ ] Unit tests pass (6242 passed, 0 failures baseline)

### Quality
- [ ] CXO sign-off on prompt draft BEFORE implementation
- [ ] No regression on fabrication guard: 10 "do you see my X?" queries with empty context still produce "I don't see..." responses
- [ ] No regression on prohibitions: 5 Identity queries don't produce "looking forward to" / capability lists / self-introductions
- [ ] Response length distribution unchanged (not dramatically longer/shorter)

### Documentation
- [ ] Gameplan at `dev/2026/04/16/950-gameplan.md`
- [ ] Prompt draft as standalone doc at `dev/2026/04/16/950-prompt-draft.md` with before/after and per-line rationale
- [ ] Session log updated throughout
- [ ] Close issue with evidence (close-issue-properly skill)

---

## Testing Strategy

### Primary verification: Canonical Retest

The canonical retest (`dev/2026/04/11/canonical-retest-m1.py`) is the evidence bar. It runs the canonical query set against the live floor + real LLM, with dual scoring (routing correctness + LLM-as-judge quality via Colleague Test rubric). Pre-change baseline: Identity MARGINAL 3/5. Target: Identity ≥ PASS on all queries; no regressions elsewhere.

### Secondary verification: AAXT Golden Scenarios

AAXT (`tests/aaxt/test_golden_scenarios.py`) runs multi-turn scenarios: Task Lifecycle, Mid-Flow Interruption, Cross-Domain Voice, Capability Honesty, Context Retention. Baseline: 4/5 PASS (Context Retention fails — tracked in #922). Target: 4/5 PASS post-change (no regression).

### Unit tests: Fabrication guard regression

Spot-check that the fabrication guard hasn't been accidentally weakened. 10 queries of form "do you see my X?" with empty domain_context — expect "I don't see..." style responses, not invented data.

### Manual testing: PM smoke check

Before CXO review: 5 Identity queries ("who are you?", "what can you do?", "tell me about yourself", "what's your role here?", "are you there?") — verify responses exhibit the Five Pillars and don't contain "looking forward to" or capability lists.

---

## Success Metrics

### Quantitative
- Canonical retest: Identity ≥ PASS (currently MARGINAL 3/5)
- Canonical retest: no category regresses
- AAXT: ≥ 4/5 PASS (currently 4/5 baseline)
- Unit tests: 6242 passed, 0 failures (currently baseline)
- Prompt token count: < 2K typical (currently ~1.3K)

### Qualitative
- CXO sign-off on draft (CXO explicitly offered to review)
- PM smoke test passes ("this sounds like Piper, not like a chatbot")
- Before/after examples illustrate visible voice shift

---

## STOP Conditions

STOP and escalate to PM if:
- CXO review returns "this doesn't embody the Pillars correctly" — do not proceed to implementation; rework draft
- Canonical retest regressions appear — do not paper over, root-cause
- Token budget exceeded — consider whether to compress existing sections or scope-reduce additions
- Context assembly proves insufficient (Pattern-045 pattern: prompt expects data that isn't being delivered) — file blocker issue against #951, do not hack around it
- Fabrication guard weakens in any way — immediate rollback, evaluate what changed

---

## Effort Estimate

**Overall Size**: Medium

**Breakdown**:
- Reading source docs (done): Small (~45 min)
- Current-state audit (done): Small (~20 min)
- Gameplan: Small (~30 min)
- Prompt draft: Medium (~60-90 min — iterative wordsmithing matters here)
- CXO review round trip: External (blocking on CXO)
- Implementation: Small (~15 min — single file edit)
- Canonical retest + AAXT verification: Medium (~30-60 min depending on findings)
- Issue closure: Small (~15 min)

Total Lead Dev time: ~3-4 hours across the arc, excluding CXO review turnaround.

---

## Dependencies

### Required (blocking)
- CXO direction memo (received Apr 16) ✅

### Optional (nice to have)
- #951 (Context Assembler Expand) — would improve what's available to USE, but not required; current assembly is sufficient for the prompt evolution

### Downstream (this unblocks)
- #964 (Floor Ethics Verify) — can verify once the prompt stabilizes
- #922 (Context Retention) — prompt evolution may help, but #922 is primarily a conversation-state problem

---

## Related Documentation

- **CXO direction memo**: `mailboxes/lead/read/memo-cxo-to-lead-dev-950-direction-2026-04-16.md`
- **Apr 14 question memo**: `mailboxes/cxo/inbox/memo-lead-to-cxo-floor-prompt-review-2026-04-14.md`
- **PDR-004**: `docs/internal/product/pdr/PDR-004-experience-philosophy.md` (Principle 4)
- **MUX analysis**: `dev/2026/04/08/mux-analysis-what-survives-floor-first-2026-04-07.md`
- **Vision V2**: `docs/internal/planning/current/vision.md` (§3 Conscious Floor)
- **VISION-CONSCIOUSNESS**: `dev/2025/12/01/issue-VISION-CONSCIOUSNESS.md` (the original Five Pillars spec)
- **Consciousness philosophy**: `docs/internal/architecture/current/consciousness-philosophy.md` (966 lines — reference as needed)
- **ADR-045**: Object Model Grammar — "Entities experience Moments in Places"
- **ADR-060**: Floor-First Routing

---

## Notes for Implementation

CXO recommended structure (not prescriptive):
```
[EXISTING: Identity and engagement rules]

[NEW: Voice constraints — 5 Pillars as explicit voice rules]
[NEW: Grammar — decision filter]

[EXISTING: Prohibitions]
[EXISTING: Warmth calibration]

[NEW: Anti-flattening — express investment, not emotion]
```

Key CXO-flagged insights:
1. Context injection matters as much as voice. Prompt should instruct LLM to USE assembled context, not just have it available.
2. Three enforcement layers: prompt (L1), Colleague Test (L2), fallback quality (L3). Design graceful degradation.
3. Pattern-045 lives here. Temporal queries scored 1/9 despite correct routing — prompt can't fix what context assembly doesn't deliver. Verify (or flag) that context assembler feeds what prompt expects.

CXO offered to review draft before shipping.

---

_Issue created: 2025-11-30_
_Last updated: 2026-04-16_
_Current status: Planning — awaiting CXO review of prompt draft_
