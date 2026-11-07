# ADR-083 screen batch — preregistration (2026-11-06, Lead)

Written before any request is rendered or submitted. Rulings: Arch decisions.log 11-06 10:48,
16:21, 16:41 (A + C, no B); Exec 16:21 ceiling $10 including one re-run; PPM 16:41 (no #2270 row).
Changes to this file after a submit are a new preregistration, never an edit.

## Arms

| arm | prompt | rows |
|---|---|---|
| A | main's routing prompt, unchanged | the full corpus ×1 (622 + the new rows below) and every sentinel ×6 |
| C | A plus ADR-083's slot: the session block carries `LAST LIST SHOWN: 7 numbered todos` (wording (i), D1a), on every request | the same rows and sentinels |
| C-absent | the slot omitted (no list recorded / expired) | **no requests**: proven by the offline byte-identity pin (C's renderer with no list recorded = A's bytes, every corpus row) |

Model: the served router model, batch API, the same settings as this morning's screen.

## ADR-083 sentinels (×6 on A and on C)

| # | phrasing | source | C's bar |
|---|---|---|---|
| S1 | complete the second one | PA 11-06 09:49 (row 3) | complete_todo with a positional target in ≥ 5/6 |
| S2 | delete the third one | PA 11-06 09:49 (row 5) | delete_todo with a positional target in ≥ 5/6 |
| S3 | delete the second one | PA 11-06 09:49 (row 5) | delete_todo with a positional target in ≥ 5/6 |
| S4 | mark the first one done | ADR-083 (one complete) | complete_todo with a positional target in ≥ 5/6 |
| S5 | remove the last one | ADR-083 (one delete) | delete_todo with a positional target in ≥ 5/6 |
| S6 | what is on my calendar today | ADR-083 (topic switch after a list) | keeps A's label in ≥ 5/6 |
| S7 | delete the first two | PA 11-06 15:43 (#2310; added 15:59 before any run) | delete_todo with a positional target in ≥ 5/6 |

None is a catalog example verbatim (checked against all 72 operations' examples, 11-06 16:52 check, the derived grammar). "Positional target" means the router's args name a position or range (e.g. `targets: ["2"]`, `["1-2"]`, `["last"]`), read from the decision's own args, not inferred.

## C's corpus bar (the 10-30 10:44 clauses, C vs A)

1. A row A reads ≥ 5/6 stays ≥ 5/6 on C.
2. A row A reads ≤ 4/6 stays ≥ A − 1 on C.
3. No row gains a label in ≥ 3/6 that A never produced.

The corpus runs ×1 per arm (this morning's screen shape), so clauses 1–2 apply to the sentinels (×6). For corpus rows they read as: a row matching its expected op on A still matches on C; any row that flips is re-run ×6 on both arms before the verdict (within the re-run budget).

## New corpus rows (scored on A against their written destinations; their own measurement, not ADR-083's gate)

| phrasing | expected | source |
|---|---|---|
| link repo octocat/hello-world to Mobile Redesign | action:link_repo | #2269 3a: `ADOPTED_REPO_LINK_LINE` ("link repo {repo} to <project name>") |
| unlink repo octocat/hello-world from Mobile Redesign | action:unlink_repo | #2269 3a: the unlink sibling line |
| link repo dinp-machine/piper-test-activity to zz share-hide project | action:link_repo | #2271's offered wording (already a corpus row, 11-06) |

`_handle_list_repos`'s "link owner/repo to [project]" shape is already covered by the corpus row "link mediajunkie/test-piper-morgan to the project". #2270's row joins the next screen when its phrasing arrives (PPM 16:41).

## Price

2 × (624 + 7 × 6) ≈ 1,330 requests × $0.00185 ≈ **$2.50**; with one re-run ≈ $5. Exec's ceiling $10. Re-price to Exec before submitting if the rendered count exceeds 1,500.
