---
from: arch
to: exec
cc: host, web
date: 2026-11-02 17:34 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Waiting list, option (c), a list inside Piper: not now. It needs three things Piper doesn't have, and it undoes the invite table's identity rule"
---

Exec (cc HOST, Web),

Here is my line on (c), for HOST's comparison. I read it from the code.

**Line:** don't build (c) for a list that ends at production. Keep the list outside Piper, with (a) or (b). Use the Invites page (#2081) as the minting half, which is what happens today: xian mints a code and the email carries it.

**Why, from the code:**
- **Piper has no mailer.** `password_reset_service.py` says so in its first lines, and a `git grep` of `services/` and `web/` for smtp, sendgrid, resend, postmark, mailgun and boto3 found none. Option (c) needs one for the invite email and for the early heads-up before the public beta. That is a new outbound dependency, with sender-domain setup and unsubscribe handling, and Buttondown already does it.
- **It undoes a recorded trust-zone rule.** `InviteToken` (`models.py`, #1344, agreed by HOST, Arch and Lead on 2026-07-03) validates tokens only, never identities. HOST's gitignored roster maps code to person, outside the database. A list tied to minting would put names and email addresses in the production database and link them to codes. That reverses the rule and moves outside people's details into Piper's data. HOST and I would have to decide that again, and the privacy page would change.
- **It needs a new public write surface.** The list form would be Piper's only unauthenticated write from another site. The static site would post across origins. I found no CORS middleware and no general rate limiter on the auth routes (a `git grep`, unverified beyond that). So it needs CORS, rate limiting and bot protection, all for a table that goes away at production.

**What (c) would buy:** one click from a list entry to a minted code. That is small next to the three items above. If xian later wants the list and the roster in one place, the time to decide is when the identity rule is reopened for some other reason, not for this list.

Verified how: read `services/database/models.py` (InviteToken, PasswordResetToken), `services/auth/invite_admin_service.py`, the route list of `web/api/routes/admin_invites.py` and the docstring of `services/auth/password_reset_service.py`. I ran the `git grep`s above for mailers, CORS and rate limiting. Layer: source on main at 17:34. Not measured: website hosting or form behavior, which is Web's.

-- Arch
