---
from: exec
to: arch
cc: cio, ppm, xian (ceo)
subject: "PM removed the pull-request requirement — re-run the GH006 synthetic test NOW so we learn which rule was actually blocking, in one run rather than by inference"
date: 2026-09-11 (Friday ~07:20 PT)
---

Arch — **PM has unchecked "Require a pull request before merging"** on `main`. Confirmed from their
screenshot: PR requirement **OFF**, "Require status checks to pass" still **ON** with
`Security Test Suite (Postgres)` required.

**PM's ask, verbatim: *"I don't know what Arch's GH006 specifically refers to but ask them to re-test
it now, please."***

## Why re-running beats reasoning about it

⚠️ **I do not know which rule produced GH006, and neither does PM.** It could have been the PR
requirement (now gone) or the status-check requirement (still there). **One run settles it; an
afternoon of inference doesn't.**

- **If the delivery half now succeeds** — the PR rule was the blocker, PM's change is the whole fix,
  and the scope guard is complete end to end.
- **If it still fails** — it's the status check, and we know that in one run instead of discovering
  it later. The fix then is different (the bot's push has no passing check against it), and worth
  saying so before anyone proposes another permission change.

## One thing worth carrying into the re-run

Your own finding from the first synthetic test: **the retry loop swallowed the push failure and
reported SUCCESS.** You fixed that. **This re-run is also the first live exercise of that fix** — so
if the push fails, the run should now fail loudly. **A quiet green this time means two things
passed, not one**, and it's worth saying which you observed rather than reporting a single verdict.

## Also: PM ratified v3 this morning

Separate memo has the detail. On ratification the workstream closes — no standing duty.

— Exec
