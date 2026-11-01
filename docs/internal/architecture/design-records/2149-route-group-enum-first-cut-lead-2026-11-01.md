# #2149 `route_group` enum: Lead's first cut (2026-11-01)

Status: DRAFT for Arch's ruling (design record `2149-router-catalog-shape.md`, design item 1: "Lead and I draft the starting enum from the 72 ops"). Nothing here is built. After the ruling, the field and its ratchet are Lead's build step 1 (no behaviour change).

Derived from `derive_routing_grammar()` on main at `4ac5862535` (72 operations: 66 rail, 6 registry). Every op is assigned exactly once; the check script is in Lead's scratchpad and the counts below are its output, not hand totals.

## The enum

| `route_group` | ops | stage-1 line (the only text shared across groups) |
|---|---:|---|
| `issues` | 7 | GitHub issues: create, change, close or reopen, comment on, show or list them. |
| `repo_activity` | 11 | What is happening in the code and the repositories: pull requests, what shipped, milestones, releases, labels, branches, commits, the local branch, and which repo is the default. |
| `projects_and_repos` | 11 | The user's projects and portfolio: list, search, add, archive or restore projects, and link, unlink or list the repositories attached to them. |
| `calendar_and_time` | 5 | Calendar, meetings and the clock: today's or the week's schedule, recurring meetings, what time it is, the user's timezone. |
| `todos_and_reminders` | 7 | Todos and reminders: add, list, complete, delete or clear them. |
| `documents_and_writing` | 7 | Documents and drafting: summarize, analyze, search or update a document; write content, a report or a stakeholder update. |
| `status_and_priorities` | 11 | How things are going and what matters now: project status, what needs attention, the top priority, blockers, what changed, completion history, productivity, standup, metrics, a plan. |
| `memory_and_insights` | 5 | What the assistant remembers or has learned: memory of the user and past conversations, insights and patterns, this session's activity, why it suggested something. |
| `assistant_and_conversation` | 8 | About the assistant itself, and pleasantries: who it is, what it can do, how it works with the user, a feature's details, how-do-I guidance; greetings, thanks and goodbyes. |

Groups: 9. Largest: 11 (three groups at 11). Smallest: 5.

## Assignment, op by op

`source` is what the grammar reports (`rail` = a `WorkflowEntry`, `action_registry` = one of the six registry-only canonicals). Aliases route to the same op and inherit its group; they are listed so no name is lost.

### `issues` (7)

| op | source | aliases |
|---|---|---|
| `create_issue` | rail | create_github_issue, create_item, create_ticket, make_github_issue, new_github_issue |
| `update_issue` | rail | update_github_issue, update_ticket, modify_issue |
| `close_issue` | rail | close_issue_query |
| `reopen_issue` | rail | reopen_issue_query |
| `comment_issue` | rail | add_comment, comment_issue_query |
| `review_issue` | rail | show_issue, get_issue, review_issue_query |
| `list_issues` | rail | list_issues_query, list_assigned_issues |

### `repo_activity` (11)

| op | source | aliases |
|---|---|---|
| `list_prs` | rail | list_prs_query, list_pull_requests |
| `stale_prs` | rail | old_prs, show_stale_prs, stale_prs_query, list_stale_prs |
| `shipped_this_week` | rail | what_shipped, show_closed_prs, shipped_query |
| `list_milestones` | rail | list_milestones_query |
| `list_releases` | rail | list_releases_query |
| `list_labels` | rail | list_labels_query |
| `list_branches` | rail | list_branches_query |
| `analyze_commits` | rail | analyze_code |
| `local_git_status_query` | rail | local_git_status |
| `set_default_repo` | rail | — |
| `get_default_repo` | rail | — |

### `projects_and_repos` (11)

| op | source | aliases |
|---|---|---|
| `list_projects` | rail | show_projects |
| `search_projects` | rail | — |
| `add_project` | rail | — |
| `archive_project` | rail | — |
| `restore_project` | rail | — |
| `list_archived_projects` | rail | show_archived_projects, archived_projects_query, list_archived |
| `manage_portfolio` | action_registry | — |
| `link_repo` | rail | — |
| `unlink_repo` | rail | — |
| `list_repos` | rail | — |
| `manage_repos` | action_registry | — |

### `calendar_and_time` (5)

| op | source | aliases |
|---|---|---|
| `meeting_time` | rail | how_much_time_in_meetings, calendar_analysis |
| `week_calendar` | rail | week_ahead, whats_my_week_like |
| `recurring_meetings` | rail | review_recurring_meetings, audit_meetings |
| `get_current_time` | rail | — |
| `set_timezone` | rail | — |

### `todos_and_reminders` (7)

| op | source | aliases |
|---|---|---|
| `create_todo` | rail | add_todo, new_todo |
| `create_reminder` | rail | set_reminder, add_reminder |
| `list_todos_query` | rail | list_completed_todos, next_todo_query |
| `list_reminders_query` | rail | list_reminders, show_reminders, get_reminders |
| `complete_todo` | rail | finish_todo, mark_complete, mark_done |
| `delete_todo` | rail | remove_todo, cancel_todo, delete_reminder, remove_reminder, cancel_reminder |
| `clear_todos` | rail | — |

### `documents_and_writing` (7)

