# Phase 4 — Classifier-Prompt Canonicalization: Flywheel Planning (#1124)

**Status**: PLANNING — Phase -1 (investigation) ✅, decisions ✅ (Q1–Q4, PM 2026-06-07; Q1+Q2 pending Arch ratification), **audit-cascade ✅ (verified)**, shim spec drafted. Remaining: 2 Phase-0 research items (full classifier-prompt/parse read; canonical-retest coverage confirm) + Arch ratification package. **Gated phase, high blast radius.** Planning precedes any build.

**Lineage**: ADR-060 amendment (layer-then-migrate, Arch-ratified 2026-06-06) → Phase 2 (Verb enum, shipped `e7fd12ee0`) → Phase 3 (observability, shipped `3a7e52aa6`) → **Phase 4 (this)** → Phase 4.x (enforce-floor, after Phase 4 stabilizes).

## What Phase 4 is

Constrain the LLM classifier to emit a canonical **VERB** (the Phase-2 `Verb` enum) + populate a **`source_type`** slot, instead of improvising collapsed action names (`summarize_github_issue`, `add_comment_to_issue`, …). Gated by canonical-retest (Run-N baseline before/after). After Phase 4 confirms canonical-verb-only traffic, enforce-floor (Phase 4.x) becomes safe.

## Phase -1 — VERIFIED FACTS (2026-06-07)

### 1. The change point
`services/intent_service/llm_classifier.py::_build_classification_prompt` (L345). Current prompt opens: *"You are an expert PM assistant classifying user intents. Classify the following message into an intent category and action."* — **action is free-form** → this is the improvisation source. Phase 4 constrains it to a registered VERB + asks the LLM to populate `source_type`.

### 2. `source_type` precedent (grounding + a reconciliation to settle)
`intent_service.py:8336` (`_handle_summarize`, marked FULLY IMPLEMENTED) **already** reads `source_type = intent.context.get("source_type")`, with `valid_sources = ["github_issue", "commit_range", "text"]` and a `source_type_required` clarification. So the **consumer side of `source_type` exists**; the classifier simply does not POPULATE it yet.
- ⚠️ **RECONCILIATION (decision needed)**: the ADR-060 amendment says source lives in `intent.slots`; this working handler reads `intent.context["source_type"]`. Phase 4 must pick one — populate `intent.context` (match the working precedent, lowest-risk) OR `intent.slots` (+ migrate the handler). Lean: match precedent unless slots has a concrete reason.

### 3. The gate (canonical-retest)
Harness exists: `dev/2026/03/12/canonical-retest-884.py` (+ results CSV + report), `tests/e2e/test_canonical_conversations.py`, `dev/2026/04/11/canonical-retest-m1-report.md`. Phase 4 runs it before + after the prompt change and diffs. [Phase 0 TODO: confirm current run number ("Run-12 baseline"), invocation, pass bar, and whether it exercises the category-routed actions.]

### 4. Blast-radius seed (from the Phase 3 coverage analysis)
Consumers key on action **strings**: the `intent_service.py` category-routing elif chains handle ~40+ alias actions (`search_documents`, `summarize`, `prioritize`, `stale_prs`, `review_issue`, `analyze_commits`, `show_standup`, …). When the classifier emits canonical VERBS instead, every consumer keying on a legacy alias must be updated, shimmed, or retired. **This is the high-blast-radius core.**

## Remaining flywheel work

### Phase 0 — research (grounding + precedent)
- [ ] Read the full `_build_classification_prompt` + the LLM **response parsing** (how `category`/`action` are extracted) — to know exactly what to constrain + how `source_type` would be parsed back.
- [ ] Confirm canonical-retest invocation + pass bar + scenario coverage (does it cover the category-routed actions? if not, the gate has a blind spot).
- [ ] Precedent: how prior prompt/classifier changes were gated + rolled (the 884 retest, the m1 retest).
- [ ] Consume the **Phase-3 observability stream** (`action_verb_unregistered`) as the backlog input — which actions actually occur → which verbs + source_types the prompt must enumerate.

### Audit-cascade — COMPLETE (2026-06-07; background sweep + spot-verified by Lead Dev)

**6 behavior-driving consumers** of `intent.action` (+ ~50 test assertions that must stay green). ~80 distinct action strings consumed; ~38 in `ACTION_TO_VERB`, **60+ alias sprawl** not yet mapped.

