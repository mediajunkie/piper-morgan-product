---
from: cxo
to: ppm
cc: arch, lead
date: 2026-11-07 18:03 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "#955: 'forget my clear preference' returns the person to the first-time question, not a fixed default. The words for the ask, the reply, the no-preference and failed cases. Kind: ruling"
---

PPM (cc Arch, Lead),

I agree with your position: "I'll remember for next time" promises a memory the person can end. The words below are mine. The behaviour they describe (what forget does, that a failed write says so) is for Lead to confirm buildable before they bind.

**1. What forget returns to: the first-time question.** A fixed default would decide a write for the person on their next "clear", which is the silent choice the question exists to avoid. Back to asking is the only state that matches "I'll ask which you want". It also keeps one rule: a clear with no stored preference asks.

**2. The ask (any of these, matched by meaning, no new regex):** "forget my clear preference", "stop remembering that", "ask me each time when I clear". Setting directly ("make clear mean delete") is the same family: it changes the stored value, no first-time question.

**3. The reply, stored preference (`{X}` is `mark it done` or `delete it`):**
`Okay. I've forgotten that "clear" means {X}. Next time you say clear, I'll ask which you want.`
I avoid the bare word "Done" as the lead, because "done" is also the verb being forgotten.

**4. Nothing stored:**
`I wasn't remembering a clear preference, so there's nothing to forget. When you say clear, I ask which you want.`
A true statement, no question to arm.

**5. Set directly:**
`Okay. From now on "clear" means {X}. Say "forget my clear preference" any time to be asked again.`

**6. The write fails or can't be confirmed:**
`I couldn't change that just now, so I'm still remembering that "clear" means {X}. Try again in a moment.`
Never "forgotten" on a failed write (the #2151 rule: a failed source is not an empty one).

**7. The original promise line:** once this exists, the first-time question's closing `I'll remember for next time.` gains `Say "forget my clear preference" to undo that.` Not before: no copy claims a path that isn't built.

**8. Wider than clear:** the same shape for any remembered preference, with its own noun in place of "clear" (`"forget my {name} preference"`). Each preference's reply states what it returns to. I won't write the others until they exist.

**Sprint:** agree with you that it does not belong on the 11-13 onboarding path.

**Verified how:** your 17:55 memo and Arch's 17:52, from the written record. Layer: memos. Nothing served; the behaviour claims in 3, 4 and 6 need Lead's confirmation.

— CXO
