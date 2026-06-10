---
to: Architect (Chief Architect)
from: Lead Developer
cc: CEO (xian), PPM (Principal Product Manager), CXO (Chief Experience Officer), PA (Piper Alpha)
date: 2026-06-07
subject: #1124 Phase 4 plan ready for ratification — 2 decisions (source_type location; hybrid transition) + verified audit-cascade + shim spec
priority: medium — ratify the 2 decisions; build stays gated until you do
response-requested: ratify Q1 (source_type → intent.context) + Q2 (hybrid: big-bang prompt + shim-then-migrate consumers), or adjust. PM has reviewed + approved the plan.
---

# Phase 4 plan — your ratification on 2 decisions

Full plan (PM-reviewed + approved 2026-06-07): `docs/internal/architecture/current/phase-4-classifier-canonicalization-plan-1124.md`. Two decisions need your architectural sign-off; everything else is grounded.

## Decision 1 — `source_type` location → `intent.context` (for Phase 4)
The working `_handle_summarize` precedent (`intent_service.py:8336`) already reads `intent.context.get("source_type")` with `valid_sources=[github_issue, commit_range, text]`. Phase 4 has the classifier POPULATE that same `intent.context["source_type"]` → zero handler churn, lowest risk. **Divergence from the amendment** (which said `intent.slots`) is deliberate + flagged for revisit (**#1175**): if/when the slot-filling work (#1121 family) unifies extracted params under `intent.slots`, source_type migrates there. **Asking you to ratify context-for-now + the #1175 revisit path.**

## Decision 2 — transition → HYBRID (PM-confirmed)
- **Big-bang the classifier prompt** (atomic — a prompt can't be half-flipped; gated by canonical-retest before merge).
- **Shim-then-migrate the consumers**: a `verb + source_type → legacy-action` shim (`verb_sourcetype_to_legacy_action()` in `action_registry.py`) keeps all consumers working unchanged; migrate them off legacy aliases one discrete commit at a time, retire the shim last. **This is your layer-then-migrate, applied to the prompt-vs-consumers split.** Asking you to ratify the hybrid + the shim approach.

## Grounding — verified audit-cascade (methodology-30, pre-implementation)
Background sweep + my spot-check found **6 behavior-driving consumers** of `intent.action` (+ ~50 test assertions), ~80 action strings (~38 mapped, 60+ alias sprawl):
1. **`_handle_query_intent` elif chain** — `intent_service.py:2159–2271`, 34 branches, 40+ query aliases (the big one).
2. action-dispatch rail — `get_action_workflows()` (empty today) = the migration target.
3. `conversation_handler.py` — greeting/farewell/thanks/clarification_needed.
4. **`lens_inference.py` `ACTION_TO_LENS`** — ~30 action keys → lens (this one the Phase-3 coverage analysis missed; the cascade caught it).
5. `file_resolver.py` — `intent.action.split("_")` keyword extraction (data-use; shim feeds legacy string so it's unchanged — a bare verb would yield fewer keywords).
6. `honest_failure.py` — display humanize (shim-transparent).

**Why hybrid is the right call**: big-bang touches all 6 + ~50 tests at once; shim-then-migrate has no blocking risk and moves one commit at a time. The cascade is what made the shim's exact shape specifiable (it must satisfy all 6 consumers).

## Not blocking your ratification (Lead Dev build-prep)
2 Phase-0 items I'll close before building: full classifier-prompt/parse read, and confirming the canonical-retest actually covers the category-routed action space (gate blind-spot check). **No build until you ratify Q1+Q2.**

— Lead Dev
