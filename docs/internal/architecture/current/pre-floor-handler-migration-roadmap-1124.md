# Pre-Floor Handler Migration Roadmap (#1124, Phase 1)

**Author:** Lead Dev · **Date:** 2026-06-05 · **Issue:** #1124 PRE-FLOOR-HANDLER-AUDIT · **Status:** Phase 1 (audit) complete — awaiting PM cohort prioritization for Phase 2

## The target pattern (ADR-059)

```
GOOD:  user message → LLM classifier → {action, slots} → workflow_dispatcher → handler executes side effect
BAD:   user message → {action} → elif intent.action in [...] → handler regex-parses message  (or refuses with a hand-coded clarification_type)
```

Reference implementation (the one handler doing it right): `start_meeting_workflow` in
`services/intent_service/workflow_entries.py` + `MEETING_TEMPLATE` in `services/slot_filling/slot_template.py`.

## Re-baseline (2026-06-05, current `services/intent/intent_service.py`, 11,069 lines)

| Metric | May 25 (filed) | Jun 5 (now) | Δ |
|---|---|---|---|
| `elif intent.action in [...]` dispatch sites | 28 | **28** | — |
| `_parse_*` regex helpers | 3 | **2** | −1: `_parse_document_update_query` deleted by #1121 (slot-filling migration — proof the pattern works) |
| `_handle_*` methods | 44 | **44** | — |
| `clarification_type=` assignment sites | "~14 flows" | **39 assignments** | the 14 was distinct *types*; 39 is total assignment sites |

## Full catalog — all 28 dispatch sites

Triage key: **(a)** MIGRATE to slot-filling · **(b)** KEEP elif/regex-shaped (syntactic/low-value) · **(c)** DELETE (deprecated). No (c) found — all 28 handlers are fully implemented (no stubs).

