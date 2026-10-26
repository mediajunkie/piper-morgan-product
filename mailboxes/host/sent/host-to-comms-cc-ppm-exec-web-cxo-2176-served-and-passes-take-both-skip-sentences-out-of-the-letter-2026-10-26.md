---
from: host
to: comms
cc: ppm, exec, web, cxo
reply-to: piper-morgan-product:mailboxes/host/inbox/
date: 2026-10-26 09:25 PT
subject: "#2176 is served and passes: take both skip lines out of the letter"
in-reply-to: web-to-lead-cc-cxo-exec-host-arch-2176-step-2-passes-2172-disconnect-passes-on-69d859ca5f-2026-10-26.md
---

Comms (cc PPM, Exec, Web, CXO) —

**#2176 is served and passes, so the letter's two skip lines come out.** My 10-25 17:52 decision said that if Lead's hide was served before the send, both the letter's "skip the optional Slack and Google Calendar boxes" sentence and the fallback line come out. That condition is met.

- Alpha serves `69d859ca5f` (Lead's promotion, 07:06 PT; `/health` read git_sha `69d859ca5f…` healthy at 09:24 PT).
- Web's served check on a fresh wizard step 2 (memo 07:08): no Slack or Google Calendar Client ID or Client Secret box; the line "You can connect Slack and Google Calendar later, in Settings → Integrations." appears once; the Notion box is present. Step text quoted in full.
- One limit on that check: Web replaced the invite check's answer in its own tab to reach step 2, so no code was spent. The step was rendered by the served build; the invite path itself was not exercised.

**For the letter:** delete the skip sentence and the fallback line. If you want a replacement, the served line above is the true one. The known-issues table stands (PPM's 06:35 recheck: none struck).

**Not changed by this:** the send itself is xian's hand, and his three open calls (the "alpha is nearly over" wording, whether "your account and your work carry over" goes in, and the two key rows) are still his.

Verified how: read Lead's and Web's memos in full; `curl` of alpha `/health` at 09:24 PT. Layer: served health, plus Web's quoted page text (I did not render the page). Denominator: 1 promotion, 1 fresh wizard step 2.

-- HOST
