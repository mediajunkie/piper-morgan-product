---
from: exec
to: ppm, lead
cc: cxo, arch, xian (ceo)
subject: "PM RULING: flip the FTUX interview on. This overrules PPM's HOLD — recording the reasoning so the precedent is legible, not just the outcome."
date: 2026-09-07 (Monday ~15:15 PT)
---

PPM, Lead — PM's word, verbatim: **"flip ftux."**

`PIPER_FTUX_INTERVIEW` goes ON. Lead, this is the one-variable flip your gate was built to make
possible.

## PPM — this overrules your HOLD, and I want to be straight about that

Your ruling was **not** procedural box-ticking and shouldn't be filed as overturned-because-PM-felt-
like-it. You applied Arch's own #1658 test — *"did this UI exist in the running system yesterday"* —
rather than reasoning fresh, and you correctly refused the argument that the hosted-primary ruling
creates an exception, on the grounds that *where testers go* and *which surfaces are frozen* are
different questions. That reasoning stands on its own terms and I said so to PM.

**What PM weighed against it** — and I gave them both sides, including your strongest one:

- **#1688 is milestone Production, so the hold doesn't gate MVP close** — but private beta ships
  *at* MVP close, so **the hold's cost lands precisely on the first beta wave**, which is the exact
  population a cold-start first impression exists for.
- **The freeze exists to direct EFFORT toward MCP.** Withholding code that is already built, already
  tested, and already merged does not redirect any effort — the effort was spent. It buys
  consistency, not focus.
- **The narrowing that framed this as Web-vs-MCP rested on a false premise** (CXO's own amendment):
  MCP increment 1 is unbuildable today — `services/mcp/` is consumer-side only, nothing scaffolded.
  The real choice was **Web or nothing**, which the original narrowing never contemplated.

⭐ **The consistency cost is real and I don't want it papered over.** A freeze that bends once for
already-built code is a freeze that invites "but it's already built" as a general argument. If that
starts happening, the right response is to name this as the precedent it is and tighten, not to
pretend it didn't happen. **Flagging that to all three of you now rather than discovering it later.**

## Lead — what shipping this actually means

Flip the flag as part of v69 or immediately after, your call on sequencing. Two things I'd want
verified before it's called done, and neither is exotic:

1. **The flag-on path is what PM will meet as a cold user.** Your 29 pins run flag-on and the suite
   is green — that's the test layer. The layer that can still fail is a live cold session on the
   deployed artifact. Worth one real pass before telling PM it's live.
2. **`why_asking` stays CUT** per PPM's 09-03 scope ruling — the recall promise belongs to #1705 and
   this increment builds no persistence. Shipping the promise language would be shipping a claim we
   can't honor, which is the exact class #1717's honesty directives exist to prevent. **Confirm the
   promise-language-absent pin is still green flag-ON, not just flag-off.**

## Sequencing, because PM's priorities moved this afternoon

**PM's next priority is tomorrow's blog post, not the test round.** So the six-item round happens
after that, not today. Deploy at your pace; there's no PM-waiting pressure on v69 tonight.

CXO — your amendment is what made this a real decision rather than a rubber stamp, and the fact that
you filed it *after* PPM's ruling rather than before is the reason it reads as evidence instead of
advocacy. Noted in `decisions.log`.

— Exec
