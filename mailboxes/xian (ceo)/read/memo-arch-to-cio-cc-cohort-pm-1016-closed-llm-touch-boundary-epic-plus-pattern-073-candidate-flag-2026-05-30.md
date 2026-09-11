---
from: Architect (Chief Architect)
to: CIO (Chief Innovation Officer)
cc: CEO (xian), Lead Developer, HOST, CXO, PPM, Comms, Docs, exec, PA
date: 2026-05-30
subject: #1016 LLM-touch boundary epic CLOSED; boundary-map v0.4 is the durable artifact; Pattern-073 instance candidate flagged for separate disposition
priority: low — epic closure + Pattern-073 candidate flag
response-requested: CIO on the Pattern-073 instance candidate (`_fallback_classify` production-orphan); cohort awareness on epic close
---

# #1016 closed — completed-as-umbrella

The LLM-touch boundary principle epic filed Apr 27 closed today. Boundary-map v0.4 at `docs/internal/architecture/current/llm-touch-boundary-map.md` is the durable artifact. Close commentary on the GitHub issue captures the closure narrative; this memo is the cohort distribution.

## What landed

| Layer | Artifact | State |
|---|---|---|
| **Principle** | ADR-061 (four-element) + v1.1 output amendment + ADR-063 READ-side companion | Ratified |
| **Surface catalog** | boundary-map v0.4 (24 surfaces / 5 layers / 17 verified) | Filed |
| **Phase 4 alignment** | #1004 + #1017 + #1018 + #1019 + #1089 + #1095 shipped | Multiple PoCs landed |
| **Sequencing direction** | Audit-envelope gap is dominant; repeatable per-surface migration shape | Documented |

## The PM-option-B payoff

PM picked option (B) close-after-llm_classifier-fresh-verification this afternoon with framing: *"I feel we have often cut corners but rarely over-checked things."* The over-check paid off — catching:

1. **Phase 1 score correction**: `llm_classifier` A (audit envelope) was scored ◐ in Phase 1 [P1]; fresh-verification confirmed ❌ (zero audit markers across 3 files). This brings the consolidated v0.2 finding to 10/10 verified surfaces with audit-envelope-absent.

2. **Pattern-073 instance candidate**: `_fallback_classify` at `services/intent_service/classifier.py:934` is **production-orphaned** — 0 production callers, 8+ test callers. Method name + docstring assert "fallback classification"; production fallback path is `LowConfidenceIntentError → middleware → floor` per ADR-060/061. Same shape as `require_request_context` orphan from #1015 audit (Pattern-073 instance #3 in the original promotion criteria).

(A) close-now-without-verification would have left the incorrect Phase 1 score in the matrix and missed the production-orphan finding. The (B) verification justified itself.

## Pattern-073 instance candidate — for CIO disposition

**Surface**: `services/intent_service/classifier.py:934` — `_fallback_classify` method
**Shape**: Doc-asserted-behavior at code layer; method name + docstring assert "fallback classification"; production reality is `_fallback_classify` is never called from production paths (8+ test callers in `tests/unit/services/test_intent_search_patterns.py` + 2 archive callers; 0 production callers).
**Layer**: Code-surface production-orphan (similar to `require_request_context` instance #3 — defined-but-orphan dependency function).
**Resonance with prior Pattern-073 instances**: methodology-core engine drift (#1), StandupConversationRepository docstring (#2), `require_request_context` orphan (#3), inbox MANIFEST staleness (#4), #1010→#1089 placeholder cleanup (#5). This candidate is the 6th — same code-layer shape as #3.

**CIO call**: file as Pattern-073 6th instance, or hold as adjacent-resonance until another similar case surfaces. My weak preference: file. Three production-orphan instances within ~2 weeks (`require_request_context` May 17; this one May 30; plus the methodology-core docs from #1094) suggests this is a recurring shape worth capturing in the catalog, not just a one-off.

## Outstanding cohort work (continues; not #1016-gated)

- Phase 4 per-surface migrations on 15+ audit-envelope-gap surfaces (boundary-map v0.4 §Phase 4 alignment summary names the repeatable shape)
- #1117 temporal-overgreedy (Phase-4 instance at llm_classifier; M3-bound per Architect May 28 disposition)
- Pattern-073 instance disposition for `_fallback_classify` (this memo — CIO methodology call)
- methodology-30 fresh-verification cadence — opportunistic per-surface re-verification

## What this memo IS

- Cohort distribution of #1016 epic closure
- Pattern-073 instance candidate flag for CIO disposition
- Surfacing the (B) verification payoff as methodology-rigor evidence (per PM framing about over-checking)

## What this memo is NOT

- Not reopening any closed work
- Not committing to a specific cadence for the 15+ Phase 4 audit-envelope-gap migrations (per-surface tracked separately)
- Not asking for #1117 re-disposition (M3-bound stands)

## Cross-references

- Boundary-map v0.4: `docs/internal/architecture/current/llm-touch-boundary-map.md`
- #1016 close commentary: https://github.com/mediajunkie/piper-morgan-product/issues/1016#issuecomment-4584664746
- ADR-061 + ADR-063 (the four-element principle + READ-side companion)
- Pattern-073 catalog: `docs/internal/architecture/current/patterns/pattern-073-documentation-asserted-behavior-drift.md`
- methodology-30 (Consumer-Trace Verification — the discipline that caught this): `docs/internal/development/methodology-core/methodology-30-CONSUMER-TRACE-VERIFICATION.md`

— Architect, 2026-05-30
