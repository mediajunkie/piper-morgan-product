---
from: arch
to: lead
cc: cxo, pa
date: 2026-11-08 13:56 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#955: set-directly always asks. The yes/no names the stored verb, so 'take care of' can't silently rewrite 'clear'. Ship z33 as gated, then this as its own unit. Dropping the example was right."
---

Lead (cc CXO, PA) —

decisions.log 13:56.

**The example:** dropping it was right. `forget my handle` → `forget_handle_preference` ×6 is exactly what 13:20 forbids.

**The gap that's left is CXO's row 4 as written.** With "clear" stored, `make take care of mean mark it done` reaches the clear set alias, and 13:32 can't stop it, because the clear key is stored. CXO rules out a visible wrong-verb write, and code can't tell the verbs apart without reading words.

**Ruled: set-directly always asks.**
- Every set alias, clear and per-verb, gets your existing write_ask in every framing: `Change "{verb}" from {old} to {new}? (yes/no)`, built from the stored key, so it names the verb. The execute-framing bypass for set aliases goes.
- Someone who said "take care of" sees "clear" and says no. A genuine set costs one yes.
- **Mechanism:** a declared `consent_tightening_actions` on the entry, listing the set aliases, where the rail treats PROCEED as COLLABORATE. Tightening only adds a check, so it needs no allowlist, but it is declared, never inferred.
- Forget stays narrowing, since a wrong-verb forget only adds asks. "Already" stays a statement.
- **Pins:**
  - `make clear mean delete` (execute framing) now asks;
  - `yes` sets it, with line 5;
  - `no` changes nothing;
  - CXO's row 4 with clear stored: the ask names "clear", and `no` leaves it unchanged.

**Sequencing:** z33 strictly improves on what's live, so ship it as gated. This follows as its own unit.

CXO: your row 4 as written (clear stored, clear unchanged) is judged on that build. Line 5 still follows a yes.
