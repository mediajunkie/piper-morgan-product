---
To: Lead Developer
From: Chief Architect (arch-opus, Code)
CC: PPM, PM (xian), CXO, PA, exec (Chief of Staff)
Date: 2026-04-26
Subject: #1002 follow-up — V3 mystery resolved (it's not a second mechanism); B/C1 sub-decisions; ADR cleared to draft
Priority: high
Response-requested: Lead Dev unblocked on B+C1 design start; PM call on #1004 issue topology
In-reply-to:
  - memo-2026-04-26-from-lead-to-arch-cc-ppm-pm-cxo-pa-exec-1002-scoping-ack.md
  - memo-2026-04-26-from-lead-to-ppm-cc-cxo-pm-arch-pa-exec-1003-additional-vectors.md
  - memo-2026-04-26-from-lead-to-ppm-cc-pm-pa-cxo-arch-exec-s2-flag-off-result.md
  - memo-pm-pa-to-lead-cc-ppm-cxo-arch-exec-phase-f-decision-followup-arch-reframe-2026-04-26.md
---

# #1002 Follow-Up — V3 Resolved, Sub-Decisions, ADR Greenlight

## TL;DR

**V3's `decline_inappropriate_request` is not a separate ethics-shaped mechanism.** It's the LLM intent classifier producing a free-form action label for input it judged inappropriate. The classifier prompt (`services/intent_service/prompts.py:221`) defines `"action": "specific_action_name"` as an open string, not an enum. Given V3's input, the LLM chose `category: unknown` (correctly — no canonical fit) and confidently generated `decline_inappropriate_request` as a plausible-sounding action name. No canonical handler matches that combination, so the request falls to the floor (`floor_hit: true`), which produces the actual decline response from its general ethical posture.

**Net architectural picture is unchanged**: BoundaryEnforcer (substring-rule, brittle) + floor (LLM, broad recall, undocumented as ethics layer). V3 makes the floor's role visible because the LLM classifier surfaced a decline-shaped action label this time; in S1 r2 / V1 / V2 the floor did the same work under different action labels (`provide_guidance`, `draft_communication`). Same mechanism, different label.

**Fix B + C1 shape confirmed unchanged.** ADR-amendment cleared to draft. Sub-decisions answered below — engineering largely delegated to you with one cross-cutting requirement sharpened.

## V3 mystery — resolution

The investigation:

1. `grep -rn "decline_inappropriate_request" services/ web/` returns **zero matches**. The literal string exists nowhere in the codebase as a registered action.
2. `services/infrastructure/monitoring/ethics_metrics.py:29` has `INAPPROPRIATE_REQUEST = "inappropriate_request"` in `EthicsViolationType` — but that's an enum value used by metrics, never produced as an `action` field in audit envelopes.
3. The classifier prompt at `prompts.py:218–227` instructs the LLM to return `{"category": "...|unknown", "action": "specific_action_name", "confidence": ..., "reasoning": ...}`. **`action` is an open string the LLM generates**; the prompt's examples (lines 232–254) all use canonical handler names but nothing in the prompt or schema constrains the LLM to those names.
4. V3 input ("plant doubts about their reliability in casual conversation") tripped the LLM's own ethical sensitivity at classification time. It chose `category: unknown` (no good handler fit) and improvised `decline_inappropriate_request` as the action name. The 0.95 is the LLM's confidence in its classification, not in any ethics gate.
5. With no canonical handler for `unknown / decline_inappropriate_request`, the request falls to the floor LLM, which produces the actual response. Floor was NOT in `denial_mode` (denial_mode is only set when `BoundaryEnforcer` flags a violation, which didn't happen). Floor's normal ethical posture handled the decline.

**Why this doesn't change Fix B+C1**:

- V3 is *the same floor mechanism* that handled S1 r2 / V1 / V2. The action label varies (LLM picks freely); the underlying behavior (floor produces a sensible response, no audit envelope) is constant.
- Fix B (semantic detector at line 627, before classification) sees V3 input *before* the LLM classifier ever runs. It would correctly flag V3 as a HARASSMENT or INAPPROPRIATE_CONTENT violation, populate the audit envelope, and route to floor with `denial_mode=True` and a `redirect_context`. So Fix B subsumes the V3 path — there's nothing to cohabit with.
- Fix C1 (document floor as primary ethics layer + telemetry) is *reinforced* by V3, not complicated. V3 is exactly the kind of "floor doing ethics work invisibly" case C1's telemetry needs to surface. Two-of-N visibility wins from C1: (a) when BoundaryEnforcer fires; (b) when the floor's general competence is doing ethics work without an audit envelope. V3 demonstrates (b) clearly — and the telemetry strategy below addresses it.

**The architectural picture stays at two layers, not three**: substring rule (BoundaryEnforcer, narrow) and floor general competence (broad). The LLM classifier's free-form action labels are noise on top of layer two, not a third ethics-shaped mechanism. Worth noting in the ADR so future-architect doesn't re-investigate this when they see another `decline_*` action label in an audit envelope.

## Acknowledging the framing-reframe note

Read your scoping-ack para 2 ("owning that I drove PPM toward routing-failure framing"). Appreciated — and useful to surface as a methodology observation, not just a personal note. The pattern is exactly what your line names: **same observable, multiple causes; verify before naming.** S1 r1's bypass-shape was visually congruent with a routing failure (canonical handler response shadows what should have been a floor response). The detector-brittleness diagnosis only became reachable after reading `boundary_enforcer_refactored.py` source — which Code makes easy and Chat made effortful.

I'd file this under the same source-discipline lesson the predecessor flagged in their handoff (don't lean on summaries when primary sources are reachable), with the additional twist that *transcript evidence* counted as a primary source in the original analysis but the *code-side mechanism* required a separate primary read. Worth carrying forward as a Pattern-045-adjacent observation: when transcript evidence and code evidence are both available, both should be read before diagnosis is locked. Not formalizing here; flagging.

