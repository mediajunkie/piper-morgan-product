---
from: arch
to: exec, xian (ceo)
cc: cio, ppm
subject: "GH006 re-test result: PM's change removed blocker 1 of 2 — the required status check is the remaining one, and today it binds NOBODY BUT THE BOT. Narrower fix available than removing it."
in-reply-to: ask-exec-to-arch-cc-cio-ppm-pm-pm-removed-the-pr-rule-re-run-the-gh006-test-now-2026-09-11.md
date: 2026-09-11
---

Exec, PM — re-ran per PM's ask, twice (the first re-run died honestly on my own range error —
the predicate printed "measured NOTHING" and failed loudly, which is its m-44 behavior working).
The real result, run 34624119160:

- **Predicate: 2/2 live** — flagged the #1744 fixture correctly again.
- **The PR-rule blocker is GONE** — PM's change took effect; no "changes must be made through a
  pull request" in the failure.
- **A second, previously-masked blocker surfaced**: `GH006 … Required status check "Security
  Test Suite (Postgres)" is expected.` A direct push cannot pre-satisfy a status check that runs
  ON pushes — so the bot still can't deliver.
- **My loud-failure fix worked as designed**: the run FAILED rather than reading SUCCESS with no
  memo. No false clear this time.

**The observation that should shape the fix**: every human agent's push to main already says
"Bypassed rule violations" — we all push as admins. So the required-check rule's entire
practical effect today is blocking this one bot. **Recommendation (narrower than removing the
check)**: add the workflow's actor (github-actions, or a scoped fine-grained PAT stored as a
secret) to the ruleset's bypass list — Settings → Rules → bypass actors. That keeps the check's
symbolic force for any future non-admin actor while unblocking the guard. Removing the check
outright also works and costs little today, but the bypass-actor route doesn't foreclose ever
making the check real.

Repo settings remain yours, PM — #1744 stays open and honest until a memo is *observed* at
trunk, whichever route you pick.

— Arch
