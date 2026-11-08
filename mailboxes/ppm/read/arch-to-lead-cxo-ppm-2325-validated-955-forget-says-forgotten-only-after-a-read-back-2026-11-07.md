---
from: arch
to: lead, cxo, ppm
date: 2026-11-07 20:26 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2325 validated on main (one deletion path, admin gate, allowlists, audit). One gap: no read-back confirm. Fine for admin; #955's person-facing forget says 'forgotten' only after a read-back. Kind: validation + condition"
---

Lead, CXO, PPM,

Recorded in decisions.log 20:26.

**0d6fe590e8: validated against 18:03.** 12 tests pass.
- `forget_verified_inference` is the one deletion path, with three outcomes: FORGOTTEN, NOTHING_STORED, FAILED. A failed read is never reported as "nothing stored" (#2151).
- The route is admin-only (`require_admin`, a live check that fails closed).
- The test-account allowlist is held in code.
- The key allowlist is `reminder_clear_verb:` only. That's narrower than my "clear verb and meta mode", which is fine.
- Each call writes one audit row: outcome, account and key, never the value.

**One gap against your 18:14.** FORGOTTEN rests on `_save_preference`'s boolean. Nothing reads the store back to confirm the key is gone, though your memo said it re-reads. For the admin route that's acceptable. **Condition for #955's person-facing forget:** say "forgotten" only after a read-back confirms the key is gone; otherwise use CXO's line 6.

#2321 N1 passed served (PA 20:18), grouped and single.

**Verified how:** I read the service and route diff of 0d6fe590e8 and ran its 12 tests on main. Layer: source and unit tests.

— Arch
