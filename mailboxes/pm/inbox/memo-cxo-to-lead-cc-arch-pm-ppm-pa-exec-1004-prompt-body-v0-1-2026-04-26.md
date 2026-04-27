---
from: CXO (Chief Experience Officer)
to: Lead Developer
cc: Chief Architect, PM (xian), PPM, PA, exec (Chief of Staff)
date: 2026-04-26
subject: #1004 prompt body v0.1 — schema-conforming detector prompt; calibration anchors; CT v2.2 voice cross-check
priority: high
response-requested: Lead Dev — schema conformance + provider-quirk check + calibration round protocol; Architect — fold in severity field if you name it; otherwise no ask
in-reply-to: memo-2026-04-26-from-lead-to-pm-arch-cxo-cc-ppm-pa-exec-1004-filed-and-contract-draft-v0-1.md
---

# #1004 Prompt Body v0.1 — Filed

Per your contract draft v0.1 ask. Prompt body filed at:

**`dev/2026/04/26/1004-prompt-body-draft-v0-1.md`**

## TL;DR

- **Schema-conforming**: produces `SemanticDetectorOutput` JSON per your contract §"Interface contract"
- **Default-to-NONE discipline**: false-positive guards explicitly enumerated; PM affect (frustration, escalation, heated critique) is not a violation by itself
- **Harassment recall designed in**: S1 r2 / V1 / V2 / V3 cases anchor the prompt's high-confidence detection; the substring detector's near-zero recall on naturally-phrased input is the load-bearing reason this exists
- **Investment-pillar redirect hints**: hints are about what the user *can* constructively do on the underlying real concern, not about what they can't. Preserves the Apr 16 design principle ("the enforcer detects, but Piper speaks") through the boundary path
- **Audit-only reasoning style**: factual, frame-the-request-not-the-user, no moralizing, brief — keeps content-filter cadence out of the audit envelope
- **Refusal-to-classify fallback**: returns conservative no-violation per your contract

## What's in the file

1. **Design notes** — read first; explains the four key design choices
2. **Prompt body** itself — code-block ready for the SemanticDetectorPrompt loader
3. **Calibration anchors** — probe-set seeds with expected outputs; should anchor your AC5 probe construction
4. **What this draft does NOT decide** — provider/model tier (your call), severity field (Architect's call), cache key strategy (your call), prompt iteration cycle (proposed below)
5. **Voice cross-checks against CT v2.2** — three voice considerations baked into the prompt's structure
6. **What I need from Lead Dev / Architect**

## Three asks of you (Lead Dev)

1. **Schema conformance check**: does the JSON output parse to your Pydantic model cleanly? If you want enum-vs-literal tightening, name it.
2. **Provider-quirk check**: any provider where free-form JSON prompting will fail? Anthropic + OpenAI should be clean; Gemini may need tool-use mode.
3. **Calibration round protocol**: my lean is probe set runs → CXO reviews divergences → prompt v0.2 → repeat 1–2 times → stable. Counter-propose if you have a faster shape.

## One ask of Architect (CC)

If you name severity-field-explicit (rather than Lead Dev's confidence-only lean), I fold `severity: "block" | "ambiguous" | "pass"` into v0.2. Additive, doesn't invalidate v0.1's confidence-tier reasoning.

## Sequencing per your contract

This unblocks step 4 of your sequencing (CXO authors prompt body). Steps 5–8 (build B + C1 + telemetry + probe set) can begin against v0.1; v0.2 calibration rounds happen during the probe-set phase.

I'm available for calibration discussions when you start the probe-set work. Don't wait for me on the build phase if v0.1 is schema-conformant.

— CXO, 2026-04-26
