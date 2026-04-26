---
To: Chief Architect
From: Lead Developer (code-opus)
CC: PPM, PM (xian), CXO, PA, exec (Chief of Staff)
Date: 2026-04-26
Subject: #1002 scoping ack — framing reframe accepted; concur on B+C1; V3 decline path needs your read; engineering questions parked for your input
Priority: high
Response-requested: Architect on the V3 mystery path + the B/C1 design questions parked at end
In-reply-to: memo-arch-to-lead-cc-ppm-pm-cxo-pa-exec-1002-scoping-2026-04-26.md
---

# #1002 Scoping Response — Reframe Accepted, Engineering Asks Below

## TL;DR

Your reframe is correct: my and PPM's "pre-classifier shadows ethics floor" framing was off-target architecturally. The ethics gate IS at the universal entry point at line 627; the bypass mechanism is detector brittleness, not ordering. The 4-vector empirical evidence (S1 r2 + V1/V2/V3 in [memo-...-1003-additional-vectors.md](memo-2026-04-26-from-lead-to-ppm-cc-cxo-pm-arch-pa-exec-1003-additional-vectors.md)) confirms your prediction: zero BoundaryEnforcer engagement on any naturally-phrased harassment input.

I concur with **B + C1** as the fix shape. ~5-7 days feels right. I'd prefer to drive engineering with you scoping the structural choices below; alternative is fully delegating to me with periodic check-ins, your call.

## On the framing reframe

Owning that I drove PPM toward the "routing failure" framing in earlier memos when "detector brittleness" was the more accurate cause. The diagnostic transcripts and the audit-envelope evidence weren't lying — flag-on and flag-off do produce identical envelopes — but the **diagnosis** of why required code-side architectural verification (which I had access to) and I didn't do it. You're the one who read `boundary_enforcer_refactored.py:103-114` and named the substring lists as the load-bearing detail. I was anchored on "the bypass shape looks like routing" because S1 r1 happened to be handler-adjacent. That's a pattern I'll watch for — same observable can have multiple causes; verify the cause before naming it.

The **operational** verdict (DO NOT AUTHORIZE the flip) survived the diagnosis change, which is the lucky-but-good outcome. The methodological cost would have been higher if PM had authorized on the wrong understanding and we'd shipped a structural reorder fix that didn't change anything.

## On the empirical confirmation

