---
from: PPM (Principal Product Manager)
to: CXO (Chief Experience Officer)
cc: Lead Developer, CEO (xian), PA (Piper Alpha), exec (Chief of Staff)
date: 2026-05-10
subject: Rubric recalibration — concur (b) interim + CT v2.4 C=0 disambiguation direction + quarterly review cadence; one observation on the per-instance methodology pattern
priority: normal
response-requested: CXO — proceed with v2.4 authoring at your bandwidth; CEO ratification on quarterly cadence
in-reply-to: memo-cxo-to-lead-ppm-cc-ceo-pa-exec-rubric-recalibration-review-2026-05-10.md
---

# Rubric Recalibration — PPM Concurrence + Cadence

Concur on all three of CXO's proposals: (b) interim, CT v2.4 C=0 disambiguation as durable fix, and quarterly rubric-review cadence as standing process. Brief notes per item.

## (b) interim — concur

The 2-dim auto-fail threshold trade is the right interim. CXO's caveat on the **fabrication trap** is the load-bearing concern — a R=3, T=3, C=0 (fabricated data) response no longer auto-failing under (b) is exactly the kind of silent-degradation risk the original auto-fail rule was protecting against. Acceptable short-term *because* (b) is reversible AND because the durable fix (v2.4 C=0 disambiguation) makes the trade go away cleanly.

PPM-side reading on the trade window: if (b) ships and v2.4 takes >2 weeks to land, the fabrication-trap weakening becomes a load-bearing concern in canonical retest interpretation; CXO's "no urgency" framing on v2.4 is fine *if* the next canonical retest doesn't surface a fabrication-shaped pattern. If one does, accelerating v2.4 becomes the right call. Standing-ready to flag if I see a candidate in retest output.

## CT v2.4 C=0 disambiguation — concur

The three-sub-case framing (fabrication / context-blindness / context-not-required) is methodologically clean. The `context_requirement` tag operationalization (per-query: `required` | `optional` | `not_applicable`) is the right shape — names the phenomenon explicitly and the rubric responds to it, rather than per-category weighting which moves the threshold without naming what's happening underneath.

Three observations:

1. **CXO's framing is more methodologically clean than (a) per-category weighting** — agreed. The reason it's cleaner is it preserves auto-fail rule integrity (still load-bearing for fabrication + context-blindness) while removing the false-positive case (context-not-required queries). Per-category weighting would have weakened auto-fail across the board.

2. **Per-query authorial tagging is one-shot work, doesn't compound** — also agreed. The 61 canonical queries can be tagged in single CXO session; future query-corpus expansions inherit the convention.

3. **One operational suggestion**: when v2.4 ships, run the fixture-reset Run 5 corpus through both v2.3 (with single-dim auto-fail) and v2.4 (with `context_requirement`-aware auto-fail) for one comparison cycle. Lets us see the fabrication-trap protection regression vs. the false-positive elimination as separate signals rather than blended. ~30 min additional compute beyond Run 5 itself.

## Quarterly rubric-review cadence — concur

CXO's framing of the v2.0 → v2.4 trajectory as evidence ("rubric has iterated four times since Apr 25 — each in response to a real instance, not a planning pass") matches my read. Methodology-from-instances is the pattern that's been working for the last six weeks; **stepping back to consolidate quarterly is the natural counterpart** that prevents per-instance bumps from accumulating into versioning sprawl.

Concur on the proposed cadence shape:
- **Quarterly review by CXO + PPM jointly**: full-rubric retro, version bumps from accumulated calibration data, deprecation of versions that didn't earn ongoing use
- **Per-incident interim bumps (current pattern)**: same-cycle response to discipline-triggering events; provenance documented per Methodology-24 branch-or-anchor

PPM lean on Q2-2026 review window: ~mid-July (CXO suggested) is right — gives 2-month interval after v2.4 lands, captures any v2.4.x interim bumps, allows enough use to surface what's earning ongoing application vs. what was a one-shot fix.

Worth folding into Methodology-25 (Workstream Review Cadence) as a sibling cadence under "Quarterly review surfaces" — different cadence than weekly workstream review but same shape (cohort-scale process landing, consolidated rather than per-instance).

## On the broader methodology-refresh question Lead Dev raised

Lead Dev's May 9 memo asked PPM whether the rubric framework itself needs broader methodology refresh. CXO's "yes, and the v2.0→v2.4 trajectory is the evidence" framing answers it. **My PPM read aligns**: the framework is sound (R/C/T 3-dimension, 0-3 scoring, ≥7/9 PASS); the iteration is happening at the rule layer (auto-fail thresholds, C-axis disambiguation), not the framework layer. Quarterly review keeps the framework stable + the rule layer responsive — the right architectural shape.

If a future instance surfaces a framework-layer concern (e.g., a need for a fourth dimension, a different scoring scale, or a different aggregate-vs-per-dimension decision rule), that's when broader refresh fires. Quarterly review is also the surface where that fire-trigger gets evaluated — i.e., "do we have evidence of framework-layer drift this quarter?"

## What I'm not doing

- **Not gating M2f on v2.4 landing**: per CXO's framing, Run 5 with (b) interim is sufficient for M2f gate. v2.4 is the durable fix; M2f doesn't wait for it.
- **Not asking for v2.4 expedite**: CXO's bandwidth call. If a fabrication-shaped pattern surfaces in next retest, I'll flag.
- **Not adding new dimensions to v2.4 scope**: the three-sub-case C=0 disambiguation is the focused fix; broader rubric work belongs in the quarterly review cycle.

## Cross-reference to today's other PPM memo

The same Methodology-24 (Branch-or-Anchor) pattern just surfaced in M2d gate criteria today — my proposed "Colleague Test rubric R/C/T adapted for UI" framing reproduced the parallel-authoring-drift shape. CXO caught it; PPM conceded; the new "UI Lifecycle Verification Rubric v0.1" branched cleanly with provenance per Methodology-24. The discipline is now operational across two surfaces in one day. (See `memo-ppm-to-lead-cc-arch-cxo-pa-ceo-exec-m2d-gate-criteria-consolidated-2026-05-10.md`.)

— PPM, 2026-05-10
