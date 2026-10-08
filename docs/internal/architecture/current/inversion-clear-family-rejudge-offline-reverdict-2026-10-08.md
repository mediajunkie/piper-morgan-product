# Offline re-verdict of inversion-clear-family-score-2026-10-08-anthropic.md

**No LLM calls.** Router decisions are the RECORDED ones from the source report; only the verdict
is recomputed, against the corpus expectations at this commit, with the scorer's own `router_matches`.
Valid evidence only while the catalog is unchanged since the source run (procedure rule 7).

Served (#1620 — resolved, post-fallback, per row): anthropic:claude-haiku-4-5 (518/518) — recorded in the source report, not re-served
Source: `docs/internal/architecture/current/inversion-clear-family-score-2026-10-08-anthropic.md`
Rows: 2 written · 2 MATCH · 2 with a changed expectation · 0 unreadable route cells skipped · 7 source phrases no longer in the corpus

## Row detail (asserted rows)

| phrase | category | expected | router route @conf | verdict | note |
|---|---|---|---|---|---|
| what are my projects? | PORTFOLIO | action:list_projects | `list_projects` @0.95 | MATCH |  |
| what are my current projects | STATUS | action:list_projects | `list_projects` @0.95 | MATCH |  |
