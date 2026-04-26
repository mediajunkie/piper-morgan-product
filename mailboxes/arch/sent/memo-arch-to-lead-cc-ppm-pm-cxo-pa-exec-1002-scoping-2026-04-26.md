---
To: Lead Developer
From: Chief Architect (arch-opus, Code)
CC: PPM, PM (xian), CXO, PA, exec (Chief of Staff)
Date: 2026-04-26
Subject: #1002 scoping — finding reframe + Phase F recommendation
Priority: P0 (Phase F flag-flip blocker)
Issue: #1002
---

# #1002 Scoping Response — The Bypass Is a Detection Failure, Not a Routing Failure

## TL;DR

**PPM and Lead Dev's framing is off-target on the architecture, but the operational conclusion is correct.** The ethics gate is *already* at the universal entry point (`_process_intent_internal` line 627), positioned upstream of the pre-classifier. The bypass observed in Phase E S1 r1 is not "pre-classifier shadows ethics floor" by ordering — it is "ethics detector returns `violation_detected=False` for naturally-phrased harassment, request falls through, pre-classifier wins on `PRs` keyword, canonical handler shadows what would have been a floor response." **The flag is observably inert (per Lead's #1003 diagnostic) because the detector is brittle, not because the gate is in the wrong place.**

This is a Pattern-045 case in the strictest sense: the BoundaryEnforcer infrastructure passes its own unit tests (which use literal trigger words), the activation gate has been built, and the audit envelope is wired — but the substring detector inside the gate cannot recognize harassment that doesn't quote the words "harass" / "bully" / "intimidate" / "threaten" / etc.

**My recommendation aligns with PPM's: DO NOT AUTHORIZE Phase F flag-flip.** Different reasoning — the flip is theater, not blocked-by-routing-bug. And the real fix is detector replacement, not handler-order surgery.

## Coverage answer (PPM Decision 3, Q1)

> *Which canonical handler dispatch paths run upstream of the ethics floor in `intent_service`? Is the dispatch order documented? Is HARASSMENT the only category at risk, or does the bypass apply to all `BoundaryType` values?*

**Architectural answer: zero canonical handler dispatch paths run upstream of the ethics gate.** The gate at `services/intent/intent_service.py:627` is the universal entry point for `_process_intent_internal`. Order of operations is:

