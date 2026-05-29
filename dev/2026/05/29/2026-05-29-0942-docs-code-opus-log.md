# Session Log — Docs (Documentation Management) — 2026-05-29 09:42 PT

**Agent**: Claude Code, Opus 4.7 (1M context)
**Role**: Docs (Documentation Management)
**Branch**: main (still on-main; awaiting PM's worktree relaunch sweep per yesterday's cron-vacate)
**Origin**: PM-engaged manual session open (off-cron since 2026-05-28 Fire 17 — on-main cron vacated per ratified "do not register on main"; resume = relaunch in `claude/docs-cycle` worktree)

## Session start (09:42 — PM-engaged)

New day; off-cron (no START cron fire). PM opened with the GitHub Support resolution on the stuck workflow.

## GitHub Actions — Support resolution + verification (09:42)

PM relayed GitHub Support (Arthur, 2026-05-28 21:19 UTC): marked the stuck queued run completed; refreshed schedules; confirmed **"high load can cause delays and dropped events"** for schedule triggers (validates the May 27 forensic diagnosis exactly). Recommended an external scheduler → `workflow_dispatch` via API/CLI for consistent triggering.

**Verification (gh):**
- Stuck run #25923061467 ("Tests", from May 15) → now `completed`/`cancelled` (updatedAt 2026-05-28T21:09Z). ✅ Cleared.
- **Schedules firing again**: `E2E & AAXT Tests` triggered via `schedule` at 2026-05-29T09:32Z. ✅ Trigger fixed.
- **BUT new failure surfaced** (was masked while schedules weren't firing): the run hard-failed in 7s at "Set up job" with:
  `##[error] ...deprecated version of actions/upload-artifact: v3`
  GitHub now auto-fails any workflow referencing `actions/upload-artifact@v3`.

**Scope of the deprecation (grep .github/workflows/):**
- Hard-fails (`upload-artifact@v3`): `e2e-aaxt.yml:298`, `test.yml:415`, `pm034-llm-intent-classification.yml:145,229`
- Already on v4 (good): `dependency-health.yml`, `link-checker.yml`
- Deprecation warnings only (still functional): `cache@v3` + `checkout@v3` across lint/test/ci/windows-test/architecture-enforcement/e2e-aaxt/pm034
- Caveat: `upload-artifact@v3→v4` is a breaking change (immutable artifacts; no same-name re-upload) — not a blind sed; needs Lead Dev judgment.

**Disposition**: filed to Lead Dev (GitHub Actions operational refactor lane). The trigger-drop is resolved; the artifact-deprecation is a separate newly-surfaced fix.

## Carry-over from 2026-05-28

- On-main cron vacated; awaiting PM worktree-relaunch sweep (PM said "I will sweep through tomorrow helping agents get settled").
- #972 MEM-TEMPORAL: 2 design questions gate backfills (attention doc).
- #974 MEM-EVAL pilot data collection ongoing.
- Standing lane: #1058 template hygiene (idle-advanceable).
