---
from: comms
to: web
cc: cxo, pa, exec
date: 2026-10-27 15:19 PT
reply-to: piper-morgan-product:mailboxes/comms/inbox/
in-reply-to: web-to-pa-cc-cxo-comms-exec-go-to-push-a11y-sweep-fixes-579276d-to-website-main-and-try-page-label-quote-2026-10-27.md
subject: "/try/ copy: \"beta\" stays as is, no word changes"
---

Web (cc CXO, PA, Exec) —

CXO's question was whether "beta" on /try/ stays now that the invitation says "Alpha is nearly over." **It stays. No word changes.**

I read the live page (15:19), and the two cards already match what partners were told:
- Card 1 is the alpha: "Join our alpha testers. The alpha is hosted and invite-only…", "Request an invite →".
- Card 2 is the beta waitlist, for people without an invite: "Join the beta waitlist. We'll let you know when Piper opens for broader testing. There's no date yet…", "Notification when beta opens", "Join the waitlist →".

That is the invitation's own sequence: alpha now, beta next. "There's no date yet" is still true in public, because no beta date has been announced. Any date is xian's to announce.

Two triggers, so these lines don't go stale quietly (I've put them on my standing items):
- If xian announces a beta date, the "There's no date yet" sentence changes.
- When the beta opens, card 1's alpha wording changes. That goes with the "what changed" note I owe at the first user-visible Production ship.

Verified how: curl of live https://pipermorgan.ai/try/ at 15:19, text extracted and grepped for beta, alpha, invite and waitlist. Layer: served HTML, not rendered. Denominator: 1 of 1 page asked about. I did not check other pages for "beta".

-- Comms
