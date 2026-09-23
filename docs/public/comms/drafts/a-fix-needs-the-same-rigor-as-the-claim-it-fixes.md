---
image: ''
alt: ''
caption: ''
---

# A Fix Needs the Same Rigor as the Claim It Fixes

*August 7–11, 2026*

My communications agent (Comms) shipped a tool in early August meant to fix one specific, well-understood problem: a mail-reading script that only recognized one header format for the memos my agents send each other. The tool skipped  about one in five real messages written in a slightly different style. The proposed fix was a three-tier fallback parser, tested against the full corpus that had exposed the gap, and it came back clean. Zero unparsed. The team adopted it the same day. (I don't recall being consulted on the solution or if I did, my suggestion that we standardize the header format fell on deaf ears.)

Over the next four days, five more people found five more reasons the fix didn't do the job.

# One layer at a time

The first two gaps showed up within days: a fourth header variant the fallback logic didn't cover, and a counter that used an "and" where it needed an "or," which meant it could only ever report zero regardless of what it was supposed to be counting. Comms caught both gaps in its own tool, fixed them, and logged the update.

Then another agent found a fifth header format entirely: a notation style that didn't share a single structural marker with the previous four. A fast patch to fix it produced sixty-eight false positives when tested against a deliberately narrow, controlled slice of real messages (where only eighteen were expected). The fix for the fifth gap had introduced a sixth problem, caught before it shipped, thanks to testing.

*I haven't figured out how to minimize or eliminate errors up front but assiduous testing has at least tamed some of the sloppiness.*

# "It's just a fix" is the trap

There's a natural asymmetry in how much scrutiny a first claim gets versus a fix to that claim. Discovering the original bug earns real investigation — you don't trust "it's probably fine," you trace it, reproduce it, measure the blast radius. A fix to that bug tends to inherit less scrutiny by default, because it feels like the hard part is already done. Someone already found the problem. The fix is just closing the loop.

But a fix is a new claim, not a footnote to the old one. "This resolves the gap" is exactly as falsifiable as "there is a gap" was in the first place, and it deserves the same posture: don't assume it worked because it's supposed to, go check that it actually does, against something at least as demanding as what exposed the original problem.

The saga didn't actually end with someone building a smarter parser. It ended when four different people, on the same day, independently re-verified their own full corpora from scratch rather than trusting that the prior fix had covered everything — the discipline the whole chain had been missing, applied all at once, finally closing the loop for real.

# Trying to make it a rule

A fix you just requires the same rigor as the analysis of the original problem. It doesn't inherit that rigor by osmosis.

That's easy to notice and also easy to skip under time pressure, because "I already found the bug, I'm just patching it now" feels like the hard thinking is behind you. It usually isn't. The bug told you where to look once. The fix is a new claim about a system you now understand slightly less well than you think you do, because you just changed it.

---

*Next on Building Piper Morgan: "A Primary Log Can Be Wrong, Not Just Incomplete" — a session log that read as an airtight source turned out to be recording what someone believed happened, not proof that it did.*

*The next time you ship a fix, would it survive the same scrutiny you gave the bug it's fixing?*
