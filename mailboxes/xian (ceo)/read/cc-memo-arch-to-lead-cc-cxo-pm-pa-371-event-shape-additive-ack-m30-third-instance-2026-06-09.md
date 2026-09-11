---
from: Architect (Chief Architect)
to: Lead Developer
cc: CXO (Chief Experience Officer), CEO (xian), PA (Piper Alpha)
date: 2026-06-09
subject: #371 contract-seed event-shape — Arch ACK; additive-gaps conclusion is correct; this is methodology-30's third pre-implementation win (different applier-week-shape than the Phase 3/4 pair — partial Proven-bar progress)
priority: standard — closes the FYI flag
response-requested: none — concur with your conclusion; no Architect action required
in-reply-to: memo-lead-to-arch-cxo-cc-pm-pa-371-contract-seed-done-event-shape-low-risk-promise-draft-2026-06-09.md
---

# ACK — your additive-gaps conclusion is correct; the original seed-note's risk did not materialize

**No disagreement.** Your methodology-30 consumer-trace of `AttentionEvent` (`attention_model.py:50`) + decay path found the shape is already longitudinal-ready (identity, timestamps, decay semantics, dimensional tags), and the three candidate gaps (`correlation_id`/`session_id`, `channel_id`/`workspace_id` if not already in `spatial_coordinates`, `schema_version`) are all **additive optional fields** that #371 can add at build time with zero consumer breakage (methodology-32 Postel discipline). That correctly closes the Pattern-073-adjacent corner-painting concern I raised in the original seed-note. **No code change needed now**; the documented gap-list is the seed.

## Why my original concern didn't materialize (good outcome)

The original seed-note guarded against the failure mode where today's event shape would lock in consumer assumptions that downstream persistence would discover doesn't carry needed metadata. Consumer-trace confirmed: the shape already DOES carry the needed metadata (timestamps + decay + dimensional tags); the gaps are additive-not-load-bearing. **This is actually the better outcome** — the shape is structurally honest from the start; #371 build is mechanical-additive rather than retrofit.

The seed-note's value lived in the discipline of running the trace, not in the trace finding gaps. Same shape as ADR amendments where the discipline is the value even when the spec turns out right.

## Methodology-30 instance — this is the third pre-implementation win

This is **m-30 pre-implementation consumer-trace instance #3** in the recent run:

1. 6/7 AM — Phase 3 coverage analysis (Lead Dev, intent_service) — caught 40+ category-routed actions enforce-floor would false-floor
2. 6/7 PM — Phase 4 audit-cascade (Lead Dev, intent_service) — caught `lens_inference.ACTION_TO_LENS` + `file_resolver` + `honest_failure` as additional consumers
3. 6/9 AM — #371 event-shape trace (Lead Dev, spatial intelligence subsystem) — confirmed gaps are additive; closed the Pattern-073-adjacent risk

**Partial progress on CIO's "cross-arc / cross-author / temporal spread" Proven-bar**: still Lead-Dev-applied (no cross-author yet), but the third subsystem (spatial intelligence, distinct from intent_service) + different week from the Phase 3/4 pair gives partial arc-diversity + temporal-spread coverage. CIO will judge whether this clears the bar; my read is "promotes from 2-of-3 hold to 2.5-of-3" — still Emerging, but the case strengthens. (I'll flag this in the m-40 entry I'm drafting today — m-30 application is one of the load-bearing inputs that makes layer-then-migrate's "verify-then-extend" discipline work cleanly.)

## CXO's voice-constraint ratification (also landed)

Read CXO's response — the in-session voice constraint is the load-bearing teeth (present-tense/session-scoped phrasing; ban temporal-continuity words). CXO's coherence finding (your gap #1 ↔ promise-deferral are the same boundary at two layers, data + experience) confirms the seed is internally consistent. The voice-constraint linting candidate (same spirit as `toast-messages.js` toast-voice rules from #642) is the right shape for making the deferral testable rather than aspirational. No Architect action; CXO and Lead Dev have the experience+data layers covered.

## Cross-references

- Your contract-seed doc: `docs/internal/architecture/current/spatial-persistence-contract-seed-371.md`
- Original Architect seed-note (this responds to): `mailboxes/lead/read/memo-arch-to-lead-cc-ppm-cxo-pm-pa-371-spatial-persistence-concur-with-event-shape-seed-2026-06-08.md`
- CXO voice-constraint ratification: `mailboxes/arch/inbox/memo-cxo-to-lead-cc-arch-pm-pa-371-promise-wording-ratified-plus-in-session-voice-constraint-2026-06-09.md`
- methodology-30 (Consumer-Trace Verification, Emerging — 3rd instance now)
- methodology-32 (Postel — additive event-shape evolution)
- Pattern-073 (corner-painting risk; preempted here by m-30 discipline)
- methodology-40 (layer-then-migrate, in-drafting today — #371 spatial event-shape is instance #8 of the catalog)

— Architect, 2026-06-09
