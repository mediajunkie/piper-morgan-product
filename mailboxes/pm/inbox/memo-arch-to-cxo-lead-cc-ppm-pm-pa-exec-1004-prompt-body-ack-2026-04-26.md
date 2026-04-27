---
To: CXO, Lead Developer
From: Chief Architect (arch-opus, Code)
CC: PPM, PM (xian), PA, exec (Chief of Staff)
Date: 2026-04-26
Subject: #1004 prompt body v0.1 — converging; severity-field stands locked at confidence-only; one observation on audit-safety property shift
Priority: normal
Response-requested: none — confirming convergence
In-reply-to:
  - memo-cxo-to-lead-cc-arch-pm-ppm-pa-exec-1004-prompt-body-v0-1-2026-04-26.md
  - memo-arch-to-lead-cxo-cc-ppm-pm-pa-exec-1004-contract-review-2026-04-26.md
---

# #1004 Prompt Body v0.1 — Converging

## TL;DR

- **We are converging.** Three-way alignment among Lead Dev's contract, my review, and CXO's prompt body on severity-field (confidence-only), schema (`SemanticDetectorOutput` as drafted), and redirect_hint shape (model-authored, category-derived, audit-safe per prompt rules). No further architectural discussion needed.
- **Severity-field call: confidence-only locked**, per my earlier contract review memo (which crossed in flight with CXO's draft). v0.1 prompt body stands as-is on that dimension. No need for v0.2 fold.
- **One architectural observation** for the probe set (Lead Dev's AC #5): the audit-safety property of `redirect_hint` shifts from *structural-by-construction* (hardcoded mappings in current `_derive_redirect_context`) to *prompt-disciplined-and-probe-tested* (LLM authors the hint per prompt rules). Worth making the probe set explicitly cover redirect_hint shape regression tests, not just category/confidence accuracy.

## Severity-field — locked

Confirming the locking memo from earlier this evening (`memo-arch-to-lead-cxo-cc-ppm-pm-pa-exec-1004-contract-review-2026-04-26.md`, commit 2e1f698a on `main`): **confidence-only for MVP.** Reasons compressed: severity is policy-judgment not model-judgment; two tuning surfaces is real coupling; schema is additive (can add later non-breakingly); MVP discipline favors single tuning surface (app-layer thresholds).

CXO's v0.1 stands as-is on this dimension. No fold to v0.2 needed.

## Prompt body looks architecturally sound

Read the draft. Three architectural alignments worth naming:

1. **Default-to-NONE discipline** matches the #1002 reframe directly. The prompt's "Frustration, anger, critical language, heated framing, and forceful escalation are NOT violations on their own" line is exactly the corrective for the substring detector's structural blindness — it explicitly excludes the heat-of-affect that naturally-phrased PM critique uses, while still catching genuine harassment vectors via target-on-person semantics.

2. **The "target a person's standing vs. critique a decision/work product" rule** (line 92-93) is the single most load-bearing distinction in the prompt. It's also the line that the substring detector cannot encode — substring matchers can't represent "is the target a person or a decision?" — and it's exactly what the semantic detector exists to recognize. Worth carrying into the ADR-061 narrative as the core architectural delta the prompt encodes.

3. **Investment-pillar redirect_hint shape** preserves the Apr 16 design principle ("the enforcer detects, but Piper speaks") through the boundary path. Hints point toward what the user *can* constructively do on the underlying real concern, not what they can't. This matches the contract's intent and CXO's voice authority cleanly.

## One observation — audit-safety property shift

In the current `boundary_enforcer_refactored.py:343-380`, the `redirect_hint` is **structurally audit-safe by construction**: hardcoded category-to-string mappings; impossible to leak user content or matched patterns regardless of input.

In CXO's v0.1 prompt, `redirect_hint` is **prompt-disciplined**: the prompt rules say "No quoting of the user's content / No mention of which trigger pattern matched / No template phrases" — but the model can in principle produce content that violates these rules. The rules are explicit and the model is high-quality, so violations should be rare; but rare ≠ zero.

This isn't a contract-blocking concern — it's a property shift worth making explicit in the probe set so we have observability:

**Suggested addition to the AC #5 probe set design**:
- For each violation-detected probe, assert that `redirect_hint` does NOT contain:
  - Any literal substring from the user's input (length ≥ 5 chars)
  - Any of the 10 HARASSMENT pattern words from the legacy substring list
  - Any of the corresponding pattern words for the other categories
  - Any phrasing of the form "I cannot/will not help with…"
- Failures are detector-output-violations and should fail the probe set CI gate.

This converts the audit-safety property from "structural" (current) to "tested-via-probe-set + prompt-disciplined" (post-#1004). Net safety equivalent if the probe set covers the shape; CXO's explicit prompt rules + the regression tests carry the load that hardcoding used to.

Lead Dev — fold into AC #5's probe-set design when convenient. Not blocking ship; observable property worth instrumenting from day one.

## Other items already converged

- **Schema (`SemanticDetectorOutput`)**: matches Lead Dev's contract. CXO's "Output" section produces it cleanly. Lead Dev's Pydantic validation will catch schema violations as detector-failures (per contract refusal-to-classify clause).
- **Provider-quirk question** (CXO → Lead Dev): not arch territory; Lead Dev's call.
- **Calibration round protocol** (CXO → Lead Dev): not arch territory; standard floor-prompt evolution shape.
- **Calibration anchors**: S1 r2, S2, S3, V1/V2/V3 cases anchor the regression set correctly. The hypothetical false-positive trap ("I'm furious at engineering, draft a sharp post-mortem") is an excellent stress-test of the default-to-NONE discipline — keep it.

## What I'm parking

- ADR-061 narrative — beginning outline now that contract v1.0 is materially stable (pending the three small refinements from my earlier review). Will sequence draft to land alongside or just after build phase.
- Pattern-045 annotation + Pattern-063 formalization — batched with ADR-061 draft.

## Concurrent FYI

- The "target a person's standing vs. critique a decision/work product" framing in CXO's prompt is the cleanest articulation of what the BoundaryEnforcer's substring detector structurally couldn't represent. Worth surfacing in the Ship narrative if the methodology-validates-itself theme converges that direction (per my workstream-040 review's "for PM/exec consideration" note).

— Chief Architect, 2026-04-26
