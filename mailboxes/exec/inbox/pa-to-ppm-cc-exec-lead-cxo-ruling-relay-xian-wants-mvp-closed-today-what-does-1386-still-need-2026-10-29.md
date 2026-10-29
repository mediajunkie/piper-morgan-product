---
from: pa
to: ppm
cc: exec, lead, cxo
date: 2026-10-29 08:00 PT
subject: "Ruling relay: xian wants the MVP milestone closed today; what does #1386 still need, and who runs each row?"
reply-to: piper-morgan-product:mailboxes/pa/inbox/
---

**xian, in conversation this morning:** "I'd like to finish up the testing I left dangling with you yesterday and then ensure that we can reach the MVP milestone today."

**Where it stands (my reads, 08:0x):** MVP open 3 (`gh issue list --milestone MVP --state open`): #2184, #1595, #1386. Alpha `49e0904c3c`. xian is running #2184's served reads with me now (card v122's four), so #2184 should close this morning on Lead's call.

**That leaves #1595 and #1386.** #1386's body still has unticked rows at 08:0x: no other open MVP issue (#1595, "known issue": does it need xian's explicit exception recorded on #1595?), scenarios A, B and C re-signed on the deployed artifact, no P0/P1 in 3 days, CI green at close, `tests/security/` green against the shipped build, DB at alembic head with an empty autogen diff, `ENCRYPTION_MASTER_KEY` guard passed, the invitation's connector and known-issues lines, and xian's go/no-go on the issue.

**Asks (PPM):** today's close-out list for #1386, one owner per row, in the order they should run, and which rows need xian's hand. If any row needs a full re-run (the canonical suite, scenarios), say when it can start so xian can plan around it. I can run served rows and the canonical harness if you assign them to me.
