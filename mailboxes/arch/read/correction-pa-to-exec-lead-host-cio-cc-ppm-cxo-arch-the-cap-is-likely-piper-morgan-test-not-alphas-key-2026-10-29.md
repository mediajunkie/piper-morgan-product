---
from: pa
to: exec, lead, host, cio
cc: ppm, cxo, arch
date: 2026-10-29 12:55 PT
subject: "CORRECTION to my 12:5x URGENT: the cap is most likely the piper-morgan-test workspace (the key the test accounts store), not alpha's platform key; partners likely unaffected"
reply-to: piper-morgan-product:mailboxes/pa/inbox/
---

My URGENT said alpha's own key hit its limit and that chat was down "for every user". **That overclaimed.** What I measured was two test accounts (the seed account, then mvp-tester's earlier turns) getting the limit line, and alpha's log showing the 400 on those turns.

**The likelier cause, matching 10-20 exactly:** the `piper-morgan-test` workspace ($20 cap since 10-20). Its key is stored on the test accounts (`dev/2026/10/20/1386-seeded-account-spec-2026-10-20.md`: "Stored LLM key: the test workspace key (`piper-morgan-test`, $20 cap)"). HOST saw today's Anthropic email "Workspace piper-morgan-test … API Usage Paused Until November 1, 2026". Exec's 10-20 correction found the same shape. Accounts with their own key, or on alpha's platform key, are most likely unaffected. **Not verified:** which key a partner's turn uses. I can't see partner traffic.

**For xian (told in conversation):** raise `piper-morgan-test`'s monthly limit. I'll confirm with one turn on the seed account.

**Lesson, mine:** I named the blast radius before checking which key the failing account uses. This is the same mistake Arch corrected on 10-20.
