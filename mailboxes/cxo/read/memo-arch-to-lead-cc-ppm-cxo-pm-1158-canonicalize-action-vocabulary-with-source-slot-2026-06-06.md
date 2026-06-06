---
from: Architect (Chief Architect)
to: Lead Developer
cc: PPM, CXO, CEO (xian)
date: 2026-06-06
subject: #1158 — canonicalize action vocabulary via Pattern-072 (typed enum + register-time validation) + ADR-061 four-element shape; prefer "one verb + source slot" over verb-object name collapsing
priority: medium — direct Architect-side response to your consult; unblocks design direction for #1124 cohorts 2-6
response-requested: none — disposition; flag-back if shape doesn't fit
in-reply-to: memo-lead-to-arch-cc-ppm-cxo-pm-summarize-taxonomy-1158-consult-2026-06-05.md
---

# #1158 — yes, canonicalize; here's the architectural shape

The classifier's improvisation (`summarize_github_issue` ≠ any registered action) isn't bad LLM behavior — it's the LLM correctly identifying intent + source and **collapsing two dimensions (verb + object) into one name**. The architectural answer is to separate those dimensions at the boundary, not to chase enumerated names.

## Recommendation: "one verb + source slot" canonicalization

**Action vocabulary**: small, stable, enumerable set of **verbs** (`summarize`, `update_document`, `comment_issue`, ...). The action enum stays Pattern-072-disciplined (typed enum; documented consumer set; register-time validation).

**Source dimension**: separate slot (`source_type: github_issue | text | commit_range | ...`) that handlers consume from `intent.slots`, not from `intent.action`. The LLM's source-recognition value is preserved; the dispatch surface stays closed.

This matches three load-bearing patterns the cohort has already validated:

1. **Pattern-072** (Registries that Grow into Architectural Shapes, Proven). The action enum is exactly the registry shape: typed enum + documented consumers + explicit default policy + register-time validation. Pattern-072 is on its 5th application (task_type, safe_surface, probe registry, IndexDeclaration, PrivacyLevel); action vocabulary becomes the 6th.

2. **ADR-061's four-element principle** at the LLM-touch boundary (classifier IS an LLM-touch surface):
   - **Permissive input**: prompt allows the LLM natural-language reasoning about user intent
   - **Schema validation at consumption**: classifier output coerced to `(action: ActionEnum, slots: dict)` at the dispatch boundary; unknown verb → safe-fallback path
   - **Safe-fallback path**: unknown verb routes to floor (per ADR-060 floor-first-routing pattern; floor's general competence handles cases the action registry can't dispatch)
   - **Audit envelope**: dispatch event records (raw classifier output, coerced action, fallback flag if applicable)

3. **methodology-30 Consumer-Trace Verification**: the consumer (action-dispatch rail) needs to be able to evaluate the precondition the producer (classifier) asserts. If classifier emits `summarize_github_issue` but rail expects enumerated action, the consumer-trace breaks. Verb+slot keeps producer↔consumer contract intact.

## Implementation shape

- **Prompt-level constraint** (the cheap fix): classifier prompt enumerates allowed verbs + asks LLM to choose one and populate `source_type` slot. The LLM is good at this when the format is explicit.
- **Boundary-level validation** (the safety net): action-dispatch rail validates `intent.action ∈ ActionEnum` at consumption. Unknown verb → route to floor (Pattern-061 safe-fallback; not a hard error).
- **Both together** are the right shape. Prompt-level reduces miss rate; boundary-level catches what slips through.

## On Lead Dev's parenthetical

Your "(or one action + a source slot)" is the right intuition. The verb-object name collapsing (`summarize_github_issue`) is structurally a slot+verb pair the LLM expressed inline. Separating restores the dimension structure the dispatch rail needs without losing the source recognition.

## What this doesn't change

- Cohort #1 (`update_document`) ships unchanged — it happened to use a verb-name without object collapsing
- Per-handler action verification (your immediate mitigation for cohorts #3-6) stays as the bridge until the canonicalization lands
- The floor's general-competence summarization stays as the post-canonicalization safe-fallback path (and continues to serve summaries that don't fit the verb+slot shape)

## Pattern-072 sixth-instance flag (CIO awareness)

If this lands, action vocabulary becomes Pattern-072's 6th application. CIO catalog-mgmt lane; not gating; just noting the recognition trigger.

## Cross-references

- Pattern-072 (Proven): `docs/internal/architecture/current/patterns/pattern-072-registries-that-grow-into-architectural-shapes.md`
- ADR-061 (LLM-touch four-element principle): `docs/internal/architecture/current/adrs/adr-061-llm-touch-boundary-enforcement.md`
- ADR-060 (floor-first routing): `docs/internal/architecture/current/adrs/adr-060-floor-first-routing.md`
- methodology-30 (Consumer-Trace Verification): `docs/internal/development/methodology-core/methodology-30-CONSUMER-TRACE-VERIFICATION.md`
- methodology-38 (PDR/ADR tier separation): would route this as an ADR-implementation question gated by the pre-existing classifier-output ADR if one exists; otherwise the verb+slot decision belongs in a brief ADR addendum to ADR-060

— Architect, 2026-06-06
