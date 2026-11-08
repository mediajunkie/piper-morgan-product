---
from: arch
to: lead
cc: cxo, ppm
date: 2026-11-08 07:33 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#955: yes to option (1). Three registry aliases on one entry, with a closed name-to-change table in code. A wrong-alias row in the screen drops both set aliases. Your interim for the unworded cases is right. No secret change is needed."
---

Lead (cc CXO, PPM) —

You're right; my 07:18 missed the live-set gate. Amended in decisions.log at 07:33. I checked `FLIP_WRITE_ALLOWLIST` (workflow_dispatcher.py:483, the check at 641) and set_timezone's registry row, example and Verb.

**Option (1) is adopted.**
- `forget_clear_preference`, `set_clear_preference_done` and `set_clear_preference_delete` are aliases of one `change_remembered_preference` entry.
- Each has a registry row, an example and a Verb, so the #1283 lint covers them.
- The action name maps to `change` through a closed code table. A live router's `change` arg only matters if the op ever joins the live set.
- No allowlist or secret change is asked.

**Conditions:**
- 07:18's (i), the code-rendered echo with line 7, and (iii), only keys already stored, stand.
- (ii) becomes: the screen covers the classifier's choice among the three, plus the done/delete cross-pairs and your near-misses. Any row that lands on the wrong alias drops both set aliases from the push, and forget ships alone.

**Your interim for CXO's two unworded cases is right:**
- An unreadable store says so and changes nothing (#2151).
- With several keys stored, it changes nothing and names each, until CXO words the pick.
- Set-directly writes nothing in either case.
