# Lead standing items — FULL REWRITE 2026-08-31 ~15:5x PT
(Prior version was 53 days stale — CIO's cohort audit caught it, 10 of its 14 cited issues already
closed. Same failure shape as the 8/29 carry-forward staleness; same fix: this file now gets the
freshness pass at START/STOP alongside the carry-forward, and cites NO issue states — issue state
lives in GitHub, this file holds only durable owed/queued items.)

## Durable owed
- Gotchas-doc lines (queued): mypy platform skew (macOS±1 on 4 codes vs CI) · reload=False
  dev-server snapshot · restart-by-port procedure (kill by lsof -ti, verify new PID+start-time) ·
  Keychain ACL hang (#1711 tracks the code fix).
- Ratchet-coverage gap: _extract_completion_text not in TestExtractionPatternRatchet's frozen
  surfaces (measure-and-freeze).
- Pre-claim shadow probe (measurement for the pre-classifier narrowing schedule — PM-ratified
  policy 8/29, build item).
- #1522 false-trails audit: fresh scan first, then delegate.
- cli/commands/issues.py guarded-branch cleanup (1613 residue, minor).
- Beta-conditions audit at the final gate (mine + subagent cross-check; PM ruling 8/15).

## Standing disciplines (the ones this file exists to survive compaction)
- One lane at a time in this worktree — NO commits of any kind while a lane is active (hardened
  8/31 after the docs-commit sweep).
- Pinned-ruff (0.6.9) format+check before code-bearing pushes; belt green is per-push discipline.
- Deploys only on PM's explicit word; flag changes to deployed env count.
- Verify awaited items against the ISSUE, not local files; merge origin/main BEFORE inbox listing.