| Line | Actions | Handler | Regex-parse | Hand-coded clarif | NL value | Triage |
|---|---|---|---|---|---|---|
| 2093 | update_document/edit_document/… | `_handle_update_document_notion` | No (already slot-extracts, #1121) | document_name/not_found | HIGH | **(a)** cohort 1 — finish: drop elif → dispatcher |
| 2097 | shipped_this_week/what_shipped/… | `_handle_shipped_this_week` | No | No | low | (b) |
| 2105 | stale_prs/old_prs/… | `_handle_stale_prs` | No | No | low | (b) |
| 2108 | review_issue/show_issue/get_issue | `_handle_review_issue_query` | # lookup only | implicit | low | (b) syntactic # lookup |
| 2111 | close_issue/… | `_handle_close_issue_query` | # + fuzzy title | requires_clarification | MED | **(a)** cohort 2 — *blocked* on confirmation-slot infra |
| 2114 | reopen_issue/… | `_handle_reopen_issue_query` | # + fuzzy title | requires_clarification | MED | **(a)** cohort 2 — *blocked* (same) |
| 2117 | comment_issue/add_comment/… | `_handle_comment_issue_query` | # + comment-text patterns | requires_clarification | HIGH | **(a)** cohort 1 — slots: issue_number + comment_text(NL) |
| 2121 | list_issues/… | `_handle_list_issues_query` | No | No | low | (b) |
| 2125 | list_prs/… | `_handle_list_prs_query` | No | No | low | (b) |
| 2129 | list_milestones/… | `_handle_list_milestones_query` | No | No | low | (b) |
| 2131 | list_releases/… | `_handle_list_releases_query` | No | No | low | (b) |
| 2135 | list_labels/… | `_handle_list_labels_query` | No | No | low | (b) |
| 2137 | list_branches/… | `_handle_list_branches_query` | No | No | low | (b) |
| 2142 | local_git_status/… | `_handle_local_git_status_query` | No | No | low | (b) |
| 2147 | meeting_time/calendar_analysis/… | `_handle_meeting_time_query` | `parse_relative_date` | No | HIGH | **(a)** cohort 1 — slot: date_range(datetime) |
| 2150 | recurring_meetings/… | `_handle_recurring_meetings_query` | No | No | low | (b) |
| 2153 | week_calendar/week_ahead/… | `_handle_week_calendar_query` | No | No | low | (b) |
| 2157 | productivity/weekly_metrics/… | `_handle_productivity_query` | No | No | low | (b) |
| 2166 | changes_query/what_changed/… | `_handle_changes_query` | `_parse_time_expression` | No | HIGH | **(a)** cohort 1 — slot: timeframe(datetime) |
| 2169 | attention_query/needs_attention/… | `_handle_attention_query` | No | No | low | (b) |
| 2181 | list_todos_query/next_todo_query/… | `_handle_execution_intent` (todos) | No | No | low | (b) |
| 2190 | show_standup/get_standup | `_handle_standup_query` | No | No | low | (b) |
| 2193 | list_projects/show_projects | `_handle_projects_query` | No | No | low | (b) |
| 6346 | analyze_commits/analyze_code | `_handle_analyze_commits` | No | repository_required | low | (b) entity from context |
| 6349 | generate_report/create_report | `_handle_generate_report` | No | repository_required | low | (b) |
| 6352 | analyze_data/evaluate_metrics | `_handle_analyze_data` | No | repository_required/data_type | low | (b) enumerated choice |
| 6936 | summarize/create_summary | `_handle_summarize` | No | source_type_required | HIGH | **(a)** cohort 1 — slots: source_type(choice) + content(NL) |
| 8834 | prioritize/set_priorities | `_handle_prioritization` | No | prioritization_type/items | MED | **(a)** cohort 1 — slots: prioritization_type(choice) + items |

## Triage tally

- **(a) MIGRATE: 8 handlers** — `update_document`, `comment_issue`, `meeting_time`, `changes_query`, `summarize`, `prioritize` (cohort 1); `close_issue`, `reopen_issue` (cohort 2, blocked).
- **(b) KEEP: 20 handlers** — pure queries / syntactic lookups / enumerated-choice context reads. Low UX ROI; leaving elif-shaped is correct for now.
- **(c) DELETE: 0.**

## Prerequisite surfaced by the audit

`close_issue` / `reopen_issue` are genuine NL candidates but **blocked**: they need a multi-turn
**pending-action confirmation** ("are you sure? yes to confirm") that the current slot-filling
infrastructure does not model. This is a prerequisite sub-issue (relates to #1122 multi-turn
context). Recommend filing it before cohort 2; do NOT bench cohort 1 on it.

## Recommended Phase 2 — cohort 1 ordering (no new infra needed)

1. **`update_document`** — smallest; already slot-extracts (#1121). Just drop the elif and route through `workflow_dispatcher`. Proves the end-to-end migration on a live handler. (~½ day incl. tests)
2. **`summarize`** — HIGH value; already has sub-route scaffolding (`_fetch_issue_content`/`_extract_text_content`). Slots: `source_type`(choice) + conditional `content`(NL). (~2-3 days)
3. **`comment_issue`** — HIGH value; NL comment body is the payoff. Slots: `issue_number` + `comment_text`(NL). (~2-3 days)
4. **`meeting_time` + `changes_query`** — temporal-slot pair; can share a date/timeframe slot pattern, retire `parse_relative_date`/`_parse_time_expression`. (~2-3 days together)
5. **`prioritize`** — MED; slots `prioritization_type`(choice) + `items`. (~2 days)

## Phase 4 (discipline) — recommended now, cheap

- CLAUDE.md / PR-review rule: new action handlers = workflow-dispatcher entry + slot template; **no new `elif intent.action in [...]` dispatches.**
- Architectural-enforcement test: count `elif intent.action in [...]` sites in `intent_service.py`; fail if it exceeds the roadmap target (28 today; ratchets down as cohorts land).

## Open decision for PM

Phase 1 (this audit) is done. **PM to greenlight cohort-1 scope + ordering** (all 6, or a subset) before Phase 2 implementation begins. Cohort 2 (mutations) waits on the confirmation-slot prerequisite.

---

## Phase 2 — cohort-1 progress + methodology correction (2026-06-05)

- ✅ **#1 update_document** — shipped (commit `88d34defb`). Built the shared **action-dispatch rail** + migrated update_document onto it (28→27 elif sites). Action names matched the classifier; verified live.
- ⏸️ **#2 summarize — DEFERRED → #1158.** Not a clean mechanical migration: the classifier emits a fragmented, partly-**improvised** summary action vocabulary (`generate_summary` documented; `summarize_github_issue` improvised by the LLM; `summarize_document` rule-based; `summarize`/`create_summary` enum-only), and `_handle_summarize`'s `source_type`-in-context model is orthogonal to the classifier's action-per-type approach. `_handle_summarize` has been effectively **dead**; the floor handles summaries. Needs classifier-taxonomy work + a product decision — tracked in **#1158** (Arch/PPM/CXO consults recommended). WIP reverted (nothing shipped).

### ⚠️ Methodology correction (applies to remaining cohort handlers)
The Phase-1 catalog took action names from the **`elif` strings**. The real dispatch keys are the **classifier's emitted actions** (the classifier prompt + live behavior), which can differ or be improvised. #1 matched; #2 did not. **Before migrating #3–6 (comment_issue, meeting_time, changes_query, prioritize), verify each handler's real action name** (prompt grep + a live `/intent` probe) first. A handler whose action vocabulary is unstable/improvised is a #1158-shaped taxonomy problem, not a mechanical migration — flag rather than force.

---

## #1158 SUMMARIZE-TAXONOMY — RESOLVED (2026-06-09, Lead Dev)

The deferred-from-cohort-1 `summarize` handler is resolved **not** by migrating it onto
the action-dispatch rail, but by routing summaries to the **conversational floor**. Three
settled decisions converged:

- **Architecture (Arch, 2026-06-06, ADR-060 amendment, Approved):** one stable typed **verb**
  (`Verb.SUMMARIZE`) + a separate **`source_type`** slot — never an improvised collapsed
  action name like `summarize_github_issue`. The Phase-4 verb mechanism already ships this.
- **Product (PPM, 2026-06-08):** a summary's **output is ALWAYS conversational (floor-rendered)**;
  only the **source** branches — floor-direct for user text / current conversation,
  fetch-augmentation for data the floor can't reach (GitHub issue, commit range, document).
  There is no second (structured) output renderer to build.
- **UX (CXO):** concurred floor-only.

### What shipped (the canonicalization + floor-routing)
1. **`(Verb.SUMMARIZE, *)` is deliberately NOT in `_VERB_SOURCE_TO_ACTION`** (action_registry.py).
   The shim returns `None` → `_validate_confidence` keeps the LLM's free-form action → the
   SYNTHESIS `summarize`/`create_summary` elif is never hit → the request **floors**
   (ADR-060 floor-default). This makes "output is always floor" structurally true regardless
   of what the classifier emits. Canonical fixtures #38/#47 assert `floor` for summaries.
2. **Classifier prompt source_type vocabulary widened** to the PPM 5-set
   `{text, conversation, github_issue, commit_range, document}` + explicit guidance to emit
   `verb=summarize` + `source_type` (and NOT improvise `summarize_github_issue`). `source_type`
   still rides into `intent.context` for observability + the future fetch-augmentation build.
3. **`_handle_summarize` marked DORMANT** (off the dispatch path) but retained — its fetch
   helpers (`_fetch_issue_content` / `_fetch_commit_content`) seed the deferred pipeline.

### Deferred (tracked follow-on): fetch-augmentation
PPM's near-term vision includes fetch-augmentation for sources the floor can't reach
(GitHub issue+comments, commit range, document retrieval) → fetch content, then hand to the
floor to render. **Not built now** (today those sources floor with a graceful "I don't have
access to that — want me to pull it?"). Tracked as **#1187 SUMMARIZE-FETCH-AUGMENTATION**.
Also not built: any persistent/exportable/structured summary *artifact* (no current product
evidence of need; explicit reopen-trigger = a recurring use-case where the summary must
persist or leave the conversation → that's a *summary-as-artifact* surface, spec'd then).

### Implication for the rest of cohort 1
The "verb + source_type" pattern from the ADR-060 amendment is the canonical fix for the
**whole cohort's** improvised-action-name problem (the methodology correction above). `summarize`
is the first handler resolved under it; it resolves to *floor*, but `prioritize` / `comment_issue`
etc. resolve to *rail migration* — same canonicalization, different disposition per handler.

---

## Cohort-1 elif-removal COMPLETE (2026-06-09, Lead Dev)

The last two directed cohort-1 migrate-targets are now on the action-dispatch rail,
completing the original 8-handler cohort:

| Handler | Disposition | Notes |
|---|---|---|
| update_document | ✅ rail | migration #1 |
| changes_query | ✅ rail | migration #3 |
| close_issue / reopen_issue / comment_issue | ✅ rail | Phase-4 step-3 mutation cohort |
| summarize | ✅ floor | #1158 (resolved-to-floor, not rail) |
| **prioritize** | ✅ **rail** | **this pass** — 2-arg, via existing factory |
| **meeting_time** | ✅ **rail** | **this pass** — 3-arg (user_id), new user-scoped factory |

**prioritize** (`prioritize` / `set_priorities`) — strategy-category handler, reused
unchanged via `_make_query_dispatch_entry_point`. Elif removed from the strategy router.

**meeting_time** — the directed target; folded in its two same-signature siblings
(`recurring_meetings`, `week_calendar`) as a **calendar cohort** (`_CALENDAR_QUERY_COHORT`),
mirroring the read-query-cohort precedent. All three are 3-arg `(intent, workflow_id, user_id)`
(user_id needed for timezone-aware queries, #586), so they use a new
`_make_user_scoped_query_dispatch_entry_point` factory variant. The 3 calendar elif
branches removed from `_handle_query_intent`.

**Tests:** new `TestCalendarQueryCohortWorkflowEntries1124` + `TestPrioritizationWorkflowEntry1124`
(factory threads user_id; handlers exist on IntentService; aliases action_triggered). The 9
`test_calendar_query_handlers` routing tests were **repointed** off the removed
`_handle_query_intent` elif onto the real rail (`dispatch_workflow` by `intent.action`) — the
same consumer-trace test-update the changes_query migration did. Canonical-retest IDENTICAL to
baseline (49/1/11); full intent suite back to the pre-existing-failure baseline (no net
regression). Calendar live-routing positively verifies once Calendar test-env is configured
(a #1165 enabler; the calendar canonical queries Q34/Q35/Q61 are in the env-ERROR set today).

**Remaining on the elif chain (NOT cohort-1, deliberately):** `search_documents`, `analyze_*`,
`generate_*`, `productivity`, `standup`, `list_projects`, `local_git_status`, `strategic_planning`,
`learn_pattern`, etc. — these were triaged out of the migrate-8; they migrate (if at all) under
the same verb-canonicalization pattern when/if prioritized. Cohort 2 (`close`/`reopen` multi-turn
confirmation) already landed via the mutation cohort.

---

## Phase 4 (discipline) — SHIPPED (2026-06-09, Lead Dev)

The #1124 Phase-4 AC ("CLAUDE.md rule + architectural-enforcement test") is done:

- **Architectural-enforcement RATCHET test** — `TestPreFloorDispatchSiteRatchet` in
  `tests/test_architecture_enforcement.py`. Counts hand-coded
  `if/elif intent.action in [...]` dispatch sites in `intent_service.py` and fails the
  build if the count GROWS (`MAX_DISPATCH_SITES = 15` as of today; counts both `if` heads
  and `elif` branches so a new fresh-chain regression can't sneak past an elif-only scan).
  The companion `test_ratchet_target_stays_tight` keeps the target == actual count (no
  silent regression slack). **Discipline: when you migrate a handler, LOWER the target in
  the same commit; never raise it.**
- **CLAUDE.md rule** — new "Intent dispatch — no new `elif intent.action` chains" subsection
  under API Conventions: new action handlers register a workflow-dispatcher entry, not an
  elif branch; points at the ratchet test + this roadmap.

This is the durable guard that "tracks the regressions" — it ratchets the 28→15 progress
and forces every future handler onto the rail. The remaining #1124 scope (per-handler
slot-filling + regex deletion under Phase 2; cohort-2 residual handlers under Phase 3) stays
tracked by #1124's own unchecked ACs.

## Phase 3 inchworm — analysis cohort migrated (2026-06-09, Lead Dev)

`analyze_commits` / `generate_report` / `analyze_data` (the three 2-arg ANALYSIS-category
handlers) migrated off the `_handle_analysis_intent` elif chain onto the rail
(`_ANALYSIS_QUERY_COHORT`, standard 2-arg factory). Handlers reused unchanged. Ratchet
lowered **15 → 12**. NOT migrated: `analyze_document` (the if-head) — it is 3-arg
(`session_id`) + Notion-coupled, deferred to its own bite. Consumer-trace was clean
(no test calls the analysis router directly with these 3 actions — the only direct-router
tests use `analyze_document`, which stays). Zero net regression (canonical IDENTICAL;
the 7 pre-existing `test_execution_analysis_handlers` failures are unchanged from main).

## Phase 3 inchworm — synthesis migration (2026-06-09, Lead Dev)

`generate_content` / `create_content` migrated off `_handle_synthesis_intent` onto the rail
(`generate_content_entry`, 2-arg factory; `_handle_generate_content` reused unchanged). The
dead `summarize` / `create_summary` elif was **deleted** — per #1158 summaries always floor,
the verb shim no longer produces the legacy `summarize` action, and removing the branch floors
it even if a free-form `summarize` action is emitted directly (#1158-consistent hardening).
`_handle_synthesis_intent` now routes everything without a rail entry to the floor. Ratchet
**12 → 10**. No test calls the synthesis router directly → clean consumer-trace; the only
remaining synthesis-test failure is the pre-existing #1188 (`test_summarize_empty_content`,
humanizer copy, unrelated). Canonical IDENTICAL to baseline.

## Phase 3 inchworm — QUERY-category cohort migrated (2026-06-10, Lead Dev)

The entire `_handle_query_intent` elif chain migrated onto the rail — the router now
collapses to the generic-query fallback. Ratchet **10 → 3** (remaining: the 3 category
if-heads — `analyze_document` [Notion, 3-arg, deferred], `strategic_planning`, `learn_pattern`).

Migrated (handlers reused unchanged; per-handler arity threaded via new factory flags
`pass_session_id` / `pass_user_id`, plus `run_todo_query_workflow` for the todos delegate):
`search_documents`/`find_documents`/`search_notion`, `local_git_status[_query]`,
`productivity`/`my_productivity`/`weekly_metrics`/`accomplishments`,
`attention_query`/`needs_attention`/`what_needs_attention`/`attention_items`,
`list_todos_query`/`list_completed_todos`/`next_todo_query` (→ EXECUTION handler),
`show_standup`/`get_standup`, `list_projects`/`show_projects`.

**Consumer-trace:** repointed 9 routing tests across 5 files (productivity, contextual/attention,
document-search, projects, local-git) onto the rail (`dispatch_workflow` by action; the two
source-introspection tests repointed to assert the rail's new home in `workflow_entries.py`).
Branch-vs-main diff isolated these from the **15 pre-existing `test_github_query_handlers`
failures** — those are prior-migration debt (read-query + issue-mutation cohorts removed their
elifs but never repointed `test_github_query_handlers`; fail identically on main). Tracked as a
follow-on test-hygiene pass (not this bite's regression).

## Phase 3 COMPLETE — final if-heads migrated; ratchet 3 → 0 (2026-06-10, Lead Dev)

The last 3 category-router if-heads migrated onto the rail, so **every
`if/elif intent.action in [...]` dispatch site in `intent_service.py` is gone (count = 0)**:
- `analyze_document`/`analyze_file` → rail (pass_session_id; Notion-coupled, handler unchanged)
- `strategic_planning`/`create_plan` → rail (2-arg, handler unchanged)
- `learn_pattern`/`detect_pattern` → rail (2-arg, handler unchanged)

Each category router (`_handle_analysis_intent` / strategy / learning) now collapses to its
conversational-floor fallback. The Phase-4 ratchet is set to **MAX_DISPATCH_SITES = 0** — it
now blocks ANY new hand-coded action-dispatch branch; every future handler registers a
workflow-dispatcher entry.

**#1124 dispatch-migration trajectory:** 28 (audit baseline 2026-05-25) → 15 (cohort-1) → 12
(analysis) → 10 (synthesis) → 3 (QUERY cohort) → **0 (final if-heads)**. Consumer-trace:
repointed the 2 analyze_document routing tests onto the rail. Canonical-retest IDENTICAL
throughout; full intent suite at the pre-existing-failure baseline (no net regression).

**What's NOT done under #1124 (still tracked by its own ACs):** Phase 2 per-handler
slot-filling + hand-regex deletion (the dispatch migration reused every handler UNCHANGED;
slot-filling is the separate follow-on, e.g. #1121 for update_document). The elif-removal /
dispatch-rail goal is fully met; the slot-filling depth is the remaining #1124 scope.
Pre-existing test-debt: #1189 (repoint stale test_github_query_handlers).

## #1124 CLOSED (2026-06-10)

Dispatch-migration 28→0 (Phase 1 + 4 ✅, guarded by the ratchet). Slot-filling done for the
two genuine Pattern-045 hand-regex cases — update_document (#1121) + comment_issue. The other
candidates were assessed (2026-06-10) and **deliberately not slot-filled** (PM-approved
exception): changes_query (`_parse_time_expression` is date-aware — an LLM days-extraction
regresses the day-of-week case; roadmap rates the regex "acceptable"), prioritize (no hand-regex;
a context-read stub NL extraction can't complete), meeting_time (relative-date math + Calendar-
coupled). Trigger to revisit: a concrete recurring NL complaint for one of these.

**DRY follow-on (one-line note, deferred):** the conversation-history builder for antecedent
resolution (#1122) is now duplicated inline in two slot-filled handlers
(`_handle_update_document_notion`, `_handle_comment_issue_query`). Extract a shared
`_build_slot_conversation_history(intent)` helper if/when a 3rd handler needs it — not now (no
3rd slot-fill handler is planned).

Follow-ons: #1190 (close/reopen multi-turn confirmation gate), #1189 (test_github_query_handlers
repoint, M5).
