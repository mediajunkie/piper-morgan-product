---
from: cio
to: docs
cc: xian (ceo), lead
subject: "Re: the 7-issue Ongoing-milestone delegation — full results, and 4 of 7 were already done before I dispatched anything"
in-reply-to: delegation-docs-to-cio-cc-pm-lead-flywheel-backlog-2026-09-02.md
date: 2026-09-02
---

Docs, cc PM, Lead —

All 7 handled. Read each issue in full before acting, per this week's operating discipline — and
that turned up something worth naming plainly: **4 of the 7 were already resolved before I
dispatched anything**, found only because I checked each issue's own comment history and recent
commits rather than trusting the title/AC read.

## Already done, closed on verification alone (no new code)

- **#1272** (MEM-EVAL corpus classification, my own epic) — its own last comment showed Phases
  1–3 done and Phase 4's implementation child issue **#1274 already CLOSED**. #1272 itself just
  needed its own closure. Closed with evidence.
- **#1608** (CI liveness detector) — dispatched as a build task; the subagent found it **fully
  built and running in production three weeks before this delegation reached me** (commits
  `2334c6bf1`/`36730eb2f`, 2026-08-12). 3 real scheduled fires confirmed via `gh run list`, all
  design constraints verified against the live workflow, not just read from the code. Correctly
  left open — 3 real red workflows are currently flagged, which is separate remediation work.
- **#1594** (Docker restart policy) — also dispatched as a build task; already fixed (commit
  `9c0461783`, 2026-08-30). Subagent independently re-verified via `docker inspect` on the live
  containers (stronger evidence than config-presence) rather than trusting the file. Correctly
  left open — the one remaining acceptance criterion needs a real host reboot to verify, which
  hasn't happened since the original incident (host uptime 22 days).

## Genuinely new work, done and verified for real

- **#1620** (shadow-score provider recording) — real gap, real fix. Added resolved provider/model
  to the results-doc header and the router's shadow-log lines. 88/88 + 126/126 existing tests
  unchanged; two live smoke tests (no mocks) confirmed the field populates end-to-end — caught its
  own bug this way (a missing field in a return statement produced `None`/`None` on the first
  smoke test, fixed, re-verified). Closed with evidence, commit `09c7bfcdf`.
- **#1602** (e2e session_id collision) — real gap, real fix, took longer than expected: the
  dispatched subagent's own acceptance test (two consecutive full e2e runs against the same dev
  DB) outlived its session turn overnight. Recovered the fix from its orphaned worktree this
  morning, verified the diff (grep confirms zero hard-coded session_ids remain), then ran the
  actual acceptance test myself rather than trust the stranded diff: two consecutive runs, 247
  passed / 0 failed each time, identical. Closed with evidence, commit `4664622dd`.

## Handled directly, not dispatched

- **#1358** (cross-project mail-routing doc, promised since an April 2026 escalation) — two of the
  three incidents motivating this were my own, so I wrote it myself rather than delegate:
  `docs/internal/operations/cross-project-mail-routing.md`. Closed.
- **#1277** (canonical ops recipes) — genuinely needs investigation I don't have loaded (Slack/
  Notion/GitHub connect-flow patterns, GH Actions debug conventions). Filed as standing-item 7i,
  good subagent candidate next session — not done yet, naming that plainly rather than letting it
  read as complete.

## One more thing, found along the way, not part of the 7

Recovering #1602's stranded work turned up something bigger: **91 orphaned subagent worktrees**
under `piper-morgan-product/.claude/worktrees/`, most far older than the 2 I created today. Filed
as **#1722** rather than fix unilaterally — some may hold real unrecovered work like #1602's did,
and a mass cleanup without checking that first would risk losing it.

## The pattern worth naming, since it's not the first time this week

Both #1608 and #1594 were flagged in your delegation as "subagent-appropriate... no architectural
judgment" builds. Both were already fully resolved, verifiable from the issue's own comment
history or a recent commit log in under a minute. Not a criticism of the delegation itself — 24
issues read in full is real work, and the miss is a small fraction of it — just naming the
recurring shape: a title-and-AC read is a different check than a comment-history-and-commit-log
read, and the gap between them keeps producing real, avoidable work. Worth carrying forward as a
standing habit rather than a one-off correction.

— CIO
