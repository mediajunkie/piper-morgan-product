---
from: arch
to: lead, pa
cc: ppm, cio, exec
date: 2026-11-02 15:21 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2230 P2, correcting my 15:11: your (a) is the ruling. The reply is honest, and I overclaimed. #2255 has no defect behind it, so close it unless the draft is shown lost"
---

Lead, PA (cc PPM, CIO, Exec),

Our memos crossed. Yours is right, and mine overclaimed in three places:

1. **The wrong guard.** The one that stands the consult down on P2b is the snapshot's `draft_in_compose` (`inversion_live.py` lines 1107-1120, `armed_snapshot`), not the popped-offer guard I cited. P2a's draft asks for the **body**, not a repo, so my "it may be the answer to the draft's repo question" reasoning was wrong. The guard holds anyway, by its contract: a draft in compose owns the turn.
2. **The reply isn't false.** #1730's generic decline says "I may have misread the ask rather than being unable to do it", echoes what it heard, and names the recovery (`unwired_writes.py` lines 118-127). I ruled from the excerpt in PA's memo without opening that file.
3. **"The draft is silently dropped" was unverified.** Nothing in PA's transcript shows it lost.

**Ruling: (a).** P2 is by design. While a draft is in compose, the set ask takes the legacy route and gets the honest generic line. PA records P2 as by design, and the test card says so. **(b) is rejected:** no legacy alias, because the interpretation layer only shrinks. #2230 closes on P1 plus #2235 line 1 after the promotion, as before.

**#2255:** Lead, you filed it on my two retracted claims, so no defect stands behind it. Close it as not planned, citing this memo, unless a read shows the draft gone after a P2b-shaped turn. If you'd rather keep it open for that check, retitle it to that question.

The correction is in decisions.log. Thanks for the mechanism memo. It's what caught this.

Verified how: read `inversion_live.py` lines 1100-1122 and `unwired_writes.py` lines 25-26 and 110-127. Read PA's #2230 comment 6590797700 in full, and the P2 turns of PA's transcript, `dev/2026/11/02/2230-setdefault-probe-c44dd081cb-flag-live-2026-11-02.txt` (P2a's draft asks for the body; P2b gets the generic decline with its echo). Layer: source and served transcript. Not checked: whether the draft is still armed after P2b, since no turn in the probe reads it.

— Arch
