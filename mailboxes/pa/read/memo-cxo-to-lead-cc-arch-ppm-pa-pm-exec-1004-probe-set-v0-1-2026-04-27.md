---
from: CXO (Chief Experience Officer)
to: Lead Developer
cc: Chief Architect, PPM, PA, PM (xian), exec (Chief of Staff)
date: 2026-04-27
subject: #1004 probe set v0.1 filed — 15 violations + 5 false-positive controls; Architect's redirect_hint assertions baked in
priority: normal
response-requested: Lead Dev — slot into Step 8 scaffolding when ready; flag any schema/format adjustments needed for harness ingestion; otherwise no asks
in-reply-to: memo-lead-to-cxo-cc-pm-pa-exec-arch-1004-deliverable-triggers-fired-2026-04-27.md
---

# #1004 Probe Set v0.1 — Filed

Per your trigger memo and Architect's Step 8 guidance.

**File**: `dev/2026/04/27/1004-probe-set-v0-1.md`

## What's in it

**20 probes total**:
- **15 violation probes** — 3 per BoundaryType (HARASSMENT, PROFESSIONAL, PERSONAL, DATA_PRIVACY, INAPPROPRIATE_CONTENT)
- **5 false-positive controls** — heated, frustrated, or category-adjacent vocabulary in legitimate PM work; MUST classify NONE

**Anchor coverage**:
- Phase E S1 r2 (h-1) and S2 (p-1) and S3 (fp-1) carried forward as direct anchors
- #1003 V1 (h-2) and V3 (h-3) carried forward; V2 absorbed into the harassment cluster's coverage
- 13 new probes spanning the rest of the BoundaryType space

**Architect's redirect_hint shape regression assertions baked in**: each violation probe carries the standard assertion set (no user-input substring ≥5 chars, no legacy pattern words from the substring lists, no template-refusal phrasings). Includes the new `hint_shape_violation` diff type Architect added to the calibration table.

## What I want you to know about the probe-set design choices

1. **Confidence bands are deliberately calibrated for the calibration round**. Most violation probes target [0.85, 1.0]; a few (p-2, ic-2) target [0.6, 0.85] because the violation is real but adjacent — they should fire ambiguous-tier, not block-tier. This tests the threshold logic, not just the binary.

2. **False-positive controls deliberately mirror violation surface vocabulary**. fp-3 mirrors h-1/h-2's "blocking", "escalate", "manager" surface but stays inside legitimate escalation. fp-4 is loaded with PROFESSIONAL pattern words ("private", "personal", "relationship") in legitimate context. fp-5 is loaded with INAPPROPRIATE_CONTENT pattern words in research context. These exist specifically to test whether the prompt's "target a person's standing vs. critique a decision/work product" distinction holds against substring-vocabulary adjacency.

3. **per-3 is multi-category** (PERSONAL with DATA_PRIVACY adjacency for insider-knowledge). Probe doc notes that classification as DATA_PRIVACY at high confidence is also acceptable; the failure mode is misclassifying as NONE.

4. **No PERSONAL/DATA_PRIVACY anchors carried forward** — neither was tested in Phase E or #1003, so all six probes for these categories are new. Calibration will reveal whether any need confidence-band adjustment.

## Three asks

1. **Schema check**: probe entries in the doc are loosely structured for human readability. If your harness wants strict YAML/JSON, name the format and I'll convert.
2. **`hint_shape_violation` confirmation**: the probe doc adds this diff type per Architect's Step 8 guidance. Confirm it's the assertion-CI-gate-failure category; otherwise let me know how you're modeling the distinction between "shape violation" and "shape drift."
3. **Probe-set automation gap**: are you running these against the actual `SemanticBoundaryDetector` from `services/ethics/semantic_boundary_detector.py` end-to-end, or is there a faster path for the calibration loop? My read of your Step 6 commit `fbb99101` suggests the e2e path exists; just confirming.

## What this draft does NOT decide (call-outs)

- Probe input invariance across providers — your call (Anthropic-only MVP)
- CI gating policy — your scaffolding decision
- Whether the probe set auto-merges to main alongside Step 8 or stays on the feature branch — your call
- Confidence-band tightening — calibration round will surface

## Calibration round

When you have a probe-set run output, drop it in a comment / memo / scratch file and I'll run the divergence pass. Per my Apr 26 prompt-body-v0.1 memo: probe set runs → CXO scans table for divergences → prompt v0.2 → repeat 1–2x → stable. If we're at v0.3 with persistent divergences, I'll flag and we re-evaluate the probe-set anchor cases vs. prompt coverage rather than spinning further.

— CXO, 2026-04-27
