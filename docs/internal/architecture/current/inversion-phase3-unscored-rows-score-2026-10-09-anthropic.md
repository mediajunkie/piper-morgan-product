# Inversion Phase 3 — the 12 previously-UNSCORED claimed rows, scored 2026-10-09 (Lead)

Twelve single-phrase runs of `scripts/inversion_phase1_shadow_score.py --provider anthropic --phrase …` (one LLM call each),
merged here row-for-row (no row edited). Scope: exactly the claimed rows the deletion gate reported UNSCORED under alpha's
13-token live set (TODO_COMPLETE 11, REPO_MANAGEMENT 1) — rows with NO recorded verdict in any wired report, so this adds
evidence where there was none and swaps nothing (Arch's per-row rule). Same catalog as the 10-08 run.

Served (#1620 — resolved, post-fallback, per row): anthropic:claude-haiku-4-5 (1/1)
router: 12/12 asserted rows scored · 12 LLM calls · 0 ERROR

## Row detail (asserted rows)

| phrase | category | expected | router route @conf | verdict | note |
|---|---|---|---|---|---|
| list my repos on github | PORTFOLIO | action:list_repos | `list_repos` @0.95 | MATCH |  |
| Mark the first three complete and leave the fourth one  | EXECUTION | action:complete_todo | `complete_todo` @0.95 | MATCH |  |
| Mark the first one complete and leave the second one pe | EXECUTION | action:complete_todo | `complete_todo` @0.95 | MATCH |  |
| I want you to clear 'check the test card again,' and 'r | EXECUTION | action:complete_todo | `complete_todo` @0.95 | MATCH |  |
| mark all my reminders done except for 'revise the pr' | EXECUTION | action:complete_todo | `complete_todo` @0.95 | MATCH |  |
| mark the first two complete | EXECUTION | action:complete_todo | `complete_todo` @0.95 | MATCH |  |
| mark #2 as done | EXECUTION | action:complete_todo | `complete_todo` @0.95 | MATCH |  |
| mark todo 3 as complete | EXECUTION | action:complete_todo | `complete_todo` @0.99 | MATCH |  |
| mark 1, 2 and 4 done | EXECUTION | action:complete_todo | `complete_todo` @0.99 | MATCH |  |
| I'm done with the first and the third | EXECUTION | action:complete_todo | `complete_todo` @0.92 | MATCH |  |
| mark the PR review todo as done | EXECUTION | action:complete_todo | `complete_todo` @0.95 | MATCH |  |
| mark everything done except the last one | EXECUTION | action:complete_todo | `complete_todo` @0.95 | MATCH |  |
