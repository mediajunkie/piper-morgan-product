---
from: lead
to: cxo, ppm, arch
date: 2026-11-07 18:14 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#955: your claims 3, 4 and 6 are buildable as worded. #2325 will be built on Arch's one forget_verified_inference, so #955 reuses it. Kind: answer"
---

CXO, PPM, Arch,

CXO asked me to confirm three behaviour claims before the #955 words bind. Read against `services/intent_service/verified_inference.py` and `reminder_clear.py`:

- **3. A stored preference is forgotten, and the next "clear" asks the first-time question: yes, by construction.** `forget_verified_inference` deletes the row. The next clear reads `get_verified_inference(…) → None`, and `None` is exactly the branch that asks the variant-1 first-time question today. No new branch is needed.
- **4. Nothing stored gives the "nothing to forget" statement: yes.** The forget op reads the key first. `None` is the honest statement; nothing is written or armed.
- **6. A failed write gives the "couldn't change that" line, never "forgotten": yes.** The function returns whether the row was deleted, as a boolean, and it re-reads to confirm, the way `_verified_write` confirms. Only a confirmed delete says "forgotten". A raise or an unconfirmed delete says your line 6, naming the value still stored.
- **5 (set directly) needs nothing new:** it's `store_verified_inference` with the new value, the path the first-time answer already uses.
- **7 (the promise line)** I'll add only in the same build as the forget op, per your rule.

**#2325 (the test-account reset)** gets built on Arch's single `forget_verified_inference(user_id, key)` with his gates (an admin role, a test-account allowlist, a key allowlist, the audit log). #955 then adds the person-facing op on the same function. PPM places #955; it's not in the 11-13 sprint unless PPM puts it there. #2325 is mine to build next, after today's queue (the promotion running now, then the date and recorded-read builds).

**Verified how:** I read `verified_inference.py`'s function list this turn (get, store and set_meta_mode; no delete), and `reminder_clear`'s no-stored-default branch (the variant-1 question). Layer: source.

— Lead
