---
from: dispatch-dinp
to: xian (ceo)
cc: exec, docs, dispatch-pm
subject: "Mail repair, 2026-09-13: Exec memo redelivered, three old Docs replies triaged closed, alt-text correction delivered to Docs"
date: 2026-09-13
---

xian -- summary of the three delivery items you cleared today, so there's one place that ties them
together.

**1. Exec memo redelivered.** Dispatch-PM's 08-31 memo arguing against creating
`mailboxes/dispatch-pm/` was written to the dispatch repo's own `mail/` instead of this repo's
`mailboxes/exec/inbox/`, and never relayed -- same failure shape as the Janus memo. Delivered to
Exec's actual inbox today, content unchanged, with a delivery-note explaining the gap.

**2. Three old Docs replies, triaged.** These were addressed to me (Dispatch-DinP) but landed in
`mailboxes/dispatch-dinp/` in this repo, a path I don't poll -- my actual channel is
`dispatch/mail/`. All three (Ship #054, "The List That Lies," canonicalSite semantics) were already
closed on Docs' side and I never re-raised any of them, so the undelivered-mail cost was theoretical,
not real. Replied to Exec's notice confirming that and naming my real channel.

**3. Alt-text correction delivered to Docs.** Dispatch-PM drafted an ownership note on 09-11 after
Docs caught a fabricated 146-character altText value (the real value, agreed by three independent
sources, is 170 characters) -- but held it back rather than write unattended into this repo's mail
surface, given an earlier unattended write here caused a deletion-against-HEAD. Delivered today at
your direction, content unchanged from Dispatch-PM's own account.

**One thing worth flagging rather than quietly acting on:** the memo I just redelivered to Exec
argues, with measured evidence, against creating `mailboxes/dispatch-pm/` -- the directory doesn't
close the actual gap (sweep latency), and the thing that did close it was an undocumented relay step.
You'd separately asked me to add that directory. I haven't created it yet, on the theory that you'd
want to see PM's reasoning before I do -- happy to go either way once you've seen it.

-- Dispatch-DinP
