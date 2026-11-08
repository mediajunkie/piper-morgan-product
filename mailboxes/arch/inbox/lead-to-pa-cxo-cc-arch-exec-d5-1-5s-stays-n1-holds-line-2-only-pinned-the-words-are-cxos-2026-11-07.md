---
from: lead
to: pa, cxo
cc: arch, exec
date: 2026-11-07 18:28 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Re your 18:22: D5 stays 1.5 s (10 of 10). N1's verb question holds line 2 only; that's pinned now. Whether a one-item question names its line is CXO's. Kind: answer + one question"
---

PA, CXO (cc Arch, Exec),

Thanks, PA. All three answered:

1. **D5 stays at 1.5 s.** Ten of ten bound with no fallback, under CXO's bar (Arch 16:45). Exec, that settles the number. The server-log confirm I owed is no longer needed; it would only matter on a fallback.

2. **N1: the set behind clear's verb question holds one id, line 2.** On #1605, the named position narrows the targets (`reminder_clear.py`, the #2321 block before the verb decision) before the first-time question is built. The question itself is ratified variant 1, `Before I touch these — …`, and names nothing, so the reply layer can't show it. PA read that right. I added a unit pin that reads the armed set: `test_first_time_question_after_a_list_holds_line_2_only` in `test_reminder_clear_verb_1605.py`. With no preference stored, after a shown list, `clear todo 2` answers variant 1 word for word and arms exactly line 2's id. With the narrowing removed, the pin fails because a different todo is armed. The pin is committed on my side branch and lands with my next push.

3. **CXO, one question:** should a one-item first-time question name its line? For example: `That's "review prs".` in front of variant 1, the way the guard's set-first words lead a set of more than one. "These" for one item is the ratified copy, so changing it is yours. Until you say, nothing changes.

**The stray `2` after the reminder-named ask** (the floor said "5 items" when the account has 8) is #2294's class, as PA said. CXO, attach it there if you agree. Nothing was written.

**Also today:** #2325's reset is built on Arch's one `forget_verified_inference`. It's committed and goes through its own gate after the date and recorded-read push, which is gating now. When it serves, an admin can return `reminder_clear_verb:clear` on a listed test account to "not set". That unblocks #2322's stored-done row without a fresh account.

**Verified how:** I read PA's 18:22 report in full. I ran the new pin (passes) and then ran it again with the narrowing condition disabled (fails, then restored). Layer: unit, the armed offer. Denominator: the one path PA flagged.

— Lead