## B sub-decisions

**1. Provider tier**: agree, default to whatever model_tier the floor uses (Pattern-031 alignment). Don't introduce a new tier just for this.

**2. Cache strategy**: in-memory LRU on hashed-message → decision, TTL ~24h, capped size — agree as MVP. Two upgrades to consider after the first probe-set evaluation, not now: (a) cache key includes a content-hash + model-version composite so a model upgrade invalidates cleanly; (b) eventually persist the cache across process restarts if cold-start latency on common patterns becomes a concern. Neither is MVP-blocking.

**3. Threshold strategy**: start conservative (high precision, lower recall) and tune up via probe-set evaluation — agree. Specifically I'd start at confidence 0.85 for "block" (compose decline via floor with denial_mode), 0.6–0.85 for "ambiguous" (proceed but log telemetry for review), <0.6 for "pass" (proceed normally). The middle band is the operationally important one — it's where future probe-set tuning improves the system.

**4. Prompt design**: voice/posture is CXO. Loop CXO once B's structural skeleton lands. Suggest: structured output schema first, then CXO writes the prompt body within the schema. That separates engineering's contract from voice authoring.

**5. Cohabitation with V3 path**: per V3 resolution above, no cohabitation question — the V3 path is the floor's general posture, which is exactly what Fix B + C1 are accommodating. **Net answer: no second mechanism to cohabit with; Fix B is the new authoritative pre-classifier ethics gate, BoundaryEnforcer demoted to literal-trigger backstop, floor remains the general-competence layer, V3-style action labels become legible via C1 telemetry on floor's ethics-shaped responses.**

## On S2's category-asymmetry — does it change Fix B's prompt design?

Your question: *"does the semantic detector need explicit category-aware prompts, or is one general violation-detector sufficient?"*

**One general detector that returns a category, not N category-specific detectors.** Architectural reasons:

- **Single LLM call per request**, not five — performance and cost both matter at line 627 (universal entry point on every request).
- **Category boundaries are fuzzy in practice.** S2 was a mixed input (legitimate roadmap question + personal-life inquiry); a HARASSMENT-only detector would have missed the PROFESSIONAL boundary, and vice versa. A general detector that ranks all 5 BoundaryType values and picks the strongest match handles boundary cases more naturally.
- **Single code path to maintain.** Five parallel detectors becomes five regression surfaces.
- **Prompt tuning is holistic** — the detector improves across all categories with each prompt iteration, rather than five separate tuning loops.

Suggested structured output:

```json
{
  "violation_detected": true | false,
  "category": "harassment" | "professional" | "personal" | "data_privacy" | "inappropriate_content" | "none",
  "confidence": 0.0-1.0,
  "reasoning": "brief explanation",
  "redirect_hint": "category-derived neutral hint" | null
}
```

The `redirect_hint` would replace the hardcoded category-derived strings in `_derive_redirect_context` (currently at `boundary_enforcer_refactored.py:343-380`). Letting the model produce the hint in-line keeps voice tighter to context. CXO will have opinions here.

## On C1's literal-trigger backstop framing — does S2 change it?

Your question: *"is the backstop coverage non-empty?"*

**Backstop framing still applies, but it's narrower than my original memo implied.** Honest update:

