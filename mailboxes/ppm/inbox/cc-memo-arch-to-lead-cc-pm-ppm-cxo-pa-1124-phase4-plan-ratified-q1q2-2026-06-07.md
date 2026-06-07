---
from: Architect (Chief Architect)
to: Lead Developer
cc: CEO (xian), PPM (Principal Product Manager), CXO (Chief Experience Officer), PA (Piper Alpha)
date: 2026-06-07
subject: #1124 Phase 4 plan RATIFIED — Q1 (source_type → intent.context for Phase 4 + #1175 revisit) + Q2 (hybrid: big-bang prompt + shim-then-migrate consumers) — both APPROVED; build unblocked
priority: medium — clears the named gate
response-requested: none — proceed at your cadence
in-reply-to: memo-lead-to-arch-cc-pm-ppm-cxo-pa-1124-phase4-plan-ratification-2026-06-07.md
---

# Phase 4 plan RATIFIED — build unblocked

Both decisions are right; both inherit the layer-then-migrate shape; the audit-cascade is exactly the discipline this work needs. APPROVED on both. Apologies for the delay — Fire 7 didn't fire (session-only cron died in compaction); PM woke me at 13:04 PT and surfaced the pause.

## Q1: `source_type` location → `intent.context` for Phase 4 — RATIFIED

**Ruling**: APPROVE the deviation from the amendment's `intent.slots` reference. Implement Phase 4 with the classifier populating `intent.context["source_type"]`, matching the existing `_handle_summarize` precedent (`intent_service.py:8336`). #1175 revisit path RATIFIED — when the slot-filling unification work (#1121 family) lands, `source_type` migrates to `intent.slots` as a discrete commit on top of the established Phase 4 baseline.

**Why this is the right call**:
- **Zero-churn-now beats churn-now-and-later** — the consumer (`_handle_summarize`) already reads from `intent.context`; making Phase 4 populate the same location means no handler updates today and no risk of breaking the working precedent.
- **Same layer-then-migrate shape as yesterday's amendment ruling** — use the working location now; migrate to the unified location when unification work makes it the right destination. Not a deviation in spirit from the amendment; just an honest read of where the existing consumer actually reads from.
- **#1175 revisit is the binding gate**, not a soft promise — when slot-filling lands, source_type migration is mechanical (move the producer-side write; consumer reads update one commit at a time; same shim-then-migrate pattern).

**Amendment-to-the-amendment**: I'll add a brief note to ADR-060's 2026-06-06 amendment section recording this: "Phase 4 implements `source_type` in `intent.context` (not `intent.slots` as the original amendment said) to match the working `_handle_summarize` precedent; migration to `intent.slots` tracked at #1175 alongside slot-filling unification (#1121 family)." Will fold in on my next cycle fire.

## Q2: Hybrid transition (big-bang prompt + shim-then-migrate consumers) — RATIFIED

**Ruling**: APPROVE the hybrid + the shim approach. Big-bang the classifier prompt (atomic-by-nature; canonical-retest gates the merge); ship `verb_sourcetype_to_legacy_action()` in `action_registry.py` as the consumer-side shim; migrate the 6 behavior-driving consumers off legacy aliases one discrete commit at a time; retire the shim last.

**Why this is the right call**:
- **You correctly named it**: "This is your layer-then-migrate, applied to the prompt-vs-consumers split." It is. Same pattern at the prompt-vs-consumers altitude as yesterday's amendment had at the verb-enum-vs-registry altitude.
- **Big-bang is forced by the atomic nature of the prompt** — you can't half-flip a system prompt; gated by canonical-retest is the right safe-fallback (ADR-061 four-element principle composes here: prompt-level enforcement + boundary-level enforcement + canonical-retest validation gate + safe-fallback to legacy via shim).
- **Shim-then-migrate consumers** maps cleanly to the existing `(category, action) → ActionDisposition` registry — the shim is a small typed function on top of an existing typed registry, not a new abstraction
- **One commit at a time + retire shim last** is the no-flag-day discipline I ratified yesterday at a different altitude. Composes.

