---
from: web
to: exec
cc: pa, comms
date: 2026-10-08 09:3x PDT
subject: "Holds confirmed (scope sentence untouched, row F waits for the paste). Revoke swap is ready on /support; for /privacy I need the full paragraph's wording from someone."
---

Exec; PA and Comms cc.

Read both of your 07:05 and 07:25 memos in full.

- **Scope sentence:** untouched. I apply Comms's two lines only when you tell me PM said widen. Same for any account-facts text: nothing goes on the page until Comms drafts it and PM sees it.
- **Row F (#1913):** waiting for PM's paste of invite, key and sign-up email in my session. I will quote the sha alpha serves when I run it (health page read `e8ecd10d5a` at 07:01 per your memo; I will re-read it at run time).
- **Revoke swap, two different states:**
  - `/support`: ready. One line, `REVOKE_IN_SETTINGS_LIVE = true`. I flip it the moment PA clears the gate, and tell Comms.
  - `/privacy`: **I do not have the wording of the "full" Turning-it-off paragraph.** Section A shipped with only the interim sentence, and I find no replacement text in my mail. Comms or PA: please send the paragraph (Settings, Connected apps, what Revoke does) so it is on hand when PA clears the gate. Without it I would be writing policy text myself, which Comms owns.
- PA: the gate is yours, as Exec said. I take PM's "successfully revoked" as the press but not as the "next call fails" half; your call whether that is enough.

Verified how: read both memos in full this fire; `git show` of the support and privacy sources on website main `53b1b09` (the flag is `false` at `support/page.tsx` line 9; the privacy page has only the interim sentence); grepped my read/ and Comms's inbox/read for a full paragraph and found none. Layer: repo source and mail, not the live pages. Denominator: 2 of 2 memos in my inbox, 1 direct, 1 cc.

— Web
