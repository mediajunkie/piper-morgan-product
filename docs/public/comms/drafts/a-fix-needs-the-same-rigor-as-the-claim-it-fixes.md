---
image:
alt:
caption:
---

# A Fix Needs the Same Rigor as the Claim It Fixes

*August 7–11, 2026*

My communications agent (Comms) shipped a tool in early August meant to fix one specific, well-understood problem: a mail-reading script that only recognized one memo format, silently skipping about one in five real messages written in a slightly different style. The fix was a three-tier fallback parser, tested against the full corpus that had exposed the gap, and it came back clean. Zero unparsed. The team adopted it the same day.

Over the next four days, five more people found five more reasons it wasn't actually finished.

# The pattern, one layer at a time

The first two gaps showed up within days: a header variant the fallback logic didn't cover, and a counter that used an "and" where it needed an "or," which meant it could only ever report zero regardless of what it was supposed to be counting. Comms found both, in its own tool, and said so plainly in a day's summary rather than letting either quietly slide into "basically fixed."

Then a third person found a fifth header format entirely — a notation style that didn't share a single structural marker with the previous four. Someone else moved fast to patch it, and while testing that new patch against a deliberately narrow, controlled slice of real messages, caught the patch itself producing sixty-eight false positives where only eighteen were expected. The fix for the fifth gap had introduced a sixth problem, caught before it shipped, only because the person fixing it tested the fix as rigorously as the original bug had been tested.

That's the part worth sitting with. Every single person in this chain was reasonably careful. Nobody shipped something they hadn't tested. And it still took five rounds, because each round's testing covered what that round's fix touched, not the shape of the whole problem.

# Why "it's just a fix" is the trap

There's a natural asymmetry in how much scrutiny a first claim gets versus a fix to that claim. Discovering the original bug earns real investigation — you don't trust "it's probably fine," you trace it, reproduce it, measure the blast radius. A fix to that bug tends to inherit less scrutiny by default, because it feels like the hard part is already done. Someone already found the problem. The fix is just closing the loop.

But a fix is a new claim, not a footnote to the old one. "This resolves the gap" is exactly as falsifiable as "there is a gap" was in the first place, and it deserves the same posture: don't assume it worked because it's supposed to, go check that it actually does, against something at least as demanding as what exposed the original problem.

The saga didn't actually end with someone building a smarter parser. It ended when four different people, on the same day, independently re-verified their own full corpora from scratch rather than trusting that the prior fix had covered everything — the discipline the whole chain had been missing, applied all at once, finally closing the loop for real.

# The rule, stated the way it got named

A colleague put words to it partway through, in a way worth keeping intact: a fix you just wrote carries the same posture-of-rigor problem that a correction does. Not less. Fixing something doesn't retroactively make the original discovery's rigor apply to the fix too — the fix has to earn its own.

That's a small discipline to state and an easy one to skip under time pressure, because "I already found the bug, I'm just patching it now" feels like the hard thinking is behind you. It usually isn't. The bug told you where to look once. The fix is a new claim about a system you now understand slightly less well than you think you do, because you just changed it.

---

*Next on Building Piper Morgan: "The Near-Miss and the Missing Key" — a save-conflict dialog renders an editor completely blank, on bad advice my communications agent (Comms) doesn't withdraw once it's disproven, and the draft survives only because it had already been copied out by hand.*

*The next time you ship a fix, would it survive the same scrutiny you gave the bug it's fixing?*
