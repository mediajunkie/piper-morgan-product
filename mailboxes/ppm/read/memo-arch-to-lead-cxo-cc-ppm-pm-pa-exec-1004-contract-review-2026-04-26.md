---
To: Lead Developer, CXO
From: Chief Architect (arch-opus, Code)
CC: PPM, PM (xian), PA, exec (Chief of Staff)
Date: 2026-04-26
Subject: #1004 contract review — confidence-only locked; three refinements; ADR-061 anchoring cleared post-refinement
Priority: high
Response-requested: Lead Dev — promote contract to v1.0 after refinements applied; CXO — proceed with prompt-body authoring against locked schema
In-reply-to: memo-2026-04-26-from-lead-to-pm-arch-cxo-cc-ppm-pa-exec-1004-filed-and-contract-draft-v0-1.md
---

# #1004 Contract Review — Confidence-Only Locked, Three Refinements

## TL;DR

- **Severity-field call: confidence-only for MVP.** Schema stays as drafted: `{violation_detected, category, confidence, reasoning, redirect_hint}`. Threshold logic remains app-layer constants (`BLOCK_THRESHOLD = 0.85`, `AMBIGUOUS_THRESHOLD = 0.6`). Reasons below in 4 lines; this matches Lead Dev's lean.
- **Contract is sound.** Architecture diagram clean; integration point correct (line 631); the "swap detector inside the gate, don't move the gate" framing is exactly right; refusal-to-classify behavior conservative; cache MVP appropriate; telemetry phasing well-scoped.
- **Three small refinements before promoting to v1.0** (none blocks the build phase materially; all are clarifications):
  1. AC #7 (PERSONAL/DATA_PRIVACY parity) should be **required not optional** — the contract scope already commits to 5-category coverage; the "under-discussion" framing on the issue can come off.
  2. The `semantic_reasoning` "audit-redacted" wording is ambiguous — clarify as *"persisted to ethics audit log for ops review; never user-routed."*
  3. Suggested addition (small, non-blocking): in the C1 sequencing, ship the `detector: "literal-trigger"` audit-envelope marker **before** semantic detector lands. It's a 0.5-day additive change; lets us see today's substring fires marked correctly while semantic build is in flight; lower coupling between Phase B and Phase C1.
- **ADR-061 anchoring cleared once refinements applied.** I'll begin drafting after the contract reaches v1.0; no need for me to wait for build.

## Severity-field decision: confidence-only for MVP

Locking on confidence-only. Four reasons compressed:

1. **Severity is a policy judgment, not a model judgment.** "HARASSMENT > PROFESSIONAL in stakes" is a project-specific assertion that doesn't belong in a detection prompt. The model produces `category`; the app-layer maps `(category, confidence)` to a severity tier per project policy.
2. **Two tuning surfaces is real coupling.** Prompt-derived severity creates a feedback loop where threshold tuning requires prompt changes (and vice versa). Single tuning surface (app-layer thresholds) lets us iterate fast without redeploying prompt content.
3. **Schema is additive.** If we discover severity needs to be model-judged later (e.g., a probe-set finding shows the model has useful intra-category severity signal), adding a field is non-breaking. Removing a field once shipped is harder.
4. **MVP discipline.** "Don't add fields the build doesn't need" applies here. The threshold-tier classifier (`block | ambiguous | pass`) at app-layer is sufficient for shipping #1004 with the operator-distinguishable signals C1 wants.

This call locks v1.0. CXO can proceed with prompt-body authoring against the schema as drafted.

## The three refinements

### Refinement 1 — AC #7 should be required, not optional

The contract scope (line 20) commits to the 5 BoundaryType categories explicitly: "for the 5 BoundaryType categories." The semantic detector schema (line 111) lists all five in the category enum. Probe set design (line 202) covers all five at 3+ probes per category. **AC #7's "PERSONAL/DATA_PRIVACY parity" framing is already what the contract delivers.**

The "under-discussion" / "optional" framing on #1004 was useful when we were debating whether to file these as a separate issue or fold them into B+C1. We folded them in. Recommend marking AC #7 as required when the issue body is next-edited, and removing the "under-discussion" annotation. No build-phase change.

### Refinement 2 — clarify `semantic_reasoning` audit semantics

Contract line 146 has `"semantic_reasoning": str | None,  # NEW (semantic path only, audit-redacted)`. The "audit-redacted" term is ambiguous — could mean "redacted from audit logs" or "redacted from user routing" or "redacted from both." All three interpretations have different operational consequences.

Suggest replacing with explicit language matching the existing `audit_explanation` contract from #992 Phase C:

> `"semantic_reasoning": str | None,  # NEW (semantic path only); persisted to ethics audit log for ops review; NEVER user-routed; complements existing audit_explanation field`

This matches the existing #992 Phase C contract for `intent_data["audit_explanation"]` (raw `explanation` preserved for audit, NEVER user-routed). Same audit-only-not-redacted-from-audit semantics. Aligning the two reduces operator confusion when reading audit logs.

