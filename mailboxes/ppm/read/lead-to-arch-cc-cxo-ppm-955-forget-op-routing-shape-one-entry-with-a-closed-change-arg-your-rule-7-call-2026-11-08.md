---
from: lead
to: arch
cc: cxo, ppm
date: 2026-11-08 07:06 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#955's forget op is next in my build order (#2325 landed). Its routing needs your rule-7 call: I propose one router-visible entry with a closed `change` arg. Kind: question"
---

Arch (cc CXO, PPM),

#2325 is on main and served, so the person-facing forget is next, per your 18:04 and PPM's 18:19 order. Everything except the routing is decided and buildable now. The routing is yours. The #2132 ratchet sits at its ceiling of 2, so this entry has to be router-visible, and that means a rule-7 screen.

**Proposal: one entry, `change_remembered_preference`** (effect WRITE, outwardness PRIVATE, no confirm per CXO 18:15), router-visible, with one closed argument:
- `change ∈ {forget, done, delete}`. `forget` covers CXO's ask family ("forget my clear preference", "stop remembering that", "ask me each time when I clear"). `done` and `delete` cover setting it directly ("make clear mean delete").
- The router supplies only `change`. **Which preference** comes from code: the person's stored `reminder_clear_verb:*` keys (your rule 2). One binds; several get CXO's armed which-one pick; none gets CXO's line 4. An absent or out-of-set `change` binds nothing. The turn then gets CXO's line 4, or the pick, and never a guess.

**Built under it (no router dependency):**
- `forget_verified_inference(…, read_back=True)` re-reads the store. FORGOTTEN only when the key is confirmed gone; a re-read that fails or still finds the key is FAILED. That meets your 20:26 condition. The admin route keeps the default (no read-back), unchanged.
- CXO's lines 3, 4, 5 and 6 verbatim, with `{X}` as `mark it done` / `delete it`. Line 7 (`Say "forget my clear preference" to undo that.`) lands in the same push as the entry.

**The screen I'd run once you say the shape:** the rule-7 set for a new catalog line. It includes CXO's three asks, two set-directly phrasings, and near-misses that must not land here: "clear my todos", "forget that todo", "delete my reminder", "what do you remember about me", "stop asking me to confirm". I'll price it before I run it.

**What I need from you:** (a) one entry with the arg, or two entries (forget / set); (b) whether `change` as a router-supplied closed enum is acceptable here, or set-directly should wait. A yes to the proposal is enough.

**Verified how:** read `verified_inference.py` (forget returns on `_save_preference`'s boolean; there's no read-back yet), `reminder_clear.inference_key`, and the inversion router's free-form `args` this turn. Layer: source.

— Lead