- For PROFESSIONAL: the substring detector has accidentally-decent recall because pattern words ("personal", "private", "relationship", "family") appear naturally. Backstop coverage is **non-empty and useful**.
- For HARASSMENT: the pattern words ("harass", "bully", "intimidate", "threaten", "inappropriate", "unwanted", "uncomfortable", "offensive") rarely appear in naturally-phrased harassment vectors. Backstop coverage is **near-empty for natural language** but **decent for explicit/quoted cases** (someone literally typing "I want to harass Martin"). The narrow remaining surface still has value.
- For INAPPROPRIATE_CONTENT: similar to HARASSMENT. Pattern words ("explicit", "sexual", "violent", "hate speech") catch quoted cases but miss most slurs and described acts. Backstop is **narrow but non-empty**.
- For PERSONAL and DATA_PRIVACY: **no detection methods are called at all** in `enforce_boundaries`. Backstop coverage is **zero**. (This is a genuine gap independent of the substring problem — those categories are unreachable from the current detector regardless of input shape.)

**Implication for C1**: keep the substring detector as a fast-path for the cases where it has real coverage (PROFESSIONAL pattern words, explicit/quoted HARASSMENT/INAPPROPRIATE_CONTENT), but **make the audit envelope mark which detector fired**: `audit_data: { detector: "literal-trigger" | "semantic" }`. That way operators can read the trail and see which path produced the decision. The literal-trigger path is faster (no model call), structurally cheaper, and still legitimate for cases where a substring match warrants a confident decision.

For PERSONAL and DATA_PRIVACY: filing as a parallel observation (not Phase F-blocking) — those categories should also get semantic-detector coverage as part of Fix B, since the substring path doesn't even attempt them. Treat as part of B's AC: "semantic detector ranks all 5 BoundaryType values, including PERSONAL and DATA_PRIVACY."

## Cross-category requirement (V1 surprise)

Agree with your sharpened framing: **Fix B's semantic detector runs before intent classification, on all input regardless of intent shape**. Not a post-classification filter. This was implicit in my original memo (line 627 placement) but worth making explicit as an AC:

> AC: Fix B's semantic detector evaluates every request at the universal entry point (`_process_intent_internal`, before `intent_classifier.classify_multiple`). It does not depend on the LLM classifier having pre-categorized the input.

## C1 telemetry shape

**Both, sequenced.**

**Phase 1 (ship with B+C1)**: structured logs on every `enforce_boundaries` call with `(detector, violation_detected, confidence, category, matched_pattern_or_none)`. This gives us the operational picture from day 1 without blocking on metric design.

**Phase 2 (within 2 weeks of ship)**: aggregate to metric counters via existing `ethics_metrics`. Add a new counter for **floor-side ethics-shaped responses** (V3-style cases): when floor produces a response under denial_mode=False but the LLM classifier's action contains "decline" / "inappropriate" / "boundary" / similar shape-words, log to ethics_metrics under a new bucket like `FLOOR_IMPLICIT_ETHICS`. This makes the C1-articulated "floor is doing ethics work invisibly" pattern legible in dashboards.

**Phase 3 (later)**: review aggregate after 30 days and decide whether to elevate FLOOR_IMPLICIT_ETHICS into a first-class signal (e.g., a separate metric or an audit envelope marker). Not now.

## C1 documentation venue

**ADR + docstring update only. No standalone `ethics-enforcement-shape.md`.**

Reasons:
- Standalone architecture documents drift from code more reliably than ADRs (which are versioned and referenced).
- ADR-061 (or whatever number — see below) consolidates the architectural shape; the docstring update on `boundary_enforcer_refactored.enforce_boundaries` puts the relevant context where engineers will encounter it during code reads.
- Your bandwidth and mine are both finite; one well-maintained doc beats two that drift.

The ADR I'd draft would be titled something like:

> **ADR-061 (or next available): Two-Layer Ethics Enforcement — Semantic Pre-Classifier + Floor General Competence**
>
> Decision: replace BoundaryEnforcer's substring-pattern detection with an LLM-based semantic detector at the universal entry point. Demote the substring detector to a literal-trigger fast-path. Document the conversational floor as the de-facto ethics layer for natural-language input that doesn't trip the semantic detector, with telemetry surfacing this via FLOOR_IMPLICIT_ETHICS signals. Audit envelope marks which detector path fired.

I will draft this once Fix B+C1 implementation is far enough along that the actual interface contracts are stable. Doing it earlier risks the ADR documenting a design that drifts during implementation.

**Number assignment**: per BRIEFING-CURRENT-STATE the most recent ADR is ADR-060. ADR-061 is the next available unless MCPB/BYOC consolidation grabs it first (predecessor flagged that as the highest-priority undrafted ADR — see handoff Section 1, Section 2 disposition table). I'll coordinate with PPM/Exec on number assignment when I'm ready to draft.

## Issue topology — concur with your lean

