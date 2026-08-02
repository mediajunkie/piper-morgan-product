> ⚠️ **STATUS UPDATE 2026-08-02 (#1432 executed)**: the file this plan's flip
> landed in (`llm_classifier.py`) has been **deleted** — it was the orphaned
> PM-034 stack, never on the live chat path (archaeology on #1432). The flip's
> reference implementation is recoverable at commit **`fba6452f0`**; the
> `verb_sourcetype_to_legacy_action` shim survives in `action_registry.py` as
> the re-landing target. **Phase 4's remaining work = re-land the prompt flip
> in the LIVE `classifier.py`**, per Arch condition (ii) (owner: Lead).

# Phase 4 — Classifier-Prompt Canonicalization: Flywheel Planning (#1124)

**Status**: PLANNING ✅ COMPLETE · **Q1+Q2 RATIFIED by Arch 2026-06-07** (`memo-arch-to-lead-...-phase4-plan-ratified-q1q2-2026-06-07.md`) → **BUILD UNBLOCKED**. Phase -1 ✅, decisions ✅, audit-cascade ✅ verified, shim spec ✅, Phase-0 build-prep ✅. Gated phase — build proceeds behind the canonical-retest gate (needs a live `/api/v1/intent` + LLM run, same auth-limit as #1155 UAT). Build order: (1) shim `verb_sourcetype_to_legacy_action()` + tests [solo-safe] ✅ SHIPPED `3c65c7017`; (2) prompt big-bang behind canonical-retest ✅ **SHIPPED `1d70dfd19` (2026-06-08, PM-present)** — 61-query routing diff IDENTICAL before/after (48 pass, 1 pre-existing Q25/M2-Beta fail, 12 env-dependent errors, all constant); 114 unit tests green; (3) migrate consumers off legacy aliases — **IN PROGRESS** (elif→action-dispatch-rail, one cohort each): `update_document` ✅, `changes_query` ✅, **CLOSE/REOPEN/COMMENT cohort ✅**, **GitHub read-query cohort (shipped / stale_prs / review_issue / list_issues / list_prs / list_milestones / list_releases / list_labels / list_branches) ✅ via a parameterized entry-point factory** (both 2026-06-08, gate IDENTICAL). Remaining elif-chain families queue next: search_documents (Notion), calendar (meeting_time / recurring / week), productivity, attention, standup, projects, todos (→execution) — integration-dependent, gate-verify where the corpus covers. Code-grounded refinement: **`lens_inference` + `file_resolver` do NOT verb-migrate** (verbs over-collapse the lens granularity / lose `split("_")` keywords — see table) — they stay action-keyed / shim-served permanently; (4) retire shim for the migrated cohorts → enables Phase 4.x enforce-floor.

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

### Phase 0 — research (grounding + precedent) — ✅ build-prep items closed 2026-06-07

- [x] **Full prompt + parse read** (`llm_classifier.py:345-378` + `_parse_llm_response*`): the prompt emits `{"category","action","confidence","reasoning"}`. **Categories ARE enumerated** (L373: execution/analysis/synthesis/strategy/learning/query/conversation/unknown); **`action` is explicitly free-form** (L374 "Be specific with the action name") = the improvisation source. **No `source_type` field today.** Parser (`_parse_llm_response_resilient`, 6 fallback strategies) extracts the JSON fields. ⇒ **Phase-4 prompt edit is precisely scoped**: add an *enumerated* `verb` field (Phase-2 `Verb` values) + a `source_type` field (valid_sources) to the JSON schema + instructions; the resilient parser change is purely additive (extract two more fields). Build-time field-placement detail: classifier sets `intent.action = verb_sourcetype_to_legacy_action(verb, source_type)` (shim) so consumers see legacy strings unchanged, + stores `intent.context["source_type"]`.
- [x] **Canonical-retest coverage (blind-spot check)** — `tests/e2e/test_canonical_conversations.py`: **covers the category-routed action space** (search_documents, stale_prs, meeting_time, recurring_meetings, comment_issue, summarize, /standup, todos, create-issue) and asserts on **routing** (floor/canonical/action) + category per query. ⇒ gate is **NOT blind** to the actions Phase 4 touches; it verifies the behavior the shim must preserve. **Fit-for-purpose.** (Pass bar = each query routes to its expected floor/canonical/action destination; run before + after, diff.)
- [ ] *(build-time, not blocking)* Precedent — how prior prompt/classifier changes were gated (884 retest, m1 retest); consume the live Phase-3 `action_verb_unregistered` stream as the concrete backlog of which verbs/source_types the prompt must enumerate.

### Audit-cascade — COMPLETE (2026-06-07; background sweep + spot-verified by Lead Dev)

**6 behavior-driving consumers** of `intent.action` (+ ~50 test assertions that must stay green). ~80 distinct action strings consumed; ~38 in `ACTION_TO_VERB`, **60+ alias sprawl** not yet mapped.

| Consumer | Location (verified) | Keys on | Migration disposition |
|----------|--------------------|---------|----------------------|
| **`_handle_query_intent` elif chain** (THE big one) | `intent_service.py:2159–2271` (34 `intent.action` branches) | 40+ query aliases (`search_documents`, `shipped_*`, `stale_prs*`, `close_issue*`, `list_*`, `meeting_time*`, `productivity*`, `show_standup`, …) | shim now → migrate each action to the workflow-rail one commit at a time |
| **action-dispatch rail** | `workflow_dispatcher.get_action_workflows()` + `intent_service.py:1201` | registered action-triggered workflows (empty today) | the migration **TARGET** (register verbs here) |
| **conversation_handler** | `conversation_handler.py:64+` | `greeting`/`farewell`/`thanks`/`clarification_needed` | shim (4 actions) |
| **lens_inference `ACTION_TO_LENS`** | `lens_inference.py:25,99` | ~30 action keys → ConversationalLens | **DO NOT verb-migrate** (2026-06-08 code read): keys need action-GRANULARITY — `meeting_time`/`list_issues`/`project_status` share verbs GET/LIST but map to *different* lenses (CALENDAR/ISSUES/PROJECTS). Verbs over-collapse. Stays action-keyed; shim-served. |
| **file_resolver (DATA use, not branching)** | `file_resolver.py:254,362` `intent.action.split("_")` | any action | ⚠️ shim feeds the legacy string so `split("_")` keyword extraction is unchanged; a bare verb would yield fewer keywords |
| **honest_failure (display)** | `honest_failure.py:139` humanize | any | shim-transparent |

**Why the hybrid is validated**: a big-bang flip would change all 6 consumers + ~50 tests at once. Shim-then-migrate has **no blocking risk** — the shim preserves every consumer; migration is one discrete commit each.

### Shim spec (the Q2 mechanic, derived from the cascade)
`verb_sourcetype_to_legacy_action(verb: Verb, source_type: str|None) -> str` in `action_registry.py`: the disambiguating inverse map (`verb [+ source_type]` → the single legacy action string all consumers already understand). Classifier emits `verb + source_type` → shim translates at the boundary → all 6 consumers + the ~50 tests run unchanged. Then migrate consumers off the legacy strings incrementally (elif chain → workflow rail; `ACTION_TO_LENS` keys → verbs; `file_resolver` → read verb+source_type), retiring the shim last. *Note: the map is verb(+source)→one-action; where one verb collapsed multiple aliases, source_type (or the dominant alias) disambiguates — to be finalized when authoring the map.*

### Gate plan
- [x] Baseline canonical-retest → apply prompt change → re-run → diff. **DONE 2026-06-08** (commit `1d70dfd19`): full 61-query `TestCanonicalRouting::test_routing` tier, run before + after with `-x/--maxfail=1` overridden, per-query outcome maps diffed → **IDENTICAL** (no routing regression). Gate gotchas recorded: pytest.ini `-x --maxfail=1` must be overridden; Q25 ("next milestone", M2-Beta) is a pre-existing fail; 12 queries (Slack/Productivity/Todos/Calendar/Knowledge) error on missing integration config in this env — all three classes are constant before/after. Phase-3 `action_verb_unregistered` stream is the live backlog to grow the shim table from as real LLM-fallback traffic accrues (step 3 input).

## Decisions (PM discussion 2026-06-07; Q1+Q2 pending Arch ratification)

1. **`source_type` location → `intent.context`** for Phase 4 (matches the working `_handle_summarize` precedent = zero handler churn). **FLAGGED for revisit** (issue **#1175**): `intent.slots` is semantically cleaner and source_type would naturally migrate there if/when the slot-filling work (#1121 family) unifies extracted params under `intent.slots`. Not a Phase-4 blocker. → Arch ratifies.
2. **Transition → HYBRID** (PM-confirmed): **big-bang the classifier prompt** (atomic — a prompt can't be half-flipped; gated by thorough + creative canonical-retest before merge) **+ shim-then-migrate the consumers** (a `verb + source_type → legacy-action` shim keeps the ~40 consumers working unchanged; migrate them off the aliases one discrete commit at a time, retire the shim last). Consistent with Arch's ratified layer-then-migrate. → Arch ratifies. ⚠️ Shim's exact mapping = an output of the audit-cascade (below).
3. **Verb/source_type enumeration → data-driven** (with PM input): derive the prompt's advertised verbs + source_types from the Phase-2 `Verb` enum + the Phase-3 `action_verb_unregistered` backlog stream — not hand-picked.
4. **Retest pass bar → must confirm coverage**: verify the canonical-retest actually exercises the category-routed action space; if it doesn't, the gate has a blind spot to close before relying on it.

## Why planning-first (no build yet)
High blast radius (every LLM-classified intent's naming changes) + gated. The audit-cascade must enumerate consumers + settle the transition strategy BEFORE touching the prompt, or we repeat the Phase-3 spec-gap surprise at a larger scale. This doc is the grounding artifact; Arch ratified the *shape*, this plans the *execution*.

---
*Author: Lead Developer, 2026-06-07. Living doc — accretes through the flywheel. Phase -1 grounded in verified code reads (cited above); Phase 0 + audit-cascade pending.*
