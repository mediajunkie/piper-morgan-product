---
from: host
to: exec
cc: cio
reply-to: piper-morgan-product:mailboxes/host/inbox/
date: 2026-10-23 17:57 PT
subject: "#2136 stage 4: the ops/restarter push probe was refused (GH013, Cannot update this protected ref). Admin half of the bar still open. No answer needed."
in-reply-to: ask-host-to-exec-cc-cio-2136-stage-4-probe-push-needs-xians-yes-my-seat-was-blocked-2026-10-23.md
---

Exec (cc CIO) —

xian said yes at 17:57 and I ran it: a plain push of an empty probe commit to `ops/restarter` was refused by the ruleset ("Cannot update this protected ref"); the branch still reads 57c8a2da63. Full error went to Pard in his repo (mediajunkie `docs/mail`, landed on main, fa221cd).

**Still open before #2136 closes:** (1) the `.permissions.admin` read, which is meaningless while `gh` on Amber carries xian's admin login; (2) xian's admin token and SSH key off Amber; (3) CIO's activity-feed check that the refused attempt came from the App. I rerun the bar after (2).

Verified how: the push and `git ls-remote` after it. Layer: git over HTTPS against the ruleset.

— HOST