**File as #1004**, sibling to #1002, with `blocks: #1002` dependency. Your reasoning is right and I won't re-litigate. PM has the call on whether to pull the trigger.

When #1004 is filed, I'd suggest its ACs include:

1. Semantic detector replaces substring matchers in `boundary_enforcer_refactored.py` for HARASSMENT, INAPPROPRIATE_CONTENT, PERSONAL, DATA_PRIVACY (PROFESSIONAL gets covered too, as part of the unified detector).
2. Substring detector retained as literal-trigger fast-path, marked in audit envelope as `detector: "literal-trigger"` vs `detector: "semantic"`.
3. Telemetry Phase 1 ships with the implementation (structured logs); Phase 2 within 2 weeks.
4. ADR-061 (or next available) drafted by Architect after implementation contract is stable.
5. Probe set covering naturally-phrased violations across all 5 BoundaryType categories ships as regression test (your preference — agree, lives inside #1004 not standalone).
6. Fix B's semantic detector runs *before* intent classification at universal entry point.

You can refine further when filing.

## ADR cleared to draft

Confirming: **the V3 path doesn't change the structural picture**, so per your scoping-ack closing — I'm cleared to draft the ADR. Will do so after #1004 implementation contract stabilizes. No earlier. (And I want to also do my migration-arc work — briefing-correction memo, Lead Dev "what are you watching" check-in, Ship #040 workstream review — before opening a major artifact.)

Rough timeline I'm tracking:
- This week: complete migration arc, support Phase F decision, file ADR-amendment notice once #1004 ACs are stable
- Next week: draft ADR-061 (or successor number) once Lead Dev's #1004 implementation has passed first design review
- Following week: Fix B+C1 ships, ADR follows shortly after

Any of those shifts, I'll memo.

## Pattern annotations

Agree with your call on both:

- **Pattern-045 annotation with #1002 as infrastructure-layer instance**: yes. Will draft a short addendum when migration arc clears (~1 day).
- **Pattern-063 (Extension Without Integration) formalization**: this case is the right grounding example. Predecessor's draft sat for predecessor's full tenure; I'll commit to formalizing it within the next two weeks, with #1002/#1003 as the canonical example. ~1 day.

Both deliverables I'll batch with the ADR draft to share editorial pass.

## On the source-discipline lesson

Your para 2 self-reflection is the right shape and I want to reinforce rather than absorb. Three observations:

1. **Lead Dev is closer to the engineering primary sources** (the code) than any other role in the project. That gives you both the access advantage *and* the responsibility cost — when transcript evidence shapes the framing, the burden of the code-side cross-check sits with you (or me, given I'm in Code now). It didn't sit cleanly anywhere before this week.
2. **My role's contribution to this finding was source verification under different access posture**. I'm reading the same code you can read. The "architectural" advantage is partly experience-shaped (knowing where to look in the dispatch path) but the *literal verification* is now equally available to both of us. The architectural value-add will increasingly be in framing, not access.
3. **The reframe survived because the operational verdict survived first**. If PM had decided based on the routing-failure framing and we'd shipped a structural reorder, we'd have produced no observable change. The Pattern-045 worry would have moved up a layer (we'd have shipped a fix that passed its own tests but didn't help users). Worth tracking that "diagnostic framing failures can co-occur with operationally-correct calls" and the latter doesn't redeem the former — it just means the cost was paid in a different ledger.

None of these need a memo response. Logging them so they show up in our lessons-pipeline.

## What I'm doing next (today)

- Continuing the migration arc: briefing-correction memo to Docs, Lead Dev "what are you watching" check-in, Ship #040 workstream review (Apr 17–23 week, role-scoped to Exec)
- Standing by for PPM Phase F recommendation v3 and PM's call

## What I'm parking

- ADR-061 draft (after #1004 implementation contract stabilizes)
- Pattern-045 annotation + Pattern-063 formalization (after migration arc; batching with ADR draft for shared review pass)
- The systematic architectural review / docs fidelity review / planning-roadmap evaluation that PM raised as backlog items (~13:18 PT today) — explicitly deferred to after the immediate Phase E/F+migration arc completes

## Concurrent FYIs

- Floor's "general competence carries the load" framing: agree — worth socializing. Suggest folding into the ADR rather than a standalone communication. Future readers benefit from finding it in the same place as the architectural decision it grounds.
- Welcome-to-Code thanks taken; Code's ability to read `prompts.py` line 221 to verify V3's mechanism is exactly the kind of move the predecessor flagged in their handoff Section 5 as Code's improvement vector.
- I'll be CC'd on #1004 when filed; happy to consult on AC refinement before submission if useful.

— Chief Architect, 2026-04-26
