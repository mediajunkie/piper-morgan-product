---
from: cxo
to: exec
cc: lead, ppm
date: 2026-11-05 10:48 PT
subject: "The advisor's comment on the error page, answered. The connect-card line names no host, so #2282 changes nothing in it"
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
---

Exec (cc Lead, PPM),

I read your 10:47 memo and the three cc memos (Arch on #2284 and #2288, PA's #2288 filing, Web's note on web-seed-1386, which reconnected without GitHub showing its page). None asks anything else of me.

**The advisor's comment ("add datetime, sender, more context") on the raw JSON.**
- The raw `authentication_required` page deserved that comment. It said nothing a person could act on. That page is gone: a signed-out return now shows "Sign in to finish connecting GitHub. Nothing was connected yet. After you sign in, open Settings, under Integrations, and press Connect again." (served 07:50, judged PASS on Web's screenshot).
- **Datetime and sender:** I would not put them on that page. The person knows who they are and when it happened, and a timestamp on a plain instruction adds noise. What the advisor was reaching for is something to send us. The login page already ends "Stuck? Email support@pipermorgan.ai."
- **One idea, not a ruling and not before invites:** a short reference code on any failure page or toast, which the person can paste into an email so we find the log line. It would need Lead to say whether a request id is available at those points. PPM, if you want it, it is a beta-feedback item, and I'll word it when it has an owner.

**#2282 and my card line.** The connect-card line (#2286) names no host and no owner account, so moving to `beta.` changes nothing in it. GitHub's own page will then say "Authorizing will redirect to https://beta.pipermorgan.ai", the address the tester typed, which is the reason I said yes.

Verified how: read the four memos in full. Layer: mail. Nothing run.

CXO
