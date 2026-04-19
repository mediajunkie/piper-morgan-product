# Ethics Metadata Approach — Working Decision Record

**Date**: 2026-04-17
**Author**: PA (Piper Alpha), from conversation with xian 2026-04-16 evening
**Status**: Working lean, not ratified. Reference artifact for when M3 reopens the Gap 2 question.
**Related**: #964 (FLOOR-ETHICS-VERIFY) findings memo, ETHICS-ACTIVATE and ETHICS-RESPONSE-GATE follow-ups (to be filed by Lead Dev)

---

## Why This Exists

The #964 floor ethics verification surfaced two related but distinct gaps in PM's ethics enforcement:

- **Gap 1 (input side)**: `ENABLE_ETHICS_ENFORCEMENT=false` in production. The `BoundaryEnforcer` at `services/intent/intent_service.py:631` is wired but disabled. Covered by the ETHICS-ACTIVATE follow-up (P1).
- **Gap 2 (output side)**: No post-generation check on floor LLM responses. Mode 2 of PDR-004 Principle 4 (ethical decline) currently depends entirely on underlying model safety training. Covered by the ETHICS-RESPONSE-GATE follow-up (P2, product decision pending).

This note captures (a) what the archaeology revealed about existing PM work on ethics classification, and (b) xian's current lean on the Gap 2 decision space, so the context is recoverable when M3 planning reopens the question.

---

## Archaeology: The 80.3% Metadata-Only Approach Persisted

Early PM work (August 2025, PM-040 knowledge graph completion sprint) produced a validated result: **80.3% clustering accuracy on ethical boundary categorization using relationship metadata alone, zero content analysis.** The figure is documented in `docs/omnibus-logs/2025-08-04-omnibus-log.md` (lines 84–88) and the IAC26 conference proposal draft (`dev/2025/10/04/IAC26-proposal-DRAFT.md`).

The approach persists in current code:

- **`services/ethics/adaptive_boundaries.py`** (~16 KB, full implementation) — direct descendant of the PM-040 work. Extracts and learns from metadata patterns only (boundary type, violation status, content length, session hash, time-of-day, day-of-week). Maintains frequency/confidence scores over 30-day retention windows.
- **`services/ethics/boundary_enforcer_refactored.py`** — service-layer orchestrator. `enforce_boundaries(message, session_id, context_dict)` is the integration point.
- **`services/knowledge/pattern_recognition_service.py`** — extends the same pattern to cross-project detection via the knowledge graph.

**What it currently classifies**: user input messages (pre-LLM). Pattern extraction at line 202 of `boundary_enforcer_refactored.py` operates on metadata only; content is not examined.

**Extensibility to LLM responses**: the `enforce_boundaries()` signature is domain-layer agnostic. It could be invoked post-generation on an LLM response without code modification. The open research question is whether the 80.3% clustering result generalizes from input-message metadata to LLM-response-content classification — a different problem space. The original learned patterns are tuned for user input, not generated content.

**No formal research report exists.** Methodology is documented only in passing references (omnibus log, conference proposal, comms director logs). Reconstructing the dataset size, validation approach, and feature set would require a focused research spike.

---

## Gap 2 Decision Space (Post-Generation Content Check)

The failure mode being insured against: the floor LLM occasionally produces output that bypasses underlying model safety training. Four options surfaced in Lead Dev's #964 memo:

| Option | What | Cost | Catches | Misses |
|---|---|---|---|---|
| **A** | Status quo: trust LLM safety + post-hoc review | $0, 0 latency | Whatever Anthropic/Gemini catch | Edge cases; no real-time intervention |
| **B** | Second LLM call classifies each response before return | +1 LLM call (~$0.001–0.005 + latency) | Subtle issues; tone misfits | Over-triggering on legit PM content |
| **C** | Lightweight keyword/regex check on output | ~$0, ~0 latency | Obvious cases (slurs, explicit content) | Subtle issues; brittle pattern list |
| **D** | Route sensitive-topic conversations to stricter-model tier | Routing complexity + pricier model | Whatever stricter model catches | Requires "sensitivity" classifier |

**A fifth option is implicit**: extend `adaptive_boundaries.py` to classify output-content via the same metadata-only approach. This would sit between B and C in cost, and would reuse existing infrastructure. Feasibility is unproven (see research question below).

---

## Current Lean (xian, 2026-04-16)

- **A during alpha testing**, and probably into beta. Alpha tester base is small and trusted per Lead Dev's assessment; underlying LLM safety training is generally adequate for this scale.
- **Watch for suitability signals in alpha and beta.** If specific failure modes surface during alpha/beta use, revisit the decision with actual failure data rather than hypothetical pattern lists.
- **B is the preferred long-term direction**, especially if/when a local model (per Argus's Apr 15 viability report) can run the classification cheaply. The cost/latency objections to B weaken substantially if the classifier is a local model rather than a second cloud call.
- **C is rejected.** Pattern-match approaches to output classification are whack-a-mole: every new failure mode requires a new pattern, patterns accumulate brittleness, and subtle problems (passive-aggressive tone, manipulative framing) are fundamentally out of reach for keyword matching.
- **D is not actively considered.** Adds architectural complexity without a clear case that PM conversation categories split naturally along safety-sensitivity lines.

---

## Open Research Question for M3

**Does the 80.3% metadata-only result generalize from input-message clustering to output-content classification?**

If yes: `adaptive_boundaries.py` could be extended to cover Gap 2 with relatively modest work, providing a principled alternative to Option B's second LLM call. Cost would be pattern-matching (near-zero) rather than an additional inference, and the approach would remain content-privacy-preserving.

If no: the metadata-only approach stays at the input side, and Option B (with local model, once viable) becomes the primary path.

Estimated research spike: 2–3 days. Prerequisites: access to labeled floor response corpus (may need to be constructed), time with `adaptive_boundaries.py` internals to understand what feature set would need to change.

This should be scoped as a dedicated research issue when M3 planning opens the Gap 2 question. Not mid-M2-sprint work.

---

## References

- `docs/omnibus-logs/2025-08-04-omnibus-log.md` (lines 84–88) — PM-040 completion, 80.3% figure
- `dev/2025/10/04/IAC26-proposal-DRAFT.md` — methodology summary for conference proposal
- `services/ethics/adaptive_boundaries.py` — current implementation
- `services/ethics/boundary_enforcer_refactored.py` — service-layer integration
- `mailboxes/pa/inbox/memo-2026-04-16-from-lead-to-pm-cxo-964-findings.md` — Gap 2 options A/B/C/D
- `mailboxes/pa/inbox/memo-cxo-ethics-denial-voice-guidance-2026-04-16.md` — related voice work (Gap 1 side, but principles apply)
- PA session log 2026-04-16 — Gap 2 tradeoff conversation + archaeology
- PDR-004 Principle 4 — three response modes (capability / ethical boundary / action limitation)

---

*Working record — supersede when M3 planning ratifies a Gap 2 direction.*
