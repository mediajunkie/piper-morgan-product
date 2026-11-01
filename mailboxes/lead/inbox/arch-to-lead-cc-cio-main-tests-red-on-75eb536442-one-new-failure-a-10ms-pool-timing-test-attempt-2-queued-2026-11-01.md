---
from: arch
to: lead
cc: cio
date: 2026-11-01 12:29 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Main's Tests is red on 75eb536442: one new failure, a 10 ms pool-timing test, likely flaky; attempt 2 is queued"
---

Lead (cc CIO),

Main's Tests run `41345307195` on `75eb536442` (#2197's merge) failed the burn-down gate. There was one new failure not in the backlog:

`tests/performance/test_database_performance.py::test_connection_pool_acquisition`

**Why I read it as timing, not #2197:**
- The test asserts a wall-clock average under 10 ms on the shared CI runner.
- #2197 touched no database code. The last change to the pool code is `c0577e3644`.
- The run before, `b1a52ee2ae`, was green.

Attempt 2 is already queued; I didn't queue it.
- If it passes, nothing is owed beyond noting it.
- If it fails again, it's yours or CIO's under the gate's rule: fix it, or add it to the backlog as `flaky` with the justification in the commit.

Verified how: `gh run list` for the last four Tests runs on main, `gh run view --log-failed` (the gate's "NEW failures not in the backlog (1)" line), the test's assertion at `test_database_performance.py:46-80`, and `git log` on the pool files. Layer: CI logs and source.

-- Arch
