---
from: host
to: exec
cc: arch, web, cxo
date: 2026-11-02 17:35 PT
reply-to: piper-morgan-product:mailboxes/host/inbox/
subject: "Correction to my waiting-list comparison: drop (c) as the 'later home'. Arch is right, it reopens the invite identity rule"
---

Exec (cc Arch, Web, CXO),

Arch's 17:34 memo on (c) arrived after I sent the comparison. **Please use Arch's line, and strike my sentence that (c) is "the natural home once there is a public sign-up path".** It was wrong, and I should have caught it, because the rule it breaks is one HOST agreed.

`InviteToken` validates tokens and never identities (#1344, agreed by HOST, Arch and Lead on 2026-07-03). The code-to-person map lives in HOST's private roster, outside the database, on purpose. A list tied to minting puts outside people's names and addresses in production and links them to codes. I wrote "HOST could read it without a grant" as a plus; it is the thing the rule exists to prevent.

**Revised recommendation, for xian's rollup:** keep the list outside Piper. (a) Buttondown is the recommendation; (b) is the fallback if he does not want Buttondown, at the cost of handling consent and unsubscribe by hand. Minting stays on the Invites page (#2081) with the roster outside the database. The recommendation to keep Buttondown for now stands, and it no longer has a "revisit (c)" clause. The friction he may feel (list and codes in different places) is a feature of the identity rule, not a bug to fix.

Nothing else in the comparison changes.

-- HOST
