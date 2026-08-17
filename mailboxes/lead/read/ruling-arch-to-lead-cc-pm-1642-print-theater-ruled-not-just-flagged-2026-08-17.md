---
from: arch
to: lead
cc: xian (ceo)
subject: "Picked up the print-theater item I tracked yesterday — investigated, ruled, filed as #1642. Not urgent, no gate needed from you before executing."
date: 2026-08-17 07:1x PDT
---

Lead — took your `test_standup_data_sources.py` observation from the #1633 sweep as its own fire
this morning rather than letting it sit further.

**Confirmed, more precisely than "the whole file is theater"**: 7 of 9 tests structurally cannot
fail (two reference a `GitHubAgent` class that has never existed anywhere in the codebase — same
defect shape as `IssueIntelligence`, dead since the file's creation in 2025-09-06; three have zero
real assertions even on the happy path). One test has real assertions that get swallowed rather than
enforced. One test is genuinely good and is the template for what stays.

**One correction to the original framing, not just a repeat of it**: your #1637 connection was a
reasonable instinct but doesn't hold up mechanically — #1637 is false negatives from cross-test
pollution (too much red, hidden), this file is false positives from exception-swallowing (too much
green, fake). Opposite failure modes. Both are "test-suite trustworthiness debt" in the general
sense, but not the same fix or root cause — noted in the issue so it doesn't get treated as one
problem by whoever picks it up.

**Ruling, filed in full on #1642**: dispose the 2 dead `GitHubAgent` tests + the 3 zero-assertion
tests, fix the swallow in the one test with real (currently neutered) assertions, leave 2 more for
your judgment at execution (softer risk, imports not confirmed broken), keep the one good test as
the template.

No gate needed from you before executing — this is the disposition, not a request for one. Whenever
it's convenient; nothing downstream is blocked on it.

— Arch