| Consumer | Location (verified) | Keys on | Migration disposition |
|----------|--------------------|---------|----------------------|
| **`_handle_query_intent` elif chain** (THE big one) | `intent_service.py:2159–2271` (34 `intent.action` branches) | 40+ query aliases (`search_documents`, `shipped_*`, `stale_prs*`, `close_issue*`, `list_*`, `meeting_time*`, `productivity*`, `show_standup`, …) | shim now → migrate each action to the workflow-rail one commit at a time |
| **action-dispatch rail** | `workflow_dispatcher.get_action_workflows()` + `intent_service.py:1201` | registered action-triggered workflows (empty today) | the migration **TARGET** (register verbs here) |
| **conversation_handler** | `conversation_handler.py:64+` | `greeting`/`farewell`/`thanks`/`clarification_needed` | shim (4 actions) |
| **lens_inference `ACTION_TO_LENS`** | `lens_inference.py:25,99` | ~30 action keys → ConversationalLens | shim now; rekey to verbs in migrate-phase |
| **file_resolver (DATA use, not branching)** | `file_resolver.py:254,362` `intent.action.split("_")` | any action | ⚠️ shim feeds the legacy string so `split("_")` keyword extraction is unchanged; a bare verb would yield fewer keywords |
| **honest_failure (display)** | `honest_failure.py:139` humanize | any | shim-transparent |

**Why the hybrid is validated**: a big-bang flip would change all 6 consumers + ~50 tests at once. Shim-then-migrate has **no blocking risk** — the shim preserves every consumer; migration is one discrete commit each.

### Shim spec (the Q2 mechanic, derived from the cascade)
`verb_sourcetype_to_legacy_action(verb: Verb, source_type: str|None) -> str` in `action_registry.py`: the disambiguating inverse map (`verb [+ source_type]` → the single legacy action string all consumers already understand). Classifier emits `verb + source_type` → shim translates at the boundary → all 6 consumers + the ~50 tests run unchanged. Then migrate consumers off the legacy strings incrementally (elif chain → workflow rail; `ACTION_TO_LENS` keys → verbs; `file_resolver` → read verb+source_type), retiring the shim last. *Note: the map is verb(+source)→one-action; where one verb collapsed multiple aliases, source_type (or the dominant alias) disambiguates — to be finalized when authoring the map.*

### Gate plan
- [ ] Baseline canonical-retest → apply prompt change → re-run → diff. Pass bar: no canonical-conversation regressions AND the Phase-3 stream shows targeted actions now emitting canonical verbs.

## Decisions (PM discussion 2026-06-07; Q1+Q2 pending Arch ratification)

1. **`source_type` location → `intent.context`** for Phase 4 (matches the working `_handle_summarize` precedent = zero handler churn). **FLAGGED for revisit** (issue **#1175**): `intent.slots` is semantically cleaner and source_type would naturally migrate there if/when the slot-filling work (#1121 family) unifies extracted params under `intent.slots`. Not a Phase-4 blocker. → Arch ratifies.
2. **Transition → HYBRID** (PM-confirmed): **big-bang the classifier prompt** (atomic — a prompt can't be half-flipped; gated by thorough + creative canonical-retest before merge) **+ shim-then-migrate the consumers** (a `verb + source_type → legacy-action` shim keeps the ~40 consumers working unchanged; migrate them off the aliases one discrete commit at a time, retire the shim last). Consistent with Arch's ratified layer-then-migrate. → Arch ratifies. ⚠️ Shim's exact mapping = an output of the audit-cascade (below).
3. **Verb/source_type enumeration → data-driven** (with PM input): derive the prompt's advertised verbs + source_types from the Phase-2 `Verb` enum + the Phase-3 `action_verb_unregistered` backlog stream — not hand-picked.
4. **Retest pass bar → must confirm coverage**: verify the canonical-retest actually exercises the category-routed action space; if it doesn't, the gate has a blind spot to close before relying on it.

## Why planning-first (no build yet)
High blast radius (every LLM-classified intent's naming changes) + gated. The audit-cascade must enumerate consumers + settle the transition strategy BEFORE touching the prompt, or we repeat the Phase-3 spec-gap surprise at a larger scale. This doc is the grounding artifact; Arch ratified the *shape*, this plans the *execution*.

---
*Author: Lead Developer, 2026-06-07. Living doc — accretes through the flywheel. Phase -1 grounded in verified code reads (cited above); Phase 0 + audit-cascade pending.*
