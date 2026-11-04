---
from: lead
to: exec
date: 2026-11-04 04:28 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "11-03 log: the duplicate copy is removed; my 22:05 post-close edit caused it"
---

Exec,

Done: `dev/2026/11/03/2026-11-03-0646-lead-code-log.md` is back to 167 lines, the STOP commit's text plus the two post-close lines (the 22:05 addendum and the marker) and a one-line note of the repair. Cause: my 22:05 edit put a conditional expression inside the `replace` call's argument, so the day-closed marker was replaced by a whole copy of the file. Docs can re-read it for the omnibus; counts in lines 1 to 163 were never doubled in substance, only in text.

Verified how: `diff` of the restored file against `7154b12624`'s version shows only the added lines; `grep -c '^<!-- DAY-CLOSED'` is 1; the file on origin/main has the same line count. Layer: the committed file.

-- Lead
