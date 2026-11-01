---
from: arch
to: lead
cc: cxo, ppm, exec
date: 2026-11-01 11:28 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2149 removal validated; #2197: CXO's words fit the mechanism, and a tie is two or more indices inside the read"
---

Lead (cc CXO, PPM, Exec),

**#2149 removal (`b1a52ee2ae`): validated.**
- My own flat-render hash on main (`77a0e82da7`) is unchanged: 72 ops, `f2f668adcc59` / `3c10d9533aaa`.
- `git grep` for every removed name and the flag finds 0 hits across `services`, `web`, `scripts`, `tests`, `config` and `.github`.
- 562 router, inversion and usage tests pass.
- The two kept pieces each have a named consumer.

**#2197:** CXO and PPM ruled (A), and CXO's words and pins fit the approved mechanism. One shape detail, so the tie line has something code can see:
- The resolver replies `{"indices": [n, ...]}`, `{"selector": "next"}`, `{"index": null}` or `{"index": null, "named_absent": true}`.
- **Code binds on exactly one index inside the read, and renders CXO's tie line when two or more fall inside it.** It drops any index outside the read. It never works out a tie from confidence or from comparing titles.
- `total = open + closed`, computed in code.
- `due_on` renders as its own date part (CXO's pin: `2026-11-20T00:00:00Z` shows the 20th).
- The named_absent and tie lines are fixed copy, and never quote the model's string.
- The floor never receives the resolved milestone (pinned).

Build when ready. I'll validate the landing against the 11:00 and 11:14 rulings and CXO's pins.

Recorded in decisions.log at 11:28.

-- Arch
