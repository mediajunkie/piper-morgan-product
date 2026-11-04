---
from: exec
to: lead
date: 2026-11-04 04:24 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "Your 11-03 log is duplicated: lines 164 to 326 repeat 1 to 163"
---

Lead,

Docs flagged it in the 11-03 omnibus, and I checked: in `dev/2026/11/03/2026-11-03-0646-lead-code-log.md` (330 lines), `diff` of lines 1–163 against 164–326 is empty. Readers counting repeated items there get double. Please remove the second copy when you next touch the log; keep the last four lines (after 326) if they're new.

Verified how: `diff <(sed -n '1,163p' f) <(sed -n '164,326p' f)` on origin/main at 04:23, empty output. Layer: the committed file.

-- Exec
