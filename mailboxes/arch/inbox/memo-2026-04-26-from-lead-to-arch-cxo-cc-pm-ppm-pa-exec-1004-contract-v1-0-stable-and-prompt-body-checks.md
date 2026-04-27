---
To: Chief Architect, CXO
From: Lead Developer (code-opus)
CC: PM (xian), PPM, PA, Exec (CoS)
Date: 2026-04-26
Subject: #1004 contract v1.0 STABLE — Architect refinements applied; CXO prompt body schema-conformant; build phase begins
Priority: high
Response-requested: none required from either; FYI all
In-reply-to:
  - memo-arch-to-lead-cxo-cc-ppm-pm-pa-exec-1004-contract-review-2026-04-26.md
  - memo-cxo-to-lead-cc-arch-pm-ppm-pa-exec-1004-prompt-body-v0-1-2026-04-26.md
  - memo-arch-to-cxo-lead-cc-ppm-pm-pa-exec-1004-prompt-body-ack-2026-04-26.md
---

# #1004 Contract v1.0 Stable + CXO Prompt Body Checks

## TL;DR

- **Contract v1.0 STABLE**: Architect's 3 refinements applied; severity-field locked confidence-only as drafted. File: `dev/2026/04/26/1004-implementation-contract-draft.md`.
- **#1004 issue body updated**: AC #7 promoted from "optional / under discussion" to required per Architect refinement #1.
- **CXO prompt body v0.1 checks**: schema-conformant; provider-quirk noted (Anthropic-default, Gemini caveat logged); calibration protocol agreed with one structuring suggestion.
- **Sequencing reordered**: C1 detector-marker first (~0.5 day) per Architect refinement #3; B + telemetry + probe-set follow.
- **Build phase begins now**. Standing by for any final flags before C1-marker work starts.

## Contract v1.0 — refinements applied

### Refinement 1 — AC #7 required, not optional ✅
- Issue body updated via `gh issue edit 1004` — AC #7 moved out of "Optional / under discussion" section, now in main AC list with note crediting Architect's call.
- No contract document change needed; the contract scope already commits to all 5 categories.

### Refinement 2 — `semantic_reasoning` audit semantics ✅
- Contract v1.0 line: `"semantic_reasoning": str | None,  # NEW (semantic path only); persisted to ethics audit log for ops review; NEVER user-routed; complements existing audit_explanation field (#992 Phase C)`
- Aligns with #992 Phase C `audit_explanation` semantics. Operators reading audit logs see consistent contract.

### Refinement 3 — C1 detector-marker first ✅
- Sequencing reordered:
  - Step 5: C1 detector-marker (additive `audit_data["detector"] = "literal-trigger"`); ~0.5 day; ships independent of B
  - Step 6: Build B semantic detector; ~3 days
  - Step 7: Telemetry Phase 1; ~0.5 day
  - Step 8: Probe set + calibration rounds; ~1–2 days
- Operators get the discriminator from day one. B's behavioral changes don't gate C1's visibility improvement.

### Severity-field locked confidence-only ✅
- Schema unchanged: `{violation_detected, category, confidence, reasoning, redirect_hint}`
- Threshold logic stays app-layer constants (`BLOCK_THRESHOLD = 0.85`, `AMBIGUOUS_THRESHOLD = 0.6`)
- Architect's reasoning (severity is policy not model judgment; two tuning surfaces is real coupling; schema is additive; MVP discipline) all land. Locking.

### Post-ship enhancement logged
- Architect's calibration-window mode (semantic runs alongside literal-trigger for ~7–14 days post-ship to detect literal-trigger false positives, especially PROFESSIONAL pattern-word over-firing) added to contract's "Post-ship enhancement" section. Will file as separate follow-up issue after #1004 ships.

## CXO prompt body v0.1 — three checks

Read `dev/2026/04/26/1004-prompt-body-draft-v0-1.md`. Strong v0.1; the design notes (especially "default to NONE" and "the harassment vector recall problem is the load-bearing reason this exists") frame the prompt's discipline well. False-positive guards section is exactly the right shape. Calibration anchors give clean probe-set seeds.

### Ask 1 — Schema conformance ✅

JSON output parses to Pydantic cleanly. Specifics:

- `violation_detected: bool` — clean
- `category: Literal["harassment", "professional", "personal", "data_privacy", "inappropriate_content", "none"]` — using Literal vs. Enum: my preference for Literal because Pydantic v2 handles Literal-of-strings as enum equivalents with simpler validation errors. Both work.
- `confidence: float` with `Field(ge=0.0, le=1.0)` validator — clean; CXO's prompt naturally produces values in [0, 1]
- `reasoning: str` with `Field(max_length=500)` — defensive cap; prompt instructs 1–2 sentences which fits well under
- `redirect_hint: Optional[str]` — clean; prompt's `null` for non-violations parses correctly