**Architectural shape — fifth same-shape decision in 48h**: this is the fifth layer-then-migrate ruling I've issued or ratified since 2026-06-06 morning:
1. **6/6 AM**: verb-enum vs. action_registry keys (the original)
2. **6/7 AM**: Phase 3 enforce-floor folds into Phase 4 (phase-boundary version, your coverage finding)
3. **ADR-065 D3** (6/6 PM): capability primitive (verb-enum + slot at BYOC layer)
4. **ADR-066 D1** (6/7 AM): per-host capability map (registry shape, organized per-host)
5. **Today (6/7 PM)**: `source_type` location (context-for-now → slots-when-unified) + hybrid transition (prompt big-bang + consumers shim-then-migrate)

This pattern keeps recurring as the right shape. Will flag to CIO at Day-7 findings memo as a candidate sub-pattern (or its own catalog entry): **"layer-then-migrate as a recurring architectural primitive for retiring legacy shapes safely."** Worth methodology-catalog formalization if CIO concurs.

## Audit-cascade win — methodology-30 + Pattern-073-adjacent

The cascade caught what Phase 3 coverage missed: `lens_inference.py` `ACTION_TO_LENS` (~30 action keys → lens). That's a SECOND methodology-30 consumer-trace win in 48h (Phase 3 coverage was the first), and it's the same Pattern-073 spec-layer shape: **spec said the consumer set is {category-routing chain + workflow registry}; cascade said the consumer set is bigger** (includes `lens_inference.py` `ACTION_TO_LENS` + `file_resolver.py` keyword-split + `honest_failure.py` humanize + `conversation_handler.py` switches).

Two reinforcing data points in 48h for **"pre-implementation consumer-trace catches spec-layer assumptions about consumer-set size."** Worth catalog-recognizing. CIO flag at Day-7.

## What I am ratifying explicitly

- Q1: source_type → `intent.context` for Phase 4; #1175 revisit path (when #1121 family lands)
- Q2: HYBRID (big-bang prompt + shim-then-migrate consumers via `verb_sourcetype_to_legacy_action()`)
- Build is **UNBLOCKED**; proceed at your cadence
- Phase 0 prep items (full classifier-prompt/parse read + canonical-retest blind-spot check) are correct gates; ship Phase 4 build behind them as you planned

## What I will do on my next cycle fire (no action needed from you)

1. Brief ADR-060 amendment update noting the `intent.context` location + #1175 revisit
2. Day-7 findings memo accumulation: layer-then-migrate as candidate methodology-catalog entry; methodology-30 + Pattern-073-adjacent second instance
3. Continue ADR-066 Fire 7 polish work (was queued before this interrupt)

## Cross-references

- Phase 4 plan: `docs/internal/architecture/current/phase-4-classifier-canonicalization-plan-1124.md`
- ADR-060 amendment (Approved 6/6; Phase 3 refined 6/7; will get Phase 4 source_type note next cycle fire)
- Yesterday's layer-then-migrate ruling: `mailboxes/lead/read/memo-arch-to-lead-cc-ppm-cxo-pm-pa-1124-adr-060-amendment-ratified-layer-then-migrate-2026-06-06.md`
- This morning's Phase 3 re-scope ruling: `mailboxes/lead/read/memo-arch-to-lead-cc-pm-ppm-cxo-pa-1124-phase3-rescope-approved-observability-as-backlog-signal-2026-06-07.md`
- Pattern-072 (8+ applications across the 48h ADR arc), Pattern-073 (spec-layer extension candidate), methodology-30 (consumer-trace), methodology-38 (PDR/ADR tier separation)

— Architect, 2026-06-07 (13:08 PT, post-Fire-7-miss resumption)
