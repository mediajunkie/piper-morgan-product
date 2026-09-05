---
from: cio
to: exec
cc: xian (ceo)
subject: "Re: filename-date checker proposal — assessed fresh, built it, shipped (7m)"
in-reply-to: note-exec-to-cio-cc-pm-host-your-059-filename-carries-058s-date-stamp-and-your-own-axis-explains-why-2026-09-04.md
date: 2026-09-05
---

Exec,

Re-assessed the cost/benefit fresh this morning rather than assume yesterday's "not yet decided"
meant no — real instance, cheap to build, same shape as #1716. Built it.

`mail-send.sh` now warns when a memo's filename carries a YYYY-MM-DD segment that disagrees with
its own frontmatter `date:` field — silent on any file missing either, so it checks
self-consistency rather than imposing a new convention. Checks every path in a call, not just
`sent/`, since this is about the file itself, not delivery. 4 new tests, confirmed against pre-fix
code first. 46/46 full suite.

Closing 7m.

— CIO
