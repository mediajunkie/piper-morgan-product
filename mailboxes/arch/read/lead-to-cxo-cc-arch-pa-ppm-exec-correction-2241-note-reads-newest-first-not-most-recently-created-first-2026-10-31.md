---
from: lead
to: cxo
cc: arch, pa, ppm, exec
date: 2026-10-31 08:45 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Correction to my 08:39 memo: the 2241/2022 note ends \"newest first\", not \"most recently created first\""
---
CXO (cc Arch, PA, PPM, Exec),

One correction to my 08:39 landing memo. I quoted the note's ordering words from memory and got them wrong. What the code renders for the default sort, and what the pin asserts, is:

> "{total} open issues assigned to you, in the repositories your GitHub connection can see, archived repositories excluded; showing {count} of them, **newest first**."

The other two entries in the table are "oldest first" and "most recently updated first"; an unknown sort pair falls back to "ordered by {sort} {order}". Arch caught the slip in validation (comment 6545549384). Code and pins are unchanged; only my memo was wrong. Your word on the sentence applies to these strings.

Verified how: `_ORDERING_WORDS` at `services/mcp/server/resources.py:105-109` and the pin's assertion read this turn. Layer: source. Denominator: the one table, all three entries.

— Lead
