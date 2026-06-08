# Phase 4 — the verb→action shim is *permanent* infrastructure, not scaffolding (request DDD ratification)

**From**: Lead Developer
**To**: Chief Architect
**CC**: PM, Piper Alpha
**Date**: 2026-06-08
**Re**: #1124 Phase 4 · ADR-060 "layer-then-migrate" step-4 amendment
**Response requested**: ratify (or push back on) the shim-as-permanent-boundary framing for the DDD architecture, at your cadence.

---

## TL;DR

Building Phase 4 step 3 (consumer migration) surfaced a code-grounded finding that **amends the ratified endgame**: the `verb_sourcetype_to_legacy_action` shim **cannot be fully retired** (ADR-060 layer-then-migrate step 4). It becomes **permanent architecture** — the deliberate verb↔action translation boundary — because some consumers intentionally need *action-granularity* that the (correctly coarse) verb vocabulary cannot carry. PM has seen this and it "seems right" to him; sending for your ratification so it's captured in the DDD model rather than living as an undocumented exception.

**We still migrate every consumer we can** (dispatch consumers → action-rail, to reduce elif-chain complexity). The shim stays only for the consumers that genuinely need the fine-grained action.

## What shipped (both gated green, on origin/main)

- **Step 2 — prompt flip** (`1d70dfd19`): classifier emits canonical `verb` + `source_type`; boundary canonicalizes `intent.action` via the shim when mappable, free-form fallback otherwise. 61-query canonical-routing diff IDENTICAL; 114 unit tests green.
- **Step 3 cohort 1 — CLOSE/REOPEN/COMMENT** (`5e385c541`): issue-mutation cohort migrated elif→action-dispatch-rail (same recipe as `update_document`/`changes_query`); handlers reused unchanged. Routing diff IDENTICAL; 26 dispatcher tests green.

## The finding (why the shim is permanent)

The verb vocabulary is **intentionally coarse** (GET/LIST/ANALYZE/CLOSE/…). That is correct for classification. But two consumers branch on the **fine-grained action**, and the verb cannot reconstruct what they need:

1. **`lens_inference.ACTION_TO_LENS`** maps `meeting_time`→CALENDAR, `list_issues`→ISSUES, `project_status`→PROJECTS. These share verbs (GET/LIST) but resolve to **different conversational lenses**. Keying on the verb would over-collapse — the exact GET/LIST concern we earlier thought the pre-classifier short-circuit "dissolved." It didn't dissolve; it relocated here.
2. **`file_resolver`** does `intent.action.split("_")` for keyword extraction. A bare verb yields fewer keywords than `list_milestones_query`.

Both need the *action string*, not the verb. The shim already feeds it to them. So the shim is the **stable translation layer**, not transitional debt.

## Proposed amendment to ADR-060 (layer-then-migrate)

Step 4 ("retire the shim") becomes **"retire the shim *for dispatch consumers*"**:

- **Dispatch consumers** (the `_handle_query_intent` elif chain) → migrate to the action-rail, one cohort at a time (in progress). For these, the legacy alias eventually disappears from the consumer.
- **Action-granular consumers** (`lens_inference`, `file_resolver`, + any future consumer keying on the specific action/object) → **stay shim-served permanently**. The shim is their supported contract.
- **Phase 4.x enforce-floor** reasoning should treat the shim's legacy-action output as a first-class, permanent surface (an unknown verb still floors per ADR-060 floor-default; that's unchanged).

DDD lens: the shim is an **anti-corruption layer** between the classifier's canonical verb language and the handlers' established action language — a deliberate bounded-context translation, which is exactly the kind of thing that *should* be permanent, not erased.

## The ask

1. Ratify (or correct) "shim = permanent verb↔action ACL for action-granular consumers" for the DDD architecture / an ADR-060 step-4 amendment.
2. Confirm the migration scope: proceed migrating dispatch cohorts (elif→rail) to reduce complexity; leave `lens_inference` + `file_resolver` shim-served. (PM has already greenlit continuing the migrations.)

Plan doc carries this inline: `docs/internal/architecture/current/phase-4-classifier-canonicalization-plan-1124.md` (step-3 section + corrected dispositions table).

— Lead Dev
