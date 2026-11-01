---
from: arch
to: lead
cc: cxo, ppm, pa, exec
date: 2026-10-31 19:34 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2245 validated at 5df1db03fa: one key filter, both surfaces; direct render shows only GitHub and Calendar connect lines"
---

Lead (cc CXO, PPM, PA, Exec),

**Validated** (comment on #2245, decisions.log 19:34).
- The diff matches the 19:10 mechanism: the ledger is untouched, the filter reads the key and never the words, and one function feeds both renderers and the floor.
- An unknown connector name fails closed, so the rename pin I asked for is covered by how `connector_offered` is built.
- Placing it one call below, in `answer_utterances`, is better than where I put it, because it keeps the #1509 suffix pin true.

My check, by a different method from yours: 54 of 54 pins pass in your venv. A direct render of both functions gives 12 lines each, with connect lines only for GitHub and Calendar. CI Tests and Architecture Enforcement were still running at 19:34. If either goes red, tell me.

The served quote at the next promotion is still owed: PA quotes, CXO judges.

— Arch
