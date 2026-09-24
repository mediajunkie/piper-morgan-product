---
from: scope-guard (automated, arch+cio design, 7t)
to: ppm
subject: "Scope-drift flag(s) from push scan — advisory; verify before acting, the predicate is in its measured period"
date: 2026-09-23
verdict: true-positive
---

Automated flag — machine-written at invocation (m-50-conformant by construction).

```
DRIFT-B #1744 — all 1 acceptance-checkbox(es) are checked, but #1744 is still OPEN. Possible scope drift: verify whether this issue is ready to close.
```

Denominator: scope-drift-check: checked 100 commit(s) in range 'HEAD~10..HEAD', 10 issue reference(s), 1 flagged, at 2026-09-23 23:45

Advisory period: set the `verdict:` line above to `true-positive` or
`false-positive` when you drain this — promotion to a required check reads the
rate from these headers (`grep -h '^verdict:' mailboxes/ppm/{inbox,read}/flag-scope-guard-*.md
| sort | uniq -c`), not a hand-kept tally. An UNSET verdict after drain just means
the count is honestly incomplete, not zero.

**PPM verdict, 2026-09-23 19:22**: `true-positive`. `#1744` is its own declared synthetic test
fixture for the delivery path ("safe to close after the memo lands... deliberately references NO
closure keyword"). Timeline shows it was closed 3x around the scan window (23:03, 23:06, 23:45:43Z
— the last matching the scan timestamp exactly), consistent with active manual close/reopen
testing of the mechanism, not a stale/missed real issue. The flag correctly caught
checklist-complete-while-open at the moment it scanned; state has since resolved (closed) per the
fixture's own instructions. Mechanism worked as designed — no PPM action beyond the verdict.
