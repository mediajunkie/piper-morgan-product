# Offline re-verdict of inversion-week-calendar-listing-only-score-2026-10-06-anthropic.md

**No LLM calls.** Router decisions are the RECORDED ones from the source report; only the verdict
is recomputed, against the corpus expectations at this commit, with the scorer's own `router_matches`.
Valid evidence only while the catalog is unchanged since the source run (procedure rule 7).

Served (#1620 — resolved, post-fallback, per row): anthropic:claude-haiku-4-5 (514/514) — recorded in the source report, not re-served
Source: `docs/internal/architecture/current/inversion-week-calendar-listing-only-score-2026-10-06-anthropic.md`
Rows: 26 written · 23 MATCH · 26 with a changed expectation · 0 unreadable route cells skipped · 7 source phrases no longer in the corpus

## Row detail (asserted rows)

| phrase | category | expected | router route @conf | verdict | note |
|---|---|---|---|---|---|
| link mediajunkie/test-piper-morgan to the project | QUERY | action:link_repo | `link_repo` @0.75 | MATCH |  |
| restore CoVa | PORTFOLIO | action:restore_project | `restore_project` @0.95 | MATCH |  |
| what projects do I have? | PORTFOLIO | action:list_projects | `list_projects` @0.95 | MATCH |  |
| list my archive projects | PORTFOLIO | action:list_archived_projects | `list_archived_projects` @0.95 | MATCH |  |
| Archive my project Test. | PORTFOLIO | action:archive_project | `archive_project` @0.99 | MATCH |  |
| Archive my project "Test" | PORTFOLIO | action:archive_project | `archive_project` @0.99 | MATCH |  |
| Archive the project called Test | PORTFOLIO | action:archive_project | `archive_project` @0.99 | MATCH |  |
| Archive my Test project, please. | PORTFOLIO | action:archive_project | `archive_project` @0.95 | MATCH |  |
| Archive my project called "Test" please | PORTFOLIO | action:archive_project | `archive_project` @0.99 | MATCH |  |
| archive CoVa | PORTFOLIO | action:archive_project | `archive_project` @0.95 | MATCH |  |
| I need to remember to submit my timesheet | TEMPORAL | action:create_todo | `create_todo` @0.95 | MATCH |  |
| what's the most urgent thing | PRIORITY | action:attention_query | `attention_query` @0.95 | MATCH |  |
| what's the most critical thing | PRIORITY | action:attention_query | `attention_query` @0.92 | MATCH |  |
| what is on my calendar | QUERY | action:week_calendar | `week_calendar` @0.85 | MATCH |  |
| what meetings are coming up | QUERY | action:week_calendar | `week_calendar` @0.85 | MATCH |  |
| schedule check for today | TEMPORAL | action:week_calendar | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| when's my next free slot | TEMPORAL | action:week_calendar | `meeting_time` @0.92 | MISMATCH |  |
| what's my available time | TEMPORAL | action:week_calendar | `week_calendar` @0.72 | MATCH |  |
| prs needing review | QUERY | action:list_prs_query | `list_prs` @0.95 | MATCH |  |
| list my active projects for this quarter | STATUS | action:list_projects | `list_projects` @0.92 | MATCH |  |
| what projects am I working on | STATUS | action:list_projects | `list_projects` @0.95 | MATCH |  |
| show today's progress | STATUS | action:session_activity_query | `session_activity_query` @0.85 | MATCH |  |
| connect octocat/hello-world to the project | PORTFOLIO | action:link_repo | `link_repo` @0.85 | MATCH |  |
| add octocat/hello-world to the project | PORTFOLIO | action:link_repo | `CLARIFY` @0.4 | MISMATCH | CLARIFY |
| please show my linked repos | PORTFOLIO | action:list_repos | `list_repos` @0.95 | MATCH |  |
| can you show project repositories for this account | PORTFOLIO | action:list_repos | `list_repos` @0.85 | MATCH |  |
