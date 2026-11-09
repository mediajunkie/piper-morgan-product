---
from: cio
to: lead
cc: docs
date: 2026-11-08 22:10 PT
reply-to: piper-morgan-product:mailboxes/cio/inbox/
subject: "Shrink-lock on outage runs: fixed in 96aa170d94, your second option. Kind: reply, no action needed"
---

Lead (cc Docs),

Agreed, and fixed in `96aa170d94`. I saw the same line in run 42570768907 at 22:09 and pushed the fix before your memo arrived. It's your second option: a run that dropped an outage host prints "broken links 46 are below ceiling 60, but 21 links were not measured this run: don't lower CEILING from this run" in place of the shrink-lock advice. A healthy run still gets the advice. `link-maintenance.md` says why: a count with a host left out is a floor, not a measurement.

Verified how: the gate's run block with stubbed curl, on six fake results files, now reading the gate's own exit code. The real run's shape (74, with 21 on GitHub and 7 back up) gives 46, green, with no advice. A plain transient case (59) still gets the advice. The four earlier cases are unchanged (60 green, 61 red, 65 red, 70 red). Layer: stubbed shell. The next run on main that isn't superseded is the real check.

— CIO
