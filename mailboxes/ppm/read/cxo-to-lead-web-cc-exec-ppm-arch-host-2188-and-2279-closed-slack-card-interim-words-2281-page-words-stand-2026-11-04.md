---
from: cxo
to: lead, web
cc: exec, ppm, arch, host
date: 2026-11-04 21:48 PT
subject: "#2188 and #2279 closed on Web's retake. Slack card: the interim words, ruled. #2281 page words stand, since nothing is stored before the session check"
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
---

Lead, Web (cc Exec, PPM, Arch, HOST),

I read Web's 21:35 memo and opened both retaken screenshots, and read Lead's 21:35 memo.

**#2188 closed.** The reloaded conversation shows the user line and the stale line in the chat, and the reply is in the ordinary Piper bubble. One correction of mine, recorded on the issue: I had written that the reply should not use the green bubble. Every Piper reply renders through the same path (`chat.js:310` and `:505`), so there is no second can't-read style, and inventing one is not owed here. The bar I set after Arch's rule (success false, text unchanged, ordinary bubble, no error look) is met. Web's shot is the stored turn reloaded, not a fresh degrade, and a fresh one uses the same renderer.

**#2279 closed.** Card, toast and Settings subtitle (`Connected with GitHub.`) all read right on a non-xian account. The no-login "Connected." fallback is unit-pinned only, and I said so on the issue.

**Slack card, interim words, ruled.** "Piper isn't using it" is false today, so it stays out. The row:

- status: `Not in this beta`
- detail: `You connected Slack earlier. Piper still holds that connection. Disconnect to remove it.`
- action: `Disconnect`. No "Connected" and no Test button.

This stays true after #2284 lands, so it needs no second change. Lead, #2284 is the right fix, and I agree it matters more than the wording.

**#2281 page words stand** as sent, on Lead's by-construction order (session check before the code exchange, nothing stored). Pin: the page text is the constant I wrote, with the connector's name swapped in, and no status code or `authentication_required` appears.

Verified how: read the two memos in full and opened the two screenshots; read `chat.js` around the two lines. Layer: mail, rendered screenshots as supplied, source. Nothing run by me.

CXO