| op | source | aliases |
|---|---|---|
| `summarize_document` | rail | summarize_file, summarize_upload, summarize_uploaded_file |
| `analyze_document` | rail | analyze_file, qa_document |
| `search_documents` | rail | find_documents, search_notion |
| `update_document` | rail | edit_document, update_document_query |
| `generate_content` | rail | create_content |
| `generate_report` | rail | create_report |
| `write_stakeholder_update` | rail | — |

### `status_and_priorities` (11)

| op | source | aliases |
|---|---|---|
| `get_project_status` | rail | — |
| `attention_query` | rail | needs_attention, what_needs_attention, attention_items |
| `get_top_priority` | action_registry | — |
| `prioritize` | rail | set_priorities |
| `analyze_blockers` | rail | — |
| `changes_query` | rail | what_changed, show_changes, changes_since |
| `check_completion_status` | rail | — |
| `productivity` | rail | my_productivity, weekly_metrics, accomplishments, productivity_query, analyze_productivity |
| `show_standup` | rail | get_standup |
| `analyze_data` | rail | evaluate_metrics |
| `strategic_planning` | rail | create_plan |

### `memory_and_insights` (5)

| op | source | aliases |
|---|---|---|
| `get_memory` | rail | — |
| `pull_insights` | rail | — |
| `learn_pattern` | rail | detect_pattern |
| `session_activity_query` | rail | what_did_we_create, session_recall |
| `explain_suggestion` | rail | — |

### `assistant_and_conversation` (8)

| op | source | aliases |
|---|---|---|
| `get_identity` | rail | — |
| `get_capabilities` | rail | — |
| `explain_trust` | rail | — |
| `get_feature_info` | rail | — |
| `get_contextual_guidance` | rail | — |
| `greeting` | action_registry | — |
| `farewell` | action_registry | — |
| `thanks` | action_registry | — |

## The judgement calls (Arch rules; each is a one-line move)

1. **`set_default_repo` / `get_default_repo` sit in `repo_activity`**, not `projects_and_repos`. Reason: the default repo is the GitHub context the issue and PR ops run against, and `projects_and_repos` was already at 11 with the portfolio ops. The alternative is a tenth group `preferences` holding these two plus `set_timezone` (3 ops); I left it out because three ops is thin for a stage-1 choice and "set my timezone" reads as a time ask.
2. **`set_timezone` and `get_current_time` sit in `calendar_and_time`.** The one write op in an otherwise read group; the user's phrasing ("set my timezone", "what time is it") is about time, which is the grouping rule in the design record ("what the user is asking about").
3. **`greeting` / `farewell` / `thanks` share `assistant_and_conversation` with the identity and capability ops** rather than a 3-op `conversation` group. Reason: they are the six registry-only canonicals' nearest kin (all about talking to the assistant, none about the user's work), and a separate group would be the smallest by far. If stage-1 error on pleasantries shows up in the corpus run, splitting them out is the first redraft.
4. **`strategic_planning` and `analyze_data` sit in `status_and_priorities`.** Both are "how are things going / what should we do" asks with no object of their own; `documents_and_writing` was the other candidate for `strategic_planning` (it produces a plan) and I chose by the ask, not the output.
5. **`generate_content`, `generate_report`, `write_stakeholder_update` sit with documents** as "drafting". The alternative is a `writing` group of 3.
6. **`changes_query` ("what changed since yesterday") sits in `status_and_priorities`**, not `repo_activity`, because the handler answers across the user's work, not only the repository. If Arch reads the handler as repo-scoped it moves.
7. **`get_feature_info` and `get_contextual_guidance` sit with the assistant ops** (help and guidance), which is where the design record's "help and guidance" bucket went; I merged that bucket into `assistant_and_conversation` to stay at 9 groups.
8. **`search_documents` (Notion search) sits in `documents_and_writing`.** When #2247 lands, Slack search is a sibling here.

## What this cut does to the preregistered isolation test

The three known-bad deltas are `week_calendar` (→ `calendar_and_time`), `attention_query` and `get_project_status` (both → `status_and_priorities`). So the ×6 replay of the `attention_query` example and the `get_project_status` clause exercises **within-group** movement for each other, and isolation across groups is tested against the rest of the corpus. That is still the preregistered pass condition ("no row moves whose stage-1 group differs from the edited op's group"), but Arch should know two of the three deltas share a group before reading the result. If he wants a cross-group pair among the known-bad three, `get_project_status` could move to `projects_and_repos` (which would make it 12); I did not do that, because the status ask is what the user is asking about.

## Build notes for step 1 (after the ruling; no behaviour change)

- `WorkflowEntry` gains `route_group: RouteGroup | None = None`; the ratchet (`tests/test_architecture_enforcement.py`) fails any `action_triggered=True` entry whose `route_group` is `None`, and any value outside the enum. Today's count of routable entries without a group is 66; the ratchet lands at 0 in the same commit that sets them.
- The six registry-only canonicals get a `ROUTE_GROUPS` map beside `ACTION_DESCRIPTIONS` in `action_registry.py`; the same ratchet covers it (6 → 0 missing).
- `derive_routing_grammar()` carries the group on each `RoutingOperation` so stage 1's list derives (constraint 4), and a test asserts the enum's groups partition `grammar.names()` with no empty group.
- The flat prompt does not read the field, so the served router is byte-identical until the two-stage flag exists.

Verified how: `derive_routing_grammar()` run in Lead's venv on main at `4ac5862535` (72 ops); the check script asserts 72 assigned, no duplicates, nothing missing, nothing extra, and prints the sizes above. Layer: a local grammar derivation and repo source; nothing served, no LLM run.
