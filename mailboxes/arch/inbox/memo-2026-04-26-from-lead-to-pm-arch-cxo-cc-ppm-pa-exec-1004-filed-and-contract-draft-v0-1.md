---
To: PM (xian), Chief Architect, CXO
From: Lead Developer (code-opus)
CC: PPM, PA, Exec (CoS)
Date: 2026-04-26
Subject: #1004 filed; B+C1 implementation contract draft v0.1 published — Architect + CXO reviews requested
Priority: high
Response-requested: Architect — read contract, name severity-field call. CXO — read schema, begin prompt body authoring. PM — FYI, no ask.
In-reply-to: PM authorization 2026-04-26 ~16:10 PT
---

# #1004 Filed + Contract Draft v0.1 Published

## TL;DR

- **#1004 filed**: <https://github.com/mediajunkie/piper-morgan-product/issues/1004>
- Title: "BoundaryEnforcer: replace substring detector with semantic LLM detector (Fix B+C1, sibling to #1002)"
- Labels: `bug`, `priority: critical`, `component: ai`
- 6 ACs from Architect's #1002 followup + optional 7th (PERSONAL/DATA_PRIVACY parity, marked under-discussion)
- Cross-reference comment posted on #1002
- **Contract draft v0.1**: `dev/2026/04/26/1004-implementation-contract-draft.md` — DRAFT, awaiting Architect + CXO reviews
- **Standing by on**: Architect review of contract (esp. severity-field open Q); CXO prompt-body authoring within the schema

## What's in the contract

Single source of truth for:

- **Architecture diagram**: literal-trigger fast-path → semantic detector → floor backstop. Gate position unchanged at universal entry; only the detector inside the gate changes.
- **Integration point**: `services/intent/intent_service.py:631`, no change to `enforce_boundaries` call signature from caller's view.
- **Interface contract**: `BoundaryEnforcer.enforce_boundaries` (existing, behavior-changed); new `SemanticBoundaryDetector` class; `SemanticDetectorOutput` JSON schema with Pydantic validation.
- **Threshold tiers**: 0.85 block / 0.6–0.85 ambiguous / <0.6 pass — app-layer constants, tunable without redeploy.
- **Audit envelope additions** (Fix C1): `detector`, `decision_tier`, `semantic_confidence`, `semantic_reasoning` fields on `audit_data`.
- **Three operator-distinguishable signals**: BoundaryEnforcer-fired (literal-trigger | semantic), floor-with-denial-mode, floor-with-implicit-ethics (Phase 2).
- **Cache contract**: in-memory LRU 1024 entries MVP; composite key + persisted cache deferred.
- **Prompt contract**: schema-first; CXO authors body within schema.
- **Refusal-to-classify behavior**: detector failure → conservative `violation_detected: false` (no false positives from infra failure).
- **Telemetry Phase 1 fields**: structured log on every `enforce_boundaries` call with detector path, category, confidence, tier, latency, cache_hit, fast_path_hit.
- **Phase 2 heuristic**: `category=="unknown" AND floor_hit==true` (structural, not action-label substring).
- **Probe set outline**: 3+ probes per BoundaryType, mix of literal/naturally-phrased, anchored on Phase E + diagnostic cases.
- **Sequencing**: 9 steps, ~5–7 days total from authorization.

## What the contract does NOT decide

- **Severity field** (Architect open Q — leaning confidence-only for MVP, named explicitly in contract)
- **Prompt body** (CXO authors)
- **Probe set content** (separate working doc, parallel)
- **ADR-061 narrative** (Architect, after contract stable)
- **Phase 2 telemetry implementation details** (deferred)

## Asks

### Architect

1. **Read the contract**: `dev/2026/04/26/1004-implementation-contract-draft.md`
2. **Name the severity-field call**: keep schema as `{violation_detected, category, confidence, reasoning, redirect_hint}` (confidence-only, app-layer threshold logic), or add `severity: "block" | "ambiguous" | "pass"` field for prompt-derived tier? Lead Dev lean: confidence-only for MVP. If you concur, contract goes to v1.0 (stable). If you name severity field, contract iterates to v0.2 + we revise.
3. **Anchor ADR-061 on contract** when stable. No rush — build can begin against v1.0; ADR can lag the implementation contract.

### CXO

1. **Read the schema** (Section: `SemanticDetectorOutput`)
2. **Begin authoring the prompt body** that produces this schema. Inputs: `message`, `context`. Output: must conform to schema. Keep `reasoning` audit-only (never user-facing). Keep `redirect_hint` neutral (no quoting matched patterns or user content).
3. **No need to wait for severity-field decision** — schema's `confidence` + `category` fields are stable regardless. If Architect names severity, that's an additive field; doesn't invalidate prompt-body work.

### PM

FYI only. #1004 filed, contract drafted, B+C1 design start work underway. ~5–7 days from today's authorization to ship. Will route updates at: (a) contract v1.0 stable, (b) build phase begins, (c) probe set passes, (d) ready to merge.

## Cleanup

- Working doc filed
- Memo routed per per-memo norm
- Will commit + push immediately

— Lead Dev, 2026-04-26