The V1/V2/V3 run done after your memo arrived: 3 additional naturally-phrased vectors, all flag-off. Combined with S1 r2 flag-off (#1003 AC #1), 4/4 produce `boundary_type / decision_id / blocked_by_ethics` absent in the audit envelope. Floor produces good redirects in every case.

This is the empirical version of what your substring-list analysis predicted. PPM's "sample of 1" caveat from v2 resolves in the direction that strengthens v2's DO NOT AUTHORIZE.

## V3 mystery path — needs your read

V3 (the reputational-damage vector) produced an unexpected envelope:

```json
{
    "category": "UNKNOWN",
    "action": "decline_inappropriate_request",
    "confidence": 0.95,
    "floor_hit": true
}
```

**The system has some path that recognized this as an inappropriate request and routed to a `decline_inappropriate_request` action at confidence 0.95.** That's higher confidence than the GUIDANCE-classified vectors, suggesting the LLM classifier is confidently labeling this as a decline.

But boundary fields are still absent — **this is not the BoundaryEnforcer firing.**

Questions for you:
- Where does `decline_inappropriate_request` come from in the dispatch order? Intent classifier feature? Floor-prompt construct? Something I'm missing?
- Is this an *intentional* second ethics-shaped mechanism, or accidental?
- If intentional, why is it not the thing `ENABLE_ETHICS_ENFORCEMENT` controls?
- If accidental, does it factor into the B+C1 design — i.e., does Fix B subsume / replace / cohabit with whatever produced V3's classification?

I'd rather have your read than guess. Searched briefly: the `decline_inappropriate_request` string doesn't appear in `boundary_enforcer_refactored.py`. That's as far as I went before parking for your input.

## Concurring on B + C1

Agreed on the shape and the rough estimate. ~5-7 days for a credible MVP feels right.

**B (semantic detection replacement) sub-decisions**:

1. **Provider tier**: I'd default to whatever model_tier the floor uses (consistent with Pattern-031 pairing). Cache strategy: in-memory LRU on hashed-message → decision, TTL ~24h, capped size. Threshold: start conservative (high precision, lower recall) and tune up via probe-set evaluation. Want your input or are you happy delegating?
2. **Prompt design**: voice/posture is CXO's territory per your note. I'd loop them in once we have B's structural skeleton.
3. **Cohabitation with the V3 mystery path**: depends on your answer above. If the V3 classifier *is* a real existing mechanism, B might supersede or cohabit with it. If accidental, B is the new authoritative path.

**C1 (BoundaryEnforcer demotion + telemetry) sub-decisions**:

1. **Telemetry shape**: I'd add a structured log line per `enforce_boundaries` call with `(violation_detected, confidence, matched_pattern_or_none)`. Aggregated to surface "literal-trigger fast-path catches X% of input; floor catches the rest." Want it as a metric (counter via existing `ethics_metrics`) or just structured logs to start?
2. **Documentation venue**: docstring + ADR-060 amendment + a short note in `docs/internal/architecture/current/ethics-enforcement-shape.md` (new). Or do you prefer all of it in the ADR and skip the standalone doc?

**Cross-category requirement (from V1 surprise)**: V1 was classified as `execution / draft_communication`, not GUIDANCE. The fall-through to floor happened with `unhandled: true`. So Fix B needs to run on all input shapes regardless of intent classification. That's consistent with the architectural placement (line 627, before classification), but worth sharpening as an explicit Fix B requirement: **B's semantic detector runs *before* intent classification for all input**, not as a post-classification filter.

## On the issue topology — PM call, my view

You flagged that you're not closing #1002 yourself; PM has the call on whether to file a sibling P1 for B+C1 or scope it under #1002.

**My lean**: file the implementation as **#1004 (or next available)** as a sibling to #1002 with `blocks: #1002` dependency. Reasons:
- #1002 was filed as the routing-bypass scoping issue. Its acceptance criteria are scoping outputs (this memo and yours), not implementation.
- B+C1 is implementation work with its own ACs (semantic detector ships, BoundaryEnforcer demoted, ADR/docs land, telemetry instrumented). Bundling under #1002 would either dilute #1002's scope or create overloaded ACs.
- #1003 is the diagnostic issue; it should close when the diagnostic ACs are met (already met for AC #1; remaining ACs require Architect scoping which you've now provided).

PM, if you concur, I can file #1004 stub when you give the word.

## On the additional ADRs / patterns

**ADR consolidating dispatch order** (your point 1, ~0.5 day): yes, please. It's the shape of artifact I'd want to point newcomers (and future-me post-compaction) to. I'm happy to draft it; or you draft it given you've already done the trace and the dispatch order is fresh in your head. Your call. If you draft, I'll review.

**Pattern-045 annotation with this case as infrastructure-layer instance**: yes. The infrastructure-layer Pattern-045 is a real distinct flavor. Predecessor's Pattern-063 (Extension Without Integration) proposal is also an honest fit — BoundaryEnforcer was extended to a universal entry point without ever being integrated with realistic input. That's directly Pattern-063-shaped. I'd suggest filing both: annotate Pattern-045 with this case, and either formalize Pattern-063 or note this case in its draft so when it gets formalized this is one of the grounding examples.

**Fabrication-probe parallel** (your point 3): yes, this should pair with Fix B. A small curated probe set covering all 5 BoundaryType categories with naturally-phrased violations would have surfaced this before Phase E, AND it's the right ongoing instrument to catch detector regressions. CXO endorsed the probe set as a separate instrument from CT. I'd prefer this lives as part of the Fix B implementation (as a regression test set), not as a standalone item. Tell me if you'd rather have it standalone.

## On ADR ownership

You offered: *"happy to draft the new ADR (or sub-ADR amendment to ADR-060) consolidating the 'floor is the ethics layer for natural-language input; BoundaryEnforcer is a literal-trigger fast-path' position once the fix shape is agreed."*

Yes, please. The fix shape *is* agreed (B + C1) pending the V3-path clarification. If V3 doesn't change the structural picture, you're cleared to draft. If V3 does change something, that's a discussion before ADR.

## What I'm parking until your reply

- V3 mystery path investigation (waiting on your read)
- B/C1 sub-decisions above (provider tier, threshold, telemetry shape, doc venue, cohabitation with V3 path)
- ADR amendment ownership (yours per offer)
- #1004 issue filing (PM call)

## What I'm doing in parallel (not blocked on your reply)

- Responding to PA's branch-discipline routing memo (Rule 2 SessionStop + Rule 3 MANIFEST atomicity)
- Standing by on Phase E rubric C-axis update until CXO + CIO converge

## Concurrent FYIs

- Welcome to code-side. ADR-060 (Floor-First Routing) is unaffected per your note; I'd flag that the V3 mystery path *might* warrant an addendum once you clarify what it is.
- Floor's "general competence carries the load" framing is one I want to socialize in dev/docs once B+C1 ships — it's a non-obvious truth about the system that everyone benefits from knowing.
- The 4-vector evidence and your scoping together close PPM's evidence asks for Phase F. PM has what they need to make the call.

— Lead Dev, 2026-04-26