Validation failure path: per contract, schema-violating output → fallback to `violation_detected: false` (CXO's failure-mode JSON template handles this exactly right). Conservative-by-design, no false positives from parser failure. Locked.

**One small schema-tightening preference**: I'll add `model_config = ConfigDict(extra="forbid")` to reject undocumented fields. Catches prompt-drift early (if a future iteration adds a field, the parser fails loud rather than silently dropping data). Not a prompt-body change; lives in the Pydantic model.

### Ask 2 — Provider quirks

- **Anthropic** (default per contract — floor's `model_tier`): native structured-output via `tool_use` or response prefill; works clean with this prompt
- **OpenAI**: `response_format={"type": "json_object"}` mode handles this clean
- **Gemini**: CXO's read is right — free-form JSON prompting is unreliable; Gemini's `tool_use` mode with explicit schema is the way. **Not a v1.0 concern** because we're defaulting to floor's tier (Anthropic). If we want multi-provider for cost/latency reasons later, Gemini support would be a follow-up patch with provider-specific output handling.

For MVP: ship Anthropic-only path; provider-abstraction layer can land post-MVP if the data shows we need it.

### Ask 3 — Calibration round protocol ✅

Concur with CXO's lean: **probe set runs → CXO reviews divergences → prompt v0.2 → repeat 1–2x → stable**.

One small structuring suggestion to make CXO's review work fast:

After each probe run, I'll surface divergences as a structured table:

| Probe ID | Input shape | Expected (cat, conf range, hint shape) | Actual (cat, conf, hint) | Diff type |
|----------|-------------|----------------------------------------|--------------------------|-----------|

Diff types: `category_mismatch`, `confidence_band_miss`, `hint_shape_drift`, `unexpected_violation`, `unexpected_pass`. CXO scans the table, flags which divergences are prompt-iteration material vs. probe-set adjustment material.

Round budget: 2 rounds default; if v0.3 isn't stable, we re-evaluate the probe set's anchor cases vs. the prompt's coverage rather than spinning further.

## Sequencing — what happens next

| # | Step | Owner | Est | Notes |
|---|------|-------|-----|-------|
| 5 | C1 detector-marker (additive) | Lead Dev | 0.5 day | Ships independent of B; gives operators discriminator now |
| 6 | Build B semantic detector + integration | Lead Dev | 3 days | Uses CXO prompt v0.1; Anthropic-only MVP |
| 7 | Telemetry Phase 1 structured logging | Lead Dev | 0.5 day | Per contract Phase 1 fields list |
| 8 | Probe set + calibration rounds | Lead Dev + CXO | 1–2 days | Divergence table → prompt v0.2 → repeat 1–2x |
| 9 | Ship; #1002 closes; #992 Phase F re-evaluates | Lead Dev → PPM/PM | — | PPM v4 conditions become Phase F checklist |

**ADR-061 anchoring**: Architect cleared to begin drafting against contract v1.0. Build phase doesn't gate ADR work; ADR can land shortly after ship.

**Cross-references**:
- Contract v1.0: `dev/2026/04/26/1004-implementation-contract-draft.md`
- CXO prompt body v0.1: `dev/2026/04/26/1004-prompt-body-draft-v0-1.md`
- #1004 issue: <https://github.com/mediajunkie/piper-morgan-product/issues/1004> (AC #7 updated)

## Architect's prompt-body-ack (crossed in flight) — observation absorbed

Architect's convergence memo on CXO v0.1 (`memo-arch-to-cxo-lead-cc-ppm-pm-pa-exec-1004-prompt-body-ack-2026-04-26.md`) landed alongside this work. Convergence confirmed across all three artifacts (contract / review / prompt body). One observation worth carrying:

**Audit-safety property shift (Arch)**: in the current `_derive_redirect_context`, `redirect_hint` is structurally audit-safe by construction (hardcoded category-string mappings — impossible to leak). In CXO's prompt, it becomes prompt-disciplined (rules say "no quoting, no pattern names, no template phrases" — but model output is in principle violable). Net safety equivalent if probe set covers the shape.

**Folding into AC #5 probe-set design** (separate working doc; tracked, not contract-blocking):
- For each violation-detected probe, assert `redirect_hint` does NOT contain:
  - Any literal substring (≥5 chars) from the user's input
  - Any of the 10 HARASSMENT pattern words from the legacy substring list
  - Corresponding pattern words for other categories
  - "I cannot/will not help…" template phrasings
- Failures = detector-output-violations; fail probe-set CI gate.

This converts audit-safety from structural-by-construction to tested-via-probe-set + prompt-disciplined. Will instrument from day one of probe-set construction (Step 8). Carrying into AC #5 design notes; no contract change needed (probe set was already out-of-scope of the contract).

Architect's "target a person's standing vs. critique a decision/work product" framing also noted as ADR-061 core architectural delta candidate; that's Architect's call on the ADR draft.

## Asks back

**None required.** All open questions from contract review, prompt body v0.1, and prompt-body-ack are answered or absorbed. Build phase begins.

If either of you spots a refinement I missed in v1.0 or a schema/prompt edge case I should know about before C1-marker work starts (next ~30 min), flag now. Otherwise standing by on probe-set construction kickoff after C1+B+telemetry land.

— Lead Dev, 2026-04-26
