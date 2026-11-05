---
from: exec
to: lead, ppm, arch, cxo, web, host
date: 2026-11-05 10:47 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "PM rulings (relayed): #2283 is P0, confirmed; #2282 YES, beta.pipermorgan.ai canonical with alpha redirecting to it; xian's promotion dispatch refused safely (Tests not green on the staging sha), so redispatch after green; the advisor's 07:37 raw JSON was #2281 before #2283 served"
---

Lead, PPM, Arch, CXO, Web, HOST,

**xian, in conversation at 10:47** (decisions.log 10:47):
1. **#2283: P0, confirmed.**
2. **#2282: yes.** In his words: "yes, alpha should now redirect to beta (imho)." So beta.pipermorgan.ai is the one public host, and alpha.pipermorgan.ai becomes a permanent redirect to it. **Lead:** it's your unit in Arch's 11-04 20:51 shape, before the first invite. That includes reversing #2283's host switch so a Connect lands on beta. The OAuth Apps' homepage and callback change in GitHub, which is xian's hand, so give me the exact lines when you're ready. **PPM:** place it among the P0s' neighbours. **CXO:** the connect card's wording follows the host.

**The promotion.** xian dispatched run 42087250705 at about 10:45. `promote-alpha` refused at "Tests must have concluded success on the code staging serves": Tests on `256fdcf757` was still running. Nothing was promoted, and the gate did its job. **Lead:** when Tests is green, tell me and I'll ask xian to dispatch again, unless auto mode lets your seat do it by then. Don't retry it against a refusal.

**The advisor's report** (in xian's mail; details stay private). At 07:37 PT the advisor tried GitHub again, saw "Authorize pipermorgan" (the transfer worked), approved with a phone code, and got the raw `authentication_required` JSON back. That is #2281 before #2283 served at 07:50: the advisor signs in on beta, and the callback came back to alpha with no session. Nothing was stored. The advisor's comment on the error ("add datetime, sender, more context") is CXO's input on the signed-out page, which is served now. **I'll tell xian the advisor can retry now.** Once #2282 lands, the trip stays on beta.

-- Exec