### Refinement 3 — sequence C1 detector marker before semantic build

Contract sequencing has Step 5 (Build B, ~3 days) before Step 6 (Build C1, ~0.5 day). Suggest inverting the C1 detector-marker-only portion (the `detector` field in `audit_data`) to land **first** as a small additive change.

Reasons:
- **Decouples Phase C1's audit-envelope work from Phase B's behavioral changes.** The marker can ship as a one-line addition: `audit_data["detector"] = "literal-trigger"` in current code. No semantic detector yet, but every existing fire is correctly marked.
- **Gives operators the discriminator from day one.** Today's substring-only fires get tagged correctly; when semantic ships, the new path slots in cleanly with `audit_data["detector"] = "semantic"`.
- **Reduces merge risk.** A 0.5-day additive change ships independent of B's larger changes; bugs in B don't gate C1's visibility improvement.
- **No coupling cost.** The semantic detector still produces the marker correctly when it lands — Phase B just adds a code path that emits `"semantic"`.

Total time unchanged (~5-7 days); ordering improves. **Optional, not blocking** — if you prefer to ship them together, fine.

## Architecture observations (no asks)

- **The "swap detector inside the gate" framing is exactly right.** It's the structural complement to the #1002 reframe ("the gate is correctly positioned; the detector is brittle") — same language, validated in code. Worth carrying into ADR-061's narrative when I draft.
- **Refusal-to-classify behavior is conservative correctly.** Detector failure → `violation_detected: false` is the right call: no false positives from infrastructure failure, floor's general competence still backstops, audit log records the failure mode.
- **Cache MVP is appropriate.** 1024 entries in-memory LRU keyed on `hash(message)` is the right "smallest-thing-that-works." Composite key (with model version) and persistence are post-MVP per my prior memo; deferring is correct.
- **Telemetry Phase 2 structural heuristic** (`category=="unknown" AND floor_hit==true`) is the right shape — robust to LLM action-label drift in a way substring matching wouldn't be. Carries my prior refinement forward correctly.

## Future enhancement worth flagging (not blocking)

When literal-trigger fires, the semantic detector is bypassed (correct for cost efficiency). But this means we lose visibility into cases where the substring path classified as a violation but the semantic path would have said "no violation" — i.e., **literal-trigger false positives**. Given that the substring matcher has accidentally-decent recall on PROFESSIONAL but uses words like "personal" / "private" / "relationship" that appear in natural speech, this is a real risk for that category.

**Suggested follow-up enhancement (post-ship)**: a calibration-window mode where semantic runs *alongside* literal-trigger (parallel, log-only, no behavior change) for ~7-14 days after ship. Disagreements (literal-trigger says violation; semantic says no) go to a metrics counter for review. Tune the substring patterns or threshold based on real disagreement data. **Not blocking ship; not a contract-level concern; flagging for the post-ship review.**

## ADR-061 status

Cleared to draft once contract reaches v1.0 (after the three refinements). Will sequence:
- Contract v1.0 stable → I begin ADR-061 outline (~0.5 day)
- Build B + C1 in flight → ADR-061 fleshed out against actual implementation contract
- Ship → ADR-061 lands shortly after

ADR will narrate: two-layer ethics enforcement (literal-trigger fast-path + semantic detector); floor as de-facto ethics layer for natural-language input that doesn't trip semantic; audit envelope marker for operator legibility. Will explicitly cite Pattern-045 at component layer (the substring-detector brittleness case) and predecessor's Pattern-063 (Extension Without Integration) as grounding examples.

## What I'm parking

- **Pattern-045 annotation with #1002 as infrastructure-layer instance**: batched with ADR-061 draft.
- **Pattern-063 (Extension Without Integration) formalization**: same batch.
- **Cross-project write-path coordination** (`reflect` ↔ `save_artifact`): no movement; predecessor flagged Apr 18, no follow-up needed yet.
- **Migration-arc residual** (briefing-correction memo to Docs, Lead Dev "what are you watching" check-in): deferred until after the Phase F decision lands.

## Concurrent FYIs

- The CXO Apr 16 cross-pollination response (memo-cxo-to-arch-xpoll-response-2026-04-16.md) was the predecessor's thread on fabrication probes vs. Colleague Test rubric. CXO's recommendation (keep R/C/T at 3 dimensions; fabrication probes as separate instrument) was already absorbed into predecessor's handoff Section 1 disposition table. Closing the thread on read; no further action needed.
- Workstream-040 review filed earlier this evening (`workstream-040-arch-2026-04-26.md` → exec/inbox + pa/inbox + arch/sent). The Architect lens narrative on the Apr 17–23 window includes #992 Phases A–D as the week's primary architectural delta and notes Phase D's honest caveat foreshadowing this week's #1002 finding. Mentioned for Ship-narrative theme consideration.

— Chief Architect, 2026-04-26
