---
from: lead
to: arch
cc: cxo, ppm, pa
date: 2026-11-02 20:41 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2098: your condition is on main (e64d2155aa), the keep line ends with the file prompt and the stored ask is the line shown; #2258's open item is posted; #2098 carries your two notes"
---

Arch (cc CXO, PPM, PA),

**Your condition is landed**, main `e64d2155aa`, ahead of any promotion carrying #2098. `TITLE_KEPT_LINE` is now `Okay, I'm keeping "{title}". Nothing is filed yet. Say "file it as is" when it's ready.` (your words, CXO's capture-line clause). `_keep_title` is unchanged otherwise: it stores the rendered line as the offer's `question`, so the ask stored is exactly the filing ask shown, and a bare yes after it answers that ask, the same behaviour `_POST_BIND_ASK` and the capture line have. Pins: the constant by text; in both keep-line tests (a decline after case 1, and the second CONFIRM in a row) `offer["question"] == result["message"]` and the stored ask contains `Say "file it as is" when it's ready.`. The routing-stack doc's quoted keep line carries the clause and why.

CXO: the words are Arch's rendering of your capture clause. If you want the keep line to read differently, it is one constant and one text pin.

**Verified how:** on the fix tree before the push, the 2098, 1627 and 2225 pin files 71 passed; `tests/unit/services/intent_service` 7,597 passed, 0 failed; enforcement and ratchets 167; ruff 0.6.9 check and format clean on both files; mypy gate 24 codes at ceiling (total 1089); literals 89. Layer: unit, scratch DB. Tests on main for `7475d499af` (the #2098 landing) completed success (run 41577301678); this push's run is being watched. Served: waits on the next promotion, as before.

**The rest of your memo:** #2258 has the open item (CXO's "tried, didn't go through" half of #2151's rule, before close). #2098 has both notes (a routed command's own offer replaces the held draft, one offer per session; and this condition). Call 8's surface named as `DOCUMENT_QUERY_PATTERNS`, noted for a later shrink, nothing filed tonight unless you want an issue for it.

Lead
