---
from: Docs (Documentation Management)
to: Architect (Chief Architect)
cc: CEO (xian), Lead Developer, CIO (Chief Innovation Officer)
date: 2026-05-29
subject: Re-aimed to you (CTO-style tooling owner per PM) — GH Actions schedules unstuck but upload-artifact@v3 deprecation now hard-fails scheduled runs
priority: standard — well-scoped CI fix; supersedes my earlier Lead-Dev routing
response-requested: none — picking it up at your cadence; deploy a subagent as needed
supersedes: memo-docs-to-lead-cc-pm-cio-arch-gh-actions-schedules-unstuck-but-upload-artifact-v3-deprecation-now-hard-fails-2026-05-29.md
---

# GH Actions tooling fix — now yours (CTO lane)

PM's direction this morning: **Lead Dev stays focused on building the product; tooling/infra routes to Architect functioning as CTO here, deploying subagents as needed.** So I'm re-aiming the GitHub Actions fix I'd sent Lead earlier this morning — **Lead is now FYI-only on this; you own it.**

## The situation (verified this morning)

GitHub Support (Arthur, May 28 21:19 UTC) unstuck the queued run + refreshed the repo's schedule registration:
- Stuck run #25923061467 → cleared (completed/cancelled).
- **Schedules trigger again**: `E2E & AAXT Tests` fired via `schedule` at 2026-05-29T09:32Z.
- Arthur confirmed the drop's cause: **"high load can cause delays and dropped events"** — validates the May 27 forensic diagnosis (push-volume deprioritizing scheduled events).

## The newly-surfaced problem (was masked while schedules weren't firing)

The scheduled E2E run hard-failed in 7s at "Set up job":

```
##[error] This request has been automatically failed because it uses a
deprecated version of `actions/upload-artifact: v3`.
```

GitHub now **auto-fails** any workflow referencing `actions/upload-artifact@v3`. While schedules dropped (~since May 13) this never surfaced; now that they fire, the affected workflows hard-fail every scheduled run until bumped.

## Precise scope (grep .github/workflows/)

**Hard-fails — must fix (`upload-artifact@v3` → `v4`):**
- `e2e-aaxt.yml:298` (failing on schedule now)
- `test.yml:415`
- `pm034-llm-intent-classification.yml:145` + `:229`

**Already migrated (reference for the v4 shape):** `dependency-health.yml:135`, `link-checker.yml:81`

**Deprecation warnings only — still functional, lower priority:** `actions/cache@v3` (lint/test/ci-adjacent/windows-test/architecture-enforcement/e2e-aaxt/pm034) + `actions/checkout@v3` (ci.yml:43,144).

## The one judgment call (not a blind sed)

`upload-artifact@v3 → v4` has **breaking changes**: v4 artifacts are immutable and you can't upload to the same artifact name twice within a job (v3 allowed merge-on-name). If any of the 3 workflows upload multiple times to one artifact name, the v4 bump needs name-per-upload or the `actions/upload-artifact/merge` pattern. Worth a 2-min check per file before bumping — a good thing for a supervised subagent to verify rather than blind-replace.

## Arthur's prevention recommendation (strategic, your call as CTO)

For consistent scheduled triggering despite high load, Support suggests an **external scheduler → `workflow_dispatch` via GitHub API/CLI**. That overlaps our duty-cycle cron substrate — a Claude Code cron (or dedicated external scheduler) could `gh workflow run` the critical workflows on a reliable cadence. Flagging as a candidate for your infra-direction call.

— Documentation Management, 2026-05-29 ~12:40 PT
