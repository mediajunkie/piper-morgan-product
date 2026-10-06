# Lead standing items — FULL REWRITE 2026-08-31 ~15:5x PT
(Prior version was 53 days stale — CIO's cohort audit caught it, 10 of its 14 cited issues already
closed. Same failure shape as the 8/29 carry-forward staleness; same fix: this file now gets the
freshness pass at START/STOP alongside the carry-forward, and cites NO issue states — issue state
lives in GitHub, this file holds only durable owed/queued items.)

## Durable owed
<!-- 2026-10-05 Lead: struck two rows found already on main during a drain check — the gotchas-doc
     lines (github-and-tooling-gotchas.md §"Four instrument-integrity gotchas", landed 08-31) and the
     _extract_completion_text ratchet gap (frozen in TestExtractionPatternRatchet 2026-09-01). -->
- Pre-claim shadow probe (measurement for the pre-classifier narrowing schedule — PM-ratified
  policy 8/29, build item).
- #1522 false-trails audit — **Filed**: 2026-08-08 · scan DONE 2026-10-05 (table on the issue). Next: inert-deletion lane (C6, C8/C9, I3),
  Arch on `services/persistence/`+migration, CXO/Arch on Places + Documents, Pard/PM on pytest.ini ignore + the Next.js scaffold.
- cli/commands/issues.py guarded-branch cleanup (1613 residue, minor).
- Beta-conditions audit at the final gate (mine + subagent cross-check; PM ruling 8/15).

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
