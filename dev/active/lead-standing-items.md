# Lead standing items — FULL REWRITE 2026-08-31 ~15:5x PT
(Prior version was 53 days stale — CIO's cohort audit caught it, 10 of its 14 cited issues already
closed. Same failure shape as the 8/29 carry-forward staleness; same fix: this file now gets the
freshness pass at START/STOP alongside the carry-forward, and cites NO issue states — issue state
lives in GitHub, this file holds only durable owed/queued items.)

## Durable owed
<!-- 2026-10-05 Lead: struck two rows found already on main during a drain check — the gotchas-doc
     lines (github-and-tooling-gotchas.md §"Four instrument-integrity gotchas", landed 08-31) and the
     _extract_completion_text ratchet gap (frozen in TestExtractionPatternRatchet 2026-09-01). -->
- Pre-claim shadow probe — **Filed**: 2026-08-29 · the INSTRUMENT is built (09-02: `preclaim_shadow.py` + `scripts/preclaim_shadow_report.py`,
  default OFF). What remains is the MEASUREMENT: enable `PIPER_PRECLAIM_SHADOW=1` where real claimed turns happen (alpha — PM's hand,
  a flag change to a deployed env) or run a local traffic pass, then read the report per pattern list against the 1.0 bar. Not a build item
  any more (corrected 2026-10-06 — the row said "build item" for five weeks after the build landed).
- #1522 false-trails audit — **Filed**: 2026-08-08 · scan DONE 2026-10-05 (table on the issue) · inert-deletion lane (C6, C8/C9, I3) DONE
  `b3f684822f` · dual-write/`get_github_repository` DONE 10-06 (`e394c6e084`). Places removed 10-06 (`d06e81186b`). `services/persistence/`
  deleted 10-07 (prod row count 0; migration `p1522drop`). Still open: Documents HELD on #1270, Pard/PM on pytest.ini ignore + the Next.js scaffold, I2 error pages (product call).
- cli/commands/issues.py guarded-branch cleanup (1613 residue, minor).
- Beta-conditions audit at the final gate (mine + subagent cross-check; PM ruling 8/15).
- **Post-promotion served checks on alpha** — **Filed**: 2026-10-08 · Blocked on: PM's next `promote_to_alpha`. Quote each served
  answer (rule 8): "delete the first two reminders"; #1959 close of a nonexistent issue (honest reply, no confirm); #1889/#1963/#1964
  (#1965 a+b landed 10-08: quote the served standup + Radar for an OAuth-only account AND a PAT-only account, the latter on its
  owner's own PAT that PM provisions, never a Piper-held one; CXO closes #1889/#1963 on the quoted output); if PM turns on the `clear_todos` token, PM's 08-15 sentence first.

- **Next catalog change's full run — named rows** (Arch 2026-10-08) — **Filed**: 2026-10-08. Batch into the NEXT rule-7 run, never a
  dedicated one: `week_calendar` description clause "the user's own calendar only; never a team's, a shared or another person's
  calendar" ADDED to CXO's 10-06 clause (not replacing it); checklist rows: "show the team calendar" (expected floor, known live miss
  in the TEMPORAL ledger), then CXO's served floor probe (pass = says it can only see the user's own calendar; never invents a team's).
  Also rides the same run (PPM 10-08, still parked): `get_project_status` x2, `get_top_priority` "what now", the non-ledgered `floor`
  rows. NOT in it: the four GUIDANCE/PRIORITY re-points (landed by PPM, expectation-only); "advise me on this decision" (stays on
  the rail); "let's analyze the risk here" (live ANALYSIS survivor; CXO reopens only on a served reply that invents or blames).

## Sequenced from Arch's aging-items route (2026-08-31)
- #973 MEM-CACHE-AUDIT Phase 1 (96d): queue position — after the corpus tag-pass lands and PM's
  next test round clears; the June blockers Arch cites are confirmed cleared.
- #1459: next after #973 (Arch's route memo in read/ has the detail; sequencing mine, action later).

## Standing disciplines (the ones this file exists to survive compaction)
- One lane at a time in this worktree — NO commits of any kind while a lane is active (hardened
  8/31 after the docs-commit sweep).
- Pinned-ruff (0.6.9) format+check before code-bearing pushes; belt green is per-push discipline.
- Deploys only on PM's explicit word; flag changes to deployed env count.
- Verify awaited items against the ISSUE, not local files; merge origin/main BEFORE inbox listing.
