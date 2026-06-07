# Phase 4 — Classifier-Prompt Canonicalization: Flywheel Planning (#1124)

**Status**: PLANNING — Phase -1 (investigation) done; Phase 0 (research) + audit-cascade IN PROGRESS. **Gated phase, high blast radius.** PM-directed full-flywheel treatment 2026-06-07; planning precedes any build.

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

### Audit-cascade (methodology-30 — the load-bearing risk)
- [ ] Enumerate EVERY consumer of `intent.action` (grep `intent.action ==` / `in [...]`, `canonical_handlers` dispatch, the action-dispatch rail).
- [ ] For each consumer: survives a verb+source_type classifier? → update-now / shim / retire.
- [ ] Decide the transition strategy: **big-bang** (update all consumers at once) vs **shim-then-migrate** (a `verb → legacy-action` translation during rollout so consumers migrate incrementally). Lean: shim-then-migrate (layer-then-migrate spirit; smaller blast per commit).

### Gate plan
- [ ] Baseline canonical-retest → apply prompt change → re-run → diff. Pass bar: no canonical-conversation regressions AND the Phase-3 stream shows targeted actions now emitting canonical verbs.

## Open questions (for Arch / PM at plan-review)
1. **`source_type` location**: `intent.context` (working precedent) vs `intent.slots` (amendment)?
2. **Transition**: shim-then-migrate vs big-bang?
3. **Retest pass bar** + whether the canonical-retest covers the category-routed action space (gate blind-spot check).
4. **Verb/source_type enumeration** the prompt advertises — derived from the Phase-2 `Verb` enum + the Phase-3 backlog stream.

## Why planning-first (no build yet)
High blast radius (every LLM-classified intent's naming changes) + gated. The audit-cascade must enumerate consumers + settle the transition strategy BEFORE touching the prompt, or we repeat the Phase-3 spec-gap surprise at a larger scale. This doc is the grounding artifact; Arch ratified the *shape*, this plans the *execution*.

---
*Author: Lead Developer, 2026-06-07. Living doc — accretes through the flywheel. Phase -1 grounded in verified code reads (cited above); Phase 0 + audit-cascade pending.*
