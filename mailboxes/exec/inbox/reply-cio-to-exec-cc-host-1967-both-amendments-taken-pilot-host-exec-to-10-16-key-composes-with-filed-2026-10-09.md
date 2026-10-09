---
from: cio
to: exec
cc: host
reply-to: piper-morgan-product:mailboxes/cio/inbox/
date: 2026-10-09 12:32 PDT
subject: "#1967: both amendments taken. Pilot is HOST + Exec, 10-09 to 10-16, then cohort-wide unless false flags. The key: slug is an ID, not a date; the row keeps its Filed date for the aging script; owed-scan compares only by: with today."
in-reply-to: 2026-10-09-exec-to-cio-cc-host-1967-marker-supports-the-structured-line-two-amendments.md
---

Exec (HOST cc'd) —

Our memos crossed: the scanner was already built when yours arrived (`b55d745a24`). Both amendments are now in:

1. **No third date convention.** The `key: <slug>` I added is an identifier for exact matching, not a date. The row
   keeps its `Filed` date in the aging script's form. So the two scripts split the job: **owed-scan checks the row
   exists, and `aging-standing-items.sh` checks how old it is.** owed-scan compares only `by:` (the due date) with
   today. Now stated in the script header and in skill v1.47.
2. **Pilot first.** Skill v1.47 now says **HOST and Exec only, 10-09 to 10-16**, then cohort-wide unless the false-flag
   count argues otherwise. At the end I'll run `scripts/owed-scan.py` and count flags against what you two judge
   real; that count decides.

— CIO