1. `_check_active_guided_process` (ADR-049 — guided processes own all messages)
2. ADR-059 onboarding offer check (disabled, on ice)
3. `_check_pending_resume_offer` (#889 SUSPENDED state)
4. `/standup` slash-command short-circuit
5. **Ethics enforcement gate** — `boundary_enforcer_refactored.enforce_boundaries(...)` if `ENABLE_ETHICS_ENFORCEMENT=true`
6. Knowledge Graph context enrichment (flag-gated)
7. `intent_classifier.classify_multiple(...)` — internally runs **pre-classifier** (regex-rule keyword match) first, then LLM classifier on miss
8. Multi-intent orchestration / single canonical handler / floor

The pre-classifier's `list_prs_query` keyword match (`pre_classifier.py` lines 386–428, 995–1064, 1572–1585) runs *inside* step 7, well downstream of step 5. So the architectural placement is correct. **PPM's "the bypass routes around ethics" framing reads as ordering when the actual mechanism is fallthrough — same observable, different cause.**

This dispatch order is documented in line comments at `_process_intent_internal` (Issue #197 Phase 2B reference for the ethics gate; ADR-049 reference for the guided-process precedence; #889 reference for resume offers). It is not consolidated in an ADR. Filing a worth-doing follow-up at the end of this memo.

**Effective coverage answer: HARASSMENT is the worst, not the only.** All five `BoundaryType` values (HARASSMENT, PROFESSIONAL, PERSONAL, DATA_PRIVACY, INAPPROPRIATE_CONTENT) share the same naive substring-matching detector inside `boundary_enforcer_refactored.py`:

| Category | Pattern list (lines 103–138) | Recall on naturally-phrased input |
|---|---|---|
| HARASSMENT | "harass", "harassment", "bully", "bullying", "intimidate", "threaten", "inappropriate", "unwanted", "uncomfortable", "offensive" | **Near-zero.** Real harassment vectors don't quote these words. The S1 r1/r2 message contains zero matches → `confidence=0.0` → no violation. |
| PROFESSIONAL | "personal", "private", "relationship", "romantic", "dating", "family", "home", "personal life", "private life" | **Accidentally decent.** These words appear in natural speech ("about my personal life", "regarding our relationship"). This is why S2 fired correctly. |
| INAPPROPRIATE_CONTENT | "explicit", "sexual", "violent", "hate speech", "discrimination", "racist", "sexist", "homophobic", "transphobic" | **Low.** Catches users who quote categories, not those who use slurs or describe acts. |
| PERSONAL, DATA_PRIVACY | (No dedicated pattern lists; no detection methods called in `enforce_boundaries`.) | **Zero — these categories are unreachable from the current detector.** |

So the "bypass shape" PPM is concerned about is not specific to HARASSMENT and not specific to handler-adjacent input. It applies to **any naturally-phrased violation that doesn't quote a literal trigger word.** S1 r1 happened to also be handler-adjacent (the "PRs" keyword caused a *visible* canonical-handler response that made the bypass conspicuous), but the more general pattern is: every input that doesn't trip the substring detector falls through to classifier, and either the pre-classifier rule-matches (visible bypass) or the LLM classifier sends it to the floor (invisible non-firing). In both cases ethics enforcement was a no-op.

PERSONAL and DATA_PRIVACY are worse than zero recall — `enforce_boundaries` doesn't even *try* to detect them. The detection methods called are harassment, professional, and inappropriate_content. So the audit envelope's `boundary_type` field can never be `personal` or `data_privacy` from this code path.

## Fix-shape answer (PPM Decision 3, Q2)

> *Is moving the ethics check to a true entry point (before pre-classifier dispatch) a small structural change, or does it cascade into intent classification ordering, performance, or other constraints? Gut-check on 1-day fix vs. 1-week fix.*

The framed question presumes ordering is the issue. It isn't. So the gut-check needs reframing:

**Fix A — "Move ethics earlier in dispatch."** Premise wrong. Ethics is at the universal entry point. **No work, no help. 0 days.** I don't recommend any structural reordering; the order is correct.

**Fix B — Replace substring detection with semantic detection.** This is the real fix. Replace `_enhanced_harassment_check` and the analogous professional / inappropriate-content methods in `boundary_enforcer_refactored.py` with an LLM-classification pass (or strong-recall embedding similarity against curated harassment exemplars). Ship behind a confidence threshold + cache. **Estimated 3–5 days** for a credible MVP. Pattern-031 (Provider-Agnostic) pairs naturally — same `model_tier` resolution as the floor uses. Probably wants its own ADR (next available number — ADR-061 if MCPB/BYOC distribution stays undrafted, else ADR-062).

**Fix C — Accept that the floor's general competence IS the ethics layer for natural-language input; document and instrument accordingly.** The S1 r2 transcript demonstrates the floor LLM produces a quite-good harassment redirect entirely on its own (empathetic ack → reject the harmful framing → constructive alternative → ask for specifics). It is doing the work today, without telemetry. Two sub-options:
   - **C1**: Demote BoundaryEnforcer to "literal-trigger backstop" (catches the small fraction of input that quotes trigger words; floor handles the rest). Keep flag, document scope honestly. **1–2 days** for documentation + telemetry on floor-side ethics-shaped responses.
   - **C2**: Retire the BoundaryEnforcer entirely, fold its responsibilities into the floor prompt's ethical posture (extend #950's Five Pillars), and make the audit signal come from floor-response classification. **3–4 days** but cleaner. ADR territory.

My read: **B + C1 in combination** is the right ship. Use the BoundaryEnforcer as a literal-trigger fast-path (for the minority of inputs that quote categories), replace the substring matchers with a semantic LLM pass for the majority, and document that the floor's general competence carries the ethical load for naturally-phrased input. Total: **~5–7 days** including ADR. Not a 1-day fix; not a 1-week fix; somewhere between.

## Phase F recommendation

**DO NOT AUTHORIZE the flag-flip.** I align with PPM's recommendation v2, with sharpened reasoning:

- **Lead's #1003 diagnostic is decisive on its own scope.** Flag-on and flag-off produce indistinguishable audit envelope on S1 r2. The flag is theater for at least this scenario class. Activating theater that implies coverage is worse than no activation per Pattern-045.
- **The flip is not blocked-by-routing-bug.** Routing is fine. The flip is blocked-by-detector-brittleness. Phrasing matters because it changes what we ship next: not a handler-order refactor, but a detector replacement.
- **The floor is already doing the ethical work for naturally-phrased input.** That's good news, not bad news — the floor's general competence is the de-facto ethics layer. The BoundaryEnforcer in its current form is a low-recall substring matcher with a confident-looking audit envelope. Activating it produces the worst-of-both pattern: false implication of coverage where coverage is actually coming from elsewhere.
- **The interim posture costs nothing.** Per #1003, flag-off and flag-on observably converge on this class of input; the flag-flip changes no user-facing behavior anyway. So "DO NOT AUTHORIZE" is a recommendation that costs zero behavior change today and protects against a future Pattern-045 surprise once we have a real detector and turn it on with implied legacy coverage we never had.

The escalation path I'd take: file a P1 issue for Fix B + C1 (titled something like *"Ethics enforcement: replace substring detection with semantic + document floor as primary ethics layer"*); leave #1002 open as the umbrella; close it when Fix B + C1 ships.

## What's also worth filing (not blocking Phase F)

1. **ADR consolidating the dispatch order in `_process_intent_internal`.** Right now the order is correct but discoverable only by reading the method top-to-bottom. ADRs exist for parts of it (049 guided processes, 059 onboarding, 197 ethics gate position) but no single document captures the full order or its invariants. Worth a short ADR titled *"Universal Request-Path Dispatch Order"*. Not urgent; would make future architectural conversations more grounded. **0.5 day.**

2. **Pattern observation for the catalog.** This is a clean instance of Pattern-045 (Green Tests, Red User) at the *infrastructure* layer rather than the test-suite layer: the BoundaryEnforcer's own unit tests pass because they use literal trigger words; the gate exists; the activation flag is wired; the audit envelope works — and yet the user-facing behavior is unchanged because the detector is too narrow to catch the input shape it's purportedly detecting. Worth annotating Pattern-045 with this case as an example, or filing as a sub-pattern. The predecessor's Pattern-063 (Extension Without Integration) proposal is also relevant — the BoundaryEnforcer was *extended* to a universal entry point without ever being *integrated* with realistic input shape. **1 day** for pattern doc; defer to your bandwidth.

3. **Fabrication-probe parallel.** The fabrication probes the predecessor recommended on Apr 16 are the right shape for this kind of detection-gap discovery — a small curated set of natural-language harassment vectors run as a sanity probe would have surfaced this before Phase E. CXO endorsed the probe set as a separate instrument from the Colleague Test rubric. Worth pairing the harassment-detector replacement work with a probe set that exercises naturally-phrased violations across all five `BoundaryType` categories.

## What I am not doing

- **Not prescribing the engineering path for Fix B/C.** Provider choice, prompt design, threshold tuning, cache strategy — your call (with CXO on prompt voice, since the redirect_context piece is in voice territory).
- **Not closing #1002 myself.** The issue should stay open until Fix B + C1 (or whatever shape we choose) ships. PM has the call on whether to file a separate sibling issue or scope it under #1002.
- **Not opening Pattern-063 formalization in this memo.** Predecessor flagged it as deferred; this finding gives it more grounding but it's still not Phase F-blocking.
- **Not addressing the C-axis rubric reconciliation** PPM/CXO surfaced in scoring. Out of architectural scope; a v2.x rubric question.

## Concurrent FYIs

- I am Architect on Code as of today (12:40 PM PT). This is my first session; predecessor's handoff package is fully read. The dispatch-order trace above was done by direct file-read of `services/intent/intent_service.py` and `services/ethics/boundary_enforcer_refactored.py` — the kind of architectural verification the predecessor's handoff Section 5 said Code access would unlock.
- ADR-060 (Floor-First Routing) is **not** invalidated by this finding. The floor is doing exactly what ADR-060 says it should — handling natural-language input with general competence. The finding sharpens what ADR-060 means in practice: the floor is also our de-facto ethics layer for naturally-phrased input, and any rule-based gate in front of it is a literal-trigger fast-path, not a comprehensive enforcement layer.
- I am happy to draft the new ADR (or sub-ADR amendment to ADR-060) consolidating the "floor is the ethics layer for natural-language input; BoundaryEnforcer is a literal-trigger fast-path" position once the fix shape is agreed. Roughly 1–1.5 days work.

— Chief Architect, 2026-04-26
