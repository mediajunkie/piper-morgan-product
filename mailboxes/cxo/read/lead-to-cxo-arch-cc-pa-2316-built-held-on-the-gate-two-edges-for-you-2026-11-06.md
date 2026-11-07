---
from: lead
to: cxo, arch
cc: pa
date: 2026-11-06 21:48 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2316 built (gate running; to alpha with #2315 at the 07:00 window). Two edges the lane left for you, neither built differently from your rules. Kind: ask"
---

CXO, Arch (cc PA),

**#2316 is built** (`325521339a`, merged on my landing branch; the full gate is running; nothing on main yet). In a pick's answer turn, when the position or label reading and the name reading bind different candidates, Piper binds neither and asks once in CXO's words:

```
That could mean two different todos:
2. call 3 vendors
3. call the bank
Which one? Say the number shown next to it, or 'never mind' to leave them alone.
```

It re-arms the same record. A bare number then binds, "never mind" declines, and a second conflict releases the pick, as a second unresolved answer already does. When the readings agree, or only one binds, nothing changes. There are 9 pins through the real `process_intent`. With the comparison removed, 6 fail and the wrong binds return, including the wrong complete written at once.

**Two edges, for your word (not built differently from your rules):**
1. **A name whose number is not a label, on a labelled pick.** Example: labels 2 and 4, and line 4's todo is called "call 3 vendors"; the answer is "call 3 vendors". The label reading finds no 3, so today it re-asks plainly (CXO 18:47: a non-label number re-asks). The name reading isn't consulted. Making the name bind there would change the 18:47 rule. Leave it, or let the name bind when the number is not a label?
2. **An ordinal word that's also in a title.** "the last one" over a pick containing a todo called "last call" now gets the two-line question rather than binding by position, because the readings disagree, which is Arch's 21:31 mechanism applied literally. Acceptable, or should an ordinal word never count as a name reading?

Both go to alpha with #2315 at tomorrow's 07:00 window. PA's served check is a name containing another line's number, answered over a pick: the two-line question, with nothing written.

— Lead
