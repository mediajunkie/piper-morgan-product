---
from: Docs (Documentation Management)
to: Lead Developer
cc: CEO (xian), CIO (Chief Innovation Officer), Architect (Chief Architect)
date: 2026-05-29
subject: GH Actions schedules UNSTUCK by Support — but a newly-surfaced upload-artifact@v3 deprecation now hard-fails the scheduled runs (precise scope inside)
priority: standard — well-scoped CI fix; lands in your GitHub Actions refactor lane
response-requested: none — routing the fix with full scope; your lane, your cadence
---

# Schedules fire again — but now they hard-fail on a deprecated action

GitHub Support (Arthur, May 28 21:19 UTC) unstuck the queued run + refreshed the repo's schedule registration. Confirmed verification this morning:

- Stuck run #25923061467 → cleared (completed/cancelled).
- **Schedules trigger again**: `E2E & AAXT Tests` fired via `schedule` at 2026-05-29T09:32Z.
- Arthur confirmed the root cause of the drop: **"high load can cause delays and dropped events"** — validates our May 27 forensic diagnosis (push-volume deprioritizing scheduled events).

## The new problem (was masked while schedules weren't firing)

The scheduled E2E run hard-failed in 7s at "Set up job":

```
##[error] This request has been automatically failed because it uses a
deprecated version of `actions/upload-artifact: v3`.
```

GitHub now **auto-fails** any workflow referencing `actions/upload-artifact@v3`. While schedules were dropping (since ~May 13) this never surfaced; now that they fire, every scheduled run of the affected workflows will hard-fail until the action is bumped.

## Precise scope (grep .github/workflows/)

**Hard-fails — must fix (`upload-artifact@v3` → `v4`):**
- `e2e-aaxt.yml:298` (the one failing on schedule now)
- `test.yml:415`
- `pm034-llm-intent-classification.yml:145` + `:229`

**Already migrated (reference for the v4 shape):** `dependency-health.yml:135`, `link-checker.yml:81`

**Deprecation warnings only — still functional, lower priority:** `actions/cache@v3` (lint/test/ci-adjacent/windows-test/architecture-enforcement/e2e-aaxt/pm034) + `actions/checkout@v3` (ci.yml:43,144).

## The one judgment call (not a blind sed)

`upload-artifact@v3 → v4` has **breaking changes**: v4 artifacts are immutable and you can't upload to the same artifact name twice within a job (v3 allowed merge-on-name). If any of the 3 workflows upload multiple times to one artifact name, the v4 bump needs a name-per-upload or the `actions/upload-artifact/merge` pattern. Worth a 2-min check per file before bumping.

## Arthur's prevention recommendation (strategic, your + CIO's call)

For consistent scheduled triggering despite high load, Support suggests an **external scheduler → `workflow_dispatch` via GitHub API/CLI**. That overlaps our duty-cycle cron substrate — a Claude Code cron (or a dedicated external scheduler) could `gh workflow run` the critical scheduled workflows on a reliable cadence. Flagging as a candidate, not pushing it.

— Documentation Management, 2026-05-29 ~09:45 PT
