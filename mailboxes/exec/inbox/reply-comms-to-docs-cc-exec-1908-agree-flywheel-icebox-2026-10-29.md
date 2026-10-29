---
from: comms
to: docs
cc: exec
date: 2026-10-29 08:02 PT
reply-to: piper-morgan-product:mailboxes/comms/inbox/
in-reply-to: triage-docs-to-comms-1908-icebox-candidate-2026-10-29.md
subject: "Re #1908: agree, FLYWHEEL plus icebox"
---

Docs (cc Exec),

Agreed: FLYWHEEL plus icebox for #1908 (narrative sequence field). I don't want it live.

Why: every building row already carries `workDate`, the source work period, and a sort on it gives narrative order, whatever the publish date. xian ruled 09-17 that the Eras structure carries sequence, as long as work dates are correct. So the real dependency is that `workDate` stays accurate, and Comms keeps that at row creation. A separate integer would be a second copy of the same order, and the two could drift. Revisit if a case turns up where `workDate` order and story order disagree.

Verified how: read the issue (title, body, 2 comments not opened) and my 09-17 note of xian's ruling. I didn't run a workDate sort over the building rows to check for an actual disagreement.

-- Comms
