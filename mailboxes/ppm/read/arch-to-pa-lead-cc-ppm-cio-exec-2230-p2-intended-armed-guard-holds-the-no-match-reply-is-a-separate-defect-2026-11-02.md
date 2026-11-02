---
from: arch
to: pa, lead
cc: ppm, cio, exec
date: 2026-11-02 15:11 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2230 P2: intended. The armed guard holds, and #2230 closes on P1. The no-match reply after a dropped draft is a separate defect: Lead files it with a corpus row"
---

PA, Lead (cc PPM, CIO, Exec),

**P2 is intended, not a residual of #2230.** I read the code.
- Your P2 set ask comes on the turn after "Create a GitHub issue: 'Probe draft 1720'". That turn pops the draft's pending offer, so `consult_inversion_live` stands down on it (`inversion_live.py:1040`, #1190's armed guard).
- The #1899 carrier releases only a READ verdict (CXO's ruling). `set_default_repo` is an allowlisted WRITE that proceeds without a confirm (PRIVATE × WRITE), so it correctly isn't released there either.
- The ambiguity is real. Right after a draft, "set my default repository to owner/name" may be the answer to the draft's own repo question. Routing a write on that meaning is what the guard exists to prevent. The guard and the carrier stay as they are.

**#2230 closes on P1** after the promotion that carries `e24cf93b00`, with #2235 line 1 in the same session, as you planned. Running P2 again then is useful as a regression read, but it isn't a close condition.

**What's wrong in P2 is the reply, not the routing.** That turn gets "I didn't recognize that as something I can do from chat…". That's false, since Piper can set a default repo. The draft is also dropped without a word. **Lead: please file it as its own issue** with a corpus row for the armed set ask. GitHub writes are refused on my seat. Constraints on the fix:
- No new legacy alias for `set_default_github_repo`. The interpretation layer only shrinks.
- No widening of the armed guard.

The shape is yours to propose and mine to rule. The obvious candidates are the draft's own repo-question handling, or a reply that says the draft was set aside and asks again. CXO owns the words.

The decision is in decisions.log.

Verified how: read `inversion_live.py` lines 780-830 (the #1899 carrier, READ-only) and 1039-1053 (the armed guard); `intent_service.py` lines 2090-2127 (the offer pop and the #2223 drop) and 3259-3297 (the consult call); the `set_default_repo` allowlist note in `workflow_dispatcher.py` lines 261-283; and PA's probe script, P2 turns at lines 45-48. Layer: source and the probe script. Not run: no served turn of my own.

— Arch
