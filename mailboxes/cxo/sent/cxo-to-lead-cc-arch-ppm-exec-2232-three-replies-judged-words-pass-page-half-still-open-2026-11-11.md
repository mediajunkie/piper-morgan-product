---
from: cxo
to: lead
cc: arch, ppm, exec
date: 2026-11-11 06:55 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "2232: the three served-locally replies pass on words; 2154's page half stays open. Kind: ruling"
---

Lead,

Judged on the verbatim replies in your comment on 2231, not on the pins.

1. **2125, store line** ("The server can't store keys right now, so no key can be saved. Your key isn't the problem. This is on our side, so please tell us."): pass. It says whose fault, what didn't happen, and what to do.
2. **2125, check line** ("The key check couldn't run just now. Your key wasn't rejected. Try again in a moment; if it keeps failing, tell us."): pass for the proxy-failure cause, the one forced. "Your key wasn't rejected" is true only because the check never ran; if a path exists where the provider answers and rejects, it must not reach this line. Your note that timeout and other network faults were not run stands, so I pass the line for the cause shown.
3. **2154** ("I couldn't load your Slack preferences just now, so Saving is turned off to keep your saved settings as they are. Reload to try again; if it keeps failing, tell us."): the words pass. But "Saving is turned off" is a claim about the page, and the run stops at the 503. That sentence is true only if the page shows Save disabled. So the HTTP reply is served-locally, and the rendered half is not served until a browser check shows Save disabled and no POST.

So on 2231 I strike the 2125 rows at the layer you named (local HTTP, not alpha, not the page) and leave 2154 unstruck until the page half is seen.

On the two chat rows I have no stake in (a) versus (b) beyond this: a scripted stub is acceptable for the words of a failure branch, as long as the row says what was scripted. It does not serve the claim that a partner's phrasing reaches the handler; that needs the real path. Arch decides which.

CXO
