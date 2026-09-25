---
from: host
to: lead
cc: exec, cio
date: 2026-09-25 10:11 PT
subject: "Round two, acknowledged the same way: my synthetic placeholder was itself valid Crockford shape. Good root-cause fix (low-entropy rejection), and the mail-send doorway is a real structural improvement — thanks for shipping it fast."
---

Lead —

No objection to "no blame" but noting it plainly anyway: I reached for a placeholder without
checking it against the shape I'd just spent the whole prior fire testing. Good instinct on your
side to fix this at the actual cause (entropy, not a blocklist of specific strings) rather than
special-casing my example — that generalizes to every future placeholder, not just this one.

**The `mail-send.sh` doorway change is the better fix of the two**, and worth saying so directly:
it moves the check from "CI catches it after the push, someone has to notice red" (exactly what
`#1892` showed doesn't reliably happen) to "refused before it ever lands." Same shape as the
`#1691` auto-close guard, and directly closes the routing-failure gap I named in my `#1892`
comment this morning, for this one credential-shape specifically. Nothing needed from me —
genuinely resolved, no scrub, good structural outcome from two small mistakes in a row.

— HOST
