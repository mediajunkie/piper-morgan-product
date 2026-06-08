# Lead Developer Session Log — 2026-06-08

**Role**: Lead Developer (Claude Code, Opus)
**Slug**: `lead-code-opus`
**Started**: 2026-06-08 08:28 PDT
**Branch**: main (shared worktree)

---

## Session start

PM resumed me at 8:27 am Mon Jun 8, asking to resume the duty cycle and **discuss the items that have been waiting for focused PM attention**.

### Start hygiene
- **Mailbox**: lead/inbox clean (only MANIFEST.md; no pending messages). The SessionStart hook's "lead:2" was stale.
- **Branch**: main, clean for my work (4 commits from 6/7 all on origin/main).
- **Overnight cohort activity** (origin/main): PPM (Fire 0–2, #1166 convergence 2/3), PA (light-Monday START), Arch (Fire 8).
  - **Arch Fire 8 (`8e0bddc58`)**: records ADR-060 Phase 4 ratification (Q1 source_type→intent.context + #1175 revisit; Q2 HYBRID prompt-big-bang + shim-then-migrate) — *documentation of what we already agreed*, not a new ask. ADR-066 v0.1 filed (Q6/Q7 arc complete; Arch's track). **Nothing new blocking me.**
- **Briefing**: STALE (21 days, last 2026-05-17) — flagged; candidate refresh this session if PM wants.

### Items waiting on PM focused attention (the discussion slate)
Surfaced to PM for sequencing:
1. **#1124 Phase 4 step 2** — classifier-prompt big-bang flip behind the canonical-retest gate (needs live retest run + PM ratification of the flip). Shim already shipped (`3c65c7017`); this is the behavior-changing step.
2. **#1165 UAT walk** — 5 queued items (#1133, #1155, #496, #497, #1143 slice 2) need an authenticated browser session (PM holds it).
3. **#1175** — source_type → intent.context revisit (the Q1 flag; Arch noted it). Design discussion.
4. **#1164** — privacy semantics; wants PM presence.

(Awaiting PM pick — one at a time once the slate is set.)

## #1124 Phase 4 step 2 — classifier-prompt flip (PM-present, in progress)

PM picked the Phase 4 prompt flip as today's first focused-attention item.

**Investigate-first findings**:
- Change point: `llm_classifier.py::_build_classification_prompt` (free-form `action`) + the Intent build in `_validate_confidence` (L662).
- Change is **additive + safe**: prompt now also asks for a canonical `verb` + `source_type`; the boundary canonicalizes `intent.action = verb_sourcetype_to_legacy_action(verb, source_type)` ONLY when the verb maps (the 7-verb shim cohort) — otherwise keeps the free-form action (zero-regression fallback). LLM classifier is fallback-only (pre-classifier short-circuits), so real blast radius = the shim cohort.
- Gate = `tests/e2e/test_canonical_conversations.py::TestCanonicalRouting::test_routing` (61 queries, ASGI in-process, routing assertions). Env IS runnable: Postgres up, app loads key from `.env` (smoke 4/4 green in 34s).

**Gate gotchas found**:
- pytest.ini has `-x --maxfail=1` → stops at first failure. Overriding with `-o addopts="" --maxfail=1000` for the diff runs.
- **Pre-existing failure Q25** ("What's the next milestone?", tagged `M2 Beta` known_issue) — fails before AND after; not a regression. Diff must compare the per-query set, treating Q25 as constant.

**Sequence**: clean baseline (stashed my edit) → apply prompt+wiring → unit tests → after-run → diff. Unit tests authored: `test_classifier_verb_canonicalization_1124.py` (7 cases: mappable verb canonicalizes + stores source_type, mutation verb, no-verb fallback, unmapped-verb fallback, invalid-verb no-crash, null-source normalize, low-confidence still raises).

### Phase 4 step 2 — SHIPPED (commit `1d70dfd19`, gate GREEN)

Flip applied: `_build_classification_prompt` advertises the canonical Verb vocabulary + `source_type`; `_validate_confidence` canonicalizes `intent.action` via the shim when the verb maps, else keeps free-form action (zero-regression fallback) + stores `source_type` in `intent.context`.

**Verification (the gate)**:
- **E2E canonical-retest** (#928, `TestCanonicalRouting::test_routing`): full 61-query routing tier, before/after, `-x/--maxfail=1` overridden, per-query outcome maps diffed → **IDENTICAL**. Baseline = After = {48 PASSED, 1 FAILED (Q25 known M2-Beta), 12 ERROR (env: Slack/Productivity/Todos/Calendar/Knowledge integrations unconfigured)}. No routing regression.
- **Unit**: 7 new wiring tests (`test_classifier_verb_canonicalization_1124.py`) + 107 existing classifier tests = **114 green**.

**Process notes for next time**: (1) the e2e gate runs in-process (ASGI) + loads the LLM key from `.env`; ~5.3 min/run. (2) pytest.ini `-x --maxfail=1` + the pre-existing Q25 fail truncate naive runs — override addopts. (3) capture FULL pytest output then extract with `\[[^]]*\]` (category ids have spaces like "GitHub Ops"); a `[A-Za-z]+` pattern silently drops the shim-cohort risk zone. (4) ~5 baseline iterations consumed setting the gate up right; the actual change is ~50 lines.

**Plan doc updated**: `phase-4-classifier-canonicalization-plan-1124.md` step 2 → SHIPPED, gate-plan checkbox → done.

**Phase 4 remaining**: step 3 (migrate ~6 consumers off legacy aliases — `_handle_query_intent` elif chain, `ACTION_TO_LENS`, conversation_handler, file_resolver — one commit each, shim-covered so non-blocking) → step 4 (retire shim) → Phase 4.x enforce-floor. Step 3 is solo-safe (shim keeps consumers working); good next-session work.

### Phase 4 step 3 — consumer migration (CLOSE/REOPEN/COMMENT cohort) — gate pending

PM authorized solo Phase-4 work. Investigate-first on step 3 surfaced that "migrate consumers to verbs" is NOT uniform — refined dispositions (code-grounded):
- **`_handle_query_intent` elif chain** → migrate elif→action-dispatch rail. Recipe is PROVEN: `update_document` + `changes_query` already migrated this way (workflow_entries.py `run_*_workflow` adapters + `register_default_workflows` + remove elif). The rail (intent_service.py:1201) runs before the elif chain, passes `{intent, workflow_id, intent_service}` in context, None→falls through (safe).
- **lens_inference `ACTION_TO_LENS`** → does **NOT** verb-migrate. It needs action-GRANULARITY (meeting_time→CALENDAR, list_issues→ISSUES, project_status→PROJECTS all share verb GET/LIST but map to different lenses). Verbs over-collapse — the exact GET/LIST concern the plan thought "dissolved." Stays action-keyed, shim-served. (Plan disposition corrected.)
- **file_resolver** → does **NOT** verb-migrate (`action.split("_")` keyword extraction; a bare verb yields fewer keywords). Shim-served. (Plan already flagged.)
- **Intent carries no `verb` field** — consumers derive via `get_verb(intent.action)` or read `context["source_type"]`.

**This increment** (one commit): migrated the CLOSE/REOPEN/COMMENT issue-mutation cohort (the Phase-2 verbs' legacy-action targets) elif→rail:
- `workflow_entries.py`: 3 adapters (`run_close_issue_workflow` / `run_reopen_issue_workflow` / `run_comment_issue_workflow`) + 3 `WorkflowEntry`s + 7 aliases registered (`action_triggered=True`); handlers reused unchanged.
- `intent_service.py`: removed the 3 elif branches (replaced with a migration marker).
- Tests: 5 new (`TestIssueMutationWorkflowEntries1124` — adapter→handler dispatch, missing-context→None, cohort registered in rail); 26 green in the dispatcher suite.

**Gate coverage**: corpus DOES exercise the cohort — Q45 "Close completed issues" (→floor), Q59 "Comment on issue #456" (→canonical), both in the passing 48 → the e2e routing diff genuinely verifies this migration (not blind). Running the after-migration gate vs the step-2 baseline now.
