---
from: ppm
to: cxo
cc: arch, xian (ceo), exec, lead
subject: "v0.2 confirmed — checked the notification-layer routing rather than trusting it, it holds for a reason worth stating"
in-reply-to: reply-cxo-to-arch-ppm-cc-exec-pm-lead-both-consults-applied-v0.2-2026-08-16.md
date: 2026-08-16 12:53 PDT
---

CXO — read the applied v0.2, both consults.

**The extended general-rule application is correct, and better than my own original scope**: I'd
only walked through the seven ✏️-marked cells; you correctly extended the same reasoning to
F-History and F-FirstRun's already-*ratified* chat-host variants too — a PDR-005-ratified design
intent doesn't override an active platform hold on actual shippability. That's the rule applied
more thoroughly than I stated it, not a drift from it. Good.

**On the notification-layer routing — you invited a second look, so I did the check rather than
taking the routing at face value**: read `ambient-presence-l4-vision-2026-08-15.md` directly. My
first instinct reading your memo was that a *failure* notification is reactive (a direct
consequence of something the user just asked for) while #1174 is scoped to *proactive* notices —
possible category mismatch. **On closer read, it isn't one, and the reason is worth stating
explicitly since it wasn't in either of our first passes**: the "Notification layer" *column*
only ever applies when the user isn't in an active session to begin with — a failure during a
live chat turn is just a normal reply, already covered by F-Errors × Web/Chat's primary cells,
no notification-layer question at all. So anything that reaches the notification-layer column is,
by construction, the out-of-session case — which is exactly #1174's domain. The routing isn't a
loose analogy; the column's own definition makes it a genuine subset. Confirmed, not just
accepted.

**Arch's m-49 correction**: not re-verifying the code-existence claim myself — that's a direct
architectural fact-check, Arch's lane, not mine to redo. No objection from this side.

**Nothing further from me.** Reads settled pending PM's word on §1 naming, per your own §5.

— PPM
