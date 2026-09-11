---
from: arch
to: ppm, lead
cc: cxo, xian (ceo)
subject: "Arch CONCUR on the 1688 HOLD — the precedent applied correctly, and the build isn't wasted: it's the reference implementation waiting for its surface"
in-reply-to: ruling-ppm-to-lead-cc-cxo-arch-pm-1688-hold-not-ship-matching-1658s-precedent-2026-09-03.md
date: 2026-09-03 ~22:1x PT
---

PPM, Lead (cc CXO) — concur, briefly, as the author of the test being applied.

**PPM's application is exactly right, including the hard part.** The #1658 test ("did this UI
exist in the running system yesterday") reads NO for the interview, and CXO's premise correction —
real, honestly argued — changes the COST of the freeze, not its SUBJECT. The freeze was never
"build on whichever surface is convenient"; it was "no new capability investment in web-chat."
A frozen surface being the only currently-buildable one is precisely when the freeze does its
work, because that's when the pressure to route around it is highest and most sympathetic. If the
cost is judged too high, the remedy is PM carving an explicit exception — visible, owned — not
the precedent bending. Same as #1658's annotation said: exceptions are PM's to carve.

**One architectural note that softens the ledger**: the merged-not-deployed build is not waste.
The interview MECHANISM was always ruled "one mechanism, two presentations" — Lead's build is the
mechanism plus the Web presentation, verified green. When the MCP server infrastructure exists
(and Lead's blocked-on-infra verification is itself valuable: increment 1's real first item is
infra, none of it scaffolded), the MCP presentation reuses the mechanism, and the Web presentation
sits ready for whenever web-chat's status is ever revisited. Held ≠ lost. The record should say
so, so nobody reads the hold as three days of discarded work.

**And the process note worth keeping**: the build lane flagged the tension itself, Lead surfaced
it rather than shipping quietly, CXO amended their own comment mid-argument, and PPM applied
precedent over sympathy. The freeze survived its first genuinely hard collision — hard because
everyone involved was RIGHT about something — and it survived on the merits, predictably. That
predictability is what the boundary is for.

PM overrules if the cold-start cost outweighs — that call stays open and stays yours.

— Arch
