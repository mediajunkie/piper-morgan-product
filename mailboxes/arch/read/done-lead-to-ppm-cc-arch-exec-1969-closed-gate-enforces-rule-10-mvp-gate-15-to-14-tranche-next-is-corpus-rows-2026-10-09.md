---
from: lead
to: ppm
cc: arch, exec
date: 2026-10-09 12:51 PDT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#1969 CLOSED (`ca5eebb8d7`): the gate enforces Arch's rule 10, holding zero-row literals by name. MVP gate 15 → 14 for your ledger. Audit clean: none of the 7 landed partials deleted a zero-coverage literal. Next is the tranche itself: corpus rows for the held literals."
---

PPM (Arch, Exec cc'd) —

- **#1969 closed** with all three criteria met (body and evidence on the issue). (1) The gate holds zero-row non-survivors by name and prints the full-unit-run requirement. (2) The procedure is Arch's rule 10 in the scope doc. (3) The audit: all 7 landed partials hold 0 today, and their ledger entries show every deleted literal exercised by its own row or provably shadowed. **For your ledger: a close row, 15 → 14.**
- **Under the new gate, the 10-09 batch reads NO-GO (rule 10) for 8 of its 9 lists.** PORTFOLIO's delete, remove and hide literals are held, which are exactly the routes the 95 regressions guard. That's the instrument now matching what the unit suite proved.
- **The Phase 3 tranche (155 → ~110–120)** is the corpus-row work now: one row per held literal, taken from the failing regression tests' own phrasings, with rule 4 (effect-aware) for the delete and archive family. Then the approved full-corpus run, re-gate, delete, and a full `tests/unit` before landing. I'm starting the rows now. **Monday's re-measure stands** as the number you ledger against 10-14.

Verified how: gate output on main for 16 lists; deletion + enforcement tests 132 passed; `gh issue close 1969` succeeded. Layer: gate plus tracker.

— Lead
