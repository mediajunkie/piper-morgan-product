# #1004 Implementation Contract — v1.0 (Stable)

**Status**: STABLE v1.0 — cleared by Architect 2026-04-26 ~17:00 PT (severity-field locked confidence-only; 3 refinements applied)
**Author**: Lead Developer (code-opus)
**Date**: 2026-04-26 (v0.1 16:20 PT; v1.0 17:30 PT)
**Refs**: #1004, #1002, #992, ADR-061 (Architect drafting post-v1.0), Pattern-045 (component layer)

## Changelog
- **v1.0** (17:30): Architect 3 refinements applied — (1) AC #7 promoted to required (5-category scope already committed); (2) `semantic_reasoning` audit semantics clarified; (3) C1 detector-marker sequenced before semantic build. CXO prompt body v0.1 received and schema-conformant.
- **v0.1** (16:20): Initial draft.

## Purpose

Define the implementation contract — interface signatures, integration point, audit envelope, telemetry shape — that B+C1 must satisfy. Stable enough that:

1. Architect can anchor ADR-061 draft on this.
2. CXO can author the prompt body within the schema this defines.
3. Build phase has a single source of truth for what "done" looks like.

This is **design**, not code. No `services/` files modified yet.

## Scope

- **In scope (Fix B)**: Semantic detector that replaces substring matchers in `boundary_enforcer_refactored.py` for the 5 BoundaryType categories. Runs before intent classification at universal entry.
- **In scope (Fix C1)**: BoundaryEnforcer demoted to literal-trigger fast-path. Audit envelope adds `detector` discriminator. Floor remains backstop.
- **In scope (Telemetry Phase 1)**: Structured logging on `enforce_boundaries` calls (detector path, category, confidence, decision, latency).
- **Out of scope (this contract)**: Telemetry Phase 2 FLOOR_IMPLICIT_ETHICS counter (separate filing). Probe set construction (#1004 AC5; separate working doc). ADR-061 narrative (Architect).

## Architecture: two-layer detector + floor backstop

```
User message
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│ Layer 1: Literal-trigger fast-path (current substring impl) │
│   - Cheap, deterministic, fast                              │
│   - Catches obvious cases that quote literal trigger words  │
│   - audit_data.detector = "literal-trigger"                 │
└────────────┬────────────────────────────────────────────────┘
             │ no fast-path hit
             ▼
┌─────────────────────────────────────────────────────────────┐
│ Layer 2: Semantic LLM detector (new, Fix B)                 │
│   - Structured JSON output (schema below)                   │
│   - confidence-tiered: 0.85+ block / 0.6–0.85 ambiguous /   │
│     <0.6 pass                                               │
│   - audit_data.detector = "semantic"                        │
└────────────┬────────────────────────────────────────────────┘
             │ violation_detected (either layer)
             ▼ (existing path, unchanged from #992 Phase C)
       Floor LLM (denial_mode=True, redirect_context hint)
       composes decline voice
```

The **gate position** (universal entry, before intent classification) is **unchanged**. We're swapping the detector inside the gate, not moving the gate.

## Integration point

**File**: `services/intent/intent_service.py`
**Line**: ~631 (call site to `boundary_enforcer_refactored.enforce_boundaries`)
**Flag**: `ENABLE_ETHICS_ENFORCEMENT` (env var, currently default `false`)

No change to call signature from `intent_service`'s perspective. The two-layer dispatch happens **inside** `BoundaryEnforcer.enforce_boundaries`. From the caller's view, it remains:

```python
ethics_decision: BoundaryDecision = await boundary_enforcer_refactored.enforce_boundaries(
    message=message,
    session_id=session_id,
    context={...},
)
```

## Interface contract

### `BoundaryEnforcer.enforce_boundaries` (existing, behavior-changed)

**Signature** (unchanged):
```python
async def enforce_boundaries(
    self,
    message: str,
    session_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> BoundaryDecision
```

**New internal flow**:
1. Run literal-trigger fast-path (existing substring checks). If hit → return `BoundaryDecision` with `audit_data.detector = "literal-trigger"`.
2. Else run semantic detector (`SemanticBoundaryDetector.detect`, new). If `confidence >= 0.85` → return with `audit_data.detector = "semantic"`. If `0.6 <= confidence < 0.85` → return as ambiguous-pass (no violation, but log telemetry tier). If `< 0.6` → return as no-violation.

### `SemanticBoundaryDetector` (new)

```python
class SemanticBoundaryDetector:
    def __init__(
        self,
        provider: LLMProvider,           # default: floor's model_tier
        cache: Optional[LRUCache] = None, # in-memory MVP
        prompt: SemanticDetectorPrompt,   # CXO authors content; schema below
    ): ...

    async def detect(
        self,
        message: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> SemanticDetectorOutput: ...
```

### `SemanticDetectorOutput` (structured JSON from LLM)

```json
{
  "violation_detected": true | false,
  "category": "harassment" | "professional" | "personal" | "data_privacy" | "inappropriate_content" | "none",
  "confidence": 0.0,
  "reasoning": "brief explanation (audit-only, never user-facing)",
  "redirect_hint": "category-derived neutral hint" | null
}
```

**Open question for Architect**: severity field separate from confidence? Lead Dev leaning **confidence-only for MVP** per #1002 followup; threshold logic stays app-layer. If Architect names a strong preference, this contract updates.

**Validation**: parse to Pydantic model with category enum; reject (treat as detector-failure → fallback to floor) if schema violated.

### Threshold tiers (app-layer)

```python
BLOCK_THRESHOLD = 0.85
AMBIGUOUS_THRESHOLD = 0.6

def classify_decision(confidence: float) -> str:
    if confidence >= BLOCK_THRESHOLD: return "block"
    if confidence >= AMBIGUOUS_THRESHOLD: return "ambiguous"
    return "pass"
```

Tunable as constants; no redeploy needed for prompt-level changes.

## Audit envelope additions (Fix C1)

Existing `BoundaryDecision.audit_data` gains:

```python
audit_data = {
    # ... existing fields ...
    "detector": "literal-trigger" | "semantic",  # NEW (#1004 AC2)
    "decision_tier": "block" | "ambiguous" | "pass",  # NEW (telemetry)
    "semantic_confidence": float | None,  # NEW (semantic path only)
    "semantic_reasoning": str | None,  # NEW (semantic path only); persisted to ethics audit log for ops review; NEVER user-routed; complements existing audit_explanation field (#992 Phase C)
    # ... rest of existing fields ...
}
```

Three operator-distinguishable signals after this ships:
1. **BoundaryEnforcer fired (literal-trigger or semantic)** — audit envelope present, `detector` field tells which
2. **Floor handled with `denial_mode=True`** — semantic detector caught it, floor performed the decline (existing path)
3. **Floor handled with `denial_mode=False` but ethics-shaped action label** (FLOOR_IMPLICIT_ETHICS, Phase 2) — invisible ethics work case

## Cache contract (MVP)

**Strategy**: in-memory LRU keyed on `hash(message)`.
**Size**: 1024 entries (tunable).
**TTL**: process-lifetime (no eviction beyond LRU pressure).
**Post-MVP** (deferred): composite key with model-version; persisted cache.

## Prompt contract (CXO authors body)

CXO writes the prompt body. The contract here is the **schema** the prompt must produce, plus the **input shape**:

**Input**:
- `message`: user content (raw, no preprocessing)
- `context`: optional dict (source, session metadata — NEVER user PII)

**Output**: must conform to `SemanticDetectorOutput` JSON schema above.

**Refusal-to-classify behavior**: if the LLM cannot classify (e.g., schema violation, timeout), the contract treats it as `violation_detected: false, confidence: 0.0` and the literal-trigger result (if any) governs. This is conservative: no false positives from detector failure.

## Telemetry Phase 1 (ships with B)

Structured log fields on every `enforce_boundaries` call:

```python
ethics_logger.info(
    "boundary_enforcement",
    extra={
        "decision_id": decision_id,
        "session_id": session_id,
        "detector": detector,                  # "literal-trigger" | "semantic" | "none"
        "violation_detected": violation_detected,
        "boundary_type": boundary_type,        # category or None
        "decision_tier": decision_tier,        # "block" | "ambiguous" | "pass"
        "confidence": confidence,
        "latency_ms": response_time_ms,
        "cache_hit": cache_hit,                # semantic path only
        "fast_path_hit": fast_path_hit,        # literal-trigger short-circuit
    },
)
```

**Phase 2** (within 2 weeks of Phase 1): FLOOR_IMPLICIT_ETHICS counter using structural heuristic `category=="unknown" AND floor_hit==true` (per Lead Dev #1002 followup refinement; not substring-matching action labels).

## Probe set (regression coverage; AC5)

Separate working doc — outline:
- 3+ probes per BoundaryType (HARASSMENT, PROFESSIONAL, PERSONAL, DATA_PRIVACY, INAPPROPRIATE_CONTENT) = 15+ probes
- Mix of literal-trigger-matchable and naturally-phrased
- Includes S1 r2, V1, V2, V3, S2 from Phase E/diagnostic record as anchor cases
- Each probe annotated with: expected detector, expected category, expected tier, expected user-facing redirect shape

## What this contract does NOT decide

- **Severity field** (Architect open question)
- **Prompt body** (CXO authors)
- **Probe set content** (separate working doc, parallel filing)
- **ADR-061 narrative** (Architect drafts after this contract is stable)
- **Phase 2 telemetry implementation details** (separate working doc when Phase 1 is in)

## Sequencing

1. ✅ Issue filed (#1004)
2. ✅ Contract draft v0.1 (~25 min)
3. ✅ Architect review — severity-field locked confidence-only; 3 refinements applied
4. ✅ CXO authors prompt body v0.1 (`dev/2026/04/26/1004-prompt-body-draft-v0-1.md`)
5. ⏳ **Build C1 detector-marker** (additive change to `audit_data["detector"] = "literal-trigger"`); ~0.5 day — sequenced FIRST per Architect refinement #3 (decouples C1 audit envelope from B build, gives operators discriminator from day one)
6. ⏳ Build B (semantic detector + integration); ~3 days
7. ⏳ Build telemetry Phase 1; ~0.5 day
8. ⏳ Probe set + regression with calibration round (CXO reviews divergences → prompt v0.2 → repeat 1–2x → stable); ~1–2 days
9. ⏳ Ship; #1002 closes; #992 Phase F gate re-evaluates against PPM v4 conditions

Total: ~5–7 days from authorization. Authorized 2026-04-26 ~16:10 PT. v1.0 contract stable 17:30 PT. Build phase begins next.

## Post-ship enhancement (logged, not blocking)

Per Architect: **calibration-window mode** where semantic runs alongside literal-trigger (parallel, log-only) for ~7–14 days post-ship to surface literal-trigger false positives (especially PROFESSIONAL pattern-word over-firing). Disagreements (literal says violation, semantic says no) feed a metrics counter for substring-pattern tuning. Not in #1004 scope; file as follow-up after ship.

## Standing by

This contract is published as DRAFT. Awaiting:
- Architect read on severity-field question
- CXO read on prompt-body authoring
- Any contract refinements before build phase begins

— Lead Dev, 2026-04-26
