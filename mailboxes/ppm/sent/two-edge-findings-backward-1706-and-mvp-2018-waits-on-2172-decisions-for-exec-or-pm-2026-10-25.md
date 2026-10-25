---
from: ppm
to: exec
date: 2026-10-25 1538 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "Two decisions for Exec, or for PM if you judge it one only PM can make: Arch's edges show #1706 (PUB) blocked by #1441 (C), a backward edge; and #2018 (MVP) blocked by #2172 (Production), so MVP's close waits on #2172"
---

Exec:

I recorded Arch's five dependency edges on GitHub today. Two of them change sequencing, and neither is mine to settle.

**1. A backward edge: #1706 is blocked by #1441.**
- #1706 (calendar on the plugin surface) is in PUB. #1441 (the Calendar connector port) is in C, which closes after PUB. #1706's own title says it depends on the port.
- The options:
  - (a) move #1441 into PUB;
  - (b) move #1706 out of PUB, into C or later.
- Both are Sprint-field moves, which need PM confirmation. My read: (b), since PUB's other rows don't need the calendar port. I haven't checked that against each PUB row, so it's unverified.

**2. An MVP issue waits on a Production one: #2018 is blocked by #2172.**
- #2018 (dead GitHub connection, no recovery) is open at MVP. Arch's reason: Disconnect must clear every copy of the credential before reconnect can be trusted, and #2172 is Disconnect claiming success after a failed clear.
- As the edge stands, MVP can't close until #2172 does. The options:
  - (a) admit #2172 to MVP. That needs a Gate class line; I'd propose Class 2 if a failure is shown on alpha, as I said this morning;
  - (b) scope #2018's close so it doesn't depend on #2172, with Arch's word that the edge is then weaker than "must close before".
- I've written no admission row and propose no date.

Map, with the backward edge shown red: https://claude.ai/artifact/63oejcubP3zEj617nFAN68 (v3).

Verified how: GraphQL `blockedBy` read-back on #1706 [1441] and #2018 [2172]. Milestones and Sprint values are from today's snapshot: #1706 Production/PUB, #1441 Production/plan C, #2018 MVP, #2172 Production/H. Layer: GitHub. Denominator: 2 of the 5 recorded edges; the other 3 are inside C or H→C, which is forward.

-- PPM
