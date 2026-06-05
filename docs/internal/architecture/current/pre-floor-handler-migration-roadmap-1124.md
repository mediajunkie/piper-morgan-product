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
